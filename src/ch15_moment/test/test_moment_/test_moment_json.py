from src.ch01_py.file_toolbox import create_path, save_json
from src.ch02_rope.rope import default_knot_if_None
from src.ch03_allot.allot import default_grain_num_if_None
from src.ch08_epoch.epoch_main import get_default_epoch_config_dict
from src.ch10_lesson._ref.ch10_path import create_moment_json_path
from src.ch15_moment.moment_main import (
    get_default_path_momentunit,
    get_momentunit_from_dict,
    momentunit_shop,
)
from src.ch15_moment.test._util.ch15_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)
from src.ref.keywords import Ch15Keywords as wx


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
    print(f"{ amy_moment._get_beliefbudhistorys_dict()=}")
    print(f"{ amy_moment.paybook.to_dict()=}")
    assert x_dict.get(wx.moment_label) == a45_str
    assert x_dict.get(wx.moment_mstr_dir) == moment_mstr_dir
    assert x_dict.get(wx.epoch) == get_default_epoch_config_dict()
    assert x_dict.get(wx.offi_times) == list(a45_offi_times)
    assert x_dict.get(wx.knot) == default_knot_if_None()
    assert x_dict.get(wx.fund_grain) == default_grain_num_if_None()
    assert x_dict.get(wx.respect_grain) == default_grain_num_if_None()
    assert x_dict.get(wx.money_grain) == default_grain_num_if_None()
    assert x_dict.get(wx.beliefbudhistorys) == amy_moment._get_beliefbudhistorys_dict()
    assert x_dict.get(wx.paybook) == amy_moment.paybook.to_dict()
    assert set(x_dict.keys()) == {
        wx.moment_label,
        wx.moment_mstr_dir,
        wx.epoch,
        wx.offi_times,
        wx.beliefbudhistorys,
        wx.knot,
        wx.fund_grain,
        wx.respect_grain,
        wx.money_grain,
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
        wx.moment_label,
        wx.moment_mstr_dir,
        wx.epoch,
        f"{wx.offi_time}s",
        wx.beliefbudhistorys,
        wx.knot,
        wx.fund_grain,
        wx.respect_grain,
        wx.money_grain,
    }


def test_get_momentunit_from_dict_ReturnsObj_Scenario0_WithParameters():
    # ESTABLISH
    amy45_str = "amy45"
    moment_mstr_dir = create_path(get_chapter_temp_dir(), "temp1")
    a45_offi_times = {17, 37}
    amy_moment = momentunit_shop(amy45_str, moment_mstr_dir, offi_times=a45_offi_times)
    sue_epoch_label = "sue casa"
    amy_moment.epoch.epoch_label = sue_epoch_label
    sue_knot = "/"
    sue_fund_grain = 0.3
    sue_respect_grain = 2
    sue_money_grain = 3
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
    amy_moment.fund_grain = sue_fund_grain
    amy_moment.respect_grain = sue_respect_grain
    amy_moment.money_grain = sue_money_grain
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
    assert x_moment.epoch.epoch_label == sue_epoch_label
    assert x_moment.offi_times == a45_offi_times
    assert x_moment.knot == sue_knot
    assert x_moment.fund_grain == sue_fund_grain
    assert x_moment.respect_grain == sue_respect_grain
    assert x_moment.money_grain == sue_money_grain
    assert x_moment.beliefbudhistorys == amy_moment.beliefbudhistorys
    assert x_moment.paybook == amy_moment.paybook
    assert x_moment.moment_mstr_dir == amy_moment.moment_mstr_dir
    assert x_moment != amy_moment
    x_moment.offi_time_max = 0
    assert x_moment == amy_moment


