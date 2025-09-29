from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch09_belief_atom_logic.atom_main import beliefatom_shop
from src.ch10_pack_logic._ref.ch10_keywords import (
    Ch01Keywords as wx,
    Ch09Keywords as wx,
    belief_voiceunit_str,
    voice_cred_points_str,
    voice_name_str,
)
from src.ch10_pack_logic.delta import beliefdelta_shop, get_minimal_beliefdelta


# all other atom dimens are covered by test_sift_atom tests
def test_get_minimal_beliefdelta_ReturnsObjUPDATEBeliefAtom_belief_voiceunit():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    old_bob_voice_cred_points = 34
    new_bob_voice_cred_points = 7
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_voiceunit(bob_str, old_bob_voice_cred_points)
    sue_belief.add_voiceunit(yao_str)

    voices_beliefdelta = beliefdelta_shop()
    bob_atom = beliefatom_shop(belief_voiceunit_str(), wx.INSERT)
    bob_atom.set_arg(voice_name_str(), bob_str)
    bob_atom.set_arg(voice_cred_points_str(), new_bob_voice_cred_points)
    yao_atom = beliefatom_shop(belief_voiceunit_str(), wx.INSERT)
    yao_atom.set_arg(voice_name_str(), yao_str)
    voices_beliefdelta.set_beliefatom(bob_atom)
    voices_beliefdelta.set_beliefatom(yao_atom)
    assert len(voices_beliefdelta.get_sorted_beliefatoms()) == 2

    # WHEN
    new_beliefdelta = get_minimal_beliefdelta(voices_beliefdelta, sue_belief)

    # THEN
    assert len(new_beliefdelta.get_sorted_beliefatoms()) == 1
    new_beliefatom = new_beliefdelta.get_sorted_beliefatoms()[0]
    assert new_beliefatom.crud_str == wx.UPDATE
    new_jvalues = new_beliefatom.get_jvalues_dict()
    assert new_jvalues == {voice_cred_points_str(): new_bob_voice_cred_points}
