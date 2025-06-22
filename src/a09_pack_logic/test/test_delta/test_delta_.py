from pytest import raises as pytest_raises
from src.a00_data_toolbox.dict_toolbox import x_is_json
from src.a01_term_logic.rope import create_rope, to_rope
from src.a03_group_logic.acct import acctunit_shop
from src.a05_concept_logic.concept import get_default_bank_label as root_label
from src.a06_plan_logic.plan import planunit_shop
from src.a06_plan_logic.test._util.a06_str import (
    acct_cred_points_str,
    acct_debt_points_str,
    acct_name_str,
    awardee_title_str,
    concept_rope_str,
    group_title_str,
    plan_acct_membership_str,
    plan_acctunit_str,
    plan_concept_awardlink_str,
    plan_conceptunit_str,
    planunit_str,
)
from src.a08_plan_atom_logic.atom import planatom_shop
from src.a08_plan_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import (
    PlanDelta,
    get_plandelta_from_ordered_dict,
    plan_built_from_delta_is_valid,
    plandelta_shop,
)
from src.a09_pack_logic.test._util.example_deltas import (
    get_plandelta_example1,
    get_plandelta_sue_example,
)


def test_PlanDelta_exists():
    # ESTABLISH / WHEN
    x_plandelta = PlanDelta()

    # THEN
    assert x_plandelta.planatoms is None
    assert x_plandelta._plan_build_validated is None


def test_plandelta_shop_ReturnsObj():
    # ESTABLISH / WHEN
    ex1_plandelta = plandelta_shop()

    # THEN
    assert ex1_plandelta.planatoms == {}
    assert ex1_plandelta._plan_build_validated is False


def test_PlanDelta_set_planatom_CorrectlySets_PlanUnitSimpleAttrs():
    # ESTABLISH
    ex1_plandelta = plandelta_shop()
    attribute_value = 55
    dimen = planunit_str()
    opt1_arg = "tally"
    jvalues = {opt1_arg: attribute_value}
    jkeys = {}
    plan_mass_planatom = planatom_shop(
        dimen,
        UPDATE_str(),
        jkeys=jkeys,
        jvalues=jvalues,
    )
    assert ex1_plandelta.planatoms == {}
    assert plan_mass_planatom.atom_order is None

    # WHEN
    ex1_plandelta.set_planatom(plan_mass_planatom)

    # THEN
    assert len(ex1_plandelta.planatoms) == 1
    x_update_dict = ex1_plandelta.planatoms.get(UPDATE_str())
    # print(f"{x_update_dict=}")
    x_dimen_planatom = x_update_dict.get(dimen)
    print(f"{x_dimen_planatom=}")
    assert x_dimen_planatom == plan_mass_planatom
    assert plan_mass_planatom.atom_order is not None


def test_PlanDelta_set_planatom_RaisesErrorWhen_is_valid_IsFalse():
    # ESTABLISH
    ex1_plandelta = plandelta_shop()
    x_dimen = plan_acctunit_str()
    plan_mass_planatom = planatom_shop(x_dimen, UPDATE_str())

    # WHEN
    with pytest_raises(Exception) as excinfo:
        ex1_plandelta.set_planatom(plan_mass_planatom)
    assert (
        str(excinfo.value)
        == f"""'{x_dimen}' UPDATE PlanAtom is invalid
                x_planatom.is_jkeys_valid()=False
                x_planatom.is_jvalues_valid()=True"""
    )


def test_ChangUnit_planatom_exists_ReturnsObj_plan_acctunit_str():
    # ESTABLISH
    bob_str = "Bob"
    x_plandelta = plandelta_shop()
    bob_planatom = planatom_shop(plan_acctunit_str(), INSERT_str())
    bob_planatom.set_arg(acct_name_str(), bob_str)
    assert not x_plandelta.planatom_exists(bob_planatom)

    # WHEN
    x_plandelta.set_planatom(bob_planatom)

    # THEN
    assert x_plandelta.planatom_exists(bob_planatom)


