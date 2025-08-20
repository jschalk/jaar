from src.a05_plan_logic.plan import planunit_shop
from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a06_belief_logic.test._util.a06_str import (
    belief_partnerunit_str,
    partner_name_str,
)
from src.a08_belief_atom_logic.test._util.a08_str import INSERT_str
from src.a09_pack_logic.delta import beliefdelta_shop, get_dimens_cruds_beliefdelta


def test_BeliefDelta_get_dimens_cruds_beliefdelta_ReturnsObjWithCorrectDimensAndCRUDsBy_partnerunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    before_sue_belief = beliefunit_shop(sue_str)
    before_sue_belief.add_partnerunit(yao_str)
    after_sue_belief = beliefunit_shop(sue_str)
    bob_str = "Bob"
    bob_partner_cred_points = 33
    bob_partner_debt_points = 44
    after_sue_belief.add_partnerunit(
        bob_str, bob_partner_cred_points, bob_partner_debt_points
    )
    after_sue_belief.set_l1_plan(planunit_shop("casa"))
    old_beliefdelta = beliefdelta_shop()
    old_beliefdelta.add_all_different_beliefatoms(before_sue_belief, after_sue_belief)

    dimen_set = [belief_partnerunit_str()]
    curd_set = {INSERT_str()}

    # WHEN
    new_beliefdelta = get_dimens_cruds_beliefdelta(old_beliefdelta, dimen_set, curd_set)

    # THEN
    new_beliefdelta.get_dimen_sorted_beliefatoms_list()
    assert len(new_beliefdelta.get_dimen_sorted_beliefatoms_list()) == 1
    sue_insert_dict = new_beliefdelta.beliefatoms.get(INSERT_str())
    sue_partnerunit_dict = sue_insert_dict.get(belief_partnerunit_str())
    bob_beliefatom = sue_partnerunit_dict.get(bob_str)
    assert bob_beliefatom.get_value(partner_name_str()) == bob_str
    assert bob_beliefatom.get_value("partner_cred_points") == bob_partner_cred_points
    assert bob_beliefatom.get_value("partner_debt_points") == bob_partner_debt_points
