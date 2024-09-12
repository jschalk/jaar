from src._road.finance import (
    default_fund_coin_if_none,
    default_bit_if_none,
    default_penny_if_none,
)
from src._road.jaar_config import get_gifts_folder, get_json_filename
from src._road.road import default_road_delimiter_if_none
from src.bud.healer import healerlink_shop
from src.bud.idea import ideaunit_shop
from src.listen.hubunit import hubunit_shop
from src.fiscal.fiscal import FiscalUnit, fiscalunit_shop
from src.fiscal.examples.fiscal_env import get_test_fiscals_dir, env_dir_setup_cleanup
from os.path import exists as os_path_exists, isdir as os_path_isdir


def test_FiscalUnit_exists(env_dir_setup_cleanup):
    music_str = "music"
    music_fiscal = FiscalUnit(fiscal_id=music_str, fiscals_dir=get_test_fiscals_dir())
    assert music_fiscal.fiscal_id == music_str
    assert music_fiscal.fiscals_dir == get_test_fiscals_dir()
    assert music_fiscal._owners_dir is None
    assert music_fiscal._journal_db is None
    assert music_fiscal._gifts_dir is None
    assert music_fiscal._road_delimiter is None
    assert music_fiscal._fund_coin is None
    assert music_fiscal._bit is None
    assert music_fiscal._penny is None


def test_fiscalunit_shop_ReturnsFiscalUnit(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"

    # WHEN
    music_fiscal = fiscalunit_shop(
        fiscal_id=music_str, fiscals_dir=get_test_fiscals_dir(), in_memory_journal=True
    )

    # THEN
    assert music_fiscal.fiscal_id == music_str
    assert music_fiscal.fiscals_dir == get_test_fiscals_dir()
    assert music_fiscal._owners_dir is not None
    assert music_fiscal._gifts_dir is not None
    assert music_fiscal._road_delimiter == default_road_delimiter_if_none()
    assert music_fiscal._fund_coin == default_fund_coin_if_none()
    assert music_fiscal._bit == default_bit_if_none()
    assert music_fiscal._penny == default_penny_if_none()


def test_fiscalunit_shop_ReturnsFiscalUnitWith_road_delimiter(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"
    slash_str = "/"
    x_fund_coin = 7.0
    x_bit = 9
    x_penny = 3

    # WHEN
    music_fiscal = fiscalunit_shop(
        fiscal_id=music_str,
        fiscals_dir=get_test_fiscals_dir(),
        in_memory_journal=True,
        _road_delimiter=slash_str,
        _fund_coin=x_fund_coin,
        _bit=x_bit,
        _penny=x_penny,
    )

    # THEN
    assert music_fiscal._road_delimiter == slash_str
    assert music_fiscal._fund_coin == x_fund_coin
    assert music_fiscal._bit == x_bit
    assert music_fiscal._penny == x_penny


def test_FiscalUnit_set_fiscal_dirs_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"
    music_fiscal = FiscalUnit(fiscal_id=music_str, fiscals_dir=get_test_fiscals_dir())
    x_fiscal_dir = f"{get_test_fiscals_dir()}/{music_str}"
    x_owners_dir = f"{x_fiscal_dir}/owners"
    x_gifts_dir = f"{x_fiscal_dir}/{get_gifts_folder()}"
    journal_file_name = "journal.db"
    journal_file_path = f"{x_fiscal_dir}/{journal_file_name}"

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
    assert music_fiscal._fiscal_dir == f"{get_test_fiscals_dir()}/{music_str}"
    assert music_fiscal._owners_dir == f"{music_fiscal._fiscal_dir}/owners"


def test_FiscalUnit_init_owner_econs_CorrectlySetsDirAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"
    slash_str = "/"
    x_fund_coin = 4
    x_bit = 5
    music_fiscal = fiscalunit_shop(
        music_str,
        get_test_fiscals_dir(),
        _road_delimiter=slash_str,
        _fund_coin=x_fund_coin,
        _bit=x_bit,
        in_memory_journal=True,
    )
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(
        None, music_str, sue_str, None, bit=x_bit, fund_coin=x_fund_coin
    )
    assert os_path_exists(sue_hubunit.action_path()) is False

    # WHEN
    music_fiscal.init_owner_econs(sue_str)

    # THEN
    print(f"{get_test_fiscals_dir()=}")
    assert os_path_exists(sue_hubunit.action_path())


def test_FiscalUnit_get_owner_voice_from_file_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"
    music_fiscal = fiscalunit_shop(
        music_str, get_test_fiscals_dir(), in_memory_journal=True
    )
    sue_str = "Sue"
    music_fiscal.init_owner_econs(sue_str)
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
    music_fiscal.init_owner_econs(sue_str)
    music_fiscal.init_owner_econs(yao_str)
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
    sue_voice_bud.set_l1_idea(ideaunit_shop(texas_str, problem_bool=True))
    yao_voice_bud.set_l1_idea(ideaunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_road = sue_voice_bud.make_road(texas_road, dallas_str)
    dallas_healerlink = healerlink_shop({sue_str, yao_str})
    dallas_idea = ideaunit_shop(dallas_str, healerlink=dallas_healerlink)
    elpaso_str = "el paso"
    elpaso_road = sue_voice_bud.make_road(texas_road, elpaso_str)
    elpaso_healerlink = healerlink_shop({sue_str})
    elpaso_idea = ideaunit_shop(elpaso_str, healerlink=elpaso_healerlink)

    sue_voice_bud.set_idea(dallas_idea, texas_road)
    sue_voice_bud.set_idea(elpaso_idea, texas_road)
    yao_voice_bud.set_idea(dallas_idea, texas_road)
    yao_voice_bud.set_idea(elpaso_idea, texas_road)

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
    music_fiscal.init_owner_econs(sue_str)
    music_fiscal.init_owner_econs(yao_str)
    music_all_owners = music_fiscal.get_owner_hubunits()

    # THEN
    sue_hubunit = hubunit_shop(
        fiscals_dir=music_fiscal.fiscals_dir,
        fiscal_id=music_fiscal.fiscal_id,
        owner_id=sue_str,
        econ_road=None,
        road_delimiter=music_fiscal._road_delimiter,
        fund_coin=music_fiscal._fund_coin,
        bit=music_fiscal._bit,
    )
    yao_hubunit = hubunit_shop(
        fiscals_dir=music_fiscal.fiscals_dir,
        fiscal_id=music_fiscal.fiscal_id,
        owner_id=yao_str,
        econ_road=None,
        road_delimiter=music_fiscal._road_delimiter,
        fund_coin=music_fiscal._fund_coin,
        bit=music_fiscal._bit,
    )
    assert music_all_owners.get(sue_str) == sue_hubunit
    assert music_all_owners.get(yao_str) == yao_hubunit
    assert len(music_fiscal.get_owner_hubunits()) == 2
