from src.f01_road.deal import brokerunit_shop
from src.f07_fisc.fisc import fiscunit_shop
from src.f07_fisc.examples.fisc_env import get_test_fisc_mstr_dir
from pytest import raises as pytest_raises


def test_FiscUnit_set_brokerunit_SetsAttr():
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = fiscunit_shop(accord45_str, get_test_fisc_mstr_dir())
    assert accord_fisc.brokerunits == {}

    # WHEN
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    accord_fisc.set_brokerunit(sue_brokerunit)

    # THEN
    assert accord_fisc.brokerunits != {}
    assert accord_fisc.brokerunits.get(sue_str) == sue_brokerunit


def test_FiscUnit_brokerunit_exists_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = fiscunit_shop(accord45_str, get_test_fisc_mstr_dir())
    sue_str = "Sue"
    assert accord_fisc.brokerunit_exists(sue_str) is False

    # WHEN
    sue_brokerunit = brokerunit_shop(sue_str)
    accord_fisc.set_brokerunit(sue_brokerunit)

    # THEN
    assert accord_fisc.brokerunit_exists(sue_str)


def test_FiscUnit_get_brokerunit_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = fiscunit_shop(accord45_str, get_test_fisc_mstr_dir())
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    accord_fisc.set_brokerunit(sue_brokerunit)
    assert accord_fisc.brokerunit_exists(sue_str)

    # WHEN
    sue_gen_brokerunit = accord_fisc.get_brokerunit(sue_str)

    # THEN
    assert sue_brokerunit
    assert sue_brokerunit == sue_gen_brokerunit


def test_FiscUnit_del_brokerunit_SetsAttr():
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = fiscunit_shop(accord45_str, get_test_fisc_mstr_dir())
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    accord_fisc.set_brokerunit(sue_brokerunit)
    assert accord_fisc.brokerunit_exists(sue_str)

    # WHEN
    accord_fisc.del_brokerunit(sue_str)

    # THEN
    assert accord_fisc.brokerunit_exists(sue_str) is False


def test_FiscUnit_add_dealepisode_SetsAttr():
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = fiscunit_shop(accord45_str, get_test_fisc_mstr_dir())
    assert accord_fisc.brokerunits == {}

    # WHEN
    bob_str = "Bob"
    bob_x0_time_int = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_time_int = 4
    sue_x4_quota = 55
    sue_x7_time_int = 7
    sue_x7_quota = 66
    accord_fisc.add_dealepisode(bob_str, bob_x0_time_int, bob_x0_quota)
    accord_fisc.add_dealepisode(sue_str, sue_x4_time_int, sue_x4_quota)
    accord_fisc.add_dealepisode(sue_str, sue_x7_time_int, sue_x7_quota)

    # THEN
    assert accord_fisc.brokerunits != {}
    sue_brokerunit = brokerunit_shop(sue_str)
    sue_brokerunit.add_episode(sue_x4_time_int, sue_x4_quota)
    sue_brokerunit.add_episode(sue_x7_time_int, sue_x7_quota)
    bob_brokerunit = brokerunit_shop(bob_str)
    bob_brokerunit.add_episode(bob_x0_time_int, bob_x0_quota)
    assert accord_fisc.get_brokerunit(sue_str) == sue_brokerunit
    assert accord_fisc.get_brokerunit(bob_str) == bob_brokerunit


def test_FiscUnit_get_brokerunits_time_ints_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = fiscunit_shop(accord45_str, get_test_fisc_mstr_dir())
    bob_str = "Bob"
    bob_x0_time_int = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_time_int = 4
    sue_x4_quota = 55
    sue_x7_time_int = 7
    sue_x7_quota = 66
    assert accord_fisc.get_brokerunits_time_ints() == set()

    # WHEN
    accord_fisc.add_dealepisode(bob_str, bob_x0_time_int, bob_x0_quota)
    accord_fisc.add_dealepisode(sue_str, sue_x4_time_int, sue_x4_quota)
    accord_fisc.add_dealepisode(sue_str, sue_x7_time_int, sue_x7_quota)

    # THEN
    all_time_ints = {bob_x0_time_int, sue_x4_time_int, sue_x7_time_int}
    assert accord_fisc.get_brokerunits_time_ints() == all_time_ints


