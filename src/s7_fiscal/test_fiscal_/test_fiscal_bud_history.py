from src.s3_chrono.bud_event import ownerbudevents_shop
from src.s7_fiscal.fiscal import fiscalunit_shop
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


def test_FiscalUnit_get_ownerbudevents_dict_ReturnsObj():
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
    x_ownerbudevents_dict = music_fiscal.get_ownerbudevents_dict()

    # THEN
    assert x_ownerbudevents_dict == {
        "fiscal_id": music_str,
        "ownerbudevents": {
            sue_str: {
                "owner_id": sue_str,
                "events": {
                    sue_x4_timestamp: {"money_magnitude": sue_x4_magnitude},
                    sue_x7_timestamp: {"money_magnitude": sue_x7_magnitude},
                },
            },
            bob_str: {
                "owner_id": bob_str,
                "events": {bob_x0_timestamp: {"money_magnitude": bob_x0_magnitude}},
            },
        },
    }
