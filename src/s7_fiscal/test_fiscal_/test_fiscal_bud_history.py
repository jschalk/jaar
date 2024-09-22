from src.s1_road.road import default_road_delimiter_if_none
from src.s1_road.finance import (
    default_fund_coin_if_none,
    default_respect_bit_if_none,
    default_penny_if_none,
)
from src.s3_chrono.chrono import get_default_timeline_config_dict
from src.s3_chrono.bud_event import ownerbudevents_shop
from src.s4_gift.atom_config import fiscal_id_str
from src.s7_fiscal.fiscal import (
    fiscalunit_shop,
    get_from_dict as fiscalunit_get_from_dict,
    get_from_json as fiscalunit_get_from_json,
)
from src.s7_fiscal.examples.fiscal_env import (
    get_test_fiscals_dir,
    env_dir_setup_cleanup,
)


def test_FiscalUnit_set_ownerbudevents_SetsAttr():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    assert music_fiscal.bud_history == {}

    # WHEN
    sue_str = "Sue"
    sue_ownerbudevents = ownerbudevents_shop(sue_str)
    music_fiscal.set_ownerbudevent(sue_ownerbudevents)

    # THEN
    assert music_fiscal.bud_history != {}
    assert music_fiscal.bud_history.get(sue_str) == sue_ownerbudevents


def test_FiscalUnit_ownerbudevents_exists_ReturnsObj():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    sue_str = "Sue"
    assert music_fiscal.ownerbudevents_exists(sue_str) is False

    # WHEN
    sue_ownerbudevents = ownerbudevents_shop(sue_str)
    music_fiscal.set_ownerbudevent(sue_ownerbudevents)

    # THEN
    assert music_fiscal.ownerbudevents_exists(sue_str)


def test_FiscalUnit_get_ownerbudevents_ReturnsObj():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    sue_str = "Sue"
    sue_ownerbudevents = ownerbudevents_shop(sue_str)
    music_fiscal.set_ownerbudevent(sue_ownerbudevents)
    assert music_fiscal.ownerbudevents_exists(sue_str)

    # WHEN
    sue_gen_ownerbudevents = music_fiscal.get_ownerbudevents(sue_str)

    # THEN
    assert sue_ownerbudevents
    assert sue_ownerbudevents == sue_gen_ownerbudevents


def test_FiscalUnit_del_ownerbudevents_SetsAttr():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    sue_str = "Sue"
    sue_ownerbudevents = ownerbudevents_shop(sue_str)
    music_fiscal.set_ownerbudevent(sue_ownerbudevents)
    assert music_fiscal.ownerbudevents_exists(sue_str)

    # WHEN
    music_fiscal.del_ownerbudevents(sue_str)

    # THEN
    assert music_fiscal.ownerbudevents_exists(sue_str) is False


def test_FiscalUnit_add_ownerbudevent_SetsAttr():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    assert music_fiscal.bud_history == {}

    # WHEN
    bob_str = "Bob"
    bob_x0_timestamp = 702
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_timestamp = 4
    sue_x4_magnitude = 55
    sue_x7_timestamp = 7
    sue_x7_magnitude = 66
    music_fiscal.add_ownerbudevent(bob_str, bob_x0_timestamp, bob_x0_magnitude)
    music_fiscal.add_ownerbudevent(sue_str, sue_x4_timestamp, sue_x4_magnitude)
    music_fiscal.add_ownerbudevent(sue_str, sue_x7_timestamp, sue_x7_magnitude)

    # THEN
    assert music_fiscal.bud_history != {}
    sue_ownerbudevents = ownerbudevents_shop(sue_str)
    sue_ownerbudevents.add_event(sue_x4_timestamp, sue_x4_magnitude)
    sue_ownerbudevents.add_event(sue_x7_timestamp, sue_x7_magnitude)
    bob_ownerbudevents = ownerbudevents_shop(bob_str)
    bob_ownerbudevents.add_event(bob_x0_timestamp, bob_x0_magnitude)
    assert music_fiscal.get_ownerbudevents(sue_str) == sue_ownerbudevents
    assert music_fiscal.get_ownerbudevents(bob_str) == bob_ownerbudevents


def test_FiscalUnit_get_dict_ReturnsObj():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    bob_str = "Bob"
    bob_x0_timestamp = 702
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_timestamp = 4
    sue_x4_magnitude = 55
    sue_x7_timestamp = 7
    sue_x7_magnitude = 66
    music_fiscal.add_ownerbudevent(bob_str, bob_x0_timestamp, bob_x0_magnitude)
    music_fiscal.add_ownerbudevent(sue_str, sue_x4_timestamp, sue_x4_magnitude)
    music_fiscal.add_ownerbudevent(sue_str, sue_x7_timestamp, sue_x7_magnitude)

    # WHEN
    x_dict = music_fiscal.get_dict()

    # THEN
    assert x_dict.get(fiscal_id_str()) == music_str
    assert x_dict.get("timeline") == get_default_timeline_config_dict()
    assert x_dict.get("current_time") == 0
    assert x_dict.get("road_delimiter") == default_road_delimiter_if_none()
    assert x_dict.get("fund_coin") == default_fund_coin_if_none()
    assert x_dict.get("respect_bit") == default_respect_bit_if_none()
    assert x_dict.get("penny") == default_penny_if_none()
    assert x_dict.get("bud_history") == music_fiscal._get_bud_history_dict()
    print(f"{ music_fiscal._get_bud_history_dict()=}")
    assert list(x_dict.keys()) == [
        "fiscal_id",
        "timeline",
        "current_time",
        "bud_history",
        "road_delimiter",
        "fund_coin",
        "respect_bit",
        "penny",
    ]


