from src._road.jaar_config import get_real_id_if_None
from src._road.road import RealID
from src.gift.atom_config import (
    acct_id_str,
    parent_road_str,
    bud_acctunit_text,
    bud_ideaunit_text,
    label_str,
)
from src.gift.atom import (
    AtomUnit,
    atom_delete,
    atom_update,
    atom_insert,
    atomunit_shop,
)
from src.gift.change import ChangeUnit, changeunit_shop


def get_atom_example_ideaunit_sports(real_id: RealID = None) -> AtomUnit:
    real_id = get_real_id_if_None(real_id)
    sports_text = "sports"
    x_category = bud_ideaunit_text()
    insert_ideaunit_atomunit = atomunit_shop(x_category, atom_insert())
    insert_ideaunit_atomunit.set_required_arg(label_str(), sports_text)
    insert_ideaunit_atomunit.set_required_arg(parent_road_str(), real_id)
    return insert_ideaunit_atomunit


def get_changeunit_sue_example() -> ChangeUnit:
    sue_changeunit = changeunit_shop()

    budunit_text = "budunit"
    pool_atomunit = atomunit_shop(budunit_text, atom_update())
    pool_attribute = "_credor_respect"
    pool_atomunit.set_optional_arg(pool_attribute, 77)
    sue_changeunit.set_atomunit(pool_atomunit)

    category = bud_acctunit_text()
    sue_text = "Sue"
    sue_atomunit = atomunit_shop(category, atom_delete())
    sue_atomunit.set_required_arg(acct_id_str(), sue_text)
    sue_changeunit.set_atomunit(sue_atomunit)
    return sue_changeunit


def get_changeunit_example1() -> ChangeUnit:
    sue_changeunit = changeunit_shop()

    budunit_text = "budunit"
    mass_name = "_mass"
    x_atomunit = atomunit_shop(budunit_text, atom_update())
    x_atomunit.set_optional_arg(mass_name, 55)
    x_attribute = "_max_tree_traverse"
    x_atomunit.set_optional_arg(x_attribute, 66)
    x_attribute = "_credor_respect"
    x_atomunit.set_optional_arg(x_attribute, 77)
    x_attribute = "_debtor_respect"
    x_atomunit.set_optional_arg(x_attribute, 88)
    sue_changeunit.set_atomunit(x_atomunit)

    category = bud_acctunit_text()
    sue_text = "Sue"
    x_atomunit = atomunit_shop(category, atom_delete())
    x_atomunit.set_required_arg(acct_id_str(), sue_text)
    sue_changeunit.set_atomunit(x_atomunit)
    return sue_changeunit


def get_changeunit_example2() -> ChangeUnit:
    sue_changeunit = changeunit_shop()

    budunit_text = "budunit"
    x_atomunit = atomunit_shop(budunit_text, atom_update())
    x_attribute = "_credor_respect"
    x_atomunit.set_optional_arg(x_attribute, 77)

    category = bud_acctunit_text()
    sue_text = "Sue"
    x_atomunit = atomunit_shop(category, atom_delete())
    x_atomunit.set_required_arg(acct_id_str(), sue_text)
    sue_changeunit.set_atomunit(x_atomunit)
    return sue_changeunit
