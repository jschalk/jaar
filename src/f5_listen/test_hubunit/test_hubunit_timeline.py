from src.f1_road.finance import default_fund_pool
from src.f5_listen.hubunit import hubunit_shop
from src.f5_listen.examples.example_listen_buds import (
    get_budunit_with_4_levels,
    get_budunit_irrational_example,
    get_budunit_3_acct,
)
from src.f5_listen.examples.example_listen_outlays import (
    get_outlayepisode_55_example,
    get_outlayepisode_66_example,
    get_outlayepisode_88_example,
    get_outlayepisode_invalid_example,
)
from src.f5_listen.examples.listen_env import (
    get_listen_temp_env_dir as fiscals_dir,
    get_default_fiscal_id_roadnode as fiscal_id,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists
from pytest import raises as pytest_raises


def test_HubUnit_timepoint_dir_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t88_timestamp = 8800

    # WHEN
    one_timepoint_dir = yao_hubunit.timepoint_dir(t88_timestamp)

    # THEN
    assert one_timepoint_dir == f"{yao_hubunit.timeline_dir()}/{t88_timestamp}"


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
        f"{yao_hubunit.timepoint_dir(t88_timestamp)}/{yao_hubunit.outlay_file_name()}"
    )
    assert t88_outlay_file_path == x_file_path


def test_HubUnit_save_valid_outlay_file_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t55_outlay = get_outlayepisode_55_example()
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
    t_outlay = get_outlayepisode_invalid_example()

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yao_hubunit._save_valid_outlay_file(t_outlay)
    exception_text = "magnitude cannot be calculated: debt_outlay=-5, cred_outlay=3"
    assert str(excinfo.value) == exception_text


def test_HubUnit_outlay_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t55_outlay = get_outlayepisode_55_example()
    t55_timestamp = t55_outlay.timestamp
    assert yao_hubunit.outlay_file_exists(t55_timestamp) is False

    # WHEN
    yao_hubunit._save_valid_outlay_file(t55_outlay)

    # THEN
    assert yao_hubunit.outlay_file_exists(t55_timestamp)


def test_HubUnit_get_outlay_file_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t55_outlay = get_outlayepisode_55_example()
    t55_timestamp = t55_outlay.timestamp
    yao_hubunit._save_valid_outlay_file(t55_outlay)
    assert yao_hubunit.outlay_file_exists(t55_timestamp)

    # WHEN / THEN
    assert yao_hubunit.get_outlay_file(t55_timestamp) == t55_outlay


def test_HubUnit_delete_outlay_file_DeletesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t55_outlay = get_outlayepisode_55_example()
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
    t55_outlay = get_outlayepisode_55_example()
    t66_outlay = get_outlayepisode_66_example()
    t55_timestamp = t55_outlay.timestamp
    t66_timestamp = t66_outlay.timestamp
    yao_hubunit._save_valid_outlay_file(t55_outlay)
    assert yao_hubunit.get_outlaylog().episode_exists(t55_timestamp)
    assert yao_hubunit.get_outlaylog().episode_exists(t66_timestamp) is False
    yao_hubunit._save_valid_outlay_file(t66_outlay)

    # WHEN / THEN
    assert yao_hubunit.get_outlaylog().episode_exists(t55_timestamp)
    assert yao_hubunit.get_outlaylog().episode_exists(t66_timestamp)
    assert yao_hubunit.get_outlaylog().get_episode(t66_timestamp).get_net_outlay("Sue")


def test_HubUnit_budpoint_file_name_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)

    # WHEN
    x_outlay_file_name = yao_hubunit.budpoint_file_name()

    # THEN
    assert x_outlay_file_name == "budpoint.json"


def test_HubUnit_budpoint_file_path_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t88_timestamp = 8800

    # WHEN
    t88_budpoint_file_path = yao_hubunit.budpoint_file_path(t88_timestamp)

    # THEN
    x_file_path = (
        f"{yao_hubunit.timepoint_dir(t88_timestamp)}/{yao_hubunit.budpoint_file_name()}"
    )
    assert t88_budpoint_file_path == x_file_path


def test_HubUnit_save_valid_budpoint_file_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t55_budpoint = get_budunit_with_4_levels()
    t55_timestamp = 55
    assert os_path_exists(yao_hubunit.budpoint_file_path(t55_timestamp)) is False

    # WHEN
    yao_hubunit._save_valid_budpoint_file(t55_timestamp, t55_budpoint)

    # THEN
    assert os_path_exists(yao_hubunit.budpoint_file_path(t55_timestamp))


