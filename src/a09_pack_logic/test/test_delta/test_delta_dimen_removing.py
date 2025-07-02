from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    believer_personunit_str,
    person_name_str,
)
from src.a08_believer_atom_logic.test._util.a08_str import INSERT_str
from src.a09_pack_logic.delta import believerdelta_shop, get_dimens_cruds_believerdelta


def test_BelieverDelta_get_dimens_cruds_believerdelta_ReturnsObjWithCorrectDimensAndCRUDsBy_personunit_insert():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    before_sue_believer = believerunit_shop(sue_str)
    before_sue_believer.add_personunit(yao_str)
    after_sue_believer = believerunit_shop(sue_str)
    bob_str = "Bob"
    bob_person_cred_points = 33
    bob_person_debt_points = 44
    after_sue_believer.add_personunit(
        bob_str, bob_person_cred_points, bob_person_debt_points
    )
    after_sue_believer.set_l1_plan(planunit_shop("casa"))
    old_believerdelta = believerdelta_shop()
    old_believerdelta.add_all_different_believeratoms(
        before_sue_believer, after_sue_believer
    )

    dimen_set = [believer_personunit_str()]
    curd_set = {INSERT_str()}
    new_believerdelta = get_dimens_cruds_believerdelta(
        old_believerdelta, dimen_set, curd_set
    )

    # THEN
    new_believerdelta.get_dimen_sorted_believeratoms_list()
    assert len(new_believerdelta.get_dimen_sorted_believeratoms_list()) == 1
    sue_insert_dict = new_believerdelta.believeratoms.get(INSERT_str())
    sue_personunit_dict = sue_insert_dict.get(believer_personunit_str())
    bob_believeratom = sue_personunit_dict.get(bob_str)
    assert bob_believeratom.get_value(person_name_str()) == bob_str
    assert bob_believeratom.get_value("person_cred_points") == bob_person_cred_points
    assert bob_believeratom.get_value("person_debt_points") == bob_person_debt_points
