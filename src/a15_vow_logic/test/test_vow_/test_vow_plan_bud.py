from pytest import raises as pytest_raises
from src.a02_finance_logic.bud import brokerunit_shop
from src.a15_vow_logic._util.a15_env import get_module_temp_dir
from src.a15_vow_logic.vow import vowunit_shop


def test_VowUnit_set_brokerunit_SetsAttr():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    assert accord_vow.brokerunits == {}

    # WHEN
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    accord_vow.set_brokerunit(sue_brokerunit)

    # THEN
    assert accord_vow.brokerunits != {}
    assert accord_vow.brokerunits.get(sue_str) == sue_brokerunit


def test_VowUnit_brokerunit_exists_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    sue_str = "Sue"
    assert accord_vow.brokerunit_exists(sue_str) is False

    # WHEN
    sue_brokerunit = brokerunit_shop(sue_str)
    accord_vow.set_brokerunit(sue_brokerunit)

    # THEN
    assert accord_vow.brokerunit_exists(sue_str)


def test_VowUnit_get_brokerunit_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    accord_vow.set_brokerunit(sue_brokerunit)
    assert accord_vow.brokerunit_exists(sue_str)

    # WHEN
    sue_gen_brokerunit = accord_vow.get_brokerunit(sue_str)

    # THEN
    assert sue_brokerunit
    assert sue_brokerunit == sue_gen_brokerunit


def test_VowUnit_del_brokerunit_SetsAttr():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    accord_vow.set_brokerunit(sue_brokerunit)
    assert accord_vow.brokerunit_exists(sue_str)

    # WHEN
    accord_vow.del_brokerunit(sue_str)

    # THEN
    assert accord_vow.brokerunit_exists(sue_str) is False


def test_VowUnit_add_budunit_SetsAttr():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    assert accord_vow.brokerunits == {}

    # WHEN
    bob_str = "Bob"
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    accord_vow.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    accord_vow.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    accord_vow.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)

    # THEN
    assert accord_vow.brokerunits != {}
    sue_brokerunit = brokerunit_shop(sue_str)
    sue_brokerunit.add_bud(sue_x4_bud_time, sue_x4_quota)
    sue_brokerunit.add_bud(sue_x7_bud_time, sue_x7_quota)
    bob_brokerunit = brokerunit_shop(bob_str)
    bob_brokerunit.add_bud(bob_x0_bud_time, bob_x0_quota)
    assert accord_vow.get_brokerunit(sue_str) == sue_brokerunit
    assert accord_vow.get_brokerunit(bob_str) == bob_brokerunit


def test_VowUnit_get_budunit_ReturnsObj_Scenario0_BrokerDoesNotExist():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    sue_str = "Sue"
    sue_x7_bud_time = 7

    # WHEN
    gen_sue_x7_budunit = accord_vow.get_budunit(sue_str, sue_x7_bud_time)

    # THEN
    assert accord_vow.brokerunits == {}
    assert not gen_sue_x7_budunit


def test_VowUnit_get_budunit_ReturnsObj_Scenario1_BudDoesNotExist():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 66
    accord_vow.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)

    # WHEN
    sue_x7_bud_time = 7
    gen_sue_x7_budunit = accord_vow.get_budunit(sue_str, sue_x7_bud_time)

    # THEN
    assert accord_vow.brokerunits != {}
    assert not gen_sue_x7_budunit


def test_VowUnit_get_budunit_ReturnsObj_Scenario2_BudExists():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    bob_str = "Bob"
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    accord_vow.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    accord_vow.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    accord_vow.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)

    # WHEN
    gen_sue_x7_budunit = accord_vow.get_budunit(sue_str, sue_x7_bud_time)

    # THEN
    assert accord_vow.brokerunits != {}
    sue_broker = accord_vow.brokerunits.get(sue_str)
    assert gen_sue_x7_budunit == sue_broker.get_bud(sue_x7_bud_time)


