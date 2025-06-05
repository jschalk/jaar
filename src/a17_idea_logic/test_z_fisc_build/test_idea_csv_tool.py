from copy import deepcopy as copy_deepcopy
from src.a00_data_toolbox.file_toolbox import create_path
from src.a01_term_logic.way import to_way
from src.a03_group_logic.group import awardlink_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a09_pack_logic.delta import buddelta_shop
from src.a09_pack_logic.pack import packunit_shop
from src.a16_pidgin_logic.pidgin import pidginunit_shop
from src.a17_idea_logic._test_util.a17_env import env_dir_setup_cleanup, idea_fiscs_dir
from src.a17_idea_logic._test_util.idea_df_examples import (  # get_ex2_br00006_df,
    get_ex2_br00000_df,
    get_ex2_br00001_df,
    get_ex2_br00002_df,
    get_ex2_br00003_df,
    get_ex2_br00004_df,
    get_ex2_br00005_df,
)
from src.a17_idea_logic.idea import fisc_build_from_df
from src.a17_idea_logic.idea_csv_tool import (
    add_bud_to_br00020_csv,
    add_bud_to_br00021_csv,
    add_bud_to_br00022_csv,
    add_bud_to_br00023_csv,
    add_bud_to_br00024_csv,
    add_bud_to_br00025_csv,
    add_bud_to_br00026_csv,
    add_bud_to_br00027_csv,
    add_bud_to_br00028_csv,
    add_bud_to_br00029_csv,
    add_budunit_to_stance_csv_strs,
    add_fiscunit_to_stance_csv_strs,
    add_fiscunits_to_stance_csv_strs,
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
    add_to_br00042_csv,
    add_to_br00043_csv,
    add_to_br00044_csv,
    add_to_br00045_csv,
    create_init_stance_idea_csv_strs,
)
from src.a17_idea_logic.idea_db_tool import get_ordered_csv


