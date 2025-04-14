from src.f00_instrument.file_toolbox import create_path
from src.f01_road.road import (
    default_bridge_if_None,
    create_road_from_titles,
    create_road,
    get_default_fisc_title as root_title,
)
from src.f01_road.finance import (
    default_respect_bit_if_None,
    filter_penny,
    default_fund_coin_if_None,
    validate_fund_pool,
)
from src.f06_listen.hub_path import create_deals_dir_path
from src.f06_listen.hubunit import HubUnit, hubunit_shop, get_keep_path
from src.f06_listen.examples.listen_env import (
    get_listen_temp_env_dir as env_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_HubUnit_Exists():
    # ESTABLISH / WHEN
    x_hubunit = HubUnit()

    # THEN
    assert not x_hubunit.fisc_mstr_dir
    assert not x_hubunit.fisc_title
    assert not x_hubunit.owner_name
    assert not x_hubunit.keep_road
    assert not x_hubunit.bridge
    assert not x_hubunit.fund_pool
    assert not x_hubunit.fund_coin
    assert not x_hubunit.respect_bit
    assert not x_hubunit.penny
    assert not x_hubunit.keep_point_magnitude
    assert not x_hubunit._fisc_dir
    assert not x_hubunit._owners_dir
    assert not x_hubunit._owner_dir
    assert not x_hubunit._keeps_dir
    assert not x_hubunit._atoms_dir
    assert not x_hubunit._deals_dir
    assert not x_hubunit._packs_dir


def test_HubUnit_RaisesError_keep_road_DoesNotExist():
    # ESTABLISH
    bob_str = "Bob"
    bob_hubunit = HubUnit(bob_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_hubunit.keep_dir()
    assert (
        str(excinfo.value)
        == f"HubUnit '{bob_str}' cannot save to keep_dir because it does not have keep_road."
    )


def test_hubunit_shop_ReturnsObj():
    # ESTABLISH
    x_fisc_mstr_dir = "src/f08_fisc/examples"
    x_fisc_title = "accord45"
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
        fisc_title=x_fisc_title,
        owner_name=sue_str,
        keep_road=None,
        bridge=x_bridge,
        fund_pool=x_fund_pool,
        fund_coin=x_fund_coin,
        respect_bit=x_respect_bit,
        penny=x_penny,
        keep_point_magnitude=x_money_magnitude,
    )

    # THEN
    assert x_hubunit.fisc_mstr_dir == x_fisc_mstr_dir
    x_fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    assert x_hubunit.fisc_title == x_fisc_title
    assert x_hubunit.owner_name == sue_str
    assert x_hubunit.bridge == x_bridge
    assert x_hubunit.fund_pool == x_fund_pool
    assert x_hubunit.fund_coin == x_fund_coin
    assert x_hubunit.respect_bit == x_respect_bit
    assert x_hubunit.penny == x_penny
    assert x_hubunit.keep_point_magnitude == x_money_magnitude
    assert x_hubunit._fisc_dir == create_path(x_fiscs_dir, x_fisc_title)
    assert x_hubunit._owners_dir == create_path(x_hubunit._fisc_dir, "owners")
    assert x_hubunit._owner_dir == create_path(x_hubunit._owners_dir, sue_str)
    assert x_hubunit._keeps_dir == create_path(x_hubunit._owner_dir, "keeps")
    assert x_hubunit._atoms_dir == create_path(x_hubunit._owner_dir, "atoms")
    assert x_hubunit._deals_dir == create_path(x_hubunit._owner_dir, "deals")
    func_deals_dir = create_deals_dir_path(
        x_fisc_mstr_dir, x_fisc_title, x_hubunit.owner_name
    )
    print(f"{x_hubunit._deals_dir=}")
    print(f"{func_deals_dir=}")
    assert x_hubunit._deals_dir == func_deals_dir
    assert x_hubunit._packs_dir == create_path(x_hubunit._owner_dir, "packs")


def test_hubunit_shop_ReturnsObjWhenEmpty():
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation-state"
    nation_road = create_road(root_title(), nation_str)
    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    texas_str = "Texas"
    texas_road = create_road(usa_road, texas_str)
    fisc_mstr_dir = env_dir()
    accord23_str = "accord23"

    # WHEN
    sue_hubunit = hubunit_shop(fisc_mstr_dir, accord23_str, sue_str, texas_road)

    # THEN
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    x_fisc_path = create_path(fiscs_dir, accord23_str)
    x_owners_path = create_path(sue_hubunit._fisc_dir, "owners")
    x_dutys_path = create_path(sue_hubunit.keep_dir(), "dutys")
    x_jobs_path = create_path(sue_hubunit.keep_dir(), "jobs")
    x_grades_path = create_path(sue_hubunit.keep_dir(), "grades")

    assert sue_hubunit.fisc_mstr_dir == fisc_mstr_dir
    assert sue_hubunit.fisc_title == accord23_str
    assert sue_hubunit._fisc_dir == x_fisc_path
    assert sue_hubunit.owner_name == sue_str
    assert sue_hubunit.bridge == default_bridge_if_None()
    assert sue_hubunit.fund_pool == validate_fund_pool()
    assert sue_hubunit.fund_coin == default_fund_coin_if_None()
    assert sue_hubunit.respect_bit == default_respect_bit_if_None()
    assert sue_hubunit.penny == filter_penny()
    assert sue_hubunit._owners_dir == x_owners_path
    x_hubunit = hubunit_shop(fisc_mstr_dir, accord23_str, sue_str)
    assert sue_hubunit.keep_road == texas_road
    assert sue_hubunit.keep_dir() == get_keep_path(x_hubunit, texas_road)
    bob_str = "Bob"
    assert sue_hubunit.dutys_dir() == x_dutys_path
    assert sue_hubunit.jobs_dir() == x_jobs_path
    assert sue_hubunit.grades_dir() == x_grades_path
    sue_dutys_dir = sue_hubunit.dutys_dir()
    sue_jobs_dir = sue_hubunit.jobs_dir()
    sue_grades_dir = sue_hubunit.grades_dir()
    x_duty_path = create_path(sue_dutys_dir, f"{bob_str}.json")
    x_job_path = create_path(sue_jobs_dir, f"{bob_str}.json")
    x_grade_path = create_path(sue_grades_dir, f"{bob_str}.json")
    assert sue_hubunit.duty_path(bob_str) == x_duty_path
    assert sue_hubunit.job_path(bob_str) == x_job_path
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
        == f"'{bob_str}' needs to be a TitleUnit. Cannot contain bridge: '{slash_str}'"
    )


