from src.f00_instrument.file import create_path
from src.f01_road.finance import default_fund_pool
from src.f05_listen.hub_path import create_dealunit_json_path, create_budpoint_path
from src.f05_listen.hubunit import hubunit_shop
from src.f05_listen.examples.example_listen_buds import (
    get_budunit_with_4_levels,
    get_budunit_irrational_example,
    get_budunit_3_acct,
)
from src.f05_listen.examples.example_listen_deals import (
    get_dealunit_55_example,
    get_dealunit_66_example,
    get_dealunit_88_example,
    get_dealunit_invalid_example,
)
from src.f05_listen.examples.listen_env import (
    get_listen_temp_env_dir as fisc_mstr_dir,
    get_default_fisc_title as fisc_title,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists
from pytest import raises as pytest_raises


def test_HubUnit_timepoint_dir_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), yao_str)
    t88_deal_time = 8800

    # WHEN
    one_timepoint_dir = yao_hubunit.timepoint_dir(t88_deal_time)

    # THEN
    x_deals_dir = yao_hubunit._deals_dir
    assert one_timepoint_dir == create_path(x_deals_dir, str(t88_deal_time))


def test_HubUnit_deal_filename_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), yao_str)

    # WHEN
    x_deal_filename = yao_hubunit.deal_filename()

    # THEN
    assert x_deal_filename == "dealunit.json"


def test_HubUnit_deal_file_path_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), yao_str)
    t88_deal_time = 8800

    # WHEN
    t88_deal_file_path = yao_hubunit.deal_file_path(t88_deal_time)

    # THEN
    x_timepoint_dir = yao_hubunit.timepoint_dir(t88_deal_time)
    x_file_path = create_path(x_timepoint_dir, yao_hubunit.deal_filename())
    assert t88_deal_file_path == x_file_path
    f_deal_path = create_dealunit_json_path(
        fisc_mstr_dir(), fisc_title(), yao_str, t88_deal_time
    )
    assert t88_deal_file_path == f_deal_path


def test_HubUnit_save_valid_deal_file_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), yao_str)
    t55_deal = get_dealunit_55_example()
    t55_deal_time = t55_deal.deal_time
    assert os_path_exists(yao_hubunit.deal_file_path(t55_deal_time)) is False

    # WHEN
    yao_hubunit._save_valid_deal_file(t55_deal)

    # THEN
    assert os_path_exists(yao_hubunit.deal_file_path(t55_deal_time))


def test_HubUnit_save_valid_deal_file_RaisesError(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), yao_str)
    t_deal = get_dealunit_invalid_example()

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_hubunit._save_valid_deal_file(t_deal)
    exception_str = (
        "magnitude cannot be calculated: debt_deal_acct_net=-5, cred_deal_acct_net=3"
    )
    assert str(excinfo.value) == exception_str


def test_HubUnit_deal_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), yao_str)
    t55_deal = get_dealunit_55_example()
    t55_deal_time = t55_deal.deal_time
    assert yao_hubunit.deal_file_exists(t55_deal_time) is False

    # WHEN
    yao_hubunit._save_valid_deal_file(t55_deal)

    # THEN
    assert yao_hubunit.deal_file_exists(t55_deal_time)


def test_HubUnit_get_deal_file_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), yao_str)
    t55_deal = get_dealunit_55_example()
    t55_deal_time = t55_deal.deal_time
    yao_hubunit._save_valid_deal_file(t55_deal)
    assert yao_hubunit.deal_file_exists(t55_deal_time)

    # WHEN / THEN
    assert yao_hubunit.get_deal_file(t55_deal_time) == t55_deal


def test_HubUnit_delete_deal_file_DeletesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), yao_str)
    t55_deal = get_dealunit_55_example()
    t55_deal_time = t55_deal.deal_time
    yao_hubunit._save_valid_deal_file(t55_deal)
    assert yao_hubunit.deal_file_exists(t55_deal_time)

    # WHEN
    yao_hubunit.delete_deal_file(t55_deal_time)

    # THEN
    assert yao_hubunit.deal_file_exists(t55_deal_time) is False


def test_HubUnit_get_brokerunit_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), yao_str)
    t55_deal = get_dealunit_55_example()
    t66_deal = get_dealunit_66_example()
    t55_deal_time = t55_deal.deal_time
    t66_deal_time = t66_deal.deal_time
    yao_hubunit._save_valid_deal_file(t55_deal)
    assert yao_hubunit.get_brokerunit().deal_exists(t55_deal_time)
    assert yao_hubunit.get_brokerunit().deal_exists(t66_deal_time) is False
    yao_hubunit._save_valid_deal_file(t66_deal)

    # WHEN / THEN
    assert yao_hubunit.get_brokerunit().deal_exists(t55_deal_time)
    assert yao_hubunit.get_brokerunit().deal_exists(t66_deal_time)
    assert yao_hubunit.get_brokerunit().get_deal(t66_deal_time).get_deal_acct_net("Sue")


