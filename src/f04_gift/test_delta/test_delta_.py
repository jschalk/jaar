from src.f01_road.road import create_road, get_default_fiscal_title as root_title
from src.f02_bud.acct import acctunit_shop
from src.f02_bud.bud_tool import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_itemunit_str,
    bud_item_awardlink_str,
)
from src.f04_gift.atom_config import (
    atom_update,
    atom_insert,
    atom_delete,
    acct_name_str,
    awardee_tag_str,
    group_label_str,
    parent_road_str,
    item_title_str,
    credit_belief_str,
    debtit_belief_str,
)
from src.f04_gift.atom import atomunit_shop
from src.f04_gift.delta import (
    DeltaUnit,
    deltaunit_shop,
    bud_built_from_delta_is_valid,
)
from src.f02_bud.bud import budunit_shop
from src.f04_gift.examples.example_deltas import get_deltaunit_example1
from src.f00_instrument.dict_toolbox import x_is_json
from pytest import raises as pytest_raises


def test_DeltaUnit_exists():
    # ESTABLISH / WHEN
    x_deltaunit = DeltaUnit()

    # THEN
    assert x_deltaunit.atomunits is None
    assert x_deltaunit._bud_build_validated is None


def test_deltaunit_shop_ReturnsCorrectObj():
    # ESTABLISH / WHEN
    ex1_deltaunit = deltaunit_shop()

    # THEN
    assert ex1_deltaunit.atomunits == {}
    assert ex1_deltaunit._bud_build_validated is False


def test_DeltaUnit_set_atomunit_CorrectlySets_BudUnitSimpleAttrs():
    # ESTABLISH
    ex1_deltaunit = deltaunit_shop()
    attribute_value = 55
    category = budunit_str()
    opt1_arg = "tally"
    jvalues = {opt1_arg: attribute_value}
    jkeys = {}
    bud_mass_atomunit = atomunit_shop(
        category,
        atom_update(),
        jkeys=jkeys,
        jvalues=jvalues,
    )
    assert ex1_deltaunit.atomunits == {}
    assert bud_mass_atomunit.atom_order is None

    # WHEN
    ex1_deltaunit.set_atomunit(bud_mass_atomunit)

    # THEN
    assert len(ex1_deltaunit.atomunits) == 1
    x_update_dict = ex1_deltaunit.atomunits.get(atom_update())
    # print(f"{x_update_dict=}")
    x_category_atomunit = x_update_dict.get(category)
    print(f"{x_category_atomunit=}")
    assert x_category_atomunit == bud_mass_atomunit
    assert bud_mass_atomunit.atom_order is not None


def test_DeltaUnit_set_atomunit_RaisesErrorWhen_is_valid_IsFalse():
    # ESTABLISH
    ex1_deltaunit = deltaunit_shop()
    x_category = bud_acctunit_str()
    bud_mass_atomunit = atomunit_shop(x_category, atom_update())

    # WHEN
    with pytest_raises(Exception) as excinfo:
        ex1_deltaunit.set_atomunit(bud_mass_atomunit)
    assert (
        str(excinfo.value)
        == f"""'{x_category}' UPDATE AtomUnit is invalid
                x_atomunit.is_jkeys_valid()=False
                x_atomunit.is_jvalues_valid()=True"""
    )


def test_ChangUnit_atomunit_exists_ReturnsObj_bud_acctunit_str():
    # ESTABLISH
    bob_str = "Bob"
    x_deltaunit = deltaunit_shop()
    bob_atomunit = atomunit_shop(bud_acctunit_str(), atom_insert())
    bob_atomunit.set_arg(acct_name_str(), bob_str)
    assert not x_deltaunit.atomunit_exists(bob_atomunit)

    # WHEN
    x_deltaunit.set_atomunit(bob_atomunit)

    # THEN
    assert x_deltaunit.atomunit_exists(bob_atomunit)


def test_ChangUnit_atomunit_exists_ReturnsObj_bud_acct_membership_str():
    # ESTABLISH
    bob_str = "Bob"
    iowa_str = ";Iowa"
    x_deltaunit = deltaunit_shop()
    bob_iowa_atomunit = atomunit_shop(bud_acct_membership_str(), atom_insert())
    bob_iowa_atomunit.set_arg(group_label_str(), iowa_str)
    bob_iowa_atomunit.set_arg(acct_name_str(), bob_str)
    assert not x_deltaunit.atomunit_exists(bob_iowa_atomunit)

    # WHEN
    x_deltaunit.set_atomunit(bob_iowa_atomunit)

    # THEN
    assert x_deltaunit.atomunit_exists(bob_iowa_atomunit)