def test_FiscalUnit_get_json_ReturnsObj():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    bob_str = "Bob"
    bob_x0_timestamp = 702
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_timestamp = 4
    sue_x4_magnitude = 55
    sue_x7_timestamp = 7
    sue_x7_magnitude = 66
    music_fiscal.add_ownerbudevent(bob_str, bob_x0_timestamp, bob_x0_magnitude)
    music_fiscal.add_ownerbudevent(sue_str, sue_x4_timestamp, sue_x4_magnitude)
    music_fiscal.add_ownerbudevent(sue_str, sue_x7_timestamp, sue_x7_magnitude)

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
    sue_road_delimiter = "/"
    sue_fund_coin = 0.3
    sue_respect_bit = 0.5
    sue_penny = 0.8
    bob_str = "Bob"
    bob_x0_timestamp = 702
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_timestamp = 4
    sue_x4_magnitude = 55
    sue_x7_timestamp = 7
    sue_x7_magnitude = 66
    music_fiscal.add_ownerbudevent(bob_str, bob_x0_timestamp, bob_x0_magnitude)
    music_fiscal.add_ownerbudevent(sue_str, sue_x4_timestamp, sue_x4_magnitude)
    music_fiscal.add_ownerbudevent(sue_str, sue_x7_timestamp, sue_x7_magnitude)
    music_fiscal.current_time = sue_current_time
    music_fiscal._road_delimiter = sue_road_delimiter
    music_fiscal._fund_coin = sue_fund_coin
    music_fiscal._respect_bit = sue_respect_bit
    music_fiscal._penny = sue_penny
    x_dict = music_fiscal.get_dict()

    # WHEN
    x_fiscal = fiscalunit_get_from_dict(x_dict)

    # THEN
    assert x_fiscal.fiscal_id == music_str
    assert x_fiscal.timeline.timeline_label == sue_timeline_label
    assert x_fiscal.current_time == sue_current_time
    assert x_fiscal._road_delimiter == sue_road_delimiter
    assert x_fiscal._fund_coin == sue_fund_coin
    assert x_fiscal._respect_bit == sue_respect_bit
    assert x_fiscal._penny == sue_penny
    assert x_fiscal.bud_history == music_fiscal.bud_history
    assert x_fiscal.fiscals_dir == music_fiscal.fiscals_dir
    assert x_fiscal == music_fiscal


def test_get_from_json_ReturnsFiscalUnit():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str)
    sue_timeline_label = "sue casa"
    music_fiscal.timeline.timeline_label = sue_timeline_label
    sue_current_time = 23
    sue_road_delimiter = "/"
    sue_fund_coin = 0.3
    sue_respect_bit = 0.5
    sue_penny = 0.8
    bob_str = "Bob"
    bob_x0_timestamp = 702
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_timestamp = 4
    sue_x4_magnitude = 55
    sue_x7_timestamp = 7
    sue_x7_magnitude = 66
    music_fiscal.add_ownerbudevent(bob_str, bob_x0_timestamp, bob_x0_magnitude)
    music_fiscal.add_ownerbudevent(sue_str, sue_x4_timestamp, sue_x4_magnitude)
    music_fiscal.add_ownerbudevent(sue_str, sue_x7_timestamp, sue_x7_magnitude)
    music_fiscal.current_time = sue_current_time
    music_fiscal._road_delimiter = sue_road_delimiter
    music_fiscal._fund_coin = sue_fund_coin
    music_fiscal._respect_bit = sue_respect_bit
    music_fiscal._penny = sue_penny
    music_json = music_fiscal.get_json()

    # WHEN
    x_fiscal = fiscalunit_get_from_json(music_json)

    # THEN
    assert x_fiscal.fiscal_id == music_str
    assert x_fiscal.timeline.timeline_label == sue_timeline_label
    assert x_fiscal.current_time == sue_current_time
    assert x_fiscal._road_delimiter == sue_road_delimiter
    assert x_fiscal._fund_coin == sue_fund_coin
    assert x_fiscal._respect_bit == sue_respect_bit
    assert x_fiscal._penny == sue_penny
    assert x_fiscal.bud_history == music_fiscal.bud_history
    assert x_fiscal.fiscals_dir == music_fiscal.fiscals_dir
    assert x_fiscal == music_fiscal
