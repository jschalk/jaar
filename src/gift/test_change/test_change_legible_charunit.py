from src.gift.atom import atomunit_shop, atom_update, atom_insert, atom_delete
from src.gift.change import changeunit_shop, create_legible_list
from src._world.world import worldunit_shop


def test_create_legible_list_ReturnsObj_charunit_INSERT():
    # GIVEN
    category = "world_charunit"
    char_id_text = "char_id"
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    credor_weight_value = 81
    debtor_weight_value = 43
    rico_text = "Rico"
    rico_atomunit = atomunit_shop(category, atom_insert())
    rico_atomunit.set_arg(char_id_text, rico_text)
    rico_atomunit.set_arg(credor_weight_text, credor_weight_value)
    rico_atomunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{rico_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(rico_atomunit)
    sue_world = worldunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_world.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"{rico_text} was added with {credor_weight_value} {sue_world._monetary_desc} cred and {debtor_weight_value} {sue_world._monetary_desc} debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_charunit_INSERT_monetary_desc_IsNone():
    # GIVEN
    category = "world_charunit"
    char_id_text = "char_id"
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    credor_weight_value = 81
    debtor_weight_value = 43
    rico_text = "Rico"
    rico_atomunit = atomunit_shop(category, atom_insert())
    rico_atomunit.set_arg(char_id_text, rico_text)
    rico_atomunit.set_arg(credor_weight_text, credor_weight_value)
    rico_atomunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{rico_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(rico_atomunit)
    sue_world = worldunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"{rico_text} was added with {credor_weight_value} monetary_desc cred and {debtor_weight_value} monetary_desc debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_charunit_UPDATE_credor_weight_debtor_weight():
    # GIVEN
    category = "world_charunit"
    char_id_text = "char_id"
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    credor_weight_value = 81
    debtor_weight_value = 43
    rico_text = "Rico"
    rico_atomunit = atomunit_shop(category, atom_update())
    rico_atomunit.set_arg(char_id_text, rico_text)
    rico_atomunit.set_arg(credor_weight_text, credor_weight_value)
    rico_atomunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{rico_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(rico_atomunit)
    sue_world = worldunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_world.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"{rico_text} now has {credor_weight_value} {sue_world._monetary_desc} cred and {debtor_weight_value} {sue_world._monetary_desc} debt."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_charunit_UPDATE_credor_weight():
    # GIVEN
    category = "world_charunit"
    char_id_text = "char_id"
    credor_weight_text = "credor_weight"
    credor_weight_value = 81
    rico_text = "Rico"
    rico_atomunit = atomunit_shop(category, atom_update())
    rico_atomunit.set_arg(char_id_text, rico_text)
    rico_atomunit.set_arg(credor_weight_text, credor_weight_value)
    # print(f"{rico_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(rico_atomunit)
    sue_world = worldunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_world.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = (
        f"{rico_text} now has {credor_weight_value} {sue_world._monetary_desc} cred."
    )
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_charunit_UPDATE_debtor_weight():
    # GIVEN
    category = "world_charunit"
    char_id_text = "char_id"
    debtor_weight_text = "debtor_weight"
    debtor_weight_value = 43
    rico_text = "Rico"
    rico_atomunit = atomunit_shop(category, atom_update())
    rico_atomunit.set_arg(char_id_text, rico_text)
    rico_atomunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{rico_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(rico_atomunit)
    sue_world = worldunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_world.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = (
        f"{rico_text} now has {debtor_weight_value} {sue_world._monetary_desc} debt."
    )
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_charunit_DELETE():
    # GIVEN
    category = "world_charunit"
    char_id_text = "char_id"
    rico_text = "Rico"
    rico_atomunit = atomunit_shop(category, atom_delete())
    rico_atomunit.set_arg(char_id_text, rico_text)
    # print(f"{rico_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(rico_atomunit)
    sue_world = worldunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_world.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"{rico_text} was removed from {sue_world._monetary_desc} chars."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