def test_HubUnit_budpoint_filename_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), yao_str)

    # WHEN
    x_deal_filename = yao_hubunit.budpoint_filename()

    # THEN
    assert x_deal_filename == "budpoint.json"


def test_HubUnit_budpoint_file_path_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), yao_str)
    t88_deal_time = 8800

    # WHEN
    t88_budpoint_file_path = yao_hubunit.budpoint_file_path(t88_deal_time)

    # THEN
    x_timepoint_dir = yao_hubunit.timepoint_dir(t88_deal_time)
    x_file_path = create_path(x_timepoint_dir, yao_hubunit.budpoint_filename())
    assert t88_budpoint_file_path == x_file_path
    f_budpoint_path = create_budpoint_path(
        fisc_mstr_dir(), fisc_title(), yao_str, t88_deal_time
    )
    assert t88_budpoint_file_path == f_budpoint_path


def test_HubUnit_save_valid_budpoint_file_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), yao_str)
    t55_budpoint = get_budunit_with_4_levels()
    t55_deal_time = 55
    assert os_path_exists(yao_hubunit.budpoint_file_path(t55_deal_time)) is False

    # WHEN
    yao_hubunit._save_valid_budpoint_file(t55_deal_time, t55_budpoint)

    # THEN
    assert os_path_exists(yao_hubunit.budpoint_file_path(t55_deal_time))


def test_HubUnit_save_valid_budpoint_file_RaisesError(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), yao_str)
    t_budpoint = get_budunit_irrational_example()
    t55_deal_time = 55

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_hubunit._save_valid_budpoint_file(t55_deal_time, t_budpoint)
    exception_str = "BudPoint could not be saved BudUnit._rational is False"
    assert str(excinfo.value) == exception_str


def test_HubUnit_budpoint_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), yao_str)
    t55_deal_time = 55
    assert yao_hubunit.budpoint_file_exists(t55_deal_time) is False

    # WHEN
    t55_budpoint = get_budunit_with_4_levels()
    yao_hubunit._save_valid_budpoint_file(t55_deal_time, t55_budpoint)

    # THEN
    assert yao_hubunit.budpoint_file_exists(t55_deal_time)


def test_HubUnit_get_budpoint_file_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), yao_str)
    t55_deal_time = 55
    t55_budpoint = get_budunit_with_4_levels()
    yao_hubunit._save_valid_budpoint_file(t55_deal_time, t55_budpoint)
    assert yao_hubunit.budpoint_file_exists(t55_deal_time)

    # WHEN
    file_budpoint = yao_hubunit.get_budpoint_file(t55_deal_time)

    # THEN
    assert file_budpoint.get_dict() == t55_budpoint.get_dict()


def test_HubUnit_delete_budpoint_file_DeletesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), yao_str)
    t55_deal_time = 55
    t55_budpoint = get_budunit_with_4_levels()
    yao_hubunit._save_valid_budpoint_file(t55_deal_time, t55_budpoint)
    assert yao_hubunit.budpoint_file_exists(t55_deal_time)

    # WHEN
    yao_hubunit.delete_budpoint_file(t55_deal_time)

    # THEN
    assert yao_hubunit.budpoint_file_exists(t55_deal_time) is False


def test_HubUnit_calc_timepoint_deal_Sets_deal_file_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    t55_deal_time = 55
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), yao_str)
    yao_hubunit._save_valid_budpoint_file(t55_deal_time, get_budunit_3_acct())
    assert yao_hubunit.budpoint_file_exists(t55_deal_time)
    assert yao_hubunit.deal_file_exists(t55_deal_time) is False

    # WHEN
    yao_hubunit.calc_timepoint_deal(t55_deal_time)

    # THEN
    assert yao_hubunit.budpoint_file_exists(t55_deal_time)
    assert yao_hubunit.deal_file_exists(t55_deal_time)
    t55_deal = yao_hubunit.get_deal_file(t55_deal_time)
    assert t55_deal.deal_time == t55_deal_time
    assert t55_deal.quota == default_fund_pool()
    assert t55_deal._magnitude == 283333333
    assert t55_deal.get_deal_acct_net("Sue") == 77380952
    assert t55_deal.get_deal_acct_net("Yao") == -283333333
    assert t55_deal.get_deal_acct_net("Zia") == 205952381


