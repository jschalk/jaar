from pytest import raises as pytest_raises
from src.a00_data_toolbox.dict_toolbox import x_is_json
from src.a01_term_logic.rope import create_rope, to_rope
from src.a03_group_logic.partner import partnerunit_shop
from src.a05_plan_logic.plan import get_default_belief_label as root_label
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    awardee_title_str,
    believer_partner_membership_str,
    believer_partnerunit_str,
    believer_plan_awardlink_str,
    believer_planunit_str,
    believerunit_str,
    group_title_str,
    partner_cred_points_str,
    partner_debt_points_str,
    partner_name_str,
    plan_rope_str,
)
from src.a08_believer_atom_logic.atom_main import believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import (
    BelieverDelta,
    believer_built_from_delta_is_valid,
    believerdelta_shop,
    get_believerdelta_from_ordered_dict,
)
from src.a09_pack_logic.test._util.example_deltas import (
    get_believerdelta_example1,
    get_believerdelta_sue_example,
)


def test_BelieverDelta_exists():
    # ESTABLISH / WHEN
    x_believerdelta = BelieverDelta()

    # THEN
    assert x_believerdelta.believeratoms is None
    assert x_believerdelta._believer_build_validated is None


def test_believerdelta_shop_ReturnsObj():
    # ESTABLISH / WHEN
    ex1_believerdelta = believerdelta_shop()

    # THEN
    assert ex1_believerdelta.believeratoms == {}
    assert ex1_believerdelta._believer_build_validated is False


def test_BelieverDelta_set_believeratom_CorrectlySets_BelieverUnitSimpleAttrs():
    # ESTABLISH
    ex1_believerdelta = believerdelta_shop()
    attribute_value = 55
    dimen = believerunit_str()
    opt1_arg = "tally"
    jvalues = {opt1_arg: attribute_value}
    jkeys = {}
    believer_mass_believeratom = believeratom_shop(
        dimen,
        UPDATE_str(),
        jkeys=jkeys,
        jvalues=jvalues,
    )
    assert ex1_believerdelta.believeratoms == {}
    assert believer_mass_believeratom.atom_order is None

    # WHEN
    ex1_believerdelta.set_believeratom(believer_mass_believeratom)

    # THEN
    assert len(ex1_believerdelta.believeratoms) == 1
    x_update_dict = ex1_believerdelta.believeratoms.get(UPDATE_str())
    # print(f"{x_update_dict=}")
    x_dimen_believeratom = x_update_dict.get(dimen)
    print(f"{x_dimen_believeratom=}")
    assert x_dimen_believeratom == believer_mass_believeratom
    assert believer_mass_believeratom.atom_order is not None


def test_BelieverDelta_set_believeratom_RaisesErrorWhen_is_valid_IsFalse():
    # ESTABLISH
    ex1_believerdelta = believerdelta_shop()
    x_dimen = believer_partnerunit_str()
    believer_mass_believeratom = believeratom_shop(x_dimen, UPDATE_str())

    # WHEN
    with pytest_raises(Exception) as excinfo:
        ex1_believerdelta.set_believeratom(believer_mass_believeratom)
    assert (
        str(excinfo.value)
        == f"""'{x_dimen}' UPDATE BelieverAtom is invalid
                x_believeratom.is_jkeys_valid()=False
                x_believeratom.is_jvalues_valid()=True"""
    )


def test_ChangUnit_believeratom_exists_ReturnsObj_believer_partnerunit_str():
    # ESTABLISH
    bob_str = "Bob"
    x_believerdelta = believerdelta_shop()
    bob_believeratom = believeratom_shop(believer_partnerunit_str(), INSERT_str())
    bob_believeratom.set_arg(partner_name_str(), bob_str)
    assert not x_believerdelta.believeratom_exists(bob_believeratom)

    # WHEN
    x_believerdelta.set_believeratom(bob_believeratom)

    # THEN
    assert x_believerdelta.believeratom_exists(bob_believeratom)


