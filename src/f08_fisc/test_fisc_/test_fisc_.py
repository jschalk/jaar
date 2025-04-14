from src.f00_data_toolboxs.file_toolbox import create_path, get_json_filename
from src.f02_finance_toolboxs.finance_config import (
    default_fund_coin_if_None,
    default_respect_bit_if_None,
    filter_penny,
)
from src.f01_word_logic.road import default_bridge_if_None
from src.f02_finance_toolboxs.deal import tranbook_shop
from src.f02_bud.healer import healerlink_shop
from src.f02_bud.item import itemunit_shop
from src.f03_chrono.chrono import timelineunit_shop
from src.f06_listen.hub_tool import (
    save_gut_file,
    open_gut_file,
    plan_file_exists,
)
from src.f06_listen.hubunit import hubunit_shop
from src.f08_fisc.fisc import FiscUnit, fiscunit_shop, DEFAULT_PLAN_LISTEN_COUNT
from src.f08_fisc.examples.fisc_env import get_test_fisc_mstr_dir, env_dir_setup_cleanup
from os.path import exists as os_path_exists, isdir as os_path_isdir
from pytest import raises as pytest_raises


def test_DEFAULT_PLAN_LISTEN_COUNT_Exists():
    # ESTABLISH / WHEN / THEN
    assert DEFAULT_PLAN_LISTEN_COUNT == 3


def test_FiscUnit_Exists():
    # ESTABLISH / WHEN
    accord_fisc = FiscUnit()
    # THEN
    assert not accord_fisc.fisc_title
    assert not accord_fisc.timeline
    assert not accord_fisc.brokerunits
    assert not accord_fisc.cashbook
    assert not accord_fisc.offi_times
    assert not accord_fisc.bridge
    assert not accord_fisc.fund_coin
    assert not accord_fisc.respect_bit
    assert not accord_fisc.penny
    assert not accord_fisc.plan_listen_rotations
    assert not accord_fisc.fisc_mstr_dir
    # Calculated fields
    assert not accord_fisc._offi_time_max
    assert not accord_fisc._owners_dir
    assert not accord_fisc._journal_db
    assert not accord_fisc._packs_dir
    assert not accord_fisc._all_tranbook


def test_fiscunit_shop_ReturnsFiscUnit():
    # ESTABLISH
    a23_str = "accord23"

    # WHEN
    accord_fisc = fiscunit_shop(a23_str)

    # THEN
    assert accord_fisc.fisc_title == a23_str
    assert accord_fisc.timeline == timelineunit_shop()
    assert accord_fisc.brokerunits == {}
    assert accord_fisc.cashbook == tranbook_shop(a23_str)
    assert accord_fisc.offi_times == set()
    assert accord_fisc.bridge == default_bridge_if_None()
    assert accord_fisc.fund_coin == default_fund_coin_if_None()
    assert accord_fisc.respect_bit == default_respect_bit_if_None()
    assert accord_fisc.penny == filter_penny()
    assert accord_fisc.fisc_mstr_dir == get_test_fisc_mstr_dir()
    assert accord_fisc.plan_listen_rotations == DEFAULT_PLAN_LISTEN_COUNT
    # Calculated fields
    assert accord_fisc._owners_dir != None
    assert accord_fisc._packs_dir != None
    assert accord_fisc._all_tranbook == tranbook_shop(a23_str)


def test_fiscunit_shop_ReturnsFiscUnitWith_fiscs_dir(env_dir_setup_cleanup):
    # ESTABLISH
    accord45_str = "accord45"

    # WHEN
    accord_fisc = fiscunit_shop(accord45_str, fisc_mstr_dir=get_test_fisc_mstr_dir())

    # THEN
    assert accord_fisc.fisc_title == accord45_str
    assert accord_fisc.fisc_mstr_dir == get_test_fisc_mstr_dir()
    assert accord_fisc._owners_dir is not None
    assert accord_fisc._packs_dir is not None


