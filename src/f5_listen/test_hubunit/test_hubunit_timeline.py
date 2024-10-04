from src.f1_road.finance import default_fund_pool
from src.f5_listen.hubunit import hubunit_shop
from src.f5_listen.examples.example_listen_buds import (
    get_budunit_with_4_levels,
    get_budunit_irrational_example,
    get_budunit_3_acct,
)
from src.f5_listen.examples.example_listen_purviews import (
    get_purviewepisode_55_example,
    get_purviewepisode_66_example,
    get_purviewepisode_88_example,
    get_purviewepisode_invalid_example,
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


def test_HubUnit_purview_file_name_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)

    # WHEN
    x_purview_file_name = yao_hubunit.purview_file_name()

    # THEN
    assert x_purview_file_name == "purview.json"


def test_HubUnit_purview_file_path_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t88_timestamp = 8800

    # WHEN
    t88_purview_file_path = yao_hubunit.purview_file_path(t88_timestamp)

    # THEN
    x_file_path = (
        f"{yao_hubunit.timepoint_dir(t88_timestamp)}/{yao_hubunit.purview_file_name()}"
    )
    assert t88_purview_file_path == x_file_path


def test_HubUnit_save_valid_purview_file_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t55_purview = get_purviewepisode_55_example()
    t55_timestamp = t55_purview.timestamp
    assert os_path_exists(yao_hubunit.purview_file_path(t55_timestamp)) is False

    # WHEN
    yao_hubunit._save_valid_purview_file(t55_purview)

    # THEN
    assert os_path_exists(yao_hubunit.purview_file_path(t55_timestamp))


def test_HubUnit_save_valid_purview_file_RaisesError(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t_purview = get_purviewepisode_invalid_example()

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yao_hubunit._save_valid_purview_file(t_purview)
    exception_str = "magnitude cannot be calculated: debt_purview=-5, cred_purview=3"
    assert str(excinfo.value) == exception_str


def test_HubUnit_purview_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t55_purview = get_purviewepisode_55_example()
    t55_timestamp = t55_purview.timestamp
    assert yao_hubunit.purview_file_exists(t55_timestamp) is False

    # WHEN
    yao_hubunit._save_valid_purview_file(t55_purview)

    # THEN
    assert yao_hubunit.purview_file_exists(t55_timestamp)


def test_HubUnit_get_purview_file_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t55_purview = get_purviewepisode_55_example()
    t55_timestamp = t55_purview.timestamp
    yao_hubunit._save_valid_purview_file(t55_purview)
    assert yao_hubunit.purview_file_exists(t55_timestamp)

    # WHEN / THEN
    assert yao_hubunit.get_purview_file(t55_timestamp) == t55_purview


def test_HubUnit_delete_purview_file_DeletesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t55_purview = get_purviewepisode_55_example()
    t55_timestamp = t55_purview.timestamp
    yao_hubunit._save_valid_purview_file(t55_purview)
    assert yao_hubunit.purview_file_exists(t55_timestamp)

    # WHEN
    yao_hubunit.delete_purview_file(t55_timestamp)

    # THEN
    assert yao_hubunit.purview_file_exists(t55_timestamp) is False


def test_HubUnit_get_purviewlog_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    t55_purview = get_purviewepisode_55_example()
    t66_purview = get_purviewepisode_66_example()
    t55_timestamp = t55_purview.timestamp
    t66_timestamp = t66_purview.timestamp
    yao_hubunit._save_valid_purview_file(t55_purview)
    assert yao_hubunit.get_purviewlog().episode_exists(t55_timestamp)
    assert yao_hubunit.get_purviewlog().episode_exists(t66_timestamp) is False
    yao_hubunit._save_valid_purview_file(t66_purview)

    # WHEN / THEN
    assert yao_hubunit.get_purviewlog().episode_exists(t55_timestamp)
    assert yao_hubunit.get_purviewlog().episode_exists(t66_timestamp)
    assert (
        yao_hubunit.get_purviewlog().get_episode(t66_timestamp).get_net_purview("Sue")
    )


def test_HubUnit_budpoint_file_name_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)

    # WHEN
    x_purview_file_name = yao_hubunit.budpoint_file_name()

    # THEN
    assert x_purview_file_name == "budpoint.json"


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
    exception_str = "BudPoint could not be saved BudUnit._rational is False"
    assert str(excinfo.value) == exception_str


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


def test_HubUnit_calc_timepoint_purview_Sets_purview_file_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    t55_timestamp = 55
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    yao_hubunit._save_valid_budpoint_file(t55_timestamp, get_budunit_3_acct())
    assert yao_hubunit.budpoint_file_exists(t55_timestamp)
    assert yao_hubunit.purview_file_exists(t55_timestamp) is False

    # WHEN
    yao_hubunit.calc_timepoint_purview(t55_timestamp)

    # THEN
    assert yao_hubunit.budpoint_file_exists(t55_timestamp)
    assert yao_hubunit.purview_file_exists(t55_timestamp)
    t55_purview = yao_hubunit.get_purview_file(t55_timestamp)
    assert t55_purview.timestamp == t55_timestamp
    assert t55_purview.amount == default_fund_pool()
    assert t55_purview._magnitude == 283333333
    assert t55_purview.get_net_purview("Sue") == 77380952
    assert t55_purview.get_net_purview("Yao") == -283333333
    assert t55_purview.get_net_purview("Zia") == 205952381


