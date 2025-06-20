from sqlite3 import connect as sqlite3_connect
from src.a02_finance_logic.test._util.a02_str import owner_name_str, vow_label_str
from src.a06_plan_logic.test._util.a06_str import (
    acct_name_str,
    concept_rope_str,
    credit_score_str,
    debt_score_str,
    labor_title_str,
)
from src.a09_pack_logic.test._util.a09_str import event_int_str, face_name_str
from src.a15_vow_logic.test._util.a15_str import amount_str
from src.a17_idea_logic.idea_config import get_idea_config_dict
from src.a17_idea_logic.idea_db_tool import (
    create_idea_sorted_table,
    get_default_sorted_list,
    get_idea_into_dimen_raw_query,
)


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario0_plan_concept_laborlink():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            event_int_str(),
            face_name_str(),
            vow_label_str(),
            concept_rope_str(),
            labor_title_str(),
            owner_name_str(),
            acct_name_str(),
            amount_str(),
        ]
        plnlabo_cat = "plan_concept_laborlink"
        src_table = f"{idea_number}_raw"
        dst_table = f"{plnlabo_cat}_raw"
        idea_config = get_idea_config_dict()
        plnlabo_config = idea_config.get(plnlabo_cat)
        print(f"{plnlabo_cat=}")
        print(f"{plnlabo_config=}")
        plnlabo_jkeys = plnlabo_config.get("jkeys")
        plnlabo_jvals = plnlabo_config.get("jvalues")
        plnlabo_args = set(plnlabo_jkeys.keys()).union(set(plnlabo_jvals.keys()))
        plnlabo_args = get_default_sorted_list(plnlabo_args)
        print(f"{plnlabo_jkeys=}")
        print(f"{plnlabo_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, dst_table, plnlabo_args)

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, plnlabo_cat, plnlabo_jkeys
        )

        # THEN
        columns_str = (
            "event_int, face_name, vow_label, owner_name, concept_rope, labor_title"
        )
        expected_sqlstr = f"""INSERT INTO {plnlabo_cat}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE event_int IS NOT NULL AND face_name IS NOT NULL AND vow_label IS NOT NULL AND owner_name IS NOT NULL AND concept_rope IS NOT NULL AND labor_title IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("")
        print(gen_sqlstr)
        print(expected_sqlstr)
        assert gen_sqlstr == expected_sqlstr


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario1_plan_acctunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            event_int_str(),
            face_name_str(),
            vow_label_str(),
            concept_rope_str(),
            labor_title_str(),
            owner_name_str(),
            acct_name_str(),
            credit_score_str(),
            debt_score_str(),
            amount_str(),
        ]
        plnacct_cat = "plan_acctunit"
        src_table = f"{idea_number}_raw"
        plnacct_table = f"{plnacct_cat}_raw"
        idea_config = get_idea_config_dict()
        plnacct_config = idea_config.get(plnacct_cat)
        plnacct_jkeys = plnacct_config.get("jkeys")
        plnacct_jvals = plnacct_config.get("jvalues")
        plnacct_args = set(plnacct_jkeys.keys()).union(set(plnacct_jvals.keys()))
        print(f"{plnacct_jkeys=}")
        print(f"{plnacct_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, plnacct_table, list(plnacct_args))

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, plnacct_cat, plnacct_jkeys
        )

        # THEN
        columns_str = "event_int, face_name, vow_label, owner_name, acct_name, credit_score, debt_score"
        expected_sqlstr = f"""INSERT INTO {plnacct_cat}_raw (idea_number, {columns_str})
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


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario2_plan_acctunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            event_int_str(),
            face_name_str(),
            vow_label_str(),
            concept_rope_str(),
            labor_title_str(),
            owner_name_str(),
            acct_name_str(),
            credit_score_str(),
            amount_str(),
        ]
        plnacct_cat = "plan_acctunit"
        src_table = f"{idea_number}_raw"
        plnacct_table = f"{plnacct_cat}_raw"
        idea_config = get_idea_config_dict()
        plnacct_config = idea_config.get(plnacct_cat)
        plnacct_jkeys = plnacct_config.get("jkeys")
        plnacct_jvals = plnacct_config.get("jvalues")
        plnacct_args = set(plnacct_jkeys.keys()).union(set(plnacct_jvals.keys()))
        print(f"{plnacct_jkeys=}")
        print(f"{plnacct_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, plnacct_table, list(plnacct_args))

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, plnacct_cat, plnacct_jkeys
        )

        # THEN
        columns_str = (
            "event_int, face_name, vow_label, owner_name, acct_name, credit_score"
        )
        expected_sqlstr = f"""INSERT INTO {plnacct_cat}_raw (idea_number, {columns_str})
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
