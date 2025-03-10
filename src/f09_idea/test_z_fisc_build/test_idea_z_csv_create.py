from src.f00_instrument.file import create_path
from src.f02_bud.group import awardlink_shop
from src.f02_bud.bud import budunit_shop
from src.f03_chrono.examples.chrono_examples import get_five_config
from src.f03_chrono.chrono import timelineunit_shop, get_default_timeline_config_dict
from src.f07_fisc.fisc import fiscunit_shop
from src.f09_idea.idea_config import get_idea_format_filename
from src.f09_idea.idea import (
    fisc_build_from_df,
    create_init_stance_idea_brick_csv_strs,
    add_fiscunit_to_stance_csv_strs,
    add_fiscunits_to_stance_csv_strs,
    add_to_br00020_csv,
    add_to_br00021_csv,
    add_to_br00022_csv,
    add_to_br00023_csv,
    add_to_br00024_csv,
    add_to_br00025_csv,
    add_to_br00026_csv,
    add_to_br00027_csv,
    add_to_br00028_csv,
    add_to_br00029_csv,
    add_budunit_to_stance_csv_strs,
)
from src.f09_idea.idea_db_tool import get_ordered_csv
from src.f09_idea.examples.idea_env import idea_fiscs_dir, idea_env_setup_cleanup
from src.f09_idea.examples.idea_df_examples import (
    get_ex1_br00000_df,
    get_ex1_br00001_df,
    get_ex1_br00002_df,
    get_ex1_br00003_df,
    get_ex1_br00004_df,
    get_ex1_br00005_df,
    get_ex2_br00000_df,
    get_ex2_br00001_df,
    get_ex2_br00002_df,
    get_ex2_br00003_df,
    get_ex2_br00004_df,
    get_ex2_br00005_df,
)


def test_create_init_stance_idea_brick_csv_strs_ReturnsObj_Scenario0_EmptyFiscUnit(
    idea_env_setup_cleanup,
):
    # ESTABLISH
    csv_delimiter = ","

    # WHEN
    x_ideabricks = create_init_stance_idea_brick_csv_strs()

    # THEN
    expected_stance_csv_strs = {
        "br00000": "fisc_title,timeline_title,c400_number,yr1_jan1_offset,monthday_distortion,fund_coin,penny,respect_bit,present_time,bridge\n",
        "br00001": "fisc_title,owner_name,time_int,quota,celldepth\n",
        "br00002": "fisc_title,owner_name,acct_name,time_int,amount\n",
        "br00003": "fisc_title,cumlative_minute,hour_title\n",
        "br00004": "fisc_title,cumlative_day,month_title\n",
        "br00005": "fisc_title,weekday_order,weekday_title\n",
        "br00020": "fisc_title,owner_name,acct_name,group_label,credit_vote,debtit_vote\n",
        "br00021": "fisc_title,owner_name,acct_name,credit_belief,debtit_belief\n",
        "br00022": "fisc_title,owner_name,road,awardee_tag,give_force,take_force\n",
        "br00023": "fisc_title,owner_name,road,base,pick,fopen,fnigh\n",
        "br00024": "fisc_title,owner_name,road,team_tag\n",
        "br00025": "fisc_title,owner_name,road,healer_name\n",
        "br00026": "fisc_title,owner_name,road,base,need,nigh,open,divisor\n",
        "br00027": "fisc_title,owner_name,road,base,base_item_active_requisite\n",
        "br00028": "fisc_title,owner_name,parent_road,item_title,begin,close,addin,numor,denom,morph,gogo_want,stop_want,mass,pledge,problem_bool\n",
        "br00029": "fisc_title,owner_name,credor_respect,debtor_respect,fund_pool,max_tree_traverse,tally,fund_coin,penny,respect_bit\n",
        "br00042": "otx_label,inx_label,otx_bridge,inx_bridge,unknown_word\n",
        "br00043": "otx_name,inx_name,otx_bridge,inx_bridge,unknown_word\n",
        "br00044": "otx_title,inx_title,otx_bridge,inx_bridge,unknown_word\n",
        "br00045": "otx_road,inx_road,otx_bridge,inx_bridge,unknown_word\n",
    }
    expected_br00000_csv = expected_stance_csv_strs.get("br00000")
    expected_br00001_csv = expected_stance_csv_strs.get("br00001")
    expected_br00002_csv = expected_stance_csv_strs.get("br00002")
    expected_br00003_csv = expected_stance_csv_strs.get("br00003")
    expected_br00004_csv = expected_stance_csv_strs.get("br00004")
    expected_br00005_csv = expected_stance_csv_strs.get("br00005")
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

    assert x_ideabricks.get("br00000") == expected_br00000_csv
    assert x_ideabricks.get("br00001") == expected_br00001_csv
    assert x_ideabricks.get("br00002") == expected_br00002_csv
    assert x_ideabricks.get("br00003") == expected_br00003_csv
    assert x_ideabricks.get("br00004") == expected_br00004_csv
    assert x_ideabricks.get("br00005") == expected_br00005_csv
    print(f"{expected_br00020_csv=}")
    print(x_ideabricks.get("br00020"))
    assert x_ideabricks.get("br00020") == expected_br00020_csv
    assert x_ideabricks.get("br00021") == expected_br00021_csv
    assert x_ideabricks.get("br00022") == expected_br00022_csv
    assert x_ideabricks.get("br00023") == expected_br00023_csv
    assert x_ideabricks.get("br00024") == expected_br00024_csv
    assert x_ideabricks.get("br00025") == expected_br00025_csv
    assert x_ideabricks.get("br00026") == expected_br00026_csv
    assert x_ideabricks.get("br00027") == expected_br00027_csv
    assert x_ideabricks.get("br00028") == expected_br00028_csv
    assert x_ideabricks.get("br00029") == expected_br00029_csv
    assert x_ideabricks.get("br00042") == expected_br00042_csv
    assert x_ideabricks.get("br00043") == expected_br00043_csv
    assert x_ideabricks.get("br00044") == expected_br00044_csv
    assert x_ideabricks.get("br00045") == expected_br00045_csv
    assert len(x_ideabricks) == 20


