from os.path import exists as os_path_exists, isdir as os_path_isdir
from src.a00_data_toolbox.file_toolbox import create_path, get_json_filename, set_dir
from src.a01_term_logic.rope import default_knot_if_None
from src.a02_finance_logic.finance_config import (
    default_fund_iota_if_None,
    default_RespectBit_if_None,
    filter_penny,
)
from src.a05_plan_logic.healer import healerlink_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a07_timeline_logic.timeline_main import timelineunit_shop
from src.a11_bud_logic.bud import tranbook_shop
from src.a12_hub_toolbox.a12_path import (
    create_believer_dir_path,
    create_keep_dutys_path,
    create_path,
)
from src.a12_hub_toolbox.hub_tool import (
    gut_file_exists,
    job_file_exists,
    open_gut_file,
    open_job_file,
    save_gut_file,
    save_job_file,
)
from src.a12_hub_toolbox.hubunit import hubunit_shop
from src.a15_belief_logic.belief_main import (
    BeliefUnit,
    beliefunit_shop,
    get_default_job_listen_count,
)
from src.a15_belief_logic.test._util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a15_belief_logic.test._util.a15_str import (
    belief_label_str,
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


def test_BeliefUnit_Exists():
    # ESTABLISH / WHEN
    amy_belief = BeliefUnit()
    # THEN
    assert not amy_belief.belief_label
    assert not amy_belief.timeline
    assert not amy_belief.brokerunits
    assert not amy_belief.paybook
    assert not amy_belief.offi_times
    assert not amy_belief.knot
    assert not amy_belief.fund_iota
    assert not amy_belief.respect_bit
    assert not amy_belief.penny
    assert not amy_belief.job_listen_rotations
    assert not amy_belief.belief_mstr_dir
    # Calculated fields
    assert not amy_belief._offi_time_max
    assert not amy_belief._believers_dir
    assert not amy_belief._packs_dir
    assert not amy_belief._all_tranbook
    assert set(amy_belief.__dict__) == {
        belief_label_str(),
        timeline_str(),
        brokerunits_str(),
        paybook_str(),
        "offi_times",
        knot_str(),
        fund_iota_str(),
        respect_bit_str(),
        penny_str(),
        job_listen_rotations_str(),
        "_belief_dir",
        "belief_mstr_dir",
        "_all_tranbook",
        "_offi_time_max",
        "_believers_dir",
        "_packs_dir",
    }


def test_beliefunit_shop_ReturnsBeliefUnit():
    # ESTABLISH
    a23_str = "amy23"

    # WHEN
    a23_belief = beliefunit_shop(a23_str, get_module_temp_dir())

    # THEN
    assert a23_belief.belief_label == a23_str
    assert a23_belief.timeline == timelineunit_shop()
    assert a23_belief.brokerunits == {}
    assert a23_belief.paybook == tranbook_shop(a23_str)
    assert a23_belief.offi_times == set()
    assert a23_belief.knot == default_knot_if_None()
    assert a23_belief.fund_iota == default_fund_iota_if_None()
    assert a23_belief.respect_bit == default_RespectBit_if_None()
    assert a23_belief.penny == filter_penny()
    assert a23_belief.belief_mstr_dir == get_module_temp_dir()
    assert a23_belief.job_listen_rotations == get_default_job_listen_count()
    # Calculated fields
    assert a23_belief._believers_dir != None
    assert a23_belief._packs_dir != None
    assert a23_belief._all_tranbook == tranbook_shop(a23_str)


def test_beliefunit_shop_ReturnsBeliefUnitWith_beliefs_dir(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"

    # WHEN
    a23_belief = beliefunit_shop(a23_str, belief_mstr_dir=get_module_temp_dir())

    # THEN
    assert a23_belief.belief_label == a23_str
    assert a23_belief.belief_mstr_dir == get_module_temp_dir()
    assert a23_belief._believers_dir is not None
    assert a23_belief._packs_dir is not None


def test_beliefunit_shop_ReturnsBeliefUnitWith_knot(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"
    slash_str = "/"
    x_fund_iota = 7.0
    x_respect_bit = 9
    x_penny = 3
    a45_offi_times = {12, 15}
    x_job_listen_rotations = 888

    # WHEN
    a23_belief = beliefunit_shop(
        belief_label=a23_str,
        belief_mstr_dir=get_module_temp_dir(),
        offi_times=a45_offi_times,
        knot=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        penny=x_penny,
        job_listen_rotations=x_job_listen_rotations,
    )

    # THEN
    assert a23_belief.knot == slash_str
    assert a23_belief.fund_iota == x_fund_iota
    assert a23_belief.respect_bit == x_respect_bit
    assert a23_belief.penny == x_penny
    assert a23_belief.offi_times == a45_offi_times
    assert a23_belief.job_listen_rotations == x_job_listen_rotations


def test_BeliefUnit_set_belief_dirs_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"
    amy_belief = BeliefUnit(a23_str, get_module_temp_dir())
    x_beliefs_dir = create_path(get_module_temp_dir(), "beliefs")
    x_belief_dir = create_path(x_beliefs_dir, a23_str)
    x_believers_dir = create_path(x_belief_dir, "believers")
    x_packs_dir = create_path(x_belief_dir, "packs")

    assert not amy_belief._belief_dir
    assert not amy_belief._believers_dir
    assert not amy_belief._packs_dir
    assert os_path_exists(x_belief_dir) is False
    assert os_path_isdir(x_belief_dir) is False
    assert os_path_exists(x_believers_dir) is False
    assert os_path_exists(x_packs_dir) is False

    # WHEN
    amy_belief._set_belief_dirs()

    # THEN
    assert amy_belief._belief_dir == x_belief_dir
    assert amy_belief._believers_dir == x_believers_dir
    assert amy_belief._packs_dir == x_packs_dir
    assert os_path_exists(x_belief_dir)
    assert os_path_isdir(x_belief_dir)
    assert os_path_exists(x_believers_dir)
    assert os_path_exists(x_packs_dir)


def test_beliefunit_shop_SetsbeliefsDirs(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"

    # WHEN
    a23_belief = beliefunit_shop(a23_str, get_module_temp_dir())

    # THEN
    assert a23_belief.belief_label == a23_str
    x_beliefs_dir = create_path(get_module_temp_dir(), "beliefs")
    assert a23_belief._belief_dir == create_path(x_beliefs_dir, a23_str)
    assert a23_belief._believers_dir == create_path(a23_belief._belief_dir, "believers")


def test_BeliefUnit_create_empty_believer_from_belief_ReturnsObj_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    slash_str = "/"
    x_fund_iota = 4
    x_respect_bit = 5
    x_penny = 6
    a23_belief = beliefunit_shop(
        a23_str,
        belief_mstr_dir,
        knot=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        penny=x_penny,
    )
    sue_str = "Sue"

    # WHEN
    generated_believer = a23_belief.create_empty_believer_from_belief(sue_str)

    # THEN
    assert generated_believer.knot == slash_str
    assert generated_believer.fund_iota == x_fund_iota
    assert generated_believer.respect_bit == x_respect_bit
    assert generated_believer.penny == x_penny


def test_BeliefUnit_create_gut_file_if_none_SetsDirAndFiles_Scenario1_believer_dir_ExistsNoFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    a23_belief = beliefunit_shop(a23_str, belief_mstr_dir)
    sue_str = "Sue"
    sue_believer_dir = create_believer_dir_path(belief_mstr_dir, a23_str, sue_str)
    assert not os_path_exists(sue_believer_dir)
    assert not gut_file_exists(belief_mstr_dir, a23_str, sue_str)

    # WHEN
    a23_belief.create_gut_file_if_none(sue_str)

    # THEN
    print(f"{belief_mstr_dir=}")
    assert gut_file_exists(belief_mstr_dir, a23_str, sue_str)
    expected_sue_gut = believerunit_shop(sue_str, a23_str)
    assert open_gut_file(belief_mstr_dir, a23_str, sue_str) == expected_sue_gut


def test_BeliefUnit_create_gut_file_if_none_SetsDirAndFiles_Scenario2_believer_dir_ExistsNoFile_Create_gut_AndConfirmBeliefAttributesPassed(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    slash_str = "/"
    x_fund_iota = 4
    x_respect_bit = 5
    x_penny = 6
    a23_belief = beliefunit_shop(
        a23_str,
        belief_mstr_dir,
        knot=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        penny=x_penny,
    )
    sue_str = "Sue"
    sue_believer_dir = create_believer_dir_path(belief_mstr_dir, a23_str, sue_str)
    set_dir(sue_believer_dir)
    assert os_path_exists(sue_believer_dir)
    assert not gut_file_exists(belief_mstr_dir, a23_str, sue_str)

    # WHEN
    a23_belief.create_gut_file_if_none(sue_str)

    # THEN
    print(f"{belief_mstr_dir=}")
    assert gut_file_exists(belief_mstr_dir, a23_str, sue_str)
    generated_gut = open_gut_file(belief_mstr_dir, a23_str, sue_str)
    assert generated_gut.knot == slash_str
    assert generated_gut.fund_iota == x_fund_iota
    assert generated_gut.respect_bit == x_respect_bit
    assert generated_gut.penny == x_penny


def test_BeliefUnit_create_gut_file_if_none_SetsDirAndFiles_Scenario3_FileExistsIsNotReplaced(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    a23_belief = beliefunit_shop(a23_str, belief_mstr_dir)
    sue_str = "Sue"
    bob_str = "Bob"
    sue_gut = believerunit_shop(sue_str, a23_str)
    sue_gut.add_partnerunit(bob_str)
    save_gut_file(belief_mstr_dir, sue_gut)
    sue_believer_dir = create_believer_dir_path(belief_mstr_dir, a23_str, sue_str)
    assert os_path_exists(sue_believer_dir)
    assert gut_file_exists(belief_mstr_dir, a23_str, sue_str)

    # WHEN
    a23_belief.create_gut_file_if_none(sue_str)

    # THEN
    print(f"{belief_mstr_dir=}")
    assert gut_file_exists(belief_mstr_dir, a23_str, sue_str)
    assert open_gut_file(belief_mstr_dir, a23_str, sue_str) == sue_gut


def test_BeliefUnit_create_init_job_from_guts_Scenario0_CreatesFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    slash_str = "/"
    x_fund_iota = 4
    x_respect_bit = 5
    a23_belief = beliefunit_shop(
        a23_str,
        belief_mstr_dir,
        knot=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
    )
    sue_str = "Sue"
    assert not job_file_exists(belief_mstr_dir, a23_str, sue_str)

    # WHEN
    a23_belief.create_init_job_from_guts(sue_str)

    # THEN
    print(f"{belief_mstr_dir=}")
    assert job_file_exists(belief_mstr_dir, a23_str, sue_str)


def test_BeliefUnit_create_init_job_from_guts_Scenario1_ReplacesFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    slash_str = "/"
    x_fund_iota = 4
    x_respect_bit = 5
    a23_belief = beliefunit_shop(
        a23_str,
        belief_mstr_dir,
        knot=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
    )
    bob_str = "Bob"
    sue_str = "Sue"
    x0_sue_job = believerunit_shop(sue_str, a23_str)
    x0_sue_job.add_partnerunit(bob_str)
    save_job_file(belief_mstr_dir, x0_sue_job)
    assert open_job_file(belief_mstr_dir, a23_str, sue_str).get_partner(bob_str)

    # WHEN
    a23_belief.create_init_job_from_guts(sue_str)

    # THEN
    assert not open_job_file(belief_mstr_dir, a23_str, sue_str).get_partner(bob_str)


def test_BeliefUnit_create_init_job_from_guts_Scenario2_job_Has_gut_Partners(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    slash_str = "/"
    x_fund_iota = 4
    x_respect_bit = 5
    a23_belief = beliefunit_shop(
        a23_str,
        belief_mstr_dir,
        knot=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
    )
    bob_str = "Bob"
    sue_str = "Sue"
    a23_belief.create_init_job_from_guts(sue_str)
    sue_gut = believerunit_shop(sue_str, a23_str)
    sue_gut.add_partnerunit(bob_str)
    save_gut_file(belief_mstr_dir, sue_gut)
    assert not open_job_file(belief_mstr_dir, a23_str, sue_str).get_partner(bob_str)

    # WHEN
    a23_belief.create_init_job_from_guts(sue_str)

    # THEN
    assert open_job_file(belief_mstr_dir, a23_str, sue_str).get_partner(bob_str)


def test_BeliefUnit_create_init_job_from_guts_Scenario3_gut_FilesAreListenedTo(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    slash_str = "/"
    x_fund_iota = 4
    x_respect_bit = 5
    a23_belief = beliefunit_shop(
        a23_str,
        belief_mstr_dir,
        knot=slash_str,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
    )
    sue_str = "Sue"
    a23_belief.create_init_job_from_guts(sue_str)

    # create Sue gut
    bob_str = "Bob"
    sue_gut = believerunit_shop(sue_str, a23_str, knot=slash_str)
    sue_gut.add_partnerunit(bob_str)
    save_gut_file(belief_mstr_dir, sue_gut)
    # create Bob gut with agenda plan for Sue
    bob_gut = believerunit_shop(bob_str, a23_str, knot=slash_str)
    bob_gut.add_partnerunit(sue_str)
    casa_rope = bob_gut.make_l1_rope("casa")
    clean_rope = bob_gut.make_rope(casa_rope, "clean")
    bob_gut.add_plan(clean_rope, task=True)
    bob_gut.get_plan_obj(clean_rope).laborunit.set_laborlink(sue_str)
    save_gut_file(belief_mstr_dir, bob_gut)
    assert not open_job_file(belief_mstr_dir, a23_str, sue_str).get_agenda_dict()

    # WHEN
    a23_belief.create_init_job_from_guts(sue_str)

    # THEN
    assert open_job_file(belief_mstr_dir, a23_str, sue_str).get_agenda_dict()
    sue_agenda = open_job_file(belief_mstr_dir, a23_str, sue_str).get_agenda_dict()
    assert len(sue_agenda) == 1
    assert sue_agenda.get(clean_rope).get_plan_rope() == clean_rope


def test_BeliefUnit__set_all_healer_dutys_CorrectlySetsdutys(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "amy23"
    x_belief_mstr_dir = get_module_temp_dir()
    a23_belief = beliefunit_shop(a23_str, x_belief_mstr_dir)
    sue_str = "Sue"
    yao_str = "Yao"
    a23_belief.create_init_job_from_guts(sue_str)
    a23_belief.create_init_job_from_guts(yao_str)
    sue_gut_believer = open_gut_file(x_belief_mstr_dir, a23_str, sue_str)
    yao_gut_believer = open_gut_file(x_belief_mstr_dir, a23_str, yao_str)

    sue_gut_believer.add_partnerunit(sue_str)
    sue_gut_believer.add_partnerunit(yao_str)
    yao_gut_believer.add_partnerunit(sue_str)
    yao_gut_believer.add_partnerunit(yao_str)
    texas_str = "Texas"
    texas_rope = sue_gut_believer.make_l1_rope(texas_str)
    sue_gut_believer.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    yao_gut_believer.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    dallas_str = "dallas"
    dallas_rope = sue_gut_believer.make_rope(texas_rope, dallas_str)
    dallas_healerlink = healerlink_shop({sue_str, yao_str})
    dallas_plan = planunit_shop(dallas_str, healerlink=dallas_healerlink)
    elpaso_str = "el paso"
    elpaso_rope = sue_gut_believer.make_rope(texas_rope, elpaso_str)
    elpaso_healerlink = healerlink_shop({sue_str})
    elpaso_plan = planunit_shop(elpaso_str, healerlink=elpaso_healerlink)

    sue_gut_believer.set_plan(dallas_plan, texas_rope)
    sue_gut_believer.set_plan(elpaso_plan, texas_rope)
    yao_gut_believer.set_plan(dallas_plan, texas_rope)
    yao_gut_believer.set_plan(elpaso_plan, texas_rope)

    save_gut_file(x_belief_mstr_dir, sue_gut_believer)
    save_gut_file(x_belief_mstr_dir, yao_gut_believer)
    sue_filename = get_json_filename(sue_str)
    yao_filename = get_json_filename(yao_str)

    mstr_dir = x_belief_mstr_dir
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
    a23_belief._set_all_healer_dutys(sue_str)

    # THEN
    assert os_path_exists(sue_dallas_sue_duty_file_path)
    assert os_path_exists(sue_dallas_yao_duty_file_path) is False
    assert os_path_exists(yao_dallas_sue_duty_file_path)
    assert os_path_exists(yao_dallas_yao_duty_file_path) is False

    # WHEN
    a23_belief._set_all_healer_dutys(yao_str)

    # THEN
    assert os_path_exists(sue_dallas_sue_duty_file_path)
    assert os_path_exists(sue_dallas_yao_duty_file_path)
    assert os_path_exists(yao_dallas_sue_duty_file_path)
    assert os_path_exists(yao_dallas_yao_duty_file_path)


# def test_BeliefUnit_set_offi_time_Scenario0_SetsAttr():
#     # ESTABLISH
#     belief_mstr_dir = get_module_temp_dir()
#     time56 = 56
#     a23_belief = beliefunit_shop("amy23", belief_mstr_dir, _offi_time_max=time56)
#     assert a23_belief.offi_time == 0
#     assert a23_belief._offi_time_max == time56

#     # WHEN
#     time23 = 23
#     a23_belief.set_offi_time(time23)

#     # THEN
#     assert a23_belief.offi_time == time23
#     assert a23_belief._offi_time_max == time56


# def test_BeliefUnit_set_offi_time_Scenario1_SetsAttr():
#     # ESTABLISH
#     a23_belief = beliefunit_shop("amy23", get_module_temp_dir())
#     assert a23_belief.offi_time == 0
#     assert a23_belief._offi_time_max == 0

#     # WHEN
#     time23 = 23
#     a23_belief.set_offi_time(time23)

#     # THEN
#     assert a23_belief.offi_time == time23
#     assert a23_belief._offi_time_max == time23


def test_BeliefUnit_set_offi_time_max_Scenario0_SetsAttr():
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    time7 = 7
    a23_belief = beliefunit_shop("amy23", belief_mstr_dir)
    a23_belief._offi_time_max = time7
    # assert a23_belief.offi_time == 0
    assert a23_belief._offi_time_max == time7

    # WHEN
    time23 = 23
    a23_belief.set_offi_time_max(time23)

    # THEN
    # assert a23_belief.offi_time == 0
    assert a23_belief._offi_time_max == time23


# def test_BeliefUnit_set_offi_time_max_Scenario1_SetsAttr():
#     # ESTABLISH
#     belief_mstr_dir = get_module_temp_dir()
#     time21 = 21
#     time77 = 77
#     a23_belief = beliefunit_shop(
#         "amy23", belief_mstr_dir, offi_time=time21, _offi_time_max=time77
#     )
#     assert a23_belief.offi_time == time21
#     assert a23_belief._offi_time_max == time77

#     # WHEN / THEN
#     time11 = 11
#     with pytest_raises(Exception) as excinfo:
#         a23_belief.set_offi_time_max(time11)
#     exception_str = f"Cannot set _offi_time_max={time11} because it is less than offi_time={time21}"
#     assert str(excinfo.value) == exception_str


# def test_BeliefUnit_set_offi_time_Scenario0_SetsAttr():
#     # ESTABLISH
#     a23_belief = beliefunit_shop("amy23", get_module_temp_dir())
#     assert a23_belief.offi_time == 0
#     assert a23_belief._offi_time_max == 0

#     # WHEN
#     time23 = 23
#     time55 = 55
#     a23_belief.set_offi_time(time23, time55)

#     # THEN
#     assert a23_belief.offi_time == time23
#     assert a23_belief._offi_time_max == time55
