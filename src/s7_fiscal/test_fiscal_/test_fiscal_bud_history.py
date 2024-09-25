from src.s1_road.finance_outlay import outlaylog_shop
from src.s7_fiscal.fiscal import fiscalunit_shop
from src.s7_fiscal.examples.fiscal_env import get_test_fiscals_dir


def test_FiscalUnit_set_outlaylog_SetsAttr():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    assert music_fiscal.bud_history == {}

    # WHEN
    sue_str = "Sue"
    sue_outlaylog = outlaylog_shop(sue_str)
    music_fiscal.set_outlayevent(sue_outlaylog)

    # THEN
    assert music_fiscal.bud_history != {}
    assert music_fiscal.bud_history.get(sue_str) == sue_outlaylog


def test_FiscalUnit_outlaylog_exists_ReturnsObj():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    sue_str = "Sue"
    assert music_fiscal.outlaylog_exists(sue_str) is False

    # WHEN
    sue_outlaylog = outlaylog_shop(sue_str)
    music_fiscal.set_outlayevent(sue_outlaylog)

    # THEN
    assert music_fiscal.outlaylog_exists(sue_str)


def test_FiscalUnit_get_outlaylog_ReturnsObj():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    sue_str = "Sue"
    sue_outlaylog = outlaylog_shop(sue_str)
    music_fiscal.set_outlayevent(sue_outlaylog)
    assert music_fiscal.outlaylog_exists(sue_str)

    # WHEN
    sue_gen_outlaylog = music_fiscal.get_outlaylog(sue_str)

    # THEN
    assert sue_outlaylog
    assert sue_outlaylog == sue_gen_outlaylog


def test_FiscalUnit_del_outlaylog_SetsAttr():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    sue_str = "Sue"
    sue_outlaylog = outlaylog_shop(sue_str)
    music_fiscal.set_outlayevent(sue_outlaylog)
    assert music_fiscal.outlaylog_exists(sue_str)

    # WHEN
    music_fiscal.del_outlaylog(sue_str)

    # THEN
    assert music_fiscal.outlaylog_exists(sue_str) is False


def test_FiscalUnit_add_outlayevent_SetsAttr():
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
    music_fiscal.add_outlayevent(bob_str, bob_x0_timestamp, bob_x0_magnitude)
    music_fiscal.add_outlayevent(sue_str, sue_x4_timestamp, sue_x4_magnitude)
    music_fiscal.add_outlayevent(sue_str, sue_x7_timestamp, sue_x7_magnitude)

    # THEN
    assert music_fiscal.bud_history != {}
    sue_outlaylog = outlaylog_shop(sue_str)
    sue_outlaylog.add_event(sue_x4_timestamp, sue_x4_magnitude)
    sue_outlaylog.add_event(sue_x7_timestamp, sue_x7_magnitude)
    bob_outlaylog = outlaylog_shop(bob_str)
    bob_outlaylog.add_event(bob_x0_timestamp, bob_x0_magnitude)
    assert music_fiscal.get_outlaylog(sue_str) == sue_outlaylog
    assert music_fiscal.get_outlaylog(bob_str) == bob_outlaylog
