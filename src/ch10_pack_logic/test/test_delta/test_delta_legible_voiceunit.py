from src.ch06_belief_logic.belief_main import beliefunit_shop
from src.ch08_belief_atom_logic.atom_main import beliefatom_shop
from src.ch10_pack_logic._ref.ch10_terms import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
    belief_voiceunit_str,
    voice_name_str,
)
from src.ch10_pack_logic.delta import beliefdelta_shop
from src.ch10_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_voiceunit_INSERT():
    # ESTABLISH
    dimen = belief_voiceunit_str()
    voice_cred_points_str = "voice_cred_points"
    voice_debt_points_str = "voice_debt_points"
    voice_cred_points_value = 81
    voice_debt_points_value = 43
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, INSERT_str())
    yao_beliefatom.set_arg(voice_name_str(), yao_str)
    yao_beliefatom.set_arg(voice_cred_points_str, voice_cred_points_value)
    yao_beliefatom.set_arg(voice_debt_points_str, voice_debt_points_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{yao_str} was added with {voice_cred_points_value} score credit and {voice_debt_points_value} score debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voiceunit_INSERT_score():
    # ESTABLISH
    dimen = belief_voiceunit_str()
    voice_cred_points_str = "voice_cred_points"
    voice_debt_points_str = "voice_debt_points"
    voice_cred_points_value = 81
    voice_debt_points_value = 43
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, INSERT_str())
    yao_beliefatom.set_arg(voice_name_str(), yao_str)
    yao_beliefatom.set_arg(voice_cred_points_str, voice_cred_points_value)
    yao_beliefatom.set_arg(voice_debt_points_str, voice_debt_points_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{yao_str} was added with {voice_cred_points_value} score credit and {voice_debt_points_value} score debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voiceunit_UPDATE_voice_cred_points_voice_debt_points():
    # ESTABLISH
    dimen = belief_voiceunit_str()
    voice_cred_points_str = "voice_cred_points"
    voice_debt_points_str = "voice_debt_points"
    voice_cred_points_value = 81
    voice_debt_points_value = 43
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, UPDATE_str())
    yao_beliefatom.set_arg(voice_name_str(), yao_str)
    yao_beliefatom.set_arg(voice_cred_points_str, voice_cred_points_value)
    yao_beliefatom.set_arg(voice_debt_points_str, voice_debt_points_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{yao_str} now has {voice_cred_points_value} score credit and {voice_debt_points_value} score debt."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voiceunit_UPDATE_voice_cred_points():
    # ESTABLISH
    dimen = belief_voiceunit_str()
    voice_cred_points_str = "voice_cred_points"
    voice_cred_points_value = 81
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, UPDATE_str())
    yao_beliefatom.set_arg(voice_name_str(), yao_str)
    yao_beliefatom.set_arg(voice_cred_points_str, voice_cred_points_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{yao_str} now has {voice_cred_points_value} score credit."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voiceunit_UPDATE_voice_debt_points():
    # ESTABLISH
    dimen = belief_voiceunit_str()
    voice_debt_points_str = "voice_debt_points"
    voice_debt_points_value = 43
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, UPDATE_str())
    yao_beliefatom.set_arg(voice_name_str(), yao_str)
    yao_beliefatom.set_arg(voice_debt_points_str, voice_debt_points_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{yao_str} now has {voice_debt_points_value} score debt."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voiceunit_DELETE():
    # ESTABLISH
    dimen = belief_voiceunit_str()
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, DELETE_str())
    yao_beliefatom.set_arg(voice_name_str(), yao_str)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{yao_str} was removed from score voices."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
