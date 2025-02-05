from src.f00_instrument.file import create_path
from src.f01_road.road import (
    default_bridge_if_None,
    create_road_from_titles,
    create_road,
    get_default_fiscal_title as root_title,
)
from src.f01_road.finance import (
    default_respect_bit_if_None,
    default_penny_if_None,
    default_fund_coin_if_None,
    validate_fund_pool,
)
from src.f01_road.jaar_config import (
    get_gifts_folder,
    get_test_fiscals_dir,
    get_rootpart_of_keep_dir,
    get_fiscal_title_if_None,
)
from src.f02_bud.bud import budunit_shop
from src.f05_listen.hub_tool import create_timeline_dir
from src.f05_listen.hubunit import HubUnit, hubunit_shop, get_keep_path
from src.f05_listen.examples.example_listen_buds import get_budunit_with_4_levels
from src.f05_listen.examples.listen_env import (
    get_listen_temp_env_dir as env_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_get_keep_path_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    peru_str = "peru"
    sue_hubunit = hubunit_shop(env_dir(), fiscal_title=peru_str, owner_name=sue_str)
    texas_str = "texas"
    dallas_str = "dallas"
    elpaso_str = "el paso"
    kern_str = "kern"
    itemroot = get_rootpart_of_keep_dir()
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
    # itemroot_dir = f"{sue_hubunit._keeps_dir}/{get_rootpart_of_keep_dir()}"
    itemroot_dir = create_path(sue_hubunit._keeps_dir, get_rootpart_of_keep_dir())
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


def test_HubUnit_Exists():
    # ESTABLISH / WHEN
    x_hubunit = HubUnit()

    # THEN
    assert not x_hubunit.fiscals_dir
    assert not x_hubunit.fiscal_title
    assert not x_hubunit.owner_name
    assert not x_hubunit.keep_road
    assert not x_hubunit.bridge
    assert not x_hubunit.fund_pool
    assert not x_hubunit.fund_coin
    assert not x_hubunit.respect_bit
    assert not x_hubunit.penny
    assert not x_hubunit.keep_point_magnitude
    assert not x_hubunit._fiscal_dir
    assert not x_hubunit._owners_dir
    assert not x_hubunit._owner_dir
    assert not x_hubunit._keeps_dir
    assert not x_hubunit._atoms_dir
    assert not x_hubunit._soul_dir
    assert not x_hubunit._voice_dir
    assert not x_hubunit._timeline_dir
    assert not x_hubunit._gifts_dir
    assert not x_hubunit._soul_file_name
    assert not x_hubunit._soul_file_path
    assert not x_hubunit._voice_file_name
    assert not x_hubunit._voice_path


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
    x_fiscals_dir = "src/f07_fiscal/examples"
    x_fiscal_title = "accord45"
    sue_str = "Sue"
    x_bridge = "/"
    x_fund_pool = 13000
    x_fund_coin = 13
    x_respect_bit = 9
    x_penny = 3
    x_money_magnitude = 900

    # WHEN
    x_hubunit = hubunit_shop(
        fiscals_dir=x_fiscals_dir,
        fiscal_title=x_fiscal_title,
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
    assert x_hubunit.fiscals_dir == x_fiscals_dir
    assert x_hubunit.fiscal_title == x_fiscal_title
    assert x_hubunit.owner_name == sue_str
    assert x_hubunit.bridge == x_bridge
    assert x_hubunit.fund_pool == x_fund_pool
    assert x_hubunit.fund_coin == x_fund_coin
    assert x_hubunit.respect_bit == x_respect_bit
    assert x_hubunit.penny == x_penny
    assert x_hubunit.keep_point_magnitude == x_money_magnitude
    assert x_hubunit._fiscal_dir == create_path(x_fiscals_dir, x_fiscal_title)
    assert x_hubunit._owners_dir == create_path(x_hubunit._fiscal_dir, "owners")
    assert x_hubunit._owner_dir == create_path(x_hubunit._owners_dir, sue_str)
    assert x_hubunit._keeps_dir == create_path(x_hubunit._owner_dir, "keeps")
    assert x_hubunit._atoms_dir == create_path(x_hubunit._owner_dir, "atoms")
    assert x_hubunit._soul_dir == create_path(x_hubunit._owner_dir, "soul")
    assert x_hubunit._voice_dir == create_path(x_hubunit._owner_dir, "voice")
    assert x_hubunit._timeline_dir == create_path(x_hubunit._owner_dir, "timeline")
    func_timeline_dir = create_timeline_dir(
        x_fiscals_dir, x_fiscal_title, x_hubunit.owner_name
    )
    print(f"{x_hubunit._timeline_dir=}")
    print(f"{func_timeline_dir=}")
    assert x_hubunit._timeline_dir == func_timeline_dir
    assert x_hubunit._gifts_dir == create_path(x_hubunit._owner_dir, get_gifts_folder())
    assert x_hubunit._soul_file_name == f"{sue_str}.json"
    x_soul_file_path = create_path(x_hubunit._soul_dir, x_hubunit._soul_file_name)
    assert x_hubunit._soul_file_path == x_soul_file_path
    assert x_hubunit._voice_file_name == f"{sue_str}.json"
    x_voicepath = create_path(x_hubunit._voice_dir, x_hubunit._voice_file_name)
    assert x_hubunit._voice_path == x_voicepath


def test_hubunit_shop_ReturnsObjWhenEmpty():
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation-state"
    nation_road = create_road(root_title(), nation_str)
    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    texas_str = "Texas"
    texas_road = create_road(usa_road, texas_str)
    fiscals_dir = get_test_fiscals_dir()
    accord23_str = "accord23"

    # WHEN
    sue_hubunit = hubunit_shop(fiscals_dir, accord23_str, sue_str, texas_road)

    # THEN
    x_fiscal_path = create_path(fiscals_dir, accord23_str)
    x_owners_path = create_path(sue_hubunit._fiscal_dir, "owners")
    x_dutys_path = create_path(sue_hubunit.keep_dir(), "dutys")
    x_jobs_path = create_path(sue_hubunit.keep_dir(), "jobs")
    x_grades_path = create_path(sue_hubunit.keep_dir(), "grades")

    assert sue_hubunit.fiscals_dir == fiscals_dir
    assert sue_hubunit.fiscal_title == accord23_str
    assert sue_hubunit._fiscal_dir == x_fiscal_path
    assert sue_hubunit.owner_name == sue_str
    assert sue_hubunit.bridge == default_bridge_if_None()
    assert sue_hubunit.fund_pool == validate_fund_pool()
    assert sue_hubunit.fund_coin == default_fund_coin_if_None()
    assert sue_hubunit.respect_bit == default_respect_bit_if_None()
    assert sue_hubunit.penny == default_penny_if_None()
    assert sue_hubunit._owners_dir == x_owners_path
    x_hubunit = hubunit_shop(fiscals_dir, accord23_str, sue_str)
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
    treasury_file_name = "treasury.db"
    x_treasury_file_path = create_path(sue_hubunit.keep_dir(), treasury_file_name)
    assert sue_hubunit.treasury_file_name() == treasury_file_name
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


def test_HubUnit_save_file_soul_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str)
    assert os_path_exists(sue_hubunit._soul_file_path) is False

    # WHEN
    sue_hubunit.save_file_soul(file_str="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_hubunit._soul_file_path)


def test_HubUnit_soul_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str)
    assert sue_hubunit.soul_file_exists() is False

    # WHEN
    sue_hubunit.save_file_soul(file_str="fooboo", replace=True)

    # THEN
    assert sue_hubunit.soul_file_exists()


def test_HubUnit_open_file_soul_OpensFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str)
    example_str = "fooboo"
    sue_hubunit.save_file_soul(example_str, replace=True)

    # WHEN / THEN
    assert sue_hubunit.open_file_soul() == example_str


