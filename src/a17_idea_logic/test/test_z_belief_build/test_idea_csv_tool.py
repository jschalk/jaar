from copy import deepcopy as copy_deepcopy
from src.a00_data_toolbox.file_toolbox import create_path
from src.a01_term_logic.rope import to_rope
from src.a03_group_logic.group import awardlink_shop
from src.a06_plan_logic.plan import planunit_shop
from src.a09_pack_logic.delta import plandelta_shop
from src.a09_pack_logic.pack import packunit_shop
from src.a16_pidgin_logic.pidgin import pidginunit_shop
from src.a17_idea_logic.idea import belief_build_from_df
from src.a17_idea_logic.idea_csv_tool import (
    add_beliefunit_to_stance_csv_strs,
    add_beliefunits_to_stance_csv_strs,
    add_pack_to_br00020_csv,
    add_pack_to_br00021_csv,
    add_pack_to_br00022_csv,
    add_pack_to_br00023_csv,
    add_pack_to_br00024_csv,
    add_pack_to_br00025_csv,
    add_pack_to_br00026_csv,
    add_pack_to_br00027_csv,
    add_pack_to_br00028_csv,
    add_pack_to_br00029_csv,
    add_packunit_to_stance_csv_strs,
    add_pidginunit_to_stance_csv_strs,
    add_plan_to_br00020_csv,
    add_plan_to_br00021_csv,
    add_plan_to_br00022_csv,
    add_plan_to_br00023_csv,
    add_plan_to_br00024_csv,
    add_plan_to_br00025_csv,
    add_plan_to_br00026_csv,
    add_plan_to_br00027_csv,
    add_plan_to_br00028_csv,
    add_plan_to_br00029_csv,
    add_planunit_to_stance_csv_strs,
    add_to_br00042_csv,
    add_to_br00043_csv,
    add_to_br00044_csv,
    add_to_br00045_csv,
    create_init_stance_idea_csv_strs,
)
from src.a17_idea_logic.idea_db_tool import get_ordered_csv
from src.a17_idea_logic.test._util.a17_env import (
    env_dir_setup_cleanup,
    idea_beliefs_dir,
)
from src.a17_idea_logic.test._util.idea_df_examples import (  # get_ex2_br00006_df,
    get_ex2_br00000_df,
    get_ex2_br00001_df,
    get_ex2_br00002_df,
    get_ex2_br00003_df,
    get_ex2_br00004_df,
    get_ex2_br00005_df,
)


