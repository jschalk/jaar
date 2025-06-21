from src.a00_data_toolbox.file_toolbox import create_path, save_file
from src.a01_term_logic.rope import default_knot_if_None
from src.a02_finance_logic.finance_config import (
    default_fund_iota_if_None,
    default_RespectBit_if_None,
    filter_penny,
)
from src.a02_finance_logic.test._util.a02_str import bank_label_str, knot_str
from src.a06_plan_logic.test._util.a06_str import (
    fund_iota_str,
    penny_str,
    respect_bit_str,
)
from src.a07_timeline_logic.timeline import get_default_timeline_config_dict
from src.a12_hub_toolbox.hub_path import create_bank_json_path
from src.a15_bank_logic.bank import (
    bankunit_shop,
    get_from_default_path as bankunit_get_from_default_path,
    get_from_dict as bankunit_get_from_dict,
    get_from_json as bankunit_get_from_json,
)
from src.a15_bank_logic.test._util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a15_bank_logic.test._util.a15_str import (
    bank_mstr_dir_str,
    brokerunits_str,
    offi_time_str,
    paybook_str,
    timeline_str,
)


def test_BankUnit_get_dict_ReturnsObjWith_paybook():
    # ESTABLISH
    bank_mstr_dir = create_path(get_module_temp_dir(), "temp1")
    a45_str = "accord45"
    a45_offi_times = {17, 37}
    accord_bank = bankunit_shop(a45_str, bank_mstr_dir, offi_times=a45_offi_times)
    accord_offi_time_max_int = 23
    bob_str = "Bob"
    bob_x0_tran_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_tran_time = 404
    sue_x4_quota = 55
    sue_x7_tran_time = 505
    sue_x7_quota = 66
    pay_tran_time = 15
    bob_sue_amount = 30000
    accord_bank.set_offi_time_max(accord_offi_time_max_int)
    accord_bank.add_budunit(bob_str, bob_x0_tran_time, bob_x0_quota)
    accord_bank.add_budunit(sue_str, sue_x4_tran_time, sue_x4_quota)
    accord_bank.add_budunit(sue_str, sue_x7_tran_time, sue_x7_quota)
    accord_bank.add_paypurchase(
        owner_name=bob_str,
        acct_name=sue_str,
        tran_time=pay_tran_time,
        amount=bob_sue_amount,
    )

    # WHEN
    x_dict = accord_bank.get_dict()

    # THEN
    offi_times_str = f"{offi_time_str()}s"
    print(f"{ accord_bank._get_brokerunits_dict()=}")
    print(f"{ accord_bank.paybook.get_dict()=}")
    assert x_dict.get(bank_label_str()) == a45_str
    assert x_dict.get(bank_mstr_dir_str()) == bank_mstr_dir
    assert x_dict.get(timeline_str()) == get_default_timeline_config_dict()
    assert x_dict.get(offi_times_str) == list(a45_offi_times)
    assert x_dict.get(knot_str()) == default_knot_if_None()
    assert x_dict.get(fund_iota_str()) == default_fund_iota_if_None()
    assert x_dict.get(respect_bit_str()) == default_RespectBit_if_None()
    assert x_dict.get(penny_str()) == filter_penny()
    assert x_dict.get(brokerunits_str()) == accord_bank._get_brokerunits_dict()
    assert x_dict.get(paybook_str()) == accord_bank.paybook.get_dict()
    assert set(x_dict.keys()) == {
        bank_label_str(),
        bank_mstr_dir_str(),
        timeline_str(),
        offi_times_str,
        brokerunits_str(),
        knot_str(),
        fund_iota_str(),
        respect_bit_str(),
        penny_str(),
        paybook_str(),
    }


def test_BankUnit_get_dict_ReturnsObjWithOut_paybook():
    # ESTABLISH
    accord45_str = "accord45"
    accord_bank = bankunit_shop(accord45_str, get_module_temp_dir())

    # WHEN
    x_dict = accord_bank.get_dict(include_paybook=False)

    # THEN
    assert not x_dict.get(paybook_str())
    assert set(x_dict.keys()) == {
        bank_label_str(),
        bank_mstr_dir_str(),
        timeline_str(),
        f"{offi_time_str()}s",
        brokerunits_str(),
        knot_str(),
        fund_iota_str(),
        respect_bit_str(),
        penny_str(),
    }


def test_BankUnit_get_json_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_bank = bankunit_shop(accord45_str, get_module_temp_dir())
    bob_str = "Bob"
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    accord_bank.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    accord_bank.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    accord_bank.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)

    # WHEN
    x_json = accord_bank.get_json()

    # THEN
    print(f"{x_json=}")
    assert x_json
    assert x_json.find(bank_label_str()) > 0