def test_fiscunit_shop_ReturnsFiscUnitWith_bridge(env_dir_setup_cleanup):
    # ESTABLISH
    accord45_str = "accord45"
    slash_str = "/"
    x_fund_coin = 7.0
    x_respect_bit = 9
    x_penny = 3
    a45_offi_times = {12, 15}
    x_plan_listen_rotations = 888

    # WHEN
    accord_fisc = fiscunit_shop(
        fisc_title=accord45_str,
        fisc_mstr_dir=get_test_fisc_mstr_dir(),
        offi_times=a45_offi_times,
        in_memory_journal=True,
        bridge=slash_str,
        fund_coin=x_fund_coin,
        respect_bit=x_respect_bit,
        penny=x_penny,
        plan_listen_rotations=x_plan_listen_rotations,
    )

    # THEN
    assert accord_fisc.bridge == slash_str
    assert accord_fisc.fund_coin == x_fund_coin
    assert accord_fisc.respect_bit == x_respect_bit
    assert accord_fisc.penny == x_penny
    assert accord_fisc.offi_times == a45_offi_times
    assert accord_fisc.plan_listen_rotations == x_plan_listen_rotations


def test_FiscUnit_set_fisc_dirs_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = FiscUnit(accord45_str, get_test_fisc_mstr_dir())
    x_fiscs_dir = create_path(get_test_fisc_mstr_dir(), "fiscs")
    x_fisc_dir = create_path(x_fiscs_dir, accord45_str)
    x_owners_dir = create_path(x_fisc_dir, "owners")
    x_packs_dir = create_path(x_fisc_dir, "packs")
    journal_filename = "journal.db"
    journal_file_path = create_path(x_fisc_dir, journal_filename)

    assert not accord_fisc._fisc_dir
    assert not accord_fisc._owners_dir
    assert not accord_fisc._packs_dir
    assert os_path_exists(x_fisc_dir) is False
    assert os_path_isdir(x_fisc_dir) is False
    assert os_path_exists(x_owners_dir) is False
    assert os_path_exists(x_packs_dir) is False
    assert os_path_exists(journal_file_path) is False

    # WHEN
    accord_fisc._set_fisc_dirs()

    # THEN
    assert accord_fisc._fisc_dir == x_fisc_dir
    assert accord_fisc._owners_dir == x_owners_dir
    assert accord_fisc._packs_dir == x_packs_dir
    assert os_path_exists(x_fisc_dir)
    assert os_path_isdir(x_fisc_dir)
    assert os_path_exists(x_owners_dir)
    assert os_path_exists(x_packs_dir)
    assert os_path_exists(journal_file_path)


def test_fiscunit_shop_SetsfiscsDirs(env_dir_setup_cleanup):
    # ESTABLISH
    accord45_str = "accord45"

    # WHEN
    accord_fisc = fiscunit_shop(
        accord45_str, get_test_fisc_mstr_dir(), in_memory_journal=True
    )

    # THEN
    assert accord_fisc.fisc_title == accord45_str
    x_fiscs_dir = create_path(get_test_fisc_mstr_dir(), "fiscs")
    assert accord_fisc._fisc_dir == create_path(x_fiscs_dir, accord45_str)
    assert accord_fisc._owners_dir == create_path(accord_fisc._fisc_dir, "owners")


def test_FiscUnit_set_init_pack_and_plan_CorrectlySetsDirAndFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    accord45_str = "accord45"
    slash_str = "/"
    x_fund_coin = 4
    x_respect_bit = 5
    accord_fisc = fiscunit_shop(
        accord45_str,
        fisc_mstr_dir,
        bridge=slash_str,
        fund_coin=x_fund_coin,
        respect_bit=x_respect_bit,
        in_memory_journal=True,
    )
    sue_str = "Sue"
    assert not plan_file_exists(fisc_mstr_dir, accord45_str, sue_str)

    # WHEN
    accord_fisc.set_init_pack_and_plan(sue_str)

    # THEN
    print(f"{fisc_mstr_dir=}")
    assert plan_file_exists(fisc_mstr_dir, accord45_str, sue_str)


def test_FiscUnit_get_owner_gut_from_file_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    accord45_str = "accord45"
    x_fisc_mstr_dir = get_test_fisc_mstr_dir()
    accord_fisc = fiscunit_shop(accord45_str, x_fisc_mstr_dir, in_memory_journal=True)
    sue_str = "Sue"
    accord_fisc.set_init_pack_and_plan(sue_str)
    bob_str = "Bob"
    sue_gut = open_gut_file(x_fisc_mstr_dir, accord45_str, sue_str)
    sue_gut.add_acctunit(bob_str)
    save_gut_file(x_fisc_mstr_dir, sue_gut)

    # WHEN
    gen_sue_gut = accord_fisc.get_owner_gut_from_file(sue_str)

    # THEN
    assert gen_sue_gut is not None
    assert gen_sue_gut.acct_exists(bob_str)


