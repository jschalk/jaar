from src.f09_brick.brick_config import (
    get_quick_bricks_column_ref,
    get_brick_sqlite_type,
    get_brick_numbers,
)
from src.f09_brick.brick_models import get_brick_holdtables, get_brick_stagetables, Base
from src.f09_brick.examples.brick_env import brick_env_setup_cleanup, brick_examples_dir
from sqlalchemy import inspect, create_engine, MetaData


def test_get_brick_holdtables_ReturnObj():
    # ESTABLISH / WHEN
    x_brick_holdtables = get_brick_holdtables()

    # THEN
    assert set(x_brick_holdtables.keys()) == get_brick_numbers()


def test_get_brick_stagetables_ReturnObj():
    # ESTABLISH / WHEN
    x_brick_stagetables = get_brick_stagetables()

    # THEN
    assert set(x_brick_stagetables.keys()) == get_brick_numbers()


def check_sqlalchemytableclass(
    tableclasses_dict: dict[str,], table_type: str, extra_columns: dict[str, str]
):
    for brick_number, SqlAlchemyTable in tableclasses_dict.items():
        # ESTABLISH
        mapper = inspect(SqlAlchemyTable)

        # WHEN / THEN
        assert SqlAlchemyTable.__tablename__ == f"{brick_number}_{table_type}"
        for x_column, column_type in extra_columns.items():
            _check_sqlalchemycolumn(x_column, mapper, SqlAlchemyTable, column_type)

        brickref_columns = get_quick_bricks_column_ref().get(brick_number)
        for brickref_column in brickref_columns:
            _check_sqlalchemycolumn(brickref_column, mapper, SqlAlchemyTable)

        assert len(mapper.columns) == len(brickref_columns) + len(extra_columns)


def _check_sqlalchemycolumn(
    brickref_column: str, mapper, SqlAlchemyTable, column_type: str = None
):
    x_column = mapper.columns.get(brickref_column)
    failed_assert_str = (
        f"{brickref_column=} is missing from TableModel {SqlAlchemyTable.__tablename__}"
    )
    assert x_column is not None, failed_assert_str
    if column_type is None:
        column_type = get_brick_sqlite_type().get(brickref_column)
    if column_type == "TEXT":
        column_type = "VARCHAR"
    elif column_type == "REAL":
        column_type = "FLOAT"
    failed_assert_str = (
        f"Table '{SqlAlchemyTable.__tablename__}' {x_column=} {column_type=}"
    )
    assert str(x_column.type) == column_type, failed_assert_str


def test_HoldTable_ClassesHaveCorrectAttrs():
    # ESTABLISH / WHEN / THEN
    check_sqlalchemytableclass(get_brick_holdtables(), "hold", {})


def test_StageTable_ClassesHaveCorrectAttrs():
    # ESTABLISH
    extra_columns = {
        "src_type": "VARCHAR",
        "src_path": "VARCHAR",
        "src_sheet": "VARCHAR",
    }
    # WHEN / THEN
    check_sqlalchemytableclass(get_brick_stagetables(), "stage", extra_columns)


def test_Base_create_all_CreatesTables_Scenario0_InMemory():
    # ESTABLISH
    engine = create_engine("sqlite://")

    # WHEN
    Base.metadata.create_all(engine)

    # THEN
    # Create a MetaData object and reflect the database schema
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # List all tables in the database
    tables = metadata.tables
    assert len(tables) == 56


def test_Base_create_all_CreatesTables_Scenario1_File(brick_env_setup_cleanup):
    # ESTABLISH
    engine = create_engine(f"sqlite:///{brick_examples_dir()}mydatabase2.db")

    # WHEN
    Base.metadata.create_all(engine)

    # THEN
    # Create a MetaData object and reflect the database schema
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # List all tables in the database
    tables = metadata.tables
    print("Tables in the database:")
    # for table_name in tables:
    #     print(table_name)

    assert len(tables) == 56
