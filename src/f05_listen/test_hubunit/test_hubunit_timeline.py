from src.f00_instrument.file import create_path
from src.f01_road.finance import default_fund_pool
from src.f05_listen.hubunit import hubunit_shop
from src.f05_listen.examples.example_listen_buds import (
    get_budunit_with_4_levels,
    get_budunit_irrational_example,
    get_budunit_3_acct,
)
from src.f05_listen.examples.example_listen_banks import (
    get_bankepisode_55_example,
    get_bankepisode_66_example,
    get_bankepisode_88_example,
    get_bankepisode_invalid_example,
)
from src.f05_listen.examples.listen_env import (
    get_listen_temp_env_dir as deals_dir,
    get_default_deal_idea as deal_idea,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists
from pytest import raises as pytest_raises


def test_HubUnit_timepoint_dir_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(deals_dir(), deal_idea(), yao_str)
    t88_time_int = 8800

    # WHEN
    one_timepoint_dir = yao_hubunit.timepoint_dir(t88_time_int)

    # THEN
    x_timeline_dir = yao_hubunit.timeline_dir()
    assert one_timepoint_dir == create_path(x_timeline_dir, str(t88_time_int))


def test_HubUnit_bank_file_name_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(deals_dir(), deal_idea(), yao_str)

    # WHEN
    x_bank_file_name = yao_hubunit.bank_file_name()

    # THEN
    assert x_bank_file_name == "bank.json"


def test_HubUnit_bank_file_path_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(deals_dir(), deal_idea(), yao_str)
    t88_time_int = 8800

    # WHEN
    t88_bank_file_path = yao_hubunit.bank_file_path(t88_time_int)

    # THEN
    x_timepoint_dir = yao_hubunit.timepoint_dir(t88_time_int)
    x_file_path = create_path(x_timepoint_dir, yao_hubunit.bank_file_name())
    assert t88_bank_file_path == x_file_path


def test_HubUnit_save_valid_bank_file_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(deals_dir(), deal_idea(), yao_str)
    t55_bank = get_bankepisode_55_example()
    t55_time_int = t55_bank.time_int
    assert os_path_exists(yao_hubunit.bank_file_path(t55_time_int)) is False

    # WHEN
    yao_hubunit._save_valid_bank_file(t55_bank)

    # THEN
    assert os_path_exists(yao_hubunit.bank_file_path(t55_time_int))


def test_HubUnit_save_valid_bank_file_RaisesError(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(deals_dir(), deal_idea(), yao_str)
    t_bank = get_bankepisode_invalid_example()

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_hubunit._save_valid_bank_file(t_bank)
    exception_str = "magnitude cannot be calculated: debt_bank=-5, cred_bank=3"
    assert str(excinfo.value) == exception_str


def test_HubUnit_bank_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(deals_dir(), deal_idea(), yao_str)
    t55_bank = get_bankepisode_55_example()
    t55_time_int = t55_bank.time_int
    assert yao_hubunit.bank_file_exists(t55_time_int) is False

    # WHEN
    yao_hubunit._save_valid_bank_file(t55_bank)

    # THEN
    assert yao_hubunit.bank_file_exists(t55_time_int)


def test_HubUnit_get_bank_file_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(deals_dir(), deal_idea(), yao_str)
    t55_bank = get_bankepisode_55_example()
    t55_time_int = t55_bank.time_int
    yao_hubunit._save_valid_bank_file(t55_bank)
    assert yao_hubunit.bank_file_exists(t55_time_int)

    # WHEN / THEN
    assert yao_hubunit.get_bank_file(t55_time_int) == t55_bank


def test_HubUnit_delete_bank_file_DeletesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(deals_dir(), deal_idea(), yao_str)
    t55_bank = get_bankepisode_55_example()
    t55_time_int = t55_bank.time_int
    yao_hubunit._save_valid_bank_file(t55_bank)
    assert yao_hubunit.bank_file_exists(t55_time_int)

    # WHEN
    yao_hubunit.delete_bank_file(t55_time_int)

    # THEN
    assert yao_hubunit.bank_file_exists(t55_time_int) is False


def test_HubUnit_get_banklog_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(deals_dir(), deal_idea(), yao_str)
    t55_bank = get_bankepisode_55_example()
    t66_bank = get_bankepisode_66_example()
    t55_time_int = t55_bank.time_int
    t66_time_int = t66_bank.time_int
    yao_hubunit._save_valid_bank_file(t55_bank)
    assert yao_hubunit.get_banklog().episode_exists(t55_time_int)
    assert yao_hubunit.get_banklog().episode_exists(t66_time_int) is False
    yao_hubunit._save_valid_bank_file(t66_bank)

    # WHEN / THEN
    assert yao_hubunit.get_banklog().episode_exists(t55_time_int)
    assert yao_hubunit.get_banklog().episode_exists(t66_time_int)
    assert yao_hubunit.get_banklog().get_episode(t66_time_int).get_net_bank("Sue")


def test_HubUnit_budpoint_file_name_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(deals_dir(), deal_idea(), yao_str)

    # WHEN
    x_bank_file_name = yao_hubunit.budpoint_file_name()

    # THEN
    assert x_bank_file_name == "budpoint.json"


def test_HubUnit_budpoint_file_path_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(deals_dir(), deal_idea(), yao_str)
    t88_time_int = 8800

    # WHEN
    t88_budpoint_file_path = yao_hubunit.budpoint_file_path(t88_time_int)

    # THEN
    x_timepoint_dir = yao_hubunit.timepoint_dir(t88_time_int)
    x_file_path = create_path(x_timepoint_dir, yao_hubunit.budpoint_file_name())
    assert t88_budpoint_file_path == x_file_path


def test_HubUnit_save_valid_budpoint_file_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(deals_dir(), deal_idea(), yao_str)
    t55_budpoint = get_budunit_with_4_levels()
    t55_time_int = 55
    assert os_path_exists(yao_hubunit.budpoint_file_path(t55_time_int)) is False

    # WHEN
    yao_hubunit._save_valid_budpoint_file(t55_time_int, t55_budpoint)

    # THEN
    assert os_path_exists(yao_hubunit.budpoint_file_path(t55_time_int))


def test_HubUnit_save_valid_budpoint_file_RaisesError(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(deals_dir(), deal_idea(), yao_str)
    t_budpoint = get_budunit_irrational_example()
    t55_time_int = 55

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_hubunit._save_valid_budpoint_file(t55_time_int, t_budpoint)
    exception_str = "BudPoint could not be saved BudUnit._rational is False"
    assert str(excinfo.value) == exception_str


def test_HubUnit_budpoint_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(deals_dir(), deal_idea(), yao_str)
    t55_time_int = 55
    assert yao_hubunit.budpoint_file_exists(t55_time_int) is False

    # WHEN
    t55_budpoint = get_budunit_with_4_levels()
    yao_hubunit._save_valid_budpoint_file(t55_time_int, t55_budpoint)

    # THEN
    assert yao_hubunit.budpoint_file_exists(t55_time_int)


def test_HubUnit_get_budpoint_file_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(deals_dir(), deal_idea(), yao_str)
    t55_time_int = 55
    t55_budpoint = get_budunit_with_4_levels()
    yao_hubunit._save_valid_budpoint_file(t55_time_int, t55_budpoint)
    assert yao_hubunit.budpoint_file_exists(t55_time_int)

    # WHEN
    file_budpoint = yao_hubunit.get_budpoint_file(t55_time_int)

    # THEN
    assert file_budpoint.get_dict() == t55_budpoint.get_dict()


def test_HubUnit_delete_budpoint_file_DeletesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(deals_dir(), deal_idea(), yao_str)
    t55_time_int = 55
    t55_budpoint = get_budunit_with_4_levels()
    yao_hubunit._save_valid_budpoint_file(t55_time_int, t55_budpoint)
    assert yao_hubunit.budpoint_file_exists(t55_time_int)

    # WHEN
    yao_hubunit.delete_budpoint_file(t55_time_int)

    # THEN
    assert yao_hubunit.budpoint_file_exists(t55_time_int) is False


def test_HubUnit_calc_timepoint_bank_Sets_bank_file_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    t55_time_int = 55
    yao_hubunit = hubunit_shop(deals_dir(), deal_idea(), yao_str)
    yao_hubunit._save_valid_budpoint_file(t55_time_int, get_budunit_3_acct())
    assert yao_hubunit.budpoint_file_exists(t55_time_int)
    assert yao_hubunit.bank_file_exists(t55_time_int) is False

    # WHEN
    yao_hubunit.calc_timepoint_bank(t55_time_int)

    # THEN
    assert yao_hubunit.budpoint_file_exists(t55_time_int)
    assert yao_hubunit.bank_file_exists(t55_time_int)
    t55_bank = yao_hubunit.get_bank_file(t55_time_int)
    assert t55_bank.time_int == t55_time_int
    assert t55_bank.quota == default_fund_pool()
    assert t55_bank._magnitude == 283333333
    assert t55_bank.get_net_bank("Sue") == 77380952
    assert t55_bank.get_net_bank("Yao") == -283333333
    assert t55_bank.get_net_bank("Zia") == 205952381


def test_HubUnit_calc_timepoint_bank_Sets_bank_file_Scenario1(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    t88_bank = get_bankepisode_88_example()
    t88_time_int = t88_bank.time_int
    yao_hubunit = hubunit_shop(deals_dir(), deal_idea(), yao_str)
    yao_hubunit._save_valid_budpoint_file(t88_time_int, get_budunit_3_acct())
    yao_hubunit._save_valid_bank_file(t88_bank)
    assert yao_hubunit.budpoint_file_exists(t88_time_int)
    assert yao_hubunit.bank_file_exists(t88_time_int)
    before_t88_bank = yao_hubunit.get_bank_file(t88_time_int)
    assert before_t88_bank.time_int == t88_time_int
    assert before_t88_bank.quota == 800
    assert before_t88_bank._magnitude == 0
    assert not before_t88_bank.get_net_bank("Sue")
    assert not before_t88_bank.get_net_bank("Yao")
    assert not before_t88_bank.get_net_bank("Zia")

    # WHEN
    yao_hubunit.calc_timepoint_bank(t88_time_int)

    # THEN
    assert yao_hubunit.budpoint_file_exists(t88_time_int)
    yao_budpoint = yao_hubunit.get_budpoint_file(t88_time_int)
    assert yao_hubunit.bank_file_exists(t88_time_int)
    after_t88_bank = yao_hubunit.get_bank_file(t88_time_int)
    assert after_t88_bank.time_int == t88_time_int
    assert after_t88_bank.quota == 800
    assert after_t88_bank.quota == yao_budpoint.fund_pool
    assert after_t88_bank.get_net_bank("Sue") == 62
    assert after_t88_bank.get_net_bank("Yao") == -227
    assert after_t88_bank.get_net_bank("Zia") == 165
    assert after_t88_bank._magnitude == 227


def test_HubUnit_calc_timepoint_bank_RaisesException(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    t88_bank = get_bankepisode_88_example()
    t88_time_int = t88_bank.time_int
    yao_hubunit = hubunit_shop(deals_dir(), deal_idea(), yao_str)
    yao_hubunit._save_valid_bank_file(t88_bank)
    assert yao_hubunit.budpoint_file_exists(t88_time_int) is False
    assert yao_hubunit.bank_file_exists(t88_time_int)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_hubunit.calc_timepoint_bank(t88_time_int)
    exception_str = (
        f"Cannot calculate timepoint {t88_time_int} banks without saved BudPoint file"
    )
    assert str(excinfo.value) == exception_str


def test_HubUnit_calc_timepoint_banks_Sets_bank_files_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    t66_bank = get_bankepisode_66_example()
    t88_bank = get_bankepisode_88_example()
    t66_time_int = t66_bank.time_int
    t88_time_int = t88_bank.time_int
    yao_hubunit = hubunit_shop(deals_dir(), deal_idea(), yao_str)
    yao_hubunit._save_valid_budpoint_file(t66_time_int, get_budunit_3_acct())
    yao_hubunit._save_valid_budpoint_file(t88_time_int, get_budunit_3_acct())
    yao_hubunit._save_valid_bank_file(t66_bank)
    yao_hubunit._save_valid_bank_file(t88_bank)
    assert yao_hubunit.budpoint_file_exists(t66_time_int)
    assert yao_hubunit.budpoint_file_exists(t88_time_int)
    assert yao_hubunit.bank_file_exists(t66_time_int)
    assert yao_hubunit.bank_file_exists(t88_time_int)
    before_t66_bank = yao_hubunit.get_bank_file(t66_time_int)
    assert before_t66_bank.time_int == t66_time_int
    assert before_t66_bank.quota == default_fund_pool()
    assert before_t66_bank._magnitude == 5
    assert before_t66_bank.get_net_bank("Sue") == -5
    assert not before_t66_bank.get_net_bank("Yao")
    assert not before_t66_bank.get_net_bank("Zia")
    before_t88_bank = yao_hubunit.get_bank_file(t88_time_int)
    assert before_t88_bank.time_int == t88_time_int
    assert before_t88_bank.quota == 800
    assert before_t88_bank._magnitude == 0
    assert not before_t88_bank.get_net_bank("Sue")
    assert not before_t88_bank.get_net_bank("Yao")
    assert not before_t88_bank.get_net_bank("Zia")

    # WHEN
    yao_hubunit.calc_timepoint_banks()

    # THEN
    assert yao_hubunit.budpoint_file_exists(t88_time_int)
    yao_budpoint = yao_hubunit.get_budpoint_file(t88_time_int)
    assert yao_hubunit.bank_file_exists(t88_time_int)
    after_t88_bank = yao_hubunit.get_bank_file(t88_time_int)
    assert after_t88_bank.time_int == t88_time_int
    assert after_t88_bank.quota == 800
    assert after_t88_bank.quota == yao_budpoint.fund_pool
    assert after_t88_bank.get_net_bank("Sue") == 62
    assert after_t88_bank.get_net_bank("Yao") == -227
    assert after_t88_bank.get_net_bank("Zia") == 165
    assert after_t88_bank._magnitude == 227
    after_t66_bank = yao_hubunit.get_bank_file(t66_time_int)
    assert after_t66_bank.time_int == t66_time_int
    assert after_t66_bank.quota == default_fund_pool()
    assert after_t66_bank.get_net_bank("Sue") == 77380952
    assert after_t66_bank.get_net_bank("Yao") == -283333333
    assert after_t66_bank.get_net_bank("Zia") == 205952381
    assert after_t66_bank._magnitude == 283333333
