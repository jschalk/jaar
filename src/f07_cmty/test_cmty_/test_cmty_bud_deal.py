from src.f01_road.finance_tran import deallog_shop
from src.f07_cmty.cmty import cmtyunit_shop
from src.f07_cmty.examples.cmty_env import get_test_cmtys_dir
from pytest import raises as pytest_raises


def test_CmtyUnit_set_deallog_SetsAttr():
    # ESTABLISH
    accord45_str = "accord45"
    accord_cmty = cmtyunit_shop(accord45_str, get_test_cmtys_dir())
    assert accord_cmty.deallogs == {}

    # WHEN
    sue_str = "Sue"
    sue_deallog = deallog_shop(sue_str)
    accord_cmty.set_deallog(sue_deallog)

    # THEN
    assert accord_cmty.deallogs != {}
    assert accord_cmty.deallogs.get(sue_str) == sue_deallog


def test_CmtyUnit_deallog_exists_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_cmty = cmtyunit_shop(accord45_str, get_test_cmtys_dir())
    sue_str = "Sue"
    assert accord_cmty.deallog_exists(sue_str) is False

    # WHEN
    sue_deallog = deallog_shop(sue_str)
    accord_cmty.set_deallog(sue_deallog)

    # THEN
    assert accord_cmty.deallog_exists(sue_str)


def test_CmtyUnit_get_deallog_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_cmty = cmtyunit_shop(accord45_str, get_test_cmtys_dir())
    sue_str = "Sue"
    sue_deallog = deallog_shop(sue_str)
    accord_cmty.set_deallog(sue_deallog)
    assert accord_cmty.deallog_exists(sue_str)

    # WHEN
    sue_gen_deallog = accord_cmty.get_deallog(sue_str)

    # THEN
    assert sue_deallog
    assert sue_deallog == sue_gen_deallog


def test_CmtyUnit_del_deallog_SetsAttr():
    # ESTABLISH
    accord45_str = "accord45"
    accord_cmty = cmtyunit_shop(accord45_str, get_test_cmtys_dir())
    sue_str = "Sue"
    sue_deallog = deallog_shop(sue_str)
    accord_cmty.set_deallog(sue_deallog)
    assert accord_cmty.deallog_exists(sue_str)

    # WHEN
    accord_cmty.del_deallog(sue_str)

    # THEN
    assert accord_cmty.deallog_exists(sue_str) is False


def test_CmtyUnit_add_dealepisode_SetsAttr():
    # ESTABLISH
    accord45_str = "accord45"
    accord_cmty = cmtyunit_shop(accord45_str, get_test_cmtys_dir())
    assert accord_cmty.deallogs == {}

    # WHEN
    bob_str = "Bob"
    bob_x0_time_int = 702
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_time_int = 4
    sue_x4_magnitude = 55
    sue_x7_time_int = 7
    sue_x7_magnitude = 66
    accord_cmty.add_dealepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_cmty.add_dealepisode(sue_str, sue_x4_time_int, sue_x4_magnitude)
    accord_cmty.add_dealepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)

    # THEN
    assert accord_cmty.deallogs != {}
    sue_deallog = deallog_shop(sue_str)
    sue_deallog.add_episode(sue_x4_time_int, sue_x4_magnitude)
    sue_deallog.add_episode(sue_x7_time_int, sue_x7_magnitude)
    bob_deallog = deallog_shop(bob_str)
    bob_deallog.add_episode(bob_x0_time_int, bob_x0_magnitude)
    assert accord_cmty.get_deallog(sue_str) == sue_deallog
    assert accord_cmty.get_deallog(bob_str) == bob_deallog


def test_CmtyUnit_get_deallogs_time_ints_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_cmty = cmtyunit_shop(accord45_str, get_test_cmtys_dir())
    bob_str = "Bob"
    bob_x0_time_int = 702
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_time_int = 4
    sue_x4_magnitude = 55
    sue_x7_time_int = 7
    sue_x7_magnitude = 66
    assert accord_cmty.get_deallogs_time_ints() == set()

    # WHEN
    accord_cmty.add_dealepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_cmty.add_dealepisode(sue_str, sue_x4_time_int, sue_x4_magnitude)
    accord_cmty.add_dealepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)

    # THEN
    all_time_ints = {bob_x0_time_int, sue_x4_time_int, sue_x7_time_int}
    assert accord_cmty.get_deallogs_time_ints() == all_time_ints


def test_CmtyUnit_add_dealepisode_RaisesErrorWhenDeal_time_int_IsLessThan_current_time():
    # ESTABLISH
    accord45_str = "accord45"
    accord_cmty = cmtyunit_shop(accord45_str, get_test_cmtys_dir())
    accord_current_time = 606
    accord_cmty.current_time = accord_current_time
    bob_str = "Bob"
    bob_x0_time_int = 707
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_time_int = 404
    sue_x4_magnitude = 55
    sue_x7_time_int = 808
    sue_x7_magnitude = 66
    assert accord_cmty.get_deallogs_time_ints() == set()
    accord_cmty.add_dealepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_cmty.add_dealepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        accord_cmty.add_dealepisode(sue_str, sue_x4_time_int, sue_x4_magnitude)
    exception_str = f"Cannot set dealepisode because time_int {sue_x4_time_int} is less than CmtyUnit.current_time {accord_current_time}."
    assert str(excinfo.value) == exception_str


def test_CmtyUnit_add_dealepisode_DoesNotRaiseError_allow_prev_to_current_time_entry_IsTrue():
    # ESTABLISH
    accord45_str = "accord45"
    accord_cmty = cmtyunit_shop(accord45_str, get_test_cmtys_dir())
    accord_current_time = 606
    accord_cmty.current_time = accord_current_time
    bob_str = "Bob"
    bob_x0_time_int = 707
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_time_int = 404
    sue_x4_magnitude = 55
    sue_x7_time_int = 808
    sue_x7_magnitude = 66
    assert accord_cmty.get_deallogs_time_ints() == set()
    accord_cmty.add_dealepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_cmty.add_dealepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)

    sue_deallog = deallog_shop(sue_str)
    sue_deallog.add_episode(sue_x4_time_int, sue_x4_magnitude)
    sue_deallog.add_episode(sue_x7_time_int, sue_x7_magnitude)
    assert accord_cmty.get_deallog(sue_str) != sue_deallog

    # WHEN
    accord_cmty.add_dealepisode(
        x_owner_name=sue_str,
        x_time_int=sue_x4_time_int,
        x_money_magnitude=sue_x4_magnitude,
        allow_prev_to_current_time_entry=True,
    )

    # THEN
    assert accord_cmty.deallogs != {}
    assert accord_cmty.get_deallog(sue_str) == sue_deallog
    bob_deallog = deallog_shop(bob_str)
    bob_deallog.add_episode(bob_x0_time_int, bob_x0_magnitude)
    assert accord_cmty.get_deallog(bob_str) == bob_deallog
