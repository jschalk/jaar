from src.bud.lobby import lobbybox_shop
from src.bud.bud import budunit_shop
from copy import deepcopy as copy_deepcopy


def test_BudUnit_get_charunit_lobby_ids_dict_ReturnsObj():
    # ESTABLISH
    yao_text = "Yao"
    sue_text = "Sue"
    zia_text = "Zia"
    bob_bud = budunit_shop("Bob")
    bob_bud.add_acctunit(yao_text)
    bob_bud.add_acctunit(sue_text)
    bob_bud.add_acctunit(zia_text)
    sue_acctunit = bob_bud.get_acct(sue_text)
    zia_acctunit = bob_bud.get_acct(zia_text)
    run_text = ",Run"
    swim_text = ",Swim"
    sue_acctunit.add_lobbyship(run_text)
    zia_acctunit.add_lobbyship(run_text)
    zia_acctunit.add_lobbyship(swim_text)

    # WHEN
    lobby_ids_dict = bob_bud.get_charunit_lobby_ids_dict()

    # THEN
    print(f"{lobby_ids_dict=}")
    all_lobby_ids = {yao_text, sue_text, zia_text, run_text, swim_text}
    assert set(lobby_ids_dict.keys()) == all_lobby_ids
    assert set(lobby_ids_dict.keys()) != {swim_text, run_text}
    assert lobby_ids_dict.get(swim_text) == {zia_text}
    assert lobby_ids_dict.get(run_text) == {zia_text, sue_text}
    assert lobby_ids_dict.get(yao_text) == {yao_text}
    assert lobby_ids_dict.get(sue_text) == {sue_text}
    assert lobby_ids_dict.get(zia_text) == {zia_text}


def test_BudUnit_set_lobbybox_SetsAttr():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    run_text = ",Run"
    assert not bob_bud._lobbyboxs.get(run_text)

    # WHEN
    bob_bud.set_lobbybox(lobbybox_shop(run_text))

    # THEN
    assert bob_bud._lobbyboxs.get(run_text)


def test_BudUnit_lobbybox_exists_ReturnsObj():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    run_text = ",Run"
    assert not bob_bud.lobbybox_exists(run_text)

    # WHEN
    bob_bud.set_lobbybox(lobbybox_shop(run_text))

    # THEN
    assert bob_bud.lobbybox_exists(run_text)


def test_BudUnit_get_lobbybox_ReturnsObj():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    run_text = ",Run"
    x_run_lobbybox = lobbybox_shop(run_text)
    bob_bud.set_lobbybox(x_run_lobbybox)
    assert bob_bud._lobbyboxs.get(run_text)

    # WHEN / THEN
    assert bob_bud.get_lobbybox(run_text) == lobbybox_shop(run_text)


def test_BudUnit_create_symmetry_lobbybox_ReturnsObj():
    # ESTABLISH
    yao_text = "Yao"
    yao_bud = budunit_shop(yao_text)
    zia_text = "Zia"
    yao_credor_weight = 3
    yao_debtor_weight = 2
    zia_credor_weight = 4
    zia_debtor_weight = 5
    yao_bud.add_acctunit(yao_text, yao_credor_weight, yao_debtor_weight)
    yao_bud.add_acctunit(zia_text, zia_credor_weight, zia_debtor_weight)

    # WHEN
    xio_text = "Xio"
    xio_lobbybox = yao_bud.create_symmetry_lobbybox(xio_text)

    # THEN
    assert xio_lobbybox.lobby_id == xio_text
    assert xio_lobbybox.lobbyship_exists(yao_text)
    assert xio_lobbybox.lobbyship_exists(zia_text)
    assert len(xio_lobbybox._lobbyships) == 2
    yao_lobbybox = xio_lobbybox.get_lobbyship(yao_text)
    zia_lobbybox = xio_lobbybox.get_lobbyship(zia_text)
    assert yao_lobbybox.credor_weight == yao_credor_weight
    assert zia_lobbybox.credor_weight == zia_credor_weight
    assert yao_lobbybox.debtor_weight == yao_debtor_weight
    assert zia_lobbybox.debtor_weight == zia_debtor_weight
