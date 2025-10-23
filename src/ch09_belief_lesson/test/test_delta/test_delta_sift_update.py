from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch08_belief_atom.atom_main import beliefatom_shop
from src.ch09_belief_lesson.delta import beliefdelta_shop, get_minimal_beliefdelta
from src.ref.keywords import Ch09Keywords as kw


# all other atom dimens are covered by test_sift_atom tests
def test_get_minimal_beliefdelta_ReturnsObjUPDATEBeliefAtom_belief_voiceunit():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    old_bob_voice_cred_lumen = 34
    new_bob_voice_cred_lumen = 7
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_voiceunit(bob_str, old_bob_voice_cred_lumen)
    sue_belief.add_voiceunit(yao_str)

    voices_beliefdelta = beliefdelta_shop()
    bob_atom = beliefatom_shop(kw.belief_voiceunit, kw.INSERT)
    bob_atom.set_arg(kw.voice_name, bob_str)
    bob_atom.set_arg(kw.voice_cred_lumen, new_bob_voice_cred_lumen)
    yao_atom = beliefatom_shop(kw.belief_voiceunit, kw.INSERT)
    yao_atom.set_arg(kw.voice_name, yao_str)
    voices_beliefdelta.set_beliefatom(bob_atom)
    voices_beliefdelta.set_beliefatom(yao_atom)
    assert len(voices_beliefdelta.get_sorted_beliefatoms()) == 2

    # WHEN
    new_beliefdelta = get_minimal_beliefdelta(voices_beliefdelta, sue_belief)

    # THEN
    assert len(new_beliefdelta.get_sorted_beliefatoms()) == 1
    new_beliefatom = new_beliefdelta.get_sorted_beliefatoms()[0]
    assert new_beliefatom.crud_str == kw.UPDATE
    new_jvalues = new_beliefatom.get_jvalues_dict()
    assert new_jvalues == {kw.voice_cred_lumen: new_bob_voice_cred_lumen}
