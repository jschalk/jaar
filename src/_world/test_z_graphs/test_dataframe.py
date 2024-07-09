from src._world.examples.example_worlds import world_v001_with_large_agenda
from src._world.world import worldunit_shop
from src._world.report import (
    get_world_charunits_dataframe,
    get_world_agenda_dataframe,
)


def test_get_world_charunits_dataframe_ReturnsCorrectDataFrame():
    # GIVEN
    luca_world = worldunit_shop()
    luca_world.set_char_credor_pool(500)
    luca_world.set_char_debtor_pool(400)
    yao_text = "Yao"
    yao_credor_weight = 66
    yao_debtor_weight = 77
    luca_world.add_charunit(yao_text, yao_credor_weight, yao_debtor_weight)
    sue_text = "Sue"
    sue_credor_weight = 434
    sue_debtor_weight = 323
    luca_world.add_charunit(sue_text, sue_credor_weight, sue_debtor_weight)

    # WHEN
    x_df = get_world_charunits_dataframe(luca_world)

    # THEN
    charunit_colums = {
        "char_id",
        "credor_weight",
        "debtor_weight",
        "_belieflinks",
        "_world_cred",
        "_world_debt",
        "_world_agenda_cred",
        "_world_agenda_debt",
        "_world_agenda_ratio_cred",
        "_world_agenda_ratio_debt",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == charunit_colums
    assert x_df.shape[0] == 2


def test_get_world_charunits_dataframe_ReturnsCorrectEmptyDataFrame():
    # GIVEN
    luca_world = worldunit_shop()

    # WHEN
    x_df = get_world_charunits_dataframe(luca_world)

    # THEN
    charunit_colums = {
        "char_id",
        "credor_weight",
        "debtor_weight",
        "_world_cred",
        "_world_debt",
        "_world_agenda_cred",
        "_world_agenda_debt",
        "_world_agenda_ratio_cred",
        "_world_agenda_ratio_debt",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == charunit_colums
    assert x_df.shape[0] == 0


def test_get_world_agenda_dataframe_ReturnsCorrectDataFrame():
    # GIVEN
    yao_world = world_v001_with_large_agenda()
    week_text = "weekdays"
    week_road = yao_world.make_l1_road(week_text)
    assert len(yao_world.get_agenda_dict()) == 63

    # WHEN
    x_df = get_world_agenda_dataframe(yao_world)
    print(x_df)

    # THEN
    charunit_colums = {
        "owner_id",
        "world_importance",
        "_label",
        "_parent_road",
        "_begin",
        "_close",
        "_addin",
        "_denom",
        "_numor",
        "_reest",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == charunit_colums
    assert x_df.shape[0] == 63


def test_get_world_agenda_dataframe_ReturnsCorrectEmptyDataFrame():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    assert len(yao_world.get_agenda_dict()) == 0

    # WHEN
    x_df = get_world_agenda_dataframe(yao_world)
    print(x_df)

    # THEN
    charunit_colums = {
        "owner_id",
        "world_importance",
        "_label",
        "_parent_road",
        "_begin",
        "_close",
        "_addin",
        "_denom",
        "_numor",
        "_reest",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == charunit_colums
