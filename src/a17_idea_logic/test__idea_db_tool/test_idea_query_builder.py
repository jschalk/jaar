from src.a02_finance_logic._utils.strs_a02 import fisc_tag_str, owner_name_str
from src.a06_bud_logic._utils.str_a06 import (
    event_int_str,
    face_name_str,
    road_str,
    team_title_str,
    acct_name_str,
    credit_belief_str,
    debtit_belief_str,
)
from src.a15_fisc_logic.fisc_config import amount_str
from src.a17_idea_logic.idea_config import get_idea_config_dict
from src.a17_idea_logic.idea_db_tool import (
    create_idea_sorted_table,
    get_idea_into_dimen_raw_query,
    get_default_sorted_list,
)
from sqlite3 import connect as sqlite3_connect


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario0_bud_item_teamlink():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            event_int_str(),
            face_name_str(),
            fisc_tag_str(),
            road_str(),
            team_title_str(),
            owner_name_str(),
            acct_name_str(),
            amount_str(),
        ]
        budteam_cat = "bud_item_teamlink"
        src_table = f"{idea_number}_raw"
        dst_table = f"{budteam_cat}_raw"
        idea_config = get_idea_config_dict()
        budteam_config = idea_config.get(budteam_cat)
        print(f"{budteam_cat=}")
        print(f"{budteam_config=}")
        budteam_jkeys = budteam_config.get("jkeys")
        budteam_jvals = budteam_config.get("jvalues")
        budteam_args = set(budteam_jkeys.keys()).union(set(budteam_jvals.keys()))
        budteam_args = get_default_sorted_list(budteam_args)
        print(f"{budteam_jkeys=}")
        print(f"{budteam_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, dst_table, budteam_args)

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, budteam_cat, budteam_jkeys
        )

        # THEN
        columns_str = "face_name, event_int, fisc_tag, owner_name, road, team_title"
        expected_sqlstr = f"""INSERT INTO {budteam_cat}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE face_name IS NOT NULL AND event_int IS NOT NULL AND fisc_tag IS NOT NULL AND owner_name IS NOT NULL AND road IS NOT NULL AND team_title IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("")
        print(gen_sqlstr)
        print(expected_sqlstr)
        assert gen_sqlstr == expected_sqlstr


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario1_bud_acctunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            event_int_str(),
            face_name_str(),
            fisc_tag_str(),
            road_str(),
            team_title_str(),
            owner_name_str(),
            acct_name_str(),
            credit_belief_str(),
            debtit_belief_str(),
            amount_str(),
        ]
        budacct_cat = "bud_acctunit"
        src_table = f"{idea_number}_raw"
        budacct_table = f"{budacct_cat}_raw"
        idea_config = get_idea_config_dict()
        budacct_config = idea_config.get(budacct_cat)
        budacct_jkeys = budacct_config.get("jkeys")
        budacct_jvals = budacct_config.get("jvalues")
        budacct_args = set(budacct_jkeys.keys()).union(set(budacct_jvals.keys()))
        print(f"{budacct_jkeys=}")
        print(f"{budacct_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, budacct_table, list(budacct_args))

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, budacct_cat, budacct_jkeys
        )

        # THEN
        columns_str = "face_name, event_int, fisc_tag, owner_name, acct_name, credit_belief, debtit_belief"
        expected_sqlstr = f"""INSERT INTO {budacct_cat}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE face_name IS NOT NULL AND event_int IS NOT NULL AND fisc_tag IS NOT NULL AND owner_name IS NOT NULL AND acct_name IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("")
        print(gen_sqlstr)
        print(expected_sqlstr)

        assert gen_sqlstr == expected_sqlstr


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario2_bud_acctunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            event_int_str(),
            face_name_str(),
            fisc_tag_str(),
            road_str(),
            team_title_str(),
            owner_name_str(),
            acct_name_str(),
            credit_belief_str(),
            amount_str(),
        ]
        budacct_cat = "bud_acctunit"
        src_table = f"{idea_number}_raw"
        budacct_table = f"{budacct_cat}_raw"
        idea_config = get_idea_config_dict()
        budacct_config = idea_config.get(budacct_cat)
        budacct_jkeys = budacct_config.get("jkeys")
        budacct_jvals = budacct_config.get("jvalues")
        budacct_args = set(budacct_jkeys.keys()).union(set(budacct_jvals.keys()))
        print(f"{budacct_jkeys=}")
        print(f"{budacct_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, budacct_table, list(budacct_args))

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, budacct_cat, budacct_jkeys
        )

        # THEN
        columns_str = (
            "face_name, event_int, fisc_tag, owner_name, acct_name, credit_belief"
        )
        expected_sqlstr = f"""INSERT INTO {budacct_cat}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE face_name IS NOT NULL AND event_int IS NOT NULL AND fisc_tag IS NOT NULL AND owner_name IS NOT NULL AND acct_name IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("generated:")
        print(gen_sqlstr)
        print(expected_sqlstr)

        assert gen_sqlstr == expected_sqlstr
