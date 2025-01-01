from src.f00_instrument.file import create_path as f_path
from src.f02_bud.bud import budunit_shop
from src.f04_gift.atom_config import (
    cmty_idea_str,
    owner_name_str,
    acct_name_str,
    debtit_belief_str,
    credit_belief_str,
)
from src.f05_listen.hubunit import hubunit_shop
from src.f09_brick.brick import (
    create_brick_df,
    get_brickref_obj,
    save_brick_csv,
    load_brick_csv,
)
from src.f09_brick.brick_config import (
    brick_format_00021_bud_acctunit_v0_0_0,
    brick_format_00012_membership_v0_0_0,
    brick_format_00013_itemunit_v0_0_0,
)
from src.f09_brick.pandas_tool import open_csv
from src.f09_brick.examples.brick_env import (
    brick_examples_dir,
    brick_cmtys_dir,
    brick_env_setup_cleanup,
)


def test_open_csv_ReturnsObj():
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
    accord_cmty_idea = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_cmty_idea)
    sue_budunit.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    sue_budunit.add_acctunit(bob_str, bob_credit_belief, bob_debtit_belief)
    sue_budunit.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    j1_brickname = brick_format_00021_bud_acctunit_v0_0_0()
    name_filename = f"{sue_str}_acct_example_01.csv"
    save_brick_csv(j1_brickname, sue_budunit, brick_examples_dir(), name_filename)

    # WHEN
    acct_dataframe = open_csv(brick_examples_dir(), name_filename)

    # THEN
    array_headers = list(acct_dataframe.columns)
    acct_brickref = get_brickref_obj(j1_brickname)
    assert array_headers == acct_brickref.get_headers_list()
    assert acct_dataframe.loc[0, cmty_idea_str()] == accord_cmty_idea
    assert acct_dataframe.loc[0, owner_name_str()] == sue_budunit.owner_name
    assert acct_dataframe.loc[0, acct_name_str()] == bob_str
    assert acct_dataframe.loc[0, credit_belief_str()] == bob_credit_belief
    assert acct_dataframe.loc[0, debtit_belief_str()] == bob_debtit_belief

    assert acct_dataframe.loc[1, cmty_idea_str()] == accord_cmty_idea
    assert acct_dataframe.loc[1, owner_name_str()] == sue_budunit.owner_name
    assert acct_dataframe.loc[1, acct_name_str()] == sue_str
    assert acct_dataframe.loc[1, credit_belief_str()] == sue_credit_belief
    assert acct_dataframe.loc[1, debtit_belief_str()] == sue_debtit_belief

    assert acct_dataframe.loc[2, cmty_idea_str()] == accord_cmty_idea
    assert acct_dataframe.loc[2, owner_name_str()] == sue_budunit.owner_name
    assert acct_dataframe.loc[2, acct_name_str()] == yao_str
    assert acct_dataframe.loc[2, credit_belief_str()] == yao_credit_belief
    assert acct_dataframe.loc[2, debtit_belief_str()] == yao_debtit_belief

    assert len(acct_dataframe) == 3


def test_load_brick_csv_Arg_brick_format_00021_bud_acctunit_v0_0_0_csvToVoice(
    brick_env_setup_cleanup,
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
    accord_cmty_idea = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_cmty_idea)
    sue_budunit.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    sue_budunit.add_acctunit(bob_str, bob_credit_belief, bob_debtit_belief)
    sue_budunit.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    j1_brickname = brick_format_00021_bud_acctunit_v0_0_0()
    name_filename = f"{sue_str}_acct_example_02.csv"
    csv_example_path = f_path(brick_examples_dir(), name_filename)
    print(f"{csv_example_path}")
    save_brick_csv(j1_brickname, sue_budunit, brick_examples_dir(), name_filename)
    sue_hubunit = hubunit_shop(brick_cmtys_dir(), accord_cmty_idea, owner_name=sue_str)
    # Open CmtyUnit and confirm voice BudUnit does not exist
    assert not sue_hubunit.voice_file_exists()

    # WHEN
    load_brick_csv(sue_hubunit.cmtys_dir, brick_examples_dir(), name_filename)

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