def test_create_init_stance_idea_csv_strs_ReturnsObj_Scenario0_EmptyBeliefUnit(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    csv_delimiter = ","

    # WHEN
    x_ideas = create_init_stance_idea_csv_strs()

    # THEN
    expected_stance_csv_strs = {
        "br00000": "belief_label,timeline_label,c400_number,yr1_jan1_offset,monthday_distortion,fund_iota,penny,respect_bit,knot,job_listen_rotations\n",
        "br00001": "belief_label,owner_name,bud_time,quota,celldepth\n",
        "br00002": "belief_label,owner_name,acct_name,tran_time,amount\n",
        "br00003": "belief_label,cumulative_minute,hour_label\n",
        "br00004": "belief_label,cumulative_day,month_label\n",
        "br00005": "belief_label,weekday_order,weekday_label\n",
        # "br00006": "belief_label,offi_time,_offi_time_max\n",
        "br00020": "belief_label,owner_name,acct_name,group_title,group_cred_points,group_debt_points\n",
        "br00021": "belief_label,owner_name,acct_name,acct_cred_points,acct_debt_points\n",
        "br00022": "belief_label,owner_name,concept_rope,awardee_title,give_force,take_force\n",
        "br00023": "belief_label,owner_name,concept_rope,fcontext,fstate,fopen,fnigh\n",
        "br00024": "belief_label,owner_name,concept_rope,labor_title\n",
        "br00025": "belief_label,owner_name,concept_rope,healer_name\n",
        "br00026": "belief_label,owner_name,concept_rope,rcontext,pstate,pnigh,popen,pdivisor\n",
        "br00027": "belief_label,owner_name,concept_rope,rcontext,rconcept_active_requisite\n",
        "br00028": "belief_label,owner_name,concept_rope,begin,close,addin,numor,denom,morph,gogo_want,stop_want,mass,task,problem_bool\n",
        "br00029": "belief_label,owner_name,credor_respect,debtor_respect,fund_pool,max_tree_traverse,tally,fund_iota,penny,respect_bit\n",
        "br00042": "otx_title,inx_title,otx_knot,inx_knot,unknown_str\n",
        "br00043": "otx_name,inx_name,otx_knot,inx_knot,unknown_str\n",
        "br00044": "otx_label,inx_label,otx_knot,inx_knot,unknown_str\n",
        "br00045": "otx_rope,inx_rope,otx_knot,inx_knot,unknown_str\n",
    }
    expected_br00000_csv = expected_stance_csv_strs.get("br00000")
    expected_br00001_csv = expected_stance_csv_strs.get("br00001")
    expected_br00002_csv = expected_stance_csv_strs.get("br00002")
    expected_br00003_csv = expected_stance_csv_strs.get("br00003")
    expected_br00004_csv = expected_stance_csv_strs.get("br00004")
    expected_br00005_csv = expected_stance_csv_strs.get("br00005")
    # expected_br00006_csv = expected_stance_csv_strs.get("br00006")
    expected_br00020_csv = expected_stance_csv_strs.get("br00020")
    expected_br00021_csv = expected_stance_csv_strs.get("br00021")
    expected_br00022_csv = expected_stance_csv_strs.get("br00022")
    expected_br00023_csv = expected_stance_csv_strs.get("br00023")
    expected_br00024_csv = expected_stance_csv_strs.get("br00024")
    expected_br00025_csv = expected_stance_csv_strs.get("br00025")
    expected_br00026_csv = expected_stance_csv_strs.get("br00026")
    expected_br00027_csv = expected_stance_csv_strs.get("br00027")
    expected_br00028_csv = expected_stance_csv_strs.get("br00028")
    expected_br00029_csv = expected_stance_csv_strs.get("br00029")
    expected_br00042_csv = expected_stance_csv_strs.get("br00042")
    expected_br00043_csv = expected_stance_csv_strs.get("br00043")
    expected_br00044_csv = expected_stance_csv_strs.get("br00044")
    expected_br00045_csv = expected_stance_csv_strs.get("br00045")
    print(f"{expected_br00001_csv=}")

    face_event_str = "event_int,face_name,"
    assert x_ideas.get("br00000") == f"{face_event_str}{expected_br00000_csv}"
    assert x_ideas.get("br00001") == f"{face_event_str}{expected_br00001_csv}"
    assert x_ideas.get("br00002") == f"{face_event_str}{expected_br00002_csv}"
    assert x_ideas.get("br00003") == f"{face_event_str}{expected_br00003_csv}"
    assert x_ideas.get("br00004") == f"{face_event_str}{expected_br00004_csv}"
    assert x_ideas.get("br00005") == f"{face_event_str}{expected_br00005_csv}"
    # assert x_ideas.get("br00006") == f"{face_event_str}{expected_br00006_csv}"
    print(f"{expected_br00020_csv=}")
    print(x_ideas.get("br00020"))
    assert x_ideas.get("br00020") == f"{face_event_str}{expected_br00020_csv}"
    assert x_ideas.get("br00021") == f"{face_event_str}{expected_br00021_csv}"
    assert x_ideas.get("br00022") == f"{face_event_str}{expected_br00022_csv}"
    assert x_ideas.get("br00023") == f"{face_event_str}{expected_br00023_csv}"
    assert x_ideas.get("br00024") == f"{face_event_str}{expected_br00024_csv}"
    assert x_ideas.get("br00025") == f"{face_event_str}{expected_br00025_csv}"
    assert x_ideas.get("br00026") == f"{face_event_str}{expected_br00026_csv}"
    assert x_ideas.get("br00027") == f"{face_event_str}{expected_br00027_csv}"
    assert x_ideas.get("br00028") == f"{face_event_str}{expected_br00028_csv}"
    assert x_ideas.get("br00029") == f"{face_event_str}{expected_br00029_csv}"
    assert x_ideas.get("br00042") == f"{face_event_str}{expected_br00042_csv}"
    assert x_ideas.get("br00043") == f"{face_event_str}{expected_br00043_csv}"
    assert x_ideas.get("br00044") == f"{face_event_str}{expected_br00044_csv}"
    assert x_ideas.get("br00045") == f"{face_event_str}{expected_br00045_csv}"
    assert len(x_ideas) == 20


def test_add_beliefunit_to_stance_csv_strs_ReturnsObj_Scenario0_OneBeliefUnit(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    br00000_df = get_ex2_br00000_df()
    # print(f"{br00000_df=}")
    br00001_df = get_ex2_br00001_df()
    br00002_df = get_ex2_br00002_df()
    br00003_df = get_ex2_br00003_df()
    br00004_df = get_ex2_br00004_df()
    br00005_df = get_ex2_br00005_df()
    # br00006_df = get_ex2_br00006_df()
    x_fund_iota = 1
    x_respect_bit = 1
    x_penny = 1
    x_beliefs_dir = create_path(idea_beliefs_dir(), "Fay")
    x_beliefunits = belief_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_iota,
        x_respect_bit,
        x_penny,
        x_beliefs_dir,
    )
    csv_delimiter = ","
    x_csvs = create_init_stance_idea_csv_strs()
    br00_csv_header = x_csvs.get("br00000")
    br01_csv_header = x_csvs.get("br00001")
    br02_csv_header = x_csvs.get("br00002")
    br03_csv_header = x_csvs.get("br00003")
    br04_csv_header = x_csvs.get("br00004")
    br05_csv_header = x_csvs.get("br00005")
    # br06_csv_header = x_csvs.get("br00006")
    a23_beliefunit = x_beliefunits.get("amy23")

    # WHEN
    add_beliefunit_to_stance_csv_strs(a23_beliefunit, x_csvs, csv_delimiter)

    # THEN
    gen_br00000_csv = x_csvs.get("br00000")
    gen_br00001_csv = x_csvs.get("br00001")
    gen_br00002_csv = x_csvs.get("br00002")
    gen_br00003_csv = x_csvs.get("br00003")
    gen_br00004_csv = x_csvs.get("br00004")
    gen_br00005_csv = x_csvs.get("br00005")
    # gen_br00006_csv = x_csvs.get("br00006")
    expected_br00000_csv = ",,amy23,creg,7,440640,1,1,1,1,/,4\n"
    expected_br00001_csv = (
        ",,amy23,Bob,999,332,3\n,,amy23,Sue,777,445,3\n,,amy23,Yao,222,700,3\n"
    )
    expected_br00002_csv = ",,amy23,Bob,Zia,777,888\n,,amy23,Sue,Zia,999,234\n,,amy23,Yao,Zia,999,234\n,,amy23,Zia,Bob,777,888\n"
    expected_br00003_csv = ",,amy23,60,0-12am\n,,amy23,120,1-1am\n,,amy23,180,2-2am\n,,amy23,240,3-3am\n,,amy23,300,4-4am\n,,amy23,360,5-5am\n,,amy23,420,6-6am\n,,amy23,480,7-7am\n,,amy23,540,8-8am\n,,amy23,600,9-9am\n,,amy23,660,10-10am\n,,amy23,720,11-11am\n,,amy23,780,12-12pm\n,,amy23,840,13-1pm\n,,amy23,900,14-2pm\n,,amy23,960,15-3pm\n,,amy23,1020,16-4pm\n,,amy23,1080,17-5pm\n,,amy23,1140,18-6pm\n,,amy23,1200,19-7pm\n,,amy23,1260,20-8pm\n,,amy23,1320,21-9pm\n,,amy23,1380,22-10pm\n,,amy23,1440,23-11pm\n"
    expected_br00004_csv = ",,amy23,31,March\n,,amy23,61,April\n,,amy23,92,May\n,,amy23,122,June\n,,amy23,153,July\n,,amy23,184,August\n,,amy23,214,September\n,,amy23,245,October\n,,amy23,275,November\n,,amy23,306,December\n,,amy23,337,January\n,,amy23,365,February\n"
    expected_br00005_csv = ",,amy23,0,Wednesday\n,,amy23,1,Thursday\n,,amy23,2,Friday\n,,amy23,3,Saturday\n,,amy23,4,Sunday\n,,amy23,5,Monday\n,,amy23,6,Tuesday\n"
    # expected_br00006_csv = ",,amy23,0,Wednesday\n,,amy23,1,Thursday\n,,amy23,2,Friday\n,,amy23,3,Saturday\n,,amy23,4,Sunday\n,,amy23,5,Monday\n,,amy23,6,Tuesday\n"

    # print(f"      {br01_csv_header=}")
    # print(f" {expected_br00000_csv=}")
    # print(f"      {gen_br00000_csv=}")
    assert gen_br00000_csv == f"{br00_csv_header}{expected_br00000_csv}"
    assert gen_br00001_csv == f"{br01_csv_header}{expected_br00001_csv}"
    assert gen_br00002_csv == f"{br02_csv_header}{expected_br00002_csv}"
    assert gen_br00003_csv == f"{br03_csv_header}{expected_br00003_csv}"
    assert gen_br00004_csv == f"{br04_csv_header}{expected_br00004_csv}"
    assert gen_br00005_csv == f"{br05_csv_header}{expected_br00005_csv}"
    # assert gen_br00006_csv == f"{br06_csv_header}{expected_br00006_csv}"


def test_add_beliefunits_to_stance_csv_strs_ReturnsObj_Scenario1_TwoBeliefUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    br00000_df = get_ex2_br00000_df()
    br00001_df = get_ex2_br00001_df()
    br00002_df = get_ex2_br00002_df()
    br00003_df = get_ex2_br00003_df()
    br00004_df = get_ex2_br00004_df()
    br00005_df = get_ex2_br00005_df()
    x_fund_iota = 1
    x_respect_bit = 1
    x_penny = 1
    x_beliefs_dir = create_path(idea_beliefs_dir(), "Fay")
    x_beliefunits = belief_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_iota,
        x_respect_bit,
        x_penny,
        x_beliefs_dir,
    )
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()

    # WHEN
    add_beliefunits_to_stance_csv_strs(x_beliefunits, x_ideas, csv_delimiter)

    # THEN
    expected_br00000_csv = get_ordered_csv(get_ex2_br00000_df())
    expected_br00001_csv = get_ordered_csv(get_ex2_br00001_df())
    expected_br00002_csv = get_ordered_csv(get_ex2_br00002_df())
    expected_br00003_csv = get_ordered_csv(get_ex2_br00003_df())
    expected_br00004_csv = get_ordered_csv(get_ex2_br00004_df())
    expected_br00005_csv = get_ordered_csv(get_ex2_br00005_df())
    expected_br00000_csv = f"event_int,face_name,{expected_br00000_csv}"
    expected_br00001_csv = f"event_int,face_name,{expected_br00001_csv}"
    expected_br00002_csv = f"event_int,face_name,{expected_br00002_csv}"
    expected_br00003_csv = f"event_int,face_name,{expected_br00003_csv}"
    expected_br00004_csv = f"event_int,face_name,{expected_br00004_csv}"
    expected_br00005_csv = f"event_int,face_name,{expected_br00005_csv}"
    expected_br00000_csv = expected_br00000_csv.replace("amy", ",,amy")
    expected_br00001_csv = expected_br00001_csv.replace("amy", ",,amy")
    expected_br00002_csv = expected_br00002_csv.replace("amy", ",,amy")
    expected_br00003_csv = expected_br00003_csv.replace("amy", ",,amy")
    expected_br00004_csv = expected_br00004_csv.replace("amy", ",,amy")
    expected_br00005_csv = expected_br00005_csv.replace("amy", ",,amy")
    expected_br00000_csv = expected_br00000_csv.replace("jeffy45", ",,jeffy45")
    expected_br00001_csv = expected_br00001_csv.replace("jeffy45", ",,jeffy45")
    expected_br00002_csv = expected_br00002_csv.replace("jeffy45", ",,jeffy45")
    expected_br00003_csv = expected_br00003_csv.replace("jeffy45", ",,jeffy45")
    expected_br00004_csv = expected_br00004_csv.replace("jeffy45", ",,jeffy45")
    expected_br00005_csv = expected_br00005_csv.replace("jeffy45", ",,jeffy45")

    assert len(x_ideas) == 20
    generated_br00000_csv = x_ideas.get("br00000")
    generated_br00001_csv = x_ideas.get("br00001")
    generated_br00002_csv = x_ideas.get("br00002")
    generated_br00003_csv = x_ideas.get("br00003")
    generated_br00004_csv = x_ideas.get("br00004")
    generated_br00005_csv = x_ideas.get("br00005")
    # print(f" {expected_br00000_csv=}")
    # print(f"{generated_br00000_csv=}")
    assert generated_br00000_csv == expected_br00000_csv
    assert generated_br00001_csv == expected_br00001_csv
    assert generated_br00002_csv == expected_br00002_csv
    assert len(generated_br00003_csv) == len(expected_br00003_csv)
    assert generated_br00004_csv == expected_br00004_csv
    assert generated_br00005_csv == expected_br00005_csv