def test_HubUnit_calc_timepoint_deal_Sets_deal_file_Scenario1(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    t88_deal = get_dealunit_88_example()
    t88_deal_time = t88_deal.deal_time
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), yao_str)
    yao_hubunit._save_valid_budpoint_file(t88_deal_time, get_budunit_3_acct())
    yao_hubunit._save_valid_deal_file(t88_deal)
    assert yao_hubunit.budpoint_file_exists(t88_deal_time)
    assert yao_hubunit.deal_file_exists(t88_deal_time)
    before_t88_deal = yao_hubunit.get_deal_file(t88_deal_time)
    assert before_t88_deal.deal_time == t88_deal_time
    assert before_t88_deal.quota == 800
    assert before_t88_deal._magnitude == 0
    assert not before_t88_deal.get_deal_acct_net("Sue")
    assert not before_t88_deal.get_deal_acct_net("Yao")
    assert not before_t88_deal.get_deal_acct_net("Zia")

    # WHEN
    yao_hubunit.calc_timepoint_deal(t88_deal_time)

    # THEN
    assert yao_hubunit.budpoint_file_exists(t88_deal_time)
    yao_budpoint = yao_hubunit.get_budpoint_file(t88_deal_time)
    assert yao_hubunit.deal_file_exists(t88_deal_time)
    after_t88_deal = yao_hubunit.get_deal_file(t88_deal_time)
    assert after_t88_deal.deal_time == t88_deal_time
    assert after_t88_deal.quota == 800
    assert after_t88_deal.quota == yao_budpoint.fund_pool
    assert after_t88_deal.get_deal_acct_net("Sue") == 62
    assert after_t88_deal.get_deal_acct_net("Yao") == -227
    assert after_t88_deal.get_deal_acct_net("Zia") == 165
    assert after_t88_deal._magnitude == 227


def test_HubUnit_calc_timepoint_deal_RaisesException(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    t88_deal = get_dealunit_88_example()
    t88_deal_time = t88_deal.deal_time
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), yao_str)
    yao_hubunit._save_valid_deal_file(t88_deal)
    assert yao_hubunit.budpoint_file_exists(t88_deal_time) is False
    assert yao_hubunit.deal_file_exists(t88_deal_time)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_hubunit.calc_timepoint_deal(t88_deal_time)
    exception_str = (
        f"Cannot calculate timepoint {t88_deal_time} deals without saved BudPoint file"
    )
    assert str(excinfo.value) == exception_str


def test_HubUnit_calc_timepoint_deals_Sets_deal_files_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    t66_deal = get_dealunit_66_example()
    t88_deal = get_dealunit_88_example()
    t66_deal_time = t66_deal.deal_time
    t88_deal_time = t88_deal.deal_time
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), yao_str)
    yao_hubunit._save_valid_budpoint_file(t66_deal_time, get_budunit_3_acct())
    yao_hubunit._save_valid_budpoint_file(t88_deal_time, get_budunit_3_acct())
    yao_hubunit._save_valid_deal_file(t66_deal)
    yao_hubunit._save_valid_deal_file(t88_deal)
    assert yao_hubunit.budpoint_file_exists(t66_deal_time)
    assert yao_hubunit.budpoint_file_exists(t88_deal_time)
    assert yao_hubunit.deal_file_exists(t66_deal_time)
    assert yao_hubunit.deal_file_exists(t88_deal_time)
    before_t66_deal = yao_hubunit.get_deal_file(t66_deal_time)
    assert before_t66_deal.deal_time == t66_deal_time
    assert before_t66_deal.quota == default_fund_pool()
    assert before_t66_deal._magnitude == 5
    assert before_t66_deal.get_deal_acct_net("Sue") == -5
    assert not before_t66_deal.get_deal_acct_net("Yao")
    assert not before_t66_deal.get_deal_acct_net("Zia")
    before_t88_deal = yao_hubunit.get_deal_file(t88_deal_time)
    assert before_t88_deal.deal_time == t88_deal_time
    assert before_t88_deal.quota == 800
    assert before_t88_deal._magnitude == 0
    assert not before_t88_deal.get_deal_acct_net("Sue")
    assert not before_t88_deal.get_deal_acct_net("Yao")
    assert not before_t88_deal.get_deal_acct_net("Zia")

    # WHEN
    yao_hubunit.calc_timepoint_deals()

    # THEN
    assert yao_hubunit.budpoint_file_exists(t88_deal_time)
    yao_budpoint = yao_hubunit.get_budpoint_file(t88_deal_time)
    assert yao_hubunit.deal_file_exists(t88_deal_time)
    after_t88_deal = yao_hubunit.get_deal_file(t88_deal_time)
    assert after_t88_deal.deal_time == t88_deal_time
    assert after_t88_deal.quota == 800
    assert after_t88_deal.quota == yao_budpoint.fund_pool
    assert after_t88_deal.get_deal_acct_net("Sue") == 62
    assert after_t88_deal.get_deal_acct_net("Yao") == -227
    assert after_t88_deal.get_deal_acct_net("Zia") == 165
    assert after_t88_deal._magnitude == 227
    after_t66_deal = yao_hubunit.get_deal_file(t66_deal_time)
    assert after_t66_deal.deal_time == t66_deal_time
    assert after_t66_deal.quota == default_fund_pool()
    assert after_t66_deal.get_deal_acct_net("Sue") == 77380952
    assert after_t66_deal.get_deal_acct_net("Yao") == -283333333
    assert after_t66_deal.get_deal_acct_net("Zia") == 205952381
    assert after_t66_deal._magnitude == 283333333
