from sqlite3 import connect as sqlite3_connect
from src.a06_believer_logic.test._util.a06_str import (
    acct_cred_points_str,
    acct_debt_points_str,
    acct_name_str,
    belief_label_str,
    believer_name_str,
    labor_title_str,
    plan_rope_str,
)
from src.a09_pack_logic.test._util.a09_str import event_int_str, face_name_str
from src.a15_belief_logic.test._util.a15_str import amount_str
from src.a17_idea_logic.idea_config import get_idea_config_dict
from src.a17_idea_logic.idea_db_tool import (
    create_idea_sorted_table,
    get_default_sorted_list,
    get_idea_into_dimen_raw_query,
)


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario0_believer_plan_laborlink():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            event_int_str(),
            face_name_str(),
            belief_label_str(),
            plan_rope_str(),
            labor_title_str(),
            believer_name_str(),
            acct_name_str(),
            amount_str(),
        ]
        onrlabo_cat = "believer_plan_laborlink"
        src_table = f"{idea_number}_raw"
        dst_table = f"{onrlabo_cat}_raw"
        idea_config = get_idea_config_dict()
        onrlabo_config = idea_config.get(onrlabo_cat)
        print(f"{onrlabo_cat=}")
        print(f"{onrlabo_config=}")
        onrlabo_jkeys = onrlabo_config.get("jkeys")
        onrlabo_jvals = onrlabo_config.get("jvalues")
        onrlabo_args = set(onrlabo_jkeys.keys()).union(set(onrlabo_jvals.keys()))
        onrlabo_args = get_default_sorted_list(onrlabo_args)
        print(f"{onrlabo_jkeys=}")
        print(f"{onrlabo_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, dst_table, onrlabo_args)

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, onrlabo_cat, onrlabo_jkeys
        )

        # THEN
        columns_str = (
            "event_int, face_name, belief_label, believer_name, plan_rope, labor_title"
        )
        expected_sqlstr = f"""INSERT INTO {onrlabo_cat}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE event_int IS NOT NULL AND face_name IS NOT NULL AND belief_label IS NOT NULL AND believer_name IS NOT NULL AND plan_rope IS NOT NULL AND labor_title IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("")
        print(gen_sqlstr)
        print(expected_sqlstr)
        assert gen_sqlstr == expected_sqlstr


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario1_believer_acctunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            event_int_str(),
            face_name_str(),
            belief_label_str(),
            plan_rope_str(),
            labor_title_str(),
            believer_name_str(),
            acct_name_str(),
            acct_cred_points_str(),
            acct_debt_points_str(),
            amount_str(),
        ]
        onracct_cat = "believer_acctunit"
        src_table = f"{idea_number}_raw"
        onracct_table = f"{onracct_cat}_raw"
        idea_config = get_idea_config_dict()
        onracct_config = idea_config.get(onracct_cat)
        onracct_jkeys = onracct_config.get("jkeys")
        onracct_jvals = onracct_config.get("jvalues")
        onracct_args = set(onracct_jkeys.keys()).union(set(onracct_jvals.keys()))
        print(f"{onracct_jkeys=}")
        print(f"{onracct_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, onracct_table, list(onracct_args))

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, onracct_cat, onracct_jkeys
        )

        # THEN
        columns_str = "event_int, face_name, belief_label, believer_name, acct_name, acct_cred_points, acct_debt_points"
        expected_sqlstr = f"""INSERT INTO {onracct_cat}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE event_int IS NOT NULL AND face_name IS NOT NULL AND belief_label IS NOT NULL AND believer_name IS NOT NULL AND acct_name IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("")
        print(gen_sqlstr)
        print(expected_sqlstr)

        assert gen_sqlstr == expected_sqlstr


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario2_believer_acctunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            event_int_str(),
            face_name_str(),
            belief_label_str(),
            plan_rope_str(),
            labor_title_str(),
            believer_name_str(),
            acct_name_str(),
            acct_cred_points_str(),
            amount_str(),
        ]
        onracct_cat = "believer_acctunit"
        src_table = f"{idea_number}_raw"
        onracct_table = f"{onracct_cat}_raw"
        idea_config = get_idea_config_dict()
        onracct_config = idea_config.get(onracct_cat)
        onracct_jkeys = onracct_config.get("jkeys")
        onracct_jvals = onracct_config.get("jvalues")
        onracct_args = set(onracct_jkeys.keys()).union(set(onracct_jvals.keys()))
        print(f"{onracct_jkeys=}")
        print(f"{onracct_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, onracct_table, list(onracct_args))

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, onracct_cat, onracct_jkeys
        )

        # THEN
        columns_str = "event_int, face_name, belief_label, believer_name, acct_name, acct_cred_points"
        expected_sqlstr = f"""INSERT INTO {onracct_cat}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE event_int IS NOT NULL AND face_name IS NOT NULL AND belief_label IS NOT NULL AND believer_name IS NOT NULL AND acct_name IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("generated:")
        print(gen_sqlstr)
        print(expected_sqlstr)

        assert gen_sqlstr == expected_sqlstr
