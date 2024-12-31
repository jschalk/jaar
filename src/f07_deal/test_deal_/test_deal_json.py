from src.f01_road.road import default_bridge_if_None
from src.f01_road.finance import (
    default_fund_coin_if_None,
    default_respect_bit_if_None,
    default_penny_if_None,
)
from src.f01_road.finance_tran import bridge_str
from src.f03_chrono.chrono import get_default_timeline_config_dict
from src.f04_gift.atom_config import (
    deal_idea_str,
    fund_coin_str,
    respect_bit_str,
    penny_str,
)
from src.f07_deal.deal import (
    dealunit_shop,
    get_from_dict as dealunit_get_from_dict,
    get_from_json as dealunit_get_from_json,
)
from src.f07_deal.deal_config import (
    timeline_str,
    current_time_str,
    banklogs_str,
    cashbook_str,
)
from src.f07_deal.examples.deal_env import (
    get_test_deals_dir,
    env_dir_setup_cleanup,
)


def test_DealUnit_get_dict_ReturnsObjWith_cashbook():
    # ESTABLISH
    accord45_str = "accord45"
    accord_deal = dealunit_shop(accord45_str, get_test_deals_dir())
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
    accord_deal.set_current_time(accord_current_time_int)
    accord_deal.add_bankepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_deal.add_bankepisode(sue_str, sue_x4_time_int, sue_x4_magnitude)
    accord_deal.add_bankepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)
    accord_deal.add_cashpurchase(
        x_owner_name=bob_str,
        x_acct_name=sue_str,
        x_time_int=cash_time_int,
        x_amount=bob_sue_amount,
    )

    # WHEN
    x_dict = accord_deal.get_dict()

    # THEN
    print(f"{ accord_deal._get_banklogs_dict()=}")
    print(f"{ accord_deal.cashbook.get_dict()=}")
    assert x_dict.get(deal_idea_str()) == accord45_str
    assert x_dict.get(timeline_str()) == get_default_timeline_config_dict()
    assert x_dict.get(current_time_str()) == accord_current_time_int
    assert x_dict.get(bridge_str()) == default_bridge_if_None()
    assert x_dict.get(fund_coin_str()) == default_fund_coin_if_None()
    assert x_dict.get(respect_bit_str()) == default_respect_bit_if_None()
    assert x_dict.get(penny_str()) == default_penny_if_None()
    assert x_dict.get(banklogs_str()) == accord_deal._get_banklogs_dict()
    assert x_dict.get(cashbook_str()) == accord_deal.cashbook.get_dict()
    assert set(x_dict.keys()) == {
        deal_idea_str(),
        timeline_str(),
        current_time_str(),
        banklogs_str(),
        bridge_str(),
        fund_coin_str(),
        respect_bit_str(),
        penny_str(),
        cashbook_str(),
    }


def test_DealUnit_get_dict_ReturnsObjWithOut_cashbook():
    # ESTABLISH
    accord45_str = "accord45"
    accord_deal = dealunit_shop(accord45_str, get_test_deals_dir())

    # WHEN
    x_dict = accord_deal.get_dict(include_cashbook=False)

    # THEN
    assert not x_dict.get(cashbook_str())
    assert set(x_dict.keys()) == {
        deal_idea_str(),
        timeline_str(),
        current_time_str(),
        banklogs_str(),
        bridge_str(),
        fund_coin_str(),
        respect_bit_str(),
        penny_str(),
    }


def test_DealUnit_get_json_ReturnsObj():
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
    accord_deal.add_bankepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_deal.add_bankepisode(sue_str, sue_x4_time_int, sue_x4_magnitude)
    accord_deal.add_bankepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)

    # WHEN
    x_json = accord_deal.get_json()

    # THEN
    print(f"{x_json=}")
    assert x_json
    assert x_json.find(deal_idea_str()) > 0


def test_get_from_dict_ReturnsDealUnit():
    # ESTABLISH
    accord45_str = "accord45"
    accord_deal = dealunit_shop(accord45_str)
    sue_timeline_idea = "sue casa"
    accord_deal.timeline.timeline_idea = sue_timeline_idea
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
    accord_deal.add_bankepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_deal.add_bankepisode(sue_str, sue_x4_time_int, sue_x4_magnitude)
    accord_deal.add_bankepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)
    accord_deal.current_time = sue_current_time
    accord_deal.bridge = sue_bridge
    accord_deal.fund_coin = sue_fund_coin
    accord_deal.respect_bit = sue_respect_bit
    accord_deal.penny = sue_penny
    accord_deal.add_cashpurchase(
        x_owner_name=bob_str,
        x_acct_name=sue_str,
        x_time_int=cash_time_int,
        x_amount=bob_sue_amount,
    )
    x_dict = accord_deal.get_dict()

    # WHEN
    x_deal = dealunit_get_from_dict(x_dict)

    # THEN
    assert x_deal.deal_idea == accord45_str
    assert x_deal.timeline.timeline_idea == sue_timeline_idea
    assert x_deal.current_time == sue_current_time
    assert x_deal.bridge == sue_bridge
    assert x_deal.fund_coin == sue_fund_coin
    assert x_deal.respect_bit == sue_respect_bit
    assert x_deal.penny == sue_penny
    assert x_deal.banklogs == accord_deal.banklogs
    assert x_deal.cashbook == accord_deal.cashbook
    assert x_deal.deals_dir == accord_deal.deals_dir
    assert x_deal == accord_deal


def test_get_from_json_ReturnsDealUnit():
    # ESTABLISH
    accord45_str = "accord45"
    accord_deal = dealunit_shop(accord45_str)
    sue_timeline_idea = "sue casa"
    accord_deal.timeline.timeline_idea = sue_timeline_idea
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
    accord_deal.add_bankepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_deal.add_bankepisode(sue_str, sue_x4_time_int, sue_x4_magnitude)
    accord_deal.add_bankepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)
    accord_deal.current_time = sue_current_time
    accord_deal.bridge = sue_bridge
    accord_deal.fund_coin = sue_fund_coin
    accord_deal.respect_bit = sue_respect_bit
    accord_deal.penny = sue_penny
    accord_json = accord_deal.get_json()

    # WHEN
    x_deal = dealunit_get_from_json(accord_json)

    # THEN
    assert x_deal.deal_idea == accord45_str
    assert x_deal.timeline.timeline_idea == sue_timeline_idea
    assert x_deal.current_time == sue_current_time
    assert x_deal.bridge == sue_bridge
    assert x_deal.fund_coin == sue_fund_coin
    assert x_deal.respect_bit == sue_respect_bit
    assert x_deal.penny == sue_penny
    assert x_deal.banklogs == accord_deal.banklogs
    assert x_deal.deals_dir == accord_deal.deals_dir
    assert x_deal == accord_deal
