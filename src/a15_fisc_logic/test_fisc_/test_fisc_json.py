from src.a00_data_toolbox.file_toolbox import create_path, save_file
from src.a01_term_logic.way import default_bridge_if_None
from src.a02_finance_logic._test_util.a02_str import bridge_str, fisc_label_str
from src.a02_finance_logic.finance_config import (
    default_fund_coin_if_None,
    default_RespectBit_if_None,
    filter_penny,
)
from src.a06_bud_logic._test_util.a06_str import (
    fund_coin_str,
    penny_str,
    respect_bit_str,
)
from src.a07_calendar_logic.chrono import get_default_timeline_config_dict
from src.a12_hub_tools.hub_path import create_fisc_json_path
from src.a15_fisc_logic._test_util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a15_fisc_logic._test_util.a15_str import (
    brokerunits_str,
    cashbook_str,
    offi_time_str,
    timeline_str,
)
from src.a15_fisc_logic.fisc import (
    fiscunit_shop,
)
from src.a15_fisc_logic.fisc import (
    get_from_default_path as fiscunit_get_from_default_path,
)
from src.a15_fisc_logic.fisc import get_from_dict as fiscunit_get_from_dict
from src.a15_fisc_logic.fisc import get_from_json as fiscunit_get_from_json


def test_FiscUnit_get_dict_ReturnsObjWith_cashbook():
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a45_str = "accord45"
    a45_offi_times = {17, 37}
    accord_fisc = fiscunit_shop(a45_str, fisc_mstr_dir, offi_times=a45_offi_times)
    accord_offi_time_max_int = 23
    bob_str = "Bob"
    bob_x0_tran_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_tran_time = 404
    sue_x4_quota = 55
    sue_x7_tran_time = 505
    sue_x7_quota = 66
    cash_tran_time = 15
    bob_sue_amount = 30000
    accord_fisc.set_offi_time_max(accord_offi_time_max_int)
    accord_fisc.add_dealunit(bob_str, bob_x0_tran_time, bob_x0_quota)
    accord_fisc.add_dealunit(sue_str, sue_x4_tran_time, sue_x4_quota)
    accord_fisc.add_dealunit(sue_str, sue_x7_tran_time, sue_x7_quota)
    accord_fisc.add_cashpurchase(
        owner_name=bob_str,
        acct_name=sue_str,
        tran_time=cash_tran_time,
        amount=bob_sue_amount,
    )

    # WHEN
    x_dict = accord_fisc.get_dict()

    # THEN
    offi_times_str = f"{offi_time_str()}s"
    print(f"{ accord_fisc._get_brokerunits_dict()=}")
    print(f"{ accord_fisc.cashbook.get_dict()=}")
    assert x_dict.get(fisc_label_str()) == a45_str
    assert x_dict.get(timeline_str()) == get_default_timeline_config_dict()
    assert x_dict.get(offi_times_str) == list(a45_offi_times)
    assert x_dict.get(bridge_str()) == default_bridge_if_None()
    assert x_dict.get(fund_coin_str()) == default_fund_coin_if_None()
    assert x_dict.get(respect_bit_str()) == default_RespectBit_if_None()
    assert x_dict.get(penny_str()) == filter_penny()
    assert x_dict.get(brokerunits_str()) == accord_fisc._get_brokerunits_dict()
    assert x_dict.get(cashbook_str()) == accord_fisc.cashbook.get_dict()
    assert set(x_dict.keys()) == {
        fisc_label_str(),
        timeline_str(),
        offi_times_str,
        brokerunits_str(),
        bridge_str(),
        fund_coin_str(),
        respect_bit_str(),
        penny_str(),
        cashbook_str(),
    }


def test_FiscUnit_get_dict_ReturnsObjWithOut_cashbook():
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = fiscunit_shop(accord45_str, get_module_temp_dir())

    # WHEN
    x_dict = accord_fisc.get_dict(include_cashbook=False)

    # THEN
    assert not x_dict.get(cashbook_str())
    assert set(x_dict.keys()) == {
        fisc_label_str(),
        timeline_str(),
        f"{offi_time_str()}s",
        brokerunits_str(),
        bridge_str(),
        fund_coin_str(),
        respect_bit_str(),
        penny_str(),
    }


