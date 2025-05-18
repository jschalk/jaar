from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic.report import (
    get_bud_acctunits_dataframe,
    get_bud_agenda_dataframe,
)
from src.a06_bud_logic._utils.example_buds import budunit_v001_with_large_agenda


def test_get_bud_acctunits_dataframe_ReturnsCorrectDataFrame():
    # ESTABLISH
    luca_bud = budunit_shop()
    luca_bud.set_credor_respect(500)
    luca_bud.set_debtor_respect(400)
    yao_str = "Yao"
    yao_credit_belief = 66
    yao_debtit_belief = 77
    luca_bud.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    sue_str = "Sue"
    sue_credit_belief = 434
    sue_debtit_belief = 323
    luca_bud.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)

    # WHEN
    x_df = get_bud_acctunits_dataframe(luca_bud)

    # THEN
    acctunit_colums = {
        "acct_name",
        "credit_belief",
        "debtit_belief",
        "_memberships",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_agenda_ratio_give",
        "_fund_agenda_ratio_take",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == acctunit_colums
    assert x_df.shape[0] == 2


def test_get_bud_acctunits_dataframe_ReturnsCorrectEmptyDataFrame():
    # ESTABLISH
    luca_bud = budunit_shop()

    # WHEN
    x_df = get_bud_acctunits_dataframe(luca_bud)

    # THEN
    acctunit_colums = {
        "acct_name",
        "credit_belief",
        "debtit_belief",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_agenda_ratio_give",
        "_fund_agenda_ratio_take",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == acctunit_colums
    assert x_df.shape[0] == 0


def test_get_bud_agenda_dataframe_ReturnsCorrectDataFrame():
    # ESTABLISH
    yao_bud = budunit_v001_with_large_agenda()
    week_str = "weekdays"
    week_way = yao_bud.make_l1_way(week_str)
    assert len(yao_bud.get_agenda_dict()) == 63

    # WHEN
    x_df = get_bud_agenda_dataframe(yao_bud)
    print(x_df)

    # THEN
    acctunit_colums = {
        "owner_name",
        "fund_ratio",
        "concept_label",
        "parent_way",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == acctunit_colums
    assert x_df.shape[0] == 63


def test_get_bud_agenda_dataframe_ReturnsCorrectEmptyDataFrame():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    assert len(yao_bud.get_agenda_dict()) == 0

    # WHEN
    x_df = get_bud_agenda_dataframe(yao_bud)
    print(x_df)

    # THEN
    acctunit_colums = {
        "owner_name",
        "fund_ratio",
        "concept_label",
        "parent_way",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == acctunit_colums
