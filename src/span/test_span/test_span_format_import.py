from src._instrument.file import delete_dir, open_file, create_file_path as f_path
from src._road.jaar_refer import sue_str, bob_str, yao_str
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.listen.hubunit import hubunit_shop
from src.span.span import (
    jaar_format_00001_acct_v0_0_0,
    jaar_format_00002_membership_v0_0_0,
    jaar_format_00003_ideaunit_v0_0_0,
    create_span_df,
    real_id_str,
    owner_id_str,
    acct_id_str,
    group_id_str,
    parent_road_str,
    label_str,
    mass_str,
    pledge_str,
    debtit_score_str,
    credit_score_str,
    debtit_vote_str,
    credit_vote_str,
    get_spanref,
    save_span_csv,
    open_span_csv,
    load_span_csv,
)
from src.span.examples.span_env import (
    span_examples_dir,
    span_reals_dir,
    span_env_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_open_span_csv_ReturnsObj():
    # ESTABLISH
    sue_text = sue_str()
    bob_text = bob_str()
    yao_text = yao_str()
    sue_credit_score = 11
    bob_credit_score = 13
    yao_credit_score = 41
    sue_debtit_score = 23
    bob_debtit_score = 29
    yao_debtit_score = 37
    music_real_id = "music56"
    sue_budunit = budunit_shop(sue_text, music_real_id)
    sue_budunit.add_acctunit(sue_text, sue_credit_score, sue_debtit_score)
    sue_budunit.add_acctunit(bob_text, bob_credit_score, bob_debtit_score)
    sue_budunit.add_acctunit(yao_text, yao_credit_score, yao_debtit_score)
    j1_spanname = jaar_format_00001_acct_v0_0_0()
    acct_filename = f"{sue_text}_acct_example_00.csv"
    save_span_csv(j1_spanname, sue_budunit, span_examples_dir(), acct_filename)

    # WHEN
    acct_dataframe = open_span_csv(span_examples_dir(), acct_filename)

    # THEN
    array_headers = list(acct_dataframe.columns)
    acct_spanref = get_spanref(j1_spanname)
    assert array_headers == acct_spanref.get_headers_list()
    assert acct_dataframe.loc[0, real_id_str()] == music_real_id
    assert acct_dataframe.loc[0, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[0, acct_id_str()] == bob_text
    assert acct_dataframe.loc[0, credit_score_str()] == bob_credit_score
    assert acct_dataframe.loc[0, debtit_score_str()] == bob_debtit_score

    assert acct_dataframe.loc[1, real_id_str()] == music_real_id
    assert acct_dataframe.loc[1, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[1, acct_id_str()] == sue_text
    assert acct_dataframe.loc[1, credit_score_str()] == sue_credit_score
    assert acct_dataframe.loc[1, debtit_score_str()] == sue_debtit_score

    assert acct_dataframe.loc[2, real_id_str()] == music_real_id
    assert acct_dataframe.loc[2, owner_id_str()] == sue_budunit._owner_id
    assert acct_dataframe.loc[2, acct_id_str()] == yao_text
    assert acct_dataframe.loc[2, credit_score_str()] == yao_credit_score
    assert acct_dataframe.loc[2, debtit_score_str()] == yao_debtit_score

    assert len(acct_dataframe) == 3


def test_save_span_csv_Arg_jaar_format_00001_acct_v0_0_0_SaveToCSV(
    span_env_setup_cleanup,
):
    # ESTABLISH
    sue_text = sue_str()
    bob_text = bob_str()
    yao_text = yao_str()
    sue_credit_score = 11
    bob_credit_score = 13
    yao_credit_score = 41
    sue_debtit_score = 23
    bob_debtit_score = 29
    yao_debtit_score = 37
    music_real_id = "music56"
    sue_budunit = budunit_shop(sue_text, music_real_id)
    sue_budunit.add_acctunit(sue_text, sue_credit_score, sue_debtit_score)
    sue_budunit.add_acctunit(bob_text, bob_credit_score, bob_debtit_score)
    sue_budunit.add_acctunit(yao_text, yao_credit_score, yao_debtit_score)
    j1_spanname = jaar_format_00001_acct_v0_0_0()
    acct_filename = f"{sue_text}_acct_example_00.csv"
    csv_example_path = f_path(span_examples_dir(), acct_filename)
    print(f"{csv_example_path}")
    delete_dir(csv_example_path)
    save_span_csv(j1_spanname, sue_budunit, span_examples_dir(), acct_filename)
    music_hubunit = hubunit_shop(span_reals_dir(), music_real_id, owner_id=sue_text)
    # Open RealUnit and confirm voice BudUnit does not exist
    assert not music_hubunit.voice_file_exists()

    # WHEN
    load_span_csv(
        reals_dir=music_hubunit.reals_dir,
        x_spanname=j1_spanname,
        x_file_dir=span_examples_dir(),
        x_filename=acct_filename,
    )

    # THEN
    # assert voice Budunit now exists
    assert music_hubunit.voice_file_exists()
    # assert voice Budunit acctunit now exists
    sue_voice = music_hubunit.get_voice_bud()
    assert sue_voice.acct_exists(sue_text)
    assert sue_voice.acct_exists(bob_text)
    assert sue_voice.acct_exists(yao_text)
    # assert voice Budunit acctunit.credit_score is correct
    sue_acctunit = sue_voice.get_acct(sue_text)
    bob_acctunit = sue_voice.get_acct(bob_text)
    yao_acctunit = sue_voice.get_acct(yao_text)
    # assert voice Budunit acctunit.credit_score is correct
    assert sue_acctunit.credit_score == sue_credit_score
    assert bob_acctunit.credit_score == bob_credit_score
    assert yao_acctunit.credit_score == yao_credit_score
    assert sue_acctunit.debtit_score == sue_debtit_score
    assert bob_acctunit.debtit_score == bob_debtit_score
    assert yao_acctunit.debtit_score == yao_debtit_score


# def test_create_span_df_Arg_jaar_format_00003_ideaunit_v0_0_0_Scenario_budunit_v001():
#     # ESTABLISH / WHEN
#     x_span_name = jaar_format_00003_ideaunit_v0_0_0()

#     # WHEN
#     ideaunit_format = create_span_df(budunit_v001(), x_span_name)

#     # THEN
#     array_headers = list(ideaunit_format.columns)
#     assert array_headers == get_spanref(x_span_name).get_headers_list()
#     assert len(ideaunit_format) == 252
