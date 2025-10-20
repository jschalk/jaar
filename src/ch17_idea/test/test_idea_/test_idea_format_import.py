from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch17_idea.idea_config import idea_format_00021_belief_voiceunit_v0_0_0
from src.ch17_idea.idea_db_tool import open_csv
from src.ch17_idea.idea_main import get_idearef_obj, save_idea_csv
from src.ch17_idea.test._util.ch17_env import get_temp_dir, temp_dir_setup
from src.ref.keywords import Ch17Keywords as kw


def test_open_csv_ReturnsObjWhenFileExists(temp_dir_setup):
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    sue_voice_cred_lumen = 11
    bob_voice_cred_lumen = 13
    yao_voice_cred_lumen = 41
    sue_voice_debt_lumen = 23
    bob_voice_debt_lumen = 29
    yao_voice_debt_lumen = 37
    amy_moment_label = "amy56"
    sue_beliefunit = beliefunit_shop(sue_str, amy_moment_label)
    sue_beliefunit.add_voiceunit(sue_str, sue_voice_cred_lumen, sue_voice_debt_lumen)
    sue_beliefunit.add_voiceunit(bob_str, bob_voice_cred_lumen, bob_voice_debt_lumen)
    sue_beliefunit.add_voiceunit(yao_str, yao_voice_cred_lumen, yao_voice_debt_lumen)
    j1_ideaname = idea_format_00021_belief_voiceunit_v0_0_0()
    name_filename = f"{sue_str}_voice_example_01.csv"
    save_idea_csv(j1_ideaname, sue_beliefunit, get_temp_dir(), name_filename)

    # WHEN
    voice_dataframe = open_csv(get_temp_dir(), name_filename)

    # THEN
    array_headers = list(voice_dataframe.columns)
    voice_idearef = get_idearef_obj(j1_ideaname)
    assert array_headers == voice_idearef.get_headers_list()
    assert voice_dataframe.loc[0, kw.moment_label] == amy_moment_label
    assert voice_dataframe.loc[0, kw.belief_name] == sue_beliefunit.belief_name
    assert voice_dataframe.loc[0, kw.voice_name] == bob_str
    assert voice_dataframe.loc[0, kw.voice_cred_lumen] == bob_voice_cred_lumen
    assert voice_dataframe.loc[0, kw.voice_debt_lumen] == bob_voice_debt_lumen

    assert voice_dataframe.loc[1, kw.moment_label] == amy_moment_label
    assert voice_dataframe.loc[1, kw.belief_name] == sue_beliefunit.belief_name
    assert voice_dataframe.loc[1, kw.voice_name] == sue_str
    assert voice_dataframe.loc[1, kw.voice_cred_lumen] == sue_voice_cred_lumen
    assert voice_dataframe.loc[1, kw.voice_debt_lumen] == sue_voice_debt_lumen

    assert voice_dataframe.loc[2, kw.moment_label] == amy_moment_label
    assert voice_dataframe.loc[2, kw.belief_name] == sue_beliefunit.belief_name
    assert voice_dataframe.loc[2, kw.voice_name] == yao_str
    assert voice_dataframe.loc[2, kw.voice_cred_lumen] == yao_voice_cred_lumen
    assert voice_dataframe.loc[2, kw.voice_debt_lumen] == yao_voice_debt_lumen

    assert len(voice_dataframe) == 3


def test_open_csv_ReturnsObjWhenNoFileExists(temp_dir_setup):
    # ESTABLISH
    sue_str = "Sue"
    name_filename = f"{sue_str}_voice_example_77.csv"

    # WHEN
    voice_dataframe = open_csv(get_temp_dir(), name_filename)

    # THEN
    assert voice_dataframe is None
