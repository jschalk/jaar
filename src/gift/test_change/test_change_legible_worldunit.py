from src.gift.atom import atomunit_shop, atom_update
from src.gift.change import changeunit_shop
from src.gift.legible import create_legible_list
from src._world.world import worldunit_shop


def test_create_legible_list_ReturnsObjGivenEmptyChange():
    # GIVEN / WHEN
    x_changeunit = changeunit_shop()
    sue_world = worldunit_shop("Sue")

    # THEN
    assert create_legible_list(x_changeunit, sue_world) == []


def test_create_legible_list_ReturnsObjGivenWorldUpdate_weight():
    # GIVEN
    category = "worldunit"
    weight_text = "_weight"
    weight_int = 55
    weight_atomunit = atomunit_shop(category, atom_update())
    weight_atomunit.set_arg(weight_text, weight_int)
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(weight_atomunit)
    sue_world = worldunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"{sue_world._owner_id}'s world weight was transited to {weight_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenWorldUpdate_monetary_desc():
    # GIVEN
    category = "worldunit"
    _monetary_desc_text = "_monetary_desc"
    sue_monetary_desc = "dragon funds"
    _monetary_desc_atomunit = atomunit_shop(category, atom_update())
    _monetary_desc_atomunit.set_arg(_monetary_desc_text, sue_monetary_desc)
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(_monetary_desc_atomunit)
    sue_world = worldunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"{sue_world._owner_id}'s monetary_desc is now called '{sue_monetary_desc}'"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenWorldUpdate_char_credor_pool():
    # GIVEN
    category = "worldunit"
    char_credor_pool_text = "_char_credor_pool"
    char_credor_pool_int = 71
    char_credor_pool_atomunit = atomunit_shop(category, atom_update())
    char_credor_pool_atomunit.set_arg(char_credor_pool_text, char_credor_pool_int)

    print(f"{char_credor_pool_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(char_credor_pool_atomunit)
    sue_world = worldunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_world.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"{sue_monetary_desc} credor pool is now {char_credor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenWorldUpdate_char_credor_pool_With_monetary_desc_None():
    # GIVEN
    category = "worldunit"
    char_credor_pool_text = "_char_credor_pool"
    char_credor_pool_int = 71
    char_credor_pool_atomunit = atomunit_shop(category, atom_update())
    char_credor_pool_atomunit.set_arg(char_credor_pool_text, char_credor_pool_int)

    print(f"{char_credor_pool_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(char_credor_pool_atomunit)
    sue_world = worldunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"{sue_world._owner_id}'s monetary_desc credor pool is now {char_credor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenWorldUpdate_char_debtor_pool():
    # GIVEN
    category = "worldunit"
    char_debtor_pool_text = "_char_debtor_pool"
    char_debtor_pool_int = 78
    char_debtor_pool_atomunit = atomunit_shop(category, atom_update())
    char_debtor_pool_atomunit.set_arg(char_debtor_pool_text, char_debtor_pool_int)

    print(f"{char_debtor_pool_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(char_debtor_pool_atomunit)
    sue_world = worldunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_world.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"{sue_monetary_desc} debtor pool is now {char_debtor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenWorldUpdate_char_credor_pool_Equal_char_debtor_pool():
    # GIVEN
    x_changeunit = changeunit_shop()
    category = "worldunit"
    char_credor_pool_text = "_char_credor_pool"
    char_debtor_pool_text = "_char_debtor_pool"
    char_pool_int = 83
    worldunit_atomunit = atomunit_shop(category, atom_update())
    worldunit_atomunit.set_arg(char_credor_pool_text, char_pool_int)
    worldunit_atomunit.set_arg(char_debtor_pool_text, char_pool_int)
    x_changeunit.set_atomunit(worldunit_atomunit)
    sue_world = worldunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_world.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"{sue_monetary_desc} total pool is now {char_pool_int}"
    assert len(legible_list) == 1
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenWorldUpdate_max_tree_traverse():
    # GIVEN
    category = "worldunit"
    max_tree_traverse_text = "_max_tree_traverse"
    max_tree_traverse_int = 71
    max_tree_traverse_atomunit = atomunit_shop(category, atom_update())
    max_tree_traverse_atomunit.set_arg(max_tree_traverse_text, max_tree_traverse_int)

    print(f"{max_tree_traverse_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(max_tree_traverse_atomunit)
    sue_world = worldunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"{sue_world._owner_id}'s maximum number of World output evaluations transited to {max_tree_traverse_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenWorldUpdate_meld_strategy():
    # GIVEN
    category = "worldunit"
    meld_strategy_text = "_meld_strategy"
    meld_strategy_value = "override"
    meld_strategy_atomunit = atomunit_shop(category, atom_update())
    meld_strategy_atomunit.set_arg(meld_strategy_text, meld_strategy_value)

    print(f"{meld_strategy_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(meld_strategy_atomunit)
    sue_world = worldunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = (
        f"{sue_world._owner_id}'s Meld strategy transited to '{meld_strategy_value}'"
    )
    assert legible_list[0] == x_str
