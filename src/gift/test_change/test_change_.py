from src._road.road import create_road, get_default_real_id_roadnode as root_label
from src._world.char import charunit_shop
from src.gift.change import (
    ChangeUnit,
    changeunit_shop,
    world_built_from_change_is_valid,
    atomunit_shop,
    atom_update,
    atom_insert,
    atom_delete,
)
from src._world.world import worldunit_shop
from src.gift.examples.example_changes import get_changeunit_example1
from src._instrument.python import x_is_json
from pytest import raises as pytest_raises


def test_ChangeUnit_exists():
    # GIVEN / WHEN
    x_changeunit = ChangeUnit()

    # THEN
    assert x_changeunit.atomunits is None
    assert x_changeunit._world_build_validated is None


def test_changeunit_shop_ReturnsCorrectObj():
    # GIVEN / WHEN
    ex1_changeunit = changeunit_shop()

    # THEN
    assert ex1_changeunit.atomunits == {}
    assert ex1_changeunit._world_build_validated is False


def test_ChangeUnit_set_atomunit_CorrectlySets_WorldUnitSimpleAttrs():
    # GIVEN
    ex1_changeunit = changeunit_shop()
    attribute_value = 55
    category = "worldunit"
    opt1_arg = "_weight"
    optional_args = {opt1_arg: attribute_value}
    required_args = {}
    world_weight_atomunit = atomunit_shop(
        category,
        atom_update(),
        required_args=required_args,
        optional_args=optional_args,
    )
    assert ex1_changeunit.atomunits == {}
    assert world_weight_atomunit.atom_order is None

    # WHEN
    ex1_changeunit.set_atomunit(world_weight_atomunit)

    # THEN
    assert len(ex1_changeunit.atomunits) == 1
    x_update_dict = ex1_changeunit.atomunits.get(atom_update())
    # print(f"{x_update_dict=}")
    x_category_atomunit = x_update_dict.get(category)
    print(f"{x_category_atomunit=}")
    assert x_category_atomunit == world_weight_atomunit
    assert world_weight_atomunit.atom_order != None


def test_ChangeUnit_set_atomunit_RaisesErrorWhen_is_valid_IsFalse():
    # GIVEN
    ex1_changeunit = changeunit_shop()
    x_category = "world_charunit"
    world_weight_atomunit = atomunit_shop(x_category, atom_update())

    # WHEN
    with pytest_raises(Exception) as excinfo:
        ex1_changeunit.set_atomunit(world_weight_atomunit)
    assert (
        str(excinfo.value)
        == f"""'{x_category}' UPDATE AtomUnit is invalid
                x_atomunit.is_required_args_valid()=False
                x_atomunit.is_optional_args_valid()=True"""
    )


def test_ChangeUnit_get_atom_ReturnsCorrectObj():
    # GIVEN
    ex1_changeunit = changeunit_shop()
    worldunit_text = "worldunit"
    opt_arg1 = "_weight"
    opt_value = 55
    worldunit_atomunit = atomunit_shop(worldunit_text, atom_update())
    worldunit_atomunit.set_optional_arg(x_key=opt_arg1, x_value=opt_value)
    ex1_changeunit.set_atomunit(worldunit_atomunit)

    # WHEN
    gen_atomunit = ex1_changeunit.get_atomunit(
        atom_update(), category=worldunit_text, required_args=[]
    )

    # THEN
    assert gen_atomunit == worldunit_atomunit


def test_ChangeUnit_add_atomunit_CorrectlySets_WorldUnitSimpleAttrs():
    # GIVEN
    ex1_changeunit = changeunit_shop()
    assert ex1_changeunit.atomunits == {}

    # WHEN
    op2_arg = "_weight"
    op2_value = 55
    worldunit_text = "worldunit"
    required_args = {}
    optional_args = {op2_arg: op2_value}
    ex1_changeunit.add_atomunit(
        worldunit_text,
        atom_update(),
        required_args,
        optional_args=optional_args,
    )

    # THEN
    assert len(ex1_changeunit.atomunits) == 1
    x_update_dict = ex1_changeunit.atomunits.get(atom_update())
    x_atomunit = x_update_dict.get(worldunit_text)
    assert x_atomunit != None
    assert x_atomunit.category == worldunit_text


