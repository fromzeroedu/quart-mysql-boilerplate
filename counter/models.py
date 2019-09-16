from sqlalchemy import Table, Column, Integer, MetaData

metadata = MetaData()

counter_table = Table(
    "counter",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("count", Integer),
)