def test_FiscUnit__set_all_healer_dutys_CorrectlySetsdutys(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord45_str = "accord45"
    x_fisc_mstr_dir = get_test_fisc_mstr_dir()
    accord_fisc = fiscunit_shop(accord45_str, x_fisc_mstr_dir, in_memory_journal=True)
    sue_str = "Sue"
    yao_str = "Yao"
    accord_fisc.set_init_pack_and_plan(sue_str)
    accord_fisc.set_init_pack_and_plan(yao_str)
    sue_gut_bud = open_gut_file(x_fisc_mstr_dir, accord45_str, sue_str)
    yao_gut_bud = open_gut_file(x_fisc_mstr_dir, accord45_str, yao_str)

    sue_gut_bud.add_acctunit(sue_str)
    sue_gut_bud.add_acctunit(yao_str)
    yao_gut_bud.add_acctunit(sue_str)
    yao_gut_bud.add_acctunit(yao_str)
    texas_str = "Texas"
    texas_road = sue_gut_bud.make_l1_road(texas_str)
    sue_gut_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    yao_gut_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_road = sue_gut_bud.make_road(texas_road, dallas_str)
    dallas_healerlink = healerlink_shop({sue_str, yao_str})
    dallas_item = itemunit_shop(dallas_str, healerlink=dallas_healerlink)
    elpaso_str = "el paso"
    elpaso_road = sue_gut_bud.make_road(texas_road, elpaso_str)
    elpaso_healerlink = healerlink_shop({sue_str})
    elpaso_item = itemunit_shop(elpaso_str, healerlink=elpaso_healerlink)

    sue_gut_bud.set_item(dallas_item, texas_road)
    sue_gut_bud.set_item(elpaso_item, texas_road)
    yao_gut_bud.set_item(dallas_item, texas_road)
    yao_gut_bud.set_item(elpaso_item, texas_road)

    save_gut_file(x_fisc_mstr_dir, sue_gut_bud)
    save_gut_file(x_fisc_mstr_dir, yao_gut_bud)
    sue_filename = get_json_filename(sue_str)
    yao_filename = get_json_filename(yao_str)
    sue_dallas_hubunit = hubunit_shop(
        x_fisc_mstr_dir, accord45_str, sue_str, dallas_road
    )
    yao_dallas_hubunit = hubunit_shop(
        x_fisc_mstr_dir, accord45_str, yao_str, dallas_road
    )
    sue_dutys_dir = sue_dallas_hubunit.dutys_dir()
    yao_dutys_dir = yao_dallas_hubunit.dutys_dir()
    sue_dallas_sue_duty_file_path = create_path(sue_dutys_dir, sue_filename)
    sue_dallas_yao_duty_file_path = create_path(sue_dutys_dir, yao_filename)
    yao_dallas_sue_duty_file_path = create_path(yao_dutys_dir, sue_filename)
    yao_dallas_yao_duty_file_path = create_path(yao_dutys_dir, yao_filename)
    assert os_path_exists(sue_dallas_sue_duty_file_path) is False
    assert os_path_exists(sue_dallas_yao_duty_file_path) is False
    assert os_path_exists(yao_dallas_sue_duty_file_path) is False
    assert os_path_exists(yao_dallas_yao_duty_file_path) is False

    # WHEN
    accord_fisc._set_all_healer_dutys(sue_str)

    # THEN
    assert os_path_exists(sue_dallas_sue_duty_file_path)
    assert os_path_exists(sue_dallas_yao_duty_file_path) is False
    assert os_path_exists(yao_dallas_sue_duty_file_path)
    assert os_path_exists(yao_dallas_yao_duty_file_path) is False

    # WHEN
    accord_fisc._set_all_healer_dutys(yao_str)

    # THEN
    assert os_path_exists(sue_dallas_sue_duty_file_path)
    assert os_path_exists(sue_dallas_yao_duty_file_path)
    assert os_path_exists(yao_dallas_sue_duty_file_path)
    assert os_path_exists(yao_dallas_yao_duty_file_path)


def test_FiscUnit_get_owner_hubunits_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    accord_fisc = fiscunit_shop(
        "accord45", get_test_fisc_mstr_dir(), in_memory_journal=True
    )
    sue_str = "Sue"
    yao_str = "Yao"

    # WHEN / THEN
    assert len(accord_fisc.get_owner_hubunits()) == 0

    # WHEN
    accord_fisc.set_init_pack_and_plan(sue_str)
    accord_fisc.set_init_pack_and_plan(yao_str)
    accord_all_owners = accord_fisc.get_owner_hubunits()

    # THEN
    sue_hubunit = hubunit_shop(
        fisc_mstr_dir=accord_fisc.fisc_mstr_dir,
        fisc_title=accord_fisc.fisc_title,
        owner_name=sue_str,
        keep_road=None,
        bridge=accord_fisc.bridge,
        fund_coin=accord_fisc.fund_coin,
        respect_bit=accord_fisc.respect_bit,
    )
    yao_hubunit = hubunit_shop(
        fisc_mstr_dir=accord_fisc.fisc_mstr_dir,
        fisc_title=accord_fisc.fisc_title,
        owner_name=yao_str,
        keep_road=None,
        bridge=accord_fisc.bridge,
        fund_coin=accord_fisc.fund_coin,
        respect_bit=accord_fisc.respect_bit,
    )
    assert accord_all_owners.get(sue_str) == sue_hubunit
    assert accord_all_owners.get(yao_str) == yao_hubunit
    assert len(accord_fisc.get_owner_hubunits()) == 2


# def test_FiscUnit_set_offi_time_Scenario0_SetsAttr():
#     # ESTABLISH
#     fisc_mstr_dir = get_test_fisc_mstr_dir()
#     time56 = 56
#     a23_fisc = fiscunit_shop("accord23", fisc_mstr_dir, _offi_time_max=time56)
#     assert a23_fisc.offi_time == 0
#     assert a23_fisc._offi_time_max == time56

#     # WHEN
#     time23 = 23
#     a23_fisc.set_offi_time(time23)

#     # THEN
#     assert a23_fisc.offi_time == time23
#     assert a23_fisc._offi_time_max == time56


# def test_FiscUnit_set_offi_time_Scenario1_SetsAttr():
#     # ESTABLISH
#     a23_fisc = fiscunit_shop("accord23", get_test_fisc_mstr_dir())
#     assert a23_fisc.offi_time == 0
#     assert a23_fisc._offi_time_max == 0

#     # WHEN
#     time23 = 23
#     a23_fisc.set_offi_time(time23)

#     # THEN
#     assert a23_fisc.offi_time == time23
#     assert a23_fisc._offi_time_max == time23


def test_FiscUnit_set_offi_time_max_Scenario0_SetsAttr():
    # ESTABLISH
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    time7 = 7
    a23_fisc = fiscunit_shop("accord23", fisc_mstr_dir)
    a23_fisc._offi_time_max = time7
    # assert a23_fisc.offi_time == 0
    assert a23_fisc._offi_time_max == time7

    # WHEN
    time23 = 23
    a23_fisc.set_offi_time_max(time23)

    # THEN
    # assert a23_fisc.offi_time == 0
    assert a23_fisc._offi_time_max == time23


# def test_FiscUnit_set_offi_time_max_Scenario1_SetsAttr():
#     # ESTABLISH
#     fisc_mstr_dir = get_test_fisc_mstr_dir()
#     time21 = 21
#     time77 = 77
#     a23_fisc = fiscunit_shop(
#         "accord23", fisc_mstr_dir, offi_time=time21, _offi_time_max=time77
#     )
#     assert a23_fisc.offi_time == time21
#     assert a23_fisc._offi_time_max == time77

#     # WHEN / THEN
#     time11 = 11
#     with pytest_raises(Exception) as excinfo:
#         a23_fisc.set_offi_time_max(time11)
#     exception_str = f"Cannot set _offi_time_max={time11} because it is less than offi_time={time21}"
#     assert str(excinfo.value) == exception_str


# def test_FiscUnit_set_offi_time_Scenario0_SetsAttr():
#     # ESTABLISH
#     a23_fisc = fiscunit_shop("accord23", get_test_fisc_mstr_dir())
#     assert a23_fisc.offi_time == 0
#     assert a23_fisc._offi_time_max == 0

#     # WHEN
#     time23 = 23
#     time55 = 55
#     a23_fisc.set_offi_time(time23, time55)

#     # THEN
#     assert a23_fisc.offi_time == time23
#     assert a23_fisc._offi_time_max == time55