def test_DeltaUnit_get_atom_ReturnsCorrectObj():
    # ESTABLISH
    ex1_deltaunit = deltaunit_shop()
    opt_arg1 = "tally"
    opt_value = 55
    budunit_atomunit = atomunit_shop(budunit_str(), atom_update())
    budunit_atomunit.set_jvalue(x_key=opt_arg1, x_value=opt_value)
    ex1_deltaunit.set_atomunit(budunit_atomunit)

    # WHEN
    gen_atomunit = ex1_deltaunit.get_atomunit(
        atom_update(), category=budunit_str(), jkeys=[]
    )

    # THEN
    assert gen_atomunit == budunit_atomunit


def test_DeltaUnit_add_atomunit_CorrectlySets_BudUnitSimpleAttrs():
    # ESTABLISH
    ex1_deltaunit = deltaunit_shop()
    assert ex1_deltaunit.atomunits == {}

    # WHEN
    op2_arg = "tally"
    op2_value = 55
    jkeys = {}
    jvalues = {op2_arg: op2_value}
    ex1_deltaunit.add_atomunit(
        budunit_str(),
        atom_update(),
        jkeys,
        jvalues=jvalues,
    )

    # THEN
    assert len(ex1_deltaunit.atomunits) == 1
    x_update_dict = ex1_deltaunit.atomunits.get(atom_update())
    x_atomunit = x_update_dict.get(budunit_str())
    assert x_atomunit is not None
    assert x_atomunit.category == budunit_str()


def test_DeltaUnit_add_atomunit_CorrectlySets_BudUnit_acctunits():
    # ESTABLISH
    ex1_deltaunit = deltaunit_shop()
    assert ex1_deltaunit.atomunits == {}

    # WHEN
    bob_str = "Bob"
    bob_credit_belief = 55
    bob_debtit_belief = 66
    bob_acctunit = acctunit_shop(bob_str, bob_credit_belief, bob_debtit_belief)
    cw_str = credit_belief_str()
    dw_str = debtit_belief_str()
    print(f"{bob_acctunit.get_dict()=}")
    bob_required_dict = {acct_name_str(): bob_acctunit.get_dict().get(acct_name_str())}
    bob_optional_dict = {cw_str: bob_acctunit.get_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_acctunit.get_dict().get(dw_str)
    print(f"{bob_required_dict=}")
    acctunit_str = bud_acctunit_str()
    ex1_deltaunit.add_atomunit(
        category=acctunit_str,
        crud_str=atom_insert(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )
    # THEN
    assert len(ex1_deltaunit.atomunits) == 1
    assert (
        ex1_deltaunit.atomunits.get(atom_insert()).get(acctunit_str).get(bob_str)
        is not None
    )


def test_DeltaUnit_get_crud_atomunits_list_ReturnsCorrectObj():
    # ESTABLISH
    ex1_deltaunit = get_deltaunit_example1()
    assert len(ex1_deltaunit.atomunits.get(atom_update()).keys()) == 1
    assert ex1_deltaunit.atomunits.get(atom_insert()) is None
    assert len(ex1_deltaunit.atomunits.get(atom_delete()).keys()) == 1

    # WHEN
    sue_atom_order_dict = ex1_deltaunit._get_crud_atomunits_list()

    # THEN
    assert len(sue_atom_order_dict) == 2
    print(f"{sue_atom_order_dict.keys()=}")
    # print(f"{sue_atom_order_dict.get(atom_update())=}")
    assert len(sue_atom_order_dict.get(atom_update())) == 1
    assert len(sue_atom_order_dict.get(atom_delete())) == 1
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.category=}")


def test_DeltaUnit_get_category_sorted_atomunits_list_ReturnsCorrectObj():
    # ESTABLISH
    ex1_deltaunit = get_deltaunit_example1()
    update_dict = ex1_deltaunit.atomunits.get(atom_update())
    assert len(update_dict.keys()) == 1
    print(f"{update_dict.keys()=}")
    assert ex1_deltaunit.atomunits.get(atom_insert()) is None
    delete_dict = ex1_deltaunit.atomunits.get(atom_delete())
    assert len(delete_dict.keys()) == 1

    # WHEN
    sue_atoms_list = ex1_deltaunit.get_category_sorted_atomunits_list()

    # THEN
    assert len(sue_atoms_list) == 2
    assert sue_atoms_list[0] == update_dict.get(budunit_str())
    z_atom = sue_atoms_list[1]
    print(f"{z_atom=}")
    print(delete_dict.get(bud_acctunit_str()).keys())
    zia_acctunit_delete = delete_dict.get(bud_acctunit_str()).get("Zia")
    assert sue_atoms_list[1] == zia_acctunit_delete
    # print(f"{sue_atom_order_dict.keys()=}")
    # # print(f"{sue_atom_order_dict.get(atom_update())=}")
    # assert len(sue_atom_order_dict.get(atom_update())) == 1
    # assert len(sue_atom_order_dict.get(atom_delete())) == 1
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.category=}")


