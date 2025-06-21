from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path
from src.a20_fis_logic.fis import FisID, FisUnit, fisunit_shop, init_bankunits_from_dirs
from src.a20_fis_logic.test._util.a20_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as fiss_dir,
)


def test_FisID_Exists():
    # ESTABLISH / WHEN / THEN
    assert FisID() == ""
    assert FisID("cookie") == "cookie"


def test_FisUnit_Exists():
    # ESTABLISH / WHEN
    x_fis = FisUnit()

    # THEN
    assert not x_fis.fis_id
    assert not x_fis.fiss_dir
    assert not x_fis.output_dir
    assert not x_fis.fis_time_pnigh
    assert not x_fis._events
    assert not x_fis._syntax_otz_dir
    assert not x_fis._fis_dir
    assert not x_fis._mud_dir
    assert not x_fis._brick_dir
    assert not x_fis._bank_mstr_dir
    assert not x_fis._bankunits
    assert not x_fis._pidgin_events


def test_FisUnit_set_mud_dir_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_fis = FisUnit("fizz")
    x_example_dir = create_path(fiss_dir(), "example_dir")
    x_mud_dir = create_path(x_example_dir, "mud")

    assert not fizz_fis._fis_dir
    assert not fizz_fis._syntax_otz_dir
    assert not fizz_fis._mud_dir
    assert not fizz_fis._brick_dir
    assert not fizz_fis._bank_mstr_dir
    assert os_path_exists(x_mud_dir) is False

    # WHEN
    fizz_fis.set_mud_dir(x_mud_dir)

    # THEN
    assert not fizz_fis._fis_dir
    assert not fizz_fis._syntax_otz_dir
    assert fizz_fis._mud_dir == x_mud_dir
    assert not fizz_fis._brick_dir
    assert not fizz_fis._bank_mstr_dir
    assert os_path_exists(x_mud_dir)


def test_FisUnit_set_fis_dirs_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_fis = FisUnit(fis_id=fizz_str, fiss_dir=fiss_dir())
    x_fis_dir = create_path(fiss_dir(), fizz_str)
    x_syntax_otz_dir = create_path(x_fis_dir, "syntax_otz")
    x_mud_dir = create_path(x_fis_dir, "mud")
    x_brick_dir = create_path(x_fis_dir, "brick")
    x_bank_mstr_dir = create_path(x_fis_dir, "bank_mstr")

    assert not fizz_fis._fis_dir
    assert not fizz_fis._syntax_otz_dir
    assert not fizz_fis._mud_dir
    assert not fizz_fis._brick_dir
    assert not fizz_fis._bank_mstr_dir
    assert os_path_exists(x_fis_dir) is False
    assert os_path_exists(x_syntax_otz_dir) is False
    assert os_path_exists(x_mud_dir) is False
    assert os_path_exists(x_brick_dir) is False
    assert os_path_exists(x_bank_mstr_dir) is False

    # WHEN
    fizz_fis._set_fis_dirs()

    # THEN
    assert fizz_fis._fis_dir == x_fis_dir
    assert fizz_fis._syntax_otz_dir == x_syntax_otz_dir
    assert not fizz_fis._mud_dir
    assert fizz_fis._brick_dir == x_brick_dir
    assert os_path_exists(x_fis_dir)
    assert os_path_exists(x_syntax_otz_dir)
    assert os_path_exists(x_mud_dir) is False
    assert os_path_exists(x_brick_dir)
    assert os_path_exists(x_bank_mstr_dir)


def test_fisunit_shop_ReturnsObj_Scenario0_WithParameters(env_dir_setup_cleanup):
    # ESTABLISH
    fiss2_dir = create_path(fiss_dir(), "fiss2")
    example_mud_dir = create_path(fiss_dir(), "example_mud")
    output_dir = create_path(fiss_dir(), "output")
    five_fis_id = "five"
    fis2_time_pnigh = 55
    fis2_bankunits = {"accord45"}

    # WHEN
    x_fis = fisunit_shop(
        fis_id=five_fis_id,
        fiss_dir=fiss2_dir,
        output_dir=output_dir,
        mud_dir=example_mud_dir,
        fis_time_pnigh=fis2_time_pnigh,
        _bankunits=fis2_bankunits,
    )

    # THEN
    fis_dir = create_path(fiss2_dir, x_fis.fis_id)
    assert x_fis.fis_id == five_fis_id
    assert x_fis.fiss_dir == fiss2_dir
    assert x_fis.output_dir == output_dir
    assert x_fis._mud_dir == example_mud_dir
    assert x_fis.fis_time_pnigh == fis2_time_pnigh
    assert x_fis._events == {}
    assert x_fis._syntax_otz_dir == create_path(fis_dir, "syntax_otz")
    assert x_fis._bankunits == fis2_bankunits
    assert x_fis._pidgin_events == {}