def test_FiscUnit_get_json_ReturnsObj():
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = fiscunit_shop(accord45_str, get_module_temp_dir())
    bob_str = "Bob"
    bob_x0_deal_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_deal_time = 4
    sue_x4_quota = 55
    sue_x7_deal_time = 7
    sue_x7_quota = 66
    accord_fisc.add_dealunit(bob_str, bob_x0_deal_time, bob_x0_quota)
    accord_fisc.add_dealunit(sue_str, sue_x4_deal_time, sue_x4_quota)
    accord_fisc.add_dealunit(sue_str, sue_x7_deal_time, sue_x7_quota)

    # WHEN
    x_json = accord_fisc.get_json()

    # THEN
    print(f"{x_json=}")
    assert x_json
    assert x_json.find(fisc_label_str()) > 0


def test_get_from_dict_ReturnsFiscUnit_Scenario0_WithParameters():
    # ESTABLISH
    accord45_str = "accord45"
    a45_offi_times = {17, 37}
    accord_fisc = fiscunit_shop(accord45_str, offi_times=a45_offi_times)
    sue_timeline_label = "sue casa"
    accord_fisc.timeline.timeline_label = sue_timeline_label
    sue_bridge = "/"
    sue_fund_coin = 0.3
    sue_respect_bit = 2
    sue_penny = 3
    bob_str = "Bob"
    bob_x0_deal_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_deal_time = 4
    sue_x4_quota = 55
    sue_x7_deal_time = 7
    sue_x7_quota = 66
    cash_tran_time = 15
    bob_sue_amount = 30000
    accord_fisc.add_dealunit(bob_str, bob_x0_deal_time, bob_x0_quota)
    accord_fisc.add_dealunit(sue_str, sue_x4_deal_time, sue_x4_quota)
    accord_fisc.add_dealunit(sue_str, sue_x7_deal_time, sue_x7_quota)
    accord_fisc.bridge = sue_bridge
    accord_fisc.fund_coin = sue_fund_coin
    accord_fisc.respect_bit = sue_respect_bit
    accord_fisc.penny = sue_penny
    accord_fisc.add_cashpurchase(
        owner_name=bob_str,
        acct_name=sue_str,
        tran_time=cash_tran_time,
        amount=bob_sue_amount,
    )
    x_dict = accord_fisc.get_dict()

    # WHEN
    x_fisc = fiscunit_get_from_dict(x_dict)

    # THEN
    assert x_fisc.fisc_label == accord45_str
    assert x_fisc.timeline.timeline_label == sue_timeline_label
    assert x_fisc.offi_times == a45_offi_times
    assert x_fisc.bridge == sue_bridge
    assert x_fisc.fund_coin == sue_fund_coin
    assert x_fisc.respect_bit == sue_respect_bit
    assert x_fisc.penny == sue_penny
    assert x_fisc.brokerunits == accord_fisc.brokerunits
    assert x_fisc.cashbook == accord_fisc.cashbook
    assert x_fisc.fisc_mstr_dir == accord_fisc.fisc_mstr_dir
    assert x_fisc != accord_fisc
    x_fisc._offi_time_max = 0
    assert x_fisc == accord_fisc