# def test_DeltaUnit_add_atomunit_CorrectlySets_BudUnit_max_tree_traverse():
#     # ESTABLISH
#     ex1_deltaunit = deltaunit_shop(get_sue_road())
#     assert ex1_deltaunit.atomunits == {}

#     # WHEN
#     opt2_value = 55
#     category = budunit_str()
#     opt2_arg = "mass"
#     mass_atomunit = atomunit_shop(category, atom_update())
#     mass_atomunit.set_jvalue(opt2_arg, opt2_value)
#     ex1_deltaunit.set_atomunit(mass_atomunit)
#     # THEN
#     assert len(ex1_deltaunit.atomunits.get(atom_update()).keys()) == 1
#     sue_budunit_dict = ex1_deltaunit.atomunits.get(atom_update())
#     sue_mass_atomunit = sue_budunit_dict.get(category)
#     print(f"{sue_mass_atomunit=}")
#     assert mass_atomunit == sue_mass_atomunit

#     # WHEN
#     new2_value = 66
#     x_attribute = "max_tree_traverse"
#     jkeys = {x_attribute: new2_value}
#     x_atomunit = atomunit_shop(x_attribute, atom_update(), None, jkeys)
#     ex1_deltaunit.set_atomunit(x_atomunit)
#     # THEN
#     print(f"{ex1_deltaunit.atomunits.keys()=}")
#     print(f"{ex1_deltaunit.atomunits.get(atom_update()).keys()=}")
#     assert len(ex1_deltaunit.atomunits.get(atom_update()).keys()) == 2
#     assert x_atomunit == ex1_deltaunit.atomunits.get(atom_update()).get(x_attribute)

#     # WHEN
#     new3_value = 77
#     x_attribute = "credor_respect"
#     jkeys = {x_attribute: new3_value}
#     x_atomunit = atomunit_shop(x_attribute, atom_update(), None, jkeys)
#     ex1_deltaunit.set_atomunit(x_atomunit)
#     # THEN
#     assert len(ex1_deltaunit.atomunits.get(atom_update()).keys()) == 3
#     assert x_atomunit == ex1_deltaunit.atomunits.get(atom_update()).get(x_attribute)

#     # WHEN
#     new4_value = 88
#     x_attribute = "debtor_respect"
#     jkeys = {x_attribute: new4_value}
#     x_atomunit = atomunit_shop(x_attribute, atom_update(), None, jkeys)
#     ex1_deltaunit.set_atomunit(x_atomunit)
#     # THEN
#     assert len(ex1_deltaunit.atomunits.get(atom_update()).keys()) == 4
#     assert x_atomunit == ex1_deltaunit.atomunits.get(atom_update()).get(x_attribute)


def test_DeltaUnit_get_sorted_atomunits_ReturnsCorrectObj():
    # ESTABLISH
    ex1_deltaunit = get_deltaunit_example1()
    update_dict = ex1_deltaunit.atomunits.get(atom_update())
    assert len(update_dict.keys()) == 1
    assert update_dict.get(budunit_str()) is not None
    print(f"atom_order 28 {ex1_deltaunit.atomunits.get(atom_update()).keys()=}")
    delete_dict = ex1_deltaunit.atomunits.get(atom_delete())
    assert len(delete_dict.keys()) == 1
    assert delete_dict.get(bud_acctunit_str()) is not None
    print(f"atom_order 26 {ex1_deltaunit.atomunits.get(atom_delete()).keys()=}")

    # WHEN
    sue_atom_order_list = ex1_deltaunit.get_sorted_atomunits()

    # THEN
    assert len(sue_atom_order_list) == 2
    print(delete_dict.get(bud_acctunit_str()).keys())
    zia_acctunit_delete = delete_dict.get(bud_acctunit_str()).get("Zia")
    # for atomunit in sue_atom_order_list:
    #     print(f"{atomunit.atom_order=}")
    assert sue_atom_order_list[0] == zia_acctunit_delete
    assert sue_atom_order_list[1] == update_dict.get(budunit_str())
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.category=}")


