from src.f00_instrument.file import create_path
from src.f01_road.road import (
    default_bridge_if_None,
    create_road_from_ideas,
    create_road,
    get_default_deal_idea as root_idea,
)
from src.f01_road.finance import (
    default_respect_bit_if_None,
    default_penny_if_None,
    default_fund_coin_if_None,
    validate_fund_pool,
)
from src.f01_road.jaar_config import (
    get_gifts_folder,
    get_test_deals_dir,
    get_rootpart_of_keep_dir,
    get_deal_idea_if_None,
)
from src.f02_bud.bud import budunit_shop
from src.f05_listen.hubunit import HubUnit, hubunit_shop, get_keep_path
from src.f05_listen.examples.example_listen_buds import get_budunit_with_4_levels
from src.f05_listen.examples.listen_env import (
    get_listen_temp_env_dir as env_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_get_keep_path_ReturnsCorrectObj():
    # ESTABLISH
    sue_str = "Sue"
    peru_str = "peru"
    sue_hubunit = hubunit_shop(None, deal_idea=peru_str, owner_name=sue_str)
    texas_str = "texas"
    dallas_str = "dallas"
    elpaso_str = "el paso"
    kern_str = "kern"
    itemroot = get_rootpart_of_keep_dir()
    texas_road = create_road_from_ideas([itemroot, texas_str])
    dallas_road = create_road_from_ideas([itemroot, texas_str, dallas_str])
    elpaso_road = create_road_from_ideas([itemroot, texas_str, elpaso_str])
    kern_road = create_road_from_ideas([itemroot, texas_str, elpaso_str, kern_str])

    # WHEN
    texas_path = get_keep_path(sue_hubunit, texas_road)
    dallas_path = get_keep_path(sue_hubunit, dallas_road)
    elpaso_path = get_keep_path(sue_hubunit, elpaso_road)
    kern_path = get_keep_path(sue_hubunit, kern_road)

    # THEN
    # itemroot_dir = f"{sue_hubunit.keeps_dir()}/{get_rootpart_of_keep_dir()}"
    itemroot_dir = create_path(sue_hubunit.keeps_dir(), get_rootpart_of_keep_dir())
    print(f"{kern_road=}")
    print(f"{itemroot_dir=}")
    assert texas_path == create_path(itemroot_dir, texas_str)
    assert dallas_path == create_path(texas_path, dallas_str)
    assert elpaso_path == create_path(texas_path, elpaso_str)
    assert kern_path == create_path(elpaso_path, kern_str)

    # WHEN / THEN
    diff_root_texas_road = create_road_from_ideas([peru_str, texas_str])
    diff_root_dallas_road = create_road_from_ideas([peru_str, texas_str, dallas_str])
    diff_root_elpaso_road = create_road_from_ideas([peru_str, texas_str, elpaso_str])
    assert texas_path == get_keep_path(sue_hubunit, diff_root_texas_road)
    assert dallas_path == get_keep_path(sue_hubunit, diff_root_dallas_road)
    assert elpaso_path == get_keep_path(sue_hubunit, diff_root_elpaso_road)


def test_HubUnit_Exists():
    # ESTABLISH / WHEN
    x_hubunit = HubUnit()

    # THEN
    assert x_hubunit.deals_dir is None
    assert x_hubunit.deal_idea is None
    assert x_hubunit.owner_name is None
    assert x_hubunit.keep_road is None
    assert x_hubunit.bridge is None
    assert x_hubunit.fund_pool is None
    assert x_hubunit.fund_coin is None
    assert x_hubunit.respect_bit is None
    assert x_hubunit.penny is None
    assert x_hubunit.keep_point_magnitude is None


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


def test_hubunit_shop_ReturnsCorrectObj():
    # ESTABLISH
    x_deals_dir = "src/f07_deal/examples"
    x_deal_idea = "accord45"
    sue_str = "Sue"
    x_bridge = "/"
    x_fund_pool = 13000
    x_fund_coin = 13
    x_respect_bit = 9
    x_penny = 3
    x_money_magnitude = 900

    # WHEN
    x_hubunit = hubunit_shop(
        deals_dir=x_deals_dir,
        deal_idea=x_deal_idea,
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
    assert x_hubunit.deals_dir == x_deals_dir
    assert x_hubunit.deal_idea == x_deal_idea
    assert x_hubunit.owner_name == sue_str
    assert x_hubunit.bridge == x_bridge
    assert x_hubunit.fund_pool == x_fund_pool
    assert x_hubunit.fund_coin == x_fund_coin
    assert x_hubunit.respect_bit == x_respect_bit
    assert x_hubunit.penny == x_penny
    assert x_hubunit.keep_point_magnitude == x_money_magnitude
    assert x_hubunit.deal_dir() == create_path(x_deals_dir, x_deal_idea)
    assert x_hubunit.owners_dir() == create_path(x_hubunit.deal_dir(), "owners")
    assert x_hubunit.owner_dir() == create_path(x_hubunit.owners_dir(), sue_str)
    assert x_hubunit.keeps_dir() == create_path(x_hubunit.owner_dir(), "keeps")
    assert x_hubunit.atoms_dir() == create_path(x_hubunit.owner_dir(), "atoms")
    assert x_hubunit.voice_dir() == create_path(x_hubunit.owner_dir(), "voice")
    assert x_hubunit.final_dir() == create_path(x_hubunit.owner_dir(), "final")
    assert x_hubunit.timeline_dir() == create_path(x_hubunit.owner_dir(), "timeline")
    assert x_hubunit.gifts_dir() == create_path(
        x_hubunit.owner_dir(), get_gifts_folder()
    )
    assert x_hubunit.voice_file_name() == f"{sue_str}.json"
    x_voice_file_path = create_path(x_hubunit.voice_dir(), x_hubunit.voice_file_name())
    assert x_hubunit.voice_file_path() == x_voice_file_path
    assert x_hubunit.final_file_name() == f"{sue_str}.json"
    x_finalpath = create_path(x_hubunit.final_dir(), x_hubunit.final_file_name())
    assert x_hubunit.final_path() == x_finalpath


def test_hubunit_shop_ReturnsCorrectObjWhenEmpty():
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation-state"
    nation_road = create_road(root_idea(), nation_str)
    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    texas_str = "Texas"
    texas_road = create_road(usa_road, texas_str)

    # WHEN
    sue_hubunit = hubunit_shop(None, None, sue_str, texas_road)

    # THEN
    x_deal_path = create_path(get_test_deals_dir(), get_deal_idea_if_None())
    x_owners_path = create_path(sue_hubunit.deal_dir(), "owners")
    x_dutys_path = create_path(sue_hubunit.keep_dir(), "dutys")
    x_jobs_path = create_path(sue_hubunit.keep_dir(), "jobs")
    x_grades_path = create_path(sue_hubunit.keep_dir(), "grades")

    assert sue_hubunit.deals_dir == get_test_deals_dir()
    assert sue_hubunit.deal_idea == get_deal_idea_if_None()
    assert sue_hubunit.deal_dir() == x_deal_path
    assert sue_hubunit.owner_name == sue_str
    assert sue_hubunit.bridge == default_bridge_if_None()
    assert sue_hubunit.fund_pool == validate_fund_pool()
    assert sue_hubunit.fund_coin == default_fund_coin_if_None()
    assert sue_hubunit.respect_bit == default_respect_bit_if_None()
    assert sue_hubunit.penny == default_penny_if_None()
    assert sue_hubunit.owners_dir() == x_owners_path
    x_hubunit = hubunit_shop(None, None, sue_str)
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
        == f"'{bob_str}' needs to be a IdeaUnit. Cannot contain bridge: '{slash_str}'"
    )


def test_HubUnit_save_file_voice_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str)
    assert os_path_exists(sue_hubunit.voice_file_path()) is False

    # WHEN
    sue_hubunit.save_file_voice(file_str="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_hubunit.voice_file_path())


def test_HubUnit_voice_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str)
    assert sue_hubunit.voice_file_exists() is False

    # WHEN
    sue_hubunit.save_file_voice(file_str="fooboo", replace=True)

    # THEN
    assert sue_hubunit.voice_file_exists()