def test_add_plan_to_br00020_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    yao_str = "Yao"
    a23_str = "amy23"
    bob_plan = planunit_shop(bob_str, a23_str)
    bob_plan.add_acctunit(yao_str)
    run_str = ";Run"
    run_credit = 33
    run_debt = 55
    bob_plan.get_acct(yao_str).add_membership(run_str, run_credit, run_debt)
    csv_header = x_ideas.get("br00020")

    # WHEN
    x_csv = add_plan_to_br00020_csv(csv_header, bob_plan, csv_delimiter)

    # THEN
    yao_yao_row = f",,{a23_str},{bob_str},{yao_str},{yao_str},1,1\n"
    yao_run_row = f",,{a23_str},{bob_str},{yao_str},{run_str},{run_credit},{run_debt}\n"
    print(f"{x_csv=}")
    print(f"{yao_run_row=}")
    assert x_csv == f"{csv_header}{yao_yao_row}{yao_run_row}"


def test_add_plan_to_br00021_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    yao_str = "Yao"
    yao_credit = 33
    yao_debt = 55
    a23_str = "amy23"
    bob_plan = planunit_shop(bob_str, a23_str)
    bob_plan.add_acctunit(yao_str, yao_credit, yao_debt)
    csv_header = x_ideas.get("br00021")

    # WHEN
    x_csv = add_plan_to_br00021_csv(csv_header, bob_plan, csv_delimiter)

    # THEN
    yao_row = f",,{a23_str},{bob_str},{yao_str},{yao_credit},{yao_debt}\n"
    assert x_csv == f"{csv_header}{yao_row}"


