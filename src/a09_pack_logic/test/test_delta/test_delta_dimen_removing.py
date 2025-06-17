from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic._util.a06_str import acct_name_str, plan_acctunit_str
from src.a06_plan_logic.plan import planunit_shop
from src.a08_plan_atom_logic._util.a08_str import INSERT_str
from src.a09_pack_logic.delta import get_dimens_cruds_plandelta, plandelta_shop


def test_PlanDelta_get_dimens_cruds_plandelta_ReturnsObjWithCorrectDimensAndCRUDsBy_acctunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    before_sue_plan = planunit_shop(sue_str)
    before_sue_plan.add_acctunit(yao_str)
    after_sue_plan = planunit_shop(sue_str)
    bob_str = "Bob"
    bob_credit_score = 33
    bob_debt_score = 44
    after_sue_plan.add_acctunit(bob_str, bob_credit_score, bob_debt_score)
    after_sue_plan.set_l1_concept(conceptunit_shop("casa"))
    old_plandelta = plandelta_shop()
    old_plandelta.add_all_different_planatoms(before_sue_plan, after_sue_plan)

    dimen_set = [plan_acctunit_str()]
    curd_set = {INSERT_str()}
    new_plandelta = get_dimens_cruds_plandelta(old_plandelta, dimen_set, curd_set)

    # THEN
    new_plandelta.get_dimen_sorted_planatoms_list()
    assert len(new_plandelta.get_dimen_sorted_planatoms_list()) == 1
    sue_insert_dict = new_plandelta.planatoms.get(INSERT_str())
    sue_acctunit_dict = sue_insert_dict.get(plan_acctunit_str())
    bob_planatom = sue_acctunit_dict.get(bob_str)
    assert bob_planatom.get_value(acct_name_str()) == bob_str
    assert bob_planatom.get_value("credit_score") == bob_credit_score
    assert bob_planatom.get_value("debt_score") == bob_debt_score
