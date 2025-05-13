from src.a02_finance_logic._utils.strs_a02 import fisc_tag_str, owner_name_str
from src.a06_bud_logic._utils.str_a06 import (
    event_int_str,
    face_name_str,
    idea_way_str,
    labor_label_str,
    acct_name_str,
    credit_belief_str,
    debtit_belief_str,
)
from src.a15_fisc_logic._utils.str_a15 import amount_str
from src.a17_creed_logic.creed_config import get_creed_config_dict
from src.a17_creed_logic.creed_db_tool import (
    create_creed_sorted_table,
    get_creed_into_dimen_raw_query,
    get_default_sorted_list,
)
from sqlite3 import connect as sqlite3_connect


def test_get_creed_into_dimen_raw_query_ReturnsObj_Scenario0_bud_idea_laborlink():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        creed_number = "br000XX"
        creed_cols = [
            event_int_str(),
            face_name_str(),
            fisc_tag_str(),
            idea_way_str(),
            labor_label_str(),
            owner_name_str(),
            acct_name_str(),
            amount_str(),
        ]
        budlabor_cat = "bud_idea_laborlink"
        src_table = f"{creed_number}_raw"
        dst_table = f"{budlabor_cat}_raw"
        creed_config = get_creed_config_dict()
        budlabor_config = creed_config.get(budlabor_cat)
        print(f"{budlabor_cat=}")
        print(f"{budlabor_config=}")
        budlabor_jkeys = budlabor_config.get("jkeys")
        budlabor_jvals = budlabor_config.get("jvalues")
        budlabor_args = set(budlabor_jkeys.keys()).union(set(budlabor_jvals.keys()))
        budlabor_args = get_default_sorted_list(budlabor_args)
        print(f"{budlabor_jkeys=}")
        print(f"{budlabor_jvals=}")
        create_creed_sorted_table(conn, src_table, creed_cols)
        create_creed_sorted_table(conn, dst_table, budlabor_args)

        # WHEN
        gen_sqlstr = get_creed_into_dimen_raw_query(
            conn, creed_number, budlabor_cat, budlabor_jkeys
        )

        # THEN
        columns_str = (
            "event_int, face_name, fisc_tag, owner_name, idea_way, labor_label"
        )
        expected_sqlstr = f"""INSERT INTO {budlabor_cat}_raw (creed_number, {columns_str})
SELECT '{creed_number}' as creed_number, {columns_str}
FROM {creed_number}_raw
WHERE event_int IS NOT NULL AND face_name IS NOT NULL AND fisc_tag IS NOT NULL AND owner_name IS NOT NULL AND idea_way IS NOT NULL AND labor_label IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("")
        print(gen_sqlstr)
        print(expected_sqlstr)
        assert gen_sqlstr == expected_sqlstr


def test_get_creed_into_dimen_raw_query_ReturnsObj_Scenario1_bud_acctunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        creed_number = "br000XX"
        creed_cols = [
            event_int_str(),
            face_name_str(),
            fisc_tag_str(),
            idea_way_str(),
            labor_label_str(),
            owner_name_str(),
            acct_name_str(),
            credit_belief_str(),
            debtit_belief_str(),
            amount_str(),
        ]
        budacct_cat = "bud_acctunit"
        src_table = f"{creed_number}_raw"
        budacct_table = f"{budacct_cat}_raw"
        creed_config = get_creed_config_dict()
        budacct_config = creed_config.get(budacct_cat)
        budacct_jkeys = budacct_config.get("jkeys")
        budacct_jvals = budacct_config.get("jvalues")
        budacct_args = set(budacct_jkeys.keys()).union(set(budacct_jvals.keys()))
        print(f"{budacct_jkeys=}")
        print(f"{budacct_jvals=}")
        create_creed_sorted_table(conn, src_table, creed_cols)
        create_creed_sorted_table(conn, budacct_table, list(budacct_args))

        # WHEN
        gen_sqlstr = get_creed_into_dimen_raw_query(
            conn, creed_number, budacct_cat, budacct_jkeys
        )

        # THEN
        columns_str = "event_int, face_name, fisc_tag, owner_name, acct_name, credit_belief, debtit_belief"
        expected_sqlstr = f"""INSERT INTO {budacct_cat}_raw (creed_number, {columns_str})
SELECT '{creed_number}' as creed_number, {columns_str}
FROM {creed_number}_raw
WHERE event_int IS NOT NULL AND face_name IS NOT NULL AND fisc_tag IS NOT NULL AND owner_name IS NOT NULL AND acct_name IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("")
        print(gen_sqlstr)
        print(expected_sqlstr)

        assert gen_sqlstr == expected_sqlstr


def test_get_creed_into_dimen_raw_query_ReturnsObj_Scenario2_bud_acctunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        creed_number = "br000XX"
        creed_cols = [
            event_int_str(),
            face_name_str(),
            fisc_tag_str(),
            idea_way_str(),
            labor_label_str(),
            owner_name_str(),
            acct_name_str(),
            credit_belief_str(),
            amount_str(),
        ]
        budacct_cat = "bud_acctunit"
        src_table = f"{creed_number}_raw"
        budacct_table = f"{budacct_cat}_raw"
        creed_config = get_creed_config_dict()
        budacct_config = creed_config.get(budacct_cat)
        budacct_jkeys = budacct_config.get("jkeys")
        budacct_jvals = budacct_config.get("jvalues")
        budacct_args = set(budacct_jkeys.keys()).union(set(budacct_jvals.keys()))
        print(f"{budacct_jkeys=}")
        print(f"{budacct_jvals=}")
        create_creed_sorted_table(conn, src_table, creed_cols)
        create_creed_sorted_table(conn, budacct_table, list(budacct_args))

        # WHEN
        gen_sqlstr = get_creed_into_dimen_raw_query(
            conn, creed_number, budacct_cat, budacct_jkeys
        )

        # THEN
        columns_str = (
            "event_int, face_name, fisc_tag, owner_name, acct_name, credit_belief"
        )
        expected_sqlstr = f"""INSERT INTO {budacct_cat}_raw (creed_number, {columns_str})
SELECT '{creed_number}' as creed_number, {columns_str}
FROM {creed_number}_raw
WHERE event_int IS NOT NULL AND face_name IS NOT NULL AND fisc_tag IS NOT NULL AND owner_name IS NOT NULL AND acct_name IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("generated:")
        print(gen_sqlstr)
        print(expected_sqlstr)

        assert gen_sqlstr == expected_sqlstr
