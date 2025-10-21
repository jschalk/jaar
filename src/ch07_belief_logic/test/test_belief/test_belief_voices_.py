from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises
from src.ch04_voice.voice import voiceunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop


def test_BeliefUnit_set_voiceunit_SetsAttr():
    # ESTABLISH
    yao_str = "Yao"
    yao_voiceunit = voiceunit_shop(yao_str)
    yao_voiceunit.add_membership(yao_str)
    deepcopy_yao_voiceunit = copy_deepcopy(yao_voiceunit)
    slash_str = "/"
    bob_belief = beliefunit_shop("Bob", knot=slash_str)

    # WHEN
    bob_belief.set_voiceunit(yao_voiceunit)

    # THEN
    assert bob_belief.voices.get(yao_str).groupmark == slash_str
    x_voices = {yao_voiceunit.voice_name: deepcopy_yao_voiceunit}
    assert bob_belief.voices != x_voices
    deepcopy_yao_voiceunit.groupmark = bob_belief.knot
    assert bob_belief.voices == x_voices


def test_BeliefUnit_set_voice_DoesNotSet_voice_name_membership():
    # ESTABLISH
    x_respect_grain = 5
    yao_belief = beliefunit_shop("Yao", respect_grain=x_respect_grain)
    zia_str = "Zia"

    # WHEN
    yao_belief.set_voiceunit(voiceunit_shop(zia_str), auto_set_membership=False)

    # THEN
    assert yao_belief.get_voice(zia_str).get_membership(zia_str) is None


def test_BeliefUnit_set_voice_DoesSet_voice_name_membership():
    # ESTABLISH
    x_respect_grain = 5
    yao_belief = beliefunit_shop("Yao", respect_grain=x_respect_grain)
    zia_str = "Zia"

    # WHEN
    yao_belief.set_voiceunit(voiceunit_shop(zia_str))

    # THEN
    zia_zia_membership = yao_belief.get_voice(zia_str).get_membership(zia_str)
    assert zia_zia_membership is not None
    assert zia_zia_membership.group_cred_lumen == 1
    assert zia_zia_membership.group_debt_lumen == 1


def test_BeliefUnit_set_voice_DoesNotOverRide_voice_name_membership():
    # ESTABLISH
    x_respect_grain = 5
    yao_belief = beliefunit_shop("Yao", respect_grain=x_respect_grain)
    zia_str = "Zia"
    ohio_str = ";Ohio"
    zia_ohio_credit_w = 33
    zia_ohio_debt_w = 44
    zia_voiceunit = voiceunit_shop(zia_str)
    zia_voiceunit.add_membership(ohio_str, zia_ohio_credit_w, zia_ohio_debt_w)

    # WHEN
    yao_belief.set_voiceunit(zia_voiceunit)

    # THEN
    zia_ohio_membership = yao_belief.get_voice(zia_str).get_membership(ohio_str)
    assert zia_ohio_membership is not None
    assert zia_ohio_membership.group_cred_lumen == zia_ohio_credit_w
    assert zia_ohio_membership.group_debt_lumen == zia_ohio_debt_w
    zia_zia_membership = yao_belief.get_voice(zia_str).get_membership(zia_str)
    assert zia_zia_membership is None


def test_BeliefUnit_add_voiceunit_Sets_voices():
    # ESTABLISH
    x_respect_grain = 6
    yao_belief = beliefunit_shop("Yao", respect_grain=x_respect_grain)
    zia_str = "Zia"
    sue_str = "Sue"
    xio_str = "Xio"

    # WHEN
    yao_belief.add_voiceunit(zia_str, voice_cred_lumen=13, voice_debt_lumen=8)
    yao_belief.add_voiceunit(sue_str, voice_debt_lumen=5)
    yao_belief.add_voiceunit(xio_str, voice_cred_lumen=17)

    # THEN
    assert len(yao_belief.voices) == 3
    assert len(yao_belief.get_voiceunit_group_titles_dict()) == 3
    assert yao_belief.voices.get(xio_str).voice_cred_lumen == 17
    assert yao_belief.voices.get(sue_str).voice_debt_lumen == 5
    assert yao_belief.voices.get(xio_str).respect_grain == x_respect_grain


