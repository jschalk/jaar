from src._road.finance import (
    default_fund_coin_if_none,
    default_bit_if_none,
    default_penny_if_none,
)
from src._road.jaar_config import get_gifts_folder, get_json_filename
from src._road.road import default_road_delimiter_if_none
from src.bud.healer import healerlink_shop
from src.bud.idea import ideaunit_shop
from src.hear.hubunit import hubunit_shop
from src.real.real import RealUnit, realunit_shop
from src.real.examples.real_env import get_test_reals_dir, env_dir_setup_cleanup
from os.path import exists as os_path_exists, isdir as os_path_isdir


def test_RealUnit_exists(env_dir_setup_cleanup):
    music_str = "music"
    music_real = RealUnit(real_id=music_str, reals_dir=get_test_reals_dir())
    assert music_real.real_id == music_str
    assert music_real.reals_dir == get_test_reals_dir()
    assert music_real._owners_dir is None
    assert music_real._journal_db is None
    assert music_real._gifts_dir is None
    assert music_real._road_delimiter is None
    assert music_real._fund_coin is None
    assert music_real._bit is None
    assert music_real._penny is None


def test_realunit_shop_ReturnsRealUnit(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"

    # WHEN
    music_real = realunit_shop(
        real_id=music_str, reals_dir=get_test_reals_dir(), in_memory_journal=True
    )

    # THEN
    assert music_real.real_id == music_str
    assert music_real.reals_dir == get_test_reals_dir()
    assert music_real._owners_dir is not None
    assert music_real._gifts_dir is not None
    assert music_real._road_delimiter == default_road_delimiter_if_none()
    assert music_real._fund_coin == default_fund_coin_if_none()
    assert music_real._bit == default_bit_if_none()
    assert music_real._penny == default_penny_if_none()


def test_realunit_shop_ReturnsRealUnitWith_road_delimiter(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"
    slash_str = "/"
    x_fund_coin = 7.0
    x_bit = 9
    x_penny = 3

    # WHEN
    music_real = realunit_shop(
        real_id=music_str,
        reals_dir=get_test_reals_dir(),
        in_memory_journal=True,
        _road_delimiter=slash_str,
        _fund_coin=x_fund_coin,
        _bit=x_bit,
        _penny=x_penny,
    )

    # THEN
    assert music_real._road_delimiter == slash_str
    assert music_real._fund_coin == x_fund_coin
    assert music_real._bit == x_bit
    assert music_real._penny == x_penny


def test_RealUnit_set_real_dirs_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"
    music_real = RealUnit(real_id=music_str, reals_dir=get_test_reals_dir())
    x_real_dir = f"{get_test_reals_dir()}/{music_str}"
    x_owners_dir = f"{x_real_dir}/owners"
    x_gifts_dir = f"{x_real_dir}/{get_gifts_folder()}"
    journal_file_name = "journal.db"
    journal_file_path = f"{x_real_dir}/{journal_file_name}"

    assert music_real._real_dir is None
    assert music_real._owners_dir is None
    assert music_real._gifts_dir is None
    assert os_path_exists(x_real_dir) is False
    assert os_path_isdir(x_real_dir) is False
    assert os_path_exists(x_owners_dir) is False
    assert os_path_exists(x_gifts_dir) is False
    assert os_path_exists(journal_file_path) is False

    # WHEN
    music_real._set_real_dirs()

    # THEN
    assert music_real._real_dir == x_real_dir
    assert music_real._owners_dir == x_owners_dir
    assert music_real._gifts_dir == x_gifts_dir
    assert os_path_exists(x_real_dir)
    assert os_path_isdir(x_real_dir)
    assert os_path_exists(x_owners_dir)
    assert os_path_exists(x_gifts_dir)
    assert os_path_exists(journal_file_path)


def test_realunit_shop_SetsRealsDirs(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"

    # WHEN
    music_real = realunit_shop(music_str, get_test_reals_dir(), in_memory_journal=True)

    # THEN
    assert music_real.real_id == music_str
    assert music_real._real_dir == f"{get_test_reals_dir()}/{music_str}"
    assert music_real._owners_dir == f"{music_real._real_dir}/owners"


def test_RealUnit_init_owner_econs_CorrectlySetsDirAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"
    slash_str = "/"
    x_fund_coin = 4
    x_bit = 5
    music_real = realunit_shop(
        music_str,
        get_test_reals_dir(),
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
    music_real.init_owner_econs(sue_str)

    # THEN
    print(f"{get_test_reals_dir()=}")
    assert os_path_exists(sue_hubunit.action_path())


def test_RealUnit_get_owner_voice_from_file_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "music"
    music_real = realunit_shop(music_str, get_test_reals_dir(), in_memory_journal=True)
    sue_str = "Sue"
    music_real.init_owner_econs(sue_str)
    sue_hubunit = hubunit_shop(None, music_str, sue_str, None)
    bob_str = "Bob"
    sue_voice = sue_hubunit.get_voice_bud()
    sue_voice.add_acctunit(bob_str)
    sue_hubunit.save_voice_bud(sue_voice)

    # WHEN
    gen_sue_voice = music_real.get_owner_voice_from_file(sue_str)

    # THEN
    assert gen_sue_voice is not None
    assert gen_sue_voice.acct_exists(bob_str)


def test_RealUnit__set_all_healer_dutys_CorrectlySetsdutys(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    music_str = "music"
    music_real = realunit_shop(music_str, get_test_reals_dir(), in_memory_journal=True)
    sue_str = "Sue"
    yao_str = "Yao"
    music_real.init_owner_econs(sue_str)
    music_real.init_owner_econs(yao_str)
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
    music_real._set_all_healer_dutys(sue_str)

    # THEN
    assert os_path_exists(sue_dallas_sue_duty_file_path)
    assert os_path_exists(sue_dallas_yao_duty_file_path) is False
    assert os_path_exists(yao_dallas_sue_duty_file_path)
    assert os_path_exists(yao_dallas_yao_duty_file_path) is False

    # WHEN
    music_real._set_all_healer_dutys(yao_str)

    # THEN
    assert os_path_exists(sue_dallas_sue_duty_file_path)
    assert os_path_exists(sue_dallas_yao_duty_file_path)
    assert os_path_exists(yao_dallas_sue_duty_file_path)
    assert os_path_exists(yao_dallas_yao_duty_file_path)


def test_RealUnit_get_owner_hubunits_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    music_real = realunit_shop("music", get_test_reals_dir(), in_memory_journal=True)
    sue_str = "Sue"
    yao_str = "Yao"

    # WHEN / THEN
    assert len(music_real.get_owner_hubunits()) == 0

    # WHEN
    music_real.init_owner_econs(sue_str)
    music_real.init_owner_econs(yao_str)
    music_all_owners = music_real.get_owner_hubunits()

    # THEN
    sue_hubunit = hubunit_shop(
        reals_dir=music_real.reals_dir,
        real_id=music_real.real_id,
        owner_id=sue_str,
        econ_road=None,
        road_delimiter=music_real._road_delimiter,
        fund_coin=music_real._fund_coin,
        bit=music_real._bit,
    )
    yao_hubunit = hubunit_shop(
        reals_dir=music_real.reals_dir,
        real_id=music_real.real_id,
        owner_id=yao_str,
        econ_road=None,
        road_delimiter=music_real._road_delimiter,
        fund_coin=music_real._fund_coin,
        bit=music_real._bit,
    )
    assert music_all_owners.get(sue_str) == sue_hubunit
    assert music_all_owners.get(yao_str) == yao_hubunit
    assert len(music_real.get_owner_hubunits()) == 2
