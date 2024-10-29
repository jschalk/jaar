from src.f01_road.finance_tran import purviewlog_shop
from src.f07_fiscal.fiscal import fiscalunit_shop
from src.f07_fiscal.examples.fiscal_env import get_test_fiscals_dir
from pytest import raises as pytest_raises


def test_FiscalUnit_set_purviewlog_SetsAttr():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    assert music_fiscal.purviewlogs == {}

    # WHEN
    sue_str = "Sue"
    sue_purviewlog = purviewlog_shop(sue_str)
    music_fiscal.set_purviewlog(sue_purviewlog)

    # THEN
    assert music_fiscal.purviewlogs != {}
    assert music_fiscal.purviewlogs.get(sue_str) == sue_purviewlog


def test_FiscalUnit_purviewlog_exists_ReturnsObj():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    sue_str = "Sue"
    assert music_fiscal.purviewlog_exists(sue_str) is False

    # WHEN
    sue_purviewlog = purviewlog_shop(sue_str)
    music_fiscal.set_purviewlog(sue_purviewlog)

    # THEN
    assert music_fiscal.purviewlog_exists(sue_str)


def test_FiscalUnit_get_purviewlog_ReturnsObj():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    sue_str = "Sue"
    sue_purviewlog = purviewlog_shop(sue_str)
    music_fiscal.set_purviewlog(sue_purviewlog)
    assert music_fiscal.purviewlog_exists(sue_str)

    # WHEN
    sue_gen_purviewlog = music_fiscal.get_purviewlog(sue_str)

    # THEN
    assert sue_purviewlog
    assert sue_purviewlog == sue_gen_purviewlog


def test_FiscalUnit_del_purviewlog_SetsAttr():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    sue_str = "Sue"
    sue_purviewlog = purviewlog_shop(sue_str)
    music_fiscal.set_purviewlog(sue_purviewlog)
    assert music_fiscal.purviewlog_exists(sue_str)

    # WHEN
    music_fiscal.del_purviewlog(sue_str)

    # THEN
    assert music_fiscal.purviewlog_exists(sue_str) is False


def test_FiscalUnit_add_purviewepisode_SetsAttr():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    assert music_fiscal.purviewlogs == {}

    # WHEN
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

    # THEN
    assert music_fiscal.purviewlogs != {}
    sue_purviewlog = purviewlog_shop(sue_str)
    sue_purviewlog.add_episode(sue_x4_time_id, sue_x4_magnitude)
    sue_purviewlog.add_episode(sue_x7_time_id, sue_x7_magnitude)
    bob_purviewlog = purviewlog_shop(bob_str)
    bob_purviewlog.add_episode(bob_x0_time_id, bob_x0_magnitude)
    assert music_fiscal.get_purviewlog(sue_str) == sue_purviewlog
    assert music_fiscal.get_purviewlog(bob_str) == bob_purviewlog


def test_FiscalUnit_get_purviewlogs_time_ids_ReturnsObj():
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
    assert music_fiscal.get_purviewlogs_time_ids() == set()

    # WHEN
    music_fiscal.add_purviewepisode(bob_str, bob_x0_time_id, bob_x0_magnitude)
    music_fiscal.add_purviewepisode(sue_str, sue_x4_time_id, sue_x4_magnitude)
    music_fiscal.add_purviewepisode(sue_str, sue_x7_time_id, sue_x7_magnitude)

    # THEN
    all_time_ids = {bob_x0_time_id, sue_x4_time_id, sue_x7_time_id}
    assert music_fiscal.get_purviewlogs_time_ids() == all_time_ids


def test_FiscalUnit_add_purviewepisode_RaisesErrorWhenPurview_time_id_IsLessThan_current_time():
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir())
    music_current_time = 606
    music_fiscal.current_time = music_current_time
    bob_str = "Bob"
    bob_x0_time_id = 707
    bob_x0_magnitude = 33
    sue_str = "Sue"
    sue_x4_time_id = 404
    sue_x4_magnitude = 55
    sue_x7_time_id = 808
    sue_x7_magnitude = 66
    assert music_fiscal.get_purviewlogs_time_ids() == set()
    music_fiscal.add_purviewepisode(bob_str, bob_x0_time_id, bob_x0_magnitude)
    music_fiscal.add_purviewepisode(sue_str, sue_x7_time_id, sue_x7_magnitude)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        music_fiscal.add_purviewepisode(sue_str, sue_x4_time_id, sue_x4_magnitude)
    exception_str = f"Cannot set purviewepisode because time_id {sue_x4_time_id} is less than FiscalUnit.current_time {music_current_time}."
    assert str(excinfo.value) == exception_str