def test_HubUnit_save_file_voice_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str)
    assert os_path_exists(sue_hubunit._voice_path) is False

    # WHEN
    sue_hubunit.save_file_voice(file_str="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_hubunit._voice_path)


def test_HubUnit_voice_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str)
    assert sue_hubunit.voice_file_exists() is False

    # WHEN
    sue_hubunit.save_file_voice(file_str="fooboo", replace=True)

    # THEN
    assert sue_hubunit.voice_file_exists()


def test_HubUnit_open_file_voice_OpensFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str)
    example_str = "fooboo"
    sue_hubunit.save_file_voice(example_str, replace=True)

    # WHEN / THEN
    assert sue_hubunit.open_file_voice() == example_str


def test_HubUnit_save_soul_bud_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels()
    sue_str = sue_budunit.owner_name
    fiscal_title = root_title()
    sue_hubunit = hubunit_shop(env_dir(), fiscal_title, sue_str, None)

    print(f"{sue_hubunit._soul_file_path=}")
    assert sue_hubunit.soul_file_exists() is False

    # WHEN
    sue_hubunit.save_soul_bud(sue_budunit)

    # THEN
    assert sue_hubunit.soul_file_exists()


def test_HubUnit_save_soul_bud_RaisesErrorWhenBud_voice_id_IsWrong(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"

    fiscal_title = root_title()
    sue_hubunit = hubunit_shop(env_dir(), fiscal_title, sue_str, None)

    # WHEN / THEN
    yao_str = "Yao"
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_soul_bud(budunit_shop(yao_str))
    assert (
        str(excinfo.value)
        == f"BudUnit with owner_name '{yao_str}' cannot be saved as owner_name '{sue_str}''s soul bud."
    )


def test_HubUnit_get_soul_bud_OpensFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels()
    sue_str = sue_budunit.owner_name
    nation_str = "nation-state"
    nation_road = create_road(root_title(), nation_str)
    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    texas_str = "Texas"
    texas_road = create_road(usa_road, texas_str)
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_road)
    sue_hubunit.save_soul_bud(sue_budunit)

    # WHEN / THEN
    assert sue_hubunit.get_soul_bud().get_dict() == sue_budunit.get_dict()


