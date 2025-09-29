from src.ch06_plan_logic.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch10_pack_logic._ref.ch10_keywords import (
    Ch01Keywords as wx,
    Ch04Keywords as wx,
    Ch07Keywords as wx,
)
from src.ch10_pack_logic.delta import beliefdelta_shop, get_dimens_cruds_beliefdelta


def test_BeliefDelta_get_dimens_cruds_beliefdelta_ReturnsObjWithCorrectDimensAndCRUDsBy_voiceunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    before_sue_belief = beliefunit_shop(sue_str)
    before_sue_belief.add_voiceunit(yao_str)
    after_sue_belief = beliefunit_shop(sue_str)
    bob_str = "Bob"
    bob_voice_cred_points = 33
    bob_voice_debt_points = 44
    after_sue_belief.add_voiceunit(
        bob_str, bob_voice_cred_points, bob_voice_debt_points
    )
    after_sue_belief.set_l1_plan(planunit_shop("casa"))
    old_beliefdelta = beliefdelta_shop()
    old_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    dimen_set = [wx.belief_voiceunit]
    curd_set = {wx.INSERT}

    # WHEN
    new_beliefdelta = get_dimens_cruds_beliefdelta(old_beliefdelta, dimen_set, curd_set)

    # THEN
    new_beliefdelta.get_dimen_sorted_beliefatoms_list()
    assert len(new_beliefdelta.get_dimen_sorted_beliefatoms_list()) == 1
    sue_insert_dict = new_beliefdelta.beliefatoms.get(wx.INSERT)
    sue_voiceunit_dict = sue_insert_dict.get(wx.belief_voiceunit)
    bob_beliefatom = sue_voiceunit_dict.get(bob_str)
    assert bob_beliefatom.get_value(wx.voice_name) == bob_str
    assert bob_beliefatom.get_value("voice_cred_points") == bob_voice_cred_points
    assert bob_beliefatom.get_value("voice_debt_points") == bob_voice_debt_points
