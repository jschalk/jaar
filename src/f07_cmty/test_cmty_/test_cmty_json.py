from src.f01_road.road import default_bridge_if_None
from src.f01_road.finance import (
    default_fund_coin_if_None,
    default_respect_bit_if_None,
    default_penny_if_None,
)
from src.f01_road.finance_tran import bridge_str
from src.f03_chrono.chrono import get_default_timeline_config_dict
from src.f04_gift.atom_config import (
    cmty_title_str,
    fund_coin_str,
    respect_bit_str,
    penny_str,
)
from src.f07_cmty.cmty import (
    cmtyunit_shop,
    get_from_dict as cmtyunit_get_from_dict,
    get_from_json as cmtyunit_get_from_json,
)
from src.f07_cmty.cmty_config import (
    timeline_str,
    current_time_str,
    deallogs_str,
    cashbook_str,
)
from src.f07_cmty.examples.cmty_env import (
    get_test_cmtys_dir,
    env_dir_setup_cleanup,
)


def test_CmtyUnit_get_dict_ReturnsObjWith_cashbook():
    # ESTABLISH
    accord45_str = "accord45"
    accord_cmty = cmtyunit_shop(accord45_str, get_test_cmtys_dir())
    accord_current_time_int = 23
    bob_str = "Bob"
    bob_x0_time_int = 702
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_time_int = 404
    sue_x4_magnitude = 55
    sue_x7_time_int = 505
    sue_x7_magnitude = 66
    cash_time_int = 15
    bob_sue_amount = 30000
    accord_cmty.set_current_time(accord_current_time_int)
    accord_cmty.add_dealepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_cmty.add_dealepisode(sue_str, sue_x4_time_int, sue_x4_magnitude)
    accord_cmty.add_dealepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)
    accord_cmty.add_cashpurchase(
        x_owner_name=bob_str,
        x_acct_name=sue_str,
        x_time_int=cash_time_int,
        x_amount=bob_sue_amount,
    )

    # WHEN
    x_dict = accord_cmty.get_dict()

    # THEN
    print(f"{ accord_cmty._get_deallogs_dict()=}")
    print(f"{ accord_cmty.cashbook.get_dict()=}")
    assert x_dict.get(cmty_title_str()) == accord45_str
    assert x_dict.get(timeline_str()) == get_default_timeline_config_dict()
    assert x_dict.get(current_time_str()) == accord_current_time_int
    assert x_dict.get(bridge_str()) == default_bridge_if_None()
    assert x_dict.get(fund_coin_str()) == default_fund_coin_if_None()
    assert x_dict.get(respect_bit_str()) == default_respect_bit_if_None()
    assert x_dict.get(penny_str()) == default_penny_if_None()
    assert x_dict.get(deallogs_str()) == accord_cmty._get_deallogs_dict()
    assert x_dict.get(cashbook_str()) == accord_cmty.cashbook.get_dict()
    assert set(x_dict.keys()) == {
        cmty_title_str(),
        timeline_str(),
        current_time_str(),
        deallogs_str(),
        bridge_str(),
        fund_coin_str(),
        respect_bit_str(),
        penny_str(),
        cashbook_str(),
    }


def test_CmtyUnit_get_dict_ReturnsObjWithOut_cashbook():
    # ESTABLISH
    accord45_str = "accord45"
    accord_cmty = cmtyunit_shop(accord45_str, get_test_cmtys_dir())

    # WHEN
    x_dict = accord_cmty.get_dict(include_cashbook=False)

    # THEN
    assert not x_dict.get(cashbook_str())
    assert set(x_dict.keys()) == {
        cmty_title_str(),
        timeline_str(),
        current_time_str(),
        deallogs_str(),
        bridge_str(),
        fund_coin_str(),
        respect_bit_str(),
        penny_str(),
    }