def test_ChangUnit_planatom_exists_ReturnsObj_plan_acct_membership_str():
    # ESTABLISH
    bob_str = "Bob"
    iowa_str = ";Iowa"
    x_plandelta = plandelta_shop()
    bob_iowa_planatom = planatom_shop(plan_acct_membership_str(), INSERT_str())
    bob_iowa_planatom.set_arg(group_title_str(), iowa_str)
    bob_iowa_planatom.set_arg(acct_name_str(), bob_str)
    assert not x_plandelta.planatom_exists(bob_iowa_planatom)

    # WHEN
    x_plandelta.set_planatom(bob_iowa_planatom)

    # THEN
    assert x_plandelta.planatom_exists(bob_iowa_planatom)


def test_PlanDelta_get_atom_ReturnsObj():
    # ESTABLISH
    ex1_plandelta = plandelta_shop()
    opt_arg1 = "tally"
    opt_value = 55
    planunit_planatom = planatom_shop(planunit_str(), UPDATE_str())
    planunit_planatom.set_jvalue(x_key=opt_arg1, x_value=opt_value)
    ex1_plandelta.set_planatom(planunit_planatom)

    # WHEN
    gen_planatom = ex1_plandelta.get_planatom(
        UPDATE_str(), dimen=planunit_str(), jkeys=[]
    )

    # THEN
    assert gen_planatom == planunit_planatom


def test_PlanDelta_add_planatom_CorrectlySets_PlanUnitSimpleAttrs():
    # ESTABLISH
    ex1_plandelta = plandelta_shop()
    assert ex1_plandelta.planatoms == {}

    # WHEN
    op2_arg = "tally"
    op2_value = 55
    jkeys = {}
    jvalues = {op2_arg: op2_value}
    ex1_plandelta.add_planatom(
        planunit_str(),
        UPDATE_str(),
        jkeys,
        jvalues=jvalues,
    )

    # THEN
    assert len(ex1_plandelta.planatoms) == 1
    x_update_dict = ex1_plandelta.planatoms.get(UPDATE_str())
    x_planatom = x_update_dict.get(planunit_str())
    assert x_planatom is not None
    assert x_planatom.dimen == planunit_str()


