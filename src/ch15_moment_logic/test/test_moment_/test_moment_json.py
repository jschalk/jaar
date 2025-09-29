from src.ch01_data_toolbox.file_toolbox import create_path, save_file
from src.ch02_rope_logic.rope import default_knot_if_None
from src.ch03_finance_logic.finance_config import (
    default_fund_iota_if_None,
    default_RespectBit_if_None,
    filter_penny,
)
from src.ch08_timeline_logic.timeline_main import get_default_timeline_config_dict
from src.ch12_hub_toolbox.ch12_path import create_moment_json_path
from src.ch15_moment_logic._ref.ch15_keywords import (
    Ch02Keywords as wx,
    Ch03Keywords as wx,
    Ch04Keywords as wx,
    Ch08Keywords as wx,
    Ch11Keywords as wx,
    Ch12Keywords as wx,
    Ch15Keywords as wx,
    moment_label_str,
)
from src.ch15_moment_logic.moment_main import (
    get_default_path_momentunit,
    get_momentunit_from_dict,
    get_momentunit_from_json,
    momentunit_shop,
)
from src.ch15_moment_logic.test._util.ch15_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)


def test_MomentUnit_to_dict_ReturnsObjWith_paybook():
    # ESTABLISH
    moment_mstr_dir = create_path(get_chapter_temp_dir(), "temp1")
    a45_str = "amy45"
    a45_offi_times = {17, 37}
    amy_moment = momentunit_shop(a45_str, moment_mstr_dir, offi_times=a45_offi_times)
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
    amy_moment.set_offi_time_max(amy_offi_time_max_int)
    amy_moment.add_budunit(bob_str, bob_x0_tran_time, bob_x0_quota)
    amy_moment.add_budunit(sue_str, sue_x4_tran_time, sue_x4_quota)
    amy_moment.add_budunit(sue_str, sue_x7_tran_time, sue_x7_quota)
    amy_moment.add_paypurchase(
        belief_name=bob_str,
        voice_name=sue_str,
        tran_time=pay_tran_time,
        amount=bob_sue_amount,
    )

    # WHEN
    x_dict = amy_moment.to_dict()

    # THEN
    offi_times_str = f"{wx.offi_time}s"
    print(f"{ amy_moment._get_beliefbudhistorys_dict()=}")
    print(f"{ amy_moment.paybook.to_dict()=}")
    assert x_dict.get(moment_label_str()) == a45_str
    assert x_dict.get(wx.moment_mstr_dir) == moment_mstr_dir
    assert x_dict.get(wx.timeline) == get_default_timeline_config_dict()
    assert x_dict.get(offi_times_str) == list(a45_offi_times)
    assert x_dict.get(wx.knot) == default_knot_if_None()
    assert x_dict.get(wx.fund_iota) == default_fund_iota_if_None()
    assert x_dict.get(wx.respect_bit) == default_RespectBit_if_None()
    assert x_dict.get(wx.penny) == filter_penny()
    assert x_dict.get(wx.beliefbudhistorys) == amy_moment._get_beliefbudhistorys_dict()
    assert x_dict.get(wx.paybook) == amy_moment.paybook.to_dict()
    assert set(x_dict.keys()) == {
        moment_label_str(),
        wx.moment_mstr_dir,
        wx.timeline,
        offi_times_str,
        wx.beliefbudhistorys,
        wx.knot,
        wx.fund_iota,
        wx.respect_bit,
        wx.penny,
        wx.paybook,
    }


def test_MomentUnit_to_dict_ReturnsObjWithOut_paybook():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_chapter_temp_dir())

    # WHEN
    x_dict = amy_moment.to_dict(include_paybook=False)

    # THEN
    assert not x_dict.get(wx.paybook)
    assert set(x_dict.keys()) == {
        moment_label_str(),
        wx.moment_mstr_dir,
        wx.timeline,
        f"{wx.offi_time}s",
        wx.beliefbudhistorys,
        wx.knot,
        wx.fund_iota,
        wx.respect_bit,
        wx.penny,
    }


def test_MomentUnit_get_json_ReturnsObj():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_chapter_temp_dir())
    bob_str = "Bob"
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    amy_moment.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    amy_moment.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    amy_moment.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)

    # WHEN
    x_json = amy_moment.get_json()

    # THEN
    print(f"{x_json=}")
    assert x_json
    assert x_json.find(moment_label_str()) > 0