def test_HubUnit_save_valid_budpoint_file_RaisesError(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t_budpoint = get_budunit_irrational_example()
    t55_timestamp = 55

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yao_hubunit._save_valid_budpoint_file(t55_timestamp, t_budpoint)
    exception_text = "BudPoint could not be saved BudUnit._rational is False"
    assert str(excinfo.value) == exception_text


def test_HubUnit_budpoint_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t55_timestamp = 55
    assert yao_hubunit.budpoint_file_exists(t55_timestamp) is False

    # WHEN
    t55_budpoint = get_budunit_with_4_levels()
    yao_hubunit._save_valid_budpoint_file(t55_timestamp, t55_budpoint)

    # THEN
    assert yao_hubunit.budpoint_file_exists(t55_timestamp)


def test_HubUnit_get_budpoint_file_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t55_timestamp = 55
    t55_budpoint = get_budunit_with_4_levels()
    yao_hubunit._save_valid_budpoint_file(t55_timestamp, t55_budpoint)
    assert yao_hubunit.budpoint_file_exists(t55_timestamp)

    # WHEN
    file_budpoint = yao_hubunit.get_budpoint_file(t55_timestamp)

    # THEN
    assert file_budpoint.get_dict() == t55_budpoint.get_dict()


def test_HubUnit_delete_budpoint_file_DeletesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t55_timestamp = 55
    t55_budpoint = get_budunit_with_4_levels()
    yao_hubunit._save_valid_budpoint_file(t55_timestamp, t55_budpoint)
    assert yao_hubunit.budpoint_file_exists(t55_timestamp)

    # WHEN
    yao_hubunit.delete_budpoint_file(t55_timestamp)

    # THEN
    assert yao_hubunit.budpoint_file_exists(t55_timestamp) is False


def test_HubUnit_calc_timepoint_outlay_Sets_outlay_file_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    t55_timestamp = 55
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    yao_hubunit._save_valid_budpoint_file(t55_timestamp, get_budunit_3_acct())
    assert yao_hubunit.budpoint_file_exists(t55_timestamp)
    assert yao_hubunit.outlay_file_exists(t55_timestamp) is False

    # WHEN
    yao_hubunit.calc_timepoint_outlay(t55_timestamp)

    # THEN
    assert yao_hubunit.budpoint_file_exists(t55_timestamp)
    assert yao_hubunit.outlay_file_exists(t55_timestamp)
    t55_outlay = yao_hubunit.get_outlay_file(t55_timestamp)
    assert t55_outlay.timestamp == t55_timestamp
    assert t55_outlay.purview == default_fund_pool()
    assert t55_outlay._magnitude == 283333333
    assert t55_outlay.get_net_outlay("Sue") == 77380952
    assert t55_outlay.get_net_outlay("Yao") == -283333333
    assert t55_outlay.get_net_outlay("Zia") == 205952381


def test_HubUnit_calc_timepoint_outlay_Sets_outlay_file_Scenario1(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    t88_outlay = get_outlayepisode_88_example()
    t88_timestamp = t88_outlay.timestamp
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    yao_hubunit._save_valid_budpoint_file(t88_timestamp, get_budunit_3_acct())
    yao_hubunit._save_valid_outlay_file(t88_outlay)
    assert yao_hubunit.budpoint_file_exists(t88_timestamp)
    assert yao_hubunit.outlay_file_exists(t88_timestamp)
    before_t88_outlay = yao_hubunit.get_outlay_file(t88_timestamp)
    assert before_t88_outlay.timestamp == t88_timestamp
    assert before_t88_outlay.purview == 800
    assert before_t88_outlay._magnitude == 0
    assert not before_t88_outlay.get_net_outlay("Sue")
    assert not before_t88_outlay.get_net_outlay("Yao")
    assert not before_t88_outlay.get_net_outlay("Zia")

    # WHEN
    yao_hubunit.calc_timepoint_outlay(t88_timestamp)

    # THEN
    assert yao_hubunit.budpoint_file_exists(t88_timestamp)
    yao_budpoint = yao_hubunit.get_budpoint_file(t88_timestamp)
    assert yao_hubunit.outlay_file_exists(t88_timestamp)
    after_t88_outlay = yao_hubunit.get_outlay_file(t88_timestamp)
    assert after_t88_outlay.timestamp == t88_timestamp
    assert after_t88_outlay.purview == 800
    assert after_t88_outlay.purview == yao_budpoint.fund_pool
    assert after_t88_outlay.get_net_outlay("Sue") == 62
    assert after_t88_outlay.get_net_outlay("Yao") == -227
    assert after_t88_outlay.get_net_outlay("Zia") == 165
    assert after_t88_outlay._magnitude == 227


def test_HubUnit_calc_timepoint_outlay_RaisesException(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    t88_outlay = get_outlayepisode_88_example()
    t88_timestamp = t88_outlay.timestamp
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    yao_hubunit._save_valid_outlay_file(t88_outlay)
    assert yao_hubunit.budpoint_file_exists(t88_timestamp) is False
    assert yao_hubunit.outlay_file_exists(t88_timestamp)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_hubunit.calc_timepoint_outlay(t88_timestamp)
    exception_str = f"Cannot calculate timepoint {t88_timestamp} outlays without saved BudPoint file"
    assert str(excinfo.value) == exception_str


def test_HubUnit_calc_timepoint_outlays_Sets_outlay_files_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    t66_outlay = get_outlayepisode_66_example()
    t88_outlay = get_outlayepisode_88_example()
    t66_timestamp = t66_outlay.timestamp
    t88_timestamp = t88_outlay.timestamp
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    yao_hubunit._save_valid_budpoint_file(t66_timestamp, get_budunit_3_acct())
    yao_hubunit._save_valid_budpoint_file(t88_timestamp, get_budunit_3_acct())
    yao_hubunit._save_valid_outlay_file(t66_outlay)
    yao_hubunit._save_valid_outlay_file(t88_outlay)
    assert yao_hubunit.budpoint_file_exists(t66_timestamp)
    assert yao_hubunit.budpoint_file_exists(t88_timestamp)
    assert yao_hubunit.outlay_file_exists(t66_timestamp)
    assert yao_hubunit.outlay_file_exists(t88_timestamp)
    before_t66_outlay = yao_hubunit.get_outlay_file(t66_timestamp)
    assert before_t66_outlay.timestamp == t66_timestamp
    assert before_t66_outlay.purview == default_fund_pool()
    assert before_t66_outlay._magnitude == 5
    assert before_t66_outlay.get_net_outlay("Sue") == -5
    assert not before_t66_outlay.get_net_outlay("Yao")
    assert not before_t66_outlay.get_net_outlay("Zia")
    before_t88_outlay = yao_hubunit.get_outlay_file(t88_timestamp)
    assert before_t88_outlay.timestamp == t88_timestamp
    assert before_t88_outlay.purview == 800
    assert before_t88_outlay._magnitude == 0
    assert not before_t88_outlay.get_net_outlay("Sue")
    assert not before_t88_outlay.get_net_outlay("Yao")
    assert not before_t88_outlay.get_net_outlay("Zia")

    # WHEN
    yao_hubunit.calc_timepoint_outlays()

    # THEN
    assert yao_hubunit.budpoint_file_exists(t88_timestamp)
    yao_budpoint = yao_hubunit.get_budpoint_file(t88_timestamp)
    assert yao_hubunit.outlay_file_exists(t88_timestamp)
    after_t88_outlay = yao_hubunit.get_outlay_file(t88_timestamp)
    assert after_t88_outlay.timestamp == t88_timestamp
    assert after_t88_outlay.purview == 800
    assert after_t88_outlay.purview == yao_budpoint.fund_pool
    assert after_t88_outlay.get_net_outlay("Sue") == 62
    assert after_t88_outlay.get_net_outlay("Yao") == -227
    assert after_t88_outlay.get_net_outlay("Zia") == 165
    assert after_t88_outlay._magnitude == 227
    after_t66_outlay = yao_hubunit.get_outlay_file(t66_timestamp)
    assert after_t66_outlay.timestamp == t66_timestamp
    assert after_t66_outlay.purview == default_fund_pool()
    assert after_t66_outlay.get_net_outlay("Sue") == 77380952
    assert after_t66_outlay.get_net_outlay("Yao") == -283333333
    assert after_t66_outlay.get_net_outlay("Zia") == 205952381
    assert after_t66_outlay._magnitude == 283333333
