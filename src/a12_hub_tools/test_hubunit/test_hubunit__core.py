from src.a00_data_toolbox.file_toolbox import create_path
from src.a01_way_logic.way import (
    default_bridge_if_None,
    create_way_from_labels,
    create_way,
    get_default_fisc_label as root_label,
)
from src.a02_finance_logic.finance_config import (
    default_respect_bit_if_None,
    filter_penny,
    default_fund_coin_if_None,
    validate_fund_pool,
)
from src.a12_hub_tools.hub_path import create_owner_dir_path
from src.a12_hub_tools.hubunit import HubUnit, hubunit_shop, get_keep_path
from src.a13_bud_listen_logic._test_util.a13_env import (
    get_module_temp_dir as env_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_HubUnit_Exists():
    # ESTABLISH / WHEN
    x_hubunit = HubUnit()

    # THEN
    assert not x_hubunit.fisc_mstr_dir
    assert not x_hubunit.fisc_label
    assert not x_hubunit.owner_name
    assert not x_hubunit.keep_way
    assert not x_hubunit.bridge
    assert not x_hubunit.fund_pool
    assert not x_hubunit.fund_coin
    assert not x_hubunit.respect_bit
    assert not x_hubunit.penny
    assert not x_hubunit.keep_point_magnitude
    assert not x_hubunit._keeps_dir
    assert not x_hubunit._atoms_dir
    assert not x_hubunit._packs_dir


def test_HubUnit_RaisesError_keep_way_DoesNotExist():
    # ESTABLISH
    bob_str = "Bob"
    bob_hubunit = HubUnit(bob_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_hubunit.keep_dir()
    assert (
        str(excinfo.value)
        == f"HubUnit '{bob_str}' cannot save to keep_dir because it does not have keep_way."
    )


def test_hubunit_shop_ReturnsObj():
    # ESTABLISH
    x_fisc_mstr_dir = "src/a15_fisc_logic/_test_util"
    x_fisc_label = "accord45"
    sue_str = "Sue"
    x_bridge = "/"
    x_fund_pool = 13000
    x_fund_coin = 13
    x_respect_bit = 9
    x_penny = 3
    x_money_magnitude = 900

    # WHEN
    x_hubunit = hubunit_shop(
        fisc_mstr_dir=x_fisc_mstr_dir,
        fisc_label=x_fisc_label,
        owner_name=sue_str,
        keep_way=None,
        bridge=x_bridge,
        fund_pool=x_fund_pool,
        fund_coin=x_fund_coin,
        respect_bit=x_respect_bit,
        penny=x_penny,
        keep_point_magnitude=x_money_magnitude,
    )

    # THEN
    assert x_hubunit.fisc_mstr_dir == x_fisc_mstr_dir
    assert x_hubunit.fisc_label == x_fisc_label
    assert x_hubunit.owner_name == sue_str
    assert x_hubunit.bridge == x_bridge
    assert x_hubunit.fund_pool == x_fund_pool
    assert x_hubunit.fund_coin == x_fund_coin
    assert x_hubunit.respect_bit == x_respect_bit
    assert x_hubunit.penny == x_penny
    assert x_hubunit.keep_point_magnitude == x_money_magnitude
    sue_dir = create_owner_dir_path(x_fisc_mstr_dir, x_fisc_label, sue_str)
    assert x_hubunit._keeps_dir == create_path(sue_dir, "keeps")
    assert x_hubunit._atoms_dir == create_path(sue_dir, "atoms")
    assert x_hubunit._packs_dir == create_path(sue_dir, "packs")


def test_hubunit_shop_ReturnsObjWhenEmpty():
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_way = create_way(root_label(), nation_str)
    usa_str = "USA"
    usa_way = create_way(nation_way, usa_str)
    texas_str = "Texas"
    texas_way = create_way(usa_way, texas_str)
    fisc_mstr_dir = env_dir()
    accord23_str = "accord23"

    # WHEN
    sue_hubunit = hubunit_shop(fisc_mstr_dir, accord23_str, sue_str, texas_way)

    # THEN
    x_dutys_path = create_path(sue_hubunit.keep_dir(), "dutys")
    x_plans_path = create_path(sue_hubunit.keep_dir(), "plans")
    x_grades_path = create_path(sue_hubunit.keep_dir(), "grades")

    assert sue_hubunit.fisc_mstr_dir == fisc_mstr_dir
    assert sue_hubunit.fisc_label == accord23_str
    assert sue_hubunit.owner_name == sue_str
    assert sue_hubunit.bridge == default_bridge_if_None()
    assert sue_hubunit.fund_pool == validate_fund_pool()
    assert sue_hubunit.fund_coin == default_fund_coin_if_None()
    assert sue_hubunit.respect_bit == default_respect_bit_if_None()
    assert sue_hubunit.penny == filter_penny()
    x_hubunit = hubunit_shop(fisc_mstr_dir, accord23_str, sue_str)
    assert sue_hubunit.keep_way == texas_way
    assert sue_hubunit.keep_dir() == get_keep_path(x_hubunit, texas_way)
    bob_str = "Bob"
    assert sue_hubunit.dutys_dir() == x_dutys_path
    assert sue_hubunit.plans_dir() == x_plans_path
    assert sue_hubunit.grades_dir() == x_grades_path
    sue_dutys_dir = sue_hubunit.dutys_dir()
    sue_plans_dir = sue_hubunit.plans_dir()
    sue_grades_dir = sue_hubunit.grades_dir()
    x_duty_path = create_path(sue_dutys_dir, f"{bob_str}.json")
    x_plan_path = create_path(sue_plans_dir, f"{bob_str}.json")
    x_grade_path = create_path(sue_grades_dir, f"{bob_str}.json")
    assert sue_hubunit.duty_path(bob_str) == x_duty_path
    assert sue_hubunit.plan_path(bob_str) == x_plan_path
    assert sue_hubunit.grade_path(bob_str) == x_grade_path
    treasury_filename = "treasury.db"
    x_treasury_file_path = create_path(sue_hubunit.keep_dir(), treasury_filename)
    assert sue_hubunit.treasury_db_path() == x_treasury_file_path


def test_hubunit_shop_RaisesErrorIf_owner_name_Contains_bridge():
    # ESTABLISH
    slash_str = "/"
    bob_str = f"Bob{slash_str}Sue"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        hubunit_shop(None, None, owner_name=bob_str, bridge=slash_str)
    assert (
        str(excinfo.value)
        == f"'{bob_str}' needs to be a LabelStr. Cannot contain bridge: '{slash_str}'"
    )


def test_get_keep_path_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    peru_str = "peru"
    sue_hubunit = hubunit_shop(env_dir(), fisc_label=peru_str, owner_name=sue_str)
    texas_str = "texas"
    dallas_str = "dallas"
    elpaso_str = "el paso"
    kern_str = "kern"
    conceptroot = "conceptroot"
    texas_way = create_way_from_labels([peru_str, texas_str])
    dallas_way = create_way_from_labels([peru_str, texas_str, dallas_str])
    elpaso_way = create_way_from_labels([peru_str, texas_str, elpaso_str])
    kern_way = create_way_from_labels([peru_str, texas_str, elpaso_str, kern_str])

    # WHEN
    texas_path = get_keep_path(sue_hubunit, texas_way)
    dallas_path = get_keep_path(sue_hubunit, dallas_way)
    elpaso_path = get_keep_path(sue_hubunit, elpaso_way)
    kern_path = get_keep_path(sue_hubunit, kern_way)

    # THEN
    conceptroot_dir = create_path(sue_hubunit._keeps_dir, peru_str)
    print(f"{kern_way=}")
    print(f"{conceptroot_dir=}")
    assert texas_path == create_path(conceptroot_dir, texas_str)
    assert dallas_path == create_path(texas_path, dallas_str)
    assert elpaso_path == create_path(texas_path, elpaso_str)
    assert kern_path == create_path(elpaso_path, kern_str)

    # WHEN / THEN
    diff_root_texas_way = create_way_from_labels([peru_str, texas_str])
    diff_root_dallas_way = create_way_from_labels([peru_str, texas_str, dallas_str])
    diff_root_elpaso_way = create_way_from_labels([peru_str, texas_str, elpaso_str])
    assert texas_path == get_keep_path(sue_hubunit, diff_root_texas_way)
    assert dallas_path == get_keep_path(sue_hubunit, diff_root_dallas_way)
    assert elpaso_path == get_keep_path(sue_hubunit, diff_root_elpaso_way)