def test_get_keep_path_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    peru_str = "peru"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title=peru_str, owner_name=sue_str)
    texas_str = "texas"
    dallas_str = "dallas"
    elpaso_str = "el paso"
    kern_str = "kern"
    itemroot = "itemroot"
    texas_road = create_road_from_titles([itemroot, texas_str])
    dallas_road = create_road_from_titles([itemroot, texas_str, dallas_str])
    elpaso_road = create_road_from_titles([itemroot, texas_str, elpaso_str])
    kern_road = create_road_from_titles([itemroot, texas_str, elpaso_str, kern_str])

    # WHEN
    texas_path = get_keep_path(sue_hubunit, texas_road)
    dallas_path = get_keep_path(sue_hubunit, dallas_road)
    elpaso_path = get_keep_path(sue_hubunit, elpaso_road)
    kern_path = get_keep_path(sue_hubunit, kern_road)

    # THEN
    itemroot_dir = create_path(sue_hubunit._keeps_dir, itemroot)
    print(f"{kern_road=}")
    print(f"{itemroot_dir=}")
    assert texas_path == create_path(itemroot_dir, texas_str)
    assert dallas_path == create_path(texas_path, dallas_str)
    assert elpaso_path == create_path(texas_path, elpaso_str)
    assert kern_path == create_path(elpaso_path, kern_str)

    # WHEN / THEN
    diff_root_texas_road = create_road_from_titles([peru_str, texas_str])
    diff_root_dallas_road = create_road_from_titles([peru_str, texas_str, dallas_str])
    diff_root_elpaso_road = create_road_from_titles([peru_str, texas_str, elpaso_str])
    assert texas_path == get_keep_path(sue_hubunit, diff_root_texas_road)
    assert dallas_path == get_keep_path(sue_hubunit, diff_root_dallas_road)
    assert elpaso_path == get_keep_path(sue_hubunit, diff_root_elpaso_road)
