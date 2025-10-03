from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch17_idea_logic.idea_config import idea_format_00021_belief_voiceunit_v0_0_0
from src.ch17_idea_logic.idea_db_tool import open_csv
from src.ch17_idea_logic.idea_main import get_idearef_obj, save_idea_csv
from src.ch17_idea_logic.test._util.ch17_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)
from src.ref.ch17_keywords import Ch17Keywords as wx


def test_open_csv_ReturnsObjWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    sue_voice_cred_points = 11
    bob_voice_cred_points = 13
    yao_voice_cred_points = 41
    sue_voice_debt_points = 23
    bob_voice_debt_points = 29
    yao_voice_debt_points = 37
    amy_moment_label = "amy56"
    sue_beliefunit = beliefunit_shop(sue_str, amy_moment_label)
    sue_beliefunit.add_voiceunit(sue_str, sue_voice_cred_points, sue_voice_debt_points)
    sue_beliefunit.add_voiceunit(bob_str, bob_voice_cred_points, bob_voice_debt_points)
    sue_beliefunit.add_voiceunit(yao_str, yao_voice_cred_points, yao_voice_debt_points)
    j1_ideaname = idea_format_00021_belief_voiceunit_v0_0_0()
    name_filename = f"{sue_str}_voice_example_01.csv"
    save_idea_csv(j1_ideaname, sue_beliefunit, get_chapter_temp_dir(), name_filename)

    # WHEN
    voice_dataframe = open_csv(get_chapter_temp_dir(), name_filename)

    # THEN
    array_headers = list(voice_dataframe.columns)
    voice_idearef = get_idearef_obj(j1_ideaname)
    assert array_headers == voice_idearef.get_headers_list()
    assert voice_dataframe.loc[0, wx.moment_label] == amy_moment_label
    assert voice_dataframe.loc[0, wx.belief_name] == sue_beliefunit.belief_name
    assert voice_dataframe.loc[0, wx.voice_name] == bob_str
    assert voice_dataframe.loc[0, wx.voice_cred_points] == bob_voice_cred_points
    assert voice_dataframe.loc[0, wx.voice_debt_points] == bob_voice_debt_points

    assert voice_dataframe.loc[1, wx.moment_label] == amy_moment_label
    assert voice_dataframe.loc[1, wx.belief_name] == sue_beliefunit.belief_name
    assert voice_dataframe.loc[1, wx.voice_name] == sue_str
    assert voice_dataframe.loc[1, wx.voice_cred_points] == sue_voice_cred_points
    assert voice_dataframe.loc[1, wx.voice_debt_points] == sue_voice_debt_points

    assert voice_dataframe.loc[2, wx.moment_label] == amy_moment_label
    assert voice_dataframe.loc[2, wx.belief_name] == sue_beliefunit.belief_name
    assert voice_dataframe.loc[2, wx.voice_name] == yao_str
    assert voice_dataframe.loc[2, wx.voice_cred_points] == yao_voice_cred_points
    assert voice_dataframe.loc[2, wx.voice_debt_points] == yao_voice_debt_points

    assert len(voice_dataframe) == 3


def test_open_csv_ReturnsObjWhenNoFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    name_filename = f"{sue_str}_voice_example_77.csv"

    # WHEN
    voice_dataframe = open_csv(get_chapter_temp_dir(), name_filename)

    # THEN
    assert voice_dataframe is None
