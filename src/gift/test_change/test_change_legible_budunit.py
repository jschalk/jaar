from src.gift.atom import atomunit_shop, atom_update
from src.gift.change import changeunit_shop
from src.gift.legible import create_legible_list
from src.bud.bud import budunit_shop


def test_create_legible_list_ReturnsObjEstablishWithEmptyChange():
    # ESTABLISH / WHEN
    x_changeunit = changeunit_shop()
    sue_bud = budunit_shop("Sue")

    # THEN
    assert create_legible_list(x_changeunit, sue_bud) == []


def test_create_legible_list_ReturnsObjEstablishWithBudUpdate_weight():
    # ESTABLISH
    category = "budunit"
    weight_text = "_weight"
    weight_int = 55
    weight_atomunit = atomunit_shop(category, atom_update())
    weight_atomunit.set_arg(weight_text, weight_int)
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(weight_atomunit)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"{sue_bud._owner_id}'s bud weight was transited to {weight_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBudUpdate_monetary_desc():
    # ESTABLISH
    category = "budunit"
    _monetary_desc_text = "_monetary_desc"
    sue_monetary_desc = "dragon dollars"
    _monetary_desc_atomunit = atomunit_shop(category, atom_update())
    _monetary_desc_atomunit.set_arg(_monetary_desc_text, sue_monetary_desc)
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(_monetary_desc_atomunit)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"{sue_bud._owner_id}'s monetary_desc is now called '{sue_monetary_desc}'"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBudUpdate_credor_respect():
    # ESTABLISH
    category = "budunit"
    char_credor_pool_text = "_credor_respect"
    char_credor_pool_int = 71
    char_credor_pool_atomunit = atomunit_shop(category, atom_update())
    char_credor_pool_atomunit.set_arg(char_credor_pool_text, char_credor_pool_int)

    print(f"{char_credor_pool_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(char_credor_pool_atomunit)
    sue_bud = budunit_shop("Sue")
    sue_monetary_desc = "dragon dollars"
    sue_bud.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"{sue_monetary_desc} credor pool is now {char_credor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBudUpdate_credor_respect_With_monetary_desc_None():
    # ESTABLISH
    category = "budunit"
    char_credor_pool_text = "_credor_respect"
    char_credor_pool_int = 71
    char_credor_pool_atomunit = atomunit_shop(category, atom_update())
    char_credor_pool_atomunit.set_arg(char_credor_pool_text, char_credor_pool_int)

    print(f"{char_credor_pool_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(char_credor_pool_atomunit)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = (
        f"{sue_bud._owner_id}'s monetary_desc credor pool is now {char_credor_pool_int}"
    )
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBudUpdate_debtor_respect():
    # ESTABLISH
    category = "budunit"
    char_debtor_pool_text = "_debtor_respect"
    char_debtor_pool_int = 78
    char_debtor_pool_atomunit = atomunit_shop(category, atom_update())
    char_debtor_pool_atomunit.set_arg(char_debtor_pool_text, char_debtor_pool_int)

    print(f"{char_debtor_pool_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(char_debtor_pool_atomunit)
    sue_bud = budunit_shop("Sue")
    sue_monetary_desc = "dragon dollars"
    sue_bud.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"{sue_monetary_desc} debtor pool is now {char_debtor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBudUpdate_credor_respect_Equal_debtor_respect():
    # ESTABLISH
    x_changeunit = changeunit_shop()
    category = "budunit"
    char_credor_pool_text = "_credor_respect"
    char_debtor_pool_text = "_debtor_respect"
    char_pool_int = 83
    budunit_atomunit = atomunit_shop(category, atom_update())
    budunit_atomunit.set_arg(char_credor_pool_text, char_pool_int)
    budunit_atomunit.set_arg(char_debtor_pool_text, char_pool_int)
    x_changeunit.set_atomunit(budunit_atomunit)
    sue_bud = budunit_shop("Sue")
    sue_monetary_desc = "dragon dollars"
    sue_bud.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"{sue_monetary_desc} total pool is now {char_pool_int}"
    assert len(legible_list) == 1
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjEstablishWithBudUpdate_max_tree_traverse():
    # ESTABLISH
    category = "budunit"
    max_tree_traverse_text = "_max_tree_traverse"
    max_tree_traverse_int = 71
    max_tree_traverse_atomunit = atomunit_shop(category, atom_update())
    max_tree_traverse_atomunit.set_arg(max_tree_traverse_text, max_tree_traverse_int)

    print(f"{max_tree_traverse_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(max_tree_traverse_atomunit)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"{sue_bud._owner_id}'s maximum number of Bud output evaluations transited to {max_tree_traverse_int}"
    assert legible_list[0] == x_str
