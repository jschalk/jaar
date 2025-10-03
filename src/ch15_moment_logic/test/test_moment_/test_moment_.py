from os.path import exists as os_path_exists, isdir as os_path_isdir
from src.ch01_data_toolbox.file_toolbox import create_path, get_json_filename, set_dir
from src.ch02_rope_logic.rope import default_knot_if_None
from src.ch03_finance_logic.allot import default_grain_num_if_None
from src.ch06_plan_logic.healer import healerunit_shop
from src.ch06_plan_logic.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch08_timeline_logic.timeline_main import timelineunit_shop
from src.ch11_bud_logic.bud import tranbook_shop
from src.ch12_hub_toolbox.ch12_path import (
    create_belief_dir_path,
    create_keep_dutys_path,
    create_path,
)
from src.ch12_hub_toolbox.hub_tool import (
    gut_file_exists,
    job_file_exists,
    open_gut_file,
    open_job_file,
    save_gut_file,
    save_job_file,
)
from src.ch15_moment_logic._ref.ch15_keywords import Ch15Keywords as wx
from src.ch15_moment_logic.moment_main import (
    MomentUnit,
    get_default_job_listen_count,
    momentunit_shop,
)
from src.ch15_moment_logic.test._util.ch15_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)


def test_get_default_job_listen_count_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_default_job_listen_count() == 3


def test_MomentUnit_Exists():
    # ESTABLISH / WHEN
    amy_moment = MomentUnit()
    # THEN
    assert not amy_moment.moment_label
    assert not amy_moment.timeline
    assert not amy_moment.beliefbudhistorys
    assert not amy_moment.paybook
    assert not amy_moment.offi_times
    assert not amy_moment.knot
    assert not amy_moment.fund_grain
    assert not amy_moment.respect_grain
    assert not amy_moment.money_grain
    assert not amy_moment.job_listen_rotations
    assert not amy_moment.moment_mstr_dir
    # Calculated fields
    assert not amy_moment._offi_time_max
    assert not amy_moment._beliefs_dir
    assert not amy_moment._packs_dir
    assert not amy_moment.all_tranbook
    assert set(amy_moment.__dict__) == {
        wx.moment_label,
        wx.timeline,
        wx.beliefbudhistorys,
        wx.paybook,
        "offi_times",
        wx.knot,
        wx.fund_grain,
        wx.respect_grain,
        wx.money_grain,
        wx.job_listen_rotations,
        "_moment_dir",
        "moment_mstr_dir",
        "all_tranbook",
        "_offi_time_max",
        "_beliefs_dir",
        "_packs_dir",
    }


def test_momentunit_shop_ReturnsMomentUnit():
    # ESTABLISH
    a23_str = "amy23"

    # WHEN
    a23_moment = momentunit_shop(a23_str, get_chapter_temp_dir())

    # THEN
    assert a23_moment.moment_label == a23_str
    assert a23_moment.timeline == timelineunit_shop()
    assert a23_moment.beliefbudhistorys == {}
    assert a23_moment.paybook == tranbook_shop(a23_str)
    assert a23_moment.offi_times == set()
    assert a23_moment.knot == default_knot_if_None()
    assert a23_moment.fund_grain == default_grain_num_if_None()
    assert a23_moment.respect_grain == default_grain_num_if_None()
    assert a23_moment.money_grain == default_grain_num_if_None()
    assert a23_moment.moment_mstr_dir == get_chapter_temp_dir()
    assert a23_moment.job_listen_rotations == get_default_job_listen_count()
    # Calculated fields
    assert a23_moment._beliefs_dir != None
    assert a23_moment._packs_dir != None
    assert a23_moment.all_tranbook == tranbook_shop(a23_str)


def test_momentunit_shop_ReturnsMomentUnitWith_moments_dir(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"

    # WHEN
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir=get_chapter_temp_dir())

    # THEN
    assert a23_moment.moment_label == a23_str
    assert a23_moment.moment_mstr_dir == get_chapter_temp_dir()
    assert a23_moment._beliefs_dir is not None
    assert a23_moment._packs_dir is not None