def test_DeltaUnit_get_sorted_atomunits_ReturnsCorrectObj_ItemUnitsSorted():
    # ESTABLISH
    x_fiscal_title = root_title()
    sports_str = "sports"
    sports_road = create_road(x_fiscal_title, sports_str)
    knee_str = "knee"
    x_category = bud_itemunit_str()
    sports_insert_itemunit_atomunit = atomunit_shop(x_category, atom_insert())
    sports_insert_itemunit_atomunit.set_jkey(item_title_str(), sports_str)
    sports_insert_itemunit_atomunit.set_jkey(parent_road_str(), x_fiscal_title)
    knee_insert_itemunit_atomunit = atomunit_shop(x_category, atom_insert())
    knee_insert_itemunit_atomunit.set_jkey(item_title_str(), knee_str)
    knee_insert_itemunit_atomunit.set_jkey(parent_road_str(), sports_road)
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(knee_insert_itemunit_atomunit)
    x_deltaunit.set_atomunit(sports_insert_itemunit_atomunit)

    # WHEN
    x_atom_order_list = x_deltaunit.get_sorted_atomunits()

    # THEN
    assert len(x_atom_order_list) == 2
    # for atomunit in x_atom_order_list:
    #     print(f"{atomunit.jkeys=}")
    assert x_atom_order_list[0] == sports_insert_itemunit_atomunit
    assert x_atom_order_list[1] == knee_insert_itemunit_atomunit
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.category=}")


def test_DeltaUnit_get_sorted_atomunits_ReturnsCorrectObj_Road_Sorted():
    # ESTABLISH
    x_fiscal_title = root_title()
    sports_str = "sports"
    sports_road = create_road(x_fiscal_title, sports_str)
    knee_str = "knee"
    knee_road = create_road(sports_road, knee_str)
    x_category = bud_item_awardlink_str()
    road_str = "road"
    swimmers_str = ",Swimmers"
    sports_awardlink_atomunit = atomunit_shop(x_category, atom_insert())
    sports_awardlink_atomunit.set_jkey(awardee_tag_str(), swimmers_str)
    sports_awardlink_atomunit.set_jkey(road_str, sports_road)
    knee_awardlink_atomunit = atomunit_shop(x_category, atom_insert())
    knee_awardlink_atomunit.set_jkey(awardee_tag_str(), swimmers_str)
    knee_awardlink_atomunit.set_jkey(road_str, knee_road)
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(knee_awardlink_atomunit)
    x_deltaunit.set_atomunit(sports_awardlink_atomunit)

    # WHEN
    x_atom_order_list = x_deltaunit.get_sorted_atomunits()

    # THEN
    assert len(x_atom_order_list) == 2
    # for atomunit in x_atom_order_list:
    #     print(f"{atomunit.jkeys=}")
    assert x_atom_order_list[0] == sports_awardlink_atomunit
    assert x_atom_order_list[1] == knee_awardlink_atomunit
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.category=}")


def test_bud_built_from_delta_is_valid_ReturnsCorrectObjEstablishWithNoBud_scenario1():
    # ESTABLISH
    sue_deltaunit = deltaunit_shop()

    x_atomunit = atomunit_shop(budunit_str(), atom_update())
    x_attribute = "credor_respect"
    x_atomunit.set_jvalue(x_attribute, 100)
    sue_deltaunit.set_atomunit(x_atomunit)

    category = bud_acctunit_str()
    zia_str = "Zia"
    x_atomunit = atomunit_shop(category, atom_insert())
    x_atomunit.set_arg(acct_name_str(), zia_str)
    x_atomunit.set_arg(credit_belief_str(), "70 is the number")
    sue_deltaunit.set_atomunit(x_atomunit)
    print(f"{sue_deltaunit=}")

    # WHEN / THEN
    assert bud_built_from_delta_is_valid(sue_deltaunit) is False


