from src.f01_road.road import default_bridge_if_None
from src.f01_road.finance import (
    default_fund_coin_if_None,
    default_respect_bit_if_None,
    filter_penny,
)
from src.f01_road.deal import bridge_str, fisc_title_str
from src.f03_chrono.chrono import get_default_timeline_config_dict
from src.f04_gift.atom_config import fund_coin_str, respect_bit_str, penny_str
from src.f07_fisc.fisc import (
    fiscunit_shop,
    get_from_dict as fiscunit_get_from_dict,
    get_from_json as fiscunit_get_from_json,
)
from src.f07_fisc.fisc_config import (
    timeline_str,
    present_time_str,
    deallogs_str,
    cashbook_str,
)
from src.f07_fisc.examples.fisc_env import (
    get_test_fisc_mstr_dir,
    env_dir_setup_cleanup,
)


def test_FiscUnit_get_dict_ReturnsObjWith_cashbook():
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = fiscunit_shop(accord45_str, get_test_fisc_mstr_dir())
    accord_present_time_int = 23
    bob_str = "Bob"
    bob_x0_time_int = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_time_int = 404
    sue_x4_quota = 55
    sue_x7_time_int = 505
    sue_x7_quota = 66
    cash_time_int = 15
    bob_sue_amount = 30000
    accord_fisc.set_present_time(accord_present_time_int)
    accord_fisc.add_dealepisode(bob_str, bob_x0_time_int, bob_x0_quota)
    accord_fisc.add_dealepisode(sue_str, sue_x4_time_int, sue_x4_quota)
    accord_fisc.add_dealepisode(sue_str, sue_x7_time_int, sue_x7_quota)
    accord_fisc.add_cashpurchase(
        owner_name=bob_str,
        acct_name=sue_str,
        time_int=cash_time_int,
        amount=bob_sue_amount,
    )

    # WHEN
    x_dict = accord_fisc.get_dict()

    # THEN
    print(f"{ accord_fisc._get_deallogs_dict()=}")
    print(f"{ accord_fisc.cashbook.get_dict()=}")
    assert x_dict.get(fisc_title_str()) == accord45_str
    assert x_dict.get(timeline_str()) == get_default_timeline_config_dict()
    assert x_dict.get(present_time_str()) == accord_present_time_int
    assert x_dict.get(bridge_str()) == default_bridge_if_None()
    assert x_dict.get(fund_coin_str()) == default_fund_coin_if_None()
    assert x_dict.get(respect_bit_str()) == default_respect_bit_if_None()
    assert x_dict.get(penny_str()) == filter_penny()
    assert x_dict.get(deallogs_str()) == accord_fisc._get_deallogs_dict()
    assert x_dict.get(cashbook_str()) == accord_fisc.cashbook.get_dict()
    assert set(x_dict.keys()) == {
        fisc_title_str(),
        timeline_str(),
        present_time_str(),
        deallogs_str(),
        bridge_str(),
        fund_coin_str(),
        respect_bit_str(),
        penny_str(),
        cashbook_str(),
    }


def test_FiscUnit_get_dict_ReturnsObjWithOut_cashbook():
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = fiscunit_shop(accord45_str, get_test_fisc_mstr_dir())

    # WHEN
    x_dict = accord_fisc.get_dict(include_cashbook=False)

    # THEN
    assert not x_dict.get(cashbook_str())
    assert set(x_dict.keys()) == {
        fisc_title_str(),
        timeline_str(),
        present_time_str(),
        deallogs_str(),
        bridge_str(),
        fund_coin_str(),
        respect_bit_str(),
        penny_str(),
    }


def test_FiscUnit_get_json_ReturnsObj():
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
    accord_fisc.add_dealepisode(bob_str, bob_x0_time_int, bob_x0_quota)
    accord_fisc.add_dealepisode(sue_str, sue_x4_time_int, sue_x4_quota)
    accord_fisc.add_dealepisode(sue_str, sue_x7_time_int, sue_x7_quota)

    # WHEN
    x_json = accord_fisc.get_json()

    # THEN
    print(f"{x_json=}")
    assert x_json
    assert x_json.find(fisc_title_str()) > 0


def test_get_from_dict_ReturnsFiscUnit():
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = fiscunit_shop(accord45_str)
    sue_timeline_title = "sue casa"
    accord_fisc.timeline.timeline_title = sue_timeline_title
    sue_present_time = 23
    sue_bridge = "/"
    sue_fund_coin = 0.3
    sue_respect_bit = 0.5
    sue_penny = 0.8
    bob_str = "Bob"
    bob_x0_time_int = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_time_int = 4
    sue_x4_quota = 55
    sue_x7_time_int = 7
    sue_x7_quota = 66
    cash_time_int = 15
    bob_sue_amount = 30000
    accord_fisc.add_dealepisode(bob_str, bob_x0_time_int, bob_x0_quota)
    accord_fisc.add_dealepisode(sue_str, sue_x4_time_int, sue_x4_quota)
    accord_fisc.add_dealepisode(sue_str, sue_x7_time_int, sue_x7_quota)
    accord_fisc.present_time = sue_present_time
    accord_fisc.bridge = sue_bridge
    accord_fisc.fund_coin = sue_fund_coin
    accord_fisc.respect_bit = sue_respect_bit
    accord_fisc.penny = sue_penny
    accord_fisc.add_cashpurchase(
        owner_name=bob_str,
        acct_name=sue_str,
        time_int=cash_time_int,
        amount=bob_sue_amount,
    )
    x_dict = accord_fisc.get_dict()

    # WHEN
    x_fisc = fiscunit_get_from_dict(x_dict)

    # THEN
    assert x_fisc.fisc_title == accord45_str
    assert x_fisc.timeline.timeline_title == sue_timeline_title
    assert x_fisc.present_time == sue_present_time
    assert x_fisc.bridge == sue_bridge
    assert x_fisc.fund_coin == sue_fund_coin
    assert x_fisc.respect_bit == sue_respect_bit
    assert x_fisc.penny == sue_penny
    assert x_fisc.deallogs == accord_fisc.deallogs
    assert x_fisc.cashbook == accord_fisc.cashbook
    assert x_fisc.fisc_mstr_dir == accord_fisc.fisc_mstr_dir
    assert x_fisc == accord_fisc


def test_get_from_json_ReturnsFiscUnit():
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = fiscunit_shop(accord45_str)
    sue_timeline_title = "sue casa"
    accord_fisc.timeline.timeline_title = sue_timeline_title
    sue_present_time = 23
    sue_bridge = "/"
    sue_fund_coin = 0.3
    sue_respect_bit = 0.5
    sue_penny = 0.8
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
    accord_fisc.present_time = sue_present_time
    accord_fisc.bridge = sue_bridge
    accord_fisc.fund_coin = sue_fund_coin
    accord_fisc.respect_bit = sue_respect_bit
    accord_fisc.penny = sue_penny
    accord_json = accord_fisc.get_json()

    # WHEN
    x_fisc = fiscunit_get_from_json(accord_json)

    # THEN
    assert x_fisc.fisc_title == accord45_str
    assert x_fisc.timeline.timeline_title == sue_timeline_title
    assert x_fisc.present_time == sue_present_time
    assert x_fisc.bridge == sue_bridge
    assert x_fisc.fund_coin == sue_fund_coin
    assert x_fisc.respect_bit == sue_respect_bit
    assert x_fisc.penny == sue_penny
    assert x_fisc.deallogs == accord_fisc.deallogs
    assert x_fisc.fisc_mstr_dir == accord_fisc.fisc_mstr_dir
    assert x_fisc == accord_fisc
