from quart import Blueprint, current_app
from sqlalchemy.sql import select

from counter.models import counter_table

counter_app = Blueprint("counter_app", __name__)


@counter_app.route("/")
async def init():
    conn = current_app.sac
    counter_query = select([counter_table])
    result = await conn.execute(counter_query)
    count = None

    if result.rowcount == 0:
        stmt = counter_table.insert(None).values(count=1)
        result = await conn.execute(stmt)
        await conn.execute("commit")
        count = 1
    else:
        row = await result.fetchone()
        count = row[counter_table.c.count] + 1
        stmt = counter_table.update(None).values(count=count)
        result = await conn.execute(stmt)
        await conn.execute("commit")
    return "<h1>Counter: " + str(count) + "</h1>"
