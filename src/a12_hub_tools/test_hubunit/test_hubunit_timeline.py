from src.a02_finance_toolboxs.finance_config import default_fund_pool
from src.a12_hub_tools.hub_tool import (
    save_deal_file,
    deal_file_exists,
    open_deal_file,
    save_budpoint_file,
    budpoint_file_exists,
    open_budpoint_file,
)
from src.a12_hub_tools.hubunit import hubunit_shop
from src.a13_bud_listen_logic.examples.example_listen_buds import get_budunit_3_acct
from src.a13_bud_listen_logic.examples.example_listen_deals import (
    get_dealunit_55_example,
    get_dealunit_66_example,
    get_dealunit_88_example,
)
from src.a13_bud_listen_logic.examples.listen_env import (
    get_listen_temp_env_dir as fisc_mstr_dir,
    get_default_fisc_title as fisc_title,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_HubUnit_calc_timepoint_deal_Sets_deal_file_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = fisc_mstr_dir()
    x_fisc_title = fisc_title()
    bob_str = "Bob"
    t55_deal_time = 55
    bob_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), bob_str)
    save_budpoint_file(mstr_dir, get_budunit_3_acct(), t55_deal_time)
    assert budpoint_file_exists(mstr_dir, x_fisc_title, bob_str, t55_deal_time)
    assert not deal_file_exists(mstr_dir, x_fisc_title, bob_str, t55_deal_time)

    # WHEN
    bob_hubunit.calc_timepoint_deal(t55_deal_time)

    # THEN
    assert budpoint_file_exists(mstr_dir, x_fisc_title, bob_str, t55_deal_time)
    assert deal_file_exists(mstr_dir, x_fisc_title, bob_str, t55_deal_time)
    t55_deal = open_deal_file(mstr_dir, x_fisc_title, bob_str, t55_deal_time)
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
    mstr_dir = fisc_mstr_dir()
    x_fisc_title = fisc_title()
    bob_str = "Bob"
    t88_deal = get_dealunit_88_example()
    t88_deal_time = t88_deal.deal_time
    sue_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), bob_str)
    save_budpoint_file(mstr_dir, get_budunit_3_acct(), t88_deal_time)
    save_deal_file(mstr_dir, x_fisc_title, bob_str, t88_deal)
    assert budpoint_file_exists(mstr_dir, x_fisc_title, bob_str, t88_deal_time)
    assert open_deal_file(mstr_dir, x_fisc_title, bob_str, t88_deal_time)
    before_t88_deal = open_deal_file(mstr_dir, x_fisc_title, bob_str, t88_deal_time)
    assert before_t88_deal.deal_time == t88_deal_time
    assert before_t88_deal.quota == 800
    assert before_t88_deal._magnitude == 0
    assert not before_t88_deal.get_deal_acct_net("Sue")
    assert not before_t88_deal.get_deal_acct_net("Yao")
    assert not before_t88_deal.get_deal_acct_net("Zia")

    # WHEN
    sue_hubunit.calc_timepoint_deal(t88_deal_time)

    # THEN
    assert budpoint_file_exists(mstr_dir, x_fisc_title, bob_str, t88_deal_time)
    sue_budpoint = open_budpoint_file(mstr_dir, x_fisc_title, bob_str, t88_deal_time)
    assert deal_file_exists(mstr_dir, x_fisc_title, bob_str, t88_deal_time)
    after_t88_deal = open_deal_file(mstr_dir, x_fisc_title, bob_str, t88_deal_time)
    assert after_t88_deal.deal_time == t88_deal_time
    assert after_t88_deal.quota == 800
    assert after_t88_deal.quota == sue_budpoint.fund_pool
    assert after_t88_deal.get_deal_acct_net("Sue") == 62
    assert after_t88_deal.get_deal_acct_net("Yao") == -227
    assert after_t88_deal.get_deal_acct_net("Zia") == 165
    assert after_t88_deal._magnitude == 227


