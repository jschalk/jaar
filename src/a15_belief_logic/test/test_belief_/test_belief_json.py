from src.a00_data_toolbox.file_toolbox import create_path, save_file
from src.a01_term_logic.rope import default_knot_if_None
from src.a02_finance_logic.finance_config import (
    default_fund_iota_if_None,
    default_RespectBit_if_None,
    filter_penny,
)
from src.a02_finance_logic.test._util.a02_str import knot_str
from src.a06_believer_logic.test._util.a06_str import (
    belief_label_str,
    fund_iota_str,
    penny_str,
    respect_bit_str,
)
from src.a07_timeline_logic.timeline import get_default_timeline_config_dict
from src.a12_hub_toolbox.hub_path import create_belief_json_path
from src.a15_belief_logic.belief import (
    beliefunit_shop,
    get_default_path_beliefunit,
    get_from_dict as beliefunit_get_from_dict,
    get_from_json as beliefunit_get_from_json,
)
from src.a15_belief_logic.test._util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a15_belief_logic.test._util.a15_str import (
    belief_mstr_dir_str,
    brokerunits_str,
    offi_time_str,
    paybook_str,
    timeline_str,
)


def test_BeliefUnit_get_dict_ReturnsObjWith_paybook():
    # ESTABLISH
    belief_mstr_dir = create_path(get_module_temp_dir(), "temp1")
    a45_str = "amy45"
    a45_offi_times = {17, 37}
    amy_belief = beliefunit_shop(a45_str, belief_mstr_dir, offi_times=a45_offi_times)
    amy_offi_time_max_int = 23
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
    amy_belief.set_offi_time_max(amy_offi_time_max_int)
    amy_belief.add_budunit(bob_str, bob_x0_tran_time, bob_x0_quota)
    amy_belief.add_budunit(sue_str, sue_x4_tran_time, sue_x4_quota)
    amy_belief.add_budunit(sue_str, sue_x7_tran_time, sue_x7_quota)
    amy_belief.add_paypurchase(
        believer_name=bob_str,
        acct_name=sue_str,
        tran_time=pay_tran_time,
        amount=bob_sue_amount,
    )

    # WHEN
    x_dict = amy_belief.get_dict()

    # THEN
    offi_times_str = f"{offi_time_str()}s"
    print(f"{ amy_belief._get_brokerunits_dict()=}")
    print(f"{ amy_belief.paybook.get_dict()=}")
    assert x_dict.get(belief_label_str()) == a45_str
    assert x_dict.get(belief_mstr_dir_str()) == belief_mstr_dir
    assert x_dict.get(timeline_str()) == get_default_timeline_config_dict()
    assert x_dict.get(offi_times_str) == list(a45_offi_times)
    assert x_dict.get(knot_str()) == default_knot_if_None()
    assert x_dict.get(fund_iota_str()) == default_fund_iota_if_None()
    assert x_dict.get(respect_bit_str()) == default_RespectBit_if_None()
    assert x_dict.get(penny_str()) == filter_penny()
    assert x_dict.get(brokerunits_str()) == amy_belief._get_brokerunits_dict()
    assert x_dict.get(paybook_str()) == amy_belief.paybook.get_dict()
    assert set(x_dict.keys()) == {
        belief_label_str(),
        belief_mstr_dir_str(),
        timeline_str(),
        offi_times_str,
        brokerunits_str(),
        knot_str(),
        fund_iota_str(),
        respect_bit_str(),
        penny_str(),
        paybook_str(),
    }


def test_BeliefUnit_get_dict_ReturnsObjWithOut_paybook():
    # ESTABLISH
    amy45_str = "amy45"
    amy_belief = beliefunit_shop(amy45_str, get_module_temp_dir())

    # WHEN
    x_dict = amy_belief.get_dict(include_paybook=False)

    # THEN
    assert not x_dict.get(paybook_str())
    assert set(x_dict.keys()) == {
        belief_label_str(),
        belief_mstr_dir_str(),
        timeline_str(),
        f"{offi_time_str()}s",
        brokerunits_str(),
        knot_str(),
        fund_iota_str(),
        respect_bit_str(),
        penny_str(),
    }


def test_BeliefUnit_get_json_ReturnsObj():
    # ESTABLISH
    amy45_str = "amy45"
    amy_belief = beliefunit_shop(amy45_str, get_module_temp_dir())
    bob_str = "Bob"
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    amy_belief.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    amy_belief.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    amy_belief.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)

    # WHEN
    x_json = amy_belief.get_json()

    # THEN
    print(f"{x_json=}")
    assert x_json
    assert x_json.find(belief_label_str()) > 0


