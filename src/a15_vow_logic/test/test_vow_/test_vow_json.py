from src.a00_data_toolbox.file_toolbox import create_path, save_file
from src.a01_term_logic.rope import default_knot_if_None
from src.a02_finance_logic.finance_config import (
    default_fund_iota_if_None,
    default_RespectBit_if_None,
    filter_penny,
)
from src.a02_finance_logic.test._util.a02_str import knot_str, vow_label_str
from src.a06_plan_logic.test._util.a06_str import (
    fund_iota_str,
    penny_str,
    respect_bit_str,
)
from src.a07_calendar_logic.chrono import get_default_timeline_config_dict
from src.a12_hub_toolbox.hub_path import create_vow_json_path
from src.a15_vow_logic.test._util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a15_vow_logic.test._util.a15_str import (
    brokerunits_str,
    offi_time_str,
    paybook_str,
    timeline_str,
)
from src.a15_vow_logic.vow import (
    get_from_default_path as vowunit_get_from_default_path,
    get_from_dict as vowunit_get_from_dict,
    get_from_json as vowunit_get_from_json,
    vowunit_shop,
)


def test_VowUnit_get_dict_ReturnsObjWith_paybook():
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a45_str = "accord45"
    a45_offi_times = {17, 37}
    accord_vow = vowunit_shop(a45_str, vow_mstr_dir, offi_times=a45_offi_times)
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
    accord_vow.set_offi_time_max(accord_offi_time_max_int)
    accord_vow.add_budunit(bob_str, bob_x0_tran_time, bob_x0_quota)
    accord_vow.add_budunit(sue_str, sue_x4_tran_time, sue_x4_quota)
    accord_vow.add_budunit(sue_str, sue_x7_tran_time, sue_x7_quota)
    accord_vow.add_paypurchase(
        owner_name=bob_str,
        acct_name=sue_str,
        tran_time=pay_tran_time,
        amount=bob_sue_amount,
    )

    # WHEN
    x_dict = accord_vow.get_dict()

    # THEN
    offi_times_str = f"{offi_time_str()}s"
    print(f"{ accord_vow._get_brokerunits_dict()=}")
    print(f"{ accord_vow.paybook.get_dict()=}")
    assert x_dict.get(vow_label_str()) == a45_str
    assert x_dict.get(timeline_str()) == get_default_timeline_config_dict()
    assert x_dict.get(offi_times_str) == list(a45_offi_times)
    assert x_dict.get(knot_str()) == default_knot_if_None()
    assert x_dict.get(fund_iota_str()) == default_fund_iota_if_None()
    assert x_dict.get(respect_bit_str()) == default_RespectBit_if_None()
    assert x_dict.get(penny_str()) == filter_penny()
    assert x_dict.get(brokerunits_str()) == accord_vow._get_brokerunits_dict()
    assert x_dict.get(paybook_str()) == accord_vow.paybook.get_dict()
    assert set(x_dict.keys()) == {
        vow_label_str(),
        timeline_str(),
        offi_times_str,
        brokerunits_str(),
        knot_str(),
        fund_iota_str(),
        respect_bit_str(),
        penny_str(),
        paybook_str(),
    }


def test_VowUnit_get_dict_ReturnsObjWithOut_paybook():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())

    # WHEN
    x_dict = accord_vow.get_dict(include_paybook=False)

    # THEN
    assert not x_dict.get(paybook_str())
    assert set(x_dict.keys()) == {
        vow_label_str(),
        timeline_str(),
        f"{offi_time_str()}s",
        brokerunits_str(),
        knot_str(),
        fund_iota_str(),
        respect_bit_str(),
        penny_str(),
    }


def test_VowUnit_get_json_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
    bob_str = "Bob"
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    accord_vow.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    accord_vow.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    accord_vow.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)

    # WHEN
    x_json = accord_vow.get_json()

    # THEN
    print(f"{x_json=}")
    assert x_json
    assert x_json.find(vow_label_str()) > 0


