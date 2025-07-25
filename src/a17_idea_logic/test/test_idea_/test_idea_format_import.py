from src.a06_believer_logic.believer import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    belief_label_str,
    believer_name_str,
    partner_cred_points_str,
    partner_debt_points_str,
    partner_name_str,
)
from src.a17_idea_logic.idea import get_idearef_obj, save_idea_csv
from src.a17_idea_logic.idea_config import idea_format_00021_believer_partnerunit_v0_0_0
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
    sue_partner_cred_points = 11
    bob_partner_cred_points = 13
    yao_partner_cred_points = 41
    sue_partner_debt_points = 23
    bob_partner_debt_points = 29
    yao_partner_debt_points = 37
    amy_belief_label = "amy56"
    sue_believerunit = believerunit_shop(sue_str, amy_belief_label)
    sue_believerunit.add_partnerunit(
        sue_str, sue_partner_cred_points, sue_partner_debt_points
    )
    sue_believerunit.add_partnerunit(
        bob_str, bob_partner_cred_points, bob_partner_debt_points
    )
    sue_believerunit.add_partnerunit(
        yao_str, yao_partner_cred_points, yao_partner_debt_points
    )
    j1_ideaname = idea_format_00021_believer_partnerunit_v0_0_0()
    name_filename = f"{sue_str}_partner_example_01.csv"
    save_idea_csv(j1_ideaname, sue_believerunit, get_module_temp_dir(), name_filename)

    # WHEN
    partner_dataframe = open_csv(get_module_temp_dir(), name_filename)

    # THEN
    array_headers = list(partner_dataframe.columns)
    partner_idearef = get_idearef_obj(j1_ideaname)
    assert array_headers == partner_idearef.get_headers_list()
    assert partner_dataframe.loc[0, belief_label_str()] == amy_belief_label
    assert (
        partner_dataframe.loc[0, believer_name_str()] == sue_believerunit.believer_name
    )
    assert partner_dataframe.loc[0, partner_name_str()] == bob_str
    assert (
        partner_dataframe.loc[0, partner_cred_points_str()] == bob_partner_cred_points
    )
    assert (
        partner_dataframe.loc[0, partner_debt_points_str()] == bob_partner_debt_points
    )

    assert partner_dataframe.loc[1, belief_label_str()] == amy_belief_label
    assert (
        partner_dataframe.loc[1, believer_name_str()] == sue_believerunit.believer_name
    )
    assert partner_dataframe.loc[1, partner_name_str()] == sue_str
    assert (
        partner_dataframe.loc[1, partner_cred_points_str()] == sue_partner_cred_points
    )
    assert (
        partner_dataframe.loc[1, partner_debt_points_str()] == sue_partner_debt_points
    )

    assert partner_dataframe.loc[2, belief_label_str()] == amy_belief_label
    assert (
        partner_dataframe.loc[2, believer_name_str()] == sue_believerunit.believer_name
    )
    assert partner_dataframe.loc[2, partner_name_str()] == yao_str
    assert (
        partner_dataframe.loc[2, partner_cred_points_str()] == yao_partner_cred_points
    )
    assert (
        partner_dataframe.loc[2, partner_debt_points_str()] == yao_partner_debt_points
    )

    assert len(partner_dataframe) == 3


def test_open_csv_ReturnsObjWhenNoFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    name_filename = f"{sue_str}_partner_example_77.csv"

    # WHEN
    partner_dataframe = open_csv(get_module_temp_dir(), name_filename)

    # THEN
    assert partner_dataframe is None
