from src.f00_instrument.file import create_path
from src.f01_road.finance import (
    default_fund_coin_if_None,
    default_respect_bit_if_None,
    default_penny_if_None,
)
from src.f01_road.jaar_config import (
    get_gifts_folder,
    get_json_filename,
    get_test_deal_id,
)
from src.f01_road.road import default_bridge_if_None
from src.f01_road.finance_tran import tranbook_shop
from src.f02_bud.healer import healerlink_shop
from src.f02_bud.item import itemunit_shop
from src.f03_chrono.chrono import timelineunit_shop
from src.f05_listen.hubunit import hubunit_shop
from src.f07_deal.deal import DealUnit, dealunit_shop
from src.f07_deal.examples.deal_env import (
    get_test_deals_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists, isdir as os_path_isdir


def test_DealUnit_Exists(env_dir_setup_cleanup):
    music_str = "music"
    music_deal = DealUnit()
    assert not music_deal.deal_id
    assert not music_deal.timeline
    assert not music_deal.current_time
    assert not music_deal.purviewlogs
    assert not music_deal.cashbook
    assert not music_deal.bridge
    assert not music_deal.fund_coin
    assert not music_deal.respect_bit
    assert not music_deal.penny
    assert not music_deal.deals_dir
    # Calculated fields
    assert not music_deal._owners_dir
    assert not music_deal._journal_db
    assert not music_deal._gifts_dir
    assert not music_deal._all_tranbook


def test_dealunit_shop_ReturnsDealUnit():
    # ESTABLISH / WHEN
    music_deal = dealunit_shop()

    # THEN
    assert music_deal.deal_id == get_test_deal_id()
    assert music_deal.timeline == timelineunit_shop()
    assert music_deal.current_time == 0
    assert music_deal.purviewlogs == {}
    assert music_deal.cashbook == tranbook_shop(get_test_deal_id())
    assert music_deal.bridge == default_bridge_if_None()
    assert music_deal.fund_coin == default_fund_coin_if_None()
    assert music_deal.respect_bit == default_respect_bit_if_None()
    assert music_deal.penny == default_penny_if_None()
    assert music_deal.deals_dir == get_test_deals_dir()
    # Calculated fields
    assert music_deal._owners_dir != None
    assert music_deal._gifts_dir != None
    assert music_deal._all_tranbook == tranbook_shop(get_test_deal_id())


def test_dealunit_shop_ReturnsDealUnitWith_deals_dir(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"

    # WHEN
    music_deal = dealunit_shop(music_str, deals_dir=get_test_deals_dir())

    # THEN
    assert music_deal.deal_id == music_str
    assert music_deal.deals_dir == get_test_deals_dir()
    assert music_deal._owners_dir is not None
    assert music_deal._gifts_dir is not None


def test_dealunit_shop_ReturnsDealUnitWith_bridge(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"
    slash_str = "/"
    x_fund_coin = 7.0
    x_respect_bit = 9
    x_penny = 3
    x_current_time = 78000000

    # WHEN
    music_deal = dealunit_shop(
        deal_id=music_str,
        deals_dir=get_test_deals_dir(),
        current_time=x_current_time,
        in_memory_journal=True,
        bridge=slash_str,
        fund_coin=x_fund_coin,
        respect_bit=x_respect_bit,
        penny=x_penny,
    )

    # THEN
    assert music_deal.current_time == x_current_time
    assert music_deal.bridge == slash_str
    assert music_deal.fund_coin == x_fund_coin
    assert music_deal.respect_bit == x_respect_bit
    assert music_deal.penny == x_penny


def test_DealUnit_set_deal_dirs_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"
    music_deal = DealUnit(deal_id=music_str, deals_dir=get_test_deals_dir())
    x_deal_dir = create_path(get_test_deals_dir(), music_str)
    x_owners_dir = create_path(x_deal_dir, "owners")
    x_gifts_dir = create_path(x_deal_dir, get_gifts_folder())
    journal_file_name = "journal.db"
    journal_file_path = create_path(x_deal_dir, journal_file_name)

    assert music_deal._deal_dir is None
    assert music_deal._owners_dir is None
    assert music_deal._gifts_dir is None
    assert os_path_exists(x_deal_dir) is False
    assert os_path_isdir(x_deal_dir) is False
    assert os_path_exists(x_owners_dir) is False
    assert os_path_exists(x_gifts_dir) is False
    assert os_path_exists(journal_file_path) is False

    # WHEN
    music_deal._set_deal_dirs()

    # THEN
    assert music_deal._deal_dir == x_deal_dir
    assert music_deal._owners_dir == x_owners_dir
    assert music_deal._gifts_dir == x_gifts_dir
    assert os_path_exists(x_deal_dir)
    assert os_path_isdir(x_deal_dir)
    assert os_path_exists(x_owners_dir)
    assert os_path_exists(x_gifts_dir)
    assert os_path_exists(journal_file_path)


def test_dealunit_shop_SetsdealsDirs(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"

    # WHEN
    music_deal = dealunit_shop(music_str, get_test_deals_dir(), in_memory_journal=True)

    # THEN
    assert music_deal.deal_id == music_str
    assert music_deal._deal_dir == create_path(get_test_deals_dir(), music_str)
    assert music_deal._owners_dir == create_path(music_deal._deal_dir, "owners")


def test_DealUnit_init_owner_keeps_CorrectlySetsDirAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"
    slash_str = "/"
    x_fund_coin = 4
    x_respect_bit = 5
    music_deal = dealunit_shop(
        music_str,
        get_test_deals_dir(),
        bridge=slash_str,
        fund_coin=x_fund_coin,
        respect_bit=x_respect_bit,
        in_memory_journal=True,
    )
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(
        None, music_str, sue_str, None, respect_bit=x_respect_bit, fund_coin=x_fund_coin
    )
    assert os_path_exists(sue_hubunit.final_path()) is False

    # WHEN
    music_deal.init_owner_keeps(sue_str)

    # THEN
    print(f"{get_test_deals_dir()=}")
    assert os_path_exists(sue_hubunit.final_path())


def test_DealUnit_get_owner_voice_from_file_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"
    music_deal = dealunit_shop(music_str, get_test_deals_dir(), in_memory_journal=True)
    sue_str = "Sue"
    music_deal.init_owner_keeps(sue_str)
    sue_hubunit = hubunit_shop(None, music_str, sue_str, None)
    bob_str = "Bob"
    sue_voice = sue_hubunit.get_voice_bud()
    sue_voice.add_acctunit(bob_str)
    sue_hubunit.save_voice_bud(sue_voice)

    # WHEN
    gen_sue_voice = music_deal.get_owner_voice_from_file(sue_str)

    # THEN
    assert gen_sue_voice is not None
    assert gen_sue_voice.acct_exists(bob_str)


def test_DealUnit__set_all_healer_dutys_CorrectlySetsdutys(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    music_str = "music"
    music_deal = dealunit_shop(music_str, get_test_deals_dir(), in_memory_journal=True)
    sue_str = "Sue"
    yao_str = "Yao"
    music_deal.init_owner_keeps(sue_str)
    music_deal.init_owner_keeps(yao_str)
    sue_hubunit = hubunit_shop(None, music_str, sue_str, None)
    yao_hubunit = hubunit_shop(None, music_str, yao_str, None)
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
    sue_dallas_hubunit = hubunit_shop(None, music_str, sue_str, dallas_road)
    yao_dallas_hubunit = hubunit_shop(None, music_str, yao_str, dallas_road)
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
    music_deal._set_all_healer_dutys(sue_str)

    # THEN
    assert os_path_exists(sue_dallas_sue_duty_file_path)
    assert os_path_exists(sue_dallas_yao_duty_file_path) is False
    assert os_path_exists(yao_dallas_sue_duty_file_path)
    assert os_path_exists(yao_dallas_yao_duty_file_path) is False

    # WHEN
    music_deal._set_all_healer_dutys(yao_str)

    # THEN
    assert os_path_exists(sue_dallas_sue_duty_file_path)
    assert os_path_exists(sue_dallas_yao_duty_file_path)
    assert os_path_exists(yao_dallas_sue_duty_file_path)
    assert os_path_exists(yao_dallas_yao_duty_file_path)


def test_DealUnit_get_owner_hubunits_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    music_deal = dealunit_shop("music", get_test_deals_dir(), in_memory_journal=True)
    sue_str = "Sue"
    yao_str = "Yao"

    # WHEN / THEN
    assert len(music_deal.get_owner_hubunits()) == 0

    # WHEN
    music_deal.init_owner_keeps(sue_str)
    music_deal.init_owner_keeps(yao_str)
    music_all_owners = music_deal.get_owner_hubunits()

    # THEN
    sue_hubunit = hubunit_shop(
        deals_dir=music_deal.deals_dir,
        deal_id=music_deal.deal_id,
        owner_id=sue_str,
        keep_road=None,
        bridge=music_deal.bridge,
        fund_coin=music_deal.fund_coin,
        respect_bit=music_deal.respect_bit,
    )
    yao_hubunit = hubunit_shop(
        deals_dir=music_deal.deals_dir,
        deal_id=music_deal.deal_id,
        owner_id=yao_str,
        keep_road=None,
        bridge=music_deal.bridge,
        fund_coin=music_deal.fund_coin,
        respect_bit=music_deal.respect_bit,
    )
    assert music_all_owners.get(sue_str) == sue_hubunit
    assert music_all_owners.get(yao_str) == yao_hubunit
    assert len(music_deal.get_owner_hubunits()) == 2
