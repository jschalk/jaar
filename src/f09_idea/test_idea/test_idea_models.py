from src.f09_idea.idea_config import (
    get_quick_ideas_column_ref,
    get_idea_sqlite_types,
    get_idea_numbers,
)
from src.f09_idea.idea_models import get_idea_holdtables, get_idea_stagetables, Base
from src.f09_idea.examples.idea_env import idea_env_setup_cleanup, idea_examples_dir
from sqlalchemy import inspect, create_engine, MetaData


def test_get_idea_holdtables_ReturnObj():
    # ESTABLISH / WHEN
    x_idea_holdtables = get_idea_holdtables()

    # THEN
    assert set(x_idea_holdtables.keys()) == get_idea_numbers()


def test_get_idea_stagetables_ReturnObj():
    # ESTABLISH / WHEN
    x_idea_stagetables = get_idea_stagetables()

    # THEN
    assert set(x_idea_stagetables.keys()) == get_idea_numbers()


def check_sqlalchemytableclass(
    tableclasses_dict: dict[str,], table_type: str, extra_columns: dict[str, str]
):
    for idea_number, SqlAlchemyTable in tableclasses_dict.items():
        # ESTABLISH
        mapper = inspect(SqlAlchemyTable)

        # WHEN / THEN
        assert SqlAlchemyTable.__tablename__ == f"{idea_number}_{table_type}"
        for x_column, column_type in extra_columns.items():
            _check_sqlalchemycolumn(x_column, mapper, SqlAlchemyTable, column_type)

        idearef_columns = get_quick_ideas_column_ref().get(idea_number)
        for idearef_column in idearef_columns:
            _check_sqlalchemycolumn(idearef_column, mapper, SqlAlchemyTable)

        assert len(mapper.columns) == len(idearef_columns) + len(extra_columns)


def _check_sqlalchemycolumn(
    idearef_column: str, mapper, SqlAlchemyTable, column_type: str = None
):
    x_column = mapper.columns.get(idearef_column)
    failed_assert_str = (
        f"{idearef_column=} is missing from TableModel {SqlAlchemyTable.__tablename__}"
    )
    assert x_column is not None, failed_assert_str
    if column_type is None:
        column_type = get_idea_sqlite_types().get(idearef_column)
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
    check_sqlalchemytableclass(get_idea_holdtables(), "hold", {})


def test_StageTable_ClassesHaveCorrectAttrs():
    # ESTABLISH
    extra_columns = {
        "src_type": "VARCHAR",
        "src_path": "VARCHAR",
        "src_sheet": "VARCHAR",
    }
    # WHEN / THEN
    check_sqlalchemytableclass(get_idea_stagetables(), "stage", extra_columns)


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
    assert len(tables) == 58


def test_Base_create_all_CreatesTables_Scenario1_File(idea_env_setup_cleanup):
    # ESTABLISH
    engine = create_engine(f"sqlite:///{idea_examples_dir()}/mydatabase3.db")

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

    assert len(tables) == 58