def test_add_fiscunit_to_stance_csv_strs_ReturnsObj_Scenario0_OneFiscUnit(
    idea_env_setup_cleanup,
):
    # ESTABLISH
    br00000_df = get_ex2_br00000_df()
    br00001_df = get_ex2_br00001_df()
    br00002_df = get_ex2_br00002_df()
    br00003_df = get_ex2_br00003_df()
    br00004_df = get_ex2_br00004_df()
    br00005_df = get_ex2_br00005_df()
    x_fund_coin = 1
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
        x_fund_coin,
        x_respect_bit,
        x_penny,
        x_fiscs_dir,
    )
    csv_delimiter = ","
    x_csvs = create_init_stance_idea_brick_csv_strs()
    br00_csv_header = x_csvs.get("br00000")
    br01_csv_header = x_csvs.get("br00001")
    br02_csv_header = x_csvs.get("br00002")
    br03_csv_header = x_csvs.get("br00003")
    br04_csv_header = x_csvs.get("br00004")
    br05_csv_header = x_csvs.get("br00005")
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
    expected_br00000_csv = "accord23,creg,7,440640,1,1,1,1,5500,/\n"
    expected_br00001_csv = (
        "accord23,Bob,999,332,3\naccord23,Sue,777,445,3\naccord23,Yao,222,700,3\n"
    )
    expected_br00002_csv = "accord23,Bob,Zia,777,888\naccord23,Sue,Zia,999,234\naccord23,Yao,Zia,999,234\naccord23,Zia,Bob,777,888\n"
    expected_br00003_csv = "accord23,60,0-12am\naccord23,120,1-1am\naccord23,180,2-2am\naccord23,240,3-3am\naccord23,300,4-4am\naccord23,360,5-5am\naccord23,420,6-6am\naccord23,480,7-7am\naccord23,540,8-8am\naccord23,600,9-9am\naccord23,660,10-10am\naccord23,720,11-11am\naccord23,780,12-12pm\naccord23,840,13-1pm\naccord23,900,14-2pm\naccord23,960,15-3pm\naccord23,1020,16-4pm\naccord23,1080,17-5pm\naccord23,1140,18-6pm\naccord23,1200,19-7pm\naccord23,1260,20-8pm\naccord23,1320,21-9pm\naccord23,1380,22-10pm\naccord23,1440,23-11pm\n"
    expected_br00004_csv = "accord23,31,March\naccord23,61,April\naccord23,92,May\naccord23,122,June\naccord23,153,July\naccord23,184,August\naccord23,214,September\naccord23,245,October\naccord23,275,November\naccord23,306,December\naccord23,337,January\naccord23,365,February\n"
    expected_br00005_csv = "accord23,0,Wednesday\naccord23,1,Thursday\naccord23,2,Friday\naccord23,3,Saturday\naccord23,4,Sunday\naccord23,5,Monday\naccord23,6,Tuesday\n"

    print(f"      {br01_csv_header=}")
    print(f" {expected_br00005_csv=}")
    print(f"      {gen_br00005_csv=}")
    assert gen_br00000_csv == f"{br00_csv_header}{expected_br00000_csv}"
    assert gen_br00001_csv == f"{br01_csv_header}{expected_br00001_csv}"
    assert gen_br00002_csv == f"{br02_csv_header}{expected_br00002_csv}"
    assert gen_br00003_csv == f"{br03_csv_header}{expected_br00003_csv}"
    assert gen_br00004_csv == f"{br04_csv_header}{expected_br00004_csv}"
    assert gen_br00005_csv == f"{br05_csv_header}{expected_br00005_csv}"


