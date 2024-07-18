from src.gift.atom import atomunit_shop, atom_update, atom_insert, atom_delete
from src.gift.change import changeunit_shop
from src.gift.legible import create_legible_list
from src.bud.bud import budunit_shop


def test_create_legible_list_ReturnsObj_char_lobbyship_INSERT():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = "bud_char_lobbyship"
    lobby_id_text = "lobby_id"
    char_id_text = "char_id"
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    swim_text = f"{sue_bud._road_delimiter}Swimmers"
    yao_text = "Yao"
    credor_weight_value = 81
    debtor_weight_value = 43
    yao_atomunit = atomunit_shop(category, atom_insert())
    yao_atomunit.set_arg(lobby_id_text, swim_text)
    yao_atomunit.set_arg(char_id_text, yao_text)
    yao_atomunit.set_arg(credor_weight_text, credor_weight_value)
    yao_atomunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Lobby '{swim_text}' has new member {yao_text} with lobby_cred={credor_weight_value} and lobby_debt={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_char_lobbyship_UPDATE_credor_weight_debtor_weight():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = "bud_char_lobbyship"
    lobby_id_text = "lobby_id"
    char_id_text = "char_id"
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    swim_text = f"{sue_bud._road_delimiter}Swimmers"
    yao_text = "Yao"
    credor_weight_value = 81
    debtor_weight_value = 43
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(lobby_id_text, swim_text)
    yao_atomunit.set_arg(char_id_text, yao_text)
    yao_atomunit.set_arg(credor_weight_text, credor_weight_value)
    yao_atomunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Lobby '{swim_text}' member {yao_text} has new lobby_cred={credor_weight_value} and lobby_debt={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_char_lobbyship_UPDATE_credor_weight():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = "bud_char_lobbyship"
    lobby_id_text = "lobby_id"
    char_id_text = "char_id"
    credor_weight_text = "credor_weight"
    swim_text = f"{sue_bud._road_delimiter}Swimmers"
    yao_text = "Yao"
    credor_weight_value = 81
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(lobby_id_text, swim_text)
    yao_atomunit.set_arg(char_id_text, yao_text)
    yao_atomunit.set_arg(credor_weight_text, credor_weight_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Lobby '{swim_text}' member {yao_text} has new lobby_cred={credor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_char_lobbyship_UPDATE_debtor_weight():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = "bud_char_lobbyship"
    lobby_id_text = "lobby_id"
    char_id_text = "char_id"
    debtor_weight_text = "debtor_weight"
    swim_text = f"{sue_bud._road_delimiter}Swimmers"
    yao_text = "Yao"
    debtor_weight_value = 43
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(lobby_id_text, swim_text)
    yao_atomunit.set_arg(char_id_text, yao_text)
    yao_atomunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Lobby '{swim_text}' member {yao_text} has new lobby_debt={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_char_lobbyship_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = "bud_char_lobbyship"
    lobby_id_text = "lobby_id"
    char_id_text = "char_id"
    swim_text = f"{sue_bud._road_delimiter}Swimmers"
    yao_text = "Yao"
    yao_atomunit = atomunit_shop(category, atom_delete())
    yao_atomunit.set_arg(lobby_id_text, swim_text)
    yao_atomunit.set_arg(char_id_text, yao_text)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Lobby '{swim_text}' no longer has member {yao_text}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