def test_VowUnit_get_brokerunits_bud_times_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    bob_str = "Bob"
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    assert accord_vow.get_brokerunits_bud_times() == set()

    # WHEN
    accord_vow.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    accord_vow.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    accord_vow.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)

    # THEN
    all_bud_times = {bob_x0_bud_time, sue_x4_bud_time, sue_x7_bud_time}
    assert accord_vow.get_brokerunits_bud_times() == all_bud_times


def test_VowUnit_add_budunit_RaisesErrorWhen_bud_time_IsLessThan_offi_time_max():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    accord_offi_time_max = 606
    accord_vow._offi_time_max = accord_offi_time_max
    bob_str = "Bob"
    bob_x0_bud_time = 707
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 404
    sue_x4_quota = 55
    sue_x7_bud_time = 808
    sue_x7_quota = 66
    assert accord_vow.get_brokerunits_bud_times() == set()
    accord_vow.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    accord_vow.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        accord_vow.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    exception_str = f"Cannot set budunit because bud_time {sue_x4_bud_time} is less than VowUnit._offi_time_max {accord_offi_time_max}."
    assert str(excinfo.value) == exception_str


def test_VowUnit_add_budunit_DoesNotRaiseError_allow_prev_to_offi_time_max_entry_IsTrue():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    accord_offi_time_max = 606
    accord_vow._offi_time_max = accord_offi_time_max
    bob_str = "Bob"
    bob_x0_bud_time = 707
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 404
    sue_x4_quota = 55
    sue_x7_bud_time = 808
    sue_x7_quota = 66
    assert accord_vow.get_brokerunits_bud_times() == set()
    accord_vow.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    accord_vow.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)

    sue_brokerunit = brokerunit_shop(sue_str)
    sue_brokerunit.add_bud(sue_x4_bud_time, sue_x4_quota)
    sue_brokerunit.add_bud(sue_x7_bud_time, sue_x7_quota)
    assert accord_vow.get_brokerunit(sue_str) != sue_brokerunit

    # WHEN
    accord_vow.add_budunit(
        owner_name=sue_str,
        bud_time=sue_x4_bud_time,
        quota=sue_x4_quota,
        allow_prev_to_offi_time_max_entry=True,
    )

    # THEN
    assert accord_vow.brokerunits != {}
    assert accord_vow.get_brokerunit(sue_str) == sue_brokerunit
    bob_brokerunit = brokerunit_shop(bob_str)
    bob_brokerunit.add_bud(bob_x0_bud_time, bob_x0_quota)
    assert accord_vow.get_brokerunit(bob_str) == bob_brokerunit


def test_VowUnit_add_budunit_SetsAttr_celldepth():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    sue_x7_celldepth = 5
    assert accord_vow.brokerunits == {}

    # WHEN
    accord_vow.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    accord_vow.add_budunit(
        sue_str, sue_x7_bud_time, sue_x7_quota, celldepth=sue_x7_celldepth
    )

    # THEN
    assert accord_vow.brokerunits != {}
    expected_sue_brokerunit = brokerunit_shop(sue_str)
    expected_sue_brokerunit.add_bud(sue_x4_bud_time, sue_x4_quota)
    expected_sue_brokerunit.add_bud(
        sue_x7_bud_time, sue_x7_quota, celldepth=sue_x7_celldepth
    )
    # print(f"{expected_sue_brokerunit=}")
    gen_sue_brokerunit = accord_vow.get_brokerunit(sue_str)
    gen_sue_x7_bud = gen_sue_brokerunit.get_bud(sue_x7_bud_time)
    print(f"{gen_sue_brokerunit=}")
    assert gen_sue_x7_bud == expected_sue_brokerunit.get_bud(sue_x7_bud_time)
    assert gen_sue_brokerunit.buds == expected_sue_brokerunit.buds
    assert gen_sue_brokerunit == expected_sue_brokerunit
    assert accord_vow.get_brokerunit(sue_str) == expected_sue_brokerunit