def test_add_fiscunits_to_stance_csv_strs_ReturnsObj_Scenario1_TwoFiscUnits(
    idea_env_setup_cleanup,
):
    # ESTABLISH
    br00000_df = get_ex2_br00000_df()
    br00001_df = get_ex2_br00001_df()
    br00002_df = get_ex2_br00002_df()
    br00003_df = get_ex2_br00003_df()
    br00004_df = get_ex2_br00004_df()
    br00005_df = get_ex2_br00005_df()
    x_fund_coin = 1
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
        x_fund_coin,
        x_respect_bit,
        x_penny,
        x_fiscs_dir,
    )
    csv_delimiter = ","
    x_ideabricks = create_init_stance_idea_brick_csv_strs()

    # WHEN
    add_fiscunits_to_stance_csv_strs(x_fiscunits, x_ideabricks, csv_delimiter)

    # THEN
    expected_br00000_csv = get_ordered_csv(get_ex2_br00000_df())
    expected_br00001_csv = get_ordered_csv(get_ex2_br00001_df())
    expected_br00002_csv = get_ordered_csv(get_ex2_br00002_df())
    expected_br00003_csv = get_ordered_csv(get_ex2_br00003_df())
    expected_br00004_csv = get_ordered_csv(get_ex2_br00004_df())
    expected_br00005_csv = get_ordered_csv(get_ex2_br00005_df())

    assert len(x_ideabricks) == 20
    generated_br00000_csv = x_ideabricks.get("br00000")
    generated_br00001_csv = x_ideabricks.get("br00001")
    generated_br00002_csv = x_ideabricks.get("br00002")
    generated_br00003_csv = x_ideabricks.get("br00003")
    generated_br00004_csv = x_ideabricks.get("br00004")
    generated_br00005_csv = x_ideabricks.get("br00005")
    generated_br00020_csv = x_ideabricks.get("br00020")
    generated_br00021_csv = x_ideabricks.get("br00021")
    generated_br00022_csv = x_ideabricks.get("br00022")
    generated_br00023_csv = x_ideabricks.get("br00023")
    generated_br00024_csv = x_ideabricks.get("br00024")
    generated_br00025_csv = x_ideabricks.get("br00025")
    generated_br00026_csv = x_ideabricks.get("br00026")
    generated_br00027_csv = x_ideabricks.get("br00027")
    generated_br00028_csv = x_ideabricks.get("br00028")
    generated_br00029_csv = x_ideabricks.get("br00029")
    generated_br00042_csv = x_ideabricks.get("br00042")
    generated_br00043_csv = x_ideabricks.get("br00043")
    generated_br00044_csv = x_ideabricks.get("br00044")
    generated_br00045_csv = x_ideabricks.get("br00045")

    # print(f" {expected_br00005_csv=}")
    # print(f"{generated_br00005_csv=}")
    assert generated_br00000_csv == expected_br00000_csv
    assert generated_br00001_csv == expected_br00001_csv
    assert generated_br00002_csv == expected_br00002_csv
    assert len(generated_br00003_csv) == len(expected_br00003_csv)
    assert generated_br00004_csv == expected_br00004_csv
    assert generated_br00005_csv == expected_br00005_csv


