from src.f02_bud.bud_tool import budunit_str, bud_acctunit_str
from src.f04_gift.atom_config import atom_delete, atom_update, acct_id_str
from src.f04_gift.atom import atomunit_shop
from src.f04_gift.delta import DeltaUnit, deltaunit_shop


def get_deltaunit_sue_example() -> DeltaUnit:
    sue_deltaunit = deltaunit_shop()

    pool_atomunit = atomunit_shop(budunit_str(), atom_update())
    pool_attribute = "credor_respect"
    pool_atomunit.set_optional_arg(pool_attribute, 77)
    sue_deltaunit.set_atomunit(pool_atomunit)

    category = bud_acctunit_str()
    sue_str = "Sue"
    sue_atomunit = atomunit_shop(category, atom_delete())
    sue_atomunit.set_required_arg(acct_id_str(), sue_str)
    sue_deltaunit.set_atomunit(sue_atomunit)
    return sue_deltaunit


def get_deltaunit_example1() -> DeltaUnit:
    sue_deltaunit = deltaunit_shop()

    tally_name = "tally"
    x_atomunit = atomunit_shop(budunit_str(), atom_update())
    x_atomunit.set_optional_arg(tally_name, 55)
    x_attribute = "max_tree_traverse"
    x_atomunit.set_optional_arg(x_attribute, 66)
    x_attribute = "credor_respect"
    x_atomunit.set_optional_arg(x_attribute, 77)
    x_attribute = "debtor_respect"
    x_atomunit.set_optional_arg(x_attribute, 88)
    x_attribute = "purview_timestamp"
    x_atomunit.set_optional_arg(x_attribute, 990000)
    sue_deltaunit.set_atomunit(x_atomunit)

    category = bud_acctunit_str()
    zia_str = "Zia"
    x_atomunit = atomunit_shop(category, atom_delete())
    x_atomunit.set_required_arg(acct_id_str(), zia_str)
    sue_deltaunit.set_atomunit(x_atomunit)
    return sue_deltaunit
