from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic._test_util.a02_str import owner_name_str, vow_label_str
from src.a06_plan_logic._test_util.a06_str import (
    acct_name_str,
    credit_score_str,
    debt_score_str,
)
from src.a06_plan_logic.plan import planunit_shop
from src.a12_hub_tools.hub_tool import gut_file_exists, open_gut_file
from src.a17_idea_logic._test_util.a17_env import (
    env_dir_setup_cleanup,
    idea_examples_dir,
)
from src.a17_idea_logic.idea import get_idearef_obj, load_idea_csv, save_idea_csv
from src.a17_idea_logic.idea_config import (
    idea_format_00012_membership_v0_0_0,
    idea_format_00013_conceptunit_v0_0_0,
    idea_format_00021_plan_acctunit_v0_0_0,
)
from src.a17_idea_logic.idea_db_tool import open_csv


def test_open_csv_ReturnsObjWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    sue_credit_score = 11
    bob_credit_score = 13
    yao_credit_score = 41
    sue_debt_score = 23
    bob_debt_score = 29
    yao_debt_score = 37
    accord_vow_label = "accord56"
    sue_planunit = planunit_shop(sue_str, accord_vow_label)
    sue_planunit.add_acctunit(sue_str, sue_credit_score, sue_debt_score)
    sue_planunit.add_acctunit(bob_str, bob_credit_score, bob_debt_score)
    sue_planunit.add_acctunit(yao_str, yao_credit_score, yao_debt_score)
    j1_ideaname = idea_format_00021_plan_acctunit_v0_0_0()
    name_filename = f"{sue_str}_acct_example_01.csv"
    save_idea_csv(j1_ideaname, sue_planunit, idea_examples_dir(), name_filename)

    # WHEN
    acct_dataframe = open_csv(idea_examples_dir(), name_filename)

    # THEN
    array_headers = list(acct_dataframe.columns)
    acct_idearef = get_idearef_obj(j1_ideaname)
    assert array_headers == acct_idearef.get_headers_list()
    assert acct_dataframe.loc[0, vow_label_str()] == accord_vow_label
    assert acct_dataframe.loc[0, owner_name_str()] == sue_planunit.owner_name
    assert acct_dataframe.loc[0, acct_name_str()] == bob_str
    assert acct_dataframe.loc[0, credit_score_str()] == bob_credit_score
    assert acct_dataframe.loc[0, debt_score_str()] == bob_debt_score

    assert acct_dataframe.loc[1, vow_label_str()] == accord_vow_label
    assert acct_dataframe.loc[1, owner_name_str()] == sue_planunit.owner_name
    assert acct_dataframe.loc[1, acct_name_str()] == sue_str
    assert acct_dataframe.loc[1, credit_score_str()] == sue_credit_score
    assert acct_dataframe.loc[1, debt_score_str()] == sue_debt_score

    assert acct_dataframe.loc[2, vow_label_str()] == accord_vow_label
    assert acct_dataframe.loc[2, owner_name_str()] == sue_planunit.owner_name
    assert acct_dataframe.loc[2, acct_name_str()] == yao_str
    assert acct_dataframe.loc[2, credit_score_str()] == yao_credit_score
    assert acct_dataframe.loc[2, debt_score_str()] == yao_debt_score

    assert len(acct_dataframe) == 3


def test_open_csv_ReturnsObjWhenNoFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    name_filename = f"{sue_str}_acct_example_77.csv"

    # WHEN
    acct_dataframe = open_csv(idea_examples_dir(), name_filename)

    # THEN
    assert acct_dataframe is None


