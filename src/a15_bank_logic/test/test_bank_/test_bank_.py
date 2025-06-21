from os.path import exists as os_path_exists, isdir as os_path_isdir
from src.a00_data_toolbox.file_toolbox import create_path, get_json_filename, set_dir
from src.a01_term_logic.rope import default_knot_if_None
from src.a02_finance_logic.bud import tranbook_shop
from src.a02_finance_logic.finance_config import (
    default_fund_iota_if_None,
    default_RespectBit_if_None,
    filter_penny,
)
from src.a05_concept_logic.concept import conceptunit_shop
from src.a05_concept_logic.healer import healerlink_shop
from src.a06_plan_logic.plan import planunit_shop
from src.a07_timeline_logic.timeline import timelineunit_shop
from src.a12_hub_toolbox.hub_path import create_owner_dir_path, create_path
from src.a12_hub_toolbox.hub_tool import (
    gut_file_exists,
    job_file_exists,
    open_gut_file,
    open_job_file,
    save_gut_file,
    save_job_file,
)
from src.a12_hub_toolbox.hubunit import hubunit_shop
from src.a15_bank_logic.bank import (
    BankUnit,
    bankunit_shop,
    get_default_job_listen_count,
)
from src.a15_bank_logic.test._util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a15_bank_logic.test._util.a15_str import (
    bank_label_str,
    brokerunits_str,
    fund_iota_str,
    job_listen_rotations_str,
    knot_str,
    paybook_str,
    penny_str,
    respect_bit_str,
    timeline_str,
)


def test_get_default_job_listen_count_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_default_job_listen_count() == 3


def test_BankUnit_Exists():
    # ESTABLISH / WHEN
    accord_bank = BankUnit()
    # THEN
    assert not accord_bank.bank_label
    assert not accord_bank.timeline
    assert not accord_bank.brokerunits
    assert not accord_bank.paybook
    assert not accord_bank.offi_times
    assert not accord_bank.knot
    assert not accord_bank.fund_iota
    assert not accord_bank.respect_bit
    assert not accord_bank.penny
    assert not accord_bank.job_listen_rotations
    assert not accord_bank.bank_mstr_dir
    # Calculated fields
    assert not accord_bank._offi_time_max
    assert not accord_bank._owners_dir
    assert not accord_bank._packs_dir
    assert not accord_bank._all_tranbook
    assert set(accord_bank.__dict__) == {
        bank_label_str(),
        timeline_str(),
        brokerunits_str(),
        paybook_str(),
        "offi_times",
        knot_str(),
        fund_iota_str(),
        respect_bit_str(),
        penny_str(),
        job_listen_rotations_str(),
        "_bank_dir",
        "bank_mstr_dir",
        "_all_tranbook",
        "_offi_time_max",
        "_owners_dir",
        "_packs_dir",
    }


def test_bankunit_shop_ReturnsBankUnit():
    # ESTABLISH
    a23_str = "accord23"

    # WHEN
    a23_bank = bankunit_shop(a23_str, get_module_temp_dir())

    # THEN
    assert a23_bank.bank_label == a23_str
    assert a23_bank.timeline == timelineunit_shop()
    assert a23_bank.brokerunits == {}
    assert a23_bank.paybook == tranbook_shop(a23_str)
    assert a23_bank.offi_times == set()
    assert a23_bank.knot == default_knot_if_None()
    assert a23_bank.fund_iota == default_fund_iota_if_None()
    assert a23_bank.respect_bit == default_RespectBit_if_None()
    assert a23_bank.penny == filter_penny()
    assert a23_bank.bank_mstr_dir == get_module_temp_dir()
    assert a23_bank.job_listen_rotations == get_default_job_listen_count()
    # Calculated fields
    assert a23_bank._owners_dir != None
    assert a23_bank._packs_dir != None
    assert a23_bank._all_tranbook == tranbook_shop(a23_str)


