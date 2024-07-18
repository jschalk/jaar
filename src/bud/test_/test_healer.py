from src._road.road import LobbyID
from src.bud.healer import HealerHold, healerhold_shop, healerhold_get_from_dict


def test_HealerHold_exists():
    # ESTABLISH
    run_text = ",runners"
    run_lobby_ids = {run_text}

    # WHEN
    x_healerhold = HealerHold(_lobby_ids=run_lobby_ids)

    # THEN
    assert x_healerhold
    assert x_healerhold._lobby_ids == run_lobby_ids


def test_healerhold_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # ESTABLISH
    run_text = ",runners"
    run_lobby_ids = {run_text}

    # WHEN
    x_healerhold = healerhold_shop(_lobby_ids=run_lobby_ids)

    # THEN
    assert x_healerhold
    assert x_healerhold._lobby_ids == run_lobby_ids


def test_healerhold_shop_ifEmptyReturnsCorrectWithCorrectAttributes():
    # ESTABLISH / WHEN
    x_healerhold = healerhold_shop()

    # THEN
    assert x_healerhold
    assert x_healerhold._lobby_ids == set()


def test_HealerHold_get_dict_ReturnsCorrectDictWithSingleLobby_id():
    # ESTABLISH
    bob_lobby_id = "Bob"
    run_lobby_ids = {bob_lobby_id}
    x_healerhold = healerhold_shop(_lobby_ids=run_lobby_ids)

    # WHEN
    obj_dict = x_healerhold.get_dict()

    # THEN
    assert obj_dict != None
    run_list = [bob_lobby_id]
    example_dict = {"healerhold_lobby_ids": run_list}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_HealerHold_set_lobby_id_CorrectlySets_lobby_ids_v1():
    # ESTABLISH
    x_healerhold = healerhold_shop()
    assert len(x_healerhold._lobby_ids) == 0

    # WHEN
    yao_text = "Yao"
    x_healerhold.set_lobby_id(x_lobby_id=yao_text)

    # THEN
    assert len(x_healerhold._lobby_ids) == 1


def test_HealerHold_del_lobby_id_CorrectlyDeletes_lobby_ids_v1():
    # ESTABLISH
    x_healerhold = healerhold_shop()
    yao_text = "Yao"
    sue_text = "Sue"
    x_healerhold.set_lobby_id(x_lobby_id=yao_text)
    x_healerhold.set_lobby_id(x_lobby_id=sue_text)
    assert len(x_healerhold._lobby_ids) == 2

    # WHEN
    x_healerhold.del_lobby_id(x_lobby_id=sue_text)

    # THEN
    assert len(x_healerhold._lobby_ids) == 1


def test_HealerHold_lobby_id_exists_ReturnsCorrectObj():
    # ESTABLISH
    x_healerhold = healerhold_shop()
    yao_text = "Yao"
    sue_text = "Sue"
    assert x_healerhold.lobby_id_exists(yao_text) is False
    assert x_healerhold.lobby_id_exists(sue_text) is False

    # WHEN
    x_healerhold.set_lobby_id(x_lobby_id=yao_text)

    # THEN
    assert x_healerhold.lobby_id_exists(yao_text)
    assert x_healerhold.lobby_id_exists(sue_text) is False


def test_HealerHold_any_lobby_id_exists_ReturnsCorrectObj():
    # ESTABLISH
    x_healerhold = healerhold_shop()
    assert x_healerhold.any_lobby_id_exists() is False

    # WHEN / THEN
    sue_text = "Sue"
    x_healerhold.set_lobby_id(x_lobby_id=sue_text)
    assert x_healerhold.any_lobby_id_exists()

    # WHEN / THEN
    yao_text = "Yao"
    x_healerhold.set_lobby_id(x_lobby_id=yao_text)
    assert x_healerhold.any_lobby_id_exists()

    # WHEN / THEN
    x_healerhold.del_lobby_id(x_lobby_id=yao_text)
    assert x_healerhold.any_lobby_id_exists()

    # WHEN / THEN
    x_healerhold.del_lobby_id(x_lobby_id=sue_text)
    assert x_healerhold.any_lobby_id_exists() is False


def test_healerhold_get_from_dict_ReturnsCorrectObj():
    # ESTABLISH
    empty_dict = {}

    # WHEN / THEN
    assert healerhold_get_from_dict(empty_dict) == healerhold_shop()

    # WHEN / THEN
    sue_text = "Sue"
    yao_text = "Yao"
    static_healerhold = healerhold_shop()
    static_healerhold.set_lobby_id(x_lobby_id=sue_text)
    static_healerhold.set_lobby_id(x_lobby_id=yao_text)

    sue_dict = {"healerhold_lobby_ids": [sue_text, yao_text]}
    assert healerhold_get_from_dict(sue_dict) == static_healerhold