def test_get_momentunit_from_dict_ReturnsMomentUnit_Scenario0_WithParameters():
    # ESTABLISH
    amy45_str = "amy45"
    moment_mstr_dir = create_path(get_chapter_temp_dir(), "temp1")
    a45_offi_times = {17, 37}
    amy_moment = momentunit_shop(amy45_str, moment_mstr_dir, offi_times=a45_offi_times)
    sue_timeline_label = "sue casa"
    amy_moment.timeline.timeline_label = sue_timeline_label
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
    amy_moment.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    amy_moment.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    amy_moment.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)
    amy_moment.knot = sue_knot
    amy_moment.fund_iota = sue_fund_iota
    amy_moment.respect_bit = sue_respect_bit
    amy_moment.penny = sue_penny
    amy_moment.add_paypurchase(
        belief_name=bob_str,
        voice_name=sue_str,
        tran_time=pay_tran_time,
        amount=bob_sue_amount,
    )
    x_dict = amy_moment.to_dict()

    # WHEN
    x_moment = get_momentunit_from_dict(x_dict)

    # THEN
    assert x_moment.moment_label == amy45_str
    assert x_moment.moment_mstr_dir == moment_mstr_dir
    assert x_moment.timeline.timeline_label == sue_timeline_label
    assert x_moment.offi_times == a45_offi_times
    assert x_moment.knot == sue_knot
    assert x_moment.fund_iota == sue_fund_iota
    assert x_moment.respect_bit == sue_respect_bit
    assert x_moment.penny == sue_penny
    assert x_moment.beliefbudhistorys == amy_moment.beliefbudhistorys
    assert x_moment.paybook == amy_moment.paybook
    assert x_moment.moment_mstr_dir == amy_moment.moment_mstr_dir
    assert x_moment != amy_moment
    x_moment._offi_time_max = 0
    assert x_moment == amy_moment


def test_get_momentunit_from_dict_ReturnsMomentUnit_Scenario1_WithOutParameters():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_chapter_temp_dir())
    x_dict = amy_moment.to_dict()
    x_dict["timeline"] = {}
    x_dict.pop("knot")
    x_dict.pop("fund_iota")
    x_dict.pop("respect_bit")
    x_dict.pop("penny")

    # WHEN
    generated_moment = get_momentunit_from_dict(x_dict)

    # THEN
    assert generated_moment.moment_label == amy45_str
    print(f"{generated_moment.timeline=}")
    print(f"   {amy_moment.timeline=}")
    assert generated_moment.timeline == amy_moment.timeline
    assert generated_moment.offi_times == set()
    assert generated_moment.knot == default_knot_if_None()
    assert generated_moment.fund_iota == default_fund_iota_if_None()
    assert generated_moment.respect_bit == default_RespectBit_if_None()
    assert generated_moment.penny == 1
    assert generated_moment.beliefbudhistorys == amy_moment.beliefbudhistorys
    assert generated_moment.paybook == amy_moment.paybook
    assert generated_moment.moment_mstr_dir == amy_moment.moment_mstr_dir
    assert generated_moment == amy_moment


def test_get_momentunit_from_json_ReturnsMomentUnit():
    # ESTABLISH
    amy45_str = "amy45"
    temp_moment_mstr_dir = create_path(get_chapter_temp_dir(), "temp")
    amy_moment = momentunit_shop(amy45_str, temp_moment_mstr_dir)
    sue_timeline_label = "sue casa"
    amy_moment.timeline.timeline_label = sue_timeline_label
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
    amy_moment.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    amy_moment.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    amy_moment.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)
    amy_moment.knot = sue_knot
    amy_moment.fund_iota = sue_fund_iota
    amy_moment.respect_bit = sue_respect_bit
    amy_moment.penny = sue_penny
    amy_json = amy_moment.get_json()

    # WHEN
    x_moment = get_momentunit_from_json(amy_json)

    # THEN
    assert x_moment.moment_label == amy45_str
    assert x_moment.moment_mstr_dir == temp_moment_mstr_dir
    assert x_moment.timeline.timeline_label == sue_timeline_label
    assert x_moment.knot == sue_knot
    assert x_moment.fund_iota == sue_fund_iota
    assert x_moment.respect_bit == sue_respect_bit
    assert x_moment.penny == sue_penny
    assert x_moment.beliefbudhistorys == amy_moment.beliefbudhistorys
    assert x_moment.moment_mstr_dir == amy_moment.moment_mstr_dir
    assert x_moment != amy_moment
    x_moment._offi_time_max = 0
    assert x_moment == amy_moment


def test_get_from_file_ReturnsMomentUnitWith_moment_mstr_dir(env_dir_setup_cleanup):
    # ESTABLISH
    amy45_str = "amy45"
    amy45_moment = momentunit_shop(amy45_str, get_chapter_temp_dir())
    sue_timeline_label = "sue casa"
    amy45_moment.timeline.timeline_label = sue_timeline_label
    sue_respect_bit = 2
    amy45_moment.respect_bit = sue_respect_bit
    x_moment_mstr_dir = create_path(get_chapter_temp_dir(), "Fay_bob")
    amy45_json_path = create_moment_json_path(x_moment_mstr_dir, amy45_str)
    save_file(amy45_json_path, None, amy45_moment.get_json())
    assert amy45_moment.moment_mstr_dir != x_moment_mstr_dir

    # WHEN
    generated_a45_moment = get_default_path_momentunit(x_moment_mstr_dir, amy45_str)

    # THEN
    assert generated_a45_moment.moment_mstr_dir == x_moment_mstr_dir
    assert generated_a45_moment.moment_label == amy45_str
    assert generated_a45_moment.timeline.timeline_label == sue_timeline_label
    assert generated_a45_moment.respect_bit == sue_respect_bit
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    expected_a45_moment_dir = create_path(x_moments_dir, amy45_str)
    assert generated_a45_moment._moment_dir == expected_a45_moment_dir