def test_get_from_dict_ReturnsBankUnit_Scenario0_WithParameters():
    # ESTABLISH
    accord45_str = "accord45"
    bank_mstr_dir = create_path(get_module_temp_dir(), "temp1")
    a45_offi_times = {17, 37}
    accord_bank = bankunit_shop(accord45_str, bank_mstr_dir, offi_times=a45_offi_times)
    sue_timeline_label = "sue casa"
    accord_bank.timeline.timeline_label = sue_timeline_label
    sue_knot = "/"
    sue_fund_iota = 0.3
    sue_respect_bit = 2
    sue_penny = 3
    bob_str = "Bob"
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    pay_tran_time = 15
    bob_sue_amount = 30000
    accord_bank.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    accord_bank.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    accord_bank.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)
    accord_bank.knot = sue_knot
    accord_bank.fund_iota = sue_fund_iota
    accord_bank.respect_bit = sue_respect_bit
    accord_bank.penny = sue_penny
    accord_bank.add_paypurchase(
        owner_name=bob_str,
        acct_name=sue_str,
        tran_time=pay_tran_time,
        amount=bob_sue_amount,
    )
    x_dict = accord_bank.get_dict()

    # WHEN
    x_bank = bankunit_get_from_dict(x_dict)

    # THEN
    assert x_bank.bank_label == accord45_str
    assert x_bank.bank_mstr_dir == bank_mstr_dir
    assert x_bank.timeline.timeline_label == sue_timeline_label
    assert x_bank.offi_times == a45_offi_times
    assert x_bank.knot == sue_knot
    assert x_bank.fund_iota == sue_fund_iota
    assert x_bank.respect_bit == sue_respect_bit
    assert x_bank.penny == sue_penny
    assert x_bank.brokerunits == accord_bank.brokerunits
    assert x_bank.paybook == accord_bank.paybook
    assert x_bank.bank_mstr_dir == accord_bank.bank_mstr_dir
    assert x_bank != accord_bank
    x_bank._offi_time_max = 0
    assert x_bank == accord_bank


def test_get_from_dict_ReturnsBankUnit_Scenario1_WithOutParameters():
    # ESTABLISH
    accord45_str = "accord45"
    accord_bank = bankunit_shop(accord45_str, get_module_temp_dir())
    x_dict = accord_bank.get_dict()
    x_dict["timeline"] = {}
    x_dict.pop("knot")
    x_dict.pop("fund_iota")
    x_dict.pop("respect_bit")
    x_dict.pop("penny")

    # WHEN
    generated_bank = bankunit_get_from_dict(x_dict)

    # THEN
    assert generated_bank.bank_label == accord45_str
    print(f"{generated_bank.timeline=}")
    print(f"   {accord_bank.timeline=}")
    assert generated_bank.timeline == accord_bank.timeline
    assert generated_bank.offi_times == set()
    assert generated_bank.knot == default_knot_if_None()
    assert generated_bank.fund_iota == default_fund_iota_if_None()
    assert generated_bank.respect_bit == default_RespectBit_if_None()
    assert generated_bank.penny == 1
    assert generated_bank.brokerunits == accord_bank.brokerunits
    assert generated_bank.paybook == accord_bank.paybook
    assert generated_bank.bank_mstr_dir == accord_bank.bank_mstr_dir
    assert generated_bank == accord_bank


def test_get_from_json_ReturnsBankUnit():
    # ESTABLISH
    accord45_str = "accord45"
    temp_bank_mstr_dir = create_path(get_module_temp_dir(), "temp")
    accord_bank = bankunit_shop(accord45_str, temp_bank_mstr_dir)
    sue_timeline_label = "sue casa"
    accord_bank.timeline.timeline_label = sue_timeline_label
    sue_offi_time_max = 23
    sue_knot = "/"
    sue_fund_iota = 0.3
    sue_respect_bit = 2
    sue_penny = 3
    bob_str = "Bob"
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    accord_bank.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    accord_bank.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    accord_bank.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)
    accord_bank.knot = sue_knot
    accord_bank.fund_iota = sue_fund_iota
    accord_bank.respect_bit = sue_respect_bit
    accord_bank.penny = sue_penny
    accord_json = accord_bank.get_json()

    # WHEN
    x_bank = bankunit_get_from_json(accord_json)

    # THEN
    assert x_bank.bank_label == accord45_str
    assert x_bank.bank_mstr_dir == temp_bank_mstr_dir
    assert x_bank.timeline.timeline_label == sue_timeline_label
    assert x_bank.knot == sue_knot
    assert x_bank.fund_iota == sue_fund_iota
    assert x_bank.respect_bit == sue_respect_bit
    assert x_bank.penny == sue_penny
    assert x_bank.brokerunits == accord_bank.brokerunits
    assert x_bank.bank_mstr_dir == accord_bank.bank_mstr_dir
    assert x_bank != accord_bank
    x_bank._offi_time_max = 0
    assert x_bank == accord_bank


def test_get_from_file_ReturnsBankUnitWith_bank_mstr_dir(env_dir_setup_cleanup):
    # ESTABLISH
    accord45_str = "accord45"
    accord45_bank = bankunit_shop(accord45_str, get_module_temp_dir())
    sue_timeline_label = "sue casa"
    accord45_bank.timeline.timeline_label = sue_timeline_label
    sue_respect_bit = 2
    accord45_bank.respect_bit = sue_respect_bit
    x_bank_mstr_dir = create_path(get_module_temp_dir(), "fizz_buzz")
    accord45_json_path = create_bank_json_path(x_bank_mstr_dir, accord45_str)
    save_file(accord45_json_path, None, accord45_bank.get_json())
    assert accord45_bank.bank_mstr_dir != x_bank_mstr_dir

    # WHEN
    generated_a45_bank = bankunit_get_from_default_path(x_bank_mstr_dir, accord45_str)

    # THEN
    assert generated_a45_bank.bank_mstr_dir == x_bank_mstr_dir
    assert generated_a45_bank.bank_label == accord45_str
    assert generated_a45_bank.timeline.timeline_label == sue_timeline_label
    assert generated_a45_bank.respect_bit == sue_respect_bit
    x_banks_dir = create_path(x_bank_mstr_dir, "banks")
    expected_a45_bank_dir = create_path(x_banks_dir, accord45_str)
    assert generated_a45_bank._bank_dir == expected_a45_bank_dir
