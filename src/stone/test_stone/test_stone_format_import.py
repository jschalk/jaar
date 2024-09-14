from src._instrument.file import create_file_path as f_path
from src.bud.bud import budunit_shop
from src.gift.atom_config import (
    fiscal_id_str,
    owner_id_str,
    acct_id_str,
    debtit_belief_str,
    credit_belief_str,
)
from src.listen.hubunit import hubunit_shop
from src.stone.stone import (
    create_stone_df,
    get_stoneref,
    save_stone_csv,
    open_stone_csv,
    load_stone_csv,
)
from src.stone.stone_config import (
    stone_format_00021_bud_acctunit_v0_0_0,
    stone_format_00002_membership_v0_0_0,
    stone_format_00003_ideaunit_v0_0_0,
)
from src.stone.examples.stone_env import (
    stone_examples_dir,
    stone_fiscals_dir,
    stone_env_setup_cleanup,
)


def test_open_stone_csv_ReturnsObj():
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
    music_fiscal_id = "music56"
    sue_budunit = budunit_shop(sue_str, music_fiscal_id)
    sue_budunit.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    sue_budunit.add_acctunit(bob_str, bob_credit_belief, bob_debtit_belief)
    sue_budunit.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    j1_stonename = stone_format_00021_bud_acctunit_v0_0_0()
    acct_filename = f"{sue_str}_acct_example_01.csv"
    save_stone_csv(j1_stonename, sue_budunit, stone_examples_dir(), acct_filename)

    # WHEN
    acct_dataframe = open_stone_csv(stone_examples_dir(), acct_filename)

    # THEN
    array_headers = list(acct_dataframe.columns)
    acct_stoneref = get_stoneref(j1_stonename)
    assert array_headers == acct_stoneref.get_headers_list()
    assert acct_dataframe.loc[0, fiscal_id_str()] == music_fiscal_id
    assert acct_dataframe.loc[0, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[0, acct_id_str()] == bob_str
    assert acct_dataframe.loc[0, credit_belief_str()] == bob_credit_belief
    assert acct_dataframe.loc[0, debtit_belief_str()] == bob_debtit_belief

    assert acct_dataframe.loc[1, fiscal_id_str()] == music_fiscal_id
    assert acct_dataframe.loc[1, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[1, acct_id_str()] == sue_str
    assert acct_dataframe.loc[1, credit_belief_str()] == sue_credit_belief
    assert acct_dataframe.loc[1, debtit_belief_str()] == sue_debtit_belief

    assert acct_dataframe.loc[2, fiscal_id_str()] == music_fiscal_id
    assert acct_dataframe.loc[2, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[2, acct_id_str()] == yao_str
    assert acct_dataframe.loc[2, credit_belief_str()] == yao_credit_belief
    assert acct_dataframe.loc[2, debtit_belief_str()] == yao_debtit_belief

    assert len(acct_dataframe) == 3


def test_load_stone_csv_Arg_stone_format_00021_bud_acctunit_v0_0_0_csvToVoice(
    stone_env_setup_cleanup,
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
    music_fiscal_id = "music56"
    sue_budunit = budunit_shop(sue_str, music_fiscal_id)
    sue_budunit.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    sue_budunit.add_acctunit(bob_str, bob_credit_belief, bob_debtit_belief)
    sue_budunit.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    j1_stonename = stone_format_00021_bud_acctunit_v0_0_0()
    acct_filename = f"{sue_str}_acct_example_02.csv"
    csv_example_path = f_path(stone_examples_dir(), acct_filename)
    print(f"{csv_example_path}")
    save_stone_csv(j1_stonename, sue_budunit, stone_examples_dir(), acct_filename)
    sue_hubunit = hubunit_shop(stone_fiscals_dir(), music_fiscal_id, owner_id=sue_str)
    # Open FiscalUnit and confirm voice BudUnit does not exist
    assert not sue_hubunit.voice_file_exists()

    # WHEN
    load_stone_csv(sue_hubunit.fiscals_dir, stone_examples_dir(), acct_filename)

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


def test_load_stone_csv_csvToVoice(
    stone_env_setup_cleanup,
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
    music_fiscal_id = "music56"
    sue_budunit = budunit_shop(sue_str, music_fiscal_id)
    sue_budunit.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    sue_budunit.add_acctunit(bob_str, bob_credit_belief, bob_debtit_belief)
    sue_budunit.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    j1_stonename = stone_format_00021_bud_acctunit_v0_0_0()
    acct_filename = f"{sue_str}_acct_example_02.csv"
    csv_example_path = f_path(stone_examples_dir(), acct_filename)
    print(f"{csv_example_path}")
    save_stone_csv(j1_stonename, sue_budunit, stone_examples_dir(), acct_filename)
    sue_hubunit = hubunit_shop(stone_fiscals_dir(), music_fiscal_id, owner_id=sue_str)
    # Open FiscalUnit and confirm voice BudUnit does not exist
    assert not sue_hubunit.voice_file_exists()

    # WHEN
    load_stone_csv(sue_hubunit.fiscals_dir, stone_examples_dir(), acct_filename)

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


# def test_load_stone_csv_csvToVoice(
#     stone_env_setup_cleanup,
# ):
#     # ESTABLISH
#     sue_str = "Sue"
#     bob_str = "Bob"
#     music_fiscal_id = "music56"
#     sue_budunit = budunit_shop(sue_str, music_fiscal_id)
#     sue_budunit.add_acctunit(sue_str)
#     sue_budunit.add_acctunit(bob_str)
#     j1_stonename = stone_format_00021_bud_acctunit_v0_0_0()
#     acct_filename = f"{sue_str}_acct_example_02.csv"
#     csv_example_path = f_path(stone_examples_dir(), acct_filename)
#     print(f"{csv_example_path}")
#     save_stone_csv(j1_stonename, sue_budunit, stone_examples_dir(), acct_filename)
#     sue_hubunit = hubunit_shop(stone_fiscals_dir(), music_fiscal_id, owner_id=sue_str)
#     sue_hubunit.save_voice_bud(budunit_shop(sue_str, music_fiscal_id))
#     sue_hubunit._create_initial_gift_files_from_voice()
#     old_sue_voice = sue_hubunit.get_voice_bud()
#     old_sue_voice.add_acctunit(sue_str)
#     sue_hubunit.save_voice_bud(old_sue_voice)

#     sue_hubunit.initialize_gift_voice_files()
#     # Open FiscalUnit and confirm voice BudUnit does not exist
#     assert sue_hubunit.voice_file_exists()
#     assert sue_hubunit.get_voice_bud().acct_exists(sue_str)
#     assert not sue_hubunit.get_voice_bud().acct_exists(bob_str)
#     assert sue_hubunit.get_max_gift_file_number() == 3

#     # WHEN
#     load_stone_csv(sue_hubunit.fiscals_dir, stone_examples_dir(), acct_filename)

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


# def test_create_stone_df_Arg_stone_format_00003_ideaunit_v0_0_0_Scenario_budunit_v001(
#     big_volume,
# ):
#     if big_volume:
#         # ESTABLISH / WHEN
#         x_stone_name = stone_format_00003_ideaunit_v0_0_0()

#         # WHEN
#         ideaunit_format = create_stone_df(budunit_v001(), x_stone_name)

#         # THEN
#         array_headers = list(ideaunit_format.columns)
#         assert array_headers == get_stoneref(x_stone_name).get_headers_list()
#         assert len(ideaunit_format) == 251
