from src.f00_instrument.file import create_path
from src.f01_road.finance import (
    default_fund_coin_if_None,
    default_respect_bit_if_None,
    default_penny_if_None,
)
from src.f01_road.jaar_config import (
    get_gifts_folder,
    get_json_filename,
    get_test_fiscal_id,
)
from src.f01_road.road import default_wall_if_None
from src.f01_road.finance_tran import tranbook_shop
from src.f02_bud.healer import healerlink_shop
from src.f02_bud.item import itemunit_shop
from src.f03_chrono.chrono import timelineunit_shop
from src.f05_listen.hubunit import hubunit_shop
from src.f07_fiscal.fiscal import FiscalUnit, fiscalunit_shop
from src.f07_fiscal.examples.fiscal_env import (
    get_test_fiscals_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists, isdir as os_path_isdir


def test_FiscalUnit_Exists(env_dir_setup_cleanup):
    music_str = "music"
    music_fiscal = FiscalUnit()
    assert not music_fiscal.fiscal_id
    assert not music_fiscal.timeline
    assert not music_fiscal.current_time
    assert not music_fiscal.purviewlogs
    assert not music_fiscal.cashbook
    assert not music_fiscal.wall
    assert not music_fiscal.fund_coin
    assert not music_fiscal.respect_bit
    assert not music_fiscal.penny
    assert not music_fiscal.fiscals_dir
    # Calculated fields
    assert not music_fiscal._owners_dir
    assert not music_fiscal._journal_db
    assert not music_fiscal._gifts_dir
    assert not music_fiscal._all_tranbook


def test_fiscalunit_shop_ReturnsFiscalUnit():
    # ESTABLISH / WHEN
    music_fiscal = fiscalunit_shop()

    # THEN
    assert music_fiscal.fiscal_id == get_test_fiscal_id()
    assert music_fiscal.timeline == timelineunit_shop()
    assert music_fiscal.current_time == 0
    assert music_fiscal.purviewlogs == {}
    assert music_fiscal.cashbook == tranbook_shop(get_test_fiscal_id())
    assert music_fiscal.wall == default_wall_if_None()
    assert music_fiscal.fund_coin == default_fund_coin_if_None()
    assert music_fiscal.respect_bit == default_respect_bit_if_None()
    assert music_fiscal.penny == default_penny_if_None()
    assert music_fiscal.fiscals_dir == get_test_fiscals_dir()
    # Calculated fields
    assert music_fiscal._owners_dir != None
    assert music_fiscal._gifts_dir != None
    assert music_fiscal._all_tranbook == tranbook_shop(get_test_fiscal_id())


def test_fiscalunit_shop_ReturnsFiscalUnitWith_fiscals_dir(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"

    # WHEN
    music_fiscal = fiscalunit_shop(music_str, fiscals_dir=get_test_fiscals_dir())

    # THEN
    assert music_fiscal.fiscal_id == music_str
    assert music_fiscal.fiscals_dir == get_test_fiscals_dir()
    assert music_fiscal._owners_dir is not None
    assert music_fiscal._gifts_dir is not None


def test_fiscalunit_shop_ReturnsFiscalUnitWith_wall(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"
    slash_str = "/"
    x_fund_coin = 7.0
    x_respect_bit = 9
    x_penny = 3
    x_current_time = 78000000

    # WHEN
    music_fiscal = fiscalunit_shop(
        fiscal_id=music_str,
        fiscals_dir=get_test_fiscals_dir(),
        current_time=x_current_time,
        in_memory_journal=True,
        wall=slash_str,
        fund_coin=x_fund_coin,
        respect_bit=x_respect_bit,
        penny=x_penny,
    )

    # THEN
    assert music_fiscal.current_time == x_current_time
    assert music_fiscal.wall == slash_str
    assert music_fiscal.fund_coin == x_fund_coin
    assert music_fiscal.respect_bit == x_respect_bit
    assert music_fiscal.penny == x_penny


def test_FiscalUnit_set_fiscal_dirs_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"
    music_fiscal = FiscalUnit(fiscal_id=music_str, fiscals_dir=get_test_fiscals_dir())
    x_fiscal_dir = create_path(get_test_fiscals_dir(), music_str)
    x_owners_dir = create_path(x_fiscal_dir, "owners")
    x_gifts_dir = create_path(x_fiscal_dir, get_gifts_folder())
    journal_file_name = "journal.db"
    journal_file_path = create_path(x_fiscal_dir, journal_file_name)

    assert music_fiscal._fiscal_dir is None
    assert music_fiscal._owners_dir is None
    assert music_fiscal._gifts_dir is None
    assert os_path_exists(x_fiscal_dir) is False
    assert os_path_isdir(x_fiscal_dir) is False
    assert os_path_exists(x_owners_dir) is False
    assert os_path_exists(x_gifts_dir) is False
    assert os_path_exists(journal_file_path) is False

    # WHEN
    music_fiscal._set_fiscal_dirs()

    # THEN
    assert music_fiscal._fiscal_dir == x_fiscal_dir
    assert music_fiscal._owners_dir == x_owners_dir
    assert music_fiscal._gifts_dir == x_gifts_dir
    assert os_path_exists(x_fiscal_dir)
    assert os_path_isdir(x_fiscal_dir)
    assert os_path_exists(x_owners_dir)
    assert os_path_exists(x_gifts_dir)
    assert os_path_exists(journal_file_path)


def test_fiscalunit_shop_SetsFiscalsDirs(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"

    # WHEN
    music_fiscal = fiscalunit_shop(
        music_str, get_test_fiscals_dir(), in_memory_journal=True
    )

    # THEN
    assert music_fiscal.fiscal_id == music_str
    assert music_fiscal._fiscal_dir == create_path(get_test_fiscals_dir(), music_str)
    assert music_fiscal._owners_dir == create_path(music_fiscal._fiscal_dir, "owners")


def test_FiscalUnit_init_owner_keeps_CorrectlySetsDirAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"
    slash_str = "/"
    x_fund_coin = 4
    x_respect_bit = 5
    music_fiscal = fiscalunit_shop(
        music_str,
        get_test_fiscals_dir(),
        wall=slash_str,
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
    music_fiscal.init_owner_keeps(sue_str)

    # THEN
    print(f"{get_test_fiscals_dir()=}")
    assert os_path_exists(sue_hubunit.final_path())


def test_FiscalUnit_get_owner_voice_from_file_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(
        music_str, get_test_fiscals_dir(), in_memory_journal=True
    )
    sue_str = "Sue"
    music_fiscal.init_owner_keeps(sue_str)
    sue_hubunit = hubunit_shop(None, music_str, sue_str, None)
    bob_str = "Bob"
    sue_voice = sue_hubunit.get_voice_bud()
    sue_voice.add_acctunit(bob_str)
    sue_hubunit.save_voice_bud(sue_voice)

    # WHEN
    gen_sue_voice = music_fiscal.get_owner_voice_from_file(sue_str)

    # THEN
    assert gen_sue_voice is not None
    assert gen_sue_voice.acct_exists(bob_str)


def test_FiscalUnit__set_all_healer_dutys_CorrectlySetsdutys(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(
        music_str, get_test_fiscals_dir(), in_memory_journal=True
    )
    sue_str = "Sue"
    yao_str = "Yao"
    music_fiscal.init_owner_keeps(sue_str)
    music_fiscal.init_owner_keeps(yao_str)
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
    music_fiscal._set_all_healer_dutys(sue_str)

    # THEN
    assert os_path_exists(sue_dallas_sue_duty_file_path)
    assert os_path_exists(sue_dallas_yao_duty_file_path) is False
    assert os_path_exists(yao_dallas_sue_duty_file_path)
    assert os_path_exists(yao_dallas_yao_duty_file_path) is False

    # WHEN
    music_fiscal._set_all_healer_dutys(yao_str)

    # THEN
    assert os_path_exists(sue_dallas_sue_duty_file_path)
    assert os_path_exists(sue_dallas_yao_duty_file_path)
    assert os_path_exists(yao_dallas_sue_duty_file_path)
    assert os_path_exists(yao_dallas_yao_duty_file_path)


def test_FiscalUnit_get_owner_hubunits_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    music_fiscal = fiscalunit_shop(
        "music", get_test_fiscals_dir(), in_memory_journal=True
    )
    sue_str = "Sue"
    yao_str = "Yao"

    # WHEN / THEN
    assert len(music_fiscal.get_owner_hubunits()) == 0

    # WHEN
    music_fiscal.init_owner_keeps(sue_str)
    music_fiscal.init_owner_keeps(yao_str)
    music_all_owners = music_fiscal.get_owner_hubunits()

    # THEN
    sue_hubunit = hubunit_shop(
        fiscals_dir=music_fiscal.fiscals_dir,
        fiscal_id=music_fiscal.fiscal_id,
        owner_id=sue_str,
        keep_road=None,
        wall=music_fiscal.wall,
        fund_coin=music_fiscal.fund_coin,
        respect_bit=music_fiscal.respect_bit,
    )
    yao_hubunit = hubunit_shop(
        fiscals_dir=music_fiscal.fiscals_dir,
        fiscal_id=music_fiscal.fiscal_id,
        owner_id=yao_str,
        keep_road=None,
        wall=music_fiscal.wall,
        fund_coin=music_fiscal.fund_coin,
        respect_bit=music_fiscal.respect_bit,
    )
    assert music_all_owners.get(sue_str) == sue_hubunit
    assert music_all_owners.get(yao_str) == yao_hubunit
    assert len(music_fiscal.get_owner_hubunits()) == 2
