from src._instrument.file import create_file_path as f_path
from src._road.jaar_refer import sue_str, bob_str, yao_str
from src.bud.bud import budunit_shop
from src.bud.examples.example_buds import budunit_v001
from src.gift.atom_config import (
    real_id_str,
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
    stone_reals_dir,
    stone_env_setup_cleanup,
)


def test_open_stone_csv_ReturnsObj():
    # ESTABLISH
    sue_text = sue_str()
    bob_text = bob_str()
    yao_text = yao_str()
    sue_credit_belief = 11
    bob_credit_belief = 13
    yao_credit_belief = 41
    sue_debtit_belief = 23
    bob_debtit_belief = 29
    yao_debtit_belief = 37
    music_real_id = "music56"
    sue_budunit = budunit_shop(sue_text, music_real_id)
    sue_budunit.add_acctunit(sue_text, sue_credit_belief, sue_debtit_belief)
    sue_budunit.add_acctunit(bob_text, bob_credit_belief, bob_debtit_belief)
    sue_budunit.add_acctunit(yao_text, yao_credit_belief, yao_debtit_belief)
    j1_stonename = stone_format_00021_bud_acctunit_v0_0_0()
    acct_filename = f"{sue_text}_acct_example_01.csv"
    save_stone_csv(j1_stonename, sue_budunit, stone_examples_dir(), acct_filename)

    # WHEN
    acct_dataframe = open_stone_csv(stone_examples_dir(), acct_filename)

    # THEN
    array_headers = list(acct_dataframe.columns)
    acct_stoneref = get_stoneref(j1_stonename)
    assert array_headers == acct_stoneref.get_headers_list()
    assert acct_dataframe.loc[0, real_id_str()] == music_real_id
    assert acct_dataframe.loc[0, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[0, acct_id_str()] == bob_text
    assert acct_dataframe.loc[0, credit_belief_str()] == bob_credit_belief
    assert acct_dataframe.loc[0, debtit_belief_str()] == bob_debtit_belief

    assert acct_dataframe.loc[1, real_id_str()] == music_real_id
    assert acct_dataframe.loc[1, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[1, acct_id_str()] == sue_text
    assert acct_dataframe.loc[1, credit_belief_str()] == sue_credit_belief
    assert acct_dataframe.loc[1, debtit_belief_str()] == sue_debtit_belief

    assert acct_dataframe.loc[2, real_id_str()] == music_real_id
    assert acct_dataframe.loc[2, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[2, acct_id_str()] == yao_text
    assert acct_dataframe.loc[2, credit_belief_str()] == yao_credit_belief
    assert acct_dataframe.loc[2, debtit_belief_str()] == yao_debtit_belief

    assert len(acct_dataframe) == 3


def test_save_stone_csv_Arg_stone_format_00021_bud_acctunit_v0_0_0_SaveToCSV(
    stone_env_setup_cleanup,
):
    # ESTABLISH
    sue_text = sue_str()
    bob_text = bob_str()
    yao_text = yao_str()
    sue_credit_belief = 11
    bob_credit_belief = 13
    yao_credit_belief = 41
    sue_debtit_belief = 23
    bob_debtit_belief = 29
    yao_debtit_belief = 37
    music_real_id = "music56"
    sue_budunit = budunit_shop(sue_text, music_real_id)
    sue_budunit.add_acctunit(sue_text, sue_credit_belief, sue_debtit_belief)
    sue_budunit.add_acctunit(bob_text, bob_credit_belief, bob_debtit_belief)
    sue_budunit.add_acctunit(yao_text, yao_credit_belief, yao_debtit_belief)
    j1_stonename = stone_format_00021_bud_acctunit_v0_0_0()
    acct_filename = f"{sue_text}_acct_example_02.csv"
    csv_example_path = f_path(stone_examples_dir(), acct_filename)
    print(f"{csv_example_path}")
    save_stone_csv(j1_stonename, sue_budunit, stone_examples_dir(), acct_filename)
    music_hubunit = hubunit_shop(stone_reals_dir(), music_real_id, owner_id=sue_text)
    # Open RealUnit and confirm voice BudUnit does not exist
    assert not music_hubunit.voice_file_exists()

    # WHEN
    load_stone_csv(music_hubunit.reals_dir, stone_examples_dir(), acct_filename)

    # THEN
    # assert voice Budunit now exists
    assert music_hubunit.voice_file_exists()
    # assert voice Budunit acctunit now exists
    sue_voice = music_hubunit.get_voice_bud()
    assert sue_voice.acct_exists(sue_text)
    assert sue_voice.acct_exists(bob_text)
    assert sue_voice.acct_exists(yao_text)
    # assert voice Budunit acctunit.credit_belief is correct
    sue_acctunit = sue_voice.get_acct(sue_text)
    bob_acctunit = sue_voice.get_acct(bob_text)
    yao_acctunit = sue_voice.get_acct(yao_text)
    # assert voice Budunit acctunit.credit_belief is correct
    assert sue_acctunit.credit_belief == sue_credit_belief
    assert bob_acctunit.credit_belief == bob_credit_belief
    assert yao_acctunit.credit_belief == yao_credit_belief
    assert sue_acctunit.debtit_belief == sue_debtit_belief
    assert bob_acctunit.debtit_belief == bob_debtit_belief
    assert yao_acctunit.debtit_belief == yao_debtit_belief


def test_create_stone_df_Arg_stone_format_00003_ideaunit_v0_0_0_Scenario_budunit_v001(
    big_volume,
):
    if big_volume:
        # ESTABLISH / WHEN
        x_stone_name = stone_format_00003_ideaunit_v0_0_0()

        # WHEN
        ideaunit_format = create_stone_df(budunit_v001(), x_stone_name)

        # THEN
        array_headers = list(ideaunit_format.columns)
        assert array_headers == get_stoneref(x_stone_name).get_headers_list()
        assert len(ideaunit_format) == 251
