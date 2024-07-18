from src.bud.examples.example_buds import bud_v001_with_large_agenda
from src.bud.bud import budunit_shop
from src.bud.report import (
    get_bud_charunits_dataframe,
    get_bud_agenda_dataframe,
)


def test_get_bud_charunits_dataframe_ReturnsCorrectDataFrame():
    # ESTABLISH
    luca_bud = budunit_shop()
    luca_bud.set_credor_respect(500)
    luca_bud.set_debtor_resepect(400)
    yao_text = "Yao"
    yao_credor_weight = 66
    yao_debtor_weight = 77
    luca_bud.add_charunit(yao_text, yao_credor_weight, yao_debtor_weight)
    sue_text = "Sue"
    sue_credor_weight = 434
    sue_debtor_weight = 323
    luca_bud.add_charunit(sue_text, sue_credor_weight, sue_debtor_weight)

    # WHEN
    x_df = get_bud_charunits_dataframe(luca_bud)

    # THEN
    charunit_colums = {
        "char_id",
        "credor_weight",
        "debtor_weight",
        "_lobbyships",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_agenda_ratio_give",
        "_fund_agenda_ratio_take",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == charunit_colums
    assert x_df.shape[0] == 2


def test_get_bud_charunits_dataframe_ReturnsCorrectEmptyDataFrame():
    # ESTABLISH
    luca_bud = budunit_shop()

    # WHEN
    x_df = get_bud_charunits_dataframe(luca_bud)

    # THEN
    charunit_colums = {
        "char_id",
        "credor_weight",
        "debtor_weight",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_agenda_ratio_give",
        "_fund_agenda_ratio_take",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == charunit_colums
    assert x_df.shape[0] == 0


def test_get_bud_agenda_dataframe_ReturnsCorrectDataFrame():
    # ESTABLISH
    yao_bud = bud_v001_with_large_agenda()
    week_text = "weekdays"
    week_road = yao_bud.make_l1_road(week_text)
    assert len(yao_bud.get_agenda_dict()) == 63

    # WHEN
    x_df = get_bud_agenda_dataframe(yao_bud)
    print(x_df)

    # THEN
    charunit_colums = {
        "owner_id",
        "fund_ratio",
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


def test_get_bud_agenda_dataframe_ReturnsCorrectEmptyDataFrame():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    assert len(yao_bud.get_agenda_dict()) == 0

    # WHEN
    x_df = get_bud_agenda_dataframe(yao_bud)
    print(x_df)

    # THEN
    charunit_colums = {
        "owner_id",
        "fund_ratio",
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