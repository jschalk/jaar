from src._road.jaar_config import get_test_real_id
from src._road.road import RealID
from src.gift.atom import (
    AtomUnit,
    atom_delete,
    atom_update,
    atom_insert,
    atomunit_shop,
)
from src.gift.change import ChangeUnit, changeunit_shop


def get_atom_example_ideaunit_sports(real_id: RealID = None) -> AtomUnit:
    if real_id is None:
        real_id = get_test_real_id()
    sports_text = "sports"
    x_category = "world_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    insert_ideaunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_ideaunit_atomunit.set_required_arg(label_text, sports_text)
    insert_ideaunit_atomunit.set_required_arg(parent_road_text, real_id)
    return insert_ideaunit_atomunit


def get_changeunit_carm_example() -> ChangeUnit:
    sue_changeunit = changeunit_shop()

    worldunit_text = "worldunit"
    pool_atomunit = atomunit_shop(worldunit_text, atom_update())
    pool_attribute = "_person_credor_pool"
    pool_atomunit.set_optional_arg(pool_attribute, 77)
    sue_changeunit.set_atomunit(pool_atomunit)

    category = "world_personunit"
    carm_text = "Carmen"
    carm_atomunit = atomunit_shop(category, atom_delete())
    carm_atomunit.set_required_arg("person_id", carm_text)
    sue_changeunit.set_atomunit(carm_atomunit)
    return sue_changeunit


def get_changeunit_example1() -> ChangeUnit:
    sue_changeunit = changeunit_shop()

    worldunit_text = "worldunit"
    weight_name = "_weight"
    x_atomunit = atomunit_shop(worldunit_text, atom_update())
    x_atomunit.set_optional_arg(weight_name, 55)
    x_attribute = "_max_tree_traverse"
    x_atomunit.set_optional_arg(x_attribute, 66)
    x_attribute = "_person_credor_pool"
    x_atomunit.set_optional_arg(x_attribute, 77)
    x_attribute = "_person_debtor_pool"
    x_atomunit.set_optional_arg(x_attribute, 88)
    x_attribute = "_meld_strategy"
    x_atomunit.set_optional_arg(x_attribute, "override")
    sue_changeunit.set_atomunit(x_atomunit)

    category = "world_personunit"
    carm_text = "Carmen"
    x_atomunit = atomunit_shop(category, atom_delete())
    x_atomunit.set_required_arg("person_id", carm_text)
    sue_changeunit.set_atomunit(x_atomunit)
    return sue_changeunit


def get_changeunit_example2() -> ChangeUnit:
    sue_changeunit = changeunit_shop()

    worldunit_text = "worldunit"
    x_atomunit = atomunit_shop(worldunit_text, atom_update())
    x_attribute = "_person_credor_pool"
    x_atomunit.set_optional_arg(x_attribute, 77)

    category = "world_personunit"
    carm_text = "Carmen"
    x_atomunit = atomunit_shop(category, atom_delete())
    x_atomunit.set_required_arg("person_id", carm_text)
    sue_changeunit.set_atomunit(x_atomunit)
    return sue_changeunit