def test_ChangeUnit_add_atomunit_CorrectlySets_WorldUnit_charunits():
    # GIVEN
    ex1_changeunit = changeunit_shop()
    assert ex1_changeunit.atomunits == {}

    # WHEN
    char_id_text = "char_id"
    bob_text = "Bob"
    bob_credor_weight = 55
    bob_debtor_weight = 66
    bob_charunit = charunit_shop(bob_text, bob_credor_weight, bob_debtor_weight)
    char_id_text = "char_id"
    cw_text = "credor_weight"
    dw_text = "debtor_weight"
    print(f"{bob_charunit.get_dict()=}")
    bob_required_dict = {char_id_text: bob_charunit.get_dict().get(char_id_text)}
    bob_optional_dict = {cw_text: bob_charunit.get_dict().get(cw_text)}
    bob_optional_dict[dw_text] = bob_charunit.get_dict().get(dw_text)
    print(f"{bob_required_dict=}")
    charunit_text = "world_charunit"
    ex1_changeunit.add_atomunit(
        category=charunit_text,
        crud_text=atom_insert(),
        required_args=bob_required_dict,
        optional_args=bob_optional_dict,
    )
    # THEN
    assert len(ex1_changeunit.atomunits) == 1
    assert (
        ex1_changeunit.atomunits.get(atom_insert()).get(charunit_text).get(bob_text)
        != None
    )


def test_ChangeUnit_get_crud_atomunits_list_ReturnsCorrectObj():
    # GIVEN
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
    # GIVEN
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
    assert sue_atoms_list[0] == update_dict.get("worldunit")
    z_atom = sue_atoms_list[1]
    print(f"{z_atom=}")
    print(delete_dict.get("world_charunit").keys())
    carmen_charunit_delete = delete_dict.get("world_charunit").get("Carmen")
    assert sue_atoms_list[1] == carmen_charunit_delete
    # print(f"{sue_atom_order_dict.keys()=}")
    # # print(f"{sue_atom_order_dict.get(atom_update())=}")
    # assert len(sue_atom_order_dict.get(atom_update())) == 1
    # assert len(sue_atom_order_dict.get(atom_delete())) == 1
    # for crud_text, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_text=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.category=}")


# def test_ChangeUnit_add_atomunit_CorrectlySets_WorldUnit_max_tree_traverse():
#     # GIVEN
#     ex1_changeunit = changeunit_shop(get_sue_road())
#     assert ex1_changeunit.atomunits == {}

#     # WHEN
#     opt2_value = 55
#     category = "worldunit"
#     opt2_arg = "_weight"
#     weight_atomunit = atomunit_shop(category, atom_update())
#     weight_atomunit.set_optional_arg(opt2_arg, opt2_value)
#     ex1_changeunit.set_atomunit(weight_atomunit)
#     # THEN
#     assert len(ex1_changeunit.atomunits.get(atom_update()).keys()) == 1
#     sue_worldunit_dict = ex1_changeunit.atomunits.get(atom_update())
#     sue_weight_atomunit = sue_worldunit_dict.get(category)
#     print(f"{sue_weight_atomunit=}")
#     assert weight_atomunit == sue_weight_atomunit

#     # WHEN
#     new2_value = 66
#     x_attribute = "_max_tree_traverse"
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
#     x_attribute = "_char_credor_pool"
#     required_args = {x_attribute: new3_value}
#     x_atomunit = atomunit_shop(x_attribute, atom_update(), None, required_args)
#     ex1_changeunit.set_atomunit(x_atomunit)
#     # THEN
#     assert len(ex1_changeunit.atomunits.get(atom_update()).keys()) == 3
#     assert x_atomunit == ex1_changeunit.atomunits.get(atom_update()).get(x_attribute)

#     # WHEN
#     new4_value = 88
#     x_attribute = "_char_debtor_pool"
#     required_args = {x_attribute: new4_value}
#     x_atomunit = atomunit_shop(x_attribute, atom_update(), None, required_args)
#     ex1_changeunit.set_atomunit(x_atomunit)
#     # THEN
#     assert len(ex1_changeunit.atomunits.get(atom_update()).keys()) == 4
#     assert x_atomunit == ex1_changeunit.atomunits.get(atom_update()).get(x_attribute)

#     # WHEN
#     new5_value = "override"
#     x_attribute = "_meld_strategy"
#     required_args = {x_attribute: new5_value}
#     x_atomunit = atomunit_shop(x_attribute, atom_update(), None, required_args)
#     ex1_changeunit.set_atomunit(x_atomunit)
#     # THEN
#     assert len(ex1_changeunit.atomunits.get(atom_update()).keys()) == 5
#     assert x_atomunit == ex1_changeunit.atomunits.get(atom_update()).get(x_attribute)