def test_momentunit_shop_ReturnsMomentUnitWith_knot(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"
    slash_str = "/"
    x_fund_grain = 7.0
    x_respect_grain = 9
    x_money_grain = 3
    a45_offi_times = {12, 15}
    x_job_listen_rotations = 888

    # WHEN
    a23_moment = momentunit_shop(
        moment_label=a23_str,
        moment_mstr_dir=get_chapter_temp_dir(),
        offi_times=a45_offi_times,
        knot=slash_str,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
        money_grain=x_money_grain,
        job_listen_rotations=x_job_listen_rotations,
    )

    # THEN
    assert a23_moment.knot == slash_str
    assert a23_moment.fund_grain == x_fund_grain
    assert a23_moment.respect_grain == x_respect_grain
    assert a23_moment.money_grain == x_money_grain
    assert a23_moment.offi_times == a45_offi_times
    assert a23_moment.job_listen_rotations == x_job_listen_rotations


def test_MomentUnit_set_moment_dirs_SetsDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"
    amy_moment = MomentUnit(a23_str, get_chapter_temp_dir())
    x_moments_dir = create_path(get_chapter_temp_dir(), "moments")
    x_moment_dir = create_path(x_moments_dir, a23_str)
    x_beliefs_dir = create_path(x_moment_dir, "beliefs")
    x_packs_dir = create_path(x_moment_dir, "packs")

    assert not amy_moment._moment_dir
    assert not amy_moment._beliefs_dir
    assert not amy_moment._packs_dir
    assert os_path_exists(x_moment_dir) is False
    assert os_path_isdir(x_moment_dir) is False
    assert os_path_exists(x_beliefs_dir) is False
    assert os_path_exists(x_packs_dir) is False

    # WHEN
    amy_moment._set_moment_dirs()

    # THEN
    assert amy_moment._moment_dir == x_moment_dir
    assert amy_moment._beliefs_dir == x_beliefs_dir
    assert amy_moment._packs_dir == x_packs_dir
    assert os_path_exists(x_moment_dir)
    assert os_path_isdir(x_moment_dir)
    assert os_path_exists(x_beliefs_dir)
    assert os_path_exists(x_packs_dir)


def test_momentunit_shop_SetsmomentsDirs(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"

    # WHEN
    a23_moment = momentunit_shop(a23_str, get_chapter_temp_dir())

    # THEN
    assert a23_moment.moment_label == a23_str
    x_moments_dir = create_path(get_chapter_temp_dir(), "moments")
    assert a23_moment._moment_dir == create_path(x_moments_dir, a23_str)
    assert a23_moment._beliefs_dir == create_path(a23_moment._moment_dir, "beliefs")


def test_MomentUnit_create_empty_belief_from_moment_ReturnsObj_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = get_chapter_temp_dir()
    a23_str = "amy23"
    slash_str = "/"
    x_fund_grain = 4
    x_respect_grain = 5
    x_money_grain = 6
    a23_moment = momentunit_shop(
        a23_str,
        moment_mstr_dir,
        knot=slash_str,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
        money_grain=x_money_grain,
    )
    sue_str = "Sue"

    # WHEN
    generated_belief = a23_moment.create_empty_belief_from_moment(sue_str)

    # THEN
    assert generated_belief.knot == slash_str
    assert generated_belief.fund_grain == x_fund_grain
    assert generated_belief.respect_grain == x_respect_grain
    assert generated_belief.money_grain == x_money_grain


def test_MomentUnit_create_gut_file_if_none_SetsDirAndFiles_Scenario1_belief_dir_ExistsNoFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = get_chapter_temp_dir()
    a23_str = "amy23"
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir)
    sue_str = "Sue"
    sue_belief_dir = create_belief_dir_path(moment_mstr_dir, a23_str, sue_str)
    assert not os_path_exists(sue_belief_dir)
    assert not gut_file_exists(moment_mstr_dir, a23_str, sue_str)

    # WHEN
    a23_moment.create_gut_file_if_none(sue_str)

    # THEN
    print(f"{moment_mstr_dir=}")
    assert gut_file_exists(moment_mstr_dir, a23_str, sue_str)
    expected_sue_gut = beliefunit_shop(sue_str, a23_str)
    assert open_gut_file(moment_mstr_dir, a23_str, sue_str) == expected_sue_gut


def test_MomentUnit_create_gut_file_if_none_SetsDirAndFiles_Scenario2_belief_dir_ExistsNoFile_Create_gut_AndConfirmMomentAttributesPassed(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = get_chapter_temp_dir()
    a23_str = "amy23"
    slash_str = "/"
    x_fund_grain = 4
    x_respect_grain = 5
    x_money_grain = 6
    a23_moment = momentunit_shop(
        a23_str,
        moment_mstr_dir,
        knot=slash_str,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
        money_grain=x_money_grain,
    )
    sue_str = "Sue"
    sue_belief_dir = create_belief_dir_path(moment_mstr_dir, a23_str, sue_str)
    set_dir(sue_belief_dir)
    assert os_path_exists(sue_belief_dir)
    assert not gut_file_exists(moment_mstr_dir, a23_str, sue_str)

    # WHEN
    a23_moment.create_gut_file_if_none(sue_str)

    # THEN
    print(f"{moment_mstr_dir=}")
    assert gut_file_exists(moment_mstr_dir, a23_str, sue_str)
    generated_gut = open_gut_file(moment_mstr_dir, a23_str, sue_str)
    assert generated_gut.knot == slash_str
    assert generated_gut.fund_grain == x_fund_grain
    assert generated_gut.respect_grain == x_respect_grain
    assert generated_gut.money_grain == x_money_grain


def test_MomentUnit_create_gut_file_if_none_SetsDirAndFiles_Scenario3_FileExistsIsNotReplaced(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = get_chapter_temp_dir()
    a23_str = "amy23"
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir)
    sue_str = "Sue"
    bob_str = "Bob"
    sue_gut = beliefunit_shop(sue_str, a23_str)
    sue_gut.add_voiceunit(bob_str)
    save_gut_file(moment_mstr_dir, sue_gut)
    sue_belief_dir = create_belief_dir_path(moment_mstr_dir, a23_str, sue_str)
    assert os_path_exists(sue_belief_dir)
    assert gut_file_exists(moment_mstr_dir, a23_str, sue_str)

    # WHEN
    a23_moment.create_gut_file_if_none(sue_str)

    # THEN
    print(f"{moment_mstr_dir=}")
    assert gut_file_exists(moment_mstr_dir, a23_str, sue_str)
    assert open_gut_file(moment_mstr_dir, a23_str, sue_str) == sue_gut


def test_MomentUnit_create_init_job_from_guts_Scenario0_CreatesFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = get_chapter_temp_dir()
    a23_str = "amy23"
    slash_str = "/"
    x_fund_grain = 4
    x_respect_grain = 5
    a23_moment = momentunit_shop(
        a23_str,
        moment_mstr_dir,
        knot=slash_str,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
    )
    sue_str = "Sue"
    assert not job_file_exists(moment_mstr_dir, a23_str, sue_str)

    # WHEN
    a23_moment.create_init_job_from_guts(sue_str)

    # THEN
    print(f"{moment_mstr_dir=}")
    assert job_file_exists(moment_mstr_dir, a23_str, sue_str)


def test_MomentUnit_create_init_job_from_guts_Scenario1_ReplacesFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = get_chapter_temp_dir()
    a23_str = "amy23"
    slash_str = "/"
    x_fund_grain = 4
    x_respect_grain = 5
    a23_moment = momentunit_shop(
        a23_str,
        moment_mstr_dir,
        knot=slash_str,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
    )
    bob_str = "Bob"
    sue_str = "Sue"
    x0_sue_job = beliefunit_shop(sue_str, a23_str)
    x0_sue_job.add_voiceunit(bob_str)
    save_job_file(moment_mstr_dir, x0_sue_job)
    assert open_job_file(moment_mstr_dir, a23_str, sue_str).get_voice(bob_str)

    # WHEN
    a23_moment.create_init_job_from_guts(sue_str)

    # THEN
    assert not open_job_file(moment_mstr_dir, a23_str, sue_str).get_voice(bob_str)


def test_MomentUnit_create_init_job_from_guts_Scenario2_job_Has_gut_Voices(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = get_chapter_temp_dir()
    a23_str = "amy23"
    slash_str = "/"
    x_fund_grain = 4
    x_respect_grain = 5
    a23_moment = momentunit_shop(
        a23_str,
        moment_mstr_dir,
        knot=slash_str,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
    )
    bob_str = "Bob"
    sue_str = "Sue"
    a23_moment.create_init_job_from_guts(sue_str)
    sue_gut = beliefunit_shop(sue_str, a23_str)
    sue_gut.add_voiceunit(bob_str)
    save_gut_file(moment_mstr_dir, sue_gut)
    assert not open_job_file(moment_mstr_dir, a23_str, sue_str).get_voice(bob_str)

    # WHEN
    a23_moment.create_init_job_from_guts(sue_str)

    # THEN
    assert open_job_file(moment_mstr_dir, a23_str, sue_str).get_voice(bob_str)


def test_MomentUnit_create_init_job_from_guts_Scenario3_gut_FilesAreListenedTo(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = get_chapter_temp_dir()
    a23_str = "amy23"
    slash_str = "/"
    x_fund_grain = 4
    x_respect_grain = 5
    a23_moment = momentunit_shop(
        a23_str,
        moment_mstr_dir,
        knot=slash_str,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
    )
    sue_str = "Sue"
    a23_moment.create_init_job_from_guts(sue_str)

    # create Sue gut
    bob_str = "Bob"
    sue_gut = beliefunit_shop(sue_str, a23_str, knot=slash_str)
    sue_gut.add_voiceunit(bob_str)
    save_gut_file(moment_mstr_dir, sue_gut)
    # create Bob gut with agenda plan for Sue
    bob_gut = beliefunit_shop(bob_str, a23_str, knot=slash_str)
    bob_gut.add_voiceunit(sue_str)
    casa_rope = bob_gut.make_l1_rope("casa")
    clean_rope = bob_gut.make_rope(casa_rope, "clean")
    bob_gut.add_plan(clean_rope, pledge=True)
    bob_gut.get_plan_obj(clean_rope).laborunit.add_party(sue_str)
    save_gut_file(moment_mstr_dir, bob_gut)
    assert not open_job_file(moment_mstr_dir, a23_str, sue_str).get_agenda_dict()

    # WHEN
    a23_moment.create_init_job_from_guts(sue_str)

    # THEN
    assert open_job_file(moment_mstr_dir, a23_str, sue_str).get_agenda_dict()
    sue_agenda = open_job_file(moment_mstr_dir, a23_str, sue_str).get_agenda_dict()
    assert len(sue_agenda) == 1
    assert sue_agenda.get(clean_rope).get_plan_rope() == clean_rope


def test_MomentUnit__set_all_healer_dutys_Setsdutys(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "amy23"
    x_moment_mstr_dir = get_chapter_temp_dir()
    a23_moment = momentunit_shop(a23_str, x_moment_mstr_dir)
    sue_str = "Sue"
    yao_str = "Yao"
    a23_moment.create_init_job_from_guts(sue_str)
    a23_moment.create_init_job_from_guts(yao_str)
    sue_gut_belief = open_gut_file(x_moment_mstr_dir, a23_str, sue_str)
    yao_gut_belief = open_gut_file(x_moment_mstr_dir, a23_str, yao_str)

    sue_gut_belief.add_voiceunit(sue_str)
    sue_gut_belief.add_voiceunit(yao_str)
    yao_gut_belief.add_voiceunit(sue_str)
    yao_gut_belief.add_voiceunit(yao_str)
    texas_str = "Texas"
    texas_rope = sue_gut_belief.make_l1_rope(texas_str)
    sue_gut_belief.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    yao_gut_belief.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_rope = sue_gut_belief.make_rope(texas_rope, dallas_str)
    dallas_healerunit = healerunit_shop({sue_str, yao_str})
    dallas_plan = planunit_shop(dallas_str, healerunit=dallas_healerunit)
    elpaso_str = "el paso"
    elpaso_rope = sue_gut_belief.make_rope(texas_rope, elpaso_str)
    elpaso_healerunit = healerunit_shop({sue_str})
    elpaso_plan = planunit_shop(elpaso_str, healerunit=elpaso_healerunit)

    sue_gut_belief.set_plan(dallas_plan, texas_rope)
    sue_gut_belief.set_plan(elpaso_plan, texas_rope)
    yao_gut_belief.set_plan(dallas_plan, texas_rope)
    yao_gut_belief.set_plan(elpaso_plan, texas_rope)

    save_gut_file(x_moment_mstr_dir, sue_gut_belief)
    save_gut_file(x_moment_mstr_dir, yao_gut_belief)
    sue_filename = get_json_filename(sue_str)
    yao_filename = get_json_filename(yao_str)

    mstr_dir = x_moment_mstr_dir
    sue_dutys_path = create_keep_dutys_path(
        mstr_dir, sue_str, a23_str, dallas_rope, None
    )
    yao_dutys_path = create_keep_dutys_path(
        mstr_dir, yao_str, a23_str, dallas_rope, None
    )
    sue_dallas_sue_duty_file_path = create_path(sue_dutys_path, sue_filename)
    sue_dallas_yao_duty_file_path = create_path(sue_dutys_path, yao_filename)
    yao_dallas_sue_duty_file_path = create_path(yao_dutys_path, sue_filename)
    yao_dallas_yao_duty_file_path = create_path(yao_dutys_path, yao_filename)
    assert os_path_exists(sue_dallas_sue_duty_file_path) is False
    assert os_path_exists(sue_dallas_yao_duty_file_path) is False
    assert os_path_exists(yao_dallas_sue_duty_file_path) is False
    assert os_path_exists(yao_dallas_yao_duty_file_path) is False

    # WHEN
    a23_moment._set_all_healer_dutys(sue_str)

    # THEN
    assert os_path_exists(sue_dallas_sue_duty_file_path)
    assert os_path_exists(sue_dallas_yao_duty_file_path) is False
    assert os_path_exists(yao_dallas_sue_duty_file_path)
    assert os_path_exists(yao_dallas_yao_duty_file_path) is False

    # WHEN
    a23_moment._set_all_healer_dutys(yao_str)

    # THEN
    assert os_path_exists(sue_dallas_sue_duty_file_path)
    assert os_path_exists(sue_dallas_yao_duty_file_path)
    assert os_path_exists(yao_dallas_sue_duty_file_path)
    assert os_path_exists(yao_dallas_yao_duty_file_path)


# def test_MomentUnit_set_offi_time_Scenario0_SetsAttr():
#     # ESTABLISH
#     moment_mstr_dir = get_chapter_temp_dir()
#     time56 = 56
#     a23_moment = momentunit_shop("amy23", moment_mstr_dir, _offi_time_max=time56)
#     assert a23_moment.offi_time == 0
#     assert a23_moment._offi_time_max == time56

#     # WHEN
#     time23 = 23
#     a23_moment.set_offi_time(time23)

#     # THEN
#     assert a23_moment.offi_time == time23
#     assert a23_moment._offi_time_max == time56


# def test_MomentUnit_set_offi_time_Scenario1_SetsAttr():
#     # ESTABLISH
#     a23_moment = momentunit_shop("amy23", get_chapter_temp_dir())
#     assert a23_moment.offi_time == 0
#     assert a23_moment._offi_time_max == 0

#     # WHEN
#     time23 = 23
#     a23_moment.set_offi_time(time23)

#     # THEN
#     assert a23_moment.offi_time == time23
#     assert a23_moment._offi_time_max == time23


def test_MomentUnit_set_offi_time_max_Scenario0_SetsAttr():
    # ESTABLISH
    moment_mstr_dir = get_chapter_temp_dir()
    time7 = 7
    a23_moment = momentunit_shop("amy23", moment_mstr_dir)
    a23_moment._offi_time_max = time7
    # assert a23_moment.offi_time == 0
    assert a23_moment._offi_time_max == time7

    # WHEN
    time23 = 23
    a23_moment.set_offi_time_max(time23)

    # THEN
    # assert a23_moment.offi_time == 0
    assert a23_moment._offi_time_max == time23


# def test_MomentUnit_set_offi_time_max_Scenario1_SetsAttr():
#     # ESTABLISH
#     moment_mstr_dir = get_chapter_temp_dir()
#     time21 = 21
#     time77 = 77
#     a23_moment = momentunit_shop(
#         "amy23", moment_mstr_dir, offi_time=time21, _offi_time_max=time77
#     )
#     assert a23_moment.offi_time == time21
#     assert a23_moment._offi_time_max == time77

#     # WHEN / THEN
#     time11 = 11
#     with pytest_raises(Exception) as excinfo:
#         a23_moment.set_offi_time_max(time11)
#     exception_str = f"Cannot set _offi_time_max={time11} because it is less than offi_time={time21}"
#     assert str(excinfo.value) == exception_str


# def test_MomentUnit_set_offi_time_Scenario0_SetsAttr():
#     # ESTABLISH
#     a23_moment = momentunit_shop("amy23", get_chapter_temp_dir())
#     assert a23_moment.offi_time == 0
#     assert a23_moment._offi_time_max == 0

#     # WHEN
#     time23 = 23
#     time55 = 55
#     a23_moment.set_offi_time(time23, time55)

#     # THEN
#     assert a23_moment.offi_time == time23
#     assert a23_moment._offi_time_max == time55
