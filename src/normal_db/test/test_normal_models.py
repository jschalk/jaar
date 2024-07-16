from src.gift.atom_config import (
    get_normalized_world_table_build,
    normal_table_name_text,
    normal_specs_text,
    columns_text,
    sqlite_datatype_text,
)
from src.normal_db.normal_models import (
    WorldTable,
    CharUnitTable,
    BeliefLinkTable,
    IdeaTable,
    AwardLinkTable,
    ReasonTable,
    PremiseTable,
    beliefholdTable,
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


def test_normalized_table_WorldTable_Exists():
    # GIVEN
    config_category = get_normalized_world_table_build().get("worldunit")
    mapper = inspect(WorldTable)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_category)
    assert config_table_name == "world"
    assert config_table_name == WorldTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_CharUnitTable_Exists():
    # GIVEN
    config_category = get_normalized_world_table_build().get("world_charunit")
    mapper = inspect(CharUnitTable)
    # print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_category)
    assert config_table_name == "charunit"
    assert config_table_name == CharUnitTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


# def test_normalized_table_BeliefTable_Exists():
#     # GIVEN
#     config_category = get_normalized_world_table_build().get("world_beliefstory")
#     mapper = inspect(BeliefTable)
#     print_out_expected_class_attribute_declarations(config_category)

#     # WHEN / THEN
#     config_table_name = get_config_table_name(config_category)
#     assert config_table_name == "beliefstory"
#     assert config_table_name == BeliefTable.__tablename__
#     all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_BeliefLinkTable_belieflink_Exists():
    # GIVEN
    config_category = get_normalized_world_table_build().get("world_char_belieflink")
    mapper = inspect(BeliefLinkTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_category)
    assert config_table_name == "belieflink"
    assert config_table_name == BeliefLinkTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_IdeaTable_idea_Exists():
    # GIVEN
    config_category = get_normalized_world_table_build().get("world_ideaunit")
    mapper = inspect(IdeaTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_category)
    assert config_table_name == "idea"
    assert config_table_name == IdeaTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_AwardLinkTable_awardlink_Exists():
    # GIVEN
    config_category = get_normalized_world_table_build().get("world_idea_awardlink")
    mapper = inspect(AwardLinkTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_category)
    assert config_table_name == "awardlink"
    assert config_table_name == AwardLinkTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_ReasonTable_reason_Exists():
    # GIVEN
    config_category = get_normalized_world_table_build().get("world_idea_reasonunit")
    mapper = inspect(ReasonTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_category)
    assert config_table_name == "reason"
    assert config_table_name == ReasonTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_PremiseTable_premise_Exists():
    # GIVEN
    config_category = get_normalized_world_table_build().get(
        "world_idea_reason_premiseunit"
    )
    mapper = inspect(PremiseTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_category)
    assert config_table_name == "premise"
    assert config_table_name == PremiseTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_beliefholdTable_beliefhold_Exists():
    # GIVEN
    config_category = get_normalized_world_table_build().get("world_idea_beliefhold")
    mapper = inspect(beliefholdTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_category)
    assert config_table_name == "beliefhold"
    assert config_table_name == beliefholdTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_HealerHoldTable_healerhold_Exists():
    # GIVEN
    config_category = get_normalized_world_table_build().get("world_idea_healerhold")
    mapper = inspect(HealerHoldTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_category)
    assert config_table_name == "healerhold"
    assert config_table_name == HealerHoldTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_FactTable_fact_Exists():
    # GIVEN
    config_category = get_normalized_world_table_build().get("world_idea_factunit")
    mapper = inspect(FactTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_category)
    assert config_table_name == "fact"
    assert config_table_name == FactTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)
