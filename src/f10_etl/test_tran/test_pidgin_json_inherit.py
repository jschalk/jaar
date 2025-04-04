from src.f00_instrument.file import create_path, open_file, save_file
from src.f04_vow.atom_config import type_AcctName_str
from src.f08_pidgin.pidgin import pidginunit_shop, get_pidginunit_from_json
from src.f08_pidgin.pidgin_config import pidgin_filename
from src.f10_etl.transformers import (
    etl_pidgin_jsons_inherit_younger_pidgins,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup


def test_etl_pidgin_jsons_inherit_younger_pidgins_Scenario0_TwoPidginUnitFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_str = "Bob"
    event3 = 3
    event7 = 7
    e3_pidginunit = pidginunit_shop(bob_str, event3)
    e7_pidginunit = pidginunit_shop(bob_str, event7)
    sue_otx = "Sue"
    sue_inx = "Suzy"
    e3_pidginunit.set_otx2inx(type_AcctName_str(), sue_otx, sue_inx)
    x_faces_otz_dir = get_test_etl_dir()
    bob_dir = create_path(x_faces_otz_dir, bob_str)
    event3_dir = create_path(bob_dir, event3)
    event7_dir = create_path(bob_dir, event7)
    save_file(event3_dir, pidgin_filename(), e3_pidginunit.get_json())
    save_file(event7_dir, pidgin_filename(), e7_pidginunit.get_json())
    e3_json_file_path = create_path(event3_dir, pidgin_filename())
    e7_json_file_path = create_path(event7_dir, pidgin_filename())
    x_pidgin_events = {bob_str: {event7, event3}}
    before_e3_pidgin = get_pidginunit_from_json(open_file(e3_json_file_path))
    before_e7_pidgin = get_pidginunit_from_json(open_file(e7_json_file_path))
    assert before_e3_pidgin == e3_pidginunit
    assert before_e7_pidgin == e7_pidginunit
    assert (
        before_e7_pidgin.otx2inx_exists(type_AcctName_str(), sue_otx, sue_inx) is False
    )

    # WHEN
    etl_pidgin_jsons_inherit_younger_pidgins(x_faces_otz_dir, x_pidgin_events)

    # THEN
    after_e3_pidgin = get_pidginunit_from_json(open_file(e3_json_file_path))
    after_e7_pidgin = get_pidginunit_from_json(open_file(e7_json_file_path))
    assert after_e3_pidgin == before_e3_pidgin
    assert after_e7_pidgin != before_e7_pidgin
    assert after_e7_pidgin.otx2inx_exists(type_AcctName_str(), sue_otx, sue_inx)
