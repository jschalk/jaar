from src.f01_road.road import default_bridge_if_None
from src.f01_road.finance import (
    default_fund_coin_if_None,
    default_respect_bit_if_None,
    default_penny_if_None,
)
from src.f01_road.finance_tran import bridge_str
from src.f03_chrono.chrono import get_default_timeline_config_dict
from src.f04_gift.atom_config import (
    gov_idea_str,
    fund_coin_str,
    respect_bit_str,
    penny_str,
)
from src.f07_gov.gov import (
    govunit_shop,
    get_from_dict as govunit_get_from_dict,
    get_from_json as govunit_get_from_json,
)
from src.f07_gov.gov_config import (
    timeline_str,
    current_time_str,
    pactlogs_str,
    cashbook_str,
)
from src.f07_gov.examples.gov_env import (
    get_test_govs_dir,
    env_dir_setup_cleanup,
)


def test_GovUnit_get_dict_ReturnsObjWith_cashbook():
    # ESTABLISH
    accord45_str = "accord45"
    accord_gov = govunit_shop(accord45_str, get_test_govs_dir())
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
    accord_gov.set_current_time(accord_current_time_int)
    accord_gov.add_pactepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_gov.add_pactepisode(sue_str, sue_x4_time_int, sue_x4_magnitude)
    accord_gov.add_pactepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)
    accord_gov.add_cashpurchase(
        x_owner_name=bob_str,
        x_acct_name=sue_str,
        x_time_int=cash_time_int,
        x_amount=bob_sue_amount,
    )

    # WHEN
    x_dict = accord_gov.get_dict()

    # THEN
    print(f"{ accord_gov._get_pactlogs_dict()=}")
    print(f"{ accord_gov.cashbook.get_dict()=}")
    assert x_dict.get(gov_idea_str()) == accord45_str
    assert x_dict.get(timeline_str()) == get_default_timeline_config_dict()
    assert x_dict.get(current_time_str()) == accord_current_time_int
    assert x_dict.get(bridge_str()) == default_bridge_if_None()
    assert x_dict.get(fund_coin_str()) == default_fund_coin_if_None()
    assert x_dict.get(respect_bit_str()) == default_respect_bit_if_None()
    assert x_dict.get(penny_str()) == default_penny_if_None()
    assert x_dict.get(pactlogs_str()) == accord_gov._get_pactlogs_dict()
    assert x_dict.get(cashbook_str()) == accord_gov.cashbook.get_dict()
    assert set(x_dict.keys()) == {
        gov_idea_str(),
        timeline_str(),
        current_time_str(),
        pactlogs_str(),
        bridge_str(),
        fund_coin_str(),
        respect_bit_str(),
        penny_str(),
        cashbook_str(),
    }


def test_GovUnit_get_dict_ReturnsObjWithOut_cashbook():
    # ESTABLISH
    accord45_str = "accord45"
    accord_gov = govunit_shop(accord45_str, get_test_govs_dir())

    # WHEN
    x_dict = accord_gov.get_dict(include_cashbook=False)

    # THEN
    assert not x_dict.get(cashbook_str())
    assert set(x_dict.keys()) == {
        gov_idea_str(),
        timeline_str(),
        current_time_str(),
        pactlogs_str(),
        bridge_str(),
        fund_coin_str(),
        respect_bit_str(),
        penny_str(),
    }


def test_GovUnit_get_json_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_gov = govunit_shop(accord45_str, get_test_govs_dir())
    bob_str = "Bob"
    bob_x0_time_int = 702
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_time_int = 4
    sue_x4_magnitude = 55
    sue_x7_time_int = 7
    sue_x7_magnitude = 66
    accord_gov.add_pactepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_gov.add_pactepisode(sue_str, sue_x4_time_int, sue_x4_magnitude)
    accord_gov.add_pactepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)

    # WHEN
    x_json = accord_gov.get_json()

    # THEN
    print(f"{x_json=}")
    assert x_json
    assert x_json.find(gov_idea_str()) > 0


def test_get_from_dict_ReturnsGovUnit():
    # ESTABLISH
    accord45_str = "accord45"
    accord_gov = govunit_shop(accord45_str)
    sue_timeline_idea = "sue casa"
    accord_gov.timeline.timeline_idea = sue_timeline_idea
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
    accord_gov.add_pactepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_gov.add_pactepisode(sue_str, sue_x4_time_int, sue_x4_magnitude)
    accord_gov.add_pactepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)
    accord_gov.current_time = sue_current_time
    accord_gov.bridge = sue_bridge
    accord_gov.fund_coin = sue_fund_coin
    accord_gov.respect_bit = sue_respect_bit
    accord_gov.penny = sue_penny
    accord_gov.add_cashpurchase(
        x_owner_name=bob_str,
        x_acct_name=sue_str,
        x_time_int=cash_time_int,
        x_amount=bob_sue_amount,
    )
    x_dict = accord_gov.get_dict()

    # WHEN
    x_gov = govunit_get_from_dict(x_dict)

    # THEN
    assert x_gov.gov_idea == accord45_str
    assert x_gov.timeline.timeline_idea == sue_timeline_idea
    assert x_gov.current_time == sue_current_time
    assert x_gov.bridge == sue_bridge
    assert x_gov.fund_coin == sue_fund_coin
    assert x_gov.respect_bit == sue_respect_bit
    assert x_gov.penny == sue_penny
    assert x_gov.pactlogs == accord_gov.pactlogs
    assert x_gov.cashbook == accord_gov.cashbook
    assert x_gov.govs_dir == accord_gov.govs_dir
    assert x_gov == accord_gov


def test_get_from_json_ReturnsGovUnit():
    # ESTABLISH
    accord45_str = "accord45"
    accord_gov = govunit_shop(accord45_str)
    sue_timeline_idea = "sue casa"
    accord_gov.timeline.timeline_idea = sue_timeline_idea
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
    accord_gov.add_pactepisode(bob_str, bob_x0_time_int, bob_x0_magnitude)
    accord_gov.add_pactepisode(sue_str, sue_x4_time_int, sue_x4_magnitude)
    accord_gov.add_pactepisode(sue_str, sue_x7_time_int, sue_x7_magnitude)
    accord_gov.current_time = sue_current_time
    accord_gov.bridge = sue_bridge
    accord_gov.fund_coin = sue_fund_coin
    accord_gov.respect_bit = sue_respect_bit
    accord_gov.penny = sue_penny
    accord_json = accord_gov.get_json()

    # WHEN
    x_gov = govunit_get_from_json(accord_json)

    # THEN
    assert x_gov.gov_idea == accord45_str
    assert x_gov.timeline.timeline_idea == sue_timeline_idea
    assert x_gov.current_time == sue_current_time
    assert x_gov.bridge == sue_bridge
    assert x_gov.fund_coin == sue_fund_coin
    assert x_gov.respect_bit == sue_respect_bit
    assert x_gov.penny == sue_penny
    assert x_gov.pactlogs == accord_gov.pactlogs
    assert x_gov.govs_dir == accord_gov.govs_dir
    assert x_gov == accord_gov
