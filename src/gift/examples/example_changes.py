from src.gift.atom_config import (
    atom_delete,
    atom_update,
    bud_acctunit_text,
    acct_id_str,
)
from src.gift.atom import atomunit_shop
from src.gift.change import ChangeUnit, changeunit_shop


def get_changeunit_sue_example() -> ChangeUnit:
    sue_changeunit = changeunit_shop()

    budunit_text = "budunit"
    pool_atomunit = atomunit_shop(budunit_text, atom_update())
    pool_attribute = "credor_respect"
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
    tally_name = "tally"
    x_atomunit = atomunit_shop(budunit_text, atom_update())
    x_atomunit.set_optional_arg(tally_name, 55)
    x_attribute = "max_tree_traverse"
    x_atomunit.set_optional_arg(x_attribute, 66)
    x_attribute = "credor_respect"
    x_atomunit.set_optional_arg(x_attribute, 77)
    x_attribute = "debtor_respect"
    x_atomunit.set_optional_arg(x_attribute, 88)
    sue_changeunit.set_atomunit(x_atomunit)

    category = bud_acctunit_text()
    zia_text = "Zia"
    x_atomunit = atomunit_shop(category, atom_delete())
    x_atomunit.set_required_arg(acct_id_str(), zia_text)
    sue_changeunit.set_atomunit(x_atomunit)
    return sue_changeunit
