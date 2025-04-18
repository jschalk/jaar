from src.a00_data_toolboxs.file_toolbox import create_path
from src.a02_finance_toolboxs.deal import owner_name_str, fisc_title_str
from src.a06_bud_logic.bud import budunit_shop
from src.a08_bud_atom_logic.atom_config import (
    acct_name_str,
    debtit_belief_str,
    credit_belief_str,
)
from src.a12_hub_tools.hub_tool import open_gut_file, gut_file_exists
from src.a12_hub_tools.hubunit import hubunit_shop
from src.a17_idea_logic.idea import (
    create_idea_df,
    get_idearef_obj,
    save_idea_csv,
    load_idea_csv,
)
from src.a17_idea_logic.idea_config import (
    idea_format_00021_bud_acctunit_v0_0_0,
    idea_format_00012_membership_v0_0_0,
    idea_format_00013_itemunit_v0_0_0,
)
from src.a17_idea_logic.idea_db_tool import open_csv
from src.a17_idea_logic.examples.idea_env import (
    idea_examples_dir,
    idea_env_setup_cleanup,
)


def test_open_csv_ReturnsObjWhenFileExists(idea_env_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    sue_credit_belief = 11
    bob_credit_belief = 13
    yao_credit_belief = 41
    sue_debtit_belief = 23
    bob_debtit_belief = 29
    yao_debtit_belief = 37
    accord_fisc_title = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_fisc_title)
    sue_budunit.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    sue_budunit.add_acctunit(bob_str, bob_credit_belief, bob_debtit_belief)
    sue_budunit.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    j1_ideaname = idea_format_00021_bud_acctunit_v0_0_0()
    name_filename = f"{sue_str}_acct_example_01.csv"
    save_idea_csv(j1_ideaname, sue_budunit, idea_examples_dir(), name_filename)

    # WHEN
    acct_dataframe = open_csv(idea_examples_dir(), name_filename)

    # THEN
    array_headers = list(acct_dataframe.columns)
    acct_idearef = get_idearef_obj(j1_ideaname)
    assert array_headers == acct_idearef.get_headers_list()
    assert acct_dataframe.loc[0, fisc_title_str()] == accord_fisc_title
    assert acct_dataframe.loc[0, owner_name_str()] == sue_budunit.owner_name
    assert acct_dataframe.loc[0, acct_name_str()] == bob_str
    assert acct_dataframe.loc[0, credit_belief_str()] == bob_credit_belief
    assert acct_dataframe.loc[0, debtit_belief_str()] == bob_debtit_belief

    assert acct_dataframe.loc[1, fisc_title_str()] == accord_fisc_title
    assert acct_dataframe.loc[1, owner_name_str()] == sue_budunit.owner_name
    assert acct_dataframe.loc[1, acct_name_str()] == sue_str
    assert acct_dataframe.loc[1, credit_belief_str()] == sue_credit_belief
    assert acct_dataframe.loc[1, debtit_belief_str()] == sue_debtit_belief

    assert acct_dataframe.loc[2, fisc_title_str()] == accord_fisc_title
    assert acct_dataframe.loc[2, owner_name_str()] == sue_budunit.owner_name
    assert acct_dataframe.loc[2, acct_name_str()] == yao_str
    assert acct_dataframe.loc[2, credit_belief_str()] == yao_credit_belief
    assert acct_dataframe.loc[2, debtit_belief_str()] == yao_debtit_belief

    assert len(acct_dataframe) == 3