def test_add_to_br00020_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideabricks = create_init_stance_idea_brick_csv_strs()
    bob_str = "Bob"
    yao_str = "Yao"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    bob_bud.add_acctunit(yao_str)
    run_str = ";Run"
    run_credit = 33
    run_debtit = 55
    bob_bud.get_acct(yao_str).add_membership(run_str, run_credit, run_debtit)
    csv_header = x_ideabricks.get("br00020")

    # WHEN
    x_csv = add_to_br00020_csv(csv_header, bob_bud, csv_delimiter)

    # THEN
    yao_yao_row = f"{a23_str},{bob_str},{yao_str},{yao_str},1,1\n"
    yao_run_row = f"{a23_str},{bob_str},{yao_str},{run_str},{run_credit},{run_debtit}\n"
    print(f"{x_csv=}")
    print(f"{yao_run_row=}")
    assert x_csv == f"{csv_header}{yao_yao_row}{yao_run_row}"


def test_add_to_br00021_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideabricks = create_init_stance_idea_brick_csv_strs()
    bob_str = "Bob"
    yao_str = "Yao"
    yao_credit = 33
    yao_debtit = 55
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    bob_bud.add_acctunit(yao_str, yao_credit, yao_debtit)
    csv_header = x_ideabricks.get("br00021")

    # WHEN
    x_csv = add_to_br00021_csv(csv_header, bob_bud, csv_delimiter)

    # THEN
    yao_row = f"{a23_str},{bob_str},{yao_str},{yao_credit},{yao_debtit}\n"
    assert x_csv == f"{csv_header}{yao_row}"


def test_add_to_br00022_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideabricks = create_init_stance_idea_brick_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    casa_road = bob_bud.make_l1_road("casa")
    yao_str = "Yao"
    yao_give_force = 55
    yao_take_force = 77
    casa_awardlink = awardlink_shop(yao_str, yao_give_force, yao_take_force)
    bob_bud.add_item(casa_road)
    bob_bud.edit_item_attr(casa_road, awardlink=casa_awardlink)
    csv_header = x_ideabricks.get("br00022")
    print(f"{csv_header=}")

    # WHEN
    bob_bud.settle_bud()
    x_csv = add_to_br00022_csv(csv_header, bob_bud, csv_delimiter)

    # THEN
    yao_award_row = (
        f"{a23_str},{bob_str},{casa_road},{yao_str},{yao_give_force},{yao_take_force}\n"
    )
    assert x_csv == f"{csv_header}{yao_award_row}"


def test_add_to_br00023_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideabricks = create_init_stance_idea_brick_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    casa_road = bob_bud.make_l1_road("casa")
    clean_road = bob_bud.make_road(casa_road, "clean")
    clean_fopen = 55
    clean_fnigh = 77
    bob_bud.add_item(casa_road)
    bob_bud.add_item(clean_road)
    bob_bud.add_fact(casa_road, clean_road, clean_fopen, clean_fnigh)
    csv_header = x_ideabricks.get("br00023")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_to_br00023_csv(csv_header, bob_bud, csv_delimiter)

    # THEN
    clean_row = (
        f"{a23_str},{bob_str},{casa_road},{clean_road},{clean_fopen},{clean_fnigh}\n"
    )
    assert x_csv == f"{csv_header}{clean_row}"