def test_ChangeUnit_get_sorted_atomunits_ReturnsCorrectObj():
    # GIVEN
    ex1_changeunit = get_changeunit_example1()
    worldunit_text = "worldunit"
    world_charunit_text = "world_charunit"
    update_dict = ex1_changeunit.atomunits.get(atom_update())
    assert len(update_dict.keys()) == 1
    assert update_dict.get(worldunit_text) != None
    print(f"atom_order 28 {ex1_changeunit.atomunits.get(atom_update()).keys()=}")
    delete_dict = ex1_changeunit.atomunits.get(atom_delete())
    assert len(delete_dict.keys()) == 1
    assert delete_dict.get(world_charunit_text) != None
    print(f"atom_order 26 {ex1_changeunit.atomunits.get(atom_delete()).keys()=}")

    # WHEN
    sue_atom_order_list = ex1_changeunit.get_sorted_atomunits()

    # THEN
    assert len(sue_atom_order_list) == 2
    print(delete_dict.get("world_charunit").keys())
    carmen_charunit_delete = delete_dict.get("world_charunit").get("Carmen")
    # for atomunit in sue_atom_order_list:
    #     print(f"{atomunit.atom_order=}")
    assert sue_atom_order_list[0] == carmen_charunit_delete
    assert sue_atom_order_list[1] == update_dict.get(worldunit_text)
    # for crud_text, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_text=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.category=}")


def test_ChangeUnit_get_sorted_atomunits_ReturnsCorrectObj_IdeaUnitsSorted():
    # GIVEN
    x_real_id = root_label()
    sports_text = "sports"
    sports_road = create_road(x_real_id, sports_text)
    knee_text = "knee"
    x_category = "world_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    sports_insert_ideaunit_atomunit = atomunit_shop(x_category, atom_insert())
    sports_insert_ideaunit_atomunit.set_required_arg(label_text, sports_text)
    sports_insert_ideaunit_atomunit.set_required_arg(parent_road_text, x_real_id)
    knee_insert_ideaunit_atomunit = atomunit_shop(x_category, atom_insert())
    knee_insert_ideaunit_atomunit.set_required_arg(label_text, knee_text)
    knee_insert_ideaunit_atomunit.set_required_arg(parent_road_text, sports_road)
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
    # GIVEN
    x_real_id = root_label()
    sports_text = "sports"
    sports_road = create_road(x_real_id, sports_text)
    knee_text = "knee"
    knee_road = create_road(sports_road, knee_text)
    x_category = "world_idea_awardlink"
    road_text = "road"
    belief_id_text = "belief_id"
    swimmers_text = ",Swimmers"
    sports_awardlink_atomunit = atomunit_shop(x_category, atom_insert())
    sports_awardlink_atomunit.set_required_arg(belief_id_text, swimmers_text)
    sports_awardlink_atomunit.set_required_arg(road_text, sports_road)
    knee_awardlink_atomunit = atomunit_shop(x_category, atom_insert())
    knee_awardlink_atomunit.set_required_arg(belief_id_text, swimmers_text)
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


def test_world_built_from_change_is_valid_ReturnsCorrectObjGivenNoWorld():
    # GIVEN
    sue_changeunit = changeunit_shop()

    worldunit_text = "worldunit"
    x_atomunit = atomunit_shop(worldunit_text, atom_update())
    x_attribute = "_char_credor_pool"
    x_atomunit.set_optional_arg(x_attribute, 100)
    sue_changeunit.set_atomunit(x_atomunit)

    category = "world_charunit"
    carm_text = "Carmen"
    x_atomunit = atomunit_shop(category, atom_insert())
    x_atomunit.set_arg("char_id", carm_text)
    x_atomunit.set_arg("credor_weight", 70)
    sue_changeunit.set_atomunit(x_atomunit)

    # WHEN/THEN
    assert world_built_from_change_is_valid(sue_changeunit) is False

    # WHEN
    rico_text = "Rico"
    x_atomunit = atomunit_shop(category, atom_insert())
    x_atomunit.set_arg("char_id", rico_text)
    x_atomunit.set_arg("credor_weight", 30)
    sue_changeunit.set_atomunit(x_atomunit)

    # THEN
    assert world_built_from_change_is_valid(sue_changeunit)

    # WHEN
    bob_text = "Bob"
    x_atomunit = atomunit_shop(category, atom_insert())
    x_atomunit.set_arg("char_id", bob_text)
    x_atomunit.set_arg("credor_weight", 35)
    sue_changeunit.set_atomunit(x_atomunit)

    # THEN
    assert world_built_from_change_is_valid(sue_changeunit) is False


