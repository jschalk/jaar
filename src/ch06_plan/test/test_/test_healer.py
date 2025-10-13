from src.ch06_plan.healer import HealerUnit, get_healerunit_from_dict, healerunit_shop


def test_HealerUnit_Exists():
    # ESTABLISH
    run_str = ";runners"
    run_healer_names = {run_str}

    # WHEN
    x_healerunit = HealerUnit(_healer_names=run_healer_names)

    # THEN
    assert x_healerunit
    assert x_healerunit._healer_names == run_healer_names


def test_healerunit_shop_ReturnsWithCorrectAttributes_v1():
    # ESTABLISH
    run_str = ";runners"
    run_healer_names = {run_str}

    # WHEN
    x_healerunit = healerunit_shop(_healer_names=run_healer_names)

    # THEN
    assert x_healerunit
    assert x_healerunit._healer_names == run_healer_names


def test_healerunit_shop_ifEmptyReturnsWithCorrectAttributes():
    # ESTABLISH / WHEN
    x_healerunit = healerunit_shop()

    # THEN
    assert x_healerunit
    assert x_healerunit._healer_names == set()


def test_HealerUnit_to_dict_ReturnsDictWithSingle_group_title():
    # ESTABLISH
    bob_healer_name = "Bob"
    run_healer_names = {bob_healer_name}
    x_healerunit = healerunit_shop(_healer_names=run_healer_names)

    # WHEN
    obj_dict = x_healerunit.to_dict()

    # THEN
    assert obj_dict is not None
    run_list = [bob_healer_name]
    example_dict = {"healerunit_healer_names": run_list}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_HealerUnit_set_healer_name_Sets_healer_names_v1():
    # ESTABLISH
    x_healerunit = healerunit_shop()
    assert len(x_healerunit._healer_names) == 0

    # WHEN
    yao_str = "Yao"
    x_healerunit.set_healer_name(x_healer_name=yao_str)

    # THEN
    assert len(x_healerunit._healer_names) == 1


def test_HealerUnit_del_healer_name_Deletes_healer_names_v1():
    # ESTABLISH
    x_healerunit = healerunit_shop()
    yao_str = "Yao"
    sue_str = "Sue"
    x_healerunit.set_healer_name(x_healer_name=yao_str)
    x_healerunit.set_healer_name(x_healer_name=sue_str)
    assert len(x_healerunit._healer_names) == 2

    # WHEN
    x_healerunit.del_healer_name(x_healer_name=sue_str)

    # THEN
    assert len(x_healerunit._healer_names) == 1


def test_HealerUnit_healer_name_exists_ReturnsObj():
    # ESTABLISH
    x_healerunit = healerunit_shop()
    yao_str = "Yao"
    sue_str = "Sue"
    assert x_healerunit.healer_name_exists(yao_str) is False
    assert x_healerunit.healer_name_exists(sue_str) is False

    # WHEN
    x_healerunit.set_healer_name(x_healer_name=yao_str)

    # THEN
    assert x_healerunit.healer_name_exists(yao_str)
    assert x_healerunit.healer_name_exists(sue_str) is False


def test_HealerUnit_any_healer_name_exists_ReturnsObj():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    x_healerunit = healerunit_shop()
    assert x_healerunit.any_healer_name_exists() is False

    # WHEN / THEN
    sue_str = "Sue"
    x_healerunit.set_healer_name(x_healer_name=sue_str)
    assert x_healerunit.any_healer_name_exists()

    # WHEN / THEN
    yao_str = "Yao"
    x_healerunit.set_healer_name(x_healer_name=yao_str)
    assert x_healerunit.any_healer_name_exists()

    # WHEN / THEN
    x_healerunit.del_healer_name(x_healer_name=yao_str)
    assert x_healerunit.any_healer_name_exists()

    # WHEN / THEN
    x_healerunit.del_healer_name(x_healer_name=sue_str)
    assert x_healerunit.any_healer_name_exists() is False


def test_get_healerunit_from_dict_ReturnsObj():
    # ESTABLISH
    empty_dict = {}

    # WHEN / THEN
    assert get_healerunit_from_dict(empty_dict) == healerunit_shop()

    # WHEN / THEN
    sue_str = "Sue"
    yao_str = "Yao"
    static_healerunit = healerunit_shop()
    static_healerunit.set_healer_name(x_healer_name=sue_str)
    static_healerunit.set_healer_name(x_healer_name=yao_str)

    sue_dict = {"healerunit_healer_names": [sue_str, yao_str]}
    assert get_healerunit_from_dict(sue_dict) == static_healerunit