def test_add_plan_to_br00022_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "amy23"
    bob_plan = planunit_shop(bob_str, a23_str)
    casa_rope = bob_plan.make_l1_rope("casa")
    yao_str = "Yao"
    yao_give_force = 55
    yao_take_force = 77
    casa_awardlink = awardlink_shop(yao_str, yao_give_force, yao_take_force)
    bob_plan.add_concept(casa_rope)
    bob_plan.edit_concept_attr(casa_rope, awardlink=casa_awardlink)
    csv_header = x_ideas.get("br00022")
    print(f"{csv_header=}")

    # WHEN
    bob_plan.settle_plan()
    x_csv = add_plan_to_br00022_csv(csv_header, bob_plan, csv_delimiter)

    # THEN
    yao_award_row = f",,{a23_str},{bob_str},{casa_rope},{yao_str},{yao_give_force},{yao_take_force}\n"
    assert x_csv == f"{csv_header}{yao_award_row}"


def test_add_plan_to_br00023_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "amy23"
    a23_rope = to_rope(a23_str)
    bob_plan = planunit_shop(bob_str, a23_str)
    casa_rope = bob_plan.make_l1_rope("casa")
    clean_rope = bob_plan.make_rope(casa_rope, "clean")
    clean_fopen = 55
    clean_fnigh = 77
    bob_plan.add_concept(casa_rope)
    bob_plan.add_concept(clean_rope)
    bob_plan.add_fact(casa_rope, clean_rope, clean_fopen, clean_fnigh)
    csv_header = x_ideas.get("br00023")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_plan_to_br00023_csv(csv_header, bob_plan, csv_delimiter)

    # THEN
    clean_row = f",,{a23_str},{bob_str},{a23_rope},{casa_rope},{clean_rope},{clean_fopen},{clean_fnigh}\n"
    assert x_csv == f"{csv_header}{clean_row}"


def test_add_plan_to_br00024_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "amy23"
    bob_plan = planunit_shop(bob_str, a23_str)
    casa_rope = bob_plan.make_l1_rope("casa")
    bob_plan.add_concept(casa_rope)
    casa_concept = bob_plan.get_concept_obj(casa_rope)
    cleaners_str = "cleaners"
    casa_concept.laborunit.set_laborlink(cleaners_str)
    csv_header = x_ideas.get("br00024")
    print(f"{csv_header=}")

    # WHEN
    bob_plan.settle_plan()
    x_csv = add_plan_to_br00024_csv(csv_header, bob_plan, csv_delimiter)

    # THEN
    cleaners_row = f",,{a23_str},{bob_str},{casa_rope},{cleaners_str}\n"
    assert x_csv == f"{csv_header}{cleaners_row}"


def test_add_plan_to_br00025_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "amy23"
    bob_plan = planunit_shop(bob_str, a23_str)
    casa_rope = bob_plan.make_l1_rope("casa")
    bob_plan.add_concept(casa_rope)
    casa_concept = bob_plan.get_concept_obj(casa_rope)
    cleaners_str = "cleaners"
    casa_concept.healerlink.set_healer_name(cleaners_str)
    csv_header = x_ideas.get("br00025")
    print(f"{csv_header=}")

    # WHEN
    bob_plan.settle_plan()
    x_csv = add_plan_to_br00025_csv(csv_header, bob_plan, csv_delimiter)

    # THEN
    cleaners_row = f",,{a23_str},{bob_str},{casa_rope},{cleaners_str}\n"
    assert x_csv == f"{csv_header}{cleaners_row}"


def test_add_plan_to_br00026_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "amy23"
    bob_plan = planunit_shop(bob_str, a23_str)
    mop_rope = bob_plan.make_l1_rope("mop")
    casa_rope = bob_plan.make_l1_rope("casa")
    clean_rope = bob_plan.make_rope(casa_rope, "clean")
    clean_popen = 22
    clean_pnigh = 55
    clean_pdivisor = 77
    bob_plan.add_concept(mop_rope)
    bob_plan.add_concept(casa_rope)
    bob_plan.add_concept(clean_rope)
    bob_plan.edit_concept_attr(
        mop_rope,
        reason_rcontext=casa_rope,
        reason_premise=clean_rope,
        popen=clean_popen,
        reason_pnigh=clean_pnigh,
        pdivisor=clean_pdivisor,
    )
    csv_header = x_ideas.get("br00026")
    print(f"{csv_header=}")

    # WHEN
    bob_plan.settle_plan()
    x_csv = add_plan_to_br00026_csv(csv_header, bob_plan, csv_delimiter)

    # THEN
    mop_row = f",,{a23_str},{bob_str},{mop_rope},{casa_rope},{clean_rope},{clean_popen},{clean_pnigh},{clean_pdivisor}\n"
    assert x_csv == f"{csv_header}{mop_row}"


def test_add_plan_to_br00027_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "amy23"
    bob_plan = planunit_shop(bob_str, a23_str)
    mop_rope = bob_plan.make_l1_rope("mop")
    casa_rope = bob_plan.make_l1_rope("casa")
    bob_plan.add_concept(mop_rope)
    bob_plan.add_concept(casa_rope)
    bob_plan.edit_concept_attr(
        mop_rope,
        reason_rcontext=casa_rope,
        reason_rconcept_active_requisite=True,
    )
    csv_header = x_ideas.get("br00027")
    print(f"{csv_header=}")

    # WHEN
    bob_plan.settle_plan()
    x_csv = add_plan_to_br00027_csv(csv_header, bob_plan, csv_delimiter)

    # THEN
    casa_row = f",,{a23_str},{bob_str},{mop_rope},{casa_rope},True\n"
    assert x_csv == f"{csv_header}{casa_row}"


