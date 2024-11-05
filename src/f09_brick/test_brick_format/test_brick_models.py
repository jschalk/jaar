from src.f02_bud.bud_tool import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_itemunit_str,
    bud_item_awardlink_str,
    bud_item_reasonunit_str,
    bud_item_reason_premiseunit_str,
    bud_item_teamlink_str,
    bud_item_healerlink_str,
    bud_item_factunit_str,
)

# from src.f04_gift.atom_config import (
#     get_normalized_bud_table_build,
#     normal_table_name_str,
#     normal_specs_str,
#     columns_str,
#     sqlite_datatype_str,
# )
from src.f09_brick.brick_config import (
    get_quick_bricks_column_ref,
    get_brick_sqlite_type,
    # get_brick_table_build,
)
from src.f09_brick.brick_models import (
    br00000Table,
    br00001Table,
    br00002Table,
    br00003Table,
    br00004Table,
    br00005Table,
    br00011Table,
    br00012Table,
    br00013Table,
    br00019Table,
    br00020Table,
    br00021Table,
    br00022Table,
    br00023Table,
    br00024Table,
    br00025Table,
    br00026Table,
    br00027Table,
    br00028Table,
    br00029Table,
    br00036Table,
    br00040Table,
    br00041Table,
)
from sqlalchemy import inspect


def check_all_columns_exist(mapper, brickref_columns: set[str], brick_number: str):

    for brickref_column in brickref_columns:
        x_column = mapper.columns.get(brickref_column)
        failed_assert_str = (
            f"{brickref_column=} is missing from TableModel {brick_number}"
        )
        assert x_column is not None, failed_assert_str
        column_type = get_brick_sqlite_type().get(brickref_column)
        if column_type == "TEXT":
            column_type = "VARCHAR"
        elif column_type == "REAL":
            column_type = "FLOAT"
        print(
            f"{brick_number=} {brickref_column=} {get_brick_sqlite_type().get(brickref_column)=} {column_type=}"
        )
        failed_assert_str = (
            f"Table '{brick_number}' {x_column=} {str(x_column.type)==column_type=}"
        )
        assert str(x_column.type) == column_type, failed_assert_str

    assert len(mapper.columns) == len(brickref_columns)


# def print_out_expected_class_attribute_declarations(config_category):
#     config_table_name = get_config_table_name(config_category)
#     config_columns = config_category.get(columns_str())

#     print(f"Table {config_table_name}")
#     for config_column, column_dict in config_columns.items():
#         declare_type = column_dict.get(sqlite_datatype_str())
#         if declare_type == "TEXT":
#             declare_type = "String"
#         elif declare_type == "INTEGER":
#             declare_type = "Integer"
#         elif declare_type == "REAL":
#             declare_type = "Float"
#         if config_column == "uid":
#             declare_type = "Integer, primary_key=True"
#         print(f"    {config_column} = Column({declare_type})")


def test_br00000Table_Exists():
    # ESTABLISH
    brick_number = "br00000"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00000Table)

    # WHEN / THEN
    assert br00000Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00001Table_Exists():
    # ESTABLISH
    brick_number = "br00001"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00001Table)

    # WHEN / THEN
    assert br00001Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00002Table_Exists():
    # ESTABLISH
    brick_number = "br00002"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00002Table)

    # WHEN / THEN
    assert br00002Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00003Table_Exists():
    # ESTABLISH
    brick_number = "br00003"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00003Table)

    # WHEN / THEN
    assert br00003Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00004Table_Exists():
    # ESTABLISH
    brick_number = "br00004"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00004Table)

    # WHEN / THEN
    assert br00004Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00005Table_Exists():
    # ESTABLISH
    brick_number = "br00005"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00005Table)

    # WHEN / THEN
    assert br00005Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00011Table_Exists():
    # ESTABLISH
    brick_number = "br00011"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00011Table)

    # WHEN / THEN
    assert br00011Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00012Table_Exists():
    # ESTABLISH
    brick_number = "br00012"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00012Table)

    # WHEN / THEN
    assert br00012Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00013Table_Exists():
    # ESTABLISH
    brick_number = "br00013"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00013Table)

    # WHEN / THEN
    assert br00013Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00019Table_Exists():
    # ESTABLISH
    brick_number = "br00019"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00019Table)

    # WHEN / THEN
    assert br00019Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00020Table_Exists():
    # ESTABLISH
    brick_number = "br00020"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00020Table)

    # WHEN / THEN
    assert br00020Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00021Table_Exists():
    # ESTABLISH
    brick_number = "br00021"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00021Table)

    # WHEN / THEN
    assert br00021Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00022Table_Exists():
    # ESTABLISH
    brick_number = "br00022"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00022Table)

    # WHEN / THEN
    assert br00022Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00023Table_Exists():
    # ESTABLISH
    brick_number = "br00023"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00023Table)

    # WHEN / THEN
    assert br00023Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00024Table_Exists():
    # ESTABLISH
    brick_number = "br00024"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00024Table)

    # WHEN / THEN
    assert br00024Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00025Table_Exists():
    # ESTABLISH
    brick_number = "br00025"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00025Table)

    # WHEN / THEN
    assert br00025Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00026Table_Exists():
    # ESTABLISH
    brick_number = "br00026"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00026Table)

    # WHEN / THEN
    assert br00026Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00027Table_Exists():
    # ESTABLISH
    brick_number = "br00027"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00027Table)

    # WHEN / THEN
    assert br00027Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00028Table_Exists():
    # ESTABLISH
    brick_number = "br00028"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00028Table)

    # WHEN / THEN
    assert br00028Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00029Table_Exists():
    # ESTABLISH
    brick_number = "br00029"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00029Table)

    # WHEN / THEN
    assert br00029Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00036Table_Exists():
    # ESTABLISH
    brick_number = "br00036"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00036Table)

    # WHEN / THEN
    assert br00036Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00040Table_Exists():
    # ESTABLISH
    brick_number = "br00040"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00040Table)

    # WHEN / THEN
    assert br00040Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)


def test_br00041Table_Exists():
    # ESTABLISH
    brick_number = "br00041"
    brickref_columns = get_quick_bricks_column_ref().get(brick_number)
    mapper = inspect(br00041Table)

    # WHEN / THEN
    assert br00041Table.__tablename__ == brick_number
    check_all_columns_exist(mapper, brickref_columns, brick_number)