def test_HubUnit_open_file_voice_OpensFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str)
    example_str = "fooboo"
    sue_hubunit.save_file_voice(example_str, replace=True)

    # WHEN / THEN
    assert sue_hubunit.open_file_voice() == example_str


def test_HubUnit_save_file_final_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str)
    assert os_path_exists(sue_hubunit.final_path()) is False

    # WHEN
    sue_hubunit.save_file_final(file_str="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_hubunit.final_path())


def test_HubUnit_final_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str)
    assert sue_hubunit.final_file_exists() is False

    # WHEN
    sue_hubunit.save_file_final(file_str="fooboo", replace=True)

    # THEN
    assert sue_hubunit.final_file_exists()


def test_HubUnit_open_file_final_OpensFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str)
    example_str = "fooboo"
    sue_hubunit.save_file_final(example_str, replace=True)

    # WHEN / THEN
    assert sue_hubunit.open_file_final() == example_str


def test_HubUnit_save_voice_bud_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels()
    sue_str = sue_budunit.owner_name
    deal_idea = root_idea()
    sue_hubunit = hubunit_shop(env_dir(), deal_idea, sue_str, None)

    print(f"{sue_hubunit.voice_file_path()=}")
    assert sue_hubunit.voice_file_exists() is False

    # WHEN
    sue_hubunit.save_voice_bud(sue_budunit)

    # THEN
    assert sue_hubunit.voice_file_exists()


