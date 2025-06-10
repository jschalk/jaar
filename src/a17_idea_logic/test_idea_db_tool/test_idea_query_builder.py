from sqlite3 import connect as sqlite3_connect
from src.a02_finance_logic._test_util.a02_str import owner_name_str, vow_label_str
from src.a06_plan_logic._test_util.a06_str import (
    acct_name_str,
    concept_way_str,
    credit_score_str,
    debtit_score_str,
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


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario0_plan_concept_laborlink():
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
        planlabo_cat = "plan_concept_laborlink"
        src_table = f"{idea_number}_raw"
        dst_table = f"{planlabo_cat}_raw"
        idea_config = get_idea_config_dict()
        planlabo_config = idea_config.get(planlabo_cat)
        print(f"{planlabo_cat=}")
        print(f"{planlabo_config=}")
        planlabo_jkeys = planlabo_config.get("jkeys")
        planlabo_jvals = planlabo_config.get("jvalues")
        planlabo_args = set(planlabo_jkeys.keys()).union(set(planlabo_jvals.keys()))
        planlabo_args = get_default_sorted_list(planlabo_args)
        print(f"{planlabo_jkeys=}")
        print(f"{planlabo_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, dst_table, planlabo_args)

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, planlabo_cat, planlabo_jkeys
        )

        # THEN
        columns_str = (
            "event_int, face_name, vow_label, owner_name, concept_way, labor_title"
        )
        expected_sqlstr = f"""INSERT INTO {planlabo_cat}_raw (idea_number, {columns_str})
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


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario1_plan_acctunit():
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
            credit_score_str(),
            debtit_score_str(),
            amount_str(),
        ]
        planacct_cat = "plan_acctunit"
        src_table = f"{idea_number}_raw"
        planacct_table = f"{planacct_cat}_raw"
        idea_config = get_idea_config_dict()
        planacct_config = idea_config.get(planacct_cat)
        planacct_jkeys = planacct_config.get("jkeys")
        planacct_jvals = planacct_config.get("jvalues")
        planacct_args = set(planacct_jkeys.keys()).union(set(planacct_jvals.keys()))
        print(f"{planacct_jkeys=}")
        print(f"{planacct_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, planacct_table, list(planacct_args))

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, planacct_cat, planacct_jkeys
        )

        # THEN
        columns_str = "event_int, face_name, vow_label, owner_name, acct_name, credit_score, debtit_score"
        expected_sqlstr = f"""INSERT INTO {planacct_cat}_raw (idea_number, {columns_str})
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
            concept_way_str(),
            labor_title_str(),
            owner_name_str(),
            acct_name_str(),
            credit_score_str(),
            amount_str(),
        ]
        planacct_cat = "plan_acctunit"
        src_table = f"{idea_number}_raw"
        planacct_table = f"{planacct_cat}_raw"
        idea_config = get_idea_config_dict()
        planacct_config = idea_config.get(planacct_cat)
        planacct_jkeys = planacct_config.get("jkeys")
        planacct_jvals = planacct_config.get("jvalues")
        planacct_args = set(planacct_jkeys.keys()).union(set(planacct_jvals.keys()))
        print(f"{planacct_jkeys=}")
        print(f"{planacct_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, planacct_table, list(planacct_args))

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, planacct_cat, planacct_jkeys
        )

        # THEN
        columns_str = (
            "event_int, face_name, vow_label, owner_name, acct_name, credit_score"
        )
        expected_sqlstr = f"""INSERT INTO {planacct_cat}_raw (idea_number, {columns_str})
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
