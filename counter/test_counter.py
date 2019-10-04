import pytest
from quart import current_app
from sqlalchemy import create_engine, select

from counter.models import counter_table, metadata as CounterMetadata

# Create this tests' models, needs a module scope
# to inherit from the model-level connection
@pytest.fixture(scope="module")
def create_counter_tables(create_db):
    engine = create_engine(create_db["DB_URI"] + "/" + create_db["DATABASE_NAME"])
    CounterMetadata.bind = engine
    CounterMetadata.create_all()


@pytest.mark.asyncio
async def test_initial_response(create_test_client, create_counter_tables):
    response = await create_test_client.get("/")
    body = await response.get_data()
    assert "Counter: 1" in str(body)