def test_add_plan_to_br00028_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "amy23"
    a23_rope = to_rope(a23_str)
    bob_plan = planunit_shop(bob_str, a23_str)
    mop_rope = bob_plan.make_l1_rope("mop")
    casa_rope = bob_plan.make_l1_rope("casa")
    casa_begin = 3
    casa_close = 5
    casa_addin = 7
    casa_numor = 13
    casa_denom = 17
    casa_morph = 27
    casa_gogo_want = 31
    casa_stop_want = 41
    casa_mass = 2
    casa_task = False
    casa_problem_bool = False
    bob_plan.add_concept(casa_rope)
    bob_plan.add_concept(mop_rope)
    bob_plan.edit_concept_attr(
        mop_rope,
        begin=casa_begin,
        close=casa_close,
        addin=casa_addin,
        numor=casa_numor,
        denom=casa_denom,
        morph=casa_morph,
        gogo_want=casa_gogo_want,
        stop_want=casa_stop_want,
        mass=casa_mass,
        task=casa_task,
        problem_bool=casa_problem_bool,
    )
    csv_header = x_ideas.get("br00028")
    print(f"{csv_header=}")

    # WHEN
    bob_plan.settle_plan()
    x_csv = add_plan_to_br00028_csv(csv_header, bob_plan, csv_delimiter)

    # THEN
    root_row = f",,{a23_str},{bob_str},,{a23_rope},,,,,,,,,1,False,False\n"
    mop_row = f",,{a23_str},{bob_str},{mop_rope},{casa_begin},{casa_close},{casa_addin},{casa_numor},{casa_denom},{casa_morph},{casa_gogo_want},{casa_stop_want},{casa_mass},{casa_task},{casa_problem_bool}\n"
    casa_row = f",,{a23_str},{bob_str},{casa_rope},,,,,,,,,0,False,False\n"
    # print(f"{mop_row=}")
    expected_csv = f"{csv_header}{mop_row}{casa_row}"
    print(f"       {x_csv=}")
    print(f"{expected_csv=}")
    assert x_csv == expected_csv


def test_add_plan_to_br00029_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "amy23"
    bob_plan = planunit_shop(bob_str, a23_str)
    bob_plan.credor_respect = 444
    bob_plan.debtor_respect = 555
    bob_plan.fund_pool = 777
    bob_plan.max_tree_traverse = 3
    bob_plan.tally = 10
    bob_plan.fund_iota = 12
    bob_plan.penny = 13
    bob_plan.respect_bit = 15
    csv_header = x_ideas.get("br00029")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_plan_to_br00029_csv(csv_header, bob_plan, csv_delimiter)

    # THEN
    plan_row = f",,{a23_str},{bob_str},{bob_plan.credor_respect},{bob_plan.debtor_respect},{bob_plan.fund_pool},{bob_plan.max_tree_traverse},{bob_plan.tally},{bob_plan.fund_iota},{bob_plan.penny},{bob_plan.respect_bit}\n"
    assert x_csv == f"{csv_header}{plan_row}"


def test_add_planunit_to_stance_csv_strs_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    yao_str = "Yao"
    a23_str = "amy23"
    bob_plan = planunit_shop(bob_str, a23_str)
    bob_plan.add_acctunit(yao_str)
    mop_rope = bob_plan.make_l1_rope("mop")
    casa_rope = bob_plan.make_l1_rope("casa")
    clean_rope = bob_plan.make_rope(casa_rope, "clean")
    bob_plan.add_concept(mop_rope)
    bob_plan.add_concept(casa_rope)
    bob_plan.add_concept(clean_rope)
    bob_plan.edit_concept_attr(
        mop_rope, reason_rcontext=casa_rope, reason_premise=clean_rope
    )
    bob_plan.add_concept(casa_rope)
    bob_plan.edit_concept_attr(casa_rope, awardlink=awardlink_shop(yao_str))
    bob_plan.add_fact(casa_rope, clean_rope)

    br00020_header = x_ideas.get("br00020")
    br00021_header = x_ideas.get("br00021")
    br00022_header = x_ideas.get("br00022")
    br00023_header = x_ideas.get("br00023")
    br00024_header = x_ideas.get("br00024")
    br00025_header = x_ideas.get("br00025")
    br00026_header = x_ideas.get("br00026")
    br00027_header = x_ideas.get("br00027")
    br00028_header = x_ideas.get("br00028")
    br00029_header = x_ideas.get("br00029")

    # WHEN
    bob_plan.settle_plan()
    add_planunit_to_stance_csv_strs(bob_plan, x_ideas, csv_delimiter)

    # THEN
    assert x_ideas.get("br00020") != br00020_header
    assert x_ideas.get("br00021") != br00021_header
    assert x_ideas.get("br00022") != br00022_header
    assert x_ideas.get("br00023") != br00023_header
    # assert x_ideas.get("br00024") != br00024_header
    # assert x_ideas.get("br00025") != br00025_header
    assert x_ideas.get("br00026") != br00026_header
    assert x_ideas.get("br00027") != br00027_header
    assert x_ideas.get("br00028") != br00028_header
    assert x_ideas.get("br00029") != br00029_header


def test_add_to_br00042_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    event7 = 7
    bob_otx_knot = ";"
    bob_inx_knot = "/"
    bob_unknown_str = "UNKNOWN"
    bob7_pidginunit = pidginunit_shop(
        bob_str, event7, bob_otx_knot, bob_inx_knot, bob_unknown_str
    )
    run_otx = "run"
    run_inx = "cours"
    bob7_pidginunit.set_otx2inx("TitleTerm", run_otx, run_inx)
    csv_header = x_ideas.get("br00042")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_to_br00042_csv(csv_header, bob7_pidginunit, csv_delimiter)

    # THEN
    run_row = f"{bob_str},{event7},{run_otx},{bob_otx_knot},{run_inx},{bob_inx_knot},{bob_unknown_str}\n"
    assert x_csv == f"{csv_header}{run_row}"