def test_bankunit_shop_ReturnsBankUnitWith_banks_dir(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "accord23"

    # WHEN
    a23_bank = bankunit_shop(a23_str, bank_mstr_dir=get_module_temp_dir())

    # THEN
    assert a23_bank.bank_label == a23_str
    assert a23_bank.bank_mstr_dir == get_module_temp_dir()
    assert a23_bank._owners_dir is not None
    assert a23_bank._packs_dir is not None


def test_bankunit_shop_ReturnsBankUnitWith_knot(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "accord23"
    slash_str = "/"
    x_fund_iota = 7.0
    x_respect_bit = 9
    x_penny = 3
    a45_offi_times = {12, 15}
    x_job_listen_rotations = 888

    # WHEN
    a23_bank = bankunit_shop(
        bank_label=a23_str,
        bank_mstr_dir=get_module_temp_dir(),
        offi_times=a45_offi_times,
        knot=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        penny=x_penny,
        job_listen_rotations=x_job_listen_rotations,
    )

    # THEN
    assert a23_bank.knot == slash_str
    assert a23_bank.fund_iota == x_fund_iota
    assert a23_bank.respect_bit == x_respect_bit
    assert a23_bank.penny == x_penny
    assert a23_bank.offi_times == a45_offi_times
    assert a23_bank.job_listen_rotations == x_job_listen_rotations


def test_BankUnit_set_bank_dirs_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "accord23"
    accord_bank = BankUnit(a23_str, get_module_temp_dir())
    x_banks_dir = create_path(get_module_temp_dir(), "banks")
    x_bank_dir = create_path(x_banks_dir, a23_str)
    x_owners_dir = create_path(x_bank_dir, "owners")
    x_packs_dir = create_path(x_bank_dir, "packs")

    assert not accord_bank._bank_dir
    assert not accord_bank._owners_dir
    assert not accord_bank._packs_dir
    assert os_path_exists(x_bank_dir) is False
    assert os_path_isdir(x_bank_dir) is False
    assert os_path_exists(x_owners_dir) is False
    assert os_path_exists(x_packs_dir) is False

    # WHEN
    accord_bank._set_bank_dirs()

    # THEN
    assert accord_bank._bank_dir == x_bank_dir
    assert accord_bank._owners_dir == x_owners_dir
    assert accord_bank._packs_dir == x_packs_dir
    assert os_path_exists(x_bank_dir)
    assert os_path_isdir(x_bank_dir)
    assert os_path_exists(x_owners_dir)
    assert os_path_exists(x_packs_dir)


def test_bankunit_shop_SetsbanksDirs(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "accord23"

    # WHEN
    a23_bank = bankunit_shop(a23_str, get_module_temp_dir())

    # THEN
    assert a23_bank.bank_label == a23_str
    x_banks_dir = create_path(get_module_temp_dir(), "banks")
    assert a23_bank._bank_dir == create_path(x_banks_dir, a23_str)
    assert a23_bank._owners_dir == create_path(a23_bank._bank_dir, "owners")


def test_BankUnit_create_empty_plan_from_bank_ReturnsObj_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bank_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    slash_str = "/"
    x_fund_iota = 4
    x_respect_bit = 5
    x_penny = 6
    a23_bank = bankunit_shop(
        a23_str,
        bank_mstr_dir,
        knot=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        penny=x_penny,
    )
    sue_str = "Sue"

    # WHEN
    generated_plan = a23_bank.create_empty_plan_from_bank(sue_str)

    # THEN
    assert generated_plan.knot == slash_str
    assert generated_plan.fund_iota == x_fund_iota
    assert generated_plan.respect_bit == x_respect_bit
    assert generated_plan.penny == x_penny


def test_BankUnit_create_gut_file_if_none_SetsDirAndFiles_Scenario1_owner_dir_ExistsNoFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bank_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    a23_bank = bankunit_shop(a23_str, bank_mstr_dir)
    sue_str = "Sue"
    sue_owner_dir = create_owner_dir_path(bank_mstr_dir, a23_str, sue_str)
    assert not os_path_exists(sue_owner_dir)
    assert not gut_file_exists(bank_mstr_dir, a23_str, sue_str)

    # WHEN
    a23_bank.create_gut_file_if_none(sue_str)

    # THEN
    print(f"{bank_mstr_dir=}")
    assert gut_file_exists(bank_mstr_dir, a23_str, sue_str)
    expected_sue_gut = planunit_shop(sue_str, a23_str)
    assert open_gut_file(bank_mstr_dir, a23_str, sue_str) == expected_sue_gut


def test_BankUnit_create_gut_file_if_none_SetsDirAndFiles_Scenario2_owner_dir_ExistsNoFile_Create_gut_AndConfirmBankAttributesPassed(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bank_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    slash_str = "/"
    x_fund_iota = 4
    x_respect_bit = 5
    x_penny = 6
    a23_bank = bankunit_shop(
        a23_str,
        bank_mstr_dir,
        knot=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        penny=x_penny,
    )
    sue_str = "Sue"
    sue_owner_dir = create_owner_dir_path(bank_mstr_dir, a23_str, sue_str)
    set_dir(sue_owner_dir)
    assert os_path_exists(sue_owner_dir)
    assert not gut_file_exists(bank_mstr_dir, a23_str, sue_str)

    # WHEN
    a23_bank.create_gut_file_if_none(sue_str)

    # THEN
    print(f"{bank_mstr_dir=}")
    assert gut_file_exists(bank_mstr_dir, a23_str, sue_str)
    generated_gut = open_gut_file(bank_mstr_dir, a23_str, sue_str)
    assert generated_gut.knot == slash_str
    assert generated_gut.fund_iota == x_fund_iota
    assert generated_gut.respect_bit == x_respect_bit
    assert generated_gut.penny == x_penny


def test_BankUnit_create_gut_file_if_none_SetsDirAndFiles_Scenario3_FileExistsIsNotReplaced(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bank_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    a23_bank = bankunit_shop(a23_str, bank_mstr_dir)
    sue_str = "Sue"
    bob_str = "Bob"
    sue_gut = planunit_shop(sue_str, a23_str)
    sue_gut.add_acctunit(bob_str)
    save_gut_file(bank_mstr_dir, sue_gut)
    sue_owner_dir = create_owner_dir_path(bank_mstr_dir, a23_str, sue_str)
    assert os_path_exists(sue_owner_dir)
    assert gut_file_exists(bank_mstr_dir, a23_str, sue_str)

    # WHEN
    a23_bank.create_gut_file_if_none(sue_str)

    # THEN
    print(f"{bank_mstr_dir=}")
    assert gut_file_exists(bank_mstr_dir, a23_str, sue_str)
    assert open_gut_file(bank_mstr_dir, a23_str, sue_str) == sue_gut


def test_BankUnit_create_init_job_from_guts_Scenario0_CreatesFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bank_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    slash_str = "/"
    x_fund_iota = 4
    x_respect_bit = 5
    a23_bank = bankunit_shop(
        a23_str,
        bank_mstr_dir,
        knot=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
    )
    sue_str = "Sue"
    assert not job_file_exists(bank_mstr_dir, a23_str, sue_str)

    # WHEN
    a23_bank.create_init_job_from_guts(sue_str)

    # THEN
    print(f"{bank_mstr_dir=}")
    assert job_file_exists(bank_mstr_dir, a23_str, sue_str)


def test_BankUnit_create_init_job_from_guts_Scenario1_ReplacesFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bank_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    slash_str = "/"
    x_fund_iota = 4
    x_respect_bit = 5
    a23_bank = bankunit_shop(
        a23_str,
        bank_mstr_dir,
        knot=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
    )
    bob_str = "Bob"
    sue_str = "Sue"
    x0_sue_job = planunit_shop(sue_str, a23_str)
    x0_sue_job.add_acctunit(bob_str)
    save_job_file(bank_mstr_dir, x0_sue_job)
    assert open_job_file(bank_mstr_dir, a23_str, sue_str).get_acct(bob_str)

    # WHEN
    a23_bank.create_init_job_from_guts(sue_str)

    # THEN
    assert not open_job_file(bank_mstr_dir, a23_str, sue_str).get_acct(bob_str)


def test_BankUnit_create_init_job_from_guts_Scenario2_job_Has_gut_Accts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bank_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    slash_str = "/"
    x_fund_iota = 4
    x_respect_bit = 5
    a23_bank = bankunit_shop(
        a23_str,
        bank_mstr_dir,
        knot=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
    )
    bob_str = "Bob"
    sue_str = "Sue"
    a23_bank.create_init_job_from_guts(sue_str)
    sue_gut = planunit_shop(sue_str, a23_str)
    sue_gut.add_acctunit(bob_str)
    save_gut_file(bank_mstr_dir, sue_gut)
    assert not open_job_file(bank_mstr_dir, a23_str, sue_str).get_acct(bob_str)

    # WHEN
    a23_bank.create_init_job_from_guts(sue_str)

    # THEN
    assert open_job_file(bank_mstr_dir, a23_str, sue_str).get_acct(bob_str)


def test_BankUnit_create_init_job_from_guts_Scenario3_gut_FilesAreListenedTo(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bank_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    slash_str = "/"
    x_fund_iota = 4
    x_respect_bit = 5
    a23_bank = bankunit_shop(
        a23_str,
        bank_mstr_dir,
        knot=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
    )
    sue_str = "Sue"
    a23_bank.create_init_job_from_guts(sue_str)

    # create Sue gut
    bob_str = "Bob"
    sue_gut = planunit_shop(sue_str, a23_str, knot=slash_str)
    sue_gut.add_acctunit(bob_str)
    save_gut_file(bank_mstr_dir, sue_gut)
    # create Bob gut with agenda concept for Sue
    bob_gut = planunit_shop(bob_str, a23_str, knot=slash_str)
    bob_gut.add_acctunit(sue_str)
    casa_rope = bob_gut.make_l1_rope("casa")
    clean_rope = bob_gut.make_rope(casa_rope, "clean")
    bob_gut.add_concept(clean_rope, task=True)
    bob_gut.get_concept_obj(clean_rope).laborunit.set_laborlink(sue_str)
    save_gut_file(bank_mstr_dir, bob_gut)
    assert not open_job_file(bank_mstr_dir, a23_str, sue_str).get_agenda_dict()

    # WHEN
    a23_bank.create_init_job_from_guts(sue_str)

    # THEN
    assert open_job_file(bank_mstr_dir, a23_str, sue_str).get_agenda_dict()
    sue_agenda = open_job_file(bank_mstr_dir, a23_str, sue_str).get_agenda_dict()
    assert len(sue_agenda) == 1
    assert sue_agenda.get(clean_rope).get_concept_rope() == clean_rope


def test_BankUnit__set_all_healer_dutys_CorrectlySetsdutys(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    x_bank_mstr_dir = get_module_temp_dir()
    a23_bank = bankunit_shop(a23_str, x_bank_mstr_dir)
    sue_str = "Sue"
    yao_str = "Yao"
    a23_bank.create_init_job_from_guts(sue_str)
    a23_bank.create_init_job_from_guts(yao_str)
    sue_gut_plan = open_gut_file(x_bank_mstr_dir, a23_str, sue_str)
    yao_gut_plan = open_gut_file(x_bank_mstr_dir, a23_str, yao_str)

    sue_gut_plan.add_acctunit(sue_str)
    sue_gut_plan.add_acctunit(yao_str)
    yao_gut_plan.add_acctunit(sue_str)
    yao_gut_plan.add_acctunit(yao_str)
    texas_str = "Texas"
    texas_rope = sue_gut_plan.make_l1_rope(texas_str)
    sue_gut_plan.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    yao_gut_plan.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_rope = sue_gut_plan.make_rope(texas_rope, dallas_str)
    dallas_healerlink = healerlink_shop({sue_str, yao_str})
    dallas_concept = conceptunit_shop(dallas_str, healerlink=dallas_healerlink)
    elpaso_str = "el paso"
    elpaso_rope = sue_gut_plan.make_rope(texas_rope, elpaso_str)
    elpaso_healerlink = healerlink_shop({sue_str})
    elpaso_concept = conceptunit_shop(elpaso_str, healerlink=elpaso_healerlink)

    sue_gut_plan.set_concept(dallas_concept, texas_rope)
    sue_gut_plan.set_concept(elpaso_concept, texas_rope)
    yao_gut_plan.set_concept(dallas_concept, texas_rope)
    yao_gut_plan.set_concept(elpaso_concept, texas_rope)

    save_gut_file(x_bank_mstr_dir, sue_gut_plan)
    save_gut_file(x_bank_mstr_dir, yao_gut_plan)
    sue_filename = get_json_filename(sue_str)
    yao_filename = get_json_filename(yao_str)
    sue_dallas_hubunit = hubunit_shop(x_bank_mstr_dir, a23_str, sue_str, dallas_rope)
    yao_dallas_hubunit = hubunit_shop(x_bank_mstr_dir, a23_str, yao_str, dallas_rope)
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
    a23_bank._set_all_healer_dutys(sue_str)

    # THEN
    assert os_path_exists(sue_dallas_sue_duty_file_path)
    assert os_path_exists(sue_dallas_yao_duty_file_path) is False
    assert os_path_exists(yao_dallas_sue_duty_file_path)
    assert os_path_exists(yao_dallas_yao_duty_file_path) is False

    # WHEN
    a23_bank._set_all_healer_dutys(yao_str)

    # THEN
    assert os_path_exists(sue_dallas_sue_duty_file_path)
    assert os_path_exists(sue_dallas_yao_duty_file_path)
    assert os_path_exists(yao_dallas_sue_duty_file_path)
    assert os_path_exists(yao_dallas_yao_duty_file_path)


# def test_BankUnit_set_offi_time_Scenario0_SetsAttr():
#     # ESTABLISH
#     bank_mstr_dir = get_module_temp_dir()
#     time56 = 56
#     a23_bank = bankunit_shop("accord23", bank_mstr_dir, _offi_time_max=time56)
#     assert a23_bank.offi_time == 0
#     assert a23_bank._offi_time_max == time56

#     # WHEN
#     time23 = 23
#     a23_bank.set_offi_time(time23)

#     # THEN
#     assert a23_bank.offi_time == time23
#     assert a23_bank._offi_time_max == time56


# def test_BankUnit_set_offi_time_Scenario1_SetsAttr():
#     # ESTABLISH
#     a23_bank = bankunit_shop("accord23", get_module_temp_dir())
#     assert a23_bank.offi_time == 0
#     assert a23_bank._offi_time_max == 0

#     # WHEN
#     time23 = 23
#     a23_bank.set_offi_time(time23)

#     # THEN
#     assert a23_bank.offi_time == time23
#     assert a23_bank._offi_time_max == time23


def test_BankUnit_set_offi_time_max_Scenario0_SetsAttr():
    # ESTABLISH
    bank_mstr_dir = get_module_temp_dir()
    time7 = 7
    a23_bank = bankunit_shop("accord23", bank_mstr_dir)
    a23_bank._offi_time_max = time7
    # assert a23_bank.offi_time == 0
    assert a23_bank._offi_time_max == time7

    # WHEN
    time23 = 23
    a23_bank.set_offi_time_max(time23)

    # THEN
    # assert a23_bank.offi_time == 0
    assert a23_bank._offi_time_max == time23


# def test_BankUnit_set_offi_time_max_Scenario1_SetsAttr():
#     # ESTABLISH
#     bank_mstr_dir = get_module_temp_dir()
#     time21 = 21
#     time77 = 77
#     a23_bank = bankunit_shop(
#         "accord23", bank_mstr_dir, offi_time=time21, _offi_time_max=time77
#     )
#     assert a23_bank.offi_time == time21
#     assert a23_bank._offi_time_max == time77

#     # WHEN / THEN
#     time11 = 11
#     with pytest_raises(Exception) as excinfo:
#         a23_bank.set_offi_time_max(time11)
#     exception_str = f"Cannot set _offi_time_max={time11} because it is less than offi_time={time21}"
#     assert str(excinfo.value) == exception_str


# def test_BankUnit_set_offi_time_Scenario0_SetsAttr():
#     # ESTABLISH
#     a23_bank = bankunit_shop("accord23", get_module_temp_dir())
#     assert a23_bank.offi_time == 0
#     assert a23_bank._offi_time_max == 0

#     # WHEN
#     time23 = 23
#     time55 = 55
#     a23_bank.set_offi_time(time23, time55)

#     # THEN
#     assert a23_bank.offi_time == time23
#     assert a23_bank._offi_time_max == time55