def test_HubUnit_calc_timepoint_purview_Sets_purview_file_Scenario1(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    t88_purview = get_purviewepisode_88_example()
    t88_timestamp = t88_purview.timestamp
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    yao_hubunit._save_valid_budpoint_file(t88_timestamp, get_budunit_3_acct())
    yao_hubunit._save_valid_purview_file(t88_purview)
    assert yao_hubunit.budpoint_file_exists(t88_timestamp)
    assert yao_hubunit.purview_file_exists(t88_timestamp)
    before_t88_purview = yao_hubunit.get_purview_file(t88_timestamp)
    assert before_t88_purview.timestamp == t88_timestamp
    assert before_t88_purview.amount == 800
    assert before_t88_purview._magnitude == 0
    assert not before_t88_purview.get_net_purview("Sue")
    assert not before_t88_purview.get_net_purview("Yao")
    assert not before_t88_purview.get_net_purview("Zia")

    # WHEN
    yao_hubunit.calc_timepoint_purview(t88_timestamp)

    # THEN
    assert yao_hubunit.budpoint_file_exists(t88_timestamp)
    yao_budpoint = yao_hubunit.get_budpoint_file(t88_timestamp)
    assert yao_hubunit.purview_file_exists(t88_timestamp)
    after_t88_purview = yao_hubunit.get_purview_file(t88_timestamp)
    assert after_t88_purview.timestamp == t88_timestamp
    assert after_t88_purview.amount == 800
    assert after_t88_purview.amount == yao_budpoint.fund_pool
    assert after_t88_purview.get_net_purview("Sue") == 62
    assert after_t88_purview.get_net_purview("Yao") == -227
    assert after_t88_purview.get_net_purview("Zia") == 165
    assert after_t88_purview._magnitude == 227


def test_HubUnit_calc_timepoint_purview_RaisesException(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    t88_purview = get_purviewepisode_88_example()
    t88_timestamp = t88_purview.timestamp
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    yao_hubunit._save_valid_purview_file(t88_purview)
    assert yao_hubunit.budpoint_file_exists(t88_timestamp) is False
    assert yao_hubunit.purview_file_exists(t88_timestamp)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_hubunit.calc_timepoint_purview(t88_timestamp)
    exception_str = f"Cannot calculate timepoint {t88_timestamp} purviews without saved BudPoint file"
    assert str(excinfo.value) == exception_str


def test_HubUnit_calc_timepoint_purviews_Sets_purview_files_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    t66_purview = get_purviewepisode_66_example()
    t88_purview = get_purviewepisode_88_example()
    t66_timestamp = t66_purview.timestamp
    t88_timestamp = t88_purview.timestamp
    yao_hubunit = hubunit_shop(fiscals_dir(), fiscal_id(), yao_str)
    yao_hubunit._save_valid_budpoint_file(t66_timestamp, get_budunit_3_acct())
    yao_hubunit._save_valid_budpoint_file(t88_timestamp, get_budunit_3_acct())
    yao_hubunit._save_valid_purview_file(t66_purview)
    yao_hubunit._save_valid_purview_file(t88_purview)
    assert yao_hubunit.budpoint_file_exists(t66_timestamp)
    assert yao_hubunit.budpoint_file_exists(t88_timestamp)
    assert yao_hubunit.purview_file_exists(t66_timestamp)
    assert yao_hubunit.purview_file_exists(t88_timestamp)
    before_t66_purview = yao_hubunit.get_purview_file(t66_timestamp)
    assert before_t66_purview.timestamp == t66_timestamp
    assert before_t66_purview.amount == default_fund_pool()
    assert before_t66_purview._magnitude == 5
    assert before_t66_purview.get_net_purview("Sue") == -5
    assert not before_t66_purview.get_net_purview("Yao")
    assert not before_t66_purview.get_net_purview("Zia")
    before_t88_purview = yao_hubunit.get_purview_file(t88_timestamp)
    assert before_t88_purview.timestamp == t88_timestamp
    assert before_t88_purview.amount == 800
    assert before_t88_purview._magnitude == 0
    assert not before_t88_purview.get_net_purview("Sue")
    assert not before_t88_purview.get_net_purview("Yao")
    assert not before_t88_purview.get_net_purview("Zia")

    # WHEN
    yao_hubunit.calc_timepoint_purviews()

    # THEN
    assert yao_hubunit.budpoint_file_exists(t88_timestamp)
    yao_budpoint = yao_hubunit.get_budpoint_file(t88_timestamp)
    assert yao_hubunit.purview_file_exists(t88_timestamp)
    after_t88_purview = yao_hubunit.get_purview_file(t88_timestamp)
    assert after_t88_purview.timestamp == t88_timestamp
    assert after_t88_purview.amount == 800
    assert after_t88_purview.amount == yao_budpoint.fund_pool
    assert after_t88_purview.get_net_purview("Sue") == 62
    assert after_t88_purview.get_net_purview("Yao") == -227
    assert after_t88_purview.get_net_purview("Zia") == 165
    assert after_t88_purview._magnitude == 227
    after_t66_purview = yao_hubunit.get_purview_file(t66_timestamp)
    assert after_t66_purview.timestamp == t66_timestamp
    assert after_t66_purview.amount == default_fund_pool()
    assert after_t66_purview.get_net_purview("Sue") == 77380952
    assert after_t66_purview.get_net_purview("Yao") == -283333333
    assert after_t66_purview.get_net_purview("Zia") == 205952381
    assert after_t66_purview._magnitude == 283333333