def test_FiscUnit_add_dealepisode_RaisesErrorWhen_time_int_IsLessThan_present_time():
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = fiscunit_shop(accord45_str, get_test_fisc_mstr_dir())
    accord_present_time = 606
    accord_fisc.present_time = accord_present_time
    bob_str = "Bob"
    bob_x0_time_int = 707
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_time_int = 404
    sue_x4_quota = 55
    sue_x7_time_int = 808
    sue_x7_quota = 66
    assert accord_fisc.get_brokerunits_time_ints() == set()
    accord_fisc.add_dealepisode(bob_str, bob_x0_time_int, bob_x0_quota)
    accord_fisc.add_dealepisode(sue_str, sue_x7_time_int, sue_x7_quota)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        accord_fisc.add_dealepisode(sue_str, sue_x4_time_int, sue_x4_quota)
    exception_str = f"Cannot set dealepisode because time_int {sue_x4_time_int} is less than FiscUnit.present_time {accord_present_time}."
    assert str(excinfo.value) == exception_str


def test_FiscUnit_add_dealepisode_DoesNotRaiseError_allow_prev_to_present_time_entry_IsTrue():
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = fiscunit_shop(accord45_str, get_test_fisc_mstr_dir())
    accord_present_time = 606
    accord_fisc.present_time = accord_present_time
    bob_str = "Bob"
    bob_x0_time_int = 707
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_time_int = 404
    sue_x4_quota = 55
    sue_x7_time_int = 808
    sue_x7_quota = 66
    assert accord_fisc.get_brokerunits_time_ints() == set()
    accord_fisc.add_dealepisode(bob_str, bob_x0_time_int, bob_x0_quota)
    accord_fisc.add_dealepisode(sue_str, sue_x7_time_int, sue_x7_quota)

    sue_brokerunit = brokerunit_shop(sue_str)
    sue_brokerunit.add_episode(sue_x4_time_int, sue_x4_quota)
    sue_brokerunit.add_episode(sue_x7_time_int, sue_x7_quota)
    assert accord_fisc.get_brokerunit(sue_str) != sue_brokerunit

    # WHEN
    accord_fisc.add_dealepisode(
        owner_name=sue_str,
        time_int=sue_x4_time_int,
        quota=sue_x4_quota,
        allow_prev_to_present_time_entry=True,
    )

    # THEN
    assert accord_fisc.brokerunits != {}
    assert accord_fisc.get_brokerunit(sue_str) == sue_brokerunit
    bob_brokerunit = brokerunit_shop(bob_str)
    bob_brokerunit.add_episode(bob_x0_time_int, bob_x0_quota)
    assert accord_fisc.get_brokerunit(bob_str) == bob_brokerunit


def test_FiscUnit_add_dealepisode_SetsAttr_ledger_depth():
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = fiscunit_shop(accord45_str, get_test_fisc_mstr_dir())
    sue_str = "Sue"
    sue_x4_time_int = 4
    sue_x4_quota = 55
    sue_x7_time_int = 7
    sue_x7_quota = 66
    sue_x7_ledger_depth = 5
    assert accord_fisc.brokerunits == {}

    # WHEN
    accord_fisc.add_dealepisode(sue_str, sue_x4_time_int, sue_x4_quota)
    accord_fisc.add_dealepisode(
        sue_str, sue_x7_time_int, sue_x7_quota, ledger_depth=sue_x7_ledger_depth
    )

    # THEN
    assert accord_fisc.brokerunits != {}
    expected_sue_brokerunit = brokerunit_shop(sue_str)
    expected_sue_brokerunit.add_episode(sue_x4_time_int, sue_x4_quota)
    expected_sue_brokerunit.add_episode(
        sue_x7_time_int, sue_x7_quota, ledger_depth=sue_x7_ledger_depth
    )
    # print(f"{expected_sue_brokerunit=}")
    gen_sue_brokerunit = accord_fisc.get_brokerunit(sue_str)
    gen_sue_x7_episode = gen_sue_brokerunit.get_episode(sue_x7_time_int)
    print(f"{gen_sue_brokerunit=}")
    assert gen_sue_x7_episode == expected_sue_brokerunit.get_episode(sue_x7_time_int)
    assert gen_sue_brokerunit.episodes == expected_sue_brokerunit.episodes
    assert gen_sue_brokerunit == expected_sue_brokerunit
    assert accord_fisc.get_brokerunit(sue_str) == expected_sue_brokerunit