def test_load_brick_csv_csvToVoice(
    brick_env_setup_cleanup,
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
    accord_cmty_idea = "accord56"
    sue_budunit = budunit_shop(sue_str, accord_cmty_idea)
    sue_budunit.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    sue_budunit.add_acctunit(bob_str, bob_credit_belief, bob_debtit_belief)
    sue_budunit.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    j1_brickname = brick_format_00021_bud_acctunit_v0_0_0()
    name_filename = f"{sue_str}_acct_example_02.csv"
    csv_example_path = f_path(brick_examples_dir(), name_filename)
    print(f"{csv_example_path}")
    save_brick_csv(j1_brickname, sue_budunit, brick_examples_dir(), name_filename)
    sue_hubunit = hubunit_shop(brick_cmtys_dir(), accord_cmty_idea, owner_name=sue_str)
    # Open CmtyUnit and confirm voice BudUnit does not exist
    assert not sue_hubunit.voice_file_exists()

    # WHEN
    load_brick_csv(sue_hubunit.cmtys_dir, brick_examples_dir(), name_filename)

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


# def test_load_brick_csv_csvToVoice(
#     brick_env_setup_cleanup,
# ):
#     # ESTABLISH
#     sue_str = "Sue"
#     bob_str = "Bob"
#     accord_cmty_idea = "accord56"
#     sue_budunit = budunit_shop(sue_str, accord_cmty_idea)
#     sue_budunit.add_acctunit(sue_str)
#     sue_budunit.add_acctunit(bob_str)
#     j1_brickname = brick_format_00021_bud_acctunit_v0_0_0()
#     name_filename = f"{sue_str}_acct_example_02.csv"
#     csv_example_path = f_path(brick_examples_dir(), name_filename)
#     print(f"{csv_example_path}")
#     save_brick_csv(j1_brickname, sue_budunit, brick_examples_dir(), name_filename)
#     sue_hubunit = hubunit_shop(brick_cmtys_dir(), accord_cmty_idea, owner_name=sue_str)
#     sue_hubunit.save_voice_bud(budunit_shop(sue_str, accord_cmty_idea))
#     sue_hubunit._create_initial_gift_files_from_voice()
#     old_sue_voice = sue_hubunit.get_voice_bud()
#     old_sue_voice.add_acctunit(sue_str)
#     sue_hubunit.save_voice_bud(old_sue_voice)

#     sue_hubunit.initialize_gift_voice_files()
#     # Open CmtyUnit and confirm voice BudUnit does not exist
#     assert sue_hubunit.voice_file_exists()
#     assert sue_hubunit.get_voice_bud().acct_exists(sue_str)
#     assert not sue_hubunit.get_voice_bud().acct_exists(bob_str)
#     assert sue_hubunit.get_max_gift_file_number() == 3

#     # WHEN
#     load_brick_csv(sue_hubunit.cmtys_dir, brick_examples_dir(), name_filename)

#     # THEN
#     # assert voice Budunit acctunit now exists
#     new_sue_voice = sue_hubunit.get_voice_bud()
#     assert new_sue_voice.acct_exists(sue_str)
#     assert new_sue_voice.acct_exists(bob_str)
#     # assert voice Budunit acctunit.credit_belief is correct
#     sue_acctunit = new_sue_voice.get_acct(sue_str)
#     bob_acctunit = new_sue_voice.get_acct(bob_str)
#     assert sue_hubunit.get_max_gift_file_number() != 3
#     assert 1 == 2


# def test_create_brick_df_Arg_brick_format_00013_itemunit_v0_0_0_Scenario_budunit_v001(
#     big_volume,
# ):
#     if big_volume:
#         # ESTABLISH / WHEN
#         x_brick_name = brick_format_00013_itemunit_v0_0_0()

#         # WHEN
#         itemunit_format = create_brick_df(budunit_v001(), x_brick_name)

#         # THEN
#         array_headers = list(itemunit_format.columns)
#         assert array_headers == get_brickref_obj(x_brick_name).get_headers_list()
#         assert len(itemunit_format) == 251