def test_HubUnit_save_voice_bud_RaisesErrorWhenBud_final_id_IsWrong(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"

    deal_idea = root_idea()
    sue_hubunit = hubunit_shop(env_dir(), deal_idea, sue_str, None)

    # WHEN / THEN
    yao_str = "Yao"
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_voice_bud(budunit_shop(yao_str))
    assert (
        str(excinfo.value)
        == f"BudUnit with owner_name '{yao_str}' cannot be saved as owner_name '{sue_str}''s voice bud."
    )


def test_HubUnit_get_voice_bud_OpensFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels()
    sue_str = sue_budunit.owner_name
    nation_str = "nation-state"
    nation_road = create_road(root_idea(), nation_str)
    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    texas_str = "Texas"
    texas_road = create_road(usa_road, texas_str)
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str, texas_road)
    sue_hubunit.save_voice_bud(sue_budunit)

    # WHEN / THEN
    assert sue_hubunit.get_voice_bud().get_dict() == sue_budunit.get_dict()


def test_HubUnit_save_final_bud_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels()
    sue_str = sue_budunit.owner_name

    deal_idea = root_idea()
    sue_hubunit = hubunit_shop(env_dir(), deal_idea, sue_str, None)

    print(f"{sue_hubunit.final_path()=}")
    assert sue_hubunit.final_file_exists() is False

    # WHEN
    sue_hubunit.save_final_bud(sue_budunit)

    # THEN
    assert sue_hubunit.final_file_exists()


def test_HubUnit_get_final_bud_OpensFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels()
    sue_str = sue_budunit.owner_name
    nation_str = "nation-state"
    nation_road = create_road(root_idea(), nation_str)
    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    texas_str = "Texas"
    texas_road = create_road(usa_road, texas_str)
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str, texas_road)
    sue_hubunit.save_final_bud(sue_budunit)

    # WHEN / THEN
    assert sue_hubunit.get_final_bud().get_dict() == sue_budunit.get_dict()


def test_HubUnit_get_final_bud_ReturnsNoneIfFileDoesNotExist(env_dir_setup_cleanup):
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels()
    sue_str = sue_budunit.owner_name
    sue_hubunit = hubunit_shop(env_dir(), None, sue_str)

    # WHEN / THEN
    assert sue_hubunit.get_final_bud() is None


def test_HubUnit_save_final_bud_RaisesErrorWhenBud_final_id_IsWrong(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"

    deal_idea = root_idea()
    sue_hubunit = hubunit_shop(env_dir(), deal_idea, sue_str, None)

    # WHEN / THEN
    yao_str = "Yao"
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_final_bud(budunit_shop(yao_str))
    assert (
        str(excinfo.value)
        == f"BudUnit with owner_name '{yao_str}' cannot be saved as owner_name '{sue_str}''s final bud."
    )
