from src.s2_bud.healer import HealerLink, healerlink_shop, healerlink_get_from_dict


def test_HealerLink_exists():
    # ESTABLISH
    run_str = ";runners"
    run_healer_ids = {run_str}

    # WHEN
    x_healerlink = HealerLink(_healer_ids=run_healer_ids)

    # THEN
    assert x_healerlink
    assert x_healerlink._healer_ids == run_healer_ids


def test_healerlink_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # ESTABLISH
    run_str = ";runners"
    run_healer_ids = {run_str}

    # WHEN
    x_healerlink = healerlink_shop(_healer_ids=run_healer_ids)

    # THEN
    assert x_healerlink
    assert x_healerlink._healer_ids == run_healer_ids


def test_healerlink_shop_ifEmptyReturnsCorrectWithCorrectAttributes():
    # ESTABLISH / WHEN
    x_healerlink = healerlink_shop()

    # THEN
    assert x_healerlink
    assert x_healerlink._healer_ids == set()


def test_HealerLink_get_dict_ReturnsCorrectDictWithSingleGroup_id():
    # ESTABLISH
    bob_healer_id = "Bob"
    run_healer_ids = {bob_healer_id}
    x_healerlink = healerlink_shop(_healer_ids=run_healer_ids)

    # WHEN
    obj_dict = x_healerlink.get_dict()

    # THEN
    assert obj_dict is not None
    run_list = [bob_healer_id]
    example_dict = {"healerlink_healer_ids": run_list}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_HealerLink_set_healer_id_CorrectlySets_healer_ids_v1():
    # ESTABLISH
    x_healerlink = healerlink_shop()
    assert len(x_healerlink._healer_ids) == 0

    # WHEN
    yao_str = "Yao"
    x_healerlink.set_healer_id(x_healer_id=yao_str)

    # THEN
    assert len(x_healerlink._healer_ids) == 1


def test_HealerLink_del_healer_id_CorrectlyDeletes_healer_ids_v1():
    # ESTABLISH
    x_healerlink = healerlink_shop()
    yao_str = "Yao"
    sue_str = "Sue"
    x_healerlink.set_healer_id(x_healer_id=yao_str)
    x_healerlink.set_healer_id(x_healer_id=sue_str)
    assert len(x_healerlink._healer_ids) == 2

    # WHEN
    x_healerlink.del_healer_id(x_healer_id=sue_str)

    # THEN
    assert len(x_healerlink._healer_ids) == 1


def test_HealerLink_healer_id_exists_ReturnsCorrectObj():
    # ESTABLISH
    x_healerlink = healerlink_shop()
    yao_str = "Yao"
    sue_str = "Sue"
    assert x_healerlink.healer_id_exists(yao_str) is False
    assert x_healerlink.healer_id_exists(sue_str) is False

    # WHEN
    x_healerlink.set_healer_id(x_healer_id=yao_str)

    # THEN
    assert x_healerlink.healer_id_exists(yao_str)
    assert x_healerlink.healer_id_exists(sue_str) is False


def test_HealerLink_any_healer_id_exists_ReturnsCorrectObj():
    # ESTABLISH
    x_healerlink = healerlink_shop()
    assert x_healerlink.any_healer_id_exists() is False

    # WHEN / THEN
    sue_str = "Sue"
    x_healerlink.set_healer_id(x_healer_id=sue_str)
    assert x_healerlink.any_healer_id_exists()

    # WHEN / THEN
    yao_str = "Yao"
    x_healerlink.set_healer_id(x_healer_id=yao_str)
    assert x_healerlink.any_healer_id_exists()

    # WHEN / THEN
    x_healerlink.del_healer_id(x_healer_id=yao_str)
    assert x_healerlink.any_healer_id_exists()

    # WHEN / THEN
    x_healerlink.del_healer_id(x_healer_id=sue_str)
    assert x_healerlink.any_healer_id_exists() is False


def test_healerlink_get_from_dict_ReturnsCorrectObj():
    # ESTABLISH
    empty_dict = {}

    # WHEN / THEN
    assert healerlink_get_from_dict(empty_dict) == healerlink_shop()

    # WHEN / THEN
    sue_str = "Sue"
    yao_str = "Yao"
    static_healerlink = healerlink_shop()
    static_healerlink.set_healer_id(x_healer_id=sue_str)
    static_healerlink.set_healer_id(x_healer_id=yao_str)

    sue_dict = {"healerlink_healer_ids": [sue_str, yao_str]}
    assert healerlink_get_from_dict(sue_dict) == static_healerlink