def test_open_csv_ReturnsObjWhenNoFileExists(idea_env_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    name_filename = f"{sue_str}_acct_example_77.csv"

    # WHEN
    acct_dataframe = open_csv(idea_examples_dir(), name_filename)

    # THEN
    assert acct_dataframe is None


def test_load_idea_csv_Arg_idea_format_00021_bud_acctunit_v0_0_0_csvTo_job(
    idea_env_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    sue_credit_belief = 11
    bob_credit_belief = 13
    yao_credit_belief = 41
    sue_debtit_belief = 23
    bob_debtit_belief = 29
    yao_debtit_belief = 37
    accord_fisc_title = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_fisc_title)
    sue_budunit.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    sue_budunit.add_acctunit(bob_str, bob_credit_belief, bob_debtit_belief)
    sue_budunit.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    j1_ideaname = idea_format_00021_bud_acctunit_v0_0_0()
    name_filename = f"{sue_str}_acct_example_02.csv"
    csv_example_path = create_path(idea_examples_dir(), name_filename)
    print(f"{csv_example_path}")
    save_idea_csv(j1_ideaname, sue_budunit, idea_examples_dir(), name_filename)
    sue_hubunit = hubunit_shop(
        idea_examples_dir(), accord_fisc_title, owner_name=sue_str
    )
    # Open FiscUnit and confirm gut BudUnit does not exist
    assert not gut_file_exists(idea_examples_dir(), accord_fisc_title, sue_str)

    # WHEN
    load_idea_csv(sue_hubunit.fisc_mstr_dir, idea_examples_dir(), name_filename)

    # THEN
    # assert gut Budunit now exists
    assert gut_file_exists(idea_examples_dir(), accord_fisc_title, sue_str)
    # assert gut Budunit acctunit now exists
    sue_gut = open_gut_file(idea_examples_dir(), accord_fisc_title, sue_str)

    assert sue_gut.acct_exists(sue_str)
    assert sue_gut.acct_exists(bob_str)
    assert sue_gut.acct_exists(yao_str)
    # assert gut Budunit acctunit.credit_belief is correct
    sue_acctunit = sue_gut.get_acct(sue_str)
    bob_acctunit = sue_gut.get_acct(bob_str)
    yao_acctunit = sue_gut.get_acct(yao_str)
    # assert gut Budunit acctunit.credit_belief is correct
    assert sue_acctunit.credit_belief == sue_credit_belief
    assert bob_acctunit.credit_belief == bob_credit_belief
    assert yao_acctunit.credit_belief == yao_credit_belief
    assert sue_acctunit.debtit_belief == sue_debtit_belief
    assert bob_acctunit.debtit_belief == bob_debtit_belief
    assert yao_acctunit.debtit_belief == yao_debtit_belief


def test_load_idea_csv_csvTo_job(
    idea_env_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    sue_credit_belief = 11
    bob_credit_belief = 13
    yao_credit_belief = 41
    sue_debtit_belief = 23
    bob_debtit_belief = 29
    yao_debtit_belief = 37
    accord_fisc_title = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_fisc_title)
    sue_budunit.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    sue_budunit.add_acctunit(bob_str, bob_credit_belief, bob_debtit_belief)
    sue_budunit.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    j1_ideaname = idea_format_00021_bud_acctunit_v0_0_0()
    name_filename = f"{sue_str}_acct_example_02.csv"
    csv_example_path = create_path(idea_examples_dir(), name_filename)
    print(f"{csv_example_path}")
    save_idea_csv(j1_ideaname, sue_budunit, idea_examples_dir(), name_filename)
    sue_hubunit = hubunit_shop(
        idea_examples_dir(), accord_fisc_title, owner_name=sue_str
    )
    # Open FiscUnit and confirm gut BudUnit does not exist
    assert not gut_file_exists(idea_examples_dir(), accord_fisc_title, sue_str)

    # WHEN
    load_idea_csv(sue_hubunit.fisc_mstr_dir, idea_examples_dir(), name_filename)

    # THEN
    # assert gut Budunit now exists
    assert gut_file_exists(idea_examples_dir(), accord_fisc_title, sue_str)
    # assert gut Budunit acctunit now exists
    sue_gut = open_gut_file(idea_examples_dir(), accord_fisc_title, sue_str)
    assert sue_gut.acct_exists(sue_str)
    assert sue_gut.acct_exists(bob_str)
    assert sue_gut.acct_exists(yao_str)
    # assert gut Budunit acctunit.credit_belief is correct
    sue_acctunit = sue_gut.get_acct(sue_str)
    bob_acctunit = sue_gut.get_acct(bob_str)
    yao_acctunit = sue_gut.get_acct(yao_str)
    # assert gut Budunit acctunit.credit_belief is correct
    assert sue_acctunit.credit_belief == sue_credit_belief
    assert bob_acctunit.credit_belief == bob_credit_belief
    assert yao_acctunit.credit_belief == yao_credit_belief
    assert sue_acctunit.debtit_belief == sue_debtit_belief
    assert bob_acctunit.debtit_belief == bob_debtit_belief
    assert yao_acctunit.debtit_belief == yao_debtit_belief