def test_get_from_dict_ReturnsFiscUnit_Scenario1_WithOutParameters():
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = fiscunit_shop(accord45_str)
    x_dict = accord_fisc.get_dict()
    x_dict["timeline"] = {}
    x_dict.pop("bridge")
    x_dict.pop("fund_coin")
    x_dict.pop("respect_bit")
    x_dict.pop("penny")

    # WHEN
    generated_fisc = fiscunit_get_from_dict(x_dict)

    # THEN
    assert generated_fisc.fisc_label == accord45_str
    print(f"{generated_fisc.timeline=}")
    print(f"   {accord_fisc.timeline=}")
    assert generated_fisc.timeline == accord_fisc.timeline
    assert generated_fisc.offi_times == set()
    assert generated_fisc.bridge == default_bridge_if_None()
    assert generated_fisc.fund_coin == default_fund_coin_if_None()
    assert generated_fisc.respect_bit == default_RespectBit_if_None()
    assert generated_fisc.penny == 1
    assert generated_fisc.brokerunits == accord_fisc.brokerunits
    assert generated_fisc.cashbook == accord_fisc.cashbook
    assert generated_fisc.fisc_mstr_dir == accord_fisc.fisc_mstr_dir
    assert generated_fisc == accord_fisc


def test_get_from_json_ReturnsFiscUnit():
    # ESTABLISH
    accord45_str = "accord45"
    accord_fisc = fiscunit_shop(accord45_str)
    sue_timeline_label = "sue casa"
    accord_fisc.timeline.timeline_label = sue_timeline_label
    sue_offi_time_max = 23
    sue_bridge = "/"
    sue_fund_coin = 0.3
    sue_respect_bit = 2
    sue_penny = 3
    bob_str = "Bob"
    bob_x0_deal_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_deal_time = 4
    sue_x4_quota = 55
    sue_x7_deal_time = 7
    sue_x7_quota = 66
    accord_fisc.add_dealunit(bob_str, bob_x0_deal_time, bob_x0_quota)
    accord_fisc.add_dealunit(sue_str, sue_x4_deal_time, sue_x4_quota)
    accord_fisc.add_dealunit(sue_str, sue_x7_deal_time, sue_x7_quota)
    accord_fisc.bridge = sue_bridge
    accord_fisc.fund_coin = sue_fund_coin
    accord_fisc.respect_bit = sue_respect_bit
    accord_fisc.penny = sue_penny
    accord_json = accord_fisc.get_json()

    # WHEN
    x_fisc = fiscunit_get_from_json(accord_json)

    # THEN
    assert x_fisc.fisc_label == accord45_str
    assert x_fisc.timeline.timeline_label == sue_timeline_label
    assert x_fisc.bridge == sue_bridge
    assert x_fisc.fund_coin == sue_fund_coin
    assert x_fisc.respect_bit == sue_respect_bit
    assert x_fisc.penny == sue_penny
    assert x_fisc.brokerunits == accord_fisc.brokerunits
    assert x_fisc.fisc_mstr_dir == accord_fisc.fisc_mstr_dir
    assert x_fisc != accord_fisc
    x_fisc._offi_time_max = 0
    assert x_fisc == accord_fisc


def test_get_from_file_ReturnsFiscUnitWith_fisc_mstr_dir(env_dir_setup_cleanup):
    # ESTABLISH
    accord45_str = "accord45"
    accord45_fisc = fiscunit_shop(accord45_str)
    sue_timeline_label = "sue casa"
    accord45_fisc.timeline.timeline_label = sue_timeline_label
    sue_respect_bit = 2
    accord45_fisc.respect_bit = sue_respect_bit
    x_fisc_mstr_dir = create_path(get_module_temp_dir(), "fizz_buzz")
    accord45_json_path = create_fisc_json_path(x_fisc_mstr_dir, accord45_str)
    save_file(accord45_json_path, None, accord45_fisc.get_json())
    assert accord45_fisc.fisc_mstr_dir != x_fisc_mstr_dir

    # WHEN
    generated_a45_fisc = fiscunit_get_from_default_path(x_fisc_mstr_dir, accord45_str)

    # THEN
    assert generated_a45_fisc.fisc_mstr_dir == x_fisc_mstr_dir
    assert generated_a45_fisc.fisc_label == accord45_str
    assert generated_a45_fisc.timeline.timeline_label == sue_timeline_label
    assert generated_a45_fisc.respect_bit == sue_respect_bit
    x_fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    expected_a45_fisc_dir = create_path(x_fiscs_dir, accord45_str)
    assert generated_a45_fisc._fisc_dir == expected_a45_fisc_dir
