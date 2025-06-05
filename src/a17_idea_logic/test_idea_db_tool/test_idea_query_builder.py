from sqlite3 import connect as sqlite3_connect
from src.a02_finance_logic._test_util.a02_str import owner_name_str, vow_label_str
from src.a06_bud_logic._test_util.a06_str import (
    acct_name_str,
    concept_way_str,
    credit_belief_str,
    debtit_belief_str,
    labor_title_str,
)
from src.a09_pack_logic._test_util.a09_str import event_int_str, face_name_str
from src.a15_vow_logic._test_util.a15_str import amount_str
from src.a17_idea_logic.idea_config import get_idea_config_dict
from src.a17_idea_logic.idea_db_tool import (
    create_idea_sorted_table,
    get_default_sorted_list,
    get_idea_into_dimen_raw_query,
)


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario0_bud_concept_laborlink():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            event_int_str(),
            face_name_str(),
            vow_label_str(),
            concept_way_str(),
            labor_title_str(),
            owner_name_str(),
            acct_name_str(),
            amount_str(),
        ]
        budlabo_cat = "bud_concept_laborlink"
        src_table = f"{idea_number}_raw"
        dst_table = f"{budlabo_cat}_raw"
        idea_config = get_idea_config_dict()
        budlabo_config = idea_config.get(budlabo_cat)
        print(f"{budlabo_cat=}")
        print(f"{budlabo_config=}")
        budlabo_jkeys = budlabo_config.get("jkeys")
        budlabo_jvals = budlabo_config.get("jvalues")
        budlabo_args = set(budlabo_jkeys.keys()).union(set(budlabo_jvals.keys()))
        budlabo_args = get_default_sorted_list(budlabo_args)
        print(f"{budlabo_jkeys=}")
        print(f"{budlabo_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, dst_table, budlabo_args)

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, budlabo_cat, budlabo_jkeys
        )

        # THEN
        columns_str = (
            "event_int, face_name, vow_label, owner_name, concept_way, labor_title"
        )
        expected_sqlstr = f"""INSERT INTO {budlabo_cat}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE event_int IS NOT NULL AND face_name IS NOT NULL AND vow_label IS NOT NULL AND owner_name IS NOT NULL AND concept_way IS NOT NULL AND labor_title IS NOT NULL
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
            vow_label_str(),
            concept_way_str(),
            labor_title_str(),
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
        columns_str = "event_int, face_name, vow_label, owner_name, acct_name, credit_belief, debtit_belief"
        expected_sqlstr = f"""INSERT INTO {budacct_cat}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE event_int IS NOT NULL AND face_name IS NOT NULL AND vow_label IS NOT NULL AND owner_name IS NOT NULL AND acct_name IS NOT NULL
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
            vow_label_str(),
            concept_way_str(),
            labor_title_str(),
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
            "event_int, face_name, vow_label, owner_name, acct_name, credit_belief"
        )
        expected_sqlstr = f"""INSERT INTO {budacct_cat}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE event_int IS NOT NULL AND face_name IS NOT NULL AND vow_label IS NOT NULL AND owner_name IS NOT NULL AND acct_name IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("generated:")
        print(gen_sqlstr)
        print(expected_sqlstr)

        assert gen_sqlstr == expected_sqlstr