def test_HubUnit_save_voice_bud_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels()
    sue_str = sue_budunit.owner_name

    fiscal_title = root_title()
    sue_hubunit = hubunit_shop(env_dir(), fiscal_title, sue_str, None)

    print(f"{sue_hubunit._voice_path=}")
    assert sue_hubunit.voice_file_exists() is False

    # WHEN
    sue_hubunit.save_voice_bud(sue_budunit)

    # THEN
    assert sue_hubunit.voice_file_exists()


def test_HubUnit_get_voice_bud_OpensFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels()
    sue_str = sue_budunit.owner_name
    nation_str = "nation-state"
    nation_road = create_road(root_title(), nation_str)
    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    texas_str = "Texas"
    texas_road = create_road(usa_road, texas_str)
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_road)
    sue_hubunit.save_voice_bud(sue_budunit)

    # WHEN / THEN
    assert sue_hubunit.get_voice_bud().get_dict() == sue_budunit.get_dict()


def test_HubUnit_get_voice_bud_ReturnsNoneIfFileDoesNotExist(env_dir_setup_cleanup):
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels()
    sue_str = sue_budunit.owner_name
    a23_str = "accord23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str)

    # WHEN / THEN
    assert sue_hubunit.get_voice_bud() is None


def test_HubUnit_save_voice_bud_RaisesErrorWhenBud_voice_id_IsWrong(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"

    fiscal_title = root_title()
    sue_hubunit = hubunit_shop(env_dir(), fiscal_title, sue_str, None)

    # WHEN / THEN
    yao_str = "Yao"
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_voice_bud(budunit_shop(yao_str))
    assert (
        str(excinfo.value)
        == f"BudUnit with owner_name '{yao_str}' cannot be saved as owner_name '{sue_str}''s voice bud."
    )
