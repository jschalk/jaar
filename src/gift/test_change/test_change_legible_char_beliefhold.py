from src.gift.atom import atomunit_shop, atom_update, atom_insert, atom_delete
from src.gift.change import changeunit_shop
from src.gift.legible import create_legible_list
from src._world.world import worldunit_shop


def test_create_legible_list_ReturnsObj_char_beliefhold_INSERT():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_char_beliefhold"
    belief_id_text = "belief_id"
    char_id_text = "char_id"
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    swim_text = f"{sue_world._road_delimiter}Swimmers"
    rico_text = "Rico"
    credor_weight_value = 81
    debtor_weight_value = 43
    rico_atomunit = atomunit_shop(category, atom_insert())
    rico_atomunit.set_arg(belief_id_text, swim_text)
    rico_atomunit.set_arg(char_id_text, rico_text)
    rico_atomunit.set_arg(credor_weight_text, credor_weight_value)
    rico_atomunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{rico_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(rico_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"Belief '{swim_text}' has new member {rico_text} with belief_cred={credor_weight_value} and belief_debt={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_char_beliefhold_UPDATE_credor_weight_debtor_weight():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_char_beliefhold"
    belief_id_text = "belief_id"
    char_id_text = "char_id"
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    swim_text = f"{sue_world._road_delimiter}Swimmers"
    rico_text = "Rico"
    credor_weight_value = 81
    debtor_weight_value = 43
    rico_atomunit = atomunit_shop(category, atom_update())
    rico_atomunit.set_arg(belief_id_text, swim_text)
    rico_atomunit.set_arg(char_id_text, rico_text)
    rico_atomunit.set_arg(credor_weight_text, credor_weight_value)
    rico_atomunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{rico_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(rico_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"Belief '{swim_text}' member {rico_text} has new belief_cred={credor_weight_value} and belief_debt={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_char_beliefhold_UPDATE_credor_weight():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_char_beliefhold"
    belief_id_text = "belief_id"
    char_id_text = "char_id"
    credor_weight_text = "credor_weight"
    swim_text = f"{sue_world._road_delimiter}Swimmers"
    rico_text = "Rico"
    credor_weight_value = 81
    rico_atomunit = atomunit_shop(category, atom_update())
    rico_atomunit.set_arg(belief_id_text, swim_text)
    rico_atomunit.set_arg(char_id_text, rico_text)
    rico_atomunit.set_arg(credor_weight_text, credor_weight_value)
    # print(f"{rico_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(rico_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"Belief '{swim_text}' member {rico_text} has new belief_cred={credor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_char_beliefhold_UPDATE_debtor_weight():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_char_beliefhold"
    belief_id_text = "belief_id"
    char_id_text = "char_id"
    debtor_weight_text = "debtor_weight"
    swim_text = f"{sue_world._road_delimiter}Swimmers"
    rico_text = "Rico"
    debtor_weight_value = 43
    rico_atomunit = atomunit_shop(category, atom_update())
    rico_atomunit.set_arg(belief_id_text, swim_text)
    rico_atomunit.set_arg(char_id_text, rico_text)
    rico_atomunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{rico_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(rico_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"Belief '{swim_text}' member {rico_text} has new belief_debt={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_char_beliefhold_DELETE():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_char_beliefhold"
    belief_id_text = "belief_id"
    char_id_text = "char_id"
    swim_text = f"{sue_world._road_delimiter}Swimmers"
    rico_text = "Rico"
    rico_atomunit = atomunit_shop(category, atom_delete())
    rico_atomunit.set_arg(belief_id_text, swim_text)
    rico_atomunit.set_arg(char_id_text, rico_text)
    # print(f"{rico_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(rico_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"Belief '{swim_text}' no longer has member {rico_text}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
