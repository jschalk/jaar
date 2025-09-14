from src.a06_belief_logic._ref.a06_terms import (
    addin_str,
    begin_str,
    close_str,
    denom_str,
    morph_str,
    numor_str,
    parent_rope_str,
    plan_label_str,
)
from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a06_belief_logic.belief_report import (
    get_belief_agenda_dataframe,
    get_belief_voiceunits_dataframe,
)
from src.a06_belief_logic.test._util.example_beliefs import (
    beliefunit_v001_with_large_agenda,
)


def test_get_belief_voiceunits_dataframe_ReturnsDataFrame():
    # ESTABLISH
    luca_belief = beliefunit_shop()
    luca_belief.set_credor_respect(500)
    luca_belief.set_debtor_respect(400)
    yao_str = "Yao"
    yao_voice_cred_points = 66
    yao_voice_debt_points = 77
    luca_belief.add_voiceunit(yao_str, yao_voice_cred_points, yao_voice_debt_points)
    sue_str = "Sue"
    sue_voice_cred_points = 434
    sue_voice_debt_points = 323
    luca_belief.add_voiceunit(sue_str, sue_voice_cred_points, sue_voice_debt_points)

    # WHEN
    x_df = get_belief_voiceunits_dataframe(luca_belief)

    # THEN
    voiceunit_colums = {
        "voice_name",
        "voice_cred_points",
        "voice_debt_points",
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
        "voice_cred_points",
        "voice_debt_points",
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
    assert len(yao_belief.get_agenda_dict()) == 63

    # WHEN
    x_df = get_belief_agenda_dataframe(yao_belief)
    print(x_df)

    # THEN
    voiceunit_colums = {
        "belief_name",
        "fund_ratio",
        plan_label_str(),
        parent_rope_str(),
        begin_str(),
        close_str(),
        addin_str(),
        denom_str(),
        numor_str(),
        morph_str(),
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == voiceunit_colums
    assert x_df.shape[0] == 63


def test_get_belief_agenda_dataframe_ReturnsEmptyDataFrame():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    assert len(yao_belief.get_agenda_dict()) == 0

    # WHEN
    x_df = get_belief_agenda_dataframe(yao_belief)
    print(x_df)

    # THEN
    voiceunit_colums = {
        "belief_name",
        "fund_ratio",
        plan_label_str(),
        parent_rope_str(),
        begin_str(),
        close_str(),
        addin_str(),
        denom_str(),
        numor_str(),
        morph_str(),
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == voiceunit_colums
