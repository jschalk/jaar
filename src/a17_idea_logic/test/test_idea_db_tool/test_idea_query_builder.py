from sqlite3 import connect as sqlite3_connect
from src.a06_believer_logic.test._util.a06_str import (
    belief_label_str,
    believer_name_str,
    partner_cred_points_str,
    partner_debt_points_str,
    partner_name_str,
    party_title_str,
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


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario0_believer_plan_partyunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            event_int_str(),
            face_name_str(),
            belief_label_str(),
            plan_rope_str(),
            party_title_str(),
            believer_name_str(),
            partner_name_str(),
            amount_str(),
        ]
        blrlabo_cat = "believer_plan_partyunit"
        src_table = f"{idea_number}_raw"
        dst_table = f"{blrlabo_cat}_raw"
        idea_config = get_idea_config_dict()
        blrlabo_config = idea_config.get(blrlabo_cat)
        print(f"{blrlabo_cat=}")
        print(f"{blrlabo_config=}")
        blrlabo_jkeys = blrlabo_config.get("jkeys")
        blrlabo_jvals = blrlabo_config.get("jvalues")
        blrlabo_args = set(blrlabo_jkeys.keys()).union(set(blrlabo_jvals.keys()))
        blrlabo_args = get_default_sorted_list(blrlabo_args)
        print(f"{blrlabo_jkeys=}")
        print(f"{blrlabo_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, dst_table, blrlabo_args)

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, blrlabo_cat, blrlabo_jkeys
        )

        # THEN
        columns_str = (
            "event_int, face_name, belief_label, believer_name, plan_rope, party_title"
        )
        expected_sqlstr = f"""INSERT INTO {blrlabo_cat}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE event_int IS NOT NULL AND face_name IS NOT NULL AND belief_label IS NOT NULL AND believer_name IS NOT NULL AND plan_rope IS NOT NULL AND party_title IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("")
        print(gen_sqlstr)
        print(expected_sqlstr)
        assert gen_sqlstr == expected_sqlstr


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario1_believer_partnerunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            event_int_str(),
            face_name_str(),
            belief_label_str(),
            plan_rope_str(),
            party_title_str(),
            believer_name_str(),
            partner_name_str(),
            partner_cred_points_str(),
            partner_debt_points_str(),
            amount_str(),
        ]
        blrpern_cat = "believer_partnerunit"
        src_table = f"{idea_number}_raw"
        blrpern_table = f"{blrpern_cat}_raw"
        idea_config = get_idea_config_dict()
        blrpern_config = idea_config.get(blrpern_cat)
        blrpern_jkeys = blrpern_config.get("jkeys")
        blrpern_jvals = blrpern_config.get("jvalues")
        blrpern_args = set(blrpern_jkeys.keys()).union(set(blrpern_jvals.keys()))
        print(f"{blrpern_jkeys=}")
        print(f"{blrpern_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, blrpern_table, list(blrpern_args))

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, blrpern_cat, blrpern_jkeys
        )

        # THEN
        columns_str = "event_int, face_name, belief_label, believer_name, partner_name, partner_cred_points, partner_debt_points"
        expected_sqlstr = f"""INSERT INTO {blrpern_cat}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE event_int IS NOT NULL AND face_name IS NOT NULL AND belief_label IS NOT NULL AND believer_name IS NOT NULL AND partner_name IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("")
        print(gen_sqlstr)
        print(expected_sqlstr)

        assert gen_sqlstr == expected_sqlstr


def test_get_idea_into_dimen_raw_query_ReturnsObj_Scenario2_believer_partnerunit():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        idea_number = "br000XX"
        idea_cols = [
            event_int_str(),
            face_name_str(),
            belief_label_str(),
            plan_rope_str(),
            party_title_str(),
            believer_name_str(),
            partner_name_str(),
            partner_cred_points_str(),
            amount_str(),
        ]
        blrpern_cat = "believer_partnerunit"
        src_table = f"{idea_number}_raw"
        blrpern_table = f"{blrpern_cat}_raw"
        idea_config = get_idea_config_dict()
        blrpern_config = idea_config.get(blrpern_cat)
        blrpern_jkeys = blrpern_config.get("jkeys")
        blrpern_jvals = blrpern_config.get("jvalues")
        blrpern_args = set(blrpern_jkeys.keys()).union(set(blrpern_jvals.keys()))
        print(f"{blrpern_jkeys=}")
        print(f"{blrpern_jvals=}")
        create_idea_sorted_table(conn, src_table, idea_cols)
        create_idea_sorted_table(conn, blrpern_table, list(blrpern_args))

        # WHEN
        gen_sqlstr = get_idea_into_dimen_raw_query(
            conn, idea_number, blrpern_cat, blrpern_jkeys
        )

        # THEN
        columns_str = "event_int, face_name, belief_label, believer_name, partner_name, partner_cred_points"
        expected_sqlstr = f"""INSERT INTO {blrpern_cat}_raw (idea_number, {columns_str})
SELECT '{idea_number}' as idea_number, {columns_str}
FROM {idea_number}_raw
WHERE event_int IS NOT NULL AND face_name IS NOT NULL AND belief_label IS NOT NULL AND believer_name IS NOT NULL AND partner_name IS NOT NULL
GROUP BY {columns_str}
;
"""
        print("generated:")
        print(gen_sqlstr)
        print(expected_sqlstr)

        assert gen_sqlstr == expected_sqlstr
