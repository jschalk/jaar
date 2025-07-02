from sqlite3 import connect as sqlite3_connect
from src.a06_owner_logic.test._util.a06_str import (
    acct_cred_points_str,
    acct_debt_points_str,
    acct_name_str,
    belief_label_str,
    labor_title_str,
    owner_name_str,
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


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario0_owner_plan_laborlink():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            event_int_str(),
            face_name_str(),
            belief_label_str(),
            plan_rope_str(),
            labor_title_str(),
            owner_name_str(),
            acct_name_str(),
            amount_str(),
        ]
        plnlabo_cat = "owner_plan_laborlink"
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
            "event_int, face_name, belief_label, owner_name, plan_rope, labor_title"
        )
        expected_sqlstr = f"""INSERT INTO {plnlabo_cat}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE event_int IS NOT NULL AND face_name IS NOT NULL AND belief_label IS NOT NULL AND owner_name IS NOT NULL AND plan_rope IS NOT NULL AND labor_title IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("")
        print(gen_sqlstr)
        print(expected_sqlstr)
        assert gen_sqlstr == expected_sqlstr


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario1_owner_acctunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            event_int_str(),
            face_name_str(),
            belief_label_str(),
            plan_rope_str(),
            labor_title_str(),
            owner_name_str(),
            acct_name_str(),
            acct_cred_points_str(),
            acct_debt_points_str(),
            amount_str(),
        ]
        plnacct_cat = "owner_acctunit"
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
        columns_str = "event_int, face_name, belief_label, owner_name, acct_name, acct_cred_points, acct_debt_points"
        expected_sqlstr = f"""INSERT INTO {plnacct_cat}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE event_int IS NOT NULL AND face_name IS NOT NULL AND belief_label IS NOT NULL AND owner_name IS NOT NULL AND acct_name IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("")
        print(gen_sqlstr)
        print(expected_sqlstr)

        assert gen_sqlstr == expected_sqlstr


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario2_owner_acctunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            event_int_str(),
            face_name_str(),
            belief_label_str(),
            plan_rope_str(),
            labor_title_str(),
            owner_name_str(),
            acct_name_str(),
            acct_cred_points_str(),
            amount_str(),
        ]
        plnacct_cat = "owner_acctunit"
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
        columns_str = "event_int, face_name, belief_label, owner_name, acct_name, acct_cred_points"
        expected_sqlstr = f"""INSERT INTO {plnacct_cat}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE event_int IS NOT NULL AND face_name IS NOT NULL AND belief_label IS NOT NULL AND owner_name IS NOT NULL AND acct_name IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("generated:")
        print(gen_sqlstr)
        print(expected_sqlstr)

        assert gen_sqlstr == expected_sqlstr
