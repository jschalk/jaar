from src.f09_brick.brick_config import (
    get_quick_bricks_column_ref,
    get_brick_sqlite_type,
    # get_brick_table_build,
)
from src.f09_brick.brick_models import (
    br00000HoldTable,
    br00001HoldTable,
    br00002HoldTable,
    br00003HoldTable,
    br00004HoldTable,
    br00005HoldTable,
    br00011HoldTable,
    br00012HoldTable,
    br00013HoldTable,
    br00019HoldTable,
    br00020HoldTable,
    br00021HoldTable,
    br00022HoldTable,
    br00023HoldTable,
    br00024HoldTable,
    br00025HoldTable,
    br00026HoldTable,
    br00027HoldTable,
    br00028HoldTable,
    br00029HoldTable,
    br00036HoldTable,
    br00040HoldTable,
    br00041HoldTable,
    br00000StageTable,
    br00001StageTable,
    br00002StageTable,
    br00003StageTable,
    br00004StageTable,
    br00005StageTable,
    br00011StageTable,
    br00012StageTable,
    br00013StageTable,
    br00019StageTable,
    br00020StageTable,
    br00021StageTable,
    br00022StageTable,
    br00023StageTable,
    br00024StageTable,
    br00025StageTable,
    br00026StageTable,
    br00027StageTable,
    br00028StageTable,
    br00029StageTable,
    br00036StageTable,
    br00040StageTable,
    br00041StageTable,
)
from sqlalchemy import inspect


def check_holdtableclass(brick_number: str, HoldTable_class):
    # ESTABLISH / WHEN\
    mapper = inspect(HoldTable_class)

    # THEN
    assert HoldTable_class.__tablename__ == f"{brick_number}_hold"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    for brickref_column in brickref_columns:
        x_column = mapper.columns.get(brickref_column)
        failed_assert_str = f"{brickref_column=} is missing from TableModel {HoldTable_class.__tablename__}"
        assert x_column is not None, failed_assert_str
        column_type = get_brick_sqlite_type().get(brickref_column)
        if column_type == "TEXT":
            column_type = "VARCHAR"
        elif column_type == "REAL":
            column_type = "FLOAT"
        failed_assert_str = f"Table '{brick_number}' {x_column=} {column_type=}"
        assert str(x_column.type) == column_type, failed_assert_str

    assert len(mapper.columns) == len(brickref_columns)


def test_HoldTable_HasCorrectAttrs():
    check_holdtableclass("br00000", br00000HoldTable)
    check_holdtableclass("br00001", br00001HoldTable)
    check_holdtableclass("br00002", br00002HoldTable)
    check_holdtableclass("br00003", br00003HoldTable)
    check_holdtableclass("br00004", br00004HoldTable)
    check_holdtableclass("br00005", br00005HoldTable)
    check_holdtableclass("br00011", br00011HoldTable)
    check_holdtableclass("br00012", br00012HoldTable)
    check_holdtableclass("br00013", br00013HoldTable)
    check_holdtableclass("br00019", br00019HoldTable)
    check_holdtableclass("br00020", br00020HoldTable)
    check_holdtableclass("br00021", br00021HoldTable)
    check_holdtableclass("br00022", br00022HoldTable)
    check_holdtableclass("br00023", br00023HoldTable)
    check_holdtableclass("br00024", br00024HoldTable)
    check_holdtableclass("br00025", br00025HoldTable)
    check_holdtableclass("br00026", br00026HoldTable)
    check_holdtableclass("br00027", br00027HoldTable)
    check_holdtableclass("br00028", br00028HoldTable)
    check_holdtableclass("br00029", br00029HoldTable)
    check_holdtableclass("br00036", br00036HoldTable)
    check_holdtableclass("br00040", br00040HoldTable)
    check_holdtableclass("br00041", br00041HoldTable)


def check_stagetableclass(brick_number, StageTable_class):
    # ESTABLISH
    mapper = inspect(StageTable_class)

    # WHEN / THEN
    assert StageTable_class.__tablename__ == f"{brick_number}_stage"
    src_type_column = mapper.columns.get("src_type")
    assert src_type_column is not None
    assert str(src_type_column.type) == "VARCHAR"
    src_path_column = mapper.columns.get("src_path")
    assert src_path_column is not None
    assert str(src_path_column.type) == "VARCHAR"
    src_sheet_column = mapper.columns.get("src_sheet")
    assert src_sheet_column is not None
    assert str(src_sheet_column.type) == "VARCHAR"


def test_StageTable_HasCorrectAttrs():
    check_stagetableclass("br00000", br00000StageTable)
    check_stagetableclass("br00001", br00001StageTable)
    check_stagetableclass("br00002", br00002StageTable)
    check_stagetableclass("br00003", br00003StageTable)
    check_stagetableclass("br00004", br00004StageTable)
    check_stagetableclass("br00005", br00005StageTable)
    check_stagetableclass("br00011", br00011StageTable)
    check_stagetableclass("br00012", br00012StageTable)
    check_stagetableclass("br00013", br00013StageTable)
    check_stagetableclass("br00019", br00019StageTable)
    check_stagetableclass("br00020", br00020StageTable)
    check_stagetableclass("br00021", br00021StageTable)
    check_stagetableclass("br00022", br00022StageTable)
    check_stagetableclass("br00023", br00023StageTable)
    check_stagetableclass("br00024", br00024StageTable)
    check_stagetableclass("br00025", br00025StageTable)
    check_stagetableclass("br00026", br00026StageTable)
    check_stagetableclass("br00027", br00027StageTable)
    check_stagetableclass("br00028", br00028StageTable)
    check_stagetableclass("br00029", br00029StageTable)
    check_stagetableclass("br00036", br00036StageTable)
    check_stagetableclass("br00040", br00040StageTable)
    check_stagetableclass("br00041", br00041StageTable)