def test_PlanDelta_add_planatom_CorrectlySets_PlanUnit_acctunits():
    # ESTABLISH
    ex1_plandelta = plandelta_shop()
    assert ex1_plandelta.planatoms == {}

    # WHEN
    bob_str = "Bob"
    bob_acct_cred_points = 55
    bob_acct_debt_points = 66
    bob_acctunit = acctunit_shop(bob_str, bob_acct_cred_points, bob_acct_debt_points)
    cw_str = acct_cred_points_str()
    dw_str = acct_debt_points_str()
    print(f"{bob_acctunit.get_dict()=}")
    bob_required_dict = {acct_name_str(): bob_acctunit.get_dict().get(acct_name_str())}
    bob_optional_dict = {cw_str: bob_acctunit.get_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_acctunit.get_dict().get(dw_str)
    print(f"{bob_required_dict=}")
    acctunit_str = plan_acctunit_str()
    ex1_plandelta.add_planatom(
        dimen=acctunit_str,
        crud_str=INSERT_str(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )
    # THEN
    assert len(ex1_plandelta.planatoms) == 1
    assert (
        ex1_plandelta.planatoms.get(INSERT_str()).get(acctunit_str).get(bob_str)
        is not None
    )


def test_PlanDelta_get_crud_planatoms_list_ReturnsObj():
    # ESTABLISH
    ex1_plandelta = get_plandelta_example1()
    assert len(ex1_plandelta.planatoms.get(UPDATE_str()).keys()) == 1
    assert ex1_plandelta.planatoms.get(INSERT_str()) is None
    assert len(ex1_plandelta.planatoms.get(DELETE_str()).keys()) == 1

    # WHEN
    sue_atom_order_dict = ex1_plandelta._get_crud_planatoms_list()

    # THEN
    assert len(sue_atom_order_dict) == 2
    print(f"{sue_atom_order_dict.keys()=}")
    # print(f"{sue_atom_order_dict.get(UPDATE_str())=}")
    assert len(sue_atom_order_dict.get(UPDATE_str())) == 1
    assert len(sue_atom_order_dict.get(DELETE_str())) == 1
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_PlanDelta_get_dimen_sorted_planatoms_list_ReturnsObj_Scenario0_rope():
    # ESTABLISH
    ex1_plandelta = get_plandelta_example1()
    update_dict = ex1_plandelta.planatoms.get(UPDATE_str())
    assert len(update_dict.keys()) == 1
    print(f"{update_dict.keys()=}")
    assert ex1_plandelta.planatoms.get(INSERT_str()) is None
    delete_dict = ex1_plandelta.planatoms.get(DELETE_str())
    assert len(delete_dict.keys()) == 1

    # WHEN
    sue_atoms_list = ex1_plandelta.get_dimen_sorted_planatoms_list()

    # THEN
    assert len(sue_atoms_list) == 2
    assert sue_atoms_list[0] == update_dict.get(planunit_str())
    z_atom = sue_atoms_list[1]
    print(f"{z_atom=}")
    print(delete_dict.get(plan_acctunit_str()).keys())
    zia_acctunit_delete = delete_dict.get(plan_acctunit_str()).get("Zia")
    assert sue_atoms_list[1] == zia_acctunit_delete


# def test_PlanDelta_add_planatom_CorrectlySets_PlanUnit_max_tree_traverse():
#     # ESTABLISH
#     ex1_plandelta = plandelta_shop(get_sue_rope())
#     assert ex1_plandelta.planatoms == {}

#     # WHEN
#     opt2_value = 55
#     dimen = planunit_str()
#     opt2_arg = "mass"
#     mass_planatom = planatom_shop(dimen, UPDATE_str())
#     mass_planatom.set_jvalue(opt2_arg, opt2_value)
#     ex1_plandelta.set_planatom(mass_planatom)
#     # THEN
#     assert len(ex1_plandelta.planatoms.get(UPDATE_str()).keys()) == 1
#     sue_planunit_dict = ex1_plandelta.planatoms.get(UPDATE_str())
#     sue_mass_planatom = sue_planunit_dict.get(dimen)
#     print(f"{sue_mass_planatom=}")
#     assert mass_planatom == sue_mass_planatom

#     # WHEN
#     new2_value = 66
#     x_attribute = "max_tree_traverse"
#     jkeys = {x_attribute: new2_value}
#     x_planatom = planatom_shop(x_attribute, UPDATE_str(), None, jkeys)
#     ex1_plandelta.set_planatom(x_planatom)
#     # THEN
#     print(f"{ex1_plandelta.planatoms.keys()=}")
#     print(f"{ex1_plandelta.planatoms.get(UPDATE_str()).keys()=}")
#     assert len(ex1_plandelta.planatoms.get(UPDATE_str()).keys()) == 2
#     assert x_planatom == ex1_plandelta.planatoms.get(UPDATE_str()).get(x_attribute)

#     # WHEN
#     new3_value = 77
#     x_attribute = "credor_respect"
#     jkeys = {x_attribute: new3_value}
#     x_planatom = planatom_shop(x_attribute, UPDATE_str(), None, jkeys)
#     ex1_plandelta.set_planatom(x_planatom)
#     # THEN
#     assert len(ex1_plandelta.planatoms.get(UPDATE_str()).keys()) == 3
#     assert x_planatom == ex1_plandelta.planatoms.get(UPDATE_str()).get(x_attribute)

#     # WHEN
#     new4_value = 88
#     x_attribute = "debtor_respect"
#     jkeys = {x_attribute: new4_value}
#     x_planatom = planatom_shop(x_attribute, UPDATE_str(), None, jkeys)
#     ex1_plandelta.set_planatom(x_planatom)
#     # THEN
#     assert len(ex1_plandelta.planatoms.get(UPDATE_str()).keys()) == 4
#     assert x_planatom == ex1_plandelta.planatoms.get(UPDATE_str()).get(x_attribute)


def test_PlanDelta_get_sorted_planatoms_ReturnsObj():
    # ESTABLISH
    ex1_plandelta = get_plandelta_example1()
    update_dict = ex1_plandelta.planatoms.get(UPDATE_str())
    assert len(update_dict.keys()) == 1
    assert update_dict.get(planunit_str()) is not None
    print(f"atom_order 28 {ex1_plandelta.planatoms.get(UPDATE_str()).keys()=}")
    delete_dict = ex1_plandelta.planatoms.get(DELETE_str())
    assert len(delete_dict.keys()) == 1
    assert delete_dict.get(plan_acctunit_str()) is not None
    print(f"atom_order 26 {ex1_plandelta.planatoms.get(DELETE_str()).keys()=}")

    # WHEN
    sue_atom_order_list = ex1_plandelta.get_sorted_planatoms()

    # THEN
    assert len(sue_atom_order_list) == 2
    print(delete_dict.get(plan_acctunit_str()).keys())
    zia_acctunit_delete = delete_dict.get(plan_acctunit_str()).get("Zia")
    # for planatom in sue_atom_order_list:
    #     print(f"{planatom.atom_order=}")
    assert sue_atom_order_list[0] == zia_acctunit_delete
    assert sue_atom_order_list[1] == update_dict.get(planunit_str())
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_PlanDelta_get_sorted_planatoms_ReturnsObj_ConceptUnitsSorted():
    # ESTABLISH
    x_bank_label = root_label()
    root_rope = to_rope(x_bank_label)
    sports_str = "sports"
    sports_rope = create_rope(x_bank_label, sports_str)
    knee_str = "knee"
    knee_rope = create_rope(x_bank_label, knee_str)
    x_dimen = plan_conceptunit_str()
    sports_insert_conceptunit_planatom = planatom_shop(x_dimen, INSERT_str())
    sports_insert_conceptunit_planatom.set_jkey(concept_rope_str(), sports_rope)
    knee_insert_conceptunit_planatom = planatom_shop(x_dimen, INSERT_str())
    knee_insert_conceptunit_planatom.set_jkey(concept_rope_str(), knee_rope)
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(knee_insert_conceptunit_planatom)
    x_plandelta.set_planatom(sports_insert_conceptunit_planatom)

    # WHEN
    x_atom_order_list = x_plandelta.get_sorted_planatoms()

    # THEN
    assert len(x_atom_order_list) == 2
    # for planatom in x_atom_order_list:
    #     print(f"{planatom.jkeys=}")
    assert x_atom_order_list[0] == knee_insert_conceptunit_planatom
    assert x_atom_order_list[1] == sports_insert_conceptunit_planatom
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_PlanDelta_get_sorted_planatoms_ReturnsObj_Rope_Sorted():
    # ESTABLISH
    x_bank_label = root_label()
    sports_str = "sports"
    sports_rope = create_rope(x_bank_label, sports_str)
    knee_str = "knee"
    knee_rope = create_rope(sports_rope, knee_str)
    x_dimen = plan_concept_awardlink_str()
    swimmers_str = ",Swimmers"
    sports_awardlink_planatom = planatom_shop(x_dimen, INSERT_str())
    sports_awardlink_planatom.set_jkey(awardee_title_str(), swimmers_str)
    sports_awardlink_planatom.set_jkey(concept_rope_str(), sports_rope)
    knee_awardlink_planatom = planatom_shop(x_dimen, INSERT_str())
    knee_awardlink_planatom.set_jkey(awardee_title_str(), swimmers_str)
    knee_awardlink_planatom.set_jkey(concept_rope_str(), knee_rope)
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(knee_awardlink_planatom)
    x_plandelta.set_planatom(sports_awardlink_planatom)

    # WHEN
    x_atom_order_list = x_plandelta.get_sorted_planatoms()

    # THEN
    assert len(x_atom_order_list) == 2
    # for planatom in x_atom_order_list:
    #     print(f"{planatom.jkeys=}")
    assert x_atom_order_list[0] == sports_awardlink_planatom
    assert x_atom_order_list[1] == knee_awardlink_planatom
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_plan_built_from_delta_is_valid_ReturnsObjEstablishWithNoPlan_scenario1():
    # ESTABLISH
    sue_plandelta = plandelta_shop()

    x_planatom = planatom_shop(planunit_str(), UPDATE_str())
    x_attribute = "credor_respect"
    x_planatom.set_jvalue(x_attribute, 100)
    sue_plandelta.set_planatom(x_planatom)

    dimen = plan_acctunit_str()
    zia_str = "Zia"
    x_planatom = planatom_shop(dimen, INSERT_str())
    x_planatom.set_arg(acct_name_str(), zia_str)
    x_planatom.set_arg(acct_cred_points_str(), "70 is the number")
    sue_plandelta.set_planatom(x_planatom)
    print(f"{sue_plandelta=}")

    # WHEN / THEN
    assert plan_built_from_delta_is_valid(sue_plandelta) is False


def test_plan_built_from_delta_is_valid_ReturnsObjEstablishWithNoPlan_scenario2():
    sue_plandelta = plandelta_shop()
    dimen = plan_acctunit_str()
    # WHEN
    yao_str = "Yao"
    x_planatom = planatom_shop(dimen, INSERT_str())
    x_planatom.set_arg(acct_name_str(), yao_str)
    x_planatom.set_arg(acct_cred_points_str(), 30)
    sue_plandelta.set_planatom(x_planatom)

    # THEN
    assert plan_built_from_delta_is_valid(sue_plandelta)

    # WHEN
    bob_str = "Bob"
    x_planatom = planatom_shop(dimen, INSERT_str())
    x_planatom.set_arg(acct_name_str(), bob_str)
    x_planatom.set_arg(acct_cred_points_str(), "70 is the number")
    sue_plandelta.set_planatom(x_planatom)

    # THEN
    assert plan_built_from_delta_is_valid(sue_plandelta) is False


def test_PlanDelta_get_ordered_planatoms_ReturnsObj_EstablishWithNoStartingNumber():
    # ESTABLISH
    sue_plandelta = plandelta_shop()
    pool_planatom = planatom_shop(planunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_planatom.set_jvalue(pool_attribute, 100)
    sue_plandelta.set_planatom(pool_planatom)
    dimen = plan_acctunit_str()
    zia_str = "Zia"
    zia_planatom = planatom_shop(dimen, INSERT_str())
    zia_planatom.set_arg(acct_name_str(), zia_str)
    zia_planatom.set_arg(acct_cred_points_str(), 70)
    sue_plandelta.set_planatom(zia_planatom)
    sue_plan = planunit_shop("Sue")
    sue_plan.set_credor_respect(100)
    yao_str = "Yao"
    yao_planatom = planatom_shop(dimen, INSERT_str())
    yao_planatom.set_arg(acct_name_str(), yao_str)
    yao_planatom.set_arg(acct_cred_points_str(), 30)
    sue_plandelta.set_planatom(yao_planatom)

    sue_plan = planunit_shop("Sue")
    assert plan_built_from_delta_is_valid(sue_plandelta, sue_plan)

    # WHEN
    plandelta_dict = sue_plandelta.get_ordered_planatoms()

    # THEN
    # delta_zia = plandelta_dict.get(0)
    # delta_yao = plandelta_dict.get(1)
    # delta_pool = plandelta_dict.get(2)
    # assert delta_zia == zia_planatom
    # assert delta_yao == yao_planatom
    # assert delta_pool == pool_planatom
    assert plandelta_dict.get(0) == zia_planatom
    assert plandelta_dict.get(1) == yao_planatom
    assert plandelta_dict.get(2) == pool_planatom


def test_PlanDelta_get_ordered_planatoms_ReturnsObj_EstablishWithStartingNumber():
    # ESTABLISH
    sue_plandelta = plandelta_shop()
    pool_planatom = planatom_shop(planunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_planatom.set_jvalue(pool_attribute, 100)
    sue_plandelta.set_planatom(pool_planatom)
    dimen = plan_acctunit_str()
    zia_str = "Zia"
    zia_planatom = planatom_shop(dimen, INSERT_str())
    zia_planatom.set_arg(acct_name_str(), zia_str)
    zia_planatom.set_arg(acct_cred_points_str(), 70)
    sue_plandelta.set_planatom(zia_planatom)
    sue_plan = planunit_shop("Sue")
    sue_plan.set_credor_respect(100)
    yao_str = "Yao"
    yao_planatom = planatom_shop(dimen, INSERT_str())
    yao_planatom.set_arg(acct_name_str(), yao_str)
    yao_planatom.set_arg(acct_cred_points_str(), 30)
    sue_plandelta.set_planatom(yao_planatom)

    sue_plan = planunit_shop("Sue")
    assert plan_built_from_delta_is_valid(sue_plandelta, sue_plan)

    # WHEN
    plandelta_dict = sue_plandelta.get_ordered_planatoms(5)

    # THEN
    # delta_zia = plandelta_dict.get(0)
    # delta_yao = plandelta_dict.get(1)
    # delta_pool = plandelta_dict.get(2)
    # assert delta_zia == zia_planatom
    # assert delta_yao == yao_planatom
    # assert delta_pool == pool_planatom
    assert plandelta_dict.get(5) == zia_planatom
    assert plandelta_dict.get(6) == yao_planatom
    assert plandelta_dict.get(7) == pool_planatom


def test_PlanDelta_get_ordered_dict_ReturnsObj_EstablishWithStartingNumber():
    # ESTABLISH
    sue_plandelta = plandelta_shop()
    pool_planatom = planatom_shop(planunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_planatom.set_jvalue(pool_attribute, 100)
    sue_plandelta.set_planatom(pool_planatom)
    dimen = plan_acctunit_str()
    zia_str = "Zia"
    zia_planatom = planatom_shop(dimen, INSERT_str())
    zia_planatom.set_arg(acct_name_str(), zia_str)
    zia_planatom.set_arg(acct_cred_points_str(), 70)
    sue_plandelta.set_planatom(zia_planatom)
    sue_plan = planunit_shop("Sue")
    sue_plan.set_credor_respect(100)
    yao_str = "Yao"
    yao_planatom = planatom_shop(dimen, INSERT_str())
    yao_planatom.set_arg(acct_name_str(), yao_str)
    yao_planatom.set_arg(acct_cred_points_str(), 30)
    sue_plandelta.set_planatom(yao_planatom)

    sue_plan = planunit_shop("Sue")
    assert plan_built_from_delta_is_valid(sue_plandelta, sue_plan)

    # WHEN
    plandelta_dict = sue_plandelta.get_ordered_dict(5)

    # THEN
    # delta_zia = plandelta_dict.get(0)
    # delta_yao = plandelta_dict.get(1)
    # delta_pool = plandelta_dict.get(2)
    # assert delta_zia == zia_planatom
    # assert delta_yao == yao_planatom
    # assert delta_pool == pool_planatom
    assert plandelta_dict.get(5) == zia_planatom.get_dict()
    assert plandelta_dict.get(6) == yao_planatom.get_dict()
    assert plandelta_dict.get(7) == pool_planatom.get_dict()


def test_get_plandelta_from_ordered_dict_ReturnsObj():
    # ESTABLISH
    expected_plandelta = plandelta_shop()
    pool_planatom = planatom_shop(planunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_planatom.set_jvalue(pool_attribute, 100)
    expected_plandelta.set_planatom(pool_planatom)
    dimen = plan_acctunit_str()
    zia_str = "Zia"
    zia_planatom = planatom_shop(dimen, INSERT_str())
    zia_planatom.set_arg(acct_name_str(), zia_str)
    zia_planatom.set_arg(acct_cred_points_str(), 70)
    expected_plandelta.set_planatom(zia_planatom)
    sue_plan = planunit_shop("Sue")
    sue_plan.set_credor_respect(100)
    yao_str = "Yao"
    yao_planatom = planatom_shop(dimen, INSERT_str())
    yao_planatom.set_arg(acct_name_str(), yao_str)
    yao_planatom.set_arg(acct_cred_points_str(), 30)
    expected_plandelta.set_planatom(yao_planatom)
    plandelta_dict = expected_plandelta.get_ordered_dict(5)

    # WHEN
    generated_plandelta = get_plandelta_from_ordered_dict(plandelta_dict)

    # THEN
    # delta_zia = plandelta_dict.get(0)
    # delta_yao = plandelta_dict.get(1)
    # delta_pool = plandelta_dict.get(2)
    # assert delta_zia == zia_planatom
    # assert delta_yao == yao_planatom
    # assert delta_pool == pool_planatom
    # assert plandelta_dict.get(5) == zia_planatom.get_dict()
    # assert plandelta_dict.get(6) == yao_planatom.get_dict()
    # assert plandelta_dict.get(7) == pool_planatom.get_dict()
    assert generated_plandelta == expected_plandelta


def test_PlanDelta_get_json_ReturnsObj():
    # ESTABLISH
    sue_plandelta = plandelta_shop()
    pool_planatom = planatom_shop(planunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_planatom.set_jvalue(pool_attribute, 100)
    sue_plandelta.set_planatom(pool_planatom)
    dimen = plan_acctunit_str()
    zia_str = "Zia"
    zia_planatom = planatom_shop(dimen, INSERT_str())
    zia_planatom.set_arg(acct_name_str(), zia_str)
    zia_planatom.set_arg(acct_cred_points_str(), 70)
    sue_plandelta.set_planatom(zia_planatom)
    yao_str = "Yao"
    yao_planatom = planatom_shop(dimen, INSERT_str())
    yao_planatom.set_arg(acct_name_str(), yao_str)
    yao_planatom.set_arg(acct_cred_points_str(), 30)
    sue_plandelta.set_planatom(yao_planatom)

    # WHEN
    delta_start_int = 5
    plandelta_json = sue_plandelta.get_json(delta_start_int)

    # THEN
    assert x_is_json(plandelta_json)


def test_PlanDelta_planatom_exists_ReturnsObj():
    # ESTABLISH
    x_plandelta = plandelta_shop()

    # WHEN / THEN
    dimen = plan_acctunit_str()
    zia_str = "Zia"
    zia_planatom = planatom_shop(dimen, INSERT_str())
    zia_planatom.set_arg(acct_name_str(), zia_str)
    zia_planatom.set_arg(acct_cred_points_str(), 70)
    assert x_plandelta.planatom_exists(zia_planatom) is False

    # WHEN
    x_plandelta.set_planatom(zia_planatom)

    # THEN
    assert x_plandelta.planatom_exists(zia_planatom)


def test_PlanDelta_is_empty_ReturnsObj():
    # ESTABLISH
    x_plandelta = plandelta_shop()

    # WHEN / THEN
    dimen = plan_acctunit_str()
    zia_str = "Zia"
    zia_planatom = planatom_shop(dimen, INSERT_str())
    zia_planatom.set_arg(acct_name_str(), zia_str)
    zia_planatom.set_arg(acct_cred_points_str(), 70)
    assert x_plandelta.is_empty()

    # WHEN
    x_plandelta.set_planatom(zia_planatom)

    # THEN
    assert x_plandelta.is_empty() is False