def test_HubUnit_calc_timepoint_deal_RaisesException(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = fisc_mstr_dir()
    x_fisc_title = fisc_title()
    sue_str = "Sue"
    t88_deal = get_dealunit_88_example()
    t88_deal_time = t88_deal.deal_time
    sue_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), sue_str)
    save_deal_file(mstr_dir, x_fisc_title, sue_str, t88_deal)
    assert not budpoint_file_exists(mstr_dir, x_fisc_title, sue_str, t88_deal_time)
    assert deal_file_exists(mstr_dir, x_fisc_title, sue_str, t88_deal_time)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.calc_timepoint_deal(t88_deal_time)
    exception_str = (
        f"Cannot calculate timepoint {t88_deal_time} deals without saved BudPoint file"
    )
    assert str(excinfo.value) == exception_str


def test_HubUnit_calc_timepoint_deals_Sets_deal_files_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = fisc_mstr_dir()
    x_fisc_title = fisc_title()
    bob_str = "Bob"
    t66_deal = get_dealunit_66_example()
    t88_deal = get_dealunit_88_example()
    t66_deal_time = t66_deal.deal_time
    t88_deal_time = t88_deal.deal_time
    sue_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_title(), bob_str)
    save_budpoint_file(mstr_dir, get_budunit_3_acct(), t66_deal_time)
    save_budpoint_file(mstr_dir, get_budunit_3_acct(), t88_deal_time)
    save_deal_file(mstr_dir, x_fisc_title, bob_str, t66_deal)
    save_deal_file(mstr_dir, x_fisc_title, bob_str, t88_deal)
    assert budpoint_file_exists(mstr_dir, x_fisc_title, bob_str, t66_deal_time)
    assert budpoint_file_exists(mstr_dir, x_fisc_title, bob_str, t88_deal_time)
    assert deal_file_exists(mstr_dir, x_fisc_title, bob_str, t66_deal_time)
    assert deal_file_exists(mstr_dir, x_fisc_title, bob_str, t88_deal_time)
    before_t66_deal = open_deal_file(mstr_dir, x_fisc_title, bob_str, t66_deal_time)
    assert before_t66_deal.deal_time == t66_deal_time
    assert before_t66_deal.quota == default_fund_pool()
    assert before_t66_deal._magnitude == 5
    assert before_t66_deal.get_deal_acct_net("Sue") == -5
    assert not before_t66_deal.get_deal_acct_net("Yao")
    assert not before_t66_deal.get_deal_acct_net("Zia")
    before_t88_deal = open_deal_file(mstr_dir, x_fisc_title, bob_str, t88_deal_time)
    assert before_t88_deal.deal_time == t88_deal_time
    assert before_t88_deal.quota == 800
    assert before_t88_deal._magnitude == 0
    assert not before_t88_deal.get_deal_acct_net("Sue")
    assert not before_t88_deal.get_deal_acct_net("Yao")
    assert not before_t88_deal.get_deal_acct_net("Zia")

    # WHEN
    sue_hubunit.calc_timepoint_deals()

    # THEN
    assert budpoint_file_exists(mstr_dir, x_fisc_title, bob_str, t88_deal_time)
    sue_budpoint = open_budpoint_file(mstr_dir, x_fisc_title, bob_str, t88_deal_time)
    assert deal_file_exists(mstr_dir, x_fisc_title, bob_str, t88_deal_time)
    after_t88_deal = open_deal_file(mstr_dir, x_fisc_title, bob_str, t88_deal_time)
    assert after_t88_deal.deal_time == t88_deal_time
    assert after_t88_deal.quota == 800
    assert after_t88_deal.quota == sue_budpoint.fund_pool
    assert after_t88_deal.get_deal_acct_net("Sue") == 62
    assert after_t88_deal.get_deal_acct_net("Yao") == -227
    assert after_t88_deal.get_deal_acct_net("Zia") == 165
    assert after_t88_deal._magnitude == 227
    after_t66_deal = open_deal_file(mstr_dir, x_fisc_title, bob_str, t66_deal_time)
    assert after_t66_deal.deal_time == t66_deal_time
    assert after_t66_deal.quota == default_fund_pool()
    assert after_t66_deal.get_deal_acct_net("Sue") == 77380952
    assert after_t66_deal.get_deal_acct_net("Yao") == -283333333
    assert after_t66_deal.get_deal_acct_net("Zia") == 205952381
    assert after_t66_deal._magnitude == 283333333