def test_get_from_dict_ReturnsVowUnit_Scenario0_WithParameters():
    # ESTABLISH
    accord45_str = "accord45"
    a45_offi_times = {17, 37}
    accord_vow = vowunit_shop(accord45_str, offi_times=a45_offi_times)
    sue_timeline_label = "sue casa"
    accord_vow.timeline.timeline_label = sue_timeline_label
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
    accord_vow.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    accord_vow.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    accord_vow.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)
    accord_vow.knot = sue_knot
    accord_vow.fund_iota = sue_fund_iota
    accord_vow.respect_bit = sue_respect_bit
    accord_vow.penny = sue_penny
    accord_vow.add_paypurchase(
        owner_name=bob_str,
        acct_name=sue_str,
        tran_time=pay_tran_time,
        amount=bob_sue_amount,
    )
    x_dict = accord_vow.get_dict()

    # WHEN
    x_vow = vowunit_get_from_dict(x_dict)

    # THEN
    assert x_vow.vow_label == accord45_str
    assert x_vow.timeline.timeline_label == sue_timeline_label
    assert x_vow.offi_times == a45_offi_times
    assert x_vow.knot == sue_knot
    assert x_vow.fund_iota == sue_fund_iota
    assert x_vow.respect_bit == sue_respect_bit
    assert x_vow.penny == sue_penny
    assert x_vow.brokerunits == accord_vow.brokerunits
    assert x_vow.paybook == accord_vow.paybook
    assert x_vow.vow_mstr_dir == accord_vow.vow_mstr_dir
    assert x_vow != accord_vow
    x_vow._offi_time_max = 0
    assert x_vow == accord_vow


def test_get_from_dict_ReturnsVowUnit_Scenario1_WithOutParameters():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str)
    x_dict = accord_vow.get_dict()
    x_dict["timeline"] = {}
    x_dict.pop("knot")
    x_dict.pop("fund_iota")
    x_dict.pop("respect_bit")
    x_dict.pop("penny")

    # WHEN
    generated_vow = vowunit_get_from_dict(x_dict)

    # THEN
    assert generated_vow.vow_label == accord45_str
    print(f"{generated_vow.timeline=}")
    print(f"   {accord_vow.timeline=}")
    assert generated_vow.timeline == accord_vow.timeline
    assert generated_vow.offi_times == set()
    assert generated_vow.knot == default_knot_if_None()
    assert generated_vow.fund_iota == default_fund_iota_if_None()
    assert generated_vow.respect_bit == default_RespectBit_if_None()
    assert generated_vow.penny == 1
    assert generated_vow.brokerunits == accord_vow.brokerunits
    assert generated_vow.paybook == accord_vow.paybook
    assert generated_vow.vow_mstr_dir == accord_vow.vow_mstr_dir
    assert generated_vow == accord_vow


def test_get_from_json_ReturnsVowUnit():
    # ESTABLISH
    accord45_str = "accord45"
    accord_vow = vowunit_shop(accord45_str)
    sue_timeline_label = "sue casa"
    accord_vow.timeline.timeline_label = sue_timeline_label
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
    accord_vow.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    accord_vow.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    accord_vow.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)
    accord_vow.knot = sue_knot
    accord_vow.fund_iota = sue_fund_iota
    accord_vow.respect_bit = sue_respect_bit
    accord_vow.penny = sue_penny
    accord_json = accord_vow.get_json()

    # WHEN
    x_vow = vowunit_get_from_json(accord_json)

    # THEN
    assert x_vow.vow_label == accord45_str
    assert x_vow.timeline.timeline_label == sue_timeline_label
    assert x_vow.knot == sue_knot
    assert x_vow.fund_iota == sue_fund_iota
    assert x_vow.respect_bit == sue_respect_bit
    assert x_vow.penny == sue_penny
    assert x_vow.brokerunits == accord_vow.brokerunits
    assert x_vow.vow_mstr_dir == accord_vow.vow_mstr_dir
    assert x_vow != accord_vow
    x_vow._offi_time_max = 0
    assert x_vow == accord_vow


def test_get_from_file_ReturnsVowUnitWith_vow_mstr_dir(env_dir_setup_cleanup):
    # ESTABLISH
    accord45_str = "accord45"
    accord45_vow = vowunit_shop(accord45_str)
    sue_timeline_label = "sue casa"
    accord45_vow.timeline.timeline_label = sue_timeline_label
    sue_respect_bit = 2
    accord45_vow.respect_bit = sue_respect_bit
    x_vow_mstr_dir = create_path(get_module_temp_dir(), "fizz_buzz")
    accord45_json_path = create_vow_json_path(x_vow_mstr_dir, accord45_str)
    save_file(accord45_json_path, None, accord45_vow.get_json())
    assert accord45_vow.vow_mstr_dir != x_vow_mstr_dir

    # WHEN
    generated_a45_vow = vowunit_get_from_default_path(x_vow_mstr_dir, accord45_str)

    # THEN
    assert generated_a45_vow.vow_mstr_dir == x_vow_mstr_dir
    assert generated_a45_vow.vow_label == accord45_str
    assert generated_a45_vow.timeline.timeline_label == sue_timeline_label
    assert generated_a45_vow.respect_bit == sue_respect_bit
    x_vows_dir = create_path(x_vow_mstr_dir, "vows")
    expected_a45_vow_dir = create_path(x_vows_dir, accord45_str)
    assert generated_a45_vow._vow_dir == expected_a45_vow_dir
