from src.f01_road.road import default_wall_if_none
from src.f01_road.finance import (
    default_fund_coin_if_none,
    default_respect_bit_if_none,
    default_penny_if_none,
)
from src.f03_chrono.chrono import get_default_timeline_config_dict
from src.f04_gift.atom_config import fiscal_id_str
from src.f07_fiscal.fiscal import (
    fiscalunit_shop,
    get_from_dict as fiscalunit_get_from_dict,
    get_from_json as fiscalunit_get_from_json,
)
from src.f07_fiscal.examples.fiscal_env import (
    get_test_fiscals_dir,
    env_dir_setup_cleanup,
)


def test_FiscalUnit_get_dict_ReturnsObj():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    bob_str = "Bob"
    bob_x0_time_id = 702
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_time_id = 4
    sue_x4_magnitude = 55
    sue_x7_time_id = 7
    sue_x7_magnitude = 66
    music_fiscal.add_purviewepisode(bob_str, bob_x0_time_id, bob_x0_magnitude)
    music_fiscal.add_purviewepisode(sue_str, sue_x4_time_id, sue_x4_magnitude)
    music_fiscal.add_purviewepisode(sue_str, sue_x7_time_id, sue_x7_magnitude)

    # WHEN
    x_dict = music_fiscal.get_dict()

    # THEN
    assert x_dict.get(fiscal_id_str()) == music_str
    assert x_dict.get("timeline") == get_default_timeline_config_dict()
    assert x_dict.get("current_time") == 0
    assert x_dict.get("wall") == default_wall_if_none()
    assert x_dict.get("fund_coin") == default_fund_coin_if_none()
    assert x_dict.get("respect_bit") == default_respect_bit_if_none()
    assert x_dict.get("penny") == default_penny_if_none()
    assert x_dict.get("purviewlogs") == music_fiscal._get_purviewlogs_dict()
    print(f"{ music_fiscal._get_purviewlogs_dict()=}")
    assert list(x_dict.keys()) == [
        "fiscal_id",
        "timeline",
        "current_time",
        "purviewlogs",
        "wall",
        "fund_coin",
        "respect_bit",
        "penny",
    ]


def test_FiscalUnit_get_json_ReturnsObj():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    bob_str = "Bob"
    bob_x0_time_id = 702
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_time_id = 4
    sue_x4_magnitude = 55
    sue_x7_time_id = 7
    sue_x7_magnitude = 66
    music_fiscal.add_purviewepisode(bob_str, bob_x0_time_id, bob_x0_magnitude)
    music_fiscal.add_purviewepisode(sue_str, sue_x4_time_id, sue_x4_magnitude)
    music_fiscal.add_purviewepisode(sue_str, sue_x7_time_id, sue_x7_magnitude)

    # WHEN
    x_json = music_fiscal.get_json()

    # THEN
    print(f"{x_json=}")
    assert x_json
    assert x_json.find("fiscal_id") > 0


def test_get_from_dict_ReturnsFiscalUnit():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str)
    sue_timeline_label = "sue casa"
    music_fiscal.timeline.timeline_label = sue_timeline_label
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
    music_fiscal.add_purviewepisode(bob_str, bob_x0_time_id, bob_x0_magnitude)
    music_fiscal.add_purviewepisode(sue_str, sue_x4_time_id, sue_x4_magnitude)
    music_fiscal.add_purviewepisode(sue_str, sue_x7_time_id, sue_x7_magnitude)
    music_fiscal.current_time = sue_current_time
    music_fiscal.wall = sue_wall
    music_fiscal.fund_coin = sue_fund_coin
    music_fiscal.respect_bit = sue_respect_bit
    music_fiscal.penny = sue_penny
    x_dict = music_fiscal.get_dict()

    # WHEN
    x_fiscal = fiscalunit_get_from_dict(x_dict)

    # THEN
    assert x_fiscal.fiscal_id == music_str
    assert x_fiscal.timeline.timeline_label == sue_timeline_label
    assert x_fiscal.current_time == sue_current_time
    assert x_fiscal.wall == sue_wall
    assert x_fiscal.fund_coin == sue_fund_coin
    assert x_fiscal.respect_bit == sue_respect_bit
    assert x_fiscal.penny == sue_penny
    assert x_fiscal.purviewlogs == music_fiscal.purviewlogs
    assert x_fiscal.fiscals_dir == music_fiscal.fiscals_dir
    assert x_fiscal == music_fiscal


def test_get_from_json_ReturnsFiscalUnit():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str)
    sue_timeline_label = "sue casa"
    music_fiscal.timeline.timeline_label = sue_timeline_label
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
    music_fiscal.add_purviewepisode(bob_str, bob_x0_time_id, bob_x0_magnitude)
    music_fiscal.add_purviewepisode(sue_str, sue_x4_time_id, sue_x4_magnitude)
    music_fiscal.add_purviewepisode(sue_str, sue_x7_time_id, sue_x7_magnitude)
    music_fiscal.current_time = sue_current_time
    music_fiscal.wall = sue_wall
    music_fiscal.fund_coin = sue_fund_coin
    music_fiscal.respect_bit = sue_respect_bit
    music_fiscal.penny = sue_penny
    music_json = music_fiscal.get_json()

    # WHEN
    x_fiscal = fiscalunit_get_from_json(music_json)

    # THEN
    assert x_fiscal.fiscal_id == music_str
    assert x_fiscal.timeline.timeline_label == sue_timeline_label
    assert x_fiscal.current_time == sue_current_time
    assert x_fiscal.wall == sue_wall
    assert x_fiscal.fund_coin == sue_fund_coin
    assert x_fiscal.respect_bit == sue_respect_bit
    assert x_fiscal.penny == sue_penny
    assert x_fiscal.purviewlogs == music_fiscal.purviewlogs
    assert x_fiscal.fiscals_dir == music_fiscal.fiscals_dir
    assert x_fiscal == music_fiscal