def test_bud_built_from_delta_is_valid_ReturnsCorrectObjEstablishWithNoBud_scenario2():
    sue_deltaunit = deltaunit_shop()
    category = bud_acctunit_str()
    # WHEN
    yao_str = "Yao"
    x_atomunit = atomunit_shop(category, atom_insert())
    x_atomunit.set_arg(acct_name_str(), yao_str)
    x_atomunit.set_arg(credit_belief_str(), 30)
    sue_deltaunit.set_atomunit(x_atomunit)

    # THEN
    assert bud_built_from_delta_is_valid(sue_deltaunit)

    # WHEN
    bob_str = "Bob"
    x_atomunit = atomunit_shop(category, atom_insert())
    x_atomunit.set_arg(acct_name_str(), bob_str)
    x_atomunit.set_arg(credit_belief_str(), "70 is the number")
    sue_deltaunit.set_atomunit(x_atomunit)

    # THEN
    assert bud_built_from_delta_is_valid(sue_deltaunit) is False


def test_DeltaUnit_get_ordered_atomunits_ReturnsCorrectObj_EstablishWithNoStartingNumber():
    # ESTABLISH
    sue_deltaunit = deltaunit_shop()
    pool_atomunit = atomunit_shop(budunit_str(), atom_update())
    pool_attribute = "credor_respect"
    pool_atomunit.set_jvalue(pool_attribute, 100)
    sue_deltaunit.set_atomunit(pool_atomunit)
    category = bud_acctunit_str()
    zia_str = "Zia"
    zia_atomunit = atomunit_shop(category, atom_insert())
    zia_atomunit.set_arg(acct_name_str(), zia_str)
    zia_atomunit.set_arg(credit_belief_str(), 70)
    sue_deltaunit.set_atomunit(zia_atomunit)
    sue_bud = budunit_shop("Sue")
    sue_bud.set_credor_respect(100)
    yao_str = "Yao"
    yao_atomunit = atomunit_shop(category, atom_insert())
    yao_atomunit.set_arg(acct_name_str(), yao_str)
    yao_atomunit.set_arg(credit_belief_str(), 30)
    sue_deltaunit.set_atomunit(yao_atomunit)

    sue_bud = budunit_shop("Sue")
    assert bud_built_from_delta_is_valid(sue_deltaunit, sue_bud)

    # WHEN
    deltaunit_dict = sue_deltaunit.get_ordered_atomunits()

    # THEN
    # delta_zia = deltaunit_dict.get(0)
    # delta_yao = deltaunit_dict.get(1)
    # delta_pool = deltaunit_dict.get(2)
    # assert delta_zia == zia_atomunit
    # assert delta_yao == yao_atomunit
    # assert delta_pool == pool_atomunit
    assert deltaunit_dict.get(0) == zia_atomunit
    assert deltaunit_dict.get(1) == yao_atomunit
    assert deltaunit_dict.get(2) == pool_atomunit


def test_DeltaUnit_get_ordered_atomunits_ReturnsCorrectObj_EstablishWithStartingNumber():
    # ESTABLISH
    sue_deltaunit = deltaunit_shop()
    pool_atomunit = atomunit_shop(budunit_str(), atom_update())
    pool_attribute = "credor_respect"
    pool_atomunit.set_jvalue(pool_attribute, 100)
    sue_deltaunit.set_atomunit(pool_atomunit)
    category = bud_acctunit_str()
    zia_str = "Zia"
    zia_atomunit = atomunit_shop(category, atom_insert())
    zia_atomunit.set_arg(acct_name_str(), zia_str)
    zia_atomunit.set_arg(credit_belief_str(), 70)
    sue_deltaunit.set_atomunit(zia_atomunit)
    sue_bud = budunit_shop("Sue")
    sue_bud.set_credor_respect(100)
    yao_str = "Yao"
    yao_atomunit = atomunit_shop(category, atom_insert())
    yao_atomunit.set_arg(acct_name_str(), yao_str)
    yao_atomunit.set_arg(credit_belief_str(), 30)
    sue_deltaunit.set_atomunit(yao_atomunit)

    sue_bud = budunit_shop("Sue")
    assert bud_built_from_delta_is_valid(sue_deltaunit, sue_bud)

    # WHEN
    deltaunit_dict = sue_deltaunit.get_ordered_atomunits(5)

    # THEN
    # delta_zia = deltaunit_dict.get(0)
    # delta_yao = deltaunit_dict.get(1)
    # delta_pool = deltaunit_dict.get(2)
    # assert delta_zia == zia_atomunit
    # assert delta_yao == yao_atomunit
    # assert delta_pool == pool_atomunit
    assert deltaunit_dict.get(5) == zia_atomunit
    assert deltaunit_dict.get(6) == yao_atomunit
    assert deltaunit_dict.get(7) == pool_atomunit


