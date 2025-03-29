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
from src.f04_stand.atom_config import (
    get_normalized_bud_table_build,
    normal_table_name_str,
    normal_specs_str,
    columns_str,
    sqlite_datatype_str,
)
from src.f04_stand.normal_models import (
    BudTable,
    AcctUnitTable,
    MemberShipTable,
    ItemTable,
    AwardLinkTable,
    ReasonTable,
    PremiseTable,
    TeamLinkTable,
    HealerLinkTable,
    FactTable,
)
from sqlalchemy import inspect


def get_config_table_name(config_dimen) -> str:
    config_specs_dict = config_dimen.get(normal_specs_str())
    return config_specs_dict.get(normal_table_name_str())


def all_columns_are_as_config_requires(mapper, config_dimen):
    config_table_name = get_config_table_name(config_dimen)
    config_columns = config_dimen.get(columns_str())

    for config_column, column_dict in config_columns.items():
        table_column = mapper.columns.get(config_column)
        failed_assert_str = f"{config_column=} is missing from {config_table_name=}"
        assert table_column is not None, failed_assert_str
        config_type = column_dict.get(sqlite_datatype_str())
        if config_type == "TEXT":
            config_type = "VARCHAR"
        elif config_type == "REAL":
            config_type = "FLOAT"
        failed_assert_str = f"Table '{config_table_name}' {config_column=} {str(table_column.type)==config_type=}"
        assert str(table_column.type) == config_type, failed_assert_str


def print_out_expected_class_attribute_declarations(config_dimen):
    config_table_name = get_config_table_name(config_dimen)
    config_columns = config_dimen.get(columns_str())

    print(f"Table {config_table_name}")
    for config_column, column_dict in config_columns.items():
        declare_type = column_dict.get(sqlite_datatype_str())
        if declare_type == "TEXT":
            declare_type = "String"
        elif declare_type == "INTEGER":
            declare_type = "Integer"
        elif declare_type == "REAL":
            declare_type = "Float"
        if config_column == "uid":
            declare_type = "Integer, primary_key=True"
        print(f"    {config_column} = Column({declare_type})")


def test_normalized_table_BudTable_Exists():
    # ESTABLISH
    config_dimen = get_normalized_bud_table_build().get(budunit_str())
    mapper = inspect(BudTable)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_dimen)
    assert config_table_name == "bud"
    assert config_table_name == BudTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_dimen)


def test_normalized_table_AcctUnitTable_Exists():
    # ESTABLISH
    config_dimen = get_normalized_bud_table_build().get(bud_acctunit_str())
    mapper = inspect(AcctUnitTable)
    # print_out_expected_class_attribute_declarations(config_dimen)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_dimen)
    assert config_table_name == "acctunit"
    assert config_table_name == AcctUnitTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_dimen)


# def test_normalized_table_GroupTable_Exists():
#     # ESTABLISH
#     config_dimen = get_normalized_bud_table_build().get("bud_groupunit")
#     mapper = inspect(GroupTable)
#     print_out_expected_class_attribute_declarations(config_dimen)

#     # WHEN / THEN
#     config_table_name = get_config_table_name(config_dimen)
#     assert config_table_name == "groupunit"
#     assert config_table_name == GroupTable.__tablename__
#     all_columns_are_as_config_requires(mapper, config_dimen)


def test_normalized_table_MemberShipTable_membership_Exists():
    # ESTABLISH
    config_dimen = get_normalized_bud_table_build().get(bud_acct_membership_str())
    mapper = inspect(MemberShipTable)
    print_out_expected_class_attribute_declarations(config_dimen)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_dimen)
    assert config_table_name == "membership"
    assert config_table_name == MemberShipTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_dimen)


def test_normalized_table_ItemTable_item_Exists():
    # ESTABLISH
    config_dimen = get_normalized_bud_table_build().get(bud_itemunit_str())
    mapper = inspect(ItemTable)
    print_out_expected_class_attribute_declarations(config_dimen)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_dimen)
    assert config_table_name == "item"
    assert config_table_name == ItemTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_dimen)


def test_normalized_table_AwardLinkTable_awardlink_Exists():
    # ESTABLISH
    config_dimen = get_normalized_bud_table_build().get(bud_item_awardlink_str())
    mapper = inspect(AwardLinkTable)
    print_out_expected_class_attribute_declarations(config_dimen)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_dimen)
    assert config_table_name == "awardlink"
    assert config_table_name == AwardLinkTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_dimen)


def test_normalized_table_ReasonTable_reason_Exists():
    # ESTABLISH
    config_dimen = get_normalized_bud_table_build().get(bud_item_reasonunit_str())
    mapper = inspect(ReasonTable)
    print_out_expected_class_attribute_declarations(config_dimen)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_dimen)
    assert config_table_name == "reason"
    assert config_table_name == ReasonTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_dimen)


def test_normalized_table_PremiseTable_premise_Exists():
    # ESTABLISH
    config_dimen = get_normalized_bud_table_build().get(
        bud_item_reason_premiseunit_str()
    )
    mapper = inspect(PremiseTable)
    print_out_expected_class_attribute_declarations(config_dimen)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_dimen)
    assert config_table_name == "premise"
    assert config_table_name == PremiseTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_dimen)


def test_normalized_table_TeamLinkTable_teamlink_Exists():
    # ESTABLISH
    config_dimen = get_normalized_bud_table_build().get(bud_item_teamlink_str())
    mapper = inspect(TeamLinkTable)
    print_out_expected_class_attribute_declarations(config_dimen)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_dimen)
    assert config_table_name == "teamlink"
    assert config_table_name == TeamLinkTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_dimen)


def test_normalized_table_HealerLinkTable_healerlink_Exists():
    # ESTABLISH
    config_dimen = get_normalized_bud_table_build().get(bud_item_healerlink_str())
    mapper = inspect(HealerLinkTable)
    print_out_expected_class_attribute_declarations(config_dimen)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_dimen)
    assert config_table_name == "healerlink"
    assert config_table_name == HealerLinkTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_dimen)


def test_normalized_table_FactTable_fact_Exists():
    # ESTABLISH
    config_dimen = get_normalized_bud_table_build().get(bud_item_factunit_str())
    mapper = inspect(FactTable)
    print_out_expected_class_attribute_declarations(config_dimen)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_dimen)
    assert config_table_name == "fact"
    assert config_table_name == FactTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_dimen)