def test_BeliefUnit_voice_exists_ReturnsObj():
    # ESTABLISH
    bob_belief = beliefunit_shop("Bob")
    yao_str = "Yao"

    # WHEN / THEN
    assert bob_belief.voice_exists(yao_str) is False

    # ESTABLISH
    bob_belief.add_voiceunit(yao_str)

    # WHEN / THEN
    assert bob_belief.voice_exists(yao_str)


def test_BeliefUnit_set_voice_Creates_membership():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    zia_str = "Zia"
    before_zia_credit = 7
    before_zia_debt = 17
    yao_belief.add_voiceunit(zia_str, before_zia_credit, before_zia_debt)
    zia_voiceunit = yao_belief.get_voice(zia_str)
    zia_membership = zia_voiceunit.get_membership(zia_str)
    assert zia_membership.group_cred_lumen != before_zia_credit
    assert zia_membership.group_debt_lumen != before_zia_debt
    assert zia_membership.group_cred_lumen == 1
    assert zia_membership.group_debt_lumen == 1

    # WHEN
    after_zia_credit = 11
    after_zia_debt = 13
    yao_belief.set_voiceunit(voiceunit_shop(zia_str, after_zia_credit, after_zia_debt))

    # THEN
    assert zia_membership.group_cred_lumen != after_zia_credit
    assert zia_membership.group_debt_lumen != after_zia_debt
    assert zia_membership.group_cred_lumen == 1
    assert zia_membership.group_debt_lumen == 1


def test_BeliefUnit_edit_voice_RaiseExceptionWhenVoiceDoesNotExist():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    zia_str = "Zia"
    zia_voice_cred_lumen = 55

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_belief.edit_voiceunit(zia_str, voice_cred_lumen=zia_voice_cred_lumen)

    # THEN
    assert str(excinfo.value) == f"VoiceUnit '{zia_str}' does not exist."


def test_BeliefUnit_edit_voice_UpdatesObj():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    zia_str = "Zia"
    old_zia_voice_cred_lumen = 55
    old_zia_voice_debt_lumen = 66
    yao_belief.set_voiceunit(
        voiceunit_shop(
            zia_str,
            old_zia_voice_cred_lumen,
            old_zia_voice_debt_lumen,
        )
    )
    zia_voiceunit = yao_belief.get_voice(zia_str)
    assert zia_voiceunit.voice_cred_lumen == old_zia_voice_cred_lumen
    assert zia_voiceunit.voice_debt_lumen == old_zia_voice_debt_lumen

    # WHEN
    new_zia_voice_cred_lumen = 22
    new_zia_voice_debt_lumen = 33
    yao_belief.edit_voiceunit(
        voice_name=zia_str,
        voice_cred_lumen=new_zia_voice_cred_lumen,
        voice_debt_lumen=new_zia_voice_debt_lumen,
    )

    # THEN
    assert zia_voiceunit.voice_cred_lumen == new_zia_voice_cred_lumen
    assert zia_voiceunit.voice_debt_lumen == new_zia_voice_debt_lumen


def test_BeliefUnit_get_voice_ReturnsObj():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    zia_str = "Zia"
    sue_str = "Sue"
    yao_belief.add_voiceunit(zia_str)
    yao_belief.add_voiceunit(sue_str)

    # WHEN
    zia_voice = yao_belief.get_voice(zia_str)
    sue_voice = yao_belief.get_voice(sue_str)

    # THEN
    assert zia_voice == yao_belief.voices.get(zia_str)
    assert sue_voice == yao_belief.voices.get(sue_str)
