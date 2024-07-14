from src.gift.atom import atomunit_shop, atom_update, atom_insert, atom_delete
from src.gift.change import changeunit_shop
from src.gift.legible import create_legible_list
from src._world.world import worldunit_shop


def test_create_legible_list_ReturnsObj_char_belieflink_INSERT():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_char_belieflink"
    belief_id_text = "belief_id"
    char_id_text = "char_id"
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    swim_text = f"{sue_world._road_delimiter}Swimmers"
    yao_text = "Yao"
    credor_weight_value = 81
    debtor_weight_value = 43
    yao_atomunit = atomunit_shop(category, atom_insert())
    yao_atomunit.set_arg(belief_id_text, swim_text)
    yao_atomunit.set_arg(char_id_text, yao_text)
    yao_atomunit.set_arg(credor_weight_text, credor_weight_value)
    yao_atomunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"Belief '{swim_text}' has new member {yao_text} with belief_cred={credor_weight_value} and belief_debt={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_char_belieflink_UPDATE_credor_weight_debtor_weight():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_char_belieflink"
    belief_id_text = "belief_id"
    char_id_text = "char_id"
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    swim_text = f"{sue_world._road_delimiter}Swimmers"
    yao_text = "Yao"
    credor_weight_value = 81
    debtor_weight_value = 43
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(belief_id_text, swim_text)
    yao_atomunit.set_arg(char_id_text, yao_text)
    yao_atomunit.set_arg(credor_weight_text, credor_weight_value)
    yao_atomunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"Belief '{swim_text}' member {yao_text} has new belief_cred={credor_weight_value} and belief_debt={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_char_belieflink_UPDATE_credor_weight():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_char_belieflink"
    belief_id_text = "belief_id"
    char_id_text = "char_id"
    credor_weight_text = "credor_weight"
    swim_text = f"{sue_world._road_delimiter}Swimmers"
    yao_text = "Yao"
    credor_weight_value = 81
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(belief_id_text, swim_text)
    yao_atomunit.set_arg(char_id_text, yao_text)
    yao_atomunit.set_arg(credor_weight_text, credor_weight_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"Belief '{swim_text}' member {yao_text} has new belief_cred={credor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_char_belieflink_UPDATE_debtor_weight():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_char_belieflink"
    belief_id_text = "belief_id"
    char_id_text = "char_id"
    debtor_weight_text = "debtor_weight"
    swim_text = f"{sue_world._road_delimiter}Swimmers"
    yao_text = "Yao"
    debtor_weight_value = 43
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(belief_id_text, swim_text)
    yao_atomunit.set_arg(char_id_text, yao_text)
    yao_atomunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"Belief '{swim_text}' member {yao_text} has new belief_debt={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_char_belieflink_DELETE():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_char_belieflink"
    belief_id_text = "belief_id"
    char_id_text = "char_id"
    swim_text = f"{sue_world._road_delimiter}Swimmers"
    yao_text = "Yao"
    yao_atomunit = atomunit_shop(category, atom_delete())
    yao_atomunit.set_arg(belief_id_text, swim_text)
    yao_atomunit.set_arg(char_id_text, yao_text)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"Belief '{swim_text}' no longer has member {yao_text}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
