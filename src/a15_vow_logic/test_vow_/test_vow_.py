from os.path import exists as os_path_exists, isdir as os_path_isdir
from src.a00_data_toolbox.file_toolbox import create_path, get_json_filename, set_dir
from src.a01_term_logic.way import default_bridge_if_None
from src.a02_finance_logic.deal import tranbook_shop
from src.a02_finance_logic.finance_config import (
    default_fund_iota_if_None,
    default_RespectBit_if_None,
    filter_penny,
)
from src.a05_concept_logic.concept import conceptunit_shop
from src.a05_concept_logic.healer import healerlink_shop
from src.a06_plan_logic.plan import planunit_shop
from src.a07_calendar_logic.chrono import timelineunit_shop
from src.a12_hub_tools.hub_path import create_owner_dir_path, create_path
from src.a12_hub_tools.hub_tool import (
    gut_file_exists,
    job_file_exists,
    open_gut_file,
    open_job_file,
    save_gut_file,
    save_job_file,
)
from src.a12_hub_tools.hubunit import hubunit_shop
from src.a15_vow_logic._test_util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a15_vow_logic.vow import VowUnit, get_default_job_listen_count, vowunit_shop


def test_get_default_job_listen_count_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_default_job_listen_count() == 3


def test_VowUnit_Exists():
    # ESTABLISH / WHEN
    accord_vow = VowUnit()
    # THEN
    assert not accord_vow.vow_label
    assert not accord_vow.timeline
    assert not accord_vow.brokerunits
    assert not accord_vow.paybook
    assert not accord_vow.offi_times
    assert not accord_vow.bridge
    assert not accord_vow.fund_iota
    assert not accord_vow.respect_bit
    assert not accord_vow.penny
    assert not accord_vow.job_listen_rotations
    assert not accord_vow.vow_mstr_dir
    # Calculated fields
    assert not accord_vow._offi_time_max
    assert not accord_vow._owners_dir
    assert not accord_vow._journal_db
    assert not accord_vow._packs_dir
    assert not accord_vow._all_tranbook


def test_vowunit_shop_ReturnsVowUnit():
    # ESTABLISH
    a23_str = "accord23"

    # WHEN
    a23_vow = vowunit_shop(a23_str)

    # THEN
    assert a23_vow.vow_label == a23_str
    assert a23_vow.timeline == timelineunit_shop()
    assert a23_vow.brokerunits == {}
    assert a23_vow.paybook == tranbook_shop(a23_str)
    assert a23_vow.offi_times == set()
    assert a23_vow.bridge == default_bridge_if_None()
    assert a23_vow.fund_iota == default_fund_iota_if_None()
    assert a23_vow.respect_bit == default_RespectBit_if_None()
    assert a23_vow.penny == filter_penny()
    assert a23_vow.vow_mstr_dir == get_module_temp_dir()
    assert a23_vow.job_listen_rotations == get_default_job_listen_count()
    # Calculated fields
    assert a23_vow._owners_dir != None
    assert a23_vow._packs_dir != None
    assert a23_vow._all_tranbook == tranbook_shop(a23_str)


