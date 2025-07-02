from src.a06_believer_logic.believer import believerunit_shop
from src.a06_believer_logic.report import (
    get_believer_acctunits_dataframe,
    get_believer_agenda_dataframe,
)
from src.a06_believer_logic.test._util.example_believers import (
    believerunit_v001_with_large_agenda,
)


def test_get_believer_acctunits_dataframe_ReturnsCorrectDataFrame():
    # ESTABLISH
    luca_believer = believerunit_shop()
    luca_believer.set_credor_respect(500)
    luca_believer.set_debtor_respect(400)
    yao_str = "Yao"
    yao_acct_cred_points = 66
    yao_acct_debt_points = 77
    luca_believer.add_acctunit(yao_str, yao_acct_cred_points, yao_acct_debt_points)
    sue_str = "Sue"
    sue_acct_cred_points = 434
    sue_acct_debt_points = 323
    luca_believer.add_acctunit(sue_str, sue_acct_cred_points, sue_acct_debt_points)

    # WHEN
    x_df = get_believer_acctunits_dataframe(luca_believer)

    # THEN
    acctunit_colums = {
        "acct_name",
        "acct_cred_points",
        "acct_debt_points",
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


def test_get_believer_acctunits_dataframe_ReturnsCorrectEmptyDataFrame():
    # ESTABLISH
    luca_believer = believerunit_shop()

    # WHEN
    x_df = get_believer_acctunits_dataframe(luca_believer)

    # THEN
    acctunit_colums = {
        "acct_name",
        "acct_cred_points",
        "acct_debt_points",
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


def test_get_believer_agenda_dataframe_ReturnsCorrectDataFrame():
    # ESTABLISH
    yao_believer = believerunit_v001_with_large_agenda()
    wk_str = "wkdays"
    wk_rope = yao_believer.make_l1_rope(wk_str)
    assert len(yao_believer.get_agenda_dict()) == 63

    # WHEN
    x_df = get_believer_agenda_dataframe(yao_believer)
    print(x_df)

    # THEN
    acctunit_colums = {
        "believer_name",
        "fund_ratio",
        "plan_label",
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


def test_get_believer_agenda_dataframe_ReturnsCorrectEmptyDataFrame():
    # ESTABLISH
    yao_believer = believerunit_shop("Yao")
    assert len(yao_believer.get_agenda_dict()) == 0

    # WHEN
    x_df = get_believer_agenda_dataframe(yao_believer)
    print(x_df)

    # THEN
    acctunit_colums = {
        "believer_name",
        "fund_ratio",
        "plan_label",
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