def test_world_built_from_change_is_valid_ReturnsCorrectObjGivenWorld():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    sue_world.set_char_credor_pool(100)

    sue_changeunit = changeunit_shop()

    category = "world_charunit"
    carm_text = "Carmen"
    x_atomunit = atomunit_shop(category, atom_insert())
    x_atomunit.set_arg("char_id", carm_text)
    x_atomunit.set_arg("credor_weight", 70)
    sue_changeunit.set_atomunit(x_atomunit)

    # WHEN/THEN
    sue_world = worldunit_shop("Sue")
    sue_world.set_char_credor_pool(100)
    assert world_built_from_change_is_valid(sue_changeunit, sue_world) is False

    # WHEN
    rico_text = "Rico"
    x_atomunit = atomunit_shop(category, atom_insert())
    x_atomunit.set_arg("char_id", rico_text)
    x_atomunit.set_arg("credor_weight", 30)
    sue_changeunit.set_atomunit(x_atomunit)

    # THEN
    sue_world = worldunit_shop("Sue")
    sue_world.set_char_credor_pool(100)
    assert world_built_from_change_is_valid(sue_changeunit, sue_world)

    # WHEN
    bob_text = "Bob"
    x_atomunit = atomunit_shop(category, atom_insert())
    x_atomunit.set_arg("char_id", bob_text)
    x_atomunit.set_arg("credor_weight", 35)
    sue_changeunit.set_atomunit(x_atomunit)

    # THEN
    sue_world = worldunit_shop("Sue")
    sue_world.set_char_credor_pool(100)
    assert world_built_from_change_is_valid(sue_changeunit, sue_world) is False


def test_ChangeUnit_get_ordered_atomunits_ReturnsCorrectObj_GivenNoStartingNumber():
    # GIVEN
    sue_changeunit = changeunit_shop()
    worldunit_text = "worldunit"
    pool_atomunit = atomunit_shop(worldunit_text, atom_update())
    pool_attribute = "_char_credor_pool"
    pool_atomunit.set_optional_arg(pool_attribute, 100)
    sue_changeunit.set_atomunit(pool_atomunit)
    category = "world_charunit"
    carm_text = "Carmen"
    carm_atomunit = atomunit_shop(category, atom_insert())
    carm_atomunit.set_arg("char_id", carm_text)
    carm_atomunit.set_arg("credor_weight", 70)
    sue_changeunit.set_atomunit(carm_atomunit)
    sue_world = worldunit_shop("Sue")
    sue_world.set_char_credor_pool(100)
    rico_text = "Rico"
    rico_atomunit = atomunit_shop(category, atom_insert())
    rico_atomunit.set_arg("char_id", rico_text)
    rico_atomunit.set_arg("credor_weight", 30)
    sue_changeunit.set_atomunit(rico_atomunit)

    sue_world = worldunit_shop("Sue")
    assert world_built_from_change_is_valid(sue_changeunit, sue_world)

    # WHEN
    changeunit_dict = sue_changeunit.get_ordered_atomunits()

    # THEN
    # change_carm = changeunit_dict.get(0)
    # change_rico = changeunit_dict.get(1)
    # change_pool = changeunit_dict.get(2)
    # assert change_carm == carm_atomunit
    # assert change_rico == rico_atomunit
    # assert change_pool == pool_atomunit
    assert changeunit_dict.get(0) == carm_atomunit
    assert changeunit_dict.get(1) == rico_atomunit
    assert changeunit_dict.get(2) == pool_atomunit


def test_ChangeUnit_get_ordered_atomunits_ReturnsCorrectObj_GivenStartingNumber():
    # GIVEN
    sue_changeunit = changeunit_shop()
    worldunit_text = "worldunit"
    pool_atomunit = atomunit_shop(worldunit_text, atom_update())
    pool_attribute = "_char_credor_pool"
    pool_atomunit.set_optional_arg(pool_attribute, 100)
    sue_changeunit.set_atomunit(pool_atomunit)
    category = "world_charunit"
    carm_text = "Carmen"
    carm_atomunit = atomunit_shop(category, atom_insert())
    carm_atomunit.set_arg("char_id", carm_text)
    carm_atomunit.set_arg("credor_weight", 70)
    sue_changeunit.set_atomunit(carm_atomunit)
    sue_world = worldunit_shop("Sue")
    sue_world.set_char_credor_pool(100)
    rico_text = "Rico"
    rico_atomunit = atomunit_shop(category, atom_insert())
    rico_atomunit.set_arg("char_id", rico_text)
    rico_atomunit.set_arg("credor_weight", 30)
    sue_changeunit.set_atomunit(rico_atomunit)

    sue_world = worldunit_shop("Sue")
    assert world_built_from_change_is_valid(sue_changeunit, sue_world)

    # WHEN
    changeunit_dict = sue_changeunit.get_ordered_atomunits(5)

    # THEN
    # change_carm = changeunit_dict.get(0)
    # change_rico = changeunit_dict.get(1)
    # change_pool = changeunit_dict.get(2)
    # assert change_carm == carm_atomunit
    # assert change_rico == rico_atomunit
    # assert change_pool == pool_atomunit
    assert changeunit_dict.get(5) == carm_atomunit
    assert changeunit_dict.get(6) == rico_atomunit
    assert changeunit_dict.get(7) == pool_atomunit