def test_add_to_br00024_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideabricks = create_init_stance_idea_brick_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    casa_road = bob_bud.make_l1_road("casa")
    bob_bud.add_item(casa_road)
    casa_item = bob_bud.get_item_obj(casa_road)
    cleaners_str = "cleaners"
    casa_item.teamunit.set_teamlink(cleaners_str)
    csv_header = x_ideabricks.get("br00024")
    print(f"{csv_header=}")

    # WHEN
    bob_bud.settle_bud()
    x_csv = add_to_br00024_csv(csv_header, bob_bud, csv_delimiter)

    # THEN
    cleaners_row = f"{a23_str},{bob_str},{casa_road},{cleaners_str}\n"
    assert x_csv == f"{csv_header}{cleaners_row}"


def test_add_to_br00025_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideabricks = create_init_stance_idea_brick_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    casa_road = bob_bud.make_l1_road("casa")
    bob_bud.add_item(casa_road)
    casa_item = bob_bud.get_item_obj(casa_road)
    cleaners_str = "cleaners"
    casa_item.healerlink.set_healer_name(cleaners_str)
    csv_header = x_ideabricks.get("br00025")
    print(f"{csv_header=}")

    # WHEN
    bob_bud.settle_bud()
    x_csv = add_to_br00025_csv(csv_header, bob_bud, csv_delimiter)

    # THEN
    cleaners_row = f"{a23_str},{bob_str},{casa_road},{cleaners_str}\n"
    assert x_csv == f"{csv_header}{cleaners_row}"


def test_add_to_br00026_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideabricks = create_init_stance_idea_brick_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    mop_road = bob_bud.make_l1_road("mop")
    casa_road = bob_bud.make_l1_road("casa")
    clean_road = bob_bud.make_road(casa_road, "clean")
    clean_premise_open = 22
    clean_premise_nigh = 55
    clean_premise_divisor = 77
    bob_bud.add_item(mop_road)
    bob_bud.add_item(casa_road)
    bob_bud.add_item(clean_road)
    bob_bud.edit_item_attr(
        mop_road,
        reason_base=casa_road,
        reason_premise=clean_road,
        reason_premise_open=clean_premise_open,
        reason_premise_nigh=clean_premise_nigh,
        reason_premise_divisor=clean_premise_divisor,
    )
    csv_header = x_ideabricks.get("br00026")
    print(f"{csv_header=}")

    # WHEN
    bob_bud.settle_bud()
    x_csv = add_to_br00026_csv(csv_header, bob_bud, csv_delimiter)

    # THEN
    mop_row = f"{a23_str},{bob_str},{mop_road},{casa_road},{clean_road},{clean_premise_open},{clean_premise_nigh},{clean_premise_divisor}\n"
    assert x_csv == f"{csv_header}{mop_row}"


def test_add_to_br00027_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideabricks = create_init_stance_idea_brick_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    mop_road = bob_bud.make_l1_road("mop")
    casa_road = bob_bud.make_l1_road("casa")
    bob_bud.add_item(mop_road)
    bob_bud.add_item(casa_road)
    bob_bud.edit_item_attr(
        mop_road,
        reason_base=casa_road,
        reason_base_item_active_requisite=True,
    )
    csv_header = x_ideabricks.get("br00027")
    print(f"{csv_header=}")

    # WHEN
    bob_bud.settle_bud()
    x_csv = add_to_br00027_csv(csv_header, bob_bud, csv_delimiter)

    # THEN
    casa_row = f"{a23_str},{bob_str},{mop_road},{casa_road},True\n"
    assert x_csv == f"{csv_header}{casa_row}"


