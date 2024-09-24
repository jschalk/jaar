from src.s3_chrono.bud_event import budlog_shop
from src.s7_fiscal.fiscal import fiscalunit_shop
from src.s7_fiscal.examples.fiscal_env import get_test_fiscals_dir


def test_FiscalUnit_set_budlog_SetsAttr():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    assert music_fiscal.bud_history == {}

    # WHEN
    sue_str = "Sue"
    sue_budlog = budlog_shop(sue_str)
    music_fiscal.set_budevent(sue_budlog)

    # THEN
    assert music_fiscal.bud_history != {}
    assert music_fiscal.bud_history.get(sue_str) == sue_budlog


def test_FiscalUnit_budlog_exists_ReturnsObj():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    sue_str = "Sue"
    assert music_fiscal.budlog_exists(sue_str) is False

    # WHEN
    sue_budlog = budlog_shop(sue_str)
    music_fiscal.set_budevent(sue_budlog)

    # THEN
    assert music_fiscal.budlog_exists(sue_str)


def test_FiscalUnit_get_budlog_ReturnsObj():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    sue_str = "Sue"
    sue_budlog = budlog_shop(sue_str)
    music_fiscal.set_budevent(sue_budlog)
    assert music_fiscal.budlog_exists(sue_str)

    # WHEN
    sue_gen_budlog = music_fiscal.get_budlog(sue_str)

    # THEN
    assert sue_budlog
    assert sue_budlog == sue_gen_budlog


def test_FiscalUnit_del_budlog_SetsAttr():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    sue_str = "Sue"
    sue_budlog = budlog_shop(sue_str)
    music_fiscal.set_budevent(sue_budlog)
    assert music_fiscal.budlog_exists(sue_str)

    # WHEN
    music_fiscal.del_budlog(sue_str)

    # THEN
    assert music_fiscal.budlog_exists(sue_str) is False


def test_FiscalUnit_add_budevent_SetsAttr():
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
    music_fiscal.add_budevent(bob_str, bob_x0_timestamp, bob_x0_magnitude)
    music_fiscal.add_budevent(sue_str, sue_x4_timestamp, sue_x4_magnitude)
    music_fiscal.add_budevent(sue_str, sue_x7_timestamp, sue_x7_magnitude)

    # THEN
    assert music_fiscal.bud_history != {}
    sue_budlog = budlog_shop(sue_str)
    sue_budlog.add_event(sue_x4_timestamp, sue_x4_magnitude)
    sue_budlog.add_event(sue_x7_timestamp, sue_x7_magnitude)
    bob_budlog = budlog_shop(bob_str)
    bob_budlog.add_event(bob_x0_timestamp, bob_x0_magnitude)
    assert music_fiscal.get_budlog(sue_str) == sue_budlog
    assert music_fiscal.get_budlog(bob_str) == bob_budlog