def test_load_idea_csv_Arg_idea_format_00021_plan_acctunit_v0_0_0_csvTo_job(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    sue_credit_score = 11
    bob_credit_score = 13
    yao_credit_score = 41
    sue_debt_score = 23
    bob_debt_score = 29
    yao_debt_score = 37
    accord_vow_label = "accord56"
    sue_planunit = planunit_shop(sue_str, accord_vow_label)
    sue_planunit.add_acctunit(sue_str, sue_credit_score, sue_debt_score)
    sue_planunit.add_acctunit(bob_str, bob_credit_score, bob_debt_score)
    sue_planunit.add_acctunit(yao_str, yao_credit_score, yao_debt_score)
    j1_ideaname = idea_format_00021_plan_acctunit_v0_0_0()
    name_filename = f"{sue_str}_acct_example_02.csv"
    vow_mstr_dir = idea_examples_dir()
    csv_example_path = create_path(vow_mstr_dir, name_filename)
    print(f"{csv_example_path}")
    save_idea_csv(j1_ideaname, sue_planunit, vow_mstr_dir, name_filename)
    # Popen VowUnit and confirm gut PlanUnit does not exist
    assert not gut_file_exists(vow_mstr_dir, accord_vow_label, sue_str)

    # WHEN
    load_idea_csv(vow_mstr_dir, idea_examples_dir(), name_filename)

    # THEN
    # assert gut Planunit now exists
    assert gut_file_exists(idea_examples_dir(), accord_vow_label, sue_str)
    # assert gut Planunit acctunit now exists
    sue_gut = open_gut_file(idea_examples_dir(), accord_vow_label, sue_str)

    assert sue_gut.acct_exists(sue_str)
    assert sue_gut.acct_exists(bob_str)
    assert sue_gut.acct_exists(yao_str)
    # assert gut Planunit acctunit.credit_score is correct
    sue_acctunit = sue_gut.get_acct(sue_str)
    bob_acctunit = sue_gut.get_acct(bob_str)
    yao_acctunit = sue_gut.get_acct(yao_str)
    # assert gut Planunit acctunit.credit_score is correct
    assert sue_acctunit.credit_score == sue_credit_score
    assert bob_acctunit.credit_score == bob_credit_score
    assert yao_acctunit.credit_score == yao_credit_score
    assert sue_acctunit.debt_score == sue_debt_score
    assert bob_acctunit.debt_score == bob_debt_score
    assert yao_acctunit.debt_score == yao_debt_score


def test_load_idea_csv_csvTo_job(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    sue_credit_score = 11
    bob_credit_score = 13
    yao_credit_score = 41
    sue_debt_score = 23
    bob_debt_score = 29
    yao_debt_score = 37
    accord_vow_label = "accord56"
    sue_planunit = planunit_shop(sue_str, accord_vow_label)
    sue_planunit.add_acctunit(sue_str, sue_credit_score, sue_debt_score)
    sue_planunit.add_acctunit(bob_str, bob_credit_score, bob_debt_score)
    sue_planunit.add_acctunit(yao_str, yao_credit_score, yao_debt_score)
    j1_ideaname = idea_format_00021_plan_acctunit_v0_0_0()
    name_filename = f"{sue_str}_acct_example_02.csv"
    csv_example_path = create_path(idea_examples_dir(), name_filename)
    print(f"{csv_example_path}")
    save_idea_csv(j1_ideaname, sue_planunit, idea_examples_dir(), name_filename)
    vow_mstr_dir = idea_examples_dir()
    # Popen VowUnit and confirm gut PlanUnit does not exist
    assert not gut_file_exists(vow_mstr_dir, accord_vow_label, sue_str)

    # WHEN
    load_idea_csv(vow_mstr_dir, idea_examples_dir(), name_filename)

    # THEN
    # assert gut Planunit now exists
    assert gut_file_exists(idea_examples_dir(), accord_vow_label, sue_str)
    # assert gut Planunit acctunit now exists
    sue_gut = open_gut_file(idea_examples_dir(), accord_vow_label, sue_str)
    assert sue_gut.acct_exists(sue_str)
    assert sue_gut.acct_exists(bob_str)
    assert sue_gut.acct_exists(yao_str)
    # assert gut Planunit acctunit.credit_score is correct
    sue_acctunit = sue_gut.get_acct(sue_str)
    bob_acctunit = sue_gut.get_acct(bob_str)
    yao_acctunit = sue_gut.get_acct(yao_str)
    # assert gut Planunit acctunit.credit_score is correct
    assert sue_acctunit.credit_score == sue_credit_score
    assert bob_acctunit.credit_score == bob_credit_score
    assert yao_acctunit.credit_score == yao_credit_score
    assert sue_acctunit.debt_score == sue_debt_score
    assert bob_acctunit.debt_score == bob_debt_score
    assert yao_acctunit.debt_score == yao_debt_score