def test_ChangUnit_believeratom_exists_ReturnsObj_believer_partner_membership_str():
    # ESTABLISH
    bob_str = "Bob"
    iowa_str = ";Iowa"
    x_believerdelta = believerdelta_shop()
    bob_iowa_believeratom = believeratom_shop(
        believer_partner_membership_str(), INSERT_str()
    )
    bob_iowa_believeratom.set_arg(group_title_str(), iowa_str)
    bob_iowa_believeratom.set_arg(partner_name_str(), bob_str)
    assert not x_believerdelta.believeratom_exists(bob_iowa_believeratom)

    # WHEN
    x_believerdelta.set_believeratom(bob_iowa_believeratom)

    # THEN
    assert x_believerdelta.believeratom_exists(bob_iowa_believeratom)


def test_BelieverDelta_get_atom_ReturnsObj():
    # ESTABLISH
    ex1_believerdelta = believerdelta_shop()
    opt_arg1 = "tally"
    opt_value = 55
    believerunit_believeratom = believeratom_shop(believerunit_str(), UPDATE_str())
    believerunit_believeratom.set_jvalue(x_key=opt_arg1, x_value=opt_value)
    ex1_believerdelta.set_believeratom(believerunit_believeratom)

    # WHEN
    gen_believeratom = ex1_believerdelta.get_believeratom(
        UPDATE_str(), dimen=believerunit_str(), jkeys=[]
    )

    # THEN
    assert gen_believeratom == believerunit_believeratom


def test_BelieverDelta_add_believeratom_CorrectlySets_BelieverUnitSimpleAttrs():
    # ESTABLISH
    ex1_believerdelta = believerdelta_shop()
    assert ex1_believerdelta.believeratoms == {}

    # WHEN
    op2_arg = "tally"
    op2_value = 55
    jkeys = {}
    jvalues = {op2_arg: op2_value}
    ex1_believerdelta.add_believeratom(
        believerunit_str(),
        UPDATE_str(),
        jkeys,
        jvalues=jvalues,
    )

    # THEN
    assert len(ex1_believerdelta.believeratoms) == 1
    x_update_dict = ex1_believerdelta.believeratoms.get(UPDATE_str())
    x_believeratom = x_update_dict.get(believerunit_str())
    assert x_believeratom is not None
    assert x_believeratom.dimen == believerunit_str()