def test_add_to_br00043_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    event7 = 7
    bob_otx_knot = ";"
    bob_inx_knot = "/"
    bob_unknown_str = "UNKNOWN"
    bob7_pidginunit = pidginunit_shop(
        bob_str, event7, bob_otx_knot, bob_inx_knot, bob_unknown_str
    )
    yao_otx = "Yao"
    yao_inx = "YaoMing"
    bob7_pidginunit.set_otx2inx("NameTerm", yao_otx, yao_inx)
    csv_header = x_ideas.get("br00043")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_to_br00043_csv(csv_header, bob7_pidginunit, csv_delimiter)

    # THEN
    bob_row = f"{bob_str},{event7},{yao_otx},{bob_otx_knot},{yao_inx},{bob_inx_knot},{bob_unknown_str}\n"
    assert x_csv == f"{csv_header}{bob_row}"


def test_add_to_br00044_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    event7 = 7
    bob_otx_knot = ";"
    bob_inx_knot = "/"
    bob_unknown_str = "UNKNOWN"
    bob7_pidginunit = pidginunit_shop(
        bob_str, event7, bob_otx_knot, bob_inx_knot, bob_unknown_str
    )
    clean_otx = "clean"
    clean_inx = "limpia"
    bob7_pidginunit.set_otx2inx("LabelTerm", clean_otx, clean_inx)
    csv_header = x_ideas.get("br00044")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_to_br00044_csv(csv_header, bob7_pidginunit, csv_delimiter)

    # THEN
    bob_row = f"{bob_str},{event7},{clean_otx},{bob_otx_knot},{clean_inx},{bob_inx_knot},{bob_unknown_str}\n"
    assert x_csv == f"{csv_header}{bob_row}"


def test_add_to_br00045_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    event7 = 7
    bob_otx_knot = ";"
    bob_inx_knot = "/"
    bob_unknown_str = "UNKNOWN"
    bob7_pidginunit = pidginunit_shop(
        bob_str, event7, bob_otx_knot, bob_inx_knot, bob_unknown_str
    )
    clean_otx = "clean"
    clean_inx = "limpia"
    bob7_pidginunit.set_otx2inx("RopeTerm", clean_otx, clean_inx)
    csv_header = x_ideas.get("br00045")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_to_br00045_csv(csv_header, bob7_pidginunit, csv_delimiter)

    # THEN
    bob_row = f"{bob_str},{event7},{clean_otx},{bob_otx_knot},{clean_inx},{bob_inx_knot},{bob_unknown_str}\n"
    assert x_csv == f"{csv_header}{bob_row}"


def test_add_pidginunit_to_stance_csv_strs_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    event7 = 7
    bob_otx_knot = ";"
    bob_inx_knot = "/"
    bob_unknown_str = "UNKNOWN"
    bob7_pidginunit = pidginunit_shop(
        bob_str, event7, bob_otx_knot, bob_inx_knot, bob_unknown_str
    )
    clean_otx = "clean"
    clean_inx = "limpia"
    bob7_pidginunit.set_otx2inx("RopeTerm", clean_otx, clean_inx)
    yao_otx = "Yao"
    yao_inx = "YaoMing"
    bob7_pidginunit.set_otx2inx("NameTerm", yao_otx, yao_inx)
    run_otx = "run"
    run_inx = "cours"
    bob7_pidginunit.set_otx2inx("TitleTerm", run_otx, run_inx)
    clean_otx = "clean"
    clean_inx = "limpia"
    bob7_pidginunit.set_otx2inx("LabelTerm", clean_otx, clean_inx)
    br00042_header = x_ideas.get("br00042")
    br00043_header = x_ideas.get("br00043")
    br00044_header = x_ideas.get("br00044")
    br00045_header = x_ideas.get("br00045")

    # WHEN
    add_pidginunit_to_stance_csv_strs(bob7_pidginunit, x_ideas, csv_delimiter)

    # THEN
    assert x_ideas.get("br00042") != br00042_header
    assert x_ideas.get("br00043") != br00043_header
    assert x_ideas.get("br00044") != br00044_header
    assert x_ideas.get("br00045") != br00045_header


def test_add_pack_to_br00020_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    yao_str = "Yao"
    a23_str = "amy23"
    bob_plan = planunit_shop(bob_str, a23_str)
    bob_plan.add_acctunit(yao_str)
    run_str = ";Run"
    run_credit = 33
    run_debt = 55
    bob_plan.get_acct(yao_str).add_membership(run_str, run_credit, run_debt)
    bob_plandelta = plandelta_shop()
    bob_plandelta.add_all_planatoms(bob_plan)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_plandelta(bob_plandelta)
    csv_header = x_ideas.get("br00020")

    # WHEN
    x_csv = add_pack_to_br00020_csv(csv_header, sue7_pack, csv_delimiter)

    # THEN
    yao_yao_row = f"{sue_str},{event7},{a23_str},{bob_str},{yao_str},{yao_str},1,1\n"
    yao_run_row = f"{sue_str},{event7},{a23_str},{bob_str},{yao_str},{run_str},{run_credit},{run_debt}\n"
    print(f"       {x_csv=}")
    expected_csv = f"{csv_header}{yao_run_row}{yao_yao_row}"
    print(f"{expected_csv=}")
    assert len(x_csv) == len(f"{csv_header}{yao_run_row}{yao_yao_row}")


def test_add_pack_to_br00021_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    yao_str = "Yao"
    yao_credit = 33
    yao_debt = 55
    a23_str = "amy23"
    bob_plan = planunit_shop(bob_str, a23_str)
    bob_plan.add_acctunit(yao_str, yao_credit, yao_debt)
    bob_plandelta = plandelta_shop()
    bob_plandelta.add_all_planatoms(bob_plan)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_plandelta(bob_plandelta)
    csv_header = x_ideas.get("br00021")

    # WHEN
    x_csv = add_pack_to_br00021_csv(csv_header, sue7_pack, csv_delimiter)

    # THEN
    yao_row = (
        f"{sue_str},{event7},{a23_str},{bob_str},{yao_str},{yao_credit},{yao_debt}\n"
    )
    assert x_csv == f"{csv_header}{yao_row}"


