from src.f01_road.finance_tran import turnlog_shop
from src.f07_deal.deal import dealunit_shop
from src.f07_deal.examples.deal_env import get_test_deals_dir
from pytest import raises as pytest_raises


def test_DealUnit_set_turnlog_SetsAttr():
    # ESTABLISH
    accord45_str = "accord45"
    accord_deal = dealunit_shop(accord45_str, get_test_deals_dir())
    assert accord_deal.turnlogs == {}

    # WHEN
    sue_str = "Sue"
    sue_turnlog = turnlog_shop(sue_str)
    accord_deal.set_turnlog(sue_turnlog)

    # THEN
    assert accord_deal.turnlogs != {}
    assert accord_deal.turnlogs.get(sue_str) == sue_turnlog


def test_DealUnit_turnlog_exists_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_deal = dealunit_shop(accord45_str, get_test_deals_dir())
    sue_str = "Sue"
    assert accord_deal.turnlog_exists(sue_str) is False

    # WHEN
    sue_turnlog = turnlog_shop(sue_str)
    accord_deal.set_turnlog(sue_turnlog)

    # THEN
    assert accord_deal.turnlog_exists(sue_str)


def test_DealUnit_get_turnlog_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_deal = dealunit_shop(accord45_str, get_test_deals_dir())
    sue_str = "Sue"
    sue_turnlog = turnlog_shop(sue_str)
    accord_deal.set_turnlog(sue_turnlog)
    assert accord_deal.turnlog_exists(sue_str)

    # WHEN
    sue_gen_turnlog = accord_deal.get_turnlog(sue_str)

    # THEN
    assert sue_turnlog
    assert sue_turnlog == sue_gen_turnlog


def test_DealUnit_del_turnlog_SetsAttr():
    # ESTABLISH
    accord45_str = "accord45"
    accord_deal = dealunit_shop(accord45_str, get_test_deals_dir())
    sue_str = "Sue"
    sue_turnlog = turnlog_shop(sue_str)
    accord_deal.set_turnlog(sue_turnlog)
    assert accord_deal.turnlog_exists(sue_str)

    # WHEN
    accord_deal.del_turnlog(sue_str)

    # THEN
    assert accord_deal.turnlog_exists(sue_str) is False


def test_DealUnit_add_turnepisode_SetsAttr():
    # ESTABLISH
    accord45_str = "accord45"
    accord_deal = dealunit_shop(accord45_str, get_test_deals_dir())
    assert accord_deal.turnlogs == {}

    # WHEN
    bob_str = "Bob"
    bob_x0_time_int = 702
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_time_int = 4
    sue_x4_magnitude = 55
    sue_x7_time_int = 7
    sue_x7_magnitude = 66
    accord_deal.add_turnepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_deal.add_turnepisode(sue_str, sue_x4_time_int, sue_x4_magnitude)
    accord_deal.add_turnepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)

    # THEN
    assert accord_deal.turnlogs != {}
    sue_turnlog = turnlog_shop(sue_str)
    sue_turnlog.add_episode(sue_x4_time_int, sue_x4_magnitude)
    sue_turnlog.add_episode(sue_x7_time_int, sue_x7_magnitude)
    bob_turnlog = turnlog_shop(bob_str)
    bob_turnlog.add_episode(bob_x0_time_int, bob_x0_magnitude)
    assert accord_deal.get_turnlog(sue_str) == sue_turnlog
    assert accord_deal.get_turnlog(bob_str) == bob_turnlog


def test_DealUnit_get_turnlogs_time_ints_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_deal = dealunit_shop(accord45_str, get_test_deals_dir())
    bob_str = "Bob"
    bob_x0_time_int = 702
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_time_int = 4
    sue_x4_magnitude = 55
    sue_x7_time_int = 7
    sue_x7_magnitude = 66
    assert accord_deal.get_turnlogs_time_ints() == set()

    # WHEN
    accord_deal.add_turnepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_deal.add_turnepisode(sue_str, sue_x4_time_int, sue_x4_magnitude)
    accord_deal.add_turnepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)

    # THEN
    all_time_ints = {bob_x0_time_int, sue_x4_time_int, sue_x7_time_int}
    assert accord_deal.get_turnlogs_time_ints() == all_time_ints


def test_DealUnit_add_turnepisode_RaisesErrorWhenTurn_time_int_IsLessThan_current_time():
    # ESTABLISH
    accord45_str = "accord45"
    accord_deal = dealunit_shop(accord45_str, get_test_deals_dir())
    accord_current_time = 606
    accord_deal.current_time = accord_current_time
    bob_str = "Bob"
    bob_x0_time_int = 707
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_time_int = 404
    sue_x4_magnitude = 55
    sue_x7_time_int = 808
    sue_x7_magnitude = 66
    assert accord_deal.get_turnlogs_time_ints() == set()
    accord_deal.add_turnepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_deal.add_turnepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        accord_deal.add_turnepisode(sue_str, sue_x4_time_int, sue_x4_magnitude)
    exception_str = f"Cannot set turnepisode because time_int {sue_x4_time_int} is less than DealUnit.current_time {accord_current_time}."
    assert str(excinfo.value) == exception_str


def test_DealUnit_add_turnepisode_DoesNotRaiseError_allow_prev_to_current_time_entry_IsTrue():
    # ESTABLISH
    accord45_str = "accord45"
    accord_deal = dealunit_shop(accord45_str, get_test_deals_dir())
    accord_current_time = 606
    accord_deal.current_time = accord_current_time
    bob_str = "Bob"
    bob_x0_time_int = 707
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_time_int = 404
    sue_x4_magnitude = 55
    sue_x7_time_int = 808
    sue_x7_magnitude = 66
    assert accord_deal.get_turnlogs_time_ints() == set()
    accord_deal.add_turnepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_deal.add_turnepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)

    sue_turnlog = turnlog_shop(sue_str)
    sue_turnlog.add_episode(sue_x4_time_int, sue_x4_magnitude)
    sue_turnlog.add_episode(sue_x7_time_int, sue_x7_magnitude)
    assert accord_deal.get_turnlog(sue_str) != sue_turnlog

    # WHEN
    accord_deal.add_turnepisode(
        x_owner_name=sue_str,
        x_time_int=sue_x4_time_int,
        x_money_magnitude=sue_x4_magnitude,
        allow_prev_to_current_time_entry=True,
    )

    # THEN
    assert accord_deal.turnlogs != {}
    assert accord_deal.get_turnlog(sue_str) == sue_turnlog
    bob_turnlog = turnlog_shop(bob_str)
    bob_turnlog.add_episode(bob_x0_time_int, bob_x0_magnitude)
    assert accord_deal.get_turnlog(bob_str) == bob_turnlog
