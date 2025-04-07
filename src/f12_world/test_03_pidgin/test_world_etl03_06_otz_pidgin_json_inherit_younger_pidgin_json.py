from src.f00_instrument.file import create_path, open_file, save_file
from src.f04_kick.atom_config import type_NameUnit_str
from src.f09_pidgin.pidgin import pidginunit_shop, get_pidginunit_from_json
from src.f09_pidgin.pidgin_config import pidgin_filename
from src.f12_world.world import worldunit_shop
from src.f12_world.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists
from pathlib import Path


def test_WorldUnit_pidgin_jsons_inherit_younger_pidgins_Scenario0_NoPidginUnitFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    assert fizz_world._pidgin_events == {}
    faces_dir = Path(fizz_world._faces_otz_dir)
    before_files = {f for f in faces_dir.glob("**/*") if f.is_file()}

    # WHEN
    fizz_world.pidgin_jsons_inherit_younger_pidgins()

    # THEN no changes, no errors raised
    assert fizz_world._pidgin_events == {}

    # Verify no files were created or modified
    forecast_files = {f for f in faces_dir.glob("**/*") if f.is_file()}
    state_change_str = "File system state changed during test execution"
    assert before_files == forecast_files, state_change_str


def test_WorldUnit_pidgin_jsons_inherit_younger_pidgins_Scenario1_OnePidginUnitFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    bob_str = "Bob"
    event3 = 3
    e3_pidginunit = pidginunit_shop(bob_str, event3)
    sue_otx = "Sue"
    sue_inx = "Suzy"
    e3_pidginunit.set_otx2inx(type_NameUnit_str(), sue_otx, sue_inx)
    bob_dir = create_path(fizz_world._faces_otz_dir, bob_str)
    event3_dir = create_path(bob_dir, event3)
    save_file(event3_dir, pidgin_filename(), e3_pidginunit.get_json())
    e3_json_file_path = create_path(event3_dir, pidgin_filename())
    assert os_path_exists(e3_json_file_path)
    fizz_world._pidgin_events = {bob_str: {event3}}
    file_e3_pidgin_json = open_file(event3_dir, pidgin_filename())
    assert get_pidginunit_from_json(file_e3_pidgin_json) == e3_pidginunit

    # WHEN
    fizz_world.pidgin_jsons_inherit_younger_pidgins()

    # THEN
    assert get_pidginunit_from_json(file_e3_pidgin_json) == e3_pidginunit


def test_WorldUnit_pidgin_jsons_inherit_younger_pidgins_Scenario2_TwoPidginUnitFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    bob_str = "Bob"
    event3 = 3
    event7 = 7
    e3_pidginunit = pidginunit_shop(bob_str, event3)
    e7_pidginunit = pidginunit_shop(bob_str, event7)
    sue_otx = "Sue"
    sue_inx = "Suzy"
    e3_pidginunit.set_otx2inx(type_NameUnit_str(), sue_otx, sue_inx)
    bob_dir = create_path(fizz_world._faces_otz_dir, bob_str)
    event3_dir = create_path(bob_dir, event3)
    event7_dir = create_path(bob_dir, event7)
    save_file(event3_dir, pidgin_filename(), e3_pidginunit.get_json())
    save_file(event7_dir, pidgin_filename(), e7_pidginunit.get_json())
    e3_json_file_path = create_path(event3_dir, pidgin_filename())
    e7_json_file_path = create_path(event7_dir, pidgin_filename())
    assert os_path_exists(e3_json_file_path)
    assert os_path_exists(e7_json_file_path)
    fizz_world._pidgin_events = {bob_str: {event3, event7}}
    file_e3_pidgin_json = open_file(event3_dir, pidgin_filename())
    file_e7_pidgin_json = open_file(event7_dir, pidgin_filename())
    before_e3_pidgin = get_pidginunit_from_json(file_e3_pidgin_json)
    before_e7_pidgin = get_pidginunit_from_json(file_e7_pidgin_json)
    assert before_e3_pidgin == e3_pidginunit
    assert before_e7_pidgin == e7_pidginunit
    assert (
        before_e7_pidgin.otx2inx_exists(type_NameUnit_str(), sue_otx, sue_inx) is False
    )

    # WHEN
    fizz_world.pidgin_jsons_inherit_younger_pidgins()

    # THEN
    after_e3_pidgin = get_pidginunit_from_json(open_file(e3_json_file_path))
    after_e7_pidgin = get_pidginunit_from_json(open_file(e7_json_file_path))
    assert after_e3_pidgin == before_e3_pidgin
    assert after_e7_pidgin != before_e7_pidgin
    assert after_e7_pidgin.otx2inx_exists(type_NameUnit_str(), sue_otx, sue_inx)