def test_get_momentunit_from_dict_ReturnsObj_Scenario1_WithOutParameters():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_chapter_temp_dir())
    x_dict = amy_moment.to_dict()
    x_dict[wx.epoch] = {}
    x_dict.pop(wx.knot)
    x_dict.pop(wx.fund_grain)
    x_dict.pop(wx.respect_grain)
    x_dict.pop(wx.money_grain)

    # WHEN
    generated_moment = get_momentunit_from_dict(x_dict)

    # THEN
    assert generated_moment.moment_label == amy45_str
    print(f"{generated_moment.epoch=}")
    print(f"   {amy_moment.epoch=}")
    assert generated_moment.epoch == amy_moment.epoch
    assert generated_moment.offi_times == set()
    assert generated_moment.knot == default_knot_if_None()
    assert generated_moment.fund_grain == default_grain_num_if_None()
    assert generated_moment.respect_grain == default_grain_num_if_None()
    assert generated_moment.money_grain == 1
    assert generated_moment.beliefbudhistorys == amy_moment.beliefbudhistorys
    assert generated_moment.paybook == amy_moment.paybook
    assert generated_moment.moment_mstr_dir == amy_moment.moment_mstr_dir
    assert generated_moment == amy_moment


def test_get_momentunit_from_dict_ReturnsObj_Scenario2():
    # ESTABLISH
    amy45_str = "amy45"
    temp_moment_mstr_dir = create_path(get_chapter_temp_dir(), "temp")
    amy_moment = momentunit_shop(amy45_str, temp_moment_mstr_dir)
    sue_epoch_label = "sue casa"
    amy_moment.epoch.epoch_label = sue_epoch_label
    sue_offi_time_max = 23
    sue_knot = "/"
    sue_fund_grain = 0.3
    sue_respect_grain = 2
    sue_money_grain = 3
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
    amy_moment.fund_grain = sue_fund_grain
    amy_moment.respect_grain = sue_respect_grain
    amy_moment.money_grain = sue_money_grain
    amy_dict = amy_moment.to_dict()

    # WHEN
    x_moment = get_momentunit_from_dict(amy_dict)

    # THEN
    assert x_moment.moment_label == amy45_str
    assert x_moment.moment_mstr_dir == temp_moment_mstr_dir
    assert x_moment.epoch.epoch_label == sue_epoch_label
    assert x_moment.knot == sue_knot
    assert x_moment.fund_grain == sue_fund_grain
    assert x_moment.respect_grain == sue_respect_grain
    assert x_moment.money_grain == sue_money_grain
    assert x_moment.beliefbudhistorys == amy_moment.beliefbudhistorys
    assert x_moment.moment_mstr_dir == amy_moment.moment_mstr_dir
    assert x_moment != amy_moment
    x_moment.offi_time_max = 0
    assert x_moment == amy_moment


def test_get_from_file_ReturnsMomentUnitWith_moment_mstr_dir(env_dir_setup_cleanup):
    # ESTABLISH
    amy45_str = "amy45"
    amy45_moment = momentunit_shop(amy45_str, get_chapter_temp_dir())
    sue_epoch_label = "sue casa"
    amy45_moment.epoch.epoch_label = sue_epoch_label
    sue_respect_grain = 2
    amy45_moment.respect_grain = sue_respect_grain
    x_moment_mstr_dir = create_path(get_chapter_temp_dir(), "Fay_bob")
    amy45_json_path = create_moment_json_path(x_moment_mstr_dir, amy45_str)
    save_json(amy45_json_path, None, amy45_moment.to_dict())
    assert amy45_moment.moment_mstr_dir != x_moment_mstr_dir

    # WHEN
    generated_a45_moment = get_default_path_momentunit(x_moment_mstr_dir, amy45_str)

    # THEN
    assert generated_a45_moment.moment_mstr_dir == x_moment_mstr_dir
    assert generated_a45_moment.moment_label == amy45_str
    assert generated_a45_moment.epoch.epoch_label == sue_epoch_label
    assert generated_a45_moment.respect_grain == sue_respect_grain
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    expected_a45_moment_dir = create_path(x_moments_dir, amy45_str)
    assert generated_a45_moment._moment_dir == expected_a45_moment_dir
