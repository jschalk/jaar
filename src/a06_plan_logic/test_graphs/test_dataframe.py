from src.a06_plan_logic._util.example_plans import planunit_v001_with_large_agenda
from src.a06_plan_logic.plan import planunit_shop
from src.a06_plan_logic.report import (
    get_plan_acctunits_dataframe,
    get_plan_agenda_dataframe,
)


def test_get_plan_acctunits_dataframe_ReturnsCorrectDataFrame():
    # ESTABLISH
    luca_plan = planunit_shop()
    luca_plan.set_credor_respect(500)
    luca_plan.set_debtor_respect(400)
    yao_str = "Yao"
    yao_credit_score = 66
    yao_debt_score = 77
    luca_plan.add_acctunit(yao_str, yao_credit_score, yao_debt_score)
    sue_str = "Sue"
    sue_credit_score = 434
    sue_debt_score = 323
    luca_plan.add_acctunit(sue_str, sue_credit_score, sue_debt_score)

    # WHEN
    x_df = get_plan_acctunits_dataframe(luca_plan)

    # THEN
    acctunit_colums = {
        "acct_name",
        "credit_score",
        "debt_score",
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


def test_get_plan_acctunits_dataframe_ReturnsCorrectEmptyDataFrame():
    # ESTABLISH
    luca_plan = planunit_shop()

    # WHEN
    x_df = get_plan_acctunits_dataframe(luca_plan)

    # THEN
    acctunit_colums = {
        "acct_name",
        "credit_score",
        "debt_score",
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


def test_get_plan_agenda_dataframe_ReturnsCorrectDataFrame():
    # ESTABLISH
    yao_plan = planunit_v001_with_large_agenda()
    wk_str = "wkdays"
    wk_rope = yao_plan.make_l1_rope(wk_str)
    assert len(yao_plan.get_agenda_dict()) == 63

    # WHEN
    x_df = get_plan_agenda_dataframe(yao_plan)
    print(x_df)

    # THEN
    acctunit_colums = {
        "owner_name",
        "fund_ratio",
        "concept_label",
        "parent_rope",
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


def test_get_plan_agenda_dataframe_ReturnsCorrectEmptyDataFrame():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    assert len(yao_plan.get_agenda_dict()) == 0

    # WHEN
    x_df = get_plan_agenda_dataframe(yao_plan)
    print(x_df)

    # THEN
    acctunit_colums = {
        "owner_name",
        "fund_ratio",
        "concept_label",
        "parent_rope",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == acctunit_colums
