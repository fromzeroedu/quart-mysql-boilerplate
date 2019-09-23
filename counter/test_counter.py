import pytest
from quart import current_app
from sqlalchemy import select

from counter.models import counter_table


@pytest.mark.asyncio
async def test_initial_response(create_test_client, create_all):
    response = await create_test_client.get("/")
    body = await response.get_data()
    assert "Counter: 1" in str(body)


@pytest.mark.asyncio
async def test_second_response(create_test_app, create_test_client, create_all):
    response = await create_test_client.get("/")
    body = await response.get_data()
    assert "Counter: 2" in str(body)

    # check on the model itself
    async with create_test_app.app_context():
        conn = current_app.sac
        counter_query = select([counter_table.c.count])
        result = await conn.execute(counter_query)
        result_row = await result.first()
        count = result_row[counter_table.c.count]
        assert count == 2
