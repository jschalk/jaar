from src.f01_road.road import default_wall_if_None
from src.f01_road.finance import (
    default_fund_coin_if_None,
    default_respect_bit_if_None,
    default_penny_if_None,
)
from src.f03_chrono.chrono import get_default_timeline_config_dict
from src.f04_gift.atom_config import deal_id_str
from src.f07_deal.deal import (
    dealunit_shop,
    get_from_dict as dealunit_get_from_dict,
    get_from_json as dealunit_get_from_json,
)
from src.f07_deal.examples.deal_env import (
    get_test_deals_dir,
    env_dir_setup_cleanup,
)


def test_DealUnit_get_dict_ReturnsObj():
    # ESTABLISH
    music_str = "music"
    music_deal = dealunit_shop(music_str, get_test_deals_dir())
    bob_str = "Bob"
    bob_x0_time_id = 702
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_time_id = 4
    sue_x4_magnitude = 55
    sue_x7_time_id = 7
    sue_x7_magnitude = 66
    music_deal.add_purviewepisode(bob_str, bob_x0_time_id, bob_x0_magnitude)
    music_deal.add_purviewepisode(sue_str, sue_x4_time_id, sue_x4_magnitude)
    music_deal.add_purviewepisode(sue_str, sue_x7_time_id, sue_x7_magnitude)

    # WHEN
    x_dict = music_deal.get_dict()

    # THEN
    assert x_dict.get(deal_id_str()) == music_str
    assert x_dict.get("timeline") == get_default_timeline_config_dict()
    assert x_dict.get("current_time") == 0
    assert x_dict.get("wall") == default_wall_if_None()
    assert x_dict.get("fund_coin") == default_fund_coin_if_None()
    assert x_dict.get("respect_bit") == default_respect_bit_if_None()
    assert x_dict.get("penny") == default_penny_if_None()
    assert x_dict.get("purviewlogs") == music_deal._get_purviewlogs_dict()
    print(f"{ music_deal._get_purviewlogs_dict()=}")
    assert list(x_dict.keys()) == [
        "deal_id",
        "timeline",
        "current_time",
        "purviewlogs",
        "wall",
        "fund_coin",
        "respect_bit",
        "penny",
    ]


def test_DealUnit_get_json_ReturnsObj():
    # ESTABLISH
    music_str = "music"
    music_deal = dealunit_shop(music_str, get_test_deals_dir())
    bob_str = "Bob"
    bob_x0_time_id = 702
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_time_id = 4
    sue_x4_magnitude = 55
    sue_x7_time_id = 7
    sue_x7_magnitude = 66
    music_deal.add_purviewepisode(bob_str, bob_x0_time_id, bob_x0_magnitude)
    music_deal.add_purviewepisode(sue_str, sue_x4_time_id, sue_x4_magnitude)
    music_deal.add_purviewepisode(sue_str, sue_x7_time_id, sue_x7_magnitude)

    # WHEN
    x_json = music_deal.get_json()

    # THEN
    print(f"{x_json=}")
    assert x_json
    assert x_json.find("deal_id") > 0


def test_get_from_dict_ReturnsDealUnit():
    # ESTABLISH
    music_str = "music"
    music_deal = dealunit_shop(music_str)
    sue_timeline_lx = "sue casa"
    music_deal.timeline.timeline_lx = sue_timeline_lx
    sue_current_time = 23
    sue_wall = "/"
    sue_fund_coin = 0.3
    sue_respect_bit = 0.5
    sue_penny = 0.8
    bob_str = "Bob"
    bob_x0_time_id = 702
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_time_id = 4
    sue_x4_magnitude = 55
    sue_x7_time_id = 7
    sue_x7_magnitude = 66
    music_deal.add_purviewepisode(bob_str, bob_x0_time_id, bob_x0_magnitude)
    music_deal.add_purviewepisode(sue_str, sue_x4_time_id, sue_x4_magnitude)
    music_deal.add_purviewepisode(sue_str, sue_x7_time_id, sue_x7_magnitude)
    music_deal.current_time = sue_current_time
    music_deal.wall = sue_wall
    music_deal.fund_coin = sue_fund_coin
    music_deal.respect_bit = sue_respect_bit
    music_deal.penny = sue_penny
    x_dict = music_deal.get_dict()

    # WHEN
    x_deal = dealunit_get_from_dict(x_dict)

    # THEN
    assert x_deal.deal_id == music_str
    assert x_deal.timeline.timeline_lx == sue_timeline_lx
    assert x_deal.current_time == sue_current_time
    assert x_deal.wall == sue_wall
    assert x_deal.fund_coin == sue_fund_coin
    assert x_deal.respect_bit == sue_respect_bit
    assert x_deal.penny == sue_penny
    assert x_deal.purviewlogs == music_deal.purviewlogs
    assert x_deal.deals_dir == music_deal.deals_dir
    assert x_deal == music_deal


def test_get_from_json_ReturnsDealUnit():
    # ESTABLISH
    music_str = "music"
    music_deal = dealunit_shop(music_str)
    sue_timeline_lx = "sue casa"
    music_deal.timeline.timeline_lx = sue_timeline_lx
    sue_current_time = 23
    sue_wall = "/"
    sue_fund_coin = 0.3
    sue_respect_bit = 0.5
    sue_penny = 0.8
    bob_str = "Bob"
    bob_x0_time_id = 702
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_time_id = 4
    sue_x4_magnitude = 55
    sue_x7_time_id = 7
    sue_x7_magnitude = 66
    music_deal.add_purviewepisode(bob_str, bob_x0_time_id, bob_x0_magnitude)
    music_deal.add_purviewepisode(sue_str, sue_x4_time_id, sue_x4_magnitude)
    music_deal.add_purviewepisode(sue_str, sue_x7_time_id, sue_x7_magnitude)
    music_deal.current_time = sue_current_time
    music_deal.wall = sue_wall
    music_deal.fund_coin = sue_fund_coin
    music_deal.respect_bit = sue_respect_bit
    music_deal.penny = sue_penny
    music_json = music_deal.get_json()

    # WHEN
    x_deal = dealunit_get_from_json(music_json)

    # THEN
    assert x_deal.deal_id == music_str
    assert x_deal.timeline.timeline_lx == sue_timeline_lx
    assert x_deal.current_time == sue_current_time
    assert x_deal.wall == sue_wall
    assert x_deal.fund_coin == sue_fund_coin
    assert x_deal.respect_bit == sue_respect_bit
    assert x_deal.penny == sue_penny
    assert x_deal.purviewlogs == music_deal.purviewlogs
    assert x_deal.deals_dir == music_deal.deals_dir
    assert x_deal == music_deal