def test_get_from_dict_ReturnsBeliefUnit_Scenario0_WithParameters():
    # ESTABLISH
    amy45_str = "amy45"
    belief_mstr_dir = create_path(get_module_temp_dir(), "temp1")
    a45_offi_times = {17, 37}
    amy_belief = beliefunit_shop(amy45_str, belief_mstr_dir, offi_times=a45_offi_times)
    sue_timeline_label = "sue casa"
    amy_belief.timeline.timeline_label = sue_timeline_label
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
    amy_belief.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    amy_belief.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    amy_belief.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)
    amy_belief.knot = sue_knot
    amy_belief.fund_iota = sue_fund_iota
    amy_belief.respect_bit = sue_respect_bit
    amy_belief.penny = sue_penny
    amy_belief.add_paypurchase(
        believer_name=bob_str,
        acct_name=sue_str,
        tran_time=pay_tran_time,
        amount=bob_sue_amount,
    )
    x_dict = amy_belief.get_dict()

    # WHEN
    x_belief = beliefunit_get_from_dict(x_dict)

    # THEN
    assert x_belief.belief_label == amy45_str
    assert x_belief.belief_mstr_dir == belief_mstr_dir
    assert x_belief.timeline.timeline_label == sue_timeline_label
    assert x_belief.offi_times == a45_offi_times
    assert x_belief.knot == sue_knot
    assert x_belief.fund_iota == sue_fund_iota
    assert x_belief.respect_bit == sue_respect_bit
    assert x_belief.penny == sue_penny
    assert x_belief.brokerunits == amy_belief.brokerunits
    assert x_belief.paybook == amy_belief.paybook
    assert x_belief.belief_mstr_dir == amy_belief.belief_mstr_dir
    assert x_belief != amy_belief
    x_belief._offi_time_max = 0
    assert x_belief == amy_belief


def test_get_from_dict_ReturnsBeliefUnit_Scenario1_WithOutParameters():
    # ESTABLISH
    amy45_str = "amy45"
    amy_belief = beliefunit_shop(amy45_str, get_module_temp_dir())
    x_dict = amy_belief.get_dict()
    x_dict["timeline"] = {}
    x_dict.pop("knot")
    x_dict.pop("fund_iota")
    x_dict.pop("respect_bit")
    x_dict.pop("penny")

    # WHEN
    generated_belief = beliefunit_get_from_dict(x_dict)

    # THEN
    assert generated_belief.belief_label == amy45_str
    print(f"{generated_belief.timeline=}")
    print(f"   {amy_belief.timeline=}")
    assert generated_belief.timeline == amy_belief.timeline
    assert generated_belief.offi_times == set()
    assert generated_belief.knot == default_knot_if_None()
    assert generated_belief.fund_iota == default_fund_iota_if_None()
    assert generated_belief.respect_bit == default_RespectBit_if_None()
    assert generated_belief.penny == 1
    assert generated_belief.brokerunits == amy_belief.brokerunits
    assert generated_belief.paybook == amy_belief.paybook
    assert generated_belief.belief_mstr_dir == amy_belief.belief_mstr_dir
    assert generated_belief == amy_belief


def test_get_from_json_ReturnsBeliefUnit():
    # ESTABLISH
    amy45_str = "amy45"
    temp_belief_mstr_dir = create_path(get_module_temp_dir(), "temp")
    amy_belief = beliefunit_shop(amy45_str, temp_belief_mstr_dir)
    sue_timeline_label = "sue casa"
    amy_belief.timeline.timeline_label = sue_timeline_label
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
    amy_belief.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    amy_belief.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    amy_belief.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)
    amy_belief.knot = sue_knot
    amy_belief.fund_iota = sue_fund_iota
    amy_belief.respect_bit = sue_respect_bit
    amy_belief.penny = sue_penny
    amy_json = amy_belief.get_json()

    # WHEN
    x_belief = beliefunit_get_from_json(amy_json)

    # THEN
    assert x_belief.belief_label == amy45_str
    assert x_belief.belief_mstr_dir == temp_belief_mstr_dir
    assert x_belief.timeline.timeline_label == sue_timeline_label
    assert x_belief.knot == sue_knot
    assert x_belief.fund_iota == sue_fund_iota
    assert x_belief.respect_bit == sue_respect_bit
    assert x_belief.penny == sue_penny
    assert x_belief.brokerunits == amy_belief.brokerunits
    assert x_belief.belief_mstr_dir == amy_belief.belief_mstr_dir
    assert x_belief != amy_belief
    x_belief._offi_time_max = 0
    assert x_belief == amy_belief


def test_get_from_file_ReturnsBeliefUnitWith_belief_mstr_dir(env_dir_setup_cleanup):
    # ESTABLISH
    amy45_str = "amy45"
    amy45_belief = beliefunit_shop(amy45_str, get_module_temp_dir())
    sue_timeline_label = "sue casa"
    amy45_belief.timeline.timeline_label = sue_timeline_label
    sue_respect_bit = 2
    amy45_belief.respect_bit = sue_respect_bit
    x_belief_mstr_dir = create_path(get_module_temp_dir(), "Fay_bob")
    amy45_json_path = create_belief_json_path(x_belief_mstr_dir, amy45_str)
    save_file(amy45_json_path, None, amy45_belief.get_json())
    assert amy45_belief.belief_mstr_dir != x_belief_mstr_dir

    # WHEN
    generated_a45_belief = get_default_path_beliefunit(x_belief_mstr_dir, amy45_str)

    # THEN
    assert generated_a45_belief.belief_mstr_dir == x_belief_mstr_dir
    assert generated_a45_belief.belief_label == amy45_str
    assert generated_a45_belief.timeline.timeline_label == sue_timeline_label
    assert generated_a45_belief.respect_bit == sue_respect_bit
    x_beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    expected_a45_belief_dir = create_path(x_beliefs_dir, amy45_str)
    assert generated_a45_belief._belief_dir == expected_a45_belief_dir
