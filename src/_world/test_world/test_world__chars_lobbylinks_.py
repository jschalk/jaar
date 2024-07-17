from src._world.world import worldunit_shop


def test_WorldUnit_get_lobby_ids_dict_ReturnsObj():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    zia_text = "Zia"
    bob_world = worldunit_shop("Bob")
    bob_world.add_charunit(yao_text)
    bob_world.add_charunit(sue_text)
    bob_world.add_charunit(zia_text)
    sue_charunit = bob_world.get_char(sue_text)
    zia_charunit = bob_world.get_char(zia_text)
    run_text = ",Run"
    swim_text = ",Swim"
    sue_charunit.add_lobbylink(run_text)
    zia_charunit.add_lobbylink(run_text)
    zia_charunit.add_lobbylink(swim_text)

    # WHEN
    lobby_ids_dict = bob_world.get_lobby_ids_dict()

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
