# from src.f00_instrument.db_toolbox import create_table_from_columns
from src.f09_idea.idea_config import get_idea_config_dict
from src.f09_idea.idea_db_tool import (
    create_idea_sorted_table,
    get_idea_into_dimen_staging_query,
    get_custom_sorted_list,
)
from sqlite3 import connect as sqlite3_connect


def test_get_idea_into_dimen_staging_query_ReturnsObj_Scenario0_bud_item_teamlink():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            "event_int",
            "face_name",
            "fiscal_title",
            "road",
            "team_tag",
            "owner_name",
            "acct_name",
            "amount",
        ]
        budteam_cat = "bud_item_teamlink"
        src_table = f"{idea_number}_staging"
        dst_table = f"{budteam_cat}_staging"
        idea_config = get_idea_config_dict()
        budteam_config = idea_config.get(budteam_cat)
        print(f"{budteam_cat=}")
        print(f"{budteam_config=}")
        budteam_jkeys = budteam_config.get("jkeys")
        budteam_jvals = budteam_config.get("jvalues")
        budteam_args = set(budteam_jkeys.keys()).union(set(budteam_jvals.keys()))
        budteam_args = get_custom_sorted_list(budteam_args)
        print(f"{budteam_jkeys=}")
        print(f"{budteam_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, dst_table, budteam_args)

        # WHEN
        gen_sqlstr = get_idea_into_dimen_staging_query(
            conn, idea_number, budteam_cat, budteam_jkeys
        )

        # THEN
        columns_str = "face_name, event_int, fiscal_title, owner_name, road, team_tag"
        expected_sqlstr = f"""INSERT INTO {budteam_cat}_staging (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_staging
WHERE face_name IS NOT NULL AND event_int IS NOT NULL AND fiscal_title IS NOT NULL AND owner_name IS NOT NULL AND road IS NOT NULL AND team_tag IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("")
        print(gen_sqlstr)
        print(expected_sqlstr)
        assert gen_sqlstr == expected_sqlstr


def test_get_idea_into_dimen_staging_query_ReturnsObj_Scenario1_bud_acctunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            "event_int",
            "face_name",
            "fiscal_title",
            "road",
            "team_tag",
            "owner_name",
            "acct_name",
            "credit_belief",
            "debtit_belief",
            "amount",
        ]
        budacct_cat = "bud_acctunit"
        src_table = f"{idea_number}_staging"
        budacct_table = f"{budacct_cat}_staging"
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
        gen_sqlstr = get_idea_into_dimen_staging_query(
            conn, idea_number, budacct_cat, budacct_jkeys
        )

        # THEN
        columns_str = "face_name, event_int, fiscal_title, owner_name, acct_name, credit_belief, debtit_belief"
        expected_sqlstr = f"""INSERT INTO {budacct_cat}_staging (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_staging
WHERE face_name IS NOT NULL AND event_int IS NOT NULL AND fiscal_title IS NOT NULL AND owner_name IS NOT NULL AND acct_name IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("")
        print(gen_sqlstr)
        print(expected_sqlstr)

        assert gen_sqlstr == expected_sqlstr


def test_get_idea_into_dimen_staging_query_ReturnsObj_Scenario2_bud_acctunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            "event_int",
            "face_name",
            "fiscal_title",
            "road",
            "team_tag",
            "owner_name",
            "acct_name",
            "credit_belief",
            "amount",
        ]
        budacct_cat = "bud_acctunit"
        src_table = f"{idea_number}_staging"
        budacct_table = f"{budacct_cat}_staging"
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
        gen_sqlstr = get_idea_into_dimen_staging_query(
            conn, idea_number, budacct_cat, budacct_jkeys
        )

        # THEN
        columns_str = (
            "face_name, event_int, fiscal_title, owner_name, acct_name, credit_belief"
        )
        expected_sqlstr = f"""INSERT INTO {budacct_cat}_staging (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_staging
WHERE face_name IS NOT NULL AND event_int IS NOT NULL AND fiscal_title IS NOT NULL AND owner_name IS NOT NULL AND acct_name IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("generated:")
        print(gen_sqlstr)
        print(expected_sqlstr)

        assert gen_sqlstr == expected_sqlstr
