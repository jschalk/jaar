from src.s0_instrument.file import dir_files as file_dir_files
from src.s5_listen.hubunit import hubunit_shop
from src.s5_listen.examples.example_listen_outlays import (
    get_outlayevent_55_example,
    get_outlayevent_66_example,
    get_outlayevent_invalid_example,
)
from src.s5_listen.examples.listen_env import (
    get_listen_temp_env_dir as fiscals_dir,
    get_default_fiscal_id_roadnode as fiscal_id,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists
from pytest import raises as pytest_raises


def test_HubUnit_outlay_dir_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t88_timestamp = 8800

    # WHEN
    one_outlay_dir = yao_hubunit.outlay_dir(t88_timestamp)

    # THEN
    assert one_outlay_dir == f"{yao_hubunit.outlays_dir()}/{t88_timestamp}"


def test_HubUnit_outlay_file_name_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)

    # WHEN
    x_outlay_file_name = yao_hubunit.outlay_file_name()

    # THEN
    assert x_outlay_file_name == "outlay.json"


def test_HubUnit_outlay_file_path_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t88_timestamp = 8800

    # WHEN
    t88_outlay_file_path = yao_hubunit.outlay_file_path(t88_timestamp)

    # THEN
    x_file_path = (
        f"{yao_hubunit.outlay_dir(t88_timestamp)}/{yao_hubunit.outlay_file_name()}"
    )
    assert t88_outlay_file_path == x_file_path


def test_HubUnit_save_valid_outlay_file_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t55_outlay = get_outlayevent_55_example()
    t55_timestamp = t55_outlay.timestamp
    assert os_path_exists(yao_hubunit.outlay_file_path(t55_timestamp)) is False

    # WHEN
    yao_hubunit._save_valid_outlay_file(t55_outlay)

    # THEN
    assert os_path_exists(yao_hubunit.outlay_file_path(t55_timestamp))


def test_HubUnit_save_valid_outlay_file_RaisesError(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t_outlay = get_outlayevent_invalid_example()

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yao_hubunit._save_valid_outlay_file(t_outlay)
    exception_text = "magnitude cannot be calculated: debt_outlay=-5, cred_outlay=3"
    assert str(excinfo.value) == exception_text


def test_HubUnit_outlay_file_exists_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t55_outlay = get_outlayevent_55_example()
    t55_timestamp = t55_outlay.timestamp
    assert yao_hubunit.outlay_file_exists(t55_timestamp) is False

    # WHEN
    yao_hubunit._save_valid_outlay_file(t55_outlay)

    # THEN
    assert yao_hubunit.outlay_file_exists(t55_timestamp)


def test_HubUnit_delete_outlay_file_DeletesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t55_outlay = get_outlayevent_55_example()
    t55_timestamp = t55_outlay.timestamp
    yao_hubunit._save_valid_outlay_file(t55_outlay)
    assert yao_hubunit.outlay_file_exists(t55_timestamp)

    # WHEN
    yao_hubunit.delete_outlay_file(t55_timestamp)

    # THEN
    assert yao_hubunit.outlay_file_exists(t55_timestamp) is False


def test_HubUnit_get_outlaylog_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t55_outlay = get_outlayevent_55_example()
    t66_outlay = get_outlayevent_66_example()
    t55_timestamp = t55_outlay.timestamp
    t66_timestamp = t66_outlay.timestamp
    yao_hubunit._save_valid_outlay_file(t55_outlay)
    assert yao_hubunit.get_outlaylog().event_exists(t55_timestamp)
    assert yao_hubunit.get_outlaylog().event_exists(t66_timestamp) is False
    yao_hubunit._save_valid_outlay_file(t66_outlay)

    # WHEN / THEN
    assert yao_hubunit.get_outlaylog().event_exists(t55_timestamp)
    assert yao_hubunit.get_outlaylog().event_exists(t66_timestamp)
    assert yao_hubunit.get_outlaylog().get_event(t66_timestamp).get_net_outlay("Sue")