def test_CmtyUnit_get_json_ReturnsObj():
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
    accord_cmty.add_dealepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_cmty.add_dealepisode(sue_str, sue_x4_time_int, sue_x4_magnitude)
    accord_cmty.add_dealepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)

    # WHEN
    x_json = accord_cmty.get_json()

    # THEN
    print(f"{x_json=}")
    assert x_json
    assert x_json.find(cmty_title_str()) > 0


def test_get_from_dict_ReturnsCmtyUnit():
    # ESTABLISH
    accord45_str = "accord45"
    accord_cmty = cmtyunit_shop(accord45_str)
    sue_timeline_title = "sue casa"
    accord_cmty.timeline.timeline_title = sue_timeline_title
    sue_current_time = 23
    sue_bridge = "/"
    sue_fund_coin = 0.3
    sue_respect_bit = 0.5
    sue_penny = 0.8
    bob_str = "Bob"
    bob_x0_time_int = 702
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_time_int = 4
    sue_x4_magnitude = 55
    sue_x7_time_int = 7
    sue_x7_magnitude = 66
    cash_time_int = 15
    bob_sue_amount = 30000
    accord_cmty.add_dealepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_cmty.add_dealepisode(sue_str, sue_x4_time_int, sue_x4_magnitude)
    accord_cmty.add_dealepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)
    accord_cmty.current_time = sue_current_time
    accord_cmty.bridge = sue_bridge
    accord_cmty.fund_coin = sue_fund_coin
    accord_cmty.respect_bit = sue_respect_bit
    accord_cmty.penny = sue_penny
    accord_cmty.add_cashpurchase(
        x_owner_name=bob_str,
        x_acct_name=sue_str,
        x_time_int=cash_time_int,
        x_amount=bob_sue_amount,
    )
    x_dict = accord_cmty.get_dict()

    # WHEN
    x_cmty = cmtyunit_get_from_dict(x_dict)

    # THEN
    assert x_cmty.cmty_title == accord45_str
    assert x_cmty.timeline.timeline_title == sue_timeline_title
    assert x_cmty.current_time == sue_current_time
    assert x_cmty.bridge == sue_bridge
    assert x_cmty.fund_coin == sue_fund_coin
    assert x_cmty.respect_bit == sue_respect_bit
    assert x_cmty.penny == sue_penny
    assert x_cmty.deallogs == accord_cmty.deallogs
    assert x_cmty.cashbook == accord_cmty.cashbook
    assert x_cmty.cmtys_dir == accord_cmty.cmtys_dir
    assert x_cmty == accord_cmty


def test_get_from_json_ReturnsCmtyUnit():
    # ESTABLISH
    accord45_str = "accord45"
    accord_cmty = cmtyunit_shop(accord45_str)
    sue_timeline_title = "sue casa"
    accord_cmty.timeline.timeline_title = sue_timeline_title
    sue_current_time = 23
    sue_bridge = "/"
    sue_fund_coin = 0.3
    sue_respect_bit = 0.5
    sue_penny = 0.8
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
    accord_cmty.current_time = sue_current_time
    accord_cmty.bridge = sue_bridge
    accord_cmty.fund_coin = sue_fund_coin
    accord_cmty.respect_bit = sue_respect_bit
    accord_cmty.penny = sue_penny
    accord_json = accord_cmty.get_json()

    # WHEN
    x_cmty = cmtyunit_get_from_json(accord_json)

    # THEN
    assert x_cmty.cmty_title == accord45_str
    assert x_cmty.timeline.timeline_title == sue_timeline_title
    assert x_cmty.current_time == sue_current_time
    assert x_cmty.bridge == sue_bridge
    assert x_cmty.fund_coin == sue_fund_coin
    assert x_cmty.respect_bit == sue_respect_bit
    assert x_cmty.penny == sue_penny
    assert x_cmty.deallogs == accord_cmty.deallogs
    assert x_cmty.cmtys_dir == accord_cmty.cmtys_dir
    assert x_cmty == accord_cmty
