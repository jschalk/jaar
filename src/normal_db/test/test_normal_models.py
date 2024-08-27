from src.gift.atom_config import (
    get_normalized_bud_table_build,
    normal_table_name_text,
    normal_specs_text,
    columns_text,
    sqlite_datatype_text,
    budunit_text,
    bud_acctunit_text,
    bud_acct_membership_text,
    bud_ideaunit_text,
    bud_idea_awardlink_text,
    bud_idea_reasonunit_text,
    bud_idea_reason_premiseunit_text,
    bud_idea_grouphold_text,
    bud_idea_range_push_text,
    bud_idea_healerhold_text,
    bud_idea_factunit_text,
)
from src.normal_db.normal_models import (
    BudTable,
    AcctUnitTable,
    MemberShipTable,
    IdeaTable,
    AwardLinkTable,
    ReasonTable,
    PremiseTable,
    GroupHoldTable,
    HealerHoldTable,
    FactTable,
)
from sqlalchemy import inspect


def get_config_table_name(config_category) -> str:
    config_specs_dict = config_category.get(normal_specs_text())
    return config_specs_dict.get(normal_table_name_text())


def all_columns_are_as_config_requires(mapper, config_category):
    config_table_name = get_config_table_name(config_category)
    config_columns = config_category.get(columns_text())

    for config_column, column_dict in config_columns.items():
        table_column = mapper.columns.get(config_column)
        failed_assert_text = f"{config_column=} is missing from {config_table_name=}"
        assert table_column is not None, failed_assert_text
        config_type = column_dict.get(sqlite_datatype_text())
        if config_type == "TEXT":
            config_type = "VARCHAR"
        elif config_type == "REAL":
            config_type = "FLOAT"
        failed_assert_text = f"Table '{config_table_name}' {config_column=} {str(table_column.type)==config_type=}"
        assert str(table_column.type) == config_type, failed_assert_text


def print_out_expected_class_attribute_declarations(config_category):
    config_table_name = get_config_table_name(config_category)
    config_columns = config_category.get(columns_text())

    print(f"Table {config_table_name}")
    for config_column, column_dict in config_columns.items():
        declare_type = column_dict.get(sqlite_datatype_text())
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
    config_category = get_normalized_bud_table_build().get("budunit")
    mapper = inspect(BudTable)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_category)
    assert config_table_name == "bud"
    assert config_table_name == BudTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_AcctUnitTable_Exists():
    # ESTABLISH
    config_category = get_normalized_bud_table_build().get(bud_acctunit_text())
    mapper = inspect(AcctUnitTable)
    # print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_category)
    assert config_table_name == "acctunit"
    assert config_table_name == AcctUnitTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


# def test_normalized_table_GroupTable_Exists():
#     # ESTABLISH
#     config_category = get_normalized_bud_table_build().get("bud_groupbox")
#     mapper = inspect(GroupTable)
#     print_out_expected_class_attribute_declarations(config_category)

#     # WHEN / THEN
#     config_table_name = get_config_table_name(config_category)
#     assert config_table_name == "groupbox"
#     assert config_table_name == GroupTable.__tablename__
#     all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_MemberShipTable_membership_Exists():
    # ESTABLISH
    config_category = get_normalized_bud_table_build().get(bud_acct_membership_text())
    mapper = inspect(MemberShipTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_category)
    assert config_table_name == "membership"
    assert config_table_name == MemberShipTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_IdeaTable_idea_Exists():
    # ESTABLISH
    config_category = get_normalized_bud_table_build().get(bud_ideaunit_text())
    mapper = inspect(IdeaTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_category)
    assert config_table_name == "idea"
    assert config_table_name == IdeaTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_AwardLinkTable_awardlink_Exists():
    # ESTABLISH
    config_category = get_normalized_bud_table_build().get(bud_idea_awardlink_text())
    mapper = inspect(AwardLinkTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_category)
    assert config_table_name == "awardlink"
    assert config_table_name == AwardLinkTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_ReasonTable_reason_Exists():
    # ESTABLISH
    config_category = get_normalized_bud_table_build().get(bud_idea_reasonunit_text())
    mapper = inspect(ReasonTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_category)
    assert config_table_name == "reason"
    assert config_table_name == ReasonTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_PremiseTable_premise_Exists():
    # ESTABLISH
    config_category = get_normalized_bud_table_build().get(
        bud_idea_reason_premiseunit_text()
    )
    mapper = inspect(PremiseTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_category)
    assert config_table_name == "premise"
    assert config_table_name == PremiseTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_GroupHoldTable_grouphold_Exists():
    # ESTABLISH
    config_category = get_normalized_bud_table_build().get(bud_idea_grouphold_text())
    mapper = inspect(GroupHoldTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_category)
    assert config_table_name == "grouphold"
    assert config_table_name == GroupHoldTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_HealerHoldTable_healerhold_Exists():
    # ESTABLISH
    config_category = get_normalized_bud_table_build().get(bud_idea_healerhold_text())
    mapper = inspect(HealerHoldTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_category)
    assert config_table_name == "healerhold"
    assert config_table_name == HealerHoldTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_FactTable_fact_Exists():
    # ESTABLISH
    config_category = get_normalized_bud_table_build().get(bud_idea_factunit_text())
    mapper = inspect(FactTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_category)
    assert config_table_name == "fact"
    assert config_table_name == FactTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)
