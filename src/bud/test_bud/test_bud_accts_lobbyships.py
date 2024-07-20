from src.bud.bud import budunit_shop


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