def test_add_pack_to_br00022_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "amy23"
    bob_plan = planunit_shop(bob_str, a23_str)
    casa_rope = bob_plan.make_l1_rope("casa")
    yao_str = "Yao"
    yao_give_force = 55
    yao_take_force = 77
    casa_awardlink = awardlink_shop(yao_str, yao_give_force, yao_take_force)
    bob_plan.add_concept(casa_rope)
    bob_plan.edit_concept_attr(casa_rope, awardlink=casa_awardlink)
    bob_plandelta = plandelta_shop()
    bob_plandelta.add_all_planatoms(bob_plan)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_plandelta(bob_plandelta)
    csv_header = x_ideas.get("br00022")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_pack_to_br00022_csv(csv_header, sue7_pack, csv_delimiter)

    # THEN
    yao_award_row = f"{sue_str},{event7},{a23_str},{bob_str},{casa_rope},{yao_str},{yao_give_force},{yao_take_force}\n"
    assert x_csv == f"{csv_header}{yao_award_row}"


def test_add_pack_to_br00023_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "amy23"
    a23_rope = to_rope(a23_str)
    bob_plan = planunit_shop(bob_str, a23_str)
    casa_rope = bob_plan.make_l1_rope("casa")
    clean_rope = bob_plan.make_rope(casa_rope, "clean")
    clean_fopen = 55
    clean_fnigh = 77
    bob_plan.add_concept(casa_rope)
    bob_plan.add_concept(clean_rope)
    bob_plan.add_fact(casa_rope, clean_rope, clean_fopen, clean_fnigh)
    bob_plandelta = plandelta_shop()
    bob_plandelta.add_all_planatoms(bob_plan)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_plandelta(bob_plandelta)
    csv_header = x_ideas.get("br00023")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_pack_to_br00023_csv(csv_header, sue7_pack, csv_delimiter)

    # THEN
    clean_row = f"{sue_str},{event7},{a23_str},{bob_str},{a23_rope},{casa_rope},{clean_rope},{clean_fopen},{clean_fnigh}\n"
    expected_csv = f"{csv_header}{clean_row}"
    print(f"       {x_csv=}")
    print(f"{expected_csv=}")
    assert x_csv == expected_csv


def test_add_pack_to_br00024_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "amy23"
    bob_plan = planunit_shop(bob_str, a23_str)
    casa_rope = bob_plan.make_l1_rope("casa")
    bob_plan.add_concept(casa_rope)
    casa_concept = bob_plan.get_concept_obj(casa_rope)
    cleaners_str = "cleaners"
    casa_concept.laborunit.set_laborlink(cleaners_str)
    bob_plandelta = plandelta_shop()
    bob_plandelta.add_all_planatoms(bob_plan)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_plandelta(bob_plandelta)
    csv_header = x_ideas.get("br00024")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_pack_to_br00024_csv(csv_header, sue7_pack, csv_delimiter)

    # THEN
    cleaners_row = (
        f"{sue_str},{event7},{a23_str},{bob_str},{casa_rope},{cleaners_str}\n"
    )
    expected_csv = f"{csv_header}{cleaners_row}"
    print(f"       {x_csv=}")
    print(f"{expected_csv=}")
    assert x_csv == f"{csv_header}{cleaners_row}"


def test_add_pack_to_br00025_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "amy23"
    bob_plan = planunit_shop(bob_str, a23_str)
    casa_rope = bob_plan.make_l1_rope("casa")
    bob_plan.add_concept(casa_rope)
    casa_concept = bob_plan.get_concept_obj(casa_rope)
    cleaners_str = "cleaners"
    casa_concept.healerlink.set_healer_name(cleaners_str)
    bob_plandelta = plandelta_shop()
    bob_plandelta.add_all_planatoms(bob_plan)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_plandelta(bob_plandelta)
    csv_header = x_ideas.get("br00025")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_pack_to_br00025_csv(csv_header, sue7_pack, csv_delimiter)

    # THEN
    cleaners_row = (
        f"{sue_str},{event7},{a23_str},{bob_str},{casa_rope},{cleaners_str}\n"
    )
    assert x_csv == f"{csv_header}{cleaners_row}"


def test_add_pack_to_br00026_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "amy23"
    bob_plan = planunit_shop(bob_str, a23_str)
    mop_rope = bob_plan.make_l1_rope("mop")
    casa_rope = bob_plan.make_l1_rope("casa")
    clean_rope = bob_plan.make_rope(casa_rope, "clean")
    clean_popen = 22
    clean_pnigh = 55
    clean_pdivisor = 77
    bob_plan.add_concept(mop_rope)
    bob_plan.add_concept(casa_rope)
    bob_plan.add_concept(clean_rope)
    bob_plan.edit_concept_attr(
        mop_rope,
        reason_rcontext=casa_rope,
        reason_premise=clean_rope,
        popen=clean_popen,
        reason_pnigh=clean_pnigh,
        pdivisor=clean_pdivisor,
    )
    bob_plandelta = plandelta_shop()
    bob_plandelta.add_all_planatoms(bob_plan)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_plandelta(bob_plandelta)
    csv_header = x_ideas.get("br00026")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_pack_to_br00026_csv(csv_header, sue7_pack, csv_delimiter)

    # THEN
    mop_row = f"{sue_str},{event7},{a23_str},{bob_str},{mop_rope},{casa_rope},{clean_rope},{clean_popen},{clean_pnigh},{clean_pdivisor}\n"
    assert x_csv == f"{csv_header}{mop_row}"


def test_add_pack_to_br00027_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "amy23"
    bob_plan = planunit_shop(bob_str, a23_str)
    mop_rope = bob_plan.make_l1_rope("mop")
    casa_rope = bob_plan.make_l1_rope("casa")
    bob_plan.add_concept(mop_rope)
    bob_plan.add_concept(casa_rope)
    bob_plan.edit_concept_attr(
        mop_rope,
        reason_rcontext=casa_rope,
        reason_rconcept_active_requisite=True,
    )
    bob_plandelta = plandelta_shop()
    bob_plandelta.add_all_planatoms(bob_plan)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_plandelta(bob_plandelta)
    csv_header = x_ideas.get("br00027")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_pack_to_br00027_csv(csv_header, sue7_pack, csv_delimiter)

    # THEN
    casa_row = f"{sue_str},{event7},{a23_str},{bob_str},{mop_rope},{casa_rope},True\n"
    assert x_csv == f"{csv_header}{casa_row}"