def test_create_init_stance_idea_csv_strs_ReturnsObj_Scenario0_EmptyFiscUnit(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    csv_delimiter = ","

    # WHEN
    x_ideas = create_init_stance_idea_csv_strs()

    # THEN
    expected_stance_csv_strs = {
        "br00000": "fisc_label,timeline_label,c400_number,yr1_jan1_offset,monthday_distortion,fund_iota,penny,respect_bit,bridge,job_listen_rotations\n",
        "br00001": "fisc_label,owner_name,deal_time,quota,celldepth\n",
        "br00002": "fisc_label,owner_name,acct_name,tran_time,amount\n",
        "br00003": "fisc_label,cumlative_minute,hour_label\n",
        "br00004": "fisc_label,cumlative_day,month_label\n",
        "br00005": "fisc_label,weekday_order,weekday_label\n",
        # "br00006": "fisc_label,offi_time,_offi_time_max\n",
        "br00020": "fisc_label,owner_name,acct_name,group_title,credit_vote,debtit_vote\n",
        "br00021": "fisc_label,owner_name,acct_name,credit_belief,debtit_belief\n",
        "br00022": "fisc_label,owner_name,concept_way,awardee_title,give_force,take_force\n",
        "br00023": "fisc_label,owner_name,concept_way,fcontext,fstate,fopen,fnigh\n",
        "br00024": "fisc_label,owner_name,concept_way,labor_title\n",
        "br00025": "fisc_label,owner_name,concept_way,healer_name\n",
        "br00026": "fisc_label,owner_name,concept_way,rcontext,pstate,pnigh,popen,pdivisor\n",
        "br00027": "fisc_label,owner_name,concept_way,rcontext,rconcept_active_requisite\n",
        "br00028": "fisc_label,owner_name,concept_way,begin,close,addin,numor,denom,morph,gogo_want,stop_want,mass,pledge,problem_bool\n",
        "br00029": "fisc_label,owner_name,credor_respect,debtor_respect,fund_pool,max_tree_traverse,tally,fund_iota,penny,respect_bit\n",
        "br00042": "otx_title,inx_title,otx_bridge,inx_bridge,unknown_str\n",
        "br00043": "otx_name,inx_name,otx_bridge,inx_bridge,unknown_str\n",
        "br00044": "otx_label,inx_label,otx_bridge,inx_bridge,unknown_str\n",
        "br00045": "otx_way,inx_way,otx_bridge,inx_bridge,unknown_str\n",
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


def test_add_fiscunit_to_stance_csv_strs_ReturnsObj_Scenario0_OneFiscUnit(
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
    x_fiscs_dir = create_path(idea_fiscs_dir(), "fizz")
    x_fiscunits = fisc_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_iota,
        x_respect_bit,
        x_penny,
        x_fiscs_dir,
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
    a23_fiscunit = x_fiscunits.get("accord23")

    # WHEN
    add_fiscunit_to_stance_csv_strs(a23_fiscunit, x_csvs, csv_delimiter)

    # THEN
    gen_br00000_csv = x_csvs.get("br00000")
    gen_br00001_csv = x_csvs.get("br00001")
    gen_br00002_csv = x_csvs.get("br00002")
    gen_br00003_csv = x_csvs.get("br00003")
    gen_br00004_csv = x_csvs.get("br00004")
    gen_br00005_csv = x_csvs.get("br00005")
    # gen_br00006_csv = x_csvs.get("br00006")
    expected_br00000_csv = ",,accord23,creg,7,440640,1,1,1,1,/,4\n"
    expected_br00001_csv = (
        ",,accord23,Bob,999,332,3\n,,accord23,Sue,777,445,3\n,,accord23,Yao,222,700,3\n"
    )
    expected_br00002_csv = ",,accord23,Bob,Zia,777,888\n,,accord23,Sue,Zia,999,234\n,,accord23,Yao,Zia,999,234\n,,accord23,Zia,Bob,777,888\n"
    expected_br00003_csv = ",,accord23,60,0-12am\n,,accord23,120,1-1am\n,,accord23,180,2-2am\n,,accord23,240,3-3am\n,,accord23,300,4-4am\n,,accord23,360,5-5am\n,,accord23,420,6-6am\n,,accord23,480,7-7am\n,,accord23,540,8-8am\n,,accord23,600,9-9am\n,,accord23,660,10-10am\n,,accord23,720,11-11am\n,,accord23,780,12-12pm\n,,accord23,840,13-1pm\n,,accord23,900,14-2pm\n,,accord23,960,15-3pm\n,,accord23,1020,16-4pm\n,,accord23,1080,17-5pm\n,,accord23,1140,18-6pm\n,,accord23,1200,19-7pm\n,,accord23,1260,20-8pm\n,,accord23,1320,21-9pm\n,,accord23,1380,22-10pm\n,,accord23,1440,23-11pm\n"
    expected_br00004_csv = ",,accord23,31,March\n,,accord23,61,April\n,,accord23,92,May\n,,accord23,122,June\n,,accord23,153,July\n,,accord23,184,August\n,,accord23,214,September\n,,accord23,245,October\n,,accord23,275,November\n,,accord23,306,December\n,,accord23,337,January\n,,accord23,365,February\n"
    expected_br00005_csv = ",,accord23,0,Wednesday\n,,accord23,1,Thursday\n,,accord23,2,Friday\n,,accord23,3,Saturday\n,,accord23,4,Sunday\n,,accord23,5,Monday\n,,accord23,6,Tuesday\n"
    # expected_br00006_csv = ",,accord23,0,Wednesday\n,,accord23,1,Thursday\n,,accord23,2,Friday\n,,accord23,3,Saturday\n,,accord23,4,Sunday\n,,accord23,5,Monday\n,,accord23,6,Tuesday\n"

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


def test_add_fiscunits_to_stance_csv_strs_ReturnsObj_Scenario1_TwoFiscUnits(
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
    x_fiscs_dir = create_path(idea_fiscs_dir(), "fizz")
    x_fiscunits = fisc_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_iota,
        x_respect_bit,
        x_penny,
        x_fiscs_dir,
    )
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()

    # WHEN
    add_fiscunits_to_stance_csv_strs(x_fiscunits, x_ideas, csv_delimiter)

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
    expected_br00000_csv = expected_br00000_csv.replace("accord", ",,accord")
    expected_br00001_csv = expected_br00001_csv.replace("accord", ",,accord")
    expected_br00002_csv = expected_br00002_csv.replace("accord", ",,accord")
    expected_br00003_csv = expected_br00003_csv.replace("accord", ",,accord")
    expected_br00004_csv = expected_br00004_csv.replace("accord", ",,accord")
    expected_br00005_csv = expected_br00005_csv.replace("accord", ",,accord")
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


def test_add_bud_to_br00020_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    yao_str = "Yao"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    bob_bud.add_acctunit(yao_str)
    run_str = ";Run"
    run_credit = 33
    run_debtit = 55
    bob_bud.get_acct(yao_str).add_membership(run_str, run_credit, run_debtit)
    csv_header = x_ideas.get("br00020")

    # WHEN
    x_csv = add_bud_to_br00020_csv(csv_header, bob_bud, csv_delimiter)

    # THEN
    yao_yao_row = f",,{a23_str},{bob_str},{yao_str},{yao_str},1,1\n"
    yao_run_row = (
        f",,{a23_str},{bob_str},{yao_str},{run_str},{run_credit},{run_debtit}\n"
    )
    print(f"{x_csv=}")
    print(f"{yao_run_row=}")
    assert x_csv == f"{csv_header}{yao_yao_row}{yao_run_row}"


def test_add_bud_to_br00021_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    yao_str = "Yao"
    yao_credit = 33
    yao_debtit = 55
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    bob_bud.add_acctunit(yao_str, yao_credit, yao_debtit)
    csv_header = x_ideas.get("br00021")

    # WHEN
    x_csv = add_bud_to_br00021_csv(csv_header, bob_bud, csv_delimiter)

    # THEN
    yao_row = f",,{a23_str},{bob_str},{yao_str},{yao_credit},{yao_debtit}\n"
    assert x_csv == f"{csv_header}{yao_row}"


def test_add_bud_to_br00022_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    casa_way = bob_bud.make_l1_way("casa")
    yao_str = "Yao"
    yao_give_force = 55
    yao_take_force = 77
    casa_awardlink = awardlink_shop(yao_str, yao_give_force, yao_take_force)
    bob_bud.add_concept(casa_way)
    bob_bud.edit_concept_attr(casa_way, awardlink=casa_awardlink)
    csv_header = x_ideas.get("br00022")
    print(f"{csv_header=}")

    # WHEN
    bob_bud.settle_bud()
    x_csv = add_bud_to_br00022_csv(csv_header, bob_bud, csv_delimiter)

    # THEN
    yao_award_row = f",,{a23_str},{bob_str},{casa_way},{yao_str},{yao_give_force},{yao_take_force}\n"
    assert x_csv == f"{csv_header}{yao_award_row}"


def test_add_bud_to_br00023_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    a23_way = to_way(a23_str)
    bob_bud = budunit_shop(bob_str, a23_str)
    casa_way = bob_bud.make_l1_way("casa")
    clean_way = bob_bud.make_way(casa_way, "clean")
    clean_fopen = 55
    clean_fnigh = 77
    bob_bud.add_concept(casa_way)
    bob_bud.add_concept(clean_way)
    bob_bud.add_fact(casa_way, clean_way, clean_fopen, clean_fnigh)
    csv_header = x_ideas.get("br00023")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_bud_to_br00023_csv(csv_header, bob_bud, csv_delimiter)

    # THEN
    clean_row = f",,{a23_str},{bob_str},{a23_way},{casa_way},{clean_way},{clean_fopen},{clean_fnigh}\n"
    assert x_csv == f"{csv_header}{clean_row}"


def test_add_bud_to_br00024_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    casa_way = bob_bud.make_l1_way("casa")
    bob_bud.add_concept(casa_way)
    casa_concept = bob_bud.get_concept_obj(casa_way)
    cleaners_str = "cleaners"
    casa_concept.laborunit.set_laborlink(cleaners_str)
    csv_header = x_ideas.get("br00024")
    print(f"{csv_header=}")

    # WHEN
    bob_bud.settle_bud()
    x_csv = add_bud_to_br00024_csv(csv_header, bob_bud, csv_delimiter)

    # THEN
    cleaners_row = f",,{a23_str},{bob_str},{casa_way},{cleaners_str}\n"
    assert x_csv == f"{csv_header}{cleaners_row}"


def test_add_bud_to_br00025_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    casa_way = bob_bud.make_l1_way("casa")
    bob_bud.add_concept(casa_way)
    casa_concept = bob_bud.get_concept_obj(casa_way)
    cleaners_str = "cleaners"
    casa_concept.healerlink.set_healer_name(cleaners_str)
    csv_header = x_ideas.get("br00025")
    print(f"{csv_header=}")

    # WHEN
    bob_bud.settle_bud()
    x_csv = add_bud_to_br00025_csv(csv_header, bob_bud, csv_delimiter)

    # THEN
    cleaners_row = f",,{a23_str},{bob_str},{casa_way},{cleaners_str}\n"
    assert x_csv == f"{csv_header}{cleaners_row}"


def test_add_bud_to_br00026_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    mop_way = bob_bud.make_l1_way("mop")
    casa_way = bob_bud.make_l1_way("casa")
    clean_way = bob_bud.make_way(casa_way, "clean")
    clean_popen = 22
    clean_pnigh = 55
    clean_pdivisor = 77
    bob_bud.add_concept(mop_way)
    bob_bud.add_concept(casa_way)
    bob_bud.add_concept(clean_way)
    bob_bud.edit_concept_attr(
        mop_way,
        reason_rcontext=casa_way,
        reason_premise=clean_way,
        popen=clean_popen,
        reason_pnigh=clean_pnigh,
        pdivisor=clean_pdivisor,
    )
    csv_header = x_ideas.get("br00026")
    print(f"{csv_header=}")

    # WHEN
    bob_bud.settle_bud()
    x_csv = add_bud_to_br00026_csv(csv_header, bob_bud, csv_delimiter)

    # THEN
    mop_row = f",,{a23_str},{bob_str},{mop_way},{casa_way},{clean_way},{clean_popen},{clean_pnigh},{clean_pdivisor}\n"
    assert x_csv == f"{csv_header}{mop_row}"


def test_add_bud_to_br00027_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    mop_way = bob_bud.make_l1_way("mop")
    casa_way = bob_bud.make_l1_way("casa")
    bob_bud.add_concept(mop_way)
    bob_bud.add_concept(casa_way)
    bob_bud.edit_concept_attr(
        mop_way,
        reason_rcontext=casa_way,
        reason_rconcept_active_requisite=True,
    )
    csv_header = x_ideas.get("br00027")
    print(f"{csv_header=}")

    # WHEN
    bob_bud.settle_bud()
    x_csv = add_bud_to_br00027_csv(csv_header, bob_bud, csv_delimiter)

    # THEN
    casa_row = f",,{a23_str},{bob_str},{mop_way},{casa_way},True\n"
    assert x_csv == f"{csv_header}{casa_row}"


def test_add_bud_to_br00028_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    a23_way = to_way(a23_str)
    bob_bud = budunit_shop(bob_str, a23_str)
    mop_way = bob_bud.make_l1_way("mop")
    casa_way = bob_bud.make_l1_way("casa")
    casa_begin = 3
    casa_close = 5
    casa_addin = 7
    casa_numor = 13
    casa_denom = 17
    casa_morph = 27
    casa_gogo_want = 31
    casa_stop_want = 41
    casa_mass = 2
    casa_pledge = False
    casa_problem_bool = False
    bob_bud.add_concept(casa_way)
    bob_bud.add_concept(mop_way)
    bob_bud.edit_concept_attr(
        mop_way,
        begin=casa_begin,
        close=casa_close,
        addin=casa_addin,
        numor=casa_numor,
        denom=casa_denom,
        morph=casa_morph,
        gogo_want=casa_gogo_want,
        stop_want=casa_stop_want,
        mass=casa_mass,
        pledge=casa_pledge,
        problem_bool=casa_problem_bool,
    )
    csv_header = x_ideas.get("br00028")
    print(f"{csv_header=}")

    # WHEN
    bob_bud.settle_bud()
    x_csv = add_bud_to_br00028_csv(csv_header, bob_bud, csv_delimiter)

    # THEN
    root_row = f",,{a23_str},{bob_str},,{a23_way},,,,,,,,,1,False,False\n"
    mop_row = f",,{a23_str},{bob_str},{mop_way},{casa_begin},{casa_close},{casa_addin},{casa_numor},{casa_denom},{casa_morph},{casa_gogo_want},{casa_stop_want},{casa_mass},{casa_pledge},{casa_problem_bool}\n"
    casa_row = f",,{a23_str},{bob_str},{casa_way},,,,,,,,,0,False,False\n"
    # print(f"{mop_row=}")
    expected_csv = f"{csv_header}{mop_row}{casa_row}"
    print(f"       {x_csv=}")
    print(f"{expected_csv=}")
    assert x_csv == expected_csv


def test_add_bud_to_br00029_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    bob_bud.credor_respect = 444
    bob_bud.debtor_respect = 555
    bob_bud.fund_pool = 777
    bob_bud.max_tree_traverse = 3
    bob_bud.tally = 10
    bob_bud.fund_iota = 12
    bob_bud.penny = 13
    bob_bud.respect_bit = 15
    csv_header = x_ideas.get("br00029")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_bud_to_br00029_csv(csv_header, bob_bud, csv_delimiter)

    # THEN
    bud_row = f",,{a23_str},{bob_str},{bob_bud.credor_respect},{bob_bud.debtor_respect},{bob_bud.fund_pool},{bob_bud.max_tree_traverse},{bob_bud.tally},{bob_bud.fund_iota},{bob_bud.penny},{bob_bud.respect_bit}\n"
    assert x_csv == f"{csv_header}{bud_row}"


def test_add_budunit_to_stance_csv_strs_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    yao_str = "Yao"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    bob_bud.add_acctunit(yao_str)
    mop_way = bob_bud.make_l1_way("mop")
    casa_way = bob_bud.make_l1_way("casa")
    clean_way = bob_bud.make_way(casa_way, "clean")
    bob_bud.add_concept(mop_way)
    bob_bud.add_concept(casa_way)
    bob_bud.add_concept(clean_way)
    bob_bud.edit_concept_attr(
        mop_way, reason_rcontext=casa_way, reason_premise=clean_way
    )
    bob_bud.add_concept(casa_way)
    bob_bud.edit_concept_attr(casa_way, awardlink=awardlink_shop(yao_str))
    bob_bud.add_fact(casa_way, clean_way)

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
    bob_bud.settle_bud()
    add_budunit_to_stance_csv_strs(bob_bud, x_ideas, csv_delimiter)

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
    bob_otx_bridge = ";"
    bob_inx_bridge = "/"
    bob_unknown_str = "UNKNOWN"
    bob7_pidginunit = pidginunit_shop(
        bob_str, event7, bob_otx_bridge, bob_inx_bridge, bob_unknown_str
    )
    run_otx = "run"
    run_inx = "cours"
    bob7_pidginunit.set_otx2inx("TitleTerm", run_otx, run_inx)
    csv_header = x_ideas.get("br00042")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_to_br00042_csv(csv_header, bob7_pidginunit, csv_delimiter)

    # THEN
    run_row = f"{bob_str},{event7},{run_otx},{bob_otx_bridge},{run_inx},{bob_inx_bridge},{bob_unknown_str}\n"
    assert x_csv == f"{csv_header}{run_row}"


def test_add_to_br00043_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    event7 = 7
    bob_otx_bridge = ";"
    bob_inx_bridge = "/"
    bob_unknown_str = "UNKNOWN"
    bob7_pidginunit = pidginunit_shop(
        bob_str, event7, bob_otx_bridge, bob_inx_bridge, bob_unknown_str
    )
    yao_otx = "Yao"
    yao_inx = "YaoMing"
    bob7_pidginunit.set_otx2inx("NameTerm", yao_otx, yao_inx)
    csv_header = x_ideas.get("br00043")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_to_br00043_csv(csv_header, bob7_pidginunit, csv_delimiter)

    # THEN
    bob_row = f"{bob_str},{event7},{yao_otx},{bob_otx_bridge},{yao_inx},{bob_inx_bridge},{bob_unknown_str}\n"
    assert x_csv == f"{csv_header}{bob_row}"


def test_add_to_br00044_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    event7 = 7
    bob_otx_bridge = ";"
    bob_inx_bridge = "/"
    bob_unknown_str = "UNKNOWN"
    bob7_pidginunit = pidginunit_shop(
        bob_str, event7, bob_otx_bridge, bob_inx_bridge, bob_unknown_str
    )
    clean_otx = "clean"
    clean_inx = "prope"
    bob7_pidginunit.set_otx2inx("LabelTerm", clean_otx, clean_inx)
    csv_header = x_ideas.get("br00044")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_to_br00044_csv(csv_header, bob7_pidginunit, csv_delimiter)

    # THEN
    bob_row = f"{bob_str},{event7},{clean_otx},{bob_otx_bridge},{clean_inx},{bob_inx_bridge},{bob_unknown_str}\n"
    assert x_csv == f"{csv_header}{bob_row}"


def test_add_to_br00045_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    event7 = 7
    bob_otx_bridge = ";"
    bob_inx_bridge = "/"
    bob_unknown_str = "UNKNOWN"
    bob7_pidginunit = pidginunit_shop(
        bob_str, event7, bob_otx_bridge, bob_inx_bridge, bob_unknown_str
    )
    clean_otx = "clean"
    clean_inx = "prope"
    bob7_pidginunit.set_otx2inx("WayTerm", clean_otx, clean_inx)
    csv_header = x_ideas.get("br00045")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_to_br00045_csv(csv_header, bob7_pidginunit, csv_delimiter)

    # THEN
    bob_row = f"{bob_str},{event7},{clean_otx},{bob_otx_bridge},{clean_inx},{bob_inx_bridge},{bob_unknown_str}\n"
    assert x_csv == f"{csv_header}{bob_row}"


def test_add_pidginunit_to_stance_csv_strs_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    event7 = 7
    bob_otx_bridge = ";"
    bob_inx_bridge = "/"
    bob_unknown_str = "UNKNOWN"
    bob7_pidginunit = pidginunit_shop(
        bob_str, event7, bob_otx_bridge, bob_inx_bridge, bob_unknown_str
    )
    clean_otx = "clean"
    clean_inx = "prope"
    bob7_pidginunit.set_otx2inx("WayTerm", clean_otx, clean_inx)
    yao_otx = "Yao"
    yao_inx = "YaoMing"
    bob7_pidginunit.set_otx2inx("NameTerm", yao_otx, yao_inx)
    run_otx = "run"
    run_inx = "cours"
    bob7_pidginunit.set_otx2inx("TitleTerm", run_otx, run_inx)
    clean_otx = "clean"
    clean_inx = "prope"
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
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    bob_bud.add_acctunit(yao_str)
    run_str = ";Run"
    run_credit = 33
    run_debtit = 55
    bob_bud.get_acct(yao_str).add_membership(run_str, run_credit, run_debtit)
    bob_buddelta = buddelta_shop()
    bob_buddelta.add_all_budatoms(bob_bud)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_buddelta(bob_buddelta)
    csv_header = x_ideas.get("br00020")

    # WHEN
    x_csv = add_pack_to_br00020_csv(csv_header, sue7_pack, csv_delimiter)

    # THEN
    yao_yao_row = f"{sue_str},{event7},{a23_str},{bob_str},{yao_str},{yao_str},1,1\n"
    yao_run_row = f"{sue_str},{event7},{a23_str},{bob_str},{yao_str},{run_str},{run_credit},{run_debtit}\n"
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
    yao_debtit = 55
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    bob_bud.add_acctunit(yao_str, yao_credit, yao_debtit)
    bob_buddelta = buddelta_shop()
    bob_buddelta.add_all_budatoms(bob_bud)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_buddelta(bob_buddelta)
    csv_header = x_ideas.get("br00021")

    # WHEN
    x_csv = add_pack_to_br00021_csv(csv_header, sue7_pack, csv_delimiter)

    # THEN
    yao_row = (
        f"{sue_str},{event7},{a23_str},{bob_str},{yao_str},{yao_credit},{yao_debtit}\n"
    )
    assert x_csv == f"{csv_header}{yao_row}"


def test_add_pack_to_br00022_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    casa_way = bob_bud.make_l1_way("casa")
    yao_str = "Yao"
    yao_give_force = 55
    yao_take_force = 77
    casa_awardlink = awardlink_shop(yao_str, yao_give_force, yao_take_force)
    bob_bud.add_concept(casa_way)
    bob_bud.edit_concept_attr(casa_way, awardlink=casa_awardlink)
    bob_buddelta = buddelta_shop()
    bob_buddelta.add_all_budatoms(bob_bud)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_buddelta(bob_buddelta)
    csv_header = x_ideas.get("br00022")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_pack_to_br00022_csv(csv_header, sue7_pack, csv_delimiter)

    # THEN
    yao_award_row = f"{sue_str},{event7},{a23_str},{bob_str},{casa_way},{yao_str},{yao_give_force},{yao_take_force}\n"
    assert x_csv == f"{csv_header}{yao_award_row}"


def test_add_pack_to_br00023_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    a23_way = to_way(a23_str)
    bob_bud = budunit_shop(bob_str, a23_str)
    casa_way = bob_bud.make_l1_way("casa")
    clean_way = bob_bud.make_way(casa_way, "clean")
    clean_fopen = 55
    clean_fnigh = 77
    bob_bud.add_concept(casa_way)
    bob_bud.add_concept(clean_way)
    bob_bud.add_fact(casa_way, clean_way, clean_fopen, clean_fnigh)
    bob_buddelta = buddelta_shop()
    bob_buddelta.add_all_budatoms(bob_bud)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_buddelta(bob_buddelta)
    csv_header = x_ideas.get("br00023")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_pack_to_br00023_csv(csv_header, sue7_pack, csv_delimiter)

    # THEN
    clean_row = f"{sue_str},{event7},{a23_str},{bob_str},{a23_way},{casa_way},{clean_way},{clean_fopen},{clean_fnigh}\n"
    expected_csv = f"{csv_header}{clean_row}"
    print(f"       {x_csv=}")
    print(f"{expected_csv=}")
    assert x_csv == expected_csv


def test_add_pack_to_br00024_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    casa_way = bob_bud.make_l1_way("casa")
    bob_bud.add_concept(casa_way)
    casa_concept = bob_bud.get_concept_obj(casa_way)
    cleaners_str = "cleaners"
    casa_concept.laborunit.set_laborlink(cleaners_str)
    bob_buddelta = buddelta_shop()
    bob_buddelta.add_all_budatoms(bob_bud)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_buddelta(bob_buddelta)
    csv_header = x_ideas.get("br00024")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_pack_to_br00024_csv(csv_header, sue7_pack, csv_delimiter)

    # THEN
    cleaners_row = f"{sue_str},{event7},{a23_str},{bob_str},{casa_way},{cleaners_str}\n"
    expected_csv = f"{csv_header}{cleaners_row}"
    print(f"       {x_csv=}")
    print(f"{expected_csv=}")
    assert x_csv == f"{csv_header}{cleaners_row}"


def test_add_pack_to_br00025_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    casa_way = bob_bud.make_l1_way("casa")
    bob_bud.add_concept(casa_way)
    casa_concept = bob_bud.get_concept_obj(casa_way)
    cleaners_str = "cleaners"
    casa_concept.healerlink.set_healer_name(cleaners_str)
    bob_buddelta = buddelta_shop()
    bob_buddelta.add_all_budatoms(bob_bud)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_buddelta(bob_buddelta)
    csv_header = x_ideas.get("br00025")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_pack_to_br00025_csv(csv_header, sue7_pack, csv_delimiter)

    # THEN
    cleaners_row = f"{sue_str},{event7},{a23_str},{bob_str},{casa_way},{cleaners_str}\n"
    assert x_csv == f"{csv_header}{cleaners_row}"


def test_add_pack_to_br00026_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    mop_way = bob_bud.make_l1_way("mop")
    casa_way = bob_bud.make_l1_way("casa")
    clean_way = bob_bud.make_way(casa_way, "clean")
    clean_popen = 22
    clean_pnigh = 55
    clean_pdivisor = 77
    bob_bud.add_concept(mop_way)
    bob_bud.add_concept(casa_way)
    bob_bud.add_concept(clean_way)
    bob_bud.edit_concept_attr(
        mop_way,
        reason_rcontext=casa_way,
        reason_premise=clean_way,
        popen=clean_popen,
        reason_pnigh=clean_pnigh,
        pdivisor=clean_pdivisor,
    )
    bob_buddelta = buddelta_shop()
    bob_buddelta.add_all_budatoms(bob_bud)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_buddelta(bob_buddelta)
    csv_header = x_ideas.get("br00026")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_pack_to_br00026_csv(csv_header, sue7_pack, csv_delimiter)

    # THEN
    mop_row = f"{sue_str},{event7},{a23_str},{bob_str},{mop_way},{casa_way},{clean_way},{clean_popen},{clean_pnigh},{clean_pdivisor}\n"
    assert x_csv == f"{csv_header}{mop_row}"


def test_add_pack_to_br00027_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    mop_way = bob_bud.make_l1_way("mop")
    casa_way = bob_bud.make_l1_way("casa")
    bob_bud.add_concept(mop_way)
    bob_bud.add_concept(casa_way)
    bob_bud.edit_concept_attr(
        mop_way,
        reason_rcontext=casa_way,
        reason_rconcept_active_requisite=True,
    )
    bob_buddelta = buddelta_shop()
    bob_buddelta.add_all_budatoms(bob_bud)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_buddelta(bob_buddelta)
    csv_header = x_ideas.get("br00027")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_pack_to_br00027_csv(csv_header, sue7_pack, csv_delimiter)

    # THEN
    casa_row = f"{sue_str},{event7},{a23_str},{bob_str},{mop_way},{casa_way},True\n"
    assert x_csv == f"{csv_header}{casa_row}"


def test_add_pack_to_br00028_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    a23_way = to_way(a23_str)
    bob_bud = budunit_shop(bob_str, a23_str)
    mop_way = bob_bud.make_l1_way("mop")
    casa_way = bob_bud.make_l1_way("casa")
    casa_begin = 3
    casa_close = 5
    casa_addin = 7
    casa_numor = 13
    casa_denom = 17
    casa_morph = 27
    casa_gogo_want = 31
    casa_stop_want = 41
    casa_mass = 2
    casa_pledge = False
    casa_problem_bool = False
    bob_bud.add_concept(casa_way)
    bob_bud.add_concept(mop_way)
    bob_bud.edit_concept_attr(
        mop_way,
        begin=casa_begin,
        close=casa_close,
        addin=casa_addin,
        numor=casa_numor,
        denom=casa_denom,
        morph=casa_morph,
        gogo_want=casa_gogo_want,
        stop_want=casa_stop_want,
        mass=casa_mass,
        pledge=casa_pledge,
        problem_bool=casa_problem_bool,
    )
    bob_buddelta = buddelta_shop()
    bob_buddelta.add_all_budatoms(bob_bud)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_buddelta(bob_buddelta)
    csv_header = x_ideas.get("br00028")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_pack_to_br00028_csv(csv_header, sue7_pack, csv_delimiter)

    # THEN
    # root_row = f"{sue_str},{event7},{a23_str},{bob_str},,{bob_bud.fisc_label},,,,,,,,,1,False,False\n"
    # mop_row = f"{sue_str},{event7},{a23_str},{bob_str},{bob_bud.fisc_label},mop,{casa_begin},{casa_close},{casa_addin},{casa_numor},{casa_denom},{casa_morph},{casa_gogo_want},{casa_stop_want},{casa_mass},{casa_pledge},{casa_problem_bool}\n"
    mop_row = f"{sue_str},{event7},{a23_str},{bob_str},{a23_way},mop,{casa_begin},{casa_close},{casa_addin},{casa_numor},{casa_denom},{casa_morph},,,{casa_mass},{casa_pledge},\n"
    casa_row = (
        f"{sue_str},{event7},{a23_str},{bob_str},{a23_way},casa,,,,,,,,,0,False,\n"
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
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    bob_bud.credor_respect = 444
    bob_bud.debtor_respect = 556
    bob_bud.fund_pool = 999
    bob_bud.max_tree_traverse = 3
    bob_bud.tally = 10
    bob_bud.fund_iota = 3
    bob_bud.penny = 13
    bob_bud.respect_bit = 2
    bob_buddelta = buddelta_shop()
    bob_buddelta.add_all_budatoms(bob_bud)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_buddelta(bob_buddelta)
    csv_header = x_ideas.get("br00029")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_pack_to_br00029_csv(csv_header, sue7_pack, csv_delimiter)

    # THEN
    bud_row = f"{sue_str},{event7},{a23_str},{bob_str},{bob_bud.credor_respect},{bob_bud.debtor_respect},{bob_bud.fund_pool},,{bob_bud.tally},{bob_bud.fund_iota},,{bob_bud.respect_bit}\n"
    assert x_csv == f"{csv_header}{bud_row}"


def test_add_packunit_to_stance_csv_strs_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    bob_str = "Bob"
    yao_str = "Yao"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    bob_bud.add_acctunit(yao_str)
    mop_way = bob_bud.make_l1_way("mop")
    casa_way = bob_bud.make_l1_way("casa")
    clean_way = bob_bud.make_way(casa_way, "clean")
    bob_bud.add_concept(mop_way)
    bob_bud.add_concept(casa_way)
    bob_bud.add_concept(clean_way)
    bob_bud.edit_concept_attr(
        mop_way, reason_rcontext=casa_way, reason_premise=clean_way
    )
    bob_bud.add_concept(casa_way)
    bob_bud.edit_concept_attr(casa_way, awardlink=awardlink_shop(yao_str))
    bob_bud.add_fact(casa_way, clean_way)
    bob_bud.credor_respect = 444
    bob_bud.debtor_respect = 556
    bob_bud.fund_pool = 999
    bob_bud.max_tree_traverse = 3
    bob_bud.tally = 10
    bob_bud.fund_iota = 3
    bob_bud.penny = 13
    bob_bud.respect_bit = 2
    bob_buddelta = buddelta_shop()
    bob_buddelta.add_all_budatoms(bob_bud)
    sue_str = "Sue"
    event7 = 7
    sue7_pack = packunit_shop(bob_str, sue_str, a23_str, event_int=event7)
    sue7_pack.set_buddelta(bob_buddelta)

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
