import pytest
from sqlalchemy import create_engine
from quart import current_app
from sqlalchemy import select

from counter.models import metadata as CounterMetadata, counter_table

# Create this tests' models
@pytest.fixture
def create_all(create_db):
    print("Creating Models")
    engine = create_engine(create_db["DB_URI"] + "/" + create_db["DATABASE_NAME"])
    CounterMetadata.bind = engine
    yield CounterMetadata.create_all()
    print("Destroying models")
    CounterMetadata.drop_all()


@pytest.mark.asyncio
async def test_initial_response(create_test_client, create_all):
    response = await create_test_client.get("/")
    body = await response.get_data()
    assert "Counter: 1" in str(body)


@pytest.mark.asyncio
async def test_second_response(create_test_client, create_all):
    # first hit
    response = await create_test_client.get("/")
    body = await response.get_data()

    # second hit
    response = await create_test_client.get("/")
    body = await response.get_data()
    assert "Counter: 2" in str(body)

    # check on the model itself
    async with create_test_client.app.app_context():
        conn = current_app.sac
        counter_query = select([counter_table.c.count])
        result = await conn.execute(counter_query)
        result_row = await result.first()
        count = result_row[counter_table.c.count]
        assert count == 2
        print("Count", count)

    print("done")
