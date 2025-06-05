from pytest import raises as pytest_raises
from src.a02_finance_logic.deal import brokerunit_shop
from src.a15_vow_logic._test_util.a15_env import get_module_temp_dir
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


def test_VowUnit_add_dealunit_SetsAttr():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    assert accord_vow.brokerunits == {}

    # WHEN
    bob_str = "Bob"
    bob_x0_deal_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_deal_time = 4
    sue_x4_quota = 55
    sue_x7_deal_time = 7
    sue_x7_quota = 66
    accord_vow.add_dealunit(bob_str, bob_x0_deal_time, bob_x0_quota)
    accord_vow.add_dealunit(sue_str, sue_x4_deal_time, sue_x4_quota)
    accord_vow.add_dealunit(sue_str, sue_x7_deal_time, sue_x7_quota)

    # THEN
    assert accord_vow.brokerunits != {}
    sue_brokerunit = brokerunit_shop(sue_str)
    sue_brokerunit.add_deal(sue_x4_deal_time, sue_x4_quota)
    sue_brokerunit.add_deal(sue_x7_deal_time, sue_x7_quota)
    bob_brokerunit = brokerunit_shop(bob_str)
    bob_brokerunit.add_deal(bob_x0_deal_time, bob_x0_quota)
    assert accord_vow.get_brokerunit(sue_str) == sue_brokerunit
    assert accord_vow.get_brokerunit(bob_str) == bob_brokerunit


def test_VowUnit_get_dealunit_ReturnsObj_Scenario0_BrokerDoesNotExist():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    sue_str = "Sue"
    sue_x7_deal_time = 7

    # WHEN
    gen_sue_x7_dealunit = accord_vow.get_dealunit(sue_str, sue_x7_deal_time)

    # THEN
    assert accord_vow.brokerunits == {}
    assert not gen_sue_x7_dealunit


def test_VowUnit_get_dealunit_ReturnsObj_Scenario1_DealDoesNotExist():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    sue_str = "Sue"
    sue_x4_deal_time = 4
    sue_x4_quota = 66
    accord_vow.add_dealunit(sue_str, sue_x4_deal_time, sue_x4_quota)

    # WHEN
    sue_x7_deal_time = 7
    gen_sue_x7_dealunit = accord_vow.get_dealunit(sue_str, sue_x7_deal_time)

    # THEN
    assert accord_vow.brokerunits != {}
    assert not gen_sue_x7_dealunit


def test_VowUnit_get_dealunit_ReturnsObj_Scenario2_DealExists():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    bob_str = "Bob"
    bob_x0_deal_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_deal_time = 4
    sue_x4_quota = 55
    sue_x7_deal_time = 7
    sue_x7_quota = 66
    accord_vow.add_dealunit(bob_str, bob_x0_deal_time, bob_x0_quota)
    accord_vow.add_dealunit(sue_str, sue_x4_deal_time, sue_x4_quota)
    accord_vow.add_dealunit(sue_str, sue_x7_deal_time, sue_x7_quota)

    # WHEN
    gen_sue_x7_dealunit = accord_vow.get_dealunit(sue_str, sue_x7_deal_time)

    # THEN
    assert accord_vow.brokerunits != {}
    sue_broker = accord_vow.brokerunits.get(sue_str)
    assert gen_sue_x7_dealunit == sue_broker.get_deal(sue_x7_deal_time)


def test_VowUnit_get_brokerunits_deal_times_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    bob_str = "Bob"
    bob_x0_deal_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_deal_time = 4
    sue_x4_quota = 55
    sue_x7_deal_time = 7
    sue_x7_quota = 66
    assert accord_vow.get_brokerunits_deal_times() == set()

    # WHEN
    accord_vow.add_dealunit(bob_str, bob_x0_deal_time, bob_x0_quota)
    accord_vow.add_dealunit(sue_str, sue_x4_deal_time, sue_x4_quota)
    accord_vow.add_dealunit(sue_str, sue_x7_deal_time, sue_x7_quota)

    # THEN
    all_deal_times = {bob_x0_deal_time, sue_x4_deal_time, sue_x7_deal_time}
    assert accord_vow.get_brokerunits_deal_times() == all_deal_times


