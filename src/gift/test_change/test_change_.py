from src._road.road import create_road, get_default_real_id_roadnode as root_label
from src.bud.acct import acctunit_shop
from src.gift.atom_config import (
    atom_update,
    atom_insert,
    atom_delete,
    bud_acctunit_text,
    bud_acct_membership_text,
    bud_idea_awardlink_text,
    bud_ideaunit_text,
    acct_id_str,
    group_id_str,
    parent_road_str,
)
from src.gift.atom import atomunit_shop
from src.gift.change import ChangeUnit, changeunit_shop, bud_built_from_change_is_valid
from src.bud.bud import budunit_shop
from src.gift.examples.example_changes import get_changeunit_example1
from src._instrument.python import x_is_json
from pytest import raises as pytest_raises


def test_ChangeUnit_exists():
    # ESTABLISH / WHEN
    x_changeunit = ChangeUnit()

    # THEN
    assert x_changeunit.atomunits is None
    assert x_changeunit._bud_build_validated is None


def test_changeunit_shop_ReturnsCorrectObj():
    # ESTABLISH / WHEN
    ex1_changeunit = changeunit_shop()

    # THEN
    assert ex1_changeunit.atomunits == {}
    assert ex1_changeunit._bud_build_validated is False


def test_ChangeUnit_set_atomunit_CorrectlySets_BudUnitSimpleAttrs():
    # ESTABLISH
    ex1_changeunit = changeunit_shop()
    attribute_value = 55
    category = "budunit"
    opt1_arg = "tally"
    optional_args = {opt1_arg: attribute_value}
    required_args = {}
    bud_mass_atomunit = atomunit_shop(
        category,
        atom_update(),
        required_args=required_args,
        optional_args=optional_args,
    )
    assert ex1_changeunit.atomunits == {}
    assert bud_mass_atomunit.atom_order is None

    # WHEN
    ex1_changeunit.set_atomunit(bud_mass_atomunit)

    # THEN
    assert len(ex1_changeunit.atomunits) == 1
    x_update_dict = ex1_changeunit.atomunits.get(atom_update())
    # print(f"{x_update_dict=}")
    x_category_atomunit = x_update_dict.get(category)
    print(f"{x_category_atomunit=}")
    assert x_category_atomunit == bud_mass_atomunit
    assert bud_mass_atomunit.atom_order is not None


def test_ChangeUnit_set_atomunit_RaisesErrorWhen_is_valid_IsFalse():
    # ESTABLISH
    ex1_changeunit = changeunit_shop()
    x_category = bud_acctunit_text()
    bud_mass_atomunit = atomunit_shop(x_category, atom_update())

    # WHEN
    with pytest_raises(Exception) as excinfo:
        ex1_changeunit.set_atomunit(bud_mass_atomunit)
    assert (
        str(excinfo.value)
        == f"""'{x_category}' UPDATE AtomUnit is invalid
                x_atomunit.is_required_args_valid()=False
                x_atomunit.is_optional_args_valid()=True"""
    )


def test_ChangUnit_atomunit_exists_ReturnsObj_bud_acctunit_text():
    # ESTABLISH
    bob_text = "Bob"
    farm_changeunit = changeunit_shop()
    bob_atomunit = atomunit_shop(bud_acctunit_text(), atom_insert())
    bob_atomunit.set_arg(acct_id_str(), bob_text)
    assert not farm_changeunit.atomunit_exists(bob_atomunit)

    # WHEN
    farm_changeunit.set_atomunit(bob_atomunit)

    # THEN
    assert farm_changeunit.atomunit_exists(bob_atomunit)


def test_ChangUnit_atomunit_exists_ReturnsObj_bud_acct_membership_text():
    # ESTABLISH
    bob_text = "Bob"
    iowa_text = ";Iowa"
    farm_changeunit = changeunit_shop()
    bob_iowa_atomunit = atomunit_shop(bud_acct_membership_text(), atom_insert())
    bob_iowa_atomunit.set_arg(group_id_str(), iowa_text)
    bob_iowa_atomunit.set_arg(acct_id_str(), bob_text)
    assert not farm_changeunit.atomunit_exists(bob_iowa_atomunit)

    # WHEN
    farm_changeunit.set_atomunit(bob_iowa_atomunit)

    # THEN
    assert farm_changeunit.atomunit_exists(bob_iowa_atomunit)


def test_ChangeUnit_get_atom_ReturnsCorrectObj():
    # ESTABLISH
    ex1_changeunit = changeunit_shop()
    budunit_text = "budunit"
    opt_arg1 = "tally"
    opt_value = 55
    budunit_atomunit = atomunit_shop(budunit_text, atom_update())
    budunit_atomunit.set_optional_arg(x_key=opt_arg1, x_value=opt_value)
    ex1_changeunit.set_atomunit(budunit_atomunit)

    # WHEN
    gen_atomunit = ex1_changeunit.get_atomunit(
        atom_update(), category=budunit_text, required_args=[]
    )

    # THEN
    assert gen_atomunit == budunit_atomunit


def test_ChangeUnit_add_atomunit_CorrectlySets_BudUnitSimpleAttrs():
    # ESTABLISH
    ex1_changeunit = changeunit_shop()
    assert ex1_changeunit.atomunits == {}

    # WHEN
    op2_arg = "tally"
    op2_value = 55
    budunit_text = "budunit"
    required_args = {}
    optional_args = {op2_arg: op2_value}
    ex1_changeunit.add_atomunit(
        budunit_text,
        atom_update(),
        required_args,
        optional_args=optional_args,
    )

    # THEN
    assert len(ex1_changeunit.atomunits) == 1
    x_update_dict = ex1_changeunit.atomunits.get(atom_update())
    x_atomunit = x_update_dict.get(budunit_text)
    assert x_atomunit is not None
    assert x_atomunit.category == budunit_text


def test_ChangeUnit_add_atomunit_CorrectlySets_BudUnit_acctunits():
    # ESTABLISH
    ex1_changeunit = changeunit_shop()
    assert ex1_changeunit.atomunits == {}

    # WHEN
    bob_text = "Bob"
    bob_credit_score = 55
    bob_debtit_score = 66
    bob_acctunit = acctunit_shop(bob_text, bob_credit_score, bob_debtit_score)
    cw_text = "credit_score"
    dw_text = "debtit_score"
    print(f"{bob_acctunit.get_dict()=}")
    bob_required_dict = {acct_id_str(): bob_acctunit.get_dict().get(acct_id_str())}
    bob_optional_dict = {cw_text: bob_acctunit.get_dict().get(cw_text)}
    bob_optional_dict[dw_text] = bob_acctunit.get_dict().get(dw_text)
    print(f"{bob_required_dict=}")
    acctunit_text = bud_acctunit_text()
    ex1_changeunit.add_atomunit(
        category=acctunit_text,
        crud_text=atom_insert(),
        required_args=bob_required_dict,
        optional_args=bob_optional_dict,
    )
    # THEN
    assert len(ex1_changeunit.atomunits) == 1
    assert (
        ex1_changeunit.atomunits.get(atom_insert()).get(acctunit_text).get(bob_text)
        is not None
    )


def test_ChangeUnit_get_crud_atomunits_list_ReturnsCorrectObj():
    # ESTABLISH
    ex1_changeunit = get_changeunit_example1()
    assert len(ex1_changeunit.atomunits.get(atom_update()).keys()) == 1
    assert ex1_changeunit.atomunits.get(atom_insert()) is None
    assert len(ex1_changeunit.atomunits.get(atom_delete()).keys()) == 1

    # WHEN
    sue_atom_order_dict = ex1_changeunit._get_crud_atomunits_list()

    # THEN
    assert len(sue_atom_order_dict) == 2
    print(f"{sue_atom_order_dict.keys()=}")
    # print(f"{sue_atom_order_dict.get(atom_update())=}")
    assert len(sue_atom_order_dict.get(atom_update())) == 1
    assert len(sue_atom_order_dict.get(atom_delete())) == 1
    # for crud_text, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_text=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.category=}")


def test_ChangeUnit_get_category_sorted_atomunits_list_ReturnsCorrectObj():
    # ESTABLISH
    ex1_changeunit = get_changeunit_example1()
    update_dict = ex1_changeunit.atomunits.get(atom_update())
    assert len(update_dict.keys()) == 1
    print(f"{update_dict.keys()=}")
    assert ex1_changeunit.atomunits.get(atom_insert()) is None
    delete_dict = ex1_changeunit.atomunits.get(atom_delete())
    assert len(delete_dict.keys()) == 1

    # WHEN
    sue_atoms_list = ex1_changeunit.get_category_sorted_atomunits_list()

    # THEN
    assert len(sue_atoms_list) == 2
    assert sue_atoms_list[0] == update_dict.get("budunit")
    z_atom = sue_atoms_list[1]
    print(f"{z_atom=}")
    print(delete_dict.get(bud_acctunit_text()).keys())
    zia_acctunit_delete = delete_dict.get(bud_acctunit_text()).get("Zia")
    assert sue_atoms_list[1] == zia_acctunit_delete
    # print(f"{sue_atom_order_dict.keys()=}")
    # # print(f"{sue_atom_order_dict.get(atom_update())=}")
    # assert len(sue_atom_order_dict.get(atom_update())) == 1
    # assert len(sue_atom_order_dict.get(atom_delete())) == 1
    # for crud_text, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_text=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.category=}")


# def test_ChangeUnit_add_atomunit_CorrectlySets_BudUnit_max_tree_traverse():
#     # ESTABLISH
#     ex1_changeunit = changeunit_shop(get_sue_road())
#     assert ex1_changeunit.atomunits == {}

#     # WHEN
#     opt2_value = 55
#     category = "budunit"
#     opt2_arg = "mass"
#     mass_atomunit = atomunit_shop(category, atom_update())
#     mass_atomunit.set_optional_arg(opt2_arg, opt2_value)
#     ex1_changeunit.set_atomunit(mass_atomunit)
#     # THEN
#     assert len(ex1_changeunit.atomunits.get(atom_update()).keys()) == 1
#     sue_budunit_dict = ex1_changeunit.atomunits.get(atom_update())
#     sue_mass_atomunit = sue_budunit_dict.get(category)
#     print(f"{sue_mass_atomunit=}")
#     assert mass_atomunit == sue_mass_atomunit

#     # WHEN
#     new2_value = 66
#     x_attribute = "max_tree_traverse"
#     required_args = {x_attribute: new2_value}
#     x_atomunit = atomunit_shop(x_attribute, atom_update(), None, required_args)
#     ex1_changeunit.set_atomunit(x_atomunit)
#     # THEN
#     print(f"{ex1_changeunit.atomunits.keys()=}")
#     print(f"{ex1_changeunit.atomunits.get(atom_update()).keys()=}")
#     assert len(ex1_changeunit.atomunits.get(atom_update()).keys()) == 2
#     assert x_atomunit == ex1_changeunit.atomunits.get(atom_update()).get(x_attribute)

#     # WHEN
#     new3_value = 77
#     x_attribute = "credor_respect"
#     required_args = {x_attribute: new3_value}
#     x_atomunit = atomunit_shop(x_attribute, atom_update(), None, required_args)
#     ex1_changeunit.set_atomunit(x_atomunit)
#     # THEN
#     assert len(ex1_changeunit.atomunits.get(atom_update()).keys()) == 3
#     assert x_atomunit == ex1_changeunit.atomunits.get(atom_update()).get(x_attribute)

#     # WHEN
#     new4_value = 88
#     x_attribute = "debtor_respect"
#     required_args = {x_attribute: new4_value}
#     x_atomunit = atomunit_shop(x_attribute, atom_update(), None, required_args)
#     ex1_changeunit.set_atomunit(x_atomunit)
#     # THEN
#     assert len(ex1_changeunit.atomunits.get(atom_update()).keys()) == 4
#     assert x_atomunit == ex1_changeunit.atomunits.get(atom_update()).get(x_attribute)


def test_ChangeUnit_get_sorted_atomunits_ReturnsCorrectObj():
    # ESTABLISH
    ex1_changeunit = get_changeunit_example1()
    budunit_text = "budunit"
    update_dict = ex1_changeunit.atomunits.get(atom_update())
    assert len(update_dict.keys()) == 1
    assert update_dict.get(budunit_text) is not None
    print(f"atom_order 28 {ex1_changeunit.atomunits.get(atom_update()).keys()=}")
    delete_dict = ex1_changeunit.atomunits.get(atom_delete())
    assert len(delete_dict.keys()) == 1
    assert delete_dict.get(bud_acctunit_text()) is not None
    print(f"atom_order 26 {ex1_changeunit.atomunits.get(atom_delete()).keys()=}")

    # WHEN
    sue_atom_order_list = ex1_changeunit.get_sorted_atomunits()

    # THEN
    assert len(sue_atom_order_list) == 2
    print(delete_dict.get(bud_acctunit_text()).keys())
    zia_acctunit_delete = delete_dict.get(bud_acctunit_text()).get("Zia")
    # for atomunit in sue_atom_order_list:
    #     print(f"{atomunit.atom_order=}")
    assert sue_atom_order_list[0] == zia_acctunit_delete
    assert sue_atom_order_list[1] == update_dict.get(budunit_text)
    # for crud_text, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_text=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.category=}")


def test_ChangeUnit_get_sorted_atomunits_ReturnsCorrectObj_IdeaUnitsSorted():
    # ESTABLISH
    x_real_id = root_label()
    sports_text = "sports"
    sports_road = create_road(x_real_id, sports_text)
    knee_text = "knee"
    x_category = bud_ideaunit_text()
    label_text = "label"
    sports_insert_ideaunit_atomunit = atomunit_shop(x_category, atom_insert())
    sports_insert_ideaunit_atomunit.set_required_arg(label_text, sports_text)
    sports_insert_ideaunit_atomunit.set_required_arg(parent_road_str(), x_real_id)
    knee_insert_ideaunit_atomunit = atomunit_shop(x_category, atom_insert())
    knee_insert_ideaunit_atomunit.set_required_arg(label_text, knee_text)
    knee_insert_ideaunit_atomunit.set_required_arg(parent_road_str(), sports_road)
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(knee_insert_ideaunit_atomunit)
    x_changeunit.set_atomunit(sports_insert_ideaunit_atomunit)

    # WHEN
    x_atom_order_list = x_changeunit.get_sorted_atomunits()

    # THEN
    assert len(x_atom_order_list) == 2
    # for atomunit in x_atom_order_list:
    #     print(f"{atomunit.required_args=}")
    assert x_atom_order_list[0] == sports_insert_ideaunit_atomunit
    assert x_atom_order_list[1] == knee_insert_ideaunit_atomunit
    # for crud_text, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_text=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.category=}")


def test_ChangeUnit_get_sorted_atomunits_ReturnsCorrectObj_Road_Sorted():
    # ESTABLISH
    x_real_id = root_label()
    sports_text = "sports"
    sports_road = create_road(x_real_id, sports_text)
    knee_text = "knee"
    knee_road = create_road(sports_road, knee_text)
    x_category = bud_idea_awardlink_text()
    road_text = "road"
    swimmers_text = ",Swimmers"
    sports_awardlink_atomunit = atomunit_shop(x_category, atom_insert())
    sports_awardlink_atomunit.set_required_arg(group_id_str(), swimmers_text)
    sports_awardlink_atomunit.set_required_arg(road_text, sports_road)
    knee_awardlink_atomunit = atomunit_shop(x_category, atom_insert())
    knee_awardlink_atomunit.set_required_arg(group_id_str(), swimmers_text)
    knee_awardlink_atomunit.set_required_arg(road_text, knee_road)
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(knee_awardlink_atomunit)
    x_changeunit.set_atomunit(sports_awardlink_atomunit)

    # WHEN
    x_atom_order_list = x_changeunit.get_sorted_atomunits()

    # THEN
    assert len(x_atom_order_list) == 2
    # for atomunit in x_atom_order_list:
    #     print(f"{atomunit.required_args=}")
    assert x_atom_order_list[0] == sports_awardlink_atomunit
    assert x_atom_order_list[1] == knee_awardlink_atomunit
    # for crud_text, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_text=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.category=}")


def test_bud_built_from_change_is_valid_ReturnsCorrectObjEstablishWithNoBud_scenario1():
    # ESTABLISH
    sue_changeunit = changeunit_shop()

    budunit_text = "budunit"
    x_atomunit = atomunit_shop(budunit_text, atom_update())
    x_attribute = "credor_respect"
    x_atomunit.set_optional_arg(x_attribute, 100)
    sue_changeunit.set_atomunit(x_atomunit)

    category = bud_acctunit_text()
    zia_text = "Zia"
    x_atomunit = atomunit_shop(category, atom_insert())
    x_atomunit.set_arg(acct_id_str(), zia_text)
    x_atomunit.set_arg("credit_score", "70 is the number")
    sue_changeunit.set_atomunit(x_atomunit)

    # WHEN/THEN
    assert bud_built_from_change_is_valid(sue_changeunit) is False


def test_bud_built_from_change_is_valid_ReturnsCorrectObjEstablishWithNoBud_scenario2():
    sue_changeunit = changeunit_shop()
    category = bud_acctunit_text()
    # WHEN
    yao_text = "Yao"
    x_atomunit = atomunit_shop(category, atom_insert())
    x_atomunit.set_arg(acct_id_str(), yao_text)
    x_atomunit.set_arg("credit_score", 30)
    sue_changeunit.set_atomunit(x_atomunit)

    # THEN
    assert bud_built_from_change_is_valid(sue_changeunit)

    # WHEN
    bob_text = "Bob"
    x_atomunit = atomunit_shop(category, atom_insert())
    x_atomunit.set_arg(acct_id_str(), bob_text)
    x_atomunit.set_arg("credit_score", "70 is the number")
    sue_changeunit.set_atomunit(x_atomunit)

    # THEN
    assert bud_built_from_change_is_valid(sue_changeunit) is False


def test_ChangeUnit_get_ordered_atomunits_ReturnsCorrectObj_EstablishWithNoStartingNumber():
    # ESTABLISH
    sue_changeunit = changeunit_shop()
    budunit_text = "budunit"
    pool_atomunit = atomunit_shop(budunit_text, atom_update())
    pool_attribute = "credor_respect"
    pool_atomunit.set_optional_arg(pool_attribute, 100)
    sue_changeunit.set_atomunit(pool_atomunit)
    category = bud_acctunit_text()
    zia_text = "Zia"
    zia_atomunit = atomunit_shop(category, atom_insert())
    zia_atomunit.set_arg(acct_id_str(), zia_text)
    zia_atomunit.set_arg("credit_score", 70)
    sue_changeunit.set_atomunit(zia_atomunit)
    sue_bud = budunit_shop("Sue")
    sue_bud.set_credor_respect(100)
    yao_text = "Yao"
    yao_atomunit = atomunit_shop(category, atom_insert())
    yao_atomunit.set_arg(acct_id_str(), yao_text)
    yao_atomunit.set_arg("credit_score", 30)
    sue_changeunit.set_atomunit(yao_atomunit)

    sue_bud = budunit_shop("Sue")
    assert bud_built_from_change_is_valid(sue_changeunit, sue_bud)

    # WHEN
    changeunit_dict = sue_changeunit.get_ordered_atomunits()

    # THEN
    # change_zia = changeunit_dict.get(0)
    # change_yao = changeunit_dict.get(1)
    # change_pool = changeunit_dict.get(2)
    # assert change_zia == zia_atomunit
    # assert change_yao == yao_atomunit
    # assert change_pool == pool_atomunit
    assert changeunit_dict.get(0) == zia_atomunit
    assert changeunit_dict.get(1) == yao_atomunit
    assert changeunit_dict.get(2) == pool_atomunit


def test_ChangeUnit_get_ordered_atomunits_ReturnsCorrectObj_EstablishWithStartingNumber():
    # ESTABLISH
    sue_changeunit = changeunit_shop()
    budunit_text = "budunit"
    pool_atomunit = atomunit_shop(budunit_text, atom_update())
    pool_attribute = "credor_respect"
    pool_atomunit.set_optional_arg(pool_attribute, 100)
    sue_changeunit.set_atomunit(pool_atomunit)
    category = bud_acctunit_text()
    zia_text = "Zia"
    zia_atomunit = atomunit_shop(category, atom_insert())
    zia_atomunit.set_arg(acct_id_str(), zia_text)
    zia_atomunit.set_arg("credit_score", 70)
    sue_changeunit.set_atomunit(zia_atomunit)
    sue_bud = budunit_shop("Sue")
    sue_bud.set_credor_respect(100)
    yao_text = "Yao"
    yao_atomunit = atomunit_shop(category, atom_insert())
    yao_atomunit.set_arg(acct_id_str(), yao_text)
    yao_atomunit.set_arg("credit_score", 30)
    sue_changeunit.set_atomunit(yao_atomunit)

    sue_bud = budunit_shop("Sue")
    assert bud_built_from_change_is_valid(sue_changeunit, sue_bud)

    # WHEN
    changeunit_dict = sue_changeunit.get_ordered_atomunits(5)

    # THEN
    # change_zia = changeunit_dict.get(0)
    # change_yao = changeunit_dict.get(1)
    # change_pool = changeunit_dict.get(2)
    # assert change_zia == zia_atomunit
    # assert change_yao == yao_atomunit
    # assert change_pool == pool_atomunit
    assert changeunit_dict.get(5) == zia_atomunit
    assert changeunit_dict.get(6) == yao_atomunit
    assert changeunit_dict.get(7) == pool_atomunit


def test_ChangeUnit_get_ordered_dict_ReturnsCorrectObj_EstablishWithStartingNumber():
    # ESTABLISH
    sue_changeunit = changeunit_shop()
    budunit_text = "budunit"
    pool_atomunit = atomunit_shop(budunit_text, atom_update())
    pool_attribute = "credor_respect"
    pool_atomunit.set_optional_arg(pool_attribute, 100)
    sue_changeunit.set_atomunit(pool_atomunit)
    category = bud_acctunit_text()
    zia_text = "Zia"
    zia_atomunit = atomunit_shop(category, atom_insert())
    zia_atomunit.set_arg(acct_id_str(), zia_text)
    zia_atomunit.set_arg("credit_score", 70)
    sue_changeunit.set_atomunit(zia_atomunit)
    sue_bud = budunit_shop("Sue")
    sue_bud.set_credor_respect(100)
    yao_text = "Yao"
    yao_atomunit = atomunit_shop(category, atom_insert())
    yao_atomunit.set_arg(acct_id_str(), yao_text)
    yao_atomunit.set_arg("credit_score", 30)
    sue_changeunit.set_atomunit(yao_atomunit)

    sue_bud = budunit_shop("Sue")
    assert bud_built_from_change_is_valid(sue_changeunit, sue_bud)

    # WHEN
    changeunit_dict = sue_changeunit.get_ordered_dict(5)

    # THEN
    # change_zia = changeunit_dict.get(0)
    # change_yao = changeunit_dict.get(1)
    # change_pool = changeunit_dict.get(2)
    # assert change_zia == zia_atomunit
    # assert change_yao == yao_atomunit
    # assert change_pool == pool_atomunit
    assert changeunit_dict.get(5) == zia_atomunit.get_dict()
    assert changeunit_dict.get(6) == yao_atomunit.get_dict()
    assert changeunit_dict.get(7) == pool_atomunit.get_dict()


def test_ChangeUnit_get_json_ReturnsCorrectObj():
    # ESTABLISH
    sue_changeunit = changeunit_shop()
    budunit_text = "budunit"
    pool_atomunit = atomunit_shop(budunit_text, atom_update())
    pool_attribute = "credor_respect"
    pool_atomunit.set_optional_arg(pool_attribute, 100)
    sue_changeunit.set_atomunit(pool_atomunit)
    category = bud_acctunit_text()
    zia_text = "Zia"
    zia_atomunit = atomunit_shop(category, atom_insert())
    zia_atomunit.set_arg(acct_id_str(), zia_text)
    zia_atomunit.set_arg("credit_score", 70)
    sue_changeunit.set_atomunit(zia_atomunit)
    yao_text = "Yao"
    yao_atomunit = atomunit_shop(category, atom_insert())
    yao_atomunit.set_arg(acct_id_str(), yao_text)
    yao_atomunit.set_arg("credit_score", 30)
    sue_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    change_start_int = 5
    changeunit_json = sue_changeunit.get_json(change_start_int)

    # THEN
    assert x_is_json(changeunit_json)


def test_ChangeUnit_atomunit_exists_ReturnsCorrectObj():
    # ESTABLISH
    farm_changeunit = changeunit_shop()

    # WHEN / THEN
    category = bud_acctunit_text()
    zia_text = "Zia"
    zia_atomunit = atomunit_shop(category, atom_insert())
    zia_atomunit.set_arg(acct_id_str(), zia_text)
    zia_atomunit.set_arg("credit_score", 70)
    assert farm_changeunit.atomunit_exists(zia_atomunit) is False

    # WHEN
    farm_changeunit.set_atomunit(zia_atomunit)

    # THEN
    assert farm_changeunit.atomunit_exists(zia_atomunit)
