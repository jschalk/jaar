from src.f00_instrument.file import create_path as f_path
from src.f01_road.deal import owner_name_str, fisc_title_str
from src.f02_bud.bud import budunit_shop
from src.f04_vow.atom_config import (
    acct_name_str,
    debtit_belief_str,
    credit_belief_str,
)
from src.f05_listen.hubunit import hubunit_shop
from src.f09_idea.idea import (
    create_idea_df,
    get_idearef_obj,
    save_idea_csv,
    load_idea_csv,
)
from src.f09_idea.idea_config import (
    idea_format_00021_bud_acctunit_v0_0_0,
    idea_format_00012_membership_v0_0_0,
    idea_format_00013_itemunit_v0_0_0,
)
from src.f09_idea.idea_db_tool import open_csv
from src.f09_idea.examples.idea_env import idea_examples_dir, idea_env_setup_cleanup


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


def test_load_idea_csv_Arg_idea_format_00021_bud_acctunit_v0_0_0_csvToForecast(
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
    csv_example_path = f_path(idea_examples_dir(), name_filename)
    print(f"{csv_example_path}")
    save_idea_csv(j1_ideaname, sue_budunit, idea_examples_dir(), name_filename)
    sue_hubunit = hubunit_shop(
        idea_examples_dir(), accord_fisc_title, owner_name=sue_str
    )
    # Open FiscUnit and confirm voice BudUnit does not exist
    assert not sue_hubunit.voice_file_exists()

    # WHEN
    load_idea_csv(sue_hubunit.fisc_mstr_dir, idea_examples_dir(), name_filename)

    # THEN
    # assert voice Budunit now exists
    assert sue_hubunit.voice_file_exists()
    # assert voice Budunit acctunit now exists
    sue_voice = sue_hubunit.get_voice_bud()
    assert sue_voice.acct_exists(sue_str)
    assert sue_voice.acct_exists(bob_str)
    assert sue_voice.acct_exists(yao_str)
    # assert voice Budunit acctunit.credit_belief is correct
    sue_acctunit = sue_voice.get_acct(sue_str)
    bob_acctunit = sue_voice.get_acct(bob_str)
    yao_acctunit = sue_voice.get_acct(yao_str)
    # assert voice Budunit acctunit.credit_belief is correct
    assert sue_acctunit.credit_belief == sue_credit_belief
    assert bob_acctunit.credit_belief == bob_credit_belief
    assert yao_acctunit.credit_belief == yao_credit_belief
    assert sue_acctunit.debtit_belief == sue_debtit_belief
    assert bob_acctunit.debtit_belief == bob_debtit_belief
    assert yao_acctunit.debtit_belief == yao_debtit_belief


def test_load_idea_csv_csvToForecast(
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
    csv_example_path = f_path(idea_examples_dir(), name_filename)
    print(f"{csv_example_path}")
    save_idea_csv(j1_ideaname, sue_budunit, idea_examples_dir(), name_filename)
    sue_hubunit = hubunit_shop(
        idea_examples_dir(), accord_fisc_title, owner_name=sue_str
    )
    # Open FiscUnit and confirm voice BudUnit does not exist
    assert not sue_hubunit.voice_file_exists()

    # WHEN
    load_idea_csv(sue_hubunit.fisc_mstr_dir, idea_examples_dir(), name_filename)

    # THEN
    # assert voice Budunit now exists
    assert sue_hubunit.voice_file_exists()
    # assert voice Budunit acctunit now exists
    sue_voice = sue_hubunit.get_voice_bud()
    assert sue_voice.acct_exists(sue_str)
    assert sue_voice.acct_exists(bob_str)
    assert sue_voice.acct_exists(yao_str)
    # assert voice Budunit acctunit.credit_belief is correct
    sue_acctunit = sue_voice.get_acct(sue_str)
    bob_acctunit = sue_voice.get_acct(bob_str)
    yao_acctunit = sue_voice.get_acct(yao_str)
    # assert voice Budunit acctunit.credit_belief is correct
    assert sue_acctunit.credit_belief == sue_credit_belief
    assert bob_acctunit.credit_belief == bob_credit_belief
    assert yao_acctunit.credit_belief == yao_credit_belief
    assert sue_acctunit.debtit_belief == sue_debtit_belief
    assert bob_acctunit.debtit_belief == bob_debtit_belief
    assert yao_acctunit.debtit_belief == yao_debtit_belief


# def test_load_idea_csv_csvToForecast(
#     idea_env_setup_cleanup,
# ):
#     # ESTABLISH
#     sue_str = "Sue"
#     bob_str = "Bob"
#     accord_fisc_title = "accord56"
#     sue_budunit = budunit_shop(sue_str, accord_fisc_title)
#     sue_budunit.add_acctunit(sue_str)
#     sue_budunit.add_acctunit(bob_str)
#     j1_ideaname = idea_format_00021_bud_acctunit_v0_0_0()
#     name_filename = f"{sue_str}_acct_example_02.csv"
#     csv_example_path = f_path(idea_examples_dir(), name_filename)
#     print(f"{csv_example_path}")
#     save_idea_csv(j1_ideaname, sue_budunit, idea_examples_dir(), name_filename)
#     sue_hubunit = hubunit_shop(idea_examples_dir(), accord_fisc_title, owner_name=sue_str)
#     sue_hubunit.save_voice_bud(budunit_shop(sue_str, accord_fisc_title))
#     sue_hubunit._create_initial_vow_files_from_voice()
#     old_sue_voice = sue_hubunit.get_voice_bud()
#     old_sue_voice.add_acctunit(sue_str)
#     sue_hubunit.save_voice_bud(old_sue_voice)

#     sue_hubunit.initialize_vow_voice_files()
#     # Open FiscUnit and confirm voice BudUnit does not exist
#     assert sue_hubunit.voice_file_exists()
#     assert sue_hubunit.get_voice_bud().acct_exists(sue_str)
#     assert not sue_hubunit.get_voice_bud().acct_exists(bob_str)
#     assert sue_hubunit.get_max_vow_file_number() == 3

#     # WHEN
#     load_idea_csv(sue_hubunit.fisc_mstr_dir, idea_examples_dir(), name_filename)

#     # THEN
#     # assert voice Budunit acctunit now exists
#     new_sue_voice = sue_hubunit.get_voice_bud()
#     assert new_sue_voice.acct_exists(sue_str)
#     assert new_sue_voice.acct_exists(bob_str)
#     # assert voice Budunit acctunit.credit_belief is correct
#     sue_acctunit = new_sue_voice.get_acct(sue_str)
#     bob_acctunit = new_sue_voice.get_acct(bob_str)
#     assert sue_hubunit.get_max_vow_file_number() != 3
#     assert 1 == 2


# def test_create_idea_df_Arg_idea_format_00013_itemunit_v0_0_0_Scenario_budunit_v001(
#     big_volume,
# ):
#     if big_volume:
#         # ESTABLISH / WHEN
#         x_idea_name = idea_format_00013_itemunit_v0_0_0()

#         # WHEN
#         itemunit_format = create_idea_df(budunit_v001(), x_idea_name)

#         # THEN
#         array_headers = list(itemunit_format.columns)
#         assert array_headers == get_idearef_obj(x_idea_name).get_headers_list()
#         assert len(itemunit_format) == 251