def test_ChangeUnit_get_ordered_dict_ReturnsCorrectObj_GivenStartingNumber():
    # GIVEN
    sue_changeunit = changeunit_shop()
    worldunit_text = "worldunit"
    pool_atomunit = atomunit_shop(worldunit_text, atom_update())
    pool_attribute = "_char_credor_pool"
    pool_atomunit.set_optional_arg(pool_attribute, 100)
    sue_changeunit.set_atomunit(pool_atomunit)
    category = "world_charunit"
    carm_text = "Carmen"
    carm_atomunit = atomunit_shop(category, atom_insert())
    carm_atomunit.set_arg("char_id", carm_text)
    carm_atomunit.set_arg("credor_weight", 70)
    sue_changeunit.set_atomunit(carm_atomunit)
    sue_world = worldunit_shop("Sue")
    sue_world.set_char_credor_pool(100)
    rico_text = "Rico"
    rico_atomunit = atomunit_shop(category, atom_insert())
    rico_atomunit.set_arg("char_id", rico_text)
    rico_atomunit.set_arg("credor_weight", 30)
    sue_changeunit.set_atomunit(rico_atomunit)

    sue_world = worldunit_shop("Sue")
    assert world_built_from_change_is_valid(sue_changeunit, sue_world)

    # WHEN
    changeunit_dict = sue_changeunit.get_ordered_dict(5)

    # THEN
    # change_carm = changeunit_dict.get(0)
    # change_rico = changeunit_dict.get(1)
    # change_pool = changeunit_dict.get(2)
    # assert change_carm == carm_atomunit
    # assert change_rico == rico_atomunit
    # assert change_pool == pool_atomunit
    assert changeunit_dict.get(5) == carm_atomunit.get_dict()
    assert changeunit_dict.get(6) == rico_atomunit.get_dict()
    assert changeunit_dict.get(7) == pool_atomunit.get_dict()


def test_ChangeUnit_get_json_ReturnsCorrectObj():
    # GIVEN
    sue_changeunit = changeunit_shop()
    worldunit_text = "worldunit"
    pool_atomunit = atomunit_shop(worldunit_text, atom_update())
    pool_attribute = "_char_credor_pool"
    pool_atomunit.set_optional_arg(pool_attribute, 100)
    sue_changeunit.set_atomunit(pool_atomunit)
    category = "world_charunit"
    carm_text = "Carmen"
    carm_atomunit = atomunit_shop(category, atom_insert())
    carm_atomunit.set_arg("char_id", carm_text)
    carm_atomunit.set_arg("credor_weight", 70)
    sue_changeunit.set_atomunit(carm_atomunit)
    rico_text = "Rico"
    rico_atomunit = atomunit_shop(category, atom_insert())
    rico_atomunit.set_arg("char_id", rico_text)
    rico_atomunit.set_arg("credor_weight", 30)
    sue_changeunit.set_atomunit(rico_atomunit)

    # WHEN
    change_start_int = 5
    changeunit_json = sue_changeunit.get_json(change_start_int)

    # THEN
    assert x_is_json(changeunit_json)


def test_ChangeUnit_atomunit_exists_ReturnsCorrectObj():
    # GIVEN
    farm_changeunit = changeunit_shop()

    # WHEN / THEN
    category = "world_charunit"
    carm_text = "Carmen"
    carm_atomunit = atomunit_shop(category, atom_insert())
    carm_atomunit.set_arg("char_id", carm_text)
    carm_atomunit.set_arg("credor_weight", 70)
    assert farm_changeunit.atomunit_exists(carm_atomunit) is False

    # WHEN
    farm_changeunit.set_atomunit(carm_atomunit)

    # THEN
    assert farm_changeunit.atomunit_exists(carm_atomunit)
