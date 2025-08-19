from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import create_insert_query
from src.a10_believer_calc.believer_calc_config import get_believer_calc_dimen_args
from src.a18_etl_toolbox.db_obj_believer_tool import (
    create_believerunit_metrics_insert_sqlstr,
    create_blrawar_metrics_insert_sqlstr,
    create_blrfact_metrics_insert_sqlstr,
    create_blrgrou_metrics_insert_sqlstr,
    create_blrheal_metrics_insert_sqlstr,
    create_blrlabo_metrics_insert_sqlstr,
    create_blrmemb_metrics_insert_sqlstr,
    create_blrpern_metrics_insert_sqlstr,
    create_blrplan_metrics_insert_sqlstr,
    create_blrprem_metrics_insert_sqlstr,
    create_blrreas_metrics_insert_sqlstr,
)
from src.a18_etl_toolbox.tran_sqlstrs import create_job_tables


def test_create_believerunit_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_believer_calc_dimen_args("believerunit")
    # for x_arg in sorted(x_args):
    #     print(f"{x_arg=}")

    x_belief_label = "amy23"
    x_believer_name = "Sue"
    x__keeps_buildable = True
    x__keeps_justified = False
    x__offtrack_fund = 55.5
    x__rational = True
    x__sum_healerlink_share = 66.6
    x__tree_traverse_count = 7
    x_credor_respect = 88.2
    x_debtor_respect = 88.4
    x_fund_iota = 3
    x_fund_pool = 3000
    x_max_tree_traverse = 22
    x_penny = 4
    x_respect_bit = 0.2
    x_tally = 6
    values_dict = {
        "belief_label": x_belief_label,
        "believer_name": x_believer_name,
        "_keeps_buildable": x__keeps_buildable,
        "_keeps_justified": x__keeps_justified,
        "_offtrack_fund": x__offtrack_fund,
        "_rational": x__rational,
        "_sum_healerlink_share": x__sum_healerlink_share,
        "_tree_traverse_count": x__tree_traverse_count,
        "credor_respect": x_credor_respect,
        "debtor_respect": x_debtor_respect,
        "fund_iota": x_fund_iota,
        "fund_pool": x_fund_pool,
        "max_tree_traverse": x_max_tree_traverse,
        "penny": x_penny,
        "respect_bit": x_respect_bit,
        "tally": x_tally,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_believerunit_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        table_name = "believerunit_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print(expected_sqlstr)
        print("")
        print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_blrplan_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_believer_calc_dimen_args("believer_planunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     # print(f"    x_{x_arg} = {x_count}")
    #     # print(f"""    "{x_arg}": x_{x_arg},""")
    #     print(f""" {x_arg} = values_dict.get("{x_arg}")""")
    #     # b0_str = "{"
    #     # b1_str = "}"
    #     # print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")

    x_belief_label = "amy23"
    x_believer_name = "Sue"
    x__active = 1
    x__all_partner_cred = 2
    x__all_partner_debt = 3
    x__descendant_task_count = 4
    x__fund_cease = 5
    x_fund_iota = 6
    x__fund_onset = 7
    x__fund_ratio = 8
    x__gogo_calc = 9
    x__healerlink_ratio = 10
    x__level = 11
    x__range_evaluated = 12
    x__stop_calc = 13
    x__chore = 14
    x_addin = 15
    x_begin = 16
    x_close = 17
    x_denom = 18
    x_gogo_want = 19
    x_star = 21
    x_morph = 22
    x_numor = 23
    x_rope = 24
    x_task = 25
    x_problem_bool = 26
    x_stop_want = 27
    values_dict = {
        "belief_label": x_belief_label,
        "believer_name": x_believer_name,
        "_active": x__active,
        "_all_partner_cred": x__all_partner_cred,
        "_all_partner_debt": x__all_partner_debt,
        "_descendant_task_count": x__descendant_task_count,
        "_fund_cease": x__fund_cease,
        "fund_iota": x_fund_iota,
        "_fund_onset": x__fund_onset,
        "_fund_ratio": x__fund_ratio,
        "_gogo_calc": x__gogo_calc,
        "_healerlink_ratio": x__healerlink_ratio,
        "_level": x__level,
        "_range_evaluated": x__range_evaluated,
        "_stop_calc": x__stop_calc,
        "_chore": x__chore,
        "addin": x_addin,
        "begin": x_begin,
        "close": x_close,
        "denom": x_denom,
        "gogo_want": x_gogo_want,
        "star": x_star,
        "morph": x_morph,
        "numor": x_numor,
        "plan_rope": x_rope,
        "task": x_task,
        "problem_bool": x_problem_bool,
        "stop_want": x_stop_want,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_blrplan_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        table_name = "believer_planunit_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print(expected_sqlstr)
        print("")
        print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_blrreas_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_believer_calc_dimen_args("believer_plan_reasonunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    "{x_arg}": x_{x_arg},""")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    {x_arg} = values_dict.get("{x_arg}")""")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     b0_str = "{"
    #     b1_str = "}"
    #     print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")

    x_belief_label = "amy23"
    x_believer_name = "Sue"
    x_rope = 1
    x_reason_context = 2
    x_reason_active_requisite = 3
    x__chore = 4
    x__status = 5
    x__rplan_active_value = 6
    values_dict = {
        "belief_label": x_belief_label,
        "believer_name": x_believer_name,
        "plan_rope": x_rope,
        "reason_context": x_reason_context,
        "reason_active_requisite": x_reason_active_requisite,
        "_chore": x__chore,
        "_status": x__status,
        "_rplan_active_value": x__rplan_active_value,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_blrreas_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        table_name = "believer_plan_reasonunit_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print(expected_sqlstr)
        print("")
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_blrprem_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_believer_calc_dimen_args("believer_plan_reason_caseunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    "{x_arg}": x_{x_arg},""")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    {x_arg} = values_dict.get("{x_arg}")""")
    # print("")
    # print("VALUES (")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     b0_str = "{"
    #     b1_str = "}"
    #     print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")
    # print(")")
    # print(";")

    x_belief_label = "amy23"
    x_believer_name = "Sue"
    x_rope = 1
    x_reason_context = 2
    x_reason_state = 3
    x_reason_upper = 4
    x_reason_lower = 5
    x_reason_divisor = 6
    x__chore = 7
    x__status = 8
    values_dict = {
        "belief_label": x_belief_label,
        "believer_name": x_believer_name,
        "plan_rope": x_rope,
        "reason_context": x_reason_context,
        "reason_state": x_reason_state,
        "reason_upper": x_reason_upper,
        "reason_lower": x_reason_lower,
        "reason_divisor": x_reason_divisor,
        "_chore": x__chore,
        "_status": x__status,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_blrprem_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        table_name = "believer_plan_reason_caseunit_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        # print(expected_sqlstr)
        print("")
        print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_blrawar_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_believer_calc_dimen_args("believer_plan_awardunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    "{x_arg}": x_{x_arg},""")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    {x_arg} = values_dict.get("{x_arg}")""")
    # print("")
    # print("VALUES (")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     b0_str = "{"
    #     b1_str = "}"
    #     print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")
    # print(")")
    # print(";")

    x_belief_label = "amy23"
    x_believer_name = "Sue"
    x_rope = 1
    x_awardee_title = 2
    x_give_force = 3
    x_take_force = 4
    x__fund_give = 5
    x__fund_take = 6
    values_dict = {
        "belief_label": x_belief_label,
        "believer_name": x_believer_name,
        "plan_rope": x_rope,
        "awardee_title": x_awardee_title,
        "give_force": x_give_force,
        "take_force": x_take_force,
        "_fund_give": x__fund_give,
        "_fund_take": x__fund_take,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_blrawar_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        table_name = "believer_plan_awardunit_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_blrfact_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_believer_calc_dimen_args("believer_plan_factunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    "{x_arg}": x_{x_arg},""")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    {x_arg} = values_dict.get("{x_arg}")""")
    # print("")
    # print("VALUES (")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     b0_str = "{"
    #     b1_str = "}"
    #     print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")
    # print(")")
    # print(";")

    x_belief_label = "amy23"
    x_believer_name = "Sue"
    x_rope = 1
    x_fact_context = 2
    x_fact_state = 3
    x_fact_lower = 4
    x_fact_upper = 5
    values_dict = {
        "belief_label": x_belief_label,
        "believer_name": x_believer_name,
        "plan_rope": x_rope,
        "fact_context": x_fact_context,
        "fact_state": x_fact_state,
        "fact_lower": x_fact_lower,
        "fact_upper": x_fact_upper,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_blrfact_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        table_name = "believer_plan_factunit_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_blrheal_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_believer_calc_dimen_args("believer_plan_healerlink")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    "{x_arg}": x_{x_arg},""")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    {x_arg} = values_dict.get("{x_arg}")""")
    # print("")
    # print("VALUES (")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     b0_str = "{"
    #     b1_str = "}"
    #     print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")
    # print(")")
    # print(";")

    x_belief_label = "amy23"
    x_believer_name = "Sue"
    x_rope = 1
    x_healer_name = 2
    values_dict = {
        "belief_label": x_belief_label,
        "believer_name": x_believer_name,
        "plan_rope": x_rope,
        "healer_name": x_healer_name,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_blrheal_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        table_name = "believer_plan_healerlink_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_blrlabo_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_believer_calc_dimen_args("believer_plan_partyunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    "{x_arg}": x_{x_arg},""")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    {x_arg} = values_dict.get("{x_arg}")""")
    # print("")
    # print("VALUES (")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     b0_str = "{"
    #     b1_str = "}"
    #     print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")
    # print(")")
    # print(";")

    x_belief_label = "amy23"
    x_believer_name = "Sue"
    x_rope = 1
    x_party_title = 2
    x_solo = 4
    x__believer_name_is_labor = 3
    values_dict = {
        "belief_label": x_belief_label,
        "believer_name": x_believer_name,
        "plan_rope": x_rope,
        "party_title": x_party_title,
        "solo": x_solo,
        "_believer_name_is_labor": x__believer_name_is_labor,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_blrlabo_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        table_name = "believer_plan_partyunit_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        print("")
        print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_blrpern_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_believer_calc_dimen_args("believer_partnerunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    "{x_arg}": x_{x_arg},""")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    {x_arg} = values_dict.get("{x_arg}")""")
    # print("")
    # print("VALUES (")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     b0_str = "{"
    #     b1_str = "}"
    #     print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")
    # print(")")
    # print(";")

    x_belief_label = "amy23"
    x_believer_name = "Sue"
    x_partner_name = 1
    x_partner_cred_points = 2
    x_partner_debt_points = 3
    x__credor_pool = 4
    x__debtor_pool = 5
    x__fund_give = 6
    x__fund_take = 7
    x__fund_agenda_give = 8
    x__fund_agenda_take = 9
    x__fund_agenda_ratio_give = 10
    x__fund_agenda_ratio_take = 11
    x__inallocable_partner_debt_points = 12
    x__irrational_partner_debt_points = 13
    values_dict = {
        "belief_label": x_belief_label,
        "believer_name": x_believer_name,
        "partner_name": x_partner_name,
        "partner_cred_points": x_partner_cred_points,
        "partner_debt_points": x_partner_debt_points,
        "_credor_pool": x__credor_pool,
        "_debtor_pool": x__debtor_pool,
        "_fund_give": x__fund_give,
        "_fund_take": x__fund_take,
        "_fund_agenda_give": x__fund_agenda_give,
        "_fund_agenda_take": x__fund_agenda_take,
        "_fund_agenda_ratio_give": x__fund_agenda_ratio_give,
        "_fund_agenda_ratio_take": x__fund_agenda_ratio_take,
        "_inallocable_partner_debt_points": x__inallocable_partner_debt_points,
        "_irrational_partner_debt_points": x__irrational_partner_debt_points,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_blrpern_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        table_name = "believer_partnerunit_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_blrmemb_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_believer_calc_dimen_args("believer_partner_membership")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    "{x_arg}": x_{x_arg},""")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    {x_arg} = values_dict.get("{x_arg}")""")
    # print("")
    # print("VALUES (")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     b0_str = "{"
    #     b1_str = "}"
    #     print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")
    # print(")")
    # print(";")

    x_belief_label = "amy23"
    x_believer_name = "Sue"
    x_partner_name = 1
    x_group_title = 2
    x_group_cred_points = 3
    x_group_debt_points = 4
    x__credor_pool = 5
    x__debtor_pool = 6
    x__fund_give = 7
    x__fund_take = 8
    x__fund_agenda_give = 9
    x__fund_agenda_take = 10
    x__fund_agenda_ratio_give = 11
    x__fund_agenda_ratio_take = 12
    values_dict = {
        "belief_label": x_belief_label,
        "believer_name": x_believer_name,
        "partner_name": x_partner_name,
        "group_title": x_group_title,
        "group_cred_points": x_group_cred_points,
        "group_debt_points": x_group_debt_points,
        "_credor_pool": x__credor_pool,
        "_debtor_pool": x__debtor_pool,
        "_fund_give": x__fund_give,
        "_fund_take": x__fund_take,
        "_fund_agenda_give": x__fund_agenda_give,
        "_fund_agenda_take": x__fund_agenda_take,
        "_fund_agenda_ratio_give": x__fund_agenda_ratio_give,
        "_fund_agenda_ratio_take": x__fund_agenda_ratio_take,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_blrmemb_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        table_name = "believer_partner_membership_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_blrgrou_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_believer_calc_dimen_args("believer_groupunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    "{x_arg}": x_{x_arg},""")
    # print("")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    {x_arg} = values_dict.get("{x_arg}")""")
    # print("")
    # print("VALUES (")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     b0_str = "{"
    #     b1_str = "}"
    #     print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")
    # print(")")
    # print(";")

    x_belief_label = "amy23"
    x_believer_name = "Sue"
    x_group_title = 1
    x__credor_pool = 2
    x__debtor_pool = 3
    x_fund_iota = 4
    x__fund_give = 5
    x__fund_take = 6
    x__fund_agenda_give = 7
    x__fund_agenda_take = 8
    x_knot = 9
    values_dict = {
        "belief_label": x_belief_label,
        "believer_name": x_believer_name,
        "group_title": x_group_title,
        "_credor_pool": x__credor_pool,
        "_debtor_pool": x__debtor_pool,
        "fund_iota": x_fund_iota,
        "_fund_give": x__fund_give,
        "_fund_take": x__fund_take,
        "_fund_agenda_give": x__fund_agenda_give,
        "_fund_agenda_take": x__fund_agenda_take,
        "knot": x_knot,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_blrgrou_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        table_name = "believer_groupunit_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr
