from pytest import raises as pytest_raises
from src.a00_data_toolbox.dict_toolbox import x_is_json
from src.a01_term_logic.rope import create_rope, to_rope
from src.a03_group_logic.acct import acctunit_shop
from src.a05_plan_logic.plan import get_default_belief_label as root_label
from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.a06_str import (
    acct_cred_points_str,
    acct_debt_points_str,
    acct_name_str,
    awardee_title_str,
    group_title_str,
    owner_acct_membership_str,
    owner_acctunit_str,
    owner_plan_awardlink_str,
    owner_planunit_str,
    ownerunit_str,
    plan_rope_str,
)
from src.a08_owner_atom_logic.atom import owneratom_shop
from src.a08_owner_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import (
    OwnerDelta,
    get_ownerdelta_from_ordered_dict,
    owner_built_from_delta_is_valid,
    ownerdelta_shop,
)
from src.a09_pack_logic.test._util.example_deltas import (
    get_ownerdelta_example1,
    get_ownerdelta_sue_example,
)


def test_OwnerDelta_exists():
    # ESTABLISH / WHEN
    x_ownerdelta = OwnerDelta()

    # THEN
    assert x_ownerdelta.owneratoms is None
    assert x_ownerdelta._owner_build_validated is None


def test_ownerdelta_shop_ReturnsObj():
    # ESTABLISH / WHEN
    ex1_ownerdelta = ownerdelta_shop()

    # THEN
    assert ex1_ownerdelta.owneratoms == {}
    assert ex1_ownerdelta._owner_build_validated is False


def test_OwnerDelta_set_owneratom_CorrectlySets_OwnerUnitSimpleAttrs():
    # ESTABLISH
    ex1_ownerdelta = ownerdelta_shop()
    attribute_value = 55
    dimen = ownerunit_str()
    opt1_arg = "tally"
    jvalues = {opt1_arg: attribute_value}
    jkeys = {}
    owner_mass_owneratom = owneratom_shop(
        dimen,
        UPDATE_str(),
        jkeys=jkeys,
        jvalues=jvalues,
    )
    assert ex1_ownerdelta.owneratoms == {}
    assert owner_mass_owneratom.atom_order is None

    # WHEN
    ex1_ownerdelta.set_owneratom(owner_mass_owneratom)

    # THEN
    assert len(ex1_ownerdelta.owneratoms) == 1
    x_update_dict = ex1_ownerdelta.owneratoms.get(UPDATE_str())
    # print(f"{x_update_dict=}")
    x_dimen_owneratom = x_update_dict.get(dimen)
    print(f"{x_dimen_owneratom=}")
    assert x_dimen_owneratom == owner_mass_owneratom
    assert owner_mass_owneratom.atom_order is not None


def test_OwnerDelta_set_owneratom_RaisesErrorWhen_is_valid_IsFalse():
    # ESTABLISH
    ex1_ownerdelta = ownerdelta_shop()
    x_dimen = owner_acctunit_str()
    owner_mass_owneratom = owneratom_shop(x_dimen, UPDATE_str())

    # WHEN
    with pytest_raises(Exception) as excinfo:
        ex1_ownerdelta.set_owneratom(owner_mass_owneratom)
    assert (
        str(excinfo.value)
        == f"""'{x_dimen}' UPDATE OwnerAtom is invalid
                x_owneratom.is_jkeys_valid()=False
                x_owneratom.is_jvalues_valid()=True"""
    )


def test_ChangUnit_owneratom_exists_ReturnsObj_owner_acctunit_str():
    # ESTABLISH
    bob_str = "Bob"
    x_ownerdelta = ownerdelta_shop()
    bob_owneratom = owneratom_shop(owner_acctunit_str(), INSERT_str())
    bob_owneratom.set_arg(acct_name_str(), bob_str)
    assert not x_ownerdelta.owneratom_exists(bob_owneratom)

    # WHEN
    x_ownerdelta.set_owneratom(bob_owneratom)

    # THEN
    assert x_ownerdelta.owneratom_exists(bob_owneratom)


def test_ChangUnit_owneratom_exists_ReturnsObj_owner_acct_membership_str():
    # ESTABLISH
    bob_str = "Bob"
    iowa_str = ";Iowa"
    x_ownerdelta = ownerdelta_shop()
    bob_iowa_owneratom = owneratom_shop(owner_acct_membership_str(), INSERT_str())
    bob_iowa_owneratom.set_arg(group_title_str(), iowa_str)
    bob_iowa_owneratom.set_arg(acct_name_str(), bob_str)
    assert not x_ownerdelta.owneratom_exists(bob_iowa_owneratom)

    # WHEN
    x_ownerdelta.set_owneratom(bob_iowa_owneratom)

    # THEN
    assert x_ownerdelta.owneratom_exists(bob_iowa_owneratom)


def test_OwnerDelta_get_atom_ReturnsObj():
    # ESTABLISH
    ex1_ownerdelta = ownerdelta_shop()
    opt_arg1 = "tally"
    opt_value = 55
    ownerunit_owneratom = owneratom_shop(ownerunit_str(), UPDATE_str())
    ownerunit_owneratom.set_jvalue(x_key=opt_arg1, x_value=opt_value)
    ex1_ownerdelta.set_owneratom(ownerunit_owneratom)

    # WHEN
    gen_owneratom = ex1_ownerdelta.get_owneratom(
        UPDATE_str(), dimen=ownerunit_str(), jkeys=[]
    )

    # THEN
    assert gen_owneratom == ownerunit_owneratom


def test_OwnerDelta_add_owneratom_CorrectlySets_OwnerUnitSimpleAttrs():
    # ESTABLISH
    ex1_ownerdelta = ownerdelta_shop()
    assert ex1_ownerdelta.owneratoms == {}

    # WHEN
    op2_arg = "tally"
    op2_value = 55
    jkeys = {}
    jvalues = {op2_arg: op2_value}
    ex1_ownerdelta.add_owneratom(
        ownerunit_str(),
        UPDATE_str(),
        jkeys,
        jvalues=jvalues,
    )

    # THEN
    assert len(ex1_ownerdelta.owneratoms) == 1
    x_update_dict = ex1_ownerdelta.owneratoms.get(UPDATE_str())
    x_owneratom = x_update_dict.get(ownerunit_str())
    assert x_owneratom is not None
    assert x_owneratom.dimen == ownerunit_str()