def test_add_to_br00028_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideabricks = create_init_stance_idea_brick_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    mop_road = bob_bud.make_l1_road("mop")
    casa_road = bob_bud.make_l1_road("casa")
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
    bob_bud.add_item(casa_road)
    bob_bud.add_item(mop_road)
    bob_bud.edit_item_attr(
        mop_road,
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
    csv_header = x_ideabricks.get("br00028")
    print(f"{csv_header=}")

    # WHEN
    bob_bud.settle_bud()
    x_csv = add_to_br00028_csv(csv_header, bob_bud, csv_delimiter)

    # THEN
    root_row = f"{a23_str},{bob_str},,{bob_bud.fisc_title},,,,,,,,,1,False,False\n"
    mop_row = f"{a23_str},{bob_str},{bob_bud.fisc_title},mop,{casa_begin},{casa_close},{casa_addin},{casa_numor},{casa_denom},{casa_morph},{casa_gogo_want},{casa_stop_want},{casa_mass},{casa_pledge},{casa_problem_bool}\n"
    casa_row = f"{a23_str},{bob_str},{bob_bud.fisc_title},casa,,,,,,,,,0,False,False\n"
    # print(f"{mop_row=}")
    expected_csv = f"{csv_header}{root_row}{mop_row}{casa_row}"
    print(f"       {x_csv=}")
    print(f"{expected_csv=}")
    assert x_csv == expected_csv


def test_add_to_br00029_csv_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideabricks = create_init_stance_idea_brick_csv_strs()
    bob_str = "Bob"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    bob_bud.credor_respect = 444
    bob_bud.debtor_respect = 555
    bob_bud.fund_pool = 777
    bob_bud.max_tree_traverse = 3
    bob_bud.tally = 10
    bob_bud.fund_coin = 12
    bob_bud.penny = 13
    bob_bud.respect_bit = 15
    csv_header = x_ideabricks.get("br00029")
    print(f"{csv_header=}")

    # WHEN
    x_csv = add_to_br00029_csv(csv_header, bob_bud, csv_delimiter)

    # THEN
    bud_row = f"{a23_str},{bob_str},{bob_bud.credor_respect},{bob_bud.debtor_respect},{bob_bud.fund_pool},{bob_bud.max_tree_traverse},{bob_bud.tally},{bob_bud.fund_coin},{bob_bud.penny},{bob_bud.respect_bit}\n"
    assert x_csv == f"{csv_header}{bud_row}"


def test_add_budunit_to_stance_csv_strs_ReturnsObj():
    # ESTABLISH
    csv_delimiter = ","
    x_ideabricks = create_init_stance_idea_brick_csv_strs()
    bob_str = "Bob"
    yao_str = "Yao"
    a23_str = "accord23"
    bob_bud = budunit_shop(bob_str, a23_str)
    bob_bud.add_acctunit(yao_str)
    mop_road = bob_bud.make_l1_road("mop")
    casa_road = bob_bud.make_l1_road("casa")
    clean_road = bob_bud.make_road(casa_road, "clean")
    bob_bud.add_item(mop_road)
    bob_bud.add_item(casa_road)
    bob_bud.add_item(clean_road)
    bob_bud.edit_item_attr(mop_road, reason_base=casa_road, reason_premise=clean_road)
    bob_bud.add_item(casa_road)
    bob_bud.edit_item_attr(casa_road, awardlink=awardlink_shop(yao_str))
    bob_bud.add_fact(casa_road, clean_road)

    br00020_header = x_ideabricks.get("br00020")
    br00021_header = x_ideabricks.get("br00021")
    br00022_header = x_ideabricks.get("br00022")
    br00023_header = x_ideabricks.get("br00023")
    br00024_header = x_ideabricks.get("br00024")
    br00025_header = x_ideabricks.get("br00025")
    br00026_header = x_ideabricks.get("br00026")
    br00027_header = x_ideabricks.get("br00027")
    br00028_header = x_ideabricks.get("br00028")
    br00029_header = x_ideabricks.get("br00029")

    # WHEN
    bob_bud.settle_bud()
    add_budunit_to_stance_csv_strs(bob_bud, x_ideabricks, csv_delimiter)

    # THEN
    assert x_ideabricks.get("br00020") != br00020_header
    assert x_ideabricks.get("br00021") != br00021_header
    assert x_ideabricks.get("br00022") != br00022_header
    assert x_ideabricks.get("br00023") != br00023_header
    # assert x_ideabricks.get("br00024") != br00024_header
    # assert x_ideabricks.get("br00025") != br00025_header
    assert x_ideabricks.get("br00026") != br00026_header
    assert x_ideabricks.get("br00027") != br00027_header
    assert x_ideabricks.get("br00028") != br00028_header
    assert x_ideabricks.get("br00029") != br00029_header
