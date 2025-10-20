from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch09_belief_atom.atom_main import beliefatom_shop
from src.ch10_lesson.delta import beliefdelta_shop
from src.ch10_lesson.legible import create_legible_list
from src.ref.keywords import Ch10Keywords as kw


def test_create_legible_list_ReturnsObj_voiceunit_INSERT():
    # ESTABLISH
    dimen = kw.belief_voiceunit
    voice_cred_lumen_value = 81
    voice_debt_lumen_value = 43
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, kw.INSERT)
    yao_beliefatom.set_arg(kw.voice_name, yao_str)
    yao_beliefatom.set_arg(kw.voice_cred_lumen, voice_cred_lumen_value)
    yao_beliefatom.set_arg(kw.voice_debt_lumen, voice_debt_lumen_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{yao_str} was added with {voice_cred_lumen_value} score credit and {voice_debt_lumen_value} score debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voiceunit_INSERT_score():
    # ESTABLISH
    dimen = kw.belief_voiceunit
    voice_cred_lumen_value = 81
    voice_debt_lumen_value = 43
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, kw.INSERT)
    yao_beliefatom.set_arg(kw.voice_name, yao_str)
    yao_beliefatom.set_arg(kw.voice_cred_lumen, voice_cred_lumen_value)
    yao_beliefatom.set_arg(kw.voice_debt_lumen, voice_debt_lumen_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{yao_str} was added with {voice_cred_lumen_value} score credit and {voice_debt_lumen_value} score debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voiceunit_UPDATE_voice_cred_lumen_voice_debt_lumen():
    # ESTABLISH
    dimen = kw.belief_voiceunit
    voice_cred_lumen_value = 81
    voice_debt_lumen_value = 43
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, kw.UPDATE)
    yao_beliefatom.set_arg(kw.voice_name, yao_str)
    yao_beliefatom.set_arg(kw.voice_cred_lumen, voice_cred_lumen_value)
    yao_beliefatom.set_arg(kw.voice_debt_lumen, voice_debt_lumen_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{yao_str} now has {voice_cred_lumen_value} score credit and {voice_debt_lumen_value} score debt."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voiceunit_UPDATE_voice_cred_lumen():
    # ESTABLISH
    dimen = kw.belief_voiceunit
    voice_cred_lumen_value = 81
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, kw.UPDATE)
    yao_beliefatom.set_arg(kw.voice_name, yao_str)
    yao_beliefatom.set_arg(kw.voice_cred_lumen, voice_cred_lumen_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{yao_str} now has {voice_cred_lumen_value} score credit."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voiceunit_UPDATE_voice_debt_lumen():
    # ESTABLISH
    dimen = kw.belief_voiceunit
    voice_debt_lumen_value = 43
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, kw.UPDATE)
    yao_beliefatom.set_arg(kw.voice_name, yao_str)
    yao_beliefatom.set_arg(kw.voice_debt_lumen, voice_debt_lumen_value)
    # print(f"{yao_beliefatom=}")
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(yao_beliefatom)
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_beliefdelta, sue_belief)

    # THEN
    x_str = f"{yao_str} now has {voice_debt_lumen_value} score debt."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_voiceunit_DELETE():
    # ESTABLISH
    dimen = kw.belief_voiceunit
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, kw.DELETE)
    yao_beliefatom.set_arg(kw.voice_name, yao_str)
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
