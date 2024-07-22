from src.bud.lobby import lobbybox_shop
from src.bud.bud import budunit_shop


def test_BudUnit_get_acctunit_lobby_ids_dict_ReturnsObj():
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
    lobby_ids_dict = bob_bud.get_acctunit_lobby_ids_dict()

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


def test_BudUnit_set_lobbybox_SetsAttr_Scenario0():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    run_text = ",Run"
    assert not bob_bud._lobbyboxs.get(run_text)

    # WHEN
    bob_bud.set_lobbybox(lobbybox_shop(run_text))

    # THEN
    assert bob_bud._lobbyboxs.get(run_text)


def test_BudUnit_set_lobbybox_Sets_road_fund_coin():
    # ESTABLISH
    x_fund_coin = 5
    bob_bud = budunit_shop("Bob", _fund_coin=x_fund_coin)
    run_text = ",Run"
    assert not bob_bud._lobbyboxs.get(run_text)

    # WHEN
    bob_bud.set_lobbybox(lobbybox_shop(run_text))

    # THEN
    assert bob_bud._lobbyboxs.get(run_text)._fund_coin == x_fund_coin


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
    yao_credit_score = 3
    yao_debtit_score = 2
    zia_credit_score = 4
    zia_debtit_score = 5
    yao_bud.add_acctunit(yao_text, yao_credit_score, yao_debtit_score)
    yao_bud.add_acctunit(zia_text, zia_credit_score, zia_debtit_score)

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
    assert yao_lobbybox.credit_score == yao_credit_score
    assert zia_lobbybox.credit_score == zia_credit_score
    assert yao_lobbybox.debtit_score == yao_debtit_score
    assert zia_lobbybox.debtit_score == zia_debtit_score