def test_DeltaUnit_get_ordered_dict_ReturnsCorrectObj_EstablishWithStartingNumber():
    # ESTABLISH
    sue_deltaunit = deltaunit_shop()
    pool_atomunit = atomunit_shop(budunit_str(), atom_update())
    pool_attribute = "credor_respect"
    pool_atomunit.set_jvalue(pool_attribute, 100)
    sue_deltaunit.set_atomunit(pool_atomunit)
    category = bud_acctunit_str()
    zia_str = "Zia"
    zia_atomunit = atomunit_shop(category, atom_insert())
    zia_atomunit.set_arg(acct_name_str(), zia_str)
    zia_atomunit.set_arg(credit_belief_str(), 70)
    sue_deltaunit.set_atomunit(zia_atomunit)
    sue_bud = budunit_shop("Sue")
    sue_bud.set_credor_respect(100)
    yao_str = "Yao"
    yao_atomunit = atomunit_shop(category, atom_insert())
    yao_atomunit.set_arg(acct_name_str(), yao_str)
    yao_atomunit.set_arg(credit_belief_str(), 30)
    sue_deltaunit.set_atomunit(yao_atomunit)

    sue_bud = budunit_shop("Sue")
    assert bud_built_from_delta_is_valid(sue_deltaunit, sue_bud)

    # WHEN
    deltaunit_dict = sue_deltaunit.get_ordered_dict(5)

    # THEN
    # delta_zia = deltaunit_dict.get(0)
    # delta_yao = deltaunit_dict.get(1)
    # delta_pool = deltaunit_dict.get(2)
    # assert delta_zia == zia_atomunit
    # assert delta_yao == yao_atomunit
    # assert delta_pool == pool_atomunit
    assert deltaunit_dict.get(5) == zia_atomunit.get_dict()
    assert deltaunit_dict.get(6) == yao_atomunit.get_dict()
    assert deltaunit_dict.get(7) == pool_atomunit.get_dict()


def test_DeltaUnit_get_json_ReturnsCorrectObj():
    # ESTABLISH
    sue_deltaunit = deltaunit_shop()
    pool_atomunit = atomunit_shop(budunit_str(), atom_update())
    pool_attribute = "credor_respect"
    pool_atomunit.set_jvalue(pool_attribute, 100)
    sue_deltaunit.set_atomunit(pool_atomunit)
    category = bud_acctunit_str()
    zia_str = "Zia"
    zia_atomunit = atomunit_shop(category, atom_insert())
    zia_atomunit.set_arg(acct_name_str(), zia_str)
    zia_atomunit.set_arg(credit_belief_str(), 70)
    sue_deltaunit.set_atomunit(zia_atomunit)
    yao_str = "Yao"
    yao_atomunit = atomunit_shop(category, atom_insert())
    yao_atomunit.set_arg(acct_name_str(), yao_str)
    yao_atomunit.set_arg(credit_belief_str(), 30)
    sue_deltaunit.set_atomunit(yao_atomunit)

    # WHEN
    delta_start_int = 5
    deltaunit_json = sue_deltaunit.get_json(delta_start_int)

    # THEN
    assert x_is_json(deltaunit_json)


def test_DeltaUnit_atomunit_exists_ReturnsCorrectObj():
    # ESTABLISH
    x_deltaunit = deltaunit_shop()

    # WHEN / THEN
    category = bud_acctunit_str()
    zia_str = "Zia"
    zia_atomunit = atomunit_shop(category, atom_insert())
    zia_atomunit.set_arg(acct_name_str(), zia_str)
    zia_atomunit.set_arg(credit_belief_str(), 70)
    assert x_deltaunit.atomunit_exists(zia_atomunit) is False

    # WHEN
    x_deltaunit.set_atomunit(zia_atomunit)

    # THEN
    assert x_deltaunit.atomunit_exists(zia_atomunit)
