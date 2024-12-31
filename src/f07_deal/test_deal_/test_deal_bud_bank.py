from src.f01_road.finance_tran import banklog_shop
from src.f07_deal.deal import dealunit_shop
from src.f07_deal.examples.deal_env import get_test_deals_dir
from pytest import raises as pytest_raises


def test_DealUnit_set_banklog_SetsAttr():
    # ESTABLISH
    accord45_str = "accord45"
    accord_deal = dealunit_shop(accord45_str, get_test_deals_dir())
    assert accord_deal.banklogs == {}

    # WHEN
    sue_str = "Sue"
    sue_banklog = banklog_shop(sue_str)
    accord_deal.set_banklog(sue_banklog)

    # THEN
    assert accord_deal.banklogs != {}
    assert accord_deal.banklogs.get(sue_str) == sue_banklog


def test_DealUnit_banklog_exists_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_deal = dealunit_shop(accord45_str, get_test_deals_dir())
    sue_str = "Sue"
    assert accord_deal.banklog_exists(sue_str) is False

    # WHEN
    sue_banklog = banklog_shop(sue_str)
    accord_deal.set_banklog(sue_banklog)

    # THEN
    assert accord_deal.banklog_exists(sue_str)


def test_DealUnit_get_banklog_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_deal = dealunit_shop(accord45_str, get_test_deals_dir())
    sue_str = "Sue"
    sue_banklog = banklog_shop(sue_str)
    accord_deal.set_banklog(sue_banklog)
    assert accord_deal.banklog_exists(sue_str)

    # WHEN
    sue_gen_banklog = accord_deal.get_banklog(sue_str)

    # THEN
    assert sue_banklog
    assert sue_banklog == sue_gen_banklog


def test_DealUnit_del_banklog_SetsAttr():
    # ESTABLISH
    accord45_str = "accord45"
    accord_deal = dealunit_shop(accord45_str, get_test_deals_dir())
    sue_str = "Sue"
    sue_banklog = banklog_shop(sue_str)
    accord_deal.set_banklog(sue_banklog)
    assert accord_deal.banklog_exists(sue_str)

    # WHEN
    accord_deal.del_banklog(sue_str)

    # THEN
    assert accord_deal.banklog_exists(sue_str) is False


def test_DealUnit_add_bankepisode_SetsAttr():
    # ESTABLISH
    accord45_str = "accord45"
    accord_deal = dealunit_shop(accord45_str, get_test_deals_dir())
    assert accord_deal.banklogs == {}

    # WHEN
    bob_str = "Bob"
    bob_x0_time_int = 702
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_time_int = 4
    sue_x4_magnitude = 55
    sue_x7_time_int = 7
    sue_x7_magnitude = 66
    accord_deal.add_bankepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_deal.add_bankepisode(sue_str, sue_x4_time_int, sue_x4_magnitude)
    accord_deal.add_bankepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)

    # THEN
    assert accord_deal.banklogs != {}
    sue_banklog = banklog_shop(sue_str)
    sue_banklog.add_episode(sue_x4_time_int, sue_x4_magnitude)
    sue_banklog.add_episode(sue_x7_time_int, sue_x7_magnitude)
    bob_banklog = banklog_shop(bob_str)
    bob_banklog.add_episode(bob_x0_time_int, bob_x0_magnitude)
    assert accord_deal.get_banklog(sue_str) == sue_banklog
    assert accord_deal.get_banklog(bob_str) == bob_banklog


def test_DealUnit_get_banklogs_time_ints_ReturnsObj():
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
    assert accord_deal.get_banklogs_time_ints() == set()

    # WHEN
    accord_deal.add_bankepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_deal.add_bankepisode(sue_str, sue_x4_time_int, sue_x4_magnitude)
    accord_deal.add_bankepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)

    # THEN
    all_time_ints = {bob_x0_time_int, sue_x4_time_int, sue_x7_time_int}
    assert accord_deal.get_banklogs_time_ints() == all_time_ints


def test_DealUnit_add_bankepisode_RaisesErrorWhenBank_time_int_IsLessThan_current_time():
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
    assert accord_deal.get_banklogs_time_ints() == set()
    accord_deal.add_bankepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_deal.add_bankepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        accord_deal.add_bankepisode(sue_str, sue_x4_time_int, sue_x4_magnitude)
    exception_str = f"Cannot set bankepisode because time_int {sue_x4_time_int} is less than DealUnit.current_time {accord_current_time}."
    assert str(excinfo.value) == exception_str


def test_DealUnit_add_bankepisode_DoesNotRaiseError_allow_prev_to_current_time_entry_IsTrue():
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
    assert accord_deal.get_banklogs_time_ints() == set()
    accord_deal.add_bankepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_deal.add_bankepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)

    sue_banklog = banklog_shop(sue_str)
    sue_banklog.add_episode(sue_x4_time_int, sue_x4_magnitude)
    sue_banklog.add_episode(sue_x7_time_int, sue_x7_magnitude)
    assert accord_deal.get_banklog(sue_str) != sue_banklog

    # WHEN
    accord_deal.add_bankepisode(
        x_owner_name=sue_str,
        x_time_int=sue_x4_time_int,
        x_money_magnitude=sue_x4_magnitude,
        allow_prev_to_current_time_entry=True,
    )

    # THEN
    assert accord_deal.banklogs != {}
    assert accord_deal.get_banklog(sue_str) == sue_banklog
    bob_banklog = banklog_shop(bob_str)
    bob_banklog.add_episode(bob_x0_time_int, bob_x0_magnitude)
    assert accord_deal.get_banklog(bob_str) == bob_banklog