def test_OwnerDelta_add_owneratom_CorrectlySets_OwnerUnit_acctunits():
    # ESTABLISH
    ex1_ownerdelta = ownerdelta_shop()
    assert ex1_ownerdelta.owneratoms == {}

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
    acctunit_str = owner_acctunit_str()
    ex1_ownerdelta.add_owneratom(
        dimen=acctunit_str,
        crud_str=INSERT_str(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )
    # THEN
    assert len(ex1_ownerdelta.owneratoms) == 1
    assert (
        ex1_ownerdelta.owneratoms.get(INSERT_str()).get(acctunit_str).get(bob_str)
        is not None
    )


def test_OwnerDelta_get_crud_owneratoms_list_ReturnsObj():
    # ESTABLISH
    ex1_ownerdelta = get_ownerdelta_example1()
    assert len(ex1_ownerdelta.owneratoms.get(UPDATE_str()).keys()) == 1
    assert ex1_ownerdelta.owneratoms.get(INSERT_str()) is None
    assert len(ex1_ownerdelta.owneratoms.get(DELETE_str()).keys()) == 1

    # WHEN
    sue_atom_order_dict = ex1_ownerdelta._get_crud_owneratoms_list()

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


def test_OwnerDelta_get_dimen_sorted_owneratoms_list_ReturnsObj_Scenario0_rope():
    # ESTABLISH
    ex1_ownerdelta = get_ownerdelta_example1()
    update_dict = ex1_ownerdelta.owneratoms.get(UPDATE_str())
    assert len(update_dict.keys()) == 1
    print(f"{update_dict.keys()=}")
    assert ex1_ownerdelta.owneratoms.get(INSERT_str()) is None
    delete_dict = ex1_ownerdelta.owneratoms.get(DELETE_str())
    assert len(delete_dict.keys()) == 1

    # WHEN
    sue_atoms_list = ex1_ownerdelta.get_dimen_sorted_owneratoms_list()

    # THEN
    assert len(sue_atoms_list) == 2
    assert sue_atoms_list[0] == update_dict.get(ownerunit_str())
    z_atom = sue_atoms_list[1]
    print(f"{z_atom=}")
    print(delete_dict.get(owner_acctunit_str()).keys())
    zia_acctunit_delete = delete_dict.get(owner_acctunit_str()).get("Zia")
    assert sue_atoms_list[1] == zia_acctunit_delete


# def test_OwnerDelta_add_owneratom_CorrectlySets_OwnerUnit_max_tree_traverse():
#     # ESTABLISH
#     ex1_ownerdelta = ownerdelta_shop(get_sue_rope())
#     assert ex1_ownerdelta.owneratoms == {}

#     # WHEN
#     opt2_value = 55
#     dimen = ownerunit_str()
#     opt2_arg = "mass"
#     mass_owneratom = owneratom_shop(dimen, UPDATE_str())
#     mass_owneratom.set_jvalue(opt2_arg, opt2_value)
#     ex1_ownerdelta.set_owneratom(mass_owneratom)
#     # THEN
#     assert len(ex1_ownerdelta.owneratoms.get(UPDATE_str()).keys()) == 1
#     sue_ownerunit_dict = ex1_ownerdelta.owneratoms.get(UPDATE_str())
#     sue_mass_owneratom = sue_ownerunit_dict.get(dimen)
#     print(f"{sue_mass_owneratom=}")
#     assert mass_owneratom == sue_mass_owneratom

#     # WHEN
#     new2_value = 66
#     x_attribute = "max_tree_traverse"
#     jkeys = {x_attribute: new2_value}
#     x_owneratom = owneratom_shop(x_attribute, UPDATE_str(), None, jkeys)
#     ex1_ownerdelta.set_owneratom(x_owneratom)
#     # THEN
#     print(f"{ex1_ownerdelta.owneratoms.keys()=}")
#     print(f"{ex1_ownerdelta.owneratoms.get(UPDATE_str()).keys()=}")
#     assert len(ex1_ownerdelta.owneratoms.get(UPDATE_str()).keys()) == 2
#     assert x_owneratom == ex1_ownerdelta.owneratoms.get(UPDATE_str()).get(x_attribute)

#     # WHEN
#     new3_value = 77
#     x_attribute = "credor_respect"
#     jkeys = {x_attribute: new3_value}
#     x_owneratom = owneratom_shop(x_attribute, UPDATE_str(), None, jkeys)
#     ex1_ownerdelta.set_owneratom(x_owneratom)
#     # THEN
#     assert len(ex1_ownerdelta.owneratoms.get(UPDATE_str()).keys()) == 3
#     assert x_owneratom == ex1_ownerdelta.owneratoms.get(UPDATE_str()).get(x_attribute)

#     # WHEN
#     new4_value = 88
#     x_attribute = "debtor_respect"
#     jkeys = {x_attribute: new4_value}
#     x_owneratom = owneratom_shop(x_attribute, UPDATE_str(), None, jkeys)
#     ex1_ownerdelta.set_owneratom(x_owneratom)
#     # THEN
#     assert len(ex1_ownerdelta.owneratoms.get(UPDATE_str()).keys()) == 4
#     assert x_owneratom == ex1_ownerdelta.owneratoms.get(UPDATE_str()).get(x_attribute)


def test_OwnerDelta_get_sorted_owneratoms_ReturnsObj():
    # ESTABLISH
    ex1_ownerdelta = get_ownerdelta_example1()
    update_dict = ex1_ownerdelta.owneratoms.get(UPDATE_str())
    assert len(update_dict.keys()) == 1
    assert update_dict.get(ownerunit_str()) is not None
    print(f"atom_order 28 {ex1_ownerdelta.owneratoms.get(UPDATE_str()).keys()=}")
    delete_dict = ex1_ownerdelta.owneratoms.get(DELETE_str())
    assert len(delete_dict.keys()) == 1
    assert delete_dict.get(owner_acctunit_str()) is not None
    print(f"atom_order 26 {ex1_ownerdelta.owneratoms.get(DELETE_str()).keys()=}")

    # WHEN
    sue_atom_order_list = ex1_ownerdelta.get_sorted_owneratoms()

    # THEN
    assert len(sue_atom_order_list) == 2
    print(delete_dict.get(owner_acctunit_str()).keys())
    zia_acctunit_delete = delete_dict.get(owner_acctunit_str()).get("Zia")
    # for owneratom in sue_atom_order_list:
    #     print(f"{owneratom.atom_order=}")
    assert sue_atom_order_list[0] == zia_acctunit_delete
    assert sue_atom_order_list[1] == update_dict.get(ownerunit_str())
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_OwnerDelta_get_sorted_owneratoms_ReturnsObj_PlanUnitsSorted():
    # ESTABLISH
    x_belief_label = root_label()
    root_rope = to_rope(x_belief_label)
    sports_str = "sports"
    sports_rope = create_rope(x_belief_label, sports_str)
    knee_str = "knee"
    knee_rope = create_rope(x_belief_label, knee_str)
    x_dimen = owner_planunit_str()
    sports_insert_planunit_owneratom = owneratom_shop(x_dimen, INSERT_str())
    sports_insert_planunit_owneratom.set_jkey(plan_rope_str(), sports_rope)
    knee_insert_planunit_owneratom = owneratom_shop(x_dimen, INSERT_str())
    knee_insert_planunit_owneratom.set_jkey(plan_rope_str(), knee_rope)
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(knee_insert_planunit_owneratom)
    x_ownerdelta.set_owneratom(sports_insert_planunit_owneratom)

    # WHEN
    x_atom_order_list = x_ownerdelta.get_sorted_owneratoms()

    # THEN
    assert len(x_atom_order_list) == 2
    # for owneratom in x_atom_order_list:
    #     print(f"{owneratom.jkeys=}")
    assert x_atom_order_list[0] == knee_insert_planunit_owneratom
    assert x_atom_order_list[1] == sports_insert_planunit_owneratom
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_OwnerDelta_get_sorted_owneratoms_ReturnsObj_Rope_Sorted():
    # ESTABLISH
    x_belief_label = root_label()
    sports_str = "sports"
    sports_rope = create_rope(x_belief_label, sports_str)
    knee_str = "knee"
    knee_rope = create_rope(sports_rope, knee_str)
    x_dimen = owner_plan_awardlink_str()
    swimmers_str = ",Swimmers"
    sports_awardlink_owneratom = owneratom_shop(x_dimen, INSERT_str())
    sports_awardlink_owneratom.set_jkey(awardee_title_str(), swimmers_str)
    sports_awardlink_owneratom.set_jkey(plan_rope_str(), sports_rope)
    knee_awardlink_owneratom = owneratom_shop(x_dimen, INSERT_str())
    knee_awardlink_owneratom.set_jkey(awardee_title_str(), swimmers_str)
    knee_awardlink_owneratom.set_jkey(plan_rope_str(), knee_rope)
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(knee_awardlink_owneratom)
    x_ownerdelta.set_owneratom(sports_awardlink_owneratom)

    # WHEN
    x_atom_order_list = x_ownerdelta.get_sorted_owneratoms()

    # THEN
    assert len(x_atom_order_list) == 2
    # for owneratom in x_atom_order_list:
    #     print(f"{owneratom.jkeys=}")
    assert x_atom_order_list[0] == sports_awardlink_owneratom
    assert x_atom_order_list[1] == knee_awardlink_owneratom
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_owner_built_from_delta_is_valid_ReturnsObjEstablishWithNoOwner_scenario1():
    # ESTABLISH
    sue_ownerdelta = ownerdelta_shop()

    x_owneratom = owneratom_shop(ownerunit_str(), UPDATE_str())
    x_attribute = "credor_respect"
    x_owneratom.set_jvalue(x_attribute, 100)
    sue_ownerdelta.set_owneratom(x_owneratom)

    dimen = owner_acctunit_str()
    zia_str = "Zia"
    x_owneratom = owneratom_shop(dimen, INSERT_str())
    x_owneratom.set_arg(acct_name_str(), zia_str)
    x_owneratom.set_arg(acct_cred_points_str(), "70 is the number")
    sue_ownerdelta.set_owneratom(x_owneratom)
    print(f"{sue_ownerdelta=}")

    # WHEN / THEN
    assert owner_built_from_delta_is_valid(sue_ownerdelta) is False


def test_owner_built_from_delta_is_valid_ReturnsObjEstablishWithNoOwner_scenario2():
    sue_ownerdelta = ownerdelta_shop()
    dimen = owner_acctunit_str()
    # WHEN
    yao_str = "Yao"
    x_owneratom = owneratom_shop(dimen, INSERT_str())
    x_owneratom.set_arg(acct_name_str(), yao_str)
    x_owneratom.set_arg(acct_cred_points_str(), 30)
    sue_ownerdelta.set_owneratom(x_owneratom)

    # THEN
    assert owner_built_from_delta_is_valid(sue_ownerdelta)

    # WHEN
    bob_str = "Bob"
    x_owneratom = owneratom_shop(dimen, INSERT_str())
    x_owneratom.set_arg(acct_name_str(), bob_str)
    x_owneratom.set_arg(acct_cred_points_str(), "70 is the number")
    sue_ownerdelta.set_owneratom(x_owneratom)

    # THEN
    assert owner_built_from_delta_is_valid(sue_ownerdelta) is False


def test_OwnerDelta_get_ordered_owneratoms_ReturnsObj_EstablishWithNoStartingNumber():
    # ESTABLISH
    sue_ownerdelta = ownerdelta_shop()
    pool_owneratom = owneratom_shop(ownerunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_owneratom.set_jvalue(pool_attribute, 100)
    sue_ownerdelta.set_owneratom(pool_owneratom)
    dimen = owner_acctunit_str()
    zia_str = "Zia"
    zia_owneratom = owneratom_shop(dimen, INSERT_str())
    zia_owneratom.set_arg(acct_name_str(), zia_str)
    zia_owneratom.set_arg(acct_cred_points_str(), 70)
    sue_ownerdelta.set_owneratom(zia_owneratom)
    sue_owner = ownerunit_shop("Sue")
    sue_owner.set_credor_respect(100)
    yao_str = "Yao"
    yao_owneratom = owneratom_shop(dimen, INSERT_str())
    yao_owneratom.set_arg(acct_name_str(), yao_str)
    yao_owneratom.set_arg(acct_cred_points_str(), 30)
    sue_ownerdelta.set_owneratom(yao_owneratom)

    sue_owner = ownerunit_shop("Sue")
    assert owner_built_from_delta_is_valid(sue_ownerdelta, sue_owner)

    # WHEN
    ownerdelta_dict = sue_ownerdelta.get_ordered_owneratoms()

    # THEN
    # delta_zia = ownerdelta_dict.get(0)
    # delta_yao = ownerdelta_dict.get(1)
    # delta_pool = ownerdelta_dict.get(2)
    # assert delta_zia == zia_owneratom
    # assert delta_yao == yao_owneratom
    # assert delta_pool == pool_owneratom
    assert ownerdelta_dict.get(0) == zia_owneratom
    assert ownerdelta_dict.get(1) == yao_owneratom
    assert ownerdelta_dict.get(2) == pool_owneratom


def test_OwnerDelta_get_ordered_owneratoms_ReturnsObj_EstablishWithStartingNumber():
    # ESTABLISH
    sue_ownerdelta = ownerdelta_shop()
    pool_owneratom = owneratom_shop(ownerunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_owneratom.set_jvalue(pool_attribute, 100)
    sue_ownerdelta.set_owneratom(pool_owneratom)
    dimen = owner_acctunit_str()
    zia_str = "Zia"
    zia_owneratom = owneratom_shop(dimen, INSERT_str())
    zia_owneratom.set_arg(acct_name_str(), zia_str)
    zia_owneratom.set_arg(acct_cred_points_str(), 70)
    sue_ownerdelta.set_owneratom(zia_owneratom)
    sue_owner = ownerunit_shop("Sue")
    sue_owner.set_credor_respect(100)
    yao_str = "Yao"
    yao_owneratom = owneratom_shop(dimen, INSERT_str())
    yao_owneratom.set_arg(acct_name_str(), yao_str)
    yao_owneratom.set_arg(acct_cred_points_str(), 30)
    sue_ownerdelta.set_owneratom(yao_owneratom)

    sue_owner = ownerunit_shop("Sue")
    assert owner_built_from_delta_is_valid(sue_ownerdelta, sue_owner)

    # WHEN
    ownerdelta_dict = sue_ownerdelta.get_ordered_owneratoms(5)

    # THEN
    # delta_zia = ownerdelta_dict.get(0)
    # delta_yao = ownerdelta_dict.get(1)
    # delta_pool = ownerdelta_dict.get(2)
    # assert delta_zia == zia_owneratom
    # assert delta_yao == yao_owneratom
    # assert delta_pool == pool_owneratom
    assert ownerdelta_dict.get(5) == zia_owneratom
    assert ownerdelta_dict.get(6) == yao_owneratom
    assert ownerdelta_dict.get(7) == pool_owneratom


def test_OwnerDelta_get_ordered_dict_ReturnsObj_EstablishWithStartingNumber():
    # ESTABLISH
    sue_ownerdelta = ownerdelta_shop()
    pool_owneratom = owneratom_shop(ownerunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_owneratom.set_jvalue(pool_attribute, 100)
    sue_ownerdelta.set_owneratom(pool_owneratom)
    dimen = owner_acctunit_str()
    zia_str = "Zia"
    zia_owneratom = owneratom_shop(dimen, INSERT_str())
    zia_owneratom.set_arg(acct_name_str(), zia_str)
    zia_owneratom.set_arg(acct_cred_points_str(), 70)
    sue_ownerdelta.set_owneratom(zia_owneratom)
    sue_owner = ownerunit_shop("Sue")
    sue_owner.set_credor_respect(100)
    yao_str = "Yao"
    yao_owneratom = owneratom_shop(dimen, INSERT_str())
    yao_owneratom.set_arg(acct_name_str(), yao_str)
    yao_owneratom.set_arg(acct_cred_points_str(), 30)
    sue_ownerdelta.set_owneratom(yao_owneratom)

    sue_owner = ownerunit_shop("Sue")
    assert owner_built_from_delta_is_valid(sue_ownerdelta, sue_owner)

    # WHEN
    ownerdelta_dict = sue_ownerdelta.get_ordered_dict(5)

    # THEN
    # delta_zia = ownerdelta_dict.get(0)
    # delta_yao = ownerdelta_dict.get(1)
    # delta_pool = ownerdelta_dict.get(2)
    # assert delta_zia == zia_owneratom
    # assert delta_yao == yao_owneratom
    # assert delta_pool == pool_owneratom
    assert ownerdelta_dict.get(5) == zia_owneratom.get_dict()
    assert ownerdelta_dict.get(6) == yao_owneratom.get_dict()
    assert ownerdelta_dict.get(7) == pool_owneratom.get_dict()


def test_get_ownerdelta_from_ordered_dict_ReturnsObj():
    # ESTABLISH
    expected_ownerdelta = ownerdelta_shop()
    pool_owneratom = owneratom_shop(ownerunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_owneratom.set_jvalue(pool_attribute, 100)
    expected_ownerdelta.set_owneratom(pool_owneratom)
    dimen = owner_acctunit_str()
    zia_str = "Zia"
    zia_owneratom = owneratom_shop(dimen, INSERT_str())
    zia_owneratom.set_arg(acct_name_str(), zia_str)
    zia_owneratom.set_arg(acct_cred_points_str(), 70)
    expected_ownerdelta.set_owneratom(zia_owneratom)
    sue_owner = ownerunit_shop("Sue")
    sue_owner.set_credor_respect(100)
    yao_str = "Yao"
    yao_owneratom = owneratom_shop(dimen, INSERT_str())
    yao_owneratom.set_arg(acct_name_str(), yao_str)
    yao_owneratom.set_arg(acct_cred_points_str(), 30)
    expected_ownerdelta.set_owneratom(yao_owneratom)
    ownerdelta_dict = expected_ownerdelta.get_ordered_dict(5)

    # WHEN
    generated_ownerdelta = get_ownerdelta_from_ordered_dict(ownerdelta_dict)

    # THEN
    # delta_zia = ownerdelta_dict.get(0)
    # delta_yao = ownerdelta_dict.get(1)
    # delta_pool = ownerdelta_dict.get(2)
    # assert delta_zia == zia_owneratom
    # assert delta_yao == yao_owneratom
    # assert delta_pool == pool_owneratom
    # assert ownerdelta_dict.get(5) == zia_owneratom.get_dict()
    # assert ownerdelta_dict.get(6) == yao_owneratom.get_dict()
    # assert ownerdelta_dict.get(7) == pool_owneratom.get_dict()
    assert generated_ownerdelta == expected_ownerdelta


def test_OwnerDelta_get_json_ReturnsObj():
    # ESTABLISH
    sue_ownerdelta = ownerdelta_shop()
    pool_owneratom = owneratom_shop(ownerunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_owneratom.set_jvalue(pool_attribute, 100)
    sue_ownerdelta.set_owneratom(pool_owneratom)
    dimen = owner_acctunit_str()
    zia_str = "Zia"
    zia_owneratom = owneratom_shop(dimen, INSERT_str())
    zia_owneratom.set_arg(acct_name_str(), zia_str)
    zia_owneratom.set_arg(acct_cred_points_str(), 70)
    sue_ownerdelta.set_owneratom(zia_owneratom)
    yao_str = "Yao"
    yao_owneratom = owneratom_shop(dimen, INSERT_str())
    yao_owneratom.set_arg(acct_name_str(), yao_str)
    yao_owneratom.set_arg(acct_cred_points_str(), 30)
    sue_ownerdelta.set_owneratom(yao_owneratom)

    # WHEN
    delta_start_int = 5
    ownerdelta_json = sue_ownerdelta.get_json(delta_start_int)

    # THEN
    assert x_is_json(ownerdelta_json)


def test_OwnerDelta_owneratom_exists_ReturnsObj():
    # ESTABLISH
    x_ownerdelta = ownerdelta_shop()

    # WHEN / THEN
    dimen = owner_acctunit_str()
    zia_str = "Zia"
    zia_owneratom = owneratom_shop(dimen, INSERT_str())
    zia_owneratom.set_arg(acct_name_str(), zia_str)
    zia_owneratom.set_arg(acct_cred_points_str(), 70)
    assert x_ownerdelta.owneratom_exists(zia_owneratom) is False

    # WHEN
    x_ownerdelta.set_owneratom(zia_owneratom)

    # THEN
    assert x_ownerdelta.owneratom_exists(zia_owneratom)


def test_OwnerDelta_is_empty_ReturnsObj():
    # ESTABLISH
    x_ownerdelta = ownerdelta_shop()

    # WHEN / THEN
    dimen = owner_acctunit_str()
    zia_str = "Zia"
    zia_owneratom = owneratom_shop(dimen, INSERT_str())
    zia_owneratom.set_arg(acct_name_str(), zia_str)
    zia_owneratom.set_arg(acct_cred_points_str(), 70)
    assert x_ownerdelta.is_empty()

    # WHEN
    x_ownerdelta.set_owneratom(zia_owneratom)

    # THEN
    assert x_ownerdelta.is_empty() is False