def test_BelieverDelta_add_believeratom_CorrectlySets_BelieverUnit_partnerunits():
    # ESTABLISH
    ex1_believerdelta = believerdelta_shop()
    assert ex1_believerdelta.believeratoms == {}

    # WHEN
    bob_str = "Bob"
    bob_partner_cred_points = 55
    bob_partner_debt_points = 66
    bob_partnerunit = partnerunit_shop(
        bob_str, bob_partner_cred_points, bob_partner_debt_points
    )
    cw_str = partner_cred_points_str()
    dw_str = partner_debt_points_str()
    print(f"{bob_partnerunit.to_dict()=}")
    bob_required_dict = {
        partner_name_str(): bob_partnerunit.to_dict().get(partner_name_str())
    }
    bob_optional_dict = {cw_str: bob_partnerunit.to_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_partnerunit.to_dict().get(dw_str)
    print(f"{bob_required_dict=}")
    partnerunit_str = believer_partnerunit_str()
    ex1_believerdelta.add_believeratom(
        dimen=partnerunit_str,
        crud_str=INSERT_str(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )
    # THEN
    assert len(ex1_believerdelta.believeratoms) == 1
    assert (
        ex1_believerdelta.believeratoms.get(INSERT_str())
        .get(partnerunit_str)
        .get(bob_str)
        is not None
    )


def test_BelieverDelta_get_crud_believeratoms_list_ReturnsObj():
    # ESTABLISH
    ex1_believerdelta = get_believerdelta_example1()
    assert len(ex1_believerdelta.believeratoms.get(UPDATE_str()).keys()) == 1
    assert ex1_believerdelta.believeratoms.get(INSERT_str()) is None
    assert len(ex1_believerdelta.believeratoms.get(DELETE_str()).keys()) == 1

    # WHEN
    sue_atom_order_dict = ex1_believerdelta._get_crud_believeratoms_list()

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


def test_BelieverDelta_get_dimen_sorted_believeratoms_list_ReturnsObj_Scenario0_rope():
    # ESTABLISH
    ex1_believerdelta = get_believerdelta_example1()
    update_dict = ex1_believerdelta.believeratoms.get(UPDATE_str())
    assert len(update_dict.keys()) == 1
    print(f"{update_dict.keys()=}")
    assert ex1_believerdelta.believeratoms.get(INSERT_str()) is None
    delete_dict = ex1_believerdelta.believeratoms.get(DELETE_str())
    assert len(delete_dict.keys()) == 1

    # WHEN
    sue_atoms_list = ex1_believerdelta.get_dimen_sorted_believeratoms_list()

    # THEN
    assert len(sue_atoms_list) == 2
    assert sue_atoms_list[0] == update_dict.get(believerunit_str())
    z_atom = sue_atoms_list[1]
    print(f"{z_atom=}")
    print(delete_dict.get(believer_partnerunit_str()).keys())
    zia_partnerunit_delete = delete_dict.get(believer_partnerunit_str()).get("Zia")
    assert sue_atoms_list[1] == zia_partnerunit_delete


# def test_BelieverDelta_add_believeratom_CorrectlySets_BelieverUnit_max_tree_traverse():
#     # ESTABLISH
#     ex1_believerdelta = believerdelta_shop(get_sue_rope())
#     assert ex1_believerdelta.believeratoms == {}

#     # WHEN
#     opt2_value = 55
#     dimen = believerunit_str()
#     opt2_arg = "mass"
#     mass_believeratom = believeratom_shop(dimen, UPDATE_str())
#     mass_believeratom.set_jvalue(opt2_arg, opt2_value)
#     ex1_believerdelta.set_believeratom(mass_believeratom)
#     # THEN
#     assert len(ex1_believerdelta.believeratoms.get(UPDATE_str()).keys()) == 1
#     sue_believerunit_dict = ex1_believerdelta.believeratoms.get(UPDATE_str())
#     sue_mass_believeratom = sue_believerunit_dict.get(dimen)
#     print(f"{sue_mass_believeratom=}")
#     assert mass_believeratom == sue_mass_believeratom

#     # WHEN
#     new2_value = 66
#     x_attribute = "max_tree_traverse"
#     jkeys = {x_attribute: new2_value}
#     x_believeratom = believeratom_shop(x_attribute, UPDATE_str(), None, jkeys)
#     ex1_believerdelta.set_believeratom(x_believeratom)
#     # THEN
#     print(f"{ex1_believerdelta.believeratoms.keys()=}")
#     print(f"{ex1_believerdelta.believeratoms.get(UPDATE_str()).keys()=}")
#     assert len(ex1_believerdelta.believeratoms.get(UPDATE_str()).keys()) == 2
#     assert x_believeratom == ex1_believerdelta.believeratoms.get(UPDATE_str()).get(x_attribute)

#     # WHEN
#     new3_value = 77
#     x_attribute = "credor_respect"
#     jkeys = {x_attribute: new3_value}
#     x_believeratom = believeratom_shop(x_attribute, UPDATE_str(), None, jkeys)
#     ex1_believerdelta.set_believeratom(x_believeratom)
#     # THEN
#     assert len(ex1_believerdelta.believeratoms.get(UPDATE_str()).keys()) == 3
#     assert x_believeratom == ex1_believerdelta.believeratoms.get(UPDATE_str()).get(x_attribute)

#     # WHEN
#     new4_value = 88
#     x_attribute = "debtor_respect"
#     jkeys = {x_attribute: new4_value}
#     x_believeratom = believeratom_shop(x_attribute, UPDATE_str(), None, jkeys)
#     ex1_believerdelta.set_believeratom(x_believeratom)
#     # THEN
#     assert len(ex1_believerdelta.believeratoms.get(UPDATE_str()).keys()) == 4
#     assert x_believeratom == ex1_believerdelta.believeratoms.get(UPDATE_str()).get(x_attribute)


def test_BelieverDelta_get_sorted_believeratoms_ReturnsObj():
    # ESTABLISH
    ex1_believerdelta = get_believerdelta_example1()
    update_dict = ex1_believerdelta.believeratoms.get(UPDATE_str())
    assert len(update_dict.keys()) == 1
    assert update_dict.get(believerunit_str()) is not None
    print(f"atom_order 28 {ex1_believerdelta.believeratoms.get(UPDATE_str()).keys()=}")
    delete_dict = ex1_believerdelta.believeratoms.get(DELETE_str())
    assert len(delete_dict.keys()) == 1
    assert delete_dict.get(believer_partnerunit_str()) is not None
    print(f"atom_order 26 {ex1_believerdelta.believeratoms.get(DELETE_str()).keys()=}")

    # WHEN
    sue_atom_order_list = ex1_believerdelta.get_sorted_believeratoms()

    # THEN
    assert len(sue_atom_order_list) == 2
    print(delete_dict.get(believer_partnerunit_str()).keys())
    zia_partnerunit_delete = delete_dict.get(believer_partnerunit_str()).get("Zia")
    # for believeratom in sue_atom_order_list:
    #     print(f"{believeratom.atom_order=}")
    assert sue_atom_order_list[0] == zia_partnerunit_delete
    assert sue_atom_order_list[1] == update_dict.get(believerunit_str())
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_BelieverDelta_get_sorted_believeratoms_ReturnsObj_PlanUnitsSorted():
    # ESTABLISH
    x_belief_label = root_label()
    root_rope = to_rope(x_belief_label)
    sports_str = "sports"
    sports_rope = create_rope(x_belief_label, sports_str)
    knee_str = "knee"
    knee_rope = create_rope(x_belief_label, knee_str)
    x_dimen = believer_planunit_str()
    sports_insert_planunit_believeratom = believeratom_shop(x_dimen, INSERT_str())
    sports_insert_planunit_believeratom.set_jkey(plan_rope_str(), sports_rope)
    knee_insert_planunit_believeratom = believeratom_shop(x_dimen, INSERT_str())
    knee_insert_planunit_believeratom.set_jkey(plan_rope_str(), knee_rope)
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(knee_insert_planunit_believeratom)
    x_believerdelta.set_believeratom(sports_insert_planunit_believeratom)

    # WHEN
    x_atom_order_list = x_believerdelta.get_sorted_believeratoms()

    # THEN
    assert len(x_atom_order_list) == 2
    # for believeratom in x_atom_order_list:
    #     print(f"{believeratom.jkeys=}")
    assert x_atom_order_list[0] == knee_insert_planunit_believeratom
    assert x_atom_order_list[1] == sports_insert_planunit_believeratom
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_BelieverDelta_get_sorted_believeratoms_ReturnsObj_Rope_Sorted():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    x_belief_label = root_label()
    sports_str = "sports"
    sports_rope = create_rope(x_belief_label, sports_str)
    knee_str = "knee"
    knee_rope = create_rope(sports_rope, knee_str)
    x_dimen = believer_plan_awardlink_str()
    swimmers_str = ",Swimmers"
    sports_awardlink_believeratom = believeratom_shop(x_dimen, INSERT_str())
    sports_awardlink_believeratom.set_jkey(awardee_title_str(), swimmers_str)
    sports_awardlink_believeratom.set_jkey(plan_rope_str(), sports_rope)
    knee_awardlink_believeratom = believeratom_shop(x_dimen, INSERT_str())
    knee_awardlink_believeratom.set_jkey(awardee_title_str(), swimmers_str)
    knee_awardlink_believeratom.set_jkey(plan_rope_str(), knee_rope)
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(knee_awardlink_believeratom)
    x_believerdelta.set_believeratom(sports_awardlink_believeratom)

    # WHEN
    x_atom_order_list = x_believerdelta.get_sorted_believeratoms()

    # THEN
    assert len(x_atom_order_list) == 2
    # for believeratom in x_atom_order_list:
    #     print(f"{believeratom.jkeys=}")
    assert x_atom_order_list[0] == sports_awardlink_believeratom
    assert x_atom_order_list[1] == knee_awardlink_believeratom
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_believer_built_from_delta_is_valid_ReturnsObjEstablishWithNoBeliever_scenario1():
    # ESTABLISH
    sue_believerdelta = believerdelta_shop()

    x_believeratom = believeratom_shop(believerunit_str(), UPDATE_str())
    x_attribute = "credor_respect"
    x_believeratom.set_jvalue(x_attribute, 100)
    sue_believerdelta.set_believeratom(x_believeratom)

    dimen = believer_partnerunit_str()
    zia_str = "Zia"
    x_believeratom = believeratom_shop(dimen, INSERT_str())
    x_believeratom.set_arg(partner_name_str(), zia_str)
    x_believeratom.set_arg(partner_cred_points_str(), "70 is the number")
    sue_believerdelta.set_believeratom(x_believeratom)
    print(f"{sue_believerdelta=}")

    # WHEN / THEN
    assert believer_built_from_delta_is_valid(sue_believerdelta) is False


def test_believer_built_from_delta_is_valid_ReturnsObjEstablishWithNoBeliever_scenario2():
    # sourcery skip: extract-duplicate-method
    sue_believerdelta = believerdelta_shop()
    dimen = believer_partnerunit_str()
    # WHEN
    yao_str = "Yao"
    x_believeratom = believeratom_shop(dimen, INSERT_str())
    x_believeratom.set_arg(partner_name_str(), yao_str)
    x_believeratom.set_arg(partner_cred_points_str(), 30)
    sue_believerdelta.set_believeratom(x_believeratom)

    # THEN
    assert believer_built_from_delta_is_valid(sue_believerdelta)

    # WHEN
    bob_str = "Bob"
    x_believeratom = believeratom_shop(dimen, INSERT_str())
    x_believeratom.set_arg(partner_name_str(), bob_str)
    x_believeratom.set_arg(partner_cred_points_str(), "70 is the number")
    sue_believerdelta.set_believeratom(x_believeratom)

    # THEN
    assert believer_built_from_delta_is_valid(sue_believerdelta) is False


def test_BelieverDelta_get_ordered_believeratoms_ReturnsObj_EstablishWithNoStartingNumber():
    # sourcery skip: extract-duplicate-method, inline-immediately-returned-variable, move-assign-in-block
    # ESTABLISH
    sue_believerdelta = believerdelta_shop()
    pool_believeratom = believeratom_shop(believerunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_believeratom.set_jvalue(pool_attribute, 100)
    sue_believerdelta.set_believeratom(pool_believeratom)
    dimen = believer_partnerunit_str()
    zia_str = "Zia"
    zia_believeratom = believeratom_shop(dimen, INSERT_str())
    zia_believeratom.set_arg(partner_name_str(), zia_str)
    zia_believeratom.set_arg(partner_cred_points_str(), 70)
    sue_believerdelta.set_believeratom(zia_believeratom)
    sue_believer = believerunit_shop("Sue")
    sue_believer.set_credor_respect(100)
    yao_str = "Yao"
    yao_believeratom = believeratom_shop(dimen, INSERT_str())
    yao_believeratom.set_arg(partner_name_str(), yao_str)
    yao_believeratom.set_arg(partner_cred_points_str(), 30)
    sue_believerdelta.set_believeratom(yao_believeratom)

    sue_believer = believerunit_shop("Sue")
    assert believer_built_from_delta_is_valid(sue_believerdelta, sue_believer)

    # WHEN
    believerdelta_dict = sue_believerdelta.get_ordered_believeratoms()

    # THEN
    # delta_zia = believerdelta_dict.get(0)
    # delta_yao = believerdelta_dict.get(1)
    # delta_pool = believerdelta_dict.get(2)
    # assert delta_zia == zia_believeratom
    # assert delta_yao == yao_believeratom
    # assert delta_pool == pool_believeratom
    assert believerdelta_dict.get(0) == zia_believeratom
    assert believerdelta_dict.get(1) == yao_believeratom
    assert believerdelta_dict.get(2) == pool_believeratom


def test_BelieverDelta_get_ordered_believeratoms_ReturnsObj_EstablishWithStartingNumber():
    # sourcery skip: extract-duplicate-method, inline-immediately-returned-variable, move-assign-in-block
    # ESTABLISH
    sue_believerdelta = believerdelta_shop()
    pool_believeratom = believeratom_shop(believerunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_believeratom.set_jvalue(pool_attribute, 100)
    sue_believerdelta.set_believeratom(pool_believeratom)
    dimen = believer_partnerunit_str()
    zia_str = "Zia"
    zia_believeratom = believeratom_shop(dimen, INSERT_str())
    zia_believeratom.set_arg(partner_name_str(), zia_str)
    zia_believeratom.set_arg(partner_cred_points_str(), 70)
    sue_believerdelta.set_believeratom(zia_believeratom)
    sue_believer = believerunit_shop("Sue")
    sue_believer.set_credor_respect(100)
    yao_str = "Yao"
    yao_believeratom = believeratom_shop(dimen, INSERT_str())
    yao_believeratom.set_arg(partner_name_str(), yao_str)
    yao_believeratom.set_arg(partner_cred_points_str(), 30)
    sue_believerdelta.set_believeratom(yao_believeratom)

    sue_believer = believerunit_shop("Sue")
    assert believer_built_from_delta_is_valid(sue_believerdelta, sue_believer)

    # WHEN
    believerdelta_dict = sue_believerdelta.get_ordered_believeratoms(5)

    # THEN
    # delta_zia = believerdelta_dict.get(0)
    # delta_yao = believerdelta_dict.get(1)
    # delta_pool = believerdelta_dict.get(2)
    # assert delta_zia == zia_believeratom
    # assert delta_yao == yao_believeratom
    # assert delta_pool == pool_believeratom
    assert believerdelta_dict.get(5) == zia_believeratom
    assert believerdelta_dict.get(6) == yao_believeratom
    assert believerdelta_dict.get(7) == pool_believeratom


def test_BelieverDelta_get_ordered_dict_ReturnsObj_EstablishWithStartingNumber():
    # sourcery skip: extract-duplicate-method, inline-immediately-returned-variable, move-assign-in-block
    # ESTABLISH
    sue_believerdelta = believerdelta_shop()
    pool_believeratom = believeratom_shop(believerunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_believeratom.set_jvalue(pool_attribute, 100)
    sue_believerdelta.set_believeratom(pool_believeratom)
    dimen = believer_partnerunit_str()
    zia_str = "Zia"
    zia_believeratom = believeratom_shop(dimen, INSERT_str())
    zia_believeratom.set_arg(partner_name_str(), zia_str)
    zia_believeratom.set_arg(partner_cred_points_str(), 70)
    sue_believerdelta.set_believeratom(zia_believeratom)
    sue_believer = believerunit_shop("Sue")
    sue_believer.set_credor_respect(100)
    yao_str = "Yao"
    yao_believeratom = believeratom_shop(dimen, INSERT_str())
    yao_believeratom.set_arg(partner_name_str(), yao_str)
    yao_believeratom.set_arg(partner_cred_points_str(), 30)
    sue_believerdelta.set_believeratom(yao_believeratom)

    sue_believer = believerunit_shop("Sue")
    assert believer_built_from_delta_is_valid(sue_believerdelta, sue_believer)

    # WHEN
    believerdelta_dict = sue_believerdelta.get_ordered_dict(5)

    # THEN
    # delta_zia = believerdelta_dict.get(0)
    # delta_yao = believerdelta_dict.get(1)
    # delta_pool = believerdelta_dict.get(2)
    # assert delta_zia == zia_believeratom
    # assert delta_yao == yao_believeratom
    # assert delta_pool == pool_believeratom
    assert believerdelta_dict.get(5) == zia_believeratom.to_dict()
    assert believerdelta_dict.get(6) == yao_believeratom.to_dict()
    assert believerdelta_dict.get(7) == pool_believeratom.to_dict()


def test_get_believerdelta_from_ordered_dict_ReturnsObj():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    expected_believerdelta = believerdelta_shop()
    pool_believeratom = believeratom_shop(believerunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_believeratom.set_jvalue(pool_attribute, 100)
    expected_believerdelta.set_believeratom(pool_believeratom)
    dimen = believer_partnerunit_str()
    zia_str = "Zia"
    zia_believeratom = believeratom_shop(dimen, INSERT_str())
    zia_believeratom.set_arg(partner_name_str(), zia_str)
    zia_believeratom.set_arg(partner_cred_points_str(), 70)
    expected_believerdelta.set_believeratom(zia_believeratom)
    sue_believer = believerunit_shop("Sue")
    sue_believer.set_credor_respect(100)
    yao_str = "Yao"
    yao_believeratom = believeratom_shop(dimen, INSERT_str())
    yao_believeratom.set_arg(partner_name_str(), yao_str)
    yao_believeratom.set_arg(partner_cred_points_str(), 30)
    expected_believerdelta.set_believeratom(yao_believeratom)
    believerdelta_dict = expected_believerdelta.get_ordered_dict(5)

    # WHEN
    generated_believerdelta = get_believerdelta_from_ordered_dict(believerdelta_dict)

    # THEN
    # delta_zia = believerdelta_dict.get(0)
    # delta_yao = believerdelta_dict.get(1)
    # delta_pool = believerdelta_dict.get(2)
    # assert delta_zia == zia_believeratom
    # assert delta_yao == yao_believeratom
    # assert delta_pool == pool_believeratom
    # assert believerdelta_dict.get(5) == zia_believeratom.to_dict()
    # assert believerdelta_dict.get(6) == yao_believeratom.to_dict()
    # assert believerdelta_dict.get(7) == pool_believeratom.to_dict()
    assert generated_believerdelta == expected_believerdelta


def test_BelieverDelta_get_json_ReturnsObj():
    # sourcery skip: extract-duplicate-method, inline-variable
    # ESTABLISH
    sue_believerdelta = believerdelta_shop()
    pool_believeratom = believeratom_shop(believerunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_believeratom.set_jvalue(pool_attribute, 100)
    sue_believerdelta.set_believeratom(pool_believeratom)
    dimen = believer_partnerunit_str()
    zia_str = "Zia"
    zia_believeratom = believeratom_shop(dimen, INSERT_str())
    zia_believeratom.set_arg(partner_name_str(), zia_str)
    zia_believeratom.set_arg(partner_cred_points_str(), 70)
    sue_believerdelta.set_believeratom(zia_believeratom)
    yao_str = "Yao"
    yao_believeratom = believeratom_shop(dimen, INSERT_str())
    yao_believeratom.set_arg(partner_name_str(), yao_str)
    yao_believeratom.set_arg(partner_cred_points_str(), 30)
    sue_believerdelta.set_believeratom(yao_believeratom)

    # WHEN
    delta_start_int = 5
    believerdelta_json = sue_believerdelta.get_json(delta_start_int)

    # THEN
    assert x_is_json(believerdelta_json)


def test_BelieverDelta_believeratom_exists_ReturnsObj():
    # ESTABLISH
    x_believerdelta = believerdelta_shop()

    # WHEN / THEN
    dimen = believer_partnerunit_str()
    zia_str = "Zia"
    zia_believeratom = believeratom_shop(dimen, INSERT_str())
    zia_believeratom.set_arg(partner_name_str(), zia_str)
    zia_believeratom.set_arg(partner_cred_points_str(), 70)
    assert x_believerdelta.believeratom_exists(zia_believeratom) is False

    # WHEN
    x_believerdelta.set_believeratom(zia_believeratom)

    # THEN
    assert x_believerdelta.believeratom_exists(zia_believeratom)


def test_BelieverDelta_is_empty_ReturnsObj():
    # ESTABLISH
    x_believerdelta = believerdelta_shop()

    # WHEN / THEN
    dimen = believer_partnerunit_str()
    zia_str = "Zia"
    zia_believeratom = believeratom_shop(dimen, INSERT_str())
    zia_believeratom.set_arg(partner_name_str(), zia_str)
    zia_believeratom.set_arg(partner_cred_points_str(), 70)
    assert x_believerdelta.is_empty()

    # WHEN
    x_believerdelta.set_believeratom(zia_believeratom)

    # THEN
    assert x_believerdelta.is_empty() is False
