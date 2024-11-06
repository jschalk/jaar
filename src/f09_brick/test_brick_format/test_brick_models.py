from src.f09_brick.brick_config import (
    get_quick_bricks_column_ref,
    get_brick_sqlite_type,
    get_brick_numbers,
)
from src.f09_brick.brick_models import get_brick_holdtables, get_brick_stagetables
from sqlalchemy import inspect


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
    brick_number: str, SqlAlchemyTable, table_type: str, extra_columns: dict[str, str]
):
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
    for brick_number, HoldTable in get_brick_holdtables().items():
        check_sqlalchemytableclass(brick_number, HoldTable, "hold", {})


def test_StageTable_ClassesHaveCorrectAttrs():
    # ESTABLISH
    extra_columns = {
        "src_type": "VARCHAR",
        "src_path": "VARCHAR",
        "src_sheet": "VARCHAR",
    }
    # WHEN / THEN
    for brick_number, StageTable in get_brick_stagetables().items():
        check_sqlalchemytableclass(brick_number, StageTable, "stage", extra_columns)