def test_VowUnit_add_dealunit_RaisesErrorWhen_deal_time_IsLessThan_offi_time_max():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    accord_offi_time_max = 606
    accord_vow._offi_time_max = accord_offi_time_max
    bob_str = "Bob"
    bob_x0_deal_time = 707
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_deal_time = 404
    sue_x4_quota = 55
    sue_x7_deal_time = 808
    sue_x7_quota = 66
    assert accord_vow.get_brokerunits_deal_times() == set()
    accord_vow.add_dealunit(bob_str, bob_x0_deal_time, bob_x0_quota)
    accord_vow.add_dealunit(sue_str, sue_x7_deal_time, sue_x7_quota)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        accord_vow.add_dealunit(sue_str, sue_x4_deal_time, sue_x4_quota)
    exception_str = f"Cannot set dealunit because deal_time {sue_x4_deal_time} is less than VowUnit._offi_time_max {accord_offi_time_max}."
    assert str(excinfo.value) == exception_str


def test_VowUnit_add_dealunit_DoesNotRaiseError_allow_prev_to_offi_time_max_entry_IsTrue():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    accord_offi_time_max = 606
    accord_vow._offi_time_max = accord_offi_time_max
    bob_str = "Bob"
    bob_x0_deal_time = 707
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_deal_time = 404
    sue_x4_quota = 55
    sue_x7_deal_time = 808
    sue_x7_quota = 66
    assert accord_vow.get_brokerunits_deal_times() == set()
    accord_vow.add_dealunit(bob_str, bob_x0_deal_time, bob_x0_quota)
    accord_vow.add_dealunit(sue_str, sue_x7_deal_time, sue_x7_quota)

    sue_brokerunit = brokerunit_shop(sue_str)
    sue_brokerunit.add_deal(sue_x4_deal_time, sue_x4_quota)
    sue_brokerunit.add_deal(sue_x7_deal_time, sue_x7_quota)
    assert accord_vow.get_brokerunit(sue_str) != sue_brokerunit

    # WHEN
    accord_vow.add_dealunit(
        owner_name=sue_str,
        deal_time=sue_x4_deal_time,
        quota=sue_x4_quota,
        allow_prev_to_offi_time_max_entry=True,
    )

    # THEN
    assert accord_vow.brokerunits != {}
    assert accord_vow.get_brokerunit(sue_str) == sue_brokerunit
    bob_brokerunit = brokerunit_shop(bob_str)
    bob_brokerunit.add_deal(bob_x0_deal_time, bob_x0_quota)
    assert accord_vow.get_brokerunit(bob_str) == bob_brokerunit


def test_VowUnit_add_dealunit_SetsAttr_celldepth():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    sue_str = "Sue"
    sue_x4_deal_time = 4
    sue_x4_quota = 55
    sue_x7_deal_time = 7
    sue_x7_quota = 66
    sue_x7_celldepth = 5
    assert accord_vow.brokerunits == {}

    # WHEN
    accord_vow.add_dealunit(sue_str, sue_x4_deal_time, sue_x4_quota)
    accord_vow.add_dealunit(
        sue_str, sue_x7_deal_time, sue_x7_quota, celldepth=sue_x7_celldepth
    )

    # THEN
    assert accord_vow.brokerunits != {}
    expected_sue_brokerunit = brokerunit_shop(sue_str)
    expected_sue_brokerunit.add_deal(sue_x4_deal_time, sue_x4_quota)
    expected_sue_brokerunit.add_deal(
        sue_x7_deal_time, sue_x7_quota, celldepth=sue_x7_celldepth
    )
    # print(f"{expected_sue_brokerunit=}")
    gen_sue_brokerunit = accord_vow.get_brokerunit(sue_str)
    gen_sue_x7_deal = gen_sue_brokerunit.get_deal(sue_x7_deal_time)
    print(f"{gen_sue_brokerunit=}")
    assert gen_sue_x7_deal == expected_sue_brokerunit.get_deal(sue_x7_deal_time)
    assert gen_sue_brokerunit.deals == expected_sue_brokerunit.deals
    assert gen_sue_brokerunit == expected_sue_brokerunit
    assert accord_vow.get_brokerunit(sue_str) == expected_sue_brokerunit
