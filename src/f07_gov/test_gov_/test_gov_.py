from src.f00_instrument.file import create_path
from src.f01_road.finance import (
    default_fund_coin_if_None,
    default_respect_bit_if_None,
    default_penny_if_None,
)
from src.f01_road.jaar_config import (
    get_gifts_folder,
    get_json_filename,
    get_test_gov_idea,
)
from src.f01_road.road import default_bridge_if_None
from src.f01_road.finance_tran import tranbook_shop
from src.f02_bud.healer import healerlink_shop
from src.f02_bud.item import itemunit_shop
from src.f03_chrono.chrono import timelineunit_shop
from src.f05_listen.hubunit import hubunit_shop
from src.f07_gov.gov import GovUnit, govunit_shop
from src.f07_gov.examples.gov_env import (
    get_test_govs_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists, isdir as os_path_isdir


def test_GovUnit_Exists(env_dir_setup_cleanup):
    accord45_str = "accord45"
    accord_gov = GovUnit()
    assert not accord_gov.gov_idea
    assert not accord_gov.timeline
    assert not accord_gov.current_time
    assert not accord_gov.deallogs
    assert not accord_gov.cashbook
    assert not accord_gov.bridge
    assert not accord_gov.fund_coin
    assert not accord_gov.respect_bit
    assert not accord_gov.penny
    assert not accord_gov.govs_dir
    # Calculated fields
    assert not accord_gov._owners_dir
    assert not accord_gov._journal_db
    assert not accord_gov._gifts_dir
    assert not accord_gov._all_tranbook


def test_govunit_shop_ReturnsGovUnit():
    # ESTABLISH / WHEN
    accord_gov = govunit_shop()

    # THEN
    assert accord_gov.gov_idea == get_test_gov_idea()
    assert accord_gov.timeline == timelineunit_shop()
    assert accord_gov.current_time == 0
    assert accord_gov.deallogs == {}
    assert accord_gov.cashbook == tranbook_shop(get_test_gov_idea())
    assert accord_gov.bridge == default_bridge_if_None()
    assert accord_gov.fund_coin == default_fund_coin_if_None()
    assert accord_gov.respect_bit == default_respect_bit_if_None()
    assert accord_gov.penny == default_penny_if_None()
    assert accord_gov.govs_dir == get_test_govs_dir()
    # Calculated fields
    assert accord_gov._owners_dir != None
    assert accord_gov._gifts_dir != None
    assert accord_gov._all_tranbook == tranbook_shop(get_test_gov_idea())


def test_govunit_shop_ReturnsGovUnitWith_govs_dir(env_dir_setup_cleanup):
    # ESTABLISH
    accord45_str = "accord45"

    # WHEN
    accord_gov = govunit_shop(accord45_str, govs_dir=get_test_govs_dir())

    # THEN
    assert accord_gov.gov_idea == accord45_str
    assert accord_gov.govs_dir == get_test_govs_dir()
    assert accord_gov._owners_dir is not None
    assert accord_gov._gifts_dir is not None


def test_govunit_shop_ReturnsGovUnitWith_bridge(env_dir_setup_cleanup):
    # ESTABLISH
    accord45_str = "accord45"
    slash_str = "/"
    x_fund_coin = 7.0
    x_respect_bit = 9
    x_penny = 3
    x_current_time = 78000000

    # WHEN
    accord_gov = govunit_shop(
        gov_idea=accord45_str,
        govs_dir=get_test_govs_dir(),
        current_time=x_current_time,
        in_memory_journal=True,
        bridge=slash_str,
        fund_coin=x_fund_coin,
        respect_bit=x_respect_bit,
        penny=x_penny,
    )

    # THEN
    assert accord_gov.current_time == x_current_time
    assert accord_gov.bridge == slash_str
    assert accord_gov.fund_coin == x_fund_coin
    assert accord_gov.respect_bit == x_respect_bit
    assert accord_gov.penny == x_penny


def test_GovUnit_set_gov_dirs_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    accord45_str = "accord45"
    accord_gov = GovUnit(gov_idea=accord45_str, govs_dir=get_test_govs_dir())
    x_gov_dir = create_path(get_test_govs_dir(), accord45_str)
    x_owners_dir = create_path(x_gov_dir, "owners")
    x_gifts_dir = create_path(x_gov_dir, get_gifts_folder())
    journal_file_name = "journal.db"
    journal_file_path = create_path(x_gov_dir, journal_file_name)

    assert accord_gov._gov_dir is None
    assert accord_gov._owners_dir is None
    assert accord_gov._gifts_dir is None
    assert os_path_exists(x_gov_dir) is False
    assert os_path_isdir(x_gov_dir) is False
    assert os_path_exists(x_owners_dir) is False
    assert os_path_exists(x_gifts_dir) is False
    assert os_path_exists(journal_file_path) is False

    # WHEN
    accord_gov._set_gov_dirs()

    # THEN
    assert accord_gov._gov_dir == x_gov_dir
    assert accord_gov._owners_dir == x_owners_dir
    assert accord_gov._gifts_dir == x_gifts_dir
    assert os_path_exists(x_gov_dir)
    assert os_path_isdir(x_gov_dir)
    assert os_path_exists(x_owners_dir)
    assert os_path_exists(x_gifts_dir)
    assert os_path_exists(journal_file_path)


def test_govunit_shop_SetsgovsDirs(env_dir_setup_cleanup):
    # ESTABLISH
    accord45_str = "accord45"

    # WHEN
    accord_gov = govunit_shop(accord45_str, get_test_govs_dir(), in_memory_journal=True)

    # THEN
    assert accord_gov.gov_idea == accord45_str
    assert accord_gov._gov_dir == create_path(get_test_govs_dir(), accord45_str)
    assert accord_gov._owners_dir == create_path(accord_gov._gov_dir, "owners")


def test_GovUnit_init_owner_keeps_CorrectlySetsDirAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    accord45_str = "accord45"
    slash_str = "/"
    x_fund_coin = 4
    x_respect_bit = 5
    accord_gov = govunit_shop(
        accord45_str,
        get_test_govs_dir(),
        bridge=slash_str,
        fund_coin=x_fund_coin,
        respect_bit=x_respect_bit,
        in_memory_journal=True,
    )
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(
        None,
        accord45_str,
        sue_str,
        None,
        respect_bit=x_respect_bit,
        fund_coin=x_fund_coin,
    )
    assert os_path_exists(sue_hubunit.final_path()) is False

    # WHEN
    accord_gov.init_owner_keeps(sue_str)

    # THEN
    print(f"{get_test_govs_dir()=}")
    assert os_path_exists(sue_hubunit.final_path())


def test_GovUnit_get_owner_voice_from_file_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    accord45_str = "accord45"
    accord_gov = govunit_shop(accord45_str, get_test_govs_dir(), in_memory_journal=True)
    sue_str = "Sue"
    accord_gov.init_owner_keeps(sue_str)
    sue_hubunit = hubunit_shop(None, accord45_str, sue_str, None)
    bob_str = "Bob"
    sue_voice = sue_hubunit.get_voice_bud()
    sue_voice.add_acctunit(bob_str)
    sue_hubunit.save_voice_bud(sue_voice)

    # WHEN
    gen_sue_voice = accord_gov.get_owner_voice_from_file(sue_str)

    # THEN
    assert gen_sue_voice is not None
    assert gen_sue_voice.acct_exists(bob_str)


def test_GovUnit__set_all_healer_dutys_CorrectlySetsdutys(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord45_str = "accord45"
    accord_gov = govunit_shop(accord45_str, get_test_govs_dir(), in_memory_journal=True)
    sue_str = "Sue"
    yao_str = "Yao"
    accord_gov.init_owner_keeps(sue_str)
    accord_gov.init_owner_keeps(yao_str)
    sue_hubunit = hubunit_shop(None, accord45_str, sue_str, None)
    yao_hubunit = hubunit_shop(None, accord45_str, yao_str, None)
    sue_voice_bud = sue_hubunit.get_voice_bud()
    yao_voice_bud = yao_hubunit.get_voice_bud()

    sue_voice_bud.add_acctunit(sue_str)
    sue_voice_bud.add_acctunit(yao_str)
    yao_voice_bud.add_acctunit(sue_str)
    yao_voice_bud.add_acctunit(yao_str)
    texas_str = "Texas"
    texas_road = sue_voice_bud.make_l1_road(texas_str)
    sue_voice_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    yao_voice_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_road = sue_voice_bud.make_road(texas_road, dallas_str)
    dallas_healerlink = healerlink_shop({sue_str, yao_str})
    dallas_item = itemunit_shop(dallas_str, healerlink=dallas_healerlink)
    elpaso_str = "el paso"
    elpaso_road = sue_voice_bud.make_road(texas_road, elpaso_str)
    elpaso_healerlink = healerlink_shop({sue_str})
    elpaso_item = itemunit_shop(elpaso_str, healerlink=elpaso_healerlink)

    sue_voice_bud.set_item(dallas_item, texas_road)
    sue_voice_bud.set_item(elpaso_item, texas_road)
    yao_voice_bud.set_item(dallas_item, texas_road)
    yao_voice_bud.set_item(elpaso_item, texas_road)

    sue_hubunit.save_voice_bud(sue_voice_bud)
    yao_hubunit.save_voice_bud(yao_voice_bud)
    sue_file_name = get_json_filename(sue_str)
    yao_file_name = get_json_filename(yao_str)
    sue_dallas_hubunit = hubunit_shop(None, accord45_str, sue_str, dallas_road)
    yao_dallas_hubunit = hubunit_shop(None, accord45_str, yao_str, dallas_road)
    sue_dutys_dir = sue_dallas_hubunit.dutys_dir()
    yao_dutys_dir = yao_dallas_hubunit.dutys_dir()
    sue_dallas_sue_duty_file_path = f"{sue_dutys_dir}/{sue_file_name}"
    sue_dallas_yao_duty_file_path = f"{sue_dutys_dir}/{yao_file_name}"
    yao_dallas_sue_duty_file_path = f"{yao_dutys_dir}/{sue_file_name}"
    yao_dallas_yao_duty_file_path = f"{yao_dutys_dir}/{yao_file_name}"
    assert os_path_exists(sue_dallas_sue_duty_file_path) is False
    assert os_path_exists(sue_dallas_yao_duty_file_path) is False
    assert os_path_exists(yao_dallas_sue_duty_file_path) is False
    assert os_path_exists(yao_dallas_yao_duty_file_path) is False

    # WHEN
    accord_gov._set_all_healer_dutys(sue_str)

    # THEN
    assert os_path_exists(sue_dallas_sue_duty_file_path)
    assert os_path_exists(sue_dallas_yao_duty_file_path) is False
    assert os_path_exists(yao_dallas_sue_duty_file_path)
    assert os_path_exists(yao_dallas_yao_duty_file_path) is False

    # WHEN
    accord_gov._set_all_healer_dutys(yao_str)

    # THEN
    assert os_path_exists(sue_dallas_sue_duty_file_path)
    assert os_path_exists(sue_dallas_yao_duty_file_path)
    assert os_path_exists(yao_dallas_sue_duty_file_path)
    assert os_path_exists(yao_dallas_yao_duty_file_path)


def test_GovUnit_get_owner_hubunits_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    accord_gov = govunit_shop("accord45", get_test_govs_dir(), in_memory_journal=True)
    sue_str = "Sue"
    yao_str = "Yao"

    # WHEN / THEN
    assert len(accord_gov.get_owner_hubunits()) == 0

    # WHEN
    accord_gov.init_owner_keeps(sue_str)
    accord_gov.init_owner_keeps(yao_str)
    accord_all_owners = accord_gov.get_owner_hubunits()

    # THEN
    sue_hubunit = hubunit_shop(
        govs_dir=accord_gov.govs_dir,
        gov_idea=accord_gov.gov_idea,
        owner_name=sue_str,
        keep_road=None,
        bridge=accord_gov.bridge,
        fund_coin=accord_gov.fund_coin,
        respect_bit=accord_gov.respect_bit,
    )
    yao_hubunit = hubunit_shop(
        govs_dir=accord_gov.govs_dir,
        gov_idea=accord_gov.gov_idea,
        owner_name=yao_str,
        keep_road=None,
        bridge=accord_gov.bridge,
        fund_coin=accord_gov.fund_coin,
        respect_bit=accord_gov.respect_bit,
    )
    assert accord_all_owners.get(sue_str) == sue_hubunit
    assert accord_all_owners.get(yao_str) == yao_hubunit
    assert len(accord_gov.get_owner_hubunits()) == 2
