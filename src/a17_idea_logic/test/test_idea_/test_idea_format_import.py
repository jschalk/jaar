from src.a06_believer_logic.believer import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    belief_label_str,
    believer_name_str,
    person_cred_points_str,
    person_debt_points_str,
    person_name_str,
)
from src.a17_idea_logic.idea import get_idearef_obj, save_idea_csv
from src.a17_idea_logic.idea_config import idea_format_00021_believer_personunit_v0_0_0
from src.a17_idea_logic.idea_db_tool import open_csv
from src.a17_idea_logic.test._util.a17_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_open_csv_ReturnsObjWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    sue_person_cred_points = 11
    bob_person_cred_points = 13
    yao_person_cred_points = 41
    sue_person_debt_points = 23
    bob_person_debt_points = 29
    yao_person_debt_points = 37
    amy_belief_label = "amy56"
    sue_believerunit = believerunit_shop(sue_str, amy_belief_label)
    sue_believerunit.add_personunit(
        sue_str, sue_person_cred_points, sue_person_debt_points
    )
    sue_believerunit.add_personunit(
        bob_str, bob_person_cred_points, bob_person_debt_points
    )
    sue_believerunit.add_personunit(
        yao_str, yao_person_cred_points, yao_person_debt_points
    )
    j1_ideaname = idea_format_00021_believer_personunit_v0_0_0()
    name_filename = f"{sue_str}_person_example_01.csv"
    save_idea_csv(j1_ideaname, sue_believerunit, get_module_temp_dir(), name_filename)

    # WHEN
    person_dataframe = open_csv(get_module_temp_dir(), name_filename)

    # THEN
    array_headers = list(person_dataframe.columns)
    person_idearef = get_idearef_obj(j1_ideaname)
    assert array_headers == person_idearef.get_headers_list()
    assert person_dataframe.loc[0, belief_label_str()] == amy_belief_label
    assert (
        person_dataframe.loc[0, believer_name_str()] == sue_believerunit.believer_name
    )
    assert person_dataframe.loc[0, person_name_str()] == bob_str
    assert person_dataframe.loc[0, person_cred_points_str()] == bob_person_cred_points
    assert person_dataframe.loc[0, person_debt_points_str()] == bob_person_debt_points

    assert person_dataframe.loc[1, belief_label_str()] == amy_belief_label
    assert (
        person_dataframe.loc[1, believer_name_str()] == sue_believerunit.believer_name
    )
    assert person_dataframe.loc[1, person_name_str()] == sue_str
    assert person_dataframe.loc[1, person_cred_points_str()] == sue_person_cred_points
    assert person_dataframe.loc[1, person_debt_points_str()] == sue_person_debt_points

    assert person_dataframe.loc[2, belief_label_str()] == amy_belief_label
    assert (
        person_dataframe.loc[2, believer_name_str()] == sue_believerunit.believer_name
    )
    assert person_dataframe.loc[2, person_name_str()] == yao_str
    assert person_dataframe.loc[2, person_cred_points_str()] == yao_person_cred_points
    assert person_dataframe.loc[2, person_debt_points_str()] == yao_person_debt_points

    assert len(person_dataframe) == 3


def test_open_csv_ReturnsObjWhenNoFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    name_filename = f"{sue_str}_person_example_77.csv"

    # WHEN
    person_dataframe = open_csv(get_module_temp_dir(), name_filename)

    # THEN
    assert person_dataframe is None
