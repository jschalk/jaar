from src.a06_believer_logic.believer import believerunit_shop
from src.a06_believer_logic.report import (
    get_believer_agenda_dataframe,
    get_believer_partnerunits_dataframe,
)
from src.a06_believer_logic.test._util.example_believers import (
    believerunit_v001_with_large_agenda,
)


def test_get_believer_partnerunits_dataframe_ReturnsCorrectDataFrame():
    # ESTABLISH
    luca_believer = believerunit_shop()
    luca_believer.set_credor_respect(500)
    luca_believer.set_debtor_respect(400)
    yao_str = "Yao"
    yao_partner_cred_points = 66
    yao_partner_debt_points = 77
    luca_believer.add_partnerunit(
        yao_str, yao_partner_cred_points, yao_partner_debt_points
    )
    sue_str = "Sue"
    sue_partner_cred_points = 434
    sue_partner_debt_points = 323
    luca_believer.add_partnerunit(
        sue_str, sue_partner_cred_points, sue_partner_debt_points
    )

    # WHEN
    x_df = get_believer_partnerunits_dataframe(luca_believer)

    # THEN
    partnerunit_colums = {
        "partner_name",
        "partner_cred_points",
        "partner_debt_points",
        "_memberships",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_agenda_ratio_give",
        "_fund_agenda_ratio_take",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == partnerunit_colums
    assert x_df.shape[0] == 2


def test_get_believer_partnerunits_dataframe_ReturnsCorrectEmptyDataFrame():
    # ESTABLISH
    luca_believer = believerunit_shop()

    # WHEN
    x_df = get_believer_partnerunits_dataframe(luca_believer)

    # THEN
    partnerunit_colums = {
        "partner_name",
        "partner_cred_points",
        "partner_debt_points",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_agenda_ratio_give",
        "_fund_agenda_ratio_take",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == partnerunit_colums
    assert x_df.shape[0] == 0


def test_get_believer_agenda_dataframe_ReturnsCorrectDataFrame():
    # ESTABLISH
    yao_believer = believerunit_v001_with_large_agenda()
    assert len(yao_believer.get_agenda_dict()) == 63

    # WHEN
    x_df = get_believer_agenda_dataframe(yao_believer)
    print(x_df)

    # THEN
    partnerunit_colums = {
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

    assert set(x_df.columns) == partnerunit_colums
    assert x_df.shape[0] == 63


def test_get_believer_agenda_dataframe_ReturnsCorrectEmptyDataFrame():
    # ESTABLISH
    yao_believer = believerunit_shop("Yao")
    assert len(yao_believer.get_agenda_dict()) == 0

    # WHEN
    x_df = get_believer_agenda_dataframe(yao_believer)
    print(x_df)

    # THEN
    partnerunit_colums = {
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

    assert set(x_df.columns) == partnerunit_colums
