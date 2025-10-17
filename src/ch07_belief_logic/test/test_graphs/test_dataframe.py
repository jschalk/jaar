from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.belief_report import (
    get_belief_agenda_dataframe,
    get_belief_voiceunits_dataframe,
)
from src.ch07_belief_logic.test._util.ch07_examples import (
    beliefunit_v001_with_large_agenda,
)
from src.ref.keywords import Ch07Keywords as wx


def test_get_belief_voiceunits_dataframe_ReturnsDataFrame():
    # ESTABLISH
    luca_belief = beliefunit_shop()
    luca_belief.set_credor_respect(500)
    luca_belief.set_debtor_respect(400)
    yao_str = "Yao"
    yao_voice_cred_lumen = 66
    yao_voice_debt_lumen = 77
    luca_belief.add_voiceunit(yao_str, yao_voice_cred_lumen, yao_voice_debt_lumen)
    sue_str = "Sue"
    sue_voice_cred_lumen = 434
    sue_voice_debt_lumen = 323
    luca_belief.add_voiceunit(sue_str, sue_voice_cred_lumen, sue_voice_debt_lumen)

    # WHEN
    x_df = get_belief_voiceunits_dataframe(luca_belief)

    # THEN
    voiceunit_colums = {
        "voice_name",
        "voice_cred_lumen",
        "voice_debt_lumen",
        "memberships",
        "fund_give",
        "fund_take",
        "fund_agenda_give",
        "fund_agenda_take",
        "fund_agenda_ratio_give",
        "fund_agenda_ratio_take",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == voiceunit_colums
    assert x_df.shape[0] == 2


def test_get_belief_voiceunits_dataframe_ReturnsEmptyDataFrame():
    # ESTABLISH
    luca_belief = beliefunit_shop()

    # WHEN
    x_df = get_belief_voiceunits_dataframe(luca_belief)

    # THEN
    voiceunit_colums = {
        "voice_name",
        "voice_cred_lumen",
        "voice_debt_lumen",
        "fund_give",
        "fund_take",
        "fund_agenda_give",
        "fund_agenda_take",
        "fund_agenda_ratio_give",
        "fund_agenda_ratio_take",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == voiceunit_colums
    assert x_df.shape[0] == 0


def test_get_belief_agenda_dataframe_ReturnsDataFrame():
    # ESTABLISH
    yao_belief = beliefunit_v001_with_large_agenda()
    assert len(yao_belief.get_agenda_dict()) == 69

    # WHEN
    x_df = get_belief_agenda_dataframe(yao_belief)
    print(x_df)

    # THEN
    voiceunit_colums = {
        wx.belief_name,
        "fund_ratio",
        wx.plan_label,
        wx.parent_rope,
        wx.begin,
        wx.close,
        wx.addin,
        wx.denom,
        wx.numor,
        wx.morph,
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == voiceunit_colums
    assert x_df.shape[0] == 69


def test_get_belief_agenda_dataframe_ReturnsEmptyDataFrame():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    assert len(yao_belief.get_agenda_dict()) == 0

    # WHEN
    x_df = get_belief_agenda_dataframe(yao_belief)
    print(x_df)

    # THEN
    voiceunit_colums = {
        wx.belief_name,
        "fund_ratio",
        wx.plan_label,
        wx.parent_rope,
        wx.begin,
        wx.close,
        wx.addin,
        wx.denom,
        wx.numor,
        wx.morph,
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == voiceunit_colums