def test_fisunit_shop_ReturnsObj_Scenario1_WithoutParameters(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "accord23"

    # WHEN
    x_fis = fisunit_shop(a23_str, fiss_dir())

    # THEN
    fis_dir = create_path(fiss_dir(), x_fis.fis_id)
    assert x_fis.fis_id == a23_str
    assert x_fis.fiss_dir == fiss_dir()
    assert not x_fis.output_dir
    assert x_fis.fis_time_pnigh == 0
    assert x_fis._events == {}
    assert x_fis._mud_dir == create_path(x_fis._fis_dir, "mud")
    assert x_fis._syntax_otz_dir == create_path(fis_dir, "syntax_otz")
    assert x_fis._bankunits == set()


def test_fisunit_shop_ReturnsObj_Scenario2_ThirdParameterIs_output_dir(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    output_dir = create_path(fiss_dir(), "output")

    # WHEN
    x_fis = fisunit_shop(a23_str, fiss_dir(), output_dir)

    # THEN
    assert x_fis.fis_id == a23_str
    assert x_fis.fiss_dir == fiss_dir()
    assert x_fis.output_dir == output_dir


# def test_FisUnit_popen_event_from_files_ReturnsObj(env_dir_setup_cleanup):
#     # ESTABLISH
#     x_fis = fisunit_shop()
#     sue_str = "Sue"
#     bob_str = "Bob"
#     x_fis.add_pidginunit(sue_str)
#     x_fis.add_pidginunit(bob_str)
#     sue_dir = create_path(x_fis._syntax_otz_dir, sue_str)
#     bob_dir = create_path(x_fis._syntax_otz_dir, bob_str)
#     assert os_path_exists(sue_dir) is False
#     assert os_path_exists(bob_dir) is False

#     # WHEN
#     x_fis.save_pidginunit_files(sue_str)

#     # THEN
#     assert os_path_exists(sue_dir)
#     assert os_path_exists(bob_dir) is False


# def test_FisUnit_save_pidginunit_ChangesFiles(env_dir_setup_cleanup):
#     # ESTABLISH
#     x_fis = fisunit_shop()
#     sue_str = "Sue"
#     bob_str = "Bob"
#     zia_str = "Zia"
#     save_file(x_fis._syntax_otz_dir, sue_str, "temp.txt", "")
#     save_file(x_fis._syntax_otz_dir, bob_str, "temp.txt", "")
#     save_file(x_fis._syntax_otz_dir, zia_str, "temp.txt", "")
#     assert x_fis.pidginunit_exists(sue_str) is False
#     assert x_fis.pidginunit_exists(bob_str) is False
#     assert x_fis.pidginunit_exists(zia_str) is False
#     assert x_fis.pidgins_empty()

#     # WHEN
#     x_fis._set_all_pidginunits_from_dirs()

#     # THEN
#     assert x_fis.pidginunit_exists(sue_str)
#     assert x_fis.pidginunit_exists(bob_str)
#     assert x_fis.pidginunit_exists(zia_str)
#     assert x_fis.pidgins_empty() is False

#     # WHEN
#     delete_dir(x_fis._syntax_otz_dir, zia_str)
#     x_fis._set_all_pidginunits_from_dirs()

#     # THEN
#     assert x_fis.pidginunit_exists(sue_str)
#     assert x_fis.pidginunit_exists(bob_str)
#     assert x_fis.pidginunit_exists(zia_str) is False
#     assert x_fis.pidgins_empty() is False


def test_init_bankunits_from_dirs_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = fiss_dir()

    # WHEN
    x_bankunits = init_bankunits_from_dirs([])

    # THEN
    assert x_bankunits == []


def test_FisUnit_set_event_SetsAttr_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    x_fis = fisunit_shop("accord23", fiss_dir())
    assert x_fis._events == {}

    # WHEN
    e5_event_int = 5
    e5_face_name = "Sue"
    x_fis.set_event(e5_event_int, e5_face_name)

    # THEN
    assert x_fis._events != {}
    assert x_fis._events == {e5_event_int: e5_face_name}


def test_FisUnit_event_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_fis = fisunit_shop("accord23", fiss_dir())
    e5_event_int = 5
    e5_face_name = "Sue"
    assert x_fis.event_exists(e5_event_int) is False

    # WHEN
    x_fis.set_event(e5_event_int, e5_face_name)

    # THEN
    assert x_fis.event_exists(e5_event_int)


def test_FisUnit_get_event_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_fis = fisunit_shop("accord23", fiss_dir())
    e5_event_int = 5
    e5_face_name = "Sue"
    assert x_fis.get_event(e5_event_int) is None

    # WHEN
    x_fis.set_event(e5_event_int, e5_face_name)

    # THEN
    assert x_fis.get_event(e5_event_int) == e5_face_name


def test_FisUnit_get_db_path_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    a23_fis = fisunit_shop("accord23", fiss_dir())

    # WHEN
    a23_db_path = a23_fis.get_db_path()

    assert a23_db_path == create_path(a23_fis._fis_dir, "fis.db")