def test_vowunit_shop_ReturnsVowUnitWith_vows_dir(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "accord23"

    # WHEN
    a23_vow = vowunit_shop(a23_str, vow_mstr_dir=get_module_temp_dir())

    # THEN
    assert a23_vow.vow_label == a23_str
    assert a23_vow.vow_mstr_dir == get_module_temp_dir()
    assert a23_vow._owners_dir is not None
    assert a23_vow._packs_dir is not None


def test_vowunit_shop_ReturnsVowUnitWith_bridge(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "accord23"
    slash_str = "/"
    x_fund_iota = 7.0
    x_respect_bit = 9
    x_penny = 3
    a45_offi_times = {12, 15}
    x_job_listen_rotations = 888

    # WHEN
    a23_vow = vowunit_shop(
        vow_label=a23_str,
        vow_mstr_dir=get_module_temp_dir(),
        offi_times=a45_offi_times,
        in_memory_journal=True,
        bridge=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        penny=x_penny,
        job_listen_rotations=x_job_listen_rotations,
    )

    # THEN
    assert a23_vow.bridge == slash_str
    assert a23_vow.fund_iota == x_fund_iota
    assert a23_vow.respect_bit == x_respect_bit
    assert a23_vow.penny == x_penny
    assert a23_vow.offi_times == a45_offi_times
    assert a23_vow.job_listen_rotations == x_job_listen_rotations


def test_VowUnit_set_vow_dirs_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "accord23"
    accord_vow = VowUnit(a23_str, get_module_temp_dir())
    x_vows_dir = create_path(get_module_temp_dir(), "vows")
    x_vow_dir = create_path(x_vows_dir, a23_str)
    x_owners_dir = create_path(x_vow_dir, "owners")
    x_packs_dir = create_path(x_vow_dir, "packs")
    journal_filename = "journal.db"
    journal_file_path = create_path(x_vow_dir, journal_filename)

    assert not accord_vow._vow_dir
    assert not accord_vow._owners_dir
    assert not accord_vow._packs_dir
    assert os_path_exists(x_vow_dir) is False
    assert os_path_isdir(x_vow_dir) is False
    assert os_path_exists(x_owners_dir) is False
    assert os_path_exists(x_packs_dir) is False
    assert os_path_exists(journal_file_path) is False

    # WHEN
    accord_vow._set_vow_dirs()

    # THEN
    assert accord_vow._vow_dir == x_vow_dir
    assert accord_vow._owners_dir == x_owners_dir
    assert accord_vow._packs_dir == x_packs_dir
    assert os_path_exists(x_vow_dir)
    assert os_path_isdir(x_vow_dir)
    assert os_path_exists(x_owners_dir)
    assert os_path_exists(x_packs_dir)
    assert os_path_exists(journal_file_path)


def test_vowunit_shop_SetsvowsDirs(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "accord23"

    # WHEN
    a23_vow = vowunit_shop(a23_str, get_module_temp_dir(), in_memory_journal=True)

    # THEN
    assert a23_vow.vow_label == a23_str
    x_vows_dir = create_path(get_module_temp_dir(), "vows")
    assert a23_vow._vow_dir == create_path(x_vows_dir, a23_str)
    assert a23_vow._owners_dir == create_path(a23_vow._vow_dir, "owners")


def test_VowUnit_create_empty_plan_from_vow_ReturnsObj_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    slash_str = "/"
    x_fund_iota = 4
    x_respect_bit = 5
    x_penny = 6
    a23_vow = vowunit_shop(
        a23_str,
        vow_mstr_dir,
        bridge=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        penny=x_penny,
    )
    sue_str = "Sue"

    # WHEN
    generated_plan = a23_vow.create_empty_plan_from_vow(sue_str)

    # THEN
    assert generated_plan.bridge == slash_str
    assert generated_plan.fund_iota == x_fund_iota
    assert generated_plan.respect_bit == x_respect_bit
    assert generated_plan.penny == x_penny


def test_VowUnit_create_gut_file_if_none_SetsDirAndFiles_Scenario1_owner_dir_ExistsNoFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    a23_vow = vowunit_shop(a23_str, vow_mstr_dir)
    sue_str = "Sue"
    sue_owner_dir = create_owner_dir_path(vow_mstr_dir, a23_str, sue_str)
    assert not os_path_exists(sue_owner_dir)
    assert not gut_file_exists(vow_mstr_dir, a23_str, sue_str)

    # WHEN
    a23_vow.create_gut_file_if_none(sue_str)

    # THEN
    print(f"{vow_mstr_dir=}")
    assert gut_file_exists(vow_mstr_dir, a23_str, sue_str)
    expected_sue_gut = planunit_shop(sue_str, a23_str)
    assert open_gut_file(vow_mstr_dir, a23_str, sue_str) == expected_sue_gut


def test_VowUnit_create_gut_file_if_none_SetsDirAndFiles_Scenario2_owner_dir_ExistsNoFile_Create_gut_AndConfirmVowAttributesPassed(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    slash_str = "/"
    x_fund_iota = 4
    x_respect_bit = 5
    x_penny = 6
    a23_vow = vowunit_shop(
        a23_str,
        vow_mstr_dir,
        bridge=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        penny=x_penny,
    )
    sue_str = "Sue"
    sue_owner_dir = create_owner_dir_path(vow_mstr_dir, a23_str, sue_str)
    set_dir(sue_owner_dir)
    assert os_path_exists(sue_owner_dir)
    assert not gut_file_exists(vow_mstr_dir, a23_str, sue_str)

    # WHEN
    a23_vow.create_gut_file_if_none(sue_str)

    # THEN
    print(f"{vow_mstr_dir=}")
    assert gut_file_exists(vow_mstr_dir, a23_str, sue_str)
    generated_gut = open_gut_file(vow_mstr_dir, a23_str, sue_str)
    assert generated_gut.bridge == slash_str
    assert generated_gut.fund_iota == x_fund_iota
    assert generated_gut.respect_bit == x_respect_bit
    assert generated_gut.penny == x_penny


def test_VowUnit_create_gut_file_if_none_SetsDirAndFiles_Scenario3_FileExistsIsNotReplaced(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    a23_vow = vowunit_shop(a23_str, vow_mstr_dir)
    sue_str = "Sue"
    bob_str = "Bob"
    sue_gut = planunit_shop(sue_str, a23_str)
    sue_gut.add_acctunit(bob_str)
    save_gut_file(vow_mstr_dir, sue_gut)
    sue_owner_dir = create_owner_dir_path(vow_mstr_dir, a23_str, sue_str)
    assert os_path_exists(sue_owner_dir)
    assert gut_file_exists(vow_mstr_dir, a23_str, sue_str)

    # WHEN
    a23_vow.create_gut_file_if_none(sue_str)

    # THEN
    print(f"{vow_mstr_dir=}")
    assert gut_file_exists(vow_mstr_dir, a23_str, sue_str)
    assert open_gut_file(vow_mstr_dir, a23_str, sue_str) == sue_gut


def test_VowUnit_create_init_job_from_guts_Scenario0_CreatesFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    slash_str = "/"
    x_fund_iota = 4
    x_respect_bit = 5
    a23_vow = vowunit_shop(
        a23_str,
        vow_mstr_dir,
        bridge=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        in_memory_journal=True,
    )
    sue_str = "Sue"
    assert not job_file_exists(vow_mstr_dir, a23_str, sue_str)

    # WHEN
    a23_vow.create_init_job_from_guts(sue_str)

    # THEN
    print(f"{vow_mstr_dir=}")
    assert job_file_exists(vow_mstr_dir, a23_str, sue_str)


def test_VowUnit_create_init_job_from_guts_Scenario1_ReplacesFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    slash_str = "/"
    x_fund_iota = 4
    x_respect_bit = 5
    a23_vow = vowunit_shop(
        a23_str,
        vow_mstr_dir,
        bridge=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        in_memory_journal=True,
    )
    bob_str = "Bob"
    sue_str = "Sue"
    x0_sue_job = planunit_shop(sue_str, a23_str)
    x0_sue_job.add_acctunit(bob_str)
    save_job_file(vow_mstr_dir, x0_sue_job)
    assert open_job_file(vow_mstr_dir, a23_str, sue_str).get_acct(bob_str)

    # WHEN
    a23_vow.create_init_job_from_guts(sue_str)

    # THEN
    assert not open_job_file(vow_mstr_dir, a23_str, sue_str).get_acct(bob_str)


def test_VowUnit_create_init_job_from_guts_Scenario2_job_Has_gut_Accts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    slash_str = "/"
    x_fund_iota = 4
    x_respect_bit = 5
    a23_vow = vowunit_shop(
        a23_str,
        vow_mstr_dir,
        bridge=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        in_memory_journal=True,
    )
    bob_str = "Bob"
    sue_str = "Sue"
    a23_vow.create_init_job_from_guts(sue_str)
    sue_gut = planunit_shop(sue_str, a23_str)
    sue_gut.add_acctunit(bob_str)
    save_gut_file(vow_mstr_dir, sue_gut)
    assert not open_job_file(vow_mstr_dir, a23_str, sue_str).get_acct(bob_str)

    # WHEN
    a23_vow.create_init_job_from_guts(sue_str)

    # THEN
    assert open_job_file(vow_mstr_dir, a23_str, sue_str).get_acct(bob_str)


def test_VowUnit_create_init_job_from_guts_Scenario3_gut_FilesAreListenedTo(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    slash_str = "/"
    x_fund_iota = 4
    x_respect_bit = 5
    a23_vow = vowunit_shop(
        a23_str,
        vow_mstr_dir,
        bridge=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        in_memory_journal=True,
    )
    sue_str = "Sue"
    a23_vow.create_init_job_from_guts(sue_str)

    # create Sue gut
    bob_str = "Bob"
    sue_gut = planunit_shop(sue_str, a23_str, bridge=slash_str)
    sue_gut.add_acctunit(bob_str)
    save_gut_file(vow_mstr_dir, sue_gut)
    # create Bob gut with agenda concept for Sue
    bob_gut = planunit_shop(bob_str, a23_str, bridge=slash_str)
    bob_gut.add_acctunit(sue_str)
    casa_way = bob_gut.make_l1_way("casa")
    clean_way = bob_gut.make_way(casa_way, "clean")
    bob_gut.add_concept(clean_way, task=True)
    bob_gut.get_concept_obj(clean_way).laborunit.set_laborlink(sue_str)
    save_gut_file(vow_mstr_dir, bob_gut)
    assert not open_job_file(vow_mstr_dir, a23_str, sue_str).get_agenda_dict()

    # WHEN
    a23_vow.create_init_job_from_guts(sue_str)

    # THEN
    assert open_job_file(vow_mstr_dir, a23_str, sue_str).get_agenda_dict()
    sue_agenda = open_job_file(vow_mstr_dir, a23_str, sue_str).get_agenda_dict()
    assert len(sue_agenda) == 1
    assert sue_agenda.get(clean_way).get_concept_way() == clean_way


def test_VowUnit__set_all_healer_dutys_CorrectlySetsdutys(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    x_vow_mstr_dir = get_module_temp_dir()
    a23_vow = vowunit_shop(a23_str, x_vow_mstr_dir, in_memory_journal=True)
    sue_str = "Sue"
    yao_str = "Yao"
    a23_vow.create_init_job_from_guts(sue_str)
    a23_vow.create_init_job_from_guts(yao_str)
    sue_gut_plan = open_gut_file(x_vow_mstr_dir, a23_str, sue_str)
    yao_gut_plan = open_gut_file(x_vow_mstr_dir, a23_str, yao_str)

    sue_gut_plan.add_acctunit(sue_str)
    sue_gut_plan.add_acctunit(yao_str)
    yao_gut_plan.add_acctunit(sue_str)
    yao_gut_plan.add_acctunit(yao_str)
    texas_str = "Texas"
    texas_way = sue_gut_plan.make_l1_way(texas_str)
    sue_gut_plan.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    yao_gut_plan.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_way = sue_gut_plan.make_way(texas_way, dallas_str)
    dallas_healerlink = healerlink_shop({sue_str, yao_str})
    dallas_concept = conceptunit_shop(dallas_str, healerlink=dallas_healerlink)
    elpaso_str = "el paso"
    elpaso_way = sue_gut_plan.make_way(texas_way, elpaso_str)
    elpaso_healerlink = healerlink_shop({sue_str})
    elpaso_concept = conceptunit_shop(elpaso_str, healerlink=elpaso_healerlink)

    sue_gut_plan.set_concept(dallas_concept, texas_way)
    sue_gut_plan.set_concept(elpaso_concept, texas_way)
    yao_gut_plan.set_concept(dallas_concept, texas_way)
    yao_gut_plan.set_concept(elpaso_concept, texas_way)

    save_gut_file(x_vow_mstr_dir, sue_gut_plan)
    save_gut_file(x_vow_mstr_dir, yao_gut_plan)
    sue_filename = get_json_filename(sue_str)
    yao_filename = get_json_filename(yao_str)
    sue_dallas_hubunit = hubunit_shop(x_vow_mstr_dir, a23_str, sue_str, dallas_way)
    yao_dallas_hubunit = hubunit_shop(x_vow_mstr_dir, a23_str, yao_str, dallas_way)
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
    a23_vow._set_all_healer_dutys(sue_str)

    # THEN
    assert os_path_exists(sue_dallas_sue_duty_file_path)
    assert os_path_exists(sue_dallas_yao_duty_file_path) is False
    assert os_path_exists(yao_dallas_sue_duty_file_path)
    assert os_path_exists(yao_dallas_yao_duty_file_path) is False

    # WHEN
    a23_vow._set_all_healer_dutys(yao_str)

    # THEN
    assert os_path_exists(sue_dallas_sue_duty_file_path)
    assert os_path_exists(sue_dallas_yao_duty_file_path)
    assert os_path_exists(yao_dallas_sue_duty_file_path)
    assert os_path_exists(yao_dallas_yao_duty_file_path)


# def test_VowUnit_set_offi_time_Scenario0_SetsAttr():
#     # ESTABLISH
#     vow_mstr_dir = get_module_temp_dir()
#     time56 = 56
#     a23_vow = vowunit_shop("accord23", vow_mstr_dir, _offi_time_max=time56)
#     assert a23_vow.offi_time == 0
#     assert a23_vow._offi_time_max == time56

#     # WHEN
#     time23 = 23
#     a23_vow.set_offi_time(time23)

#     # THEN
#     assert a23_vow.offi_time == time23
#     assert a23_vow._offi_time_max == time56


# def test_VowUnit_set_offi_time_Scenario1_SetsAttr():
#     # ESTABLISH
#     a23_vow = vowunit_shop("accord23", get_module_temp_dir())
#     assert a23_vow.offi_time == 0
#     assert a23_vow._offi_time_max == 0

#     # WHEN
#     time23 = 23
#     a23_vow.set_offi_time(time23)

#     # THEN
#     assert a23_vow.offi_time == time23
#     assert a23_vow._offi_time_max == time23


def test_VowUnit_set_offi_time_max_Scenario0_SetsAttr():
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    time7 = 7
    a23_vow = vowunit_shop("accord23", vow_mstr_dir)
    a23_vow._offi_time_max = time7
    # assert a23_vow.offi_time == 0
    assert a23_vow._offi_time_max == time7

    # WHEN
    time23 = 23
    a23_vow.set_offi_time_max(time23)

    # THEN
    # assert a23_vow.offi_time == 0
    assert a23_vow._offi_time_max == time23


# def test_VowUnit_set_offi_time_max_Scenario1_SetsAttr():
#     # ESTABLISH
#     vow_mstr_dir = get_module_temp_dir()
#     time21 = 21
#     time77 = 77
#     a23_vow = vowunit_shop(
#         "accord23", vow_mstr_dir, offi_time=time21, _offi_time_max=time77
#     )
#     assert a23_vow.offi_time == time21
#     assert a23_vow._offi_time_max == time77

#     # WHEN / THEN
#     time11 = 11
#     with pytest_raises(Exception) as excinfo:
#         a23_vow.set_offi_time_max(time11)
#     exception_str = f"Cannot set _offi_time_max={time11} because it is less than offi_time={time21}"
#     assert str(excinfo.value) == exception_str


# def test_VowUnit_set_offi_time_Scenario0_SetsAttr():
#     # ESTABLISH
#     a23_vow = vowunit_shop("accord23", get_module_temp_dir())
#     assert a23_vow.offi_time == 0
#     assert a23_vow._offi_time_max == 0

#     # WHEN
#     time23 = 23
#     time55 = 55
#     a23_vow.set_offi_time(time23, time55)

#     # THEN
#     assert a23_vow.offi_time == time23
#     assert a23_vow._offi_time_max == time55
