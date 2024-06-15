from src.atom.quark_config import (
    get_normalized_agenda_table_build,
    normal_table_name_text,
    columns_text,
    sqlite_datatype_text,
)
from src.normal_db.normal_models import (
    AgendaTable,
    PartyUnitTable,
    BeliefTable,
    PartyLinkTable,
    IdeaTable,
    BalanceLinkTable,
    ReasonTable,
    PremiseTable,
    SuffBeliefTable,
    HealerHoldTable,
    FactTable,
)
from sqlalchemy import inspect


def all_columns_are_as_config_requires(mapper, config_category):
    config_table_name = config_category.get(normal_table_name_text())
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
    config_table_name = config_category.get(normal_table_name_text())
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


def test_normalized_table_AgendaTable_Exists():
    # GIVEN
    config_category = get_normalized_agenda_table_build().get("agendaunit")
    mapper = inspect(AgendaTable)

    # WHEN / THEN
    config_table_name = config_category.get(normal_table_name_text())
    assert config_table_name == "agenda"
    assert config_table_name == AgendaTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_PartyUnitTable_Exists():
    # GIVEN
    config_category = get_normalized_agenda_table_build().get("agenda_partyunit")
    mapper = inspect(PartyUnitTable)
    # print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = config_category.get(normal_table_name_text())
    assert config_table_name == "partyunit"
    assert config_table_name == PartyUnitTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_BeliefTable_Exists():
    # GIVEN
    config_category = get_normalized_agenda_table_build().get("agenda_beliefunit")
    mapper = inspect(BeliefTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = config_category.get(normal_table_name_text())
    assert config_table_name == "beliefunit"
    assert config_table_name == BeliefTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_PartyLinkTable_partylink_Exists():
    # GIVEN
    config_category = get_normalized_agenda_table_build().get("agenda_belief_partylink")
    mapper = inspect(PartyLinkTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = config_category.get(normal_table_name_text())
    assert config_table_name == "partylink"
    assert config_table_name == PartyLinkTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_IdeaTable_idea_Exists():
    # GIVEN
    config_category = get_normalized_agenda_table_build().get("agenda_ideaunit")
    mapper = inspect(IdeaTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = config_category.get(normal_table_name_text())
    assert config_table_name == "idea"
    assert config_table_name == IdeaTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_BalanceLinkTable_balancelink_Exists():
    # GIVEN
    config_category = get_normalized_agenda_table_build().get("agenda_idea_balancelink")
    mapper = inspect(BalanceLinkTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = config_category.get(normal_table_name_text())
    assert config_table_name == "balancelink"
    assert config_table_name == BalanceLinkTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_ReasonTable_reason_Exists():
    # GIVEN
    config_category = get_normalized_agenda_table_build().get("agenda_idea_reasonunit")
    mapper = inspect(ReasonTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = config_category.get(normal_table_name_text())
    assert config_table_name == "reason"
    assert config_table_name == ReasonTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_PremiseTable_premise_Exists():
    # GIVEN
    config_category = get_normalized_agenda_table_build().get(
        "agenda_idea_reason_premiseunit"
    )
    mapper = inspect(PremiseTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = config_category.get(normal_table_name_text())
    assert config_table_name == "premise"
    assert config_table_name == PremiseTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_SuffBeliefTable_suffbelief_Exists():
    # GIVEN
    config_category = get_normalized_agenda_table_build().get("agenda_idea_suffbelief")
    mapper = inspect(SuffBeliefTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = config_category.get(normal_table_name_text())
    assert config_table_name == "suffbelief"
    assert config_table_name == SuffBeliefTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_HealerHoldTable_healerhold_Exists():
    # GIVEN
    config_category = get_normalized_agenda_table_build().get("agenda_idea_healerhold")
    mapper = inspect(HealerHoldTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = config_category.get(normal_table_name_text())
    assert config_table_name == "healerhold"
    assert config_table_name == HealerHoldTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)


def test_normalized_table_FactTable_fact_Exists():
    # GIVEN
    config_category = get_normalized_agenda_table_build().get("agenda_idea_factunit")
    mapper = inspect(FactTable)
    print_out_expected_class_attribute_declarations(config_category)

    # WHEN / THEN
    config_table_name = config_category.get(normal_table_name_text())
    assert config_table_name == "fact"
    assert config_table_name == FactTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_category)
