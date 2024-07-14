from src.gift.atom import atom_delete, atom_update, atomunit_shop
from src.gift.change import ChangeUnit, changeunit_shop


def get_changeunit_sue_example() -> ChangeUnit:
    sue_changeunit = changeunit_shop()

    worldunit_text = "worldunit"
    pool_atomunit = atomunit_shop(worldunit_text, atom_update())
    pool_attribute = "_char_credor_pool"
    pool_atomunit.set_optional_arg(pool_attribute, 77)
    sue_changeunit.set_atomunit(pool_atomunit)

    category = "world_charunit"
    sue_text = "Sue"
    sue_atomunit = atomunit_shop(category, atom_delete())
    sue_atomunit.set_required_arg("char_id", sue_text)
    sue_changeunit.set_atomunit(sue_atomunit)
    return sue_changeunit


def get_changeunit_example1() -> ChangeUnit:
    sue_changeunit = changeunit_shop()

    worldunit_text = "worldunit"
    weight_name = "_weight"
    x_atomunit = atomunit_shop(worldunit_text, atom_update())
    x_atomunit.set_optional_arg(weight_name, 55)
    x_attribute = "_max_tree_traverse"
    x_atomunit.set_optional_arg(x_attribute, 66)
    x_attribute = "_char_credor_pool"
    x_atomunit.set_optional_arg(x_attribute, 77)
    x_attribute = "_char_debtor_pool"
    x_atomunit.set_optional_arg(x_attribute, 88)
    x_attribute = "_meld_strategy"
    x_atomunit.set_optional_arg(x_attribute, "override")
    sue_changeunit.set_atomunit(x_atomunit)

    category = "world_charunit"
    zia_text = "Zia"
    x_atomunit = atomunit_shop(category, atom_delete())
    x_atomunit.set_required_arg("char_id", zia_text)
    sue_changeunit.set_atomunit(x_atomunit)
    return sue_changeunit
