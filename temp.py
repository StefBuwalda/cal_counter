from application import db, app
from sqlalchemy import MetaData, Table

with app.app_context():
    table_name = "_alembic_tmp_food_item"
    engine = db.engine
    metadata = MetaData()
    metadata.reflect(bind=engine)

    if table_name in metadata.tables:
        tmp_table = Table(table_name, metadata, autoload_with=engine)
        tmp_table.drop(engine)
        print(f"Table '{table_name}' dropped.")
    else:
        print(f"No table named '{table_name}' found.")