def test_add_pack_to_br00028_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "amy23"
    a23_rope = to_rope(a23_str)
    bob_plan = planunit_shop(bob_str, a23_str)
    mop_rope = bob_plan.make_l1_rope("mop")
    casa_rope = bob_plan.make_l1_rope("casa")
    casa_begin = 3
    casa_close = 5
    casa_addin = 7
    casa_numor = 13
    casa_denom = 17
    casa_morph = 27
    casa_gogo_want = 31
    casa_stop_want = 41
    casa_mass = 2
    casa_task = False
    casa_problem_bool = False
    bob_plan.add_concept(casa_rope)
    bob_plan.add_concept(mop_rope)
    bob_plan.edit_concept_attr(
        mop_rope,
        begin=casa_begin,
        close=casa_close,
        addin=casa_addin,
        numor=casa_numor,
        denom=casa_denom,
        morph=casa_morph,
        gogo_want=casa_gogo_want,
        stop_want=casa_stop_want,
        mass=casa_mass,
        task=casa_task,
        problem_bool=casa_problem_bool,
    )
    bob_plandelta = plandelta_shop()
    bob_plandelta.add_all_planatoms(bob_plan)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_plandelta(bob_plandelta)
    csv_header = x_ideas.get("br00028")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_pack_to_br00028_csv(csv_header, sue7_pack, csv_delimiter)

    # THEN
    # root_row = f"{sue_str},{event7},{a23_str},{bob_str},,{bob_plan.belief_label},,,,,,,,,1,False,False\n"
    # mop_row = f"{sue_str},{event7},{a23_str},{bob_str},{bob_plan.belief_label},mop,{casa_begin},{casa_close},{casa_addin},{casa_numor},{casa_denom},{casa_morph},{casa_gogo_want},{casa_stop_want},{casa_mass},{casa_task},{casa_problem_bool}\n"
    mop_row = f"{sue_str},{event7},{a23_str},{bob_str},{a23_rope},mop,{casa_begin},{casa_close},{casa_addin},{casa_numor},{casa_denom},{casa_morph},,,{casa_mass},{casa_task},\n"
    casa_row = (
        f"{sue_str},{event7},{a23_str},{bob_str},{a23_rope},casa,,,,,,,,,0,False,\n"
    )
    # print(f"{mop_row=}")
    expected_csv = f"{csv_header}{casa_row}{mop_row}"
    print(f"       {x_csv=}")
    print(f"{expected_csv=}")
    assert len(x_csv) == len(expected_csv)


def test_add_pack_to_br00029_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "amy23"
    bob_plan = planunit_shop(bob_str, a23_str)
    bob_plan.credor_respect = 444
    bob_plan.debtor_respect = 556
    bob_plan.fund_pool = 999
    bob_plan.max_tree_traverse = 3
    bob_plan.tally = 10
    bob_plan.fund_iota = 3
    bob_plan.penny = 13
    bob_plan.respect_bit = 2
    bob_plandelta = plandelta_shop()
    bob_plandelta.add_all_planatoms(bob_plan)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_plandelta(bob_plandelta)
    csv_header = x_ideas.get("br00029")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_pack_to_br00029_csv(csv_header, sue7_pack, csv_delimiter)

    # THEN
    plan_row = f"{sue_str},{event7},{a23_str},{bob_str},{bob_plan.credor_respect},{bob_plan.debtor_respect},{bob_plan.fund_pool},,{bob_plan.tally},{bob_plan.fund_iota},,{bob_plan.respect_bit}\n"
    assert x_csv == f"{csv_header}{plan_row}"


def test_add_packunit_to_stance_csv_strs_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    yao_str = "Yao"
    a23_str = "amy23"
    bob_plan = planunit_shop(bob_str, a23_str)
    bob_plan.add_acctunit(yao_str)
    mop_rope = bob_plan.make_l1_rope("mop")
    casa_rope = bob_plan.make_l1_rope("casa")
    clean_rope = bob_plan.make_rope(casa_rope, "clean")
    bob_plan.add_concept(mop_rope)
    bob_plan.add_concept(casa_rope)
    bob_plan.add_concept(clean_rope)
    bob_plan.edit_concept_attr(
        mop_rope, reason_rcontext=casa_rope, reason_premise=clean_rope
    )
    bob_plan.add_concept(casa_rope)
    bob_plan.edit_concept_attr(casa_rope, awardlink=awardlink_shop(yao_str))
    bob_plan.add_fact(casa_rope, clean_rope)
    bob_plan.credor_respect = 444
    bob_plan.debtor_respect = 556
    bob_plan.fund_pool = 999
    bob_plan.max_tree_traverse = 3
    bob_plan.tally = 10
    bob_plan.fund_iota = 3
    bob_plan.penny = 13
    bob_plan.respect_bit = 2
    bob_plandelta = plandelta_shop()
    bob_plandelta.add_all_planatoms(bob_plan)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_plandelta(bob_plandelta)

    br00020_header = x_ideas.get("br00020")
    br00021_header = x_ideas.get("br00021")
    br00022_header = x_ideas.get("br00022")
    br00023_header = x_ideas.get("br00023")
    br00024_header = x_ideas.get("br00024")
    br00025_header = x_ideas.get("br00025")
    br00026_header = x_ideas.get("br00026")
    br00027_header = x_ideas.get("br00027")
    br00028_header = x_ideas.get("br00028")
    br00029_header = x_ideas.get("br00029")

    # WHEN
    add_packunit_to_stance_csv_strs(sue7_pack, x_ideas, csv_delimiter)

    # THEN
    assert x_ideas.get("br00020") != br00020_header
    assert x_ideas.get("br00021") != br00021_header
    assert x_ideas.get("br00022") != br00022_header
    assert x_ideas.get("br00023") != br00023_header
    # assert x_ideas.get("br00024") != br00024_header
    # assert x_ideas.get("br00025") != br00025_header
    assert x_ideas.get("br00026") != br00026_header
    assert x_ideas.get("br00027") != br00027_header
    assert x_ideas.get("br00028") != br00028_header
    assert x_ideas.get("br00029") != br00029_header
