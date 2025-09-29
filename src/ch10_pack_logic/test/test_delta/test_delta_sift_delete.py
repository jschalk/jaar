# from src.ch07_belief_logic.belief_tool import pass
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch09_belief_atom_logic.atom_main import beliefatom_shop
from src.ch10_pack_logic._ref.ch10_keywords import (
    Ch04Keywords as wx,
    Ch09Keywords as wx,
    belief_voice_membership_str,
    belief_voiceunit_str,
)
from src.ch10_pack_logic.delta import beliefdelta_shop, get_minimal_beliefdelta


def test_get_minimal_beliefdelta_ReturnsObjWithoutUnecessaryDELETE_belief_voiceunit():
    # ESTABLISH beliefdelta with 2 voiceunits, beliefdelta DELETE 3 beliefdeltas,
    # assert beliefdelta has 3 atoms
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_voiceunit(yao_str)
    sue_belief.add_voiceunit(bob_str)

    voices_beliefdelta = beliefdelta_shop()
    bob_atom = beliefatom_shop(belief_voiceunit_str(), wx.DELETE)
    bob_atom.set_arg(wx.voice_name, bob_str)
    yao_atom = beliefatom_shop(belief_voiceunit_str(), wx.DELETE)
    yao_atom.set_arg(wx.voice_name, yao_str)
    zia_atom = beliefatom_shop(belief_voiceunit_str(), wx.DELETE)
    zia_atom.set_arg(wx.voice_name, zia_str)
    voices_beliefdelta.set_beliefatom(bob_atom)
    voices_beliefdelta.set_beliefatom(yao_atom)
    voices_beliefdelta.set_beliefatom(zia_atom)
    assert len(voices_beliefdelta.get_sorted_beliefatoms()) == 3
    assert len(sue_belief.voices) == 2

    # WHEN
    new_beliefdelta = get_minimal_beliefdelta(voices_beliefdelta, sue_belief)

    # THEN
    assert len(new_beliefdelta.get_sorted_beliefatoms()) == 2


def test_sift_ReturnsObjWithoutUnecessaryDELETE_belief_voice_membership():
    # ESTABLISH beliefdelta with 2 voiceunits, beliefdelta DELETE 3 beliefdeltas,
    # assert beliefdelta has 3 atoms
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_voiceunit(yao_str)
    sue_belief.add_voiceunit(bob_str)
    yao_voiceunit = sue_belief.get_voice(yao_str)
    run_str = ";run"
    swim_str = ";swim"
    run_str = ";run"
    yao_voiceunit.add_membership(run_str)
    yao_voiceunit.add_membership(swim_str)
    print(f"{yao_voiceunit.memberships.keys()=}")

    voices_beliefdelta = beliefdelta_shop()
    bob_run_atom = beliefatom_shop(belief_voice_membership_str(), wx.DELETE)
    bob_run_atom.set_arg(wx.voice_name, bob_str)
    bob_run_atom.set_arg(wx.group_title, run_str)
    yao_run_atom = beliefatom_shop(belief_voice_membership_str(), wx.DELETE)
    yao_run_atom.set_arg(wx.voice_name, yao_str)
    yao_run_atom.set_arg(wx.group_title, run_str)
    zia_run_atom = beliefatom_shop(belief_voice_membership_str(), wx.DELETE)
    zia_run_atom.set_arg(wx.voice_name, zia_str)
    zia_run_atom.set_arg(wx.group_title, run_str)
    voices_beliefdelta.set_beliefatom(bob_run_atom)
    voices_beliefdelta.set_beliefatom(yao_run_atom)
    voices_beliefdelta.set_beliefatom(zia_run_atom)
    print(f"{len(voices_beliefdelta.get_dimen_sorted_beliefatoms_list())=}")
    assert len(voices_beliefdelta.get_dimen_sorted_beliefatoms_list()) == 3

    # WHEN
    new_beliefdelta = get_minimal_beliefdelta(voices_beliefdelta, sue_belief)

    # THEN
    assert len(new_beliefdelta.get_dimen_sorted_beliefatoms_list()) == 1
