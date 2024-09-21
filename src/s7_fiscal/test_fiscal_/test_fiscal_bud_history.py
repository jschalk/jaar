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
