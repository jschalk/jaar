from sqlite3 import connect as sqlite3_connect
from src.ch01_data_toolbox.db_toolbox import create_insert_query
from src.ch07_belief_logic.belief_config import get_belief_calc_dimen_args
from src.ch18_etl_toolbox._ref.ch18_keywords import Ch18Keywords as wx
from src.ch18_etl_toolbox.db_obj_belief_tool import (
    create_beliefunit_metrics_insert_sqlstr,
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
from src.ch18_etl_toolbox.tran_sqlstrs import create_job_tables


def test_create_beliefunit_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_belief_calc_dimen_args("beliefunit")
    # for x_arg in sorted(x_args):
    #     print(f"{x_arg=}")

    x_moment_label = "amy23"
    x_belief_name = "Sue"
    x_keeps_buildable = True
    x_keeps_justified = False
    x_offtrack_fund = 55.5
    x_rational = True
    x_sum_healerunit_share = 66.6
    x_tree_traverse_count = 7
    x_credor_respect = 88.2
    x_debtor_respect = 88.4
    x_fund_grain = 3
    x_fund_pool = 3000
    x_max_tree_traverse = 22
    x_penny = 4
    x_respect_grain = 0.2
    x_tally = 6
    values_dict = {
        "moment_label": x_moment_label,
        "belief_name": x_belief_name,
        "keeps_buildable": x_keeps_buildable,
        "keeps_justified": x_keeps_justified,
        "offtrack_fund": x_offtrack_fund,
        "rational": x_rational,
        "sum_healerunit_share": x_sum_healerunit_share,
        "tree_traverse_count": x_tree_traverse_count,
        "credor_respect": x_credor_respect,
        "debtor_respect": x_debtor_respect,
        "fund_grain": x_fund_grain,
        "fund_pool": x_fund_pool,
        "max_tree_traverse": x_max_tree_traverse,
        "penny": x_penny,
        "respect_grain": x_respect_grain,
        "tally": x_tally,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_beliefunit_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        table_name = "beliefunit_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print(expected_sqlstr)
        print("")
        print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_blrplan_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_belief_calc_dimen_args("belief_planunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     # print(f"    x_{x_arg} = {x_count}")
    #     # print(f"""    "{x_arg}": x_{x_arg},""")
    #     print(f""" {x_arg} = values_dict.get("{x_arg}")""")
    #     # b0_str = "{"
    #     # b1_str = "}"
    #     # print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")

    x_moment_label = "amy23"
    x_belief_name = "Sue"
    x_active = 1
    x_all_voice_cred = 2
    x_all_voice_debt = 3
    x_descendant_pledge_count = 4
    x_fund_cease = 5
    x_fund_grain = 6
    x_fund_onset = 7
    x_fund_ratio = 8
    x_gogo_calc = 9
    x_healerunit_ratio = 10
    x_tree_level = 11
    x_range_evaluated = 12
    x_stop_calc = 13
    x_task = 14
    x_addin = 15
    x_begin = 16
    x_close = 17
    x_denom = 18
    x_gogo_want = 19
    x_star = 21
    x_morph = 22
    x_numor = 23
    x_rope = 24
    x_pledge = 25
    x_problem_bool = 26
    x_stop_want = 27
    values_dict = {
        "moment_label": x_moment_label,
        "belief_name": x_belief_name,
        "active": x_active,
        "all_voice_cred": x_all_voice_cred,
        "all_voice_debt": x_all_voice_debt,
        "descendant_pledge_count": x_descendant_pledge_count,
        "fund_cease": x_fund_cease,
        "fund_grain": x_fund_grain,
        "fund_onset": x_fund_onset,
        "fund_ratio": x_fund_ratio,
        "gogo_calc": x_gogo_calc,
        "healerunit_ratio": x_healerunit_ratio,
        "tree_level": x_tree_level,
        "range_evaluated": x_range_evaluated,
        "stop_calc": x_stop_calc,
        "task": x_task,
        "addin": x_addin,
        "begin": x_begin,
        "close": x_close,
        "denom": x_denom,
        "gogo_want": x_gogo_want,
        "star": x_star,
        "morph": x_morph,
        "numor": x_numor,
        "plan_rope": x_rope,
        "pledge": x_pledge,
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
        table_name = "belief_planunit_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print(expected_sqlstr)
        print("")
        print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_blrreas_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_belief_calc_dimen_args("belief_plan_reasonunit")
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

    x_moment_label = "amy23"
    x_belief_name = "Sue"
    x_rope = 1
    x_reason_context = 2
    x_reason_active_requisite = 3
    x_task = 4
    x_status = 5
    x__reason_active_heir = 6
    values_dict = {
        "moment_label": x_moment_label,
        "belief_name": x_belief_name,
        "plan_rope": x_rope,
        wx.reason_context: x_reason_context,
        wx.reason_active_requisite: x_reason_active_requisite,
        "task": x_task,
        "status": x_status,
        "_reason_active_heir": x__reason_active_heir,
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
        table_name = "belief_plan_reasonunit_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print(expected_sqlstr)
        print("")
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_blrprem_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_belief_calc_dimen_args("belief_plan_reason_caseunit")
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

    x_moment_label = "amy23"
    x_belief_name = "Sue"
    x_rope = 1
    x_reason_context = 2
    x_reason_state = 3
    x_reason_upper = 4
    x_reason_lower = 5
    x_reason_divisor = 6
    x_task = 7
    x_status = 8
    values_dict = {
        wx.moment_label: x_moment_label,
        wx.belief_name: x_belief_name,
        wx.plan_rope: x_rope,
        wx.reason_context: x_reason_context,
        wx.reason_state: x_reason_state,
        wx.reason_upper: x_reason_upper,
        wx.reason_lower: x_reason_lower,
        wx.reason_divisor: x_reason_divisor,
        wx.task: x_task,
        wx.status: x_status,
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
        table_name = "belief_plan_reason_caseunit_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        # print(expected_sqlstr)
        print("")
        print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_blrawar_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_belief_calc_dimen_args("belief_plan_awardunit")
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

    x_moment_label = "amy23"
    x_belief_name = "Sue"
    x_rope = 1
    x_awardee_title = 2
    x_give_force = 3
    x_take_force = 4
    x_fund_give = 5
    x_fund_take = 6
    values_dict = {
        "moment_label": x_moment_label,
        "belief_name": x_belief_name,
        "plan_rope": x_rope,
        "awardee_title": x_awardee_title,
        "give_force": x_give_force,
        "take_force": x_take_force,
        "fund_give": x_fund_give,
        "fund_take": x_fund_take,
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
        table_name = "belief_plan_awardunit_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_blrfact_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_belief_calc_dimen_args("belief_plan_factunit")
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

    x_moment_label = "amy23"
    x_belief_name = "Sue"
    x_rope = 1
    x_fact_context = 2
    x_fact_state = 3
    x_fact_lower = 4
    x_fact_upper = 5
    values_dict = {
        "moment_label": x_moment_label,
        "belief_name": x_belief_name,
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
        table_name = "belief_plan_factunit_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_blrheal_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_belief_calc_dimen_args("belief_plan_healerunit")
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

    x_moment_label = "amy23"
    x_belief_name = "Sue"
    x_rope = 1
    x_healer_name = 2
    values_dict = {
        "moment_label": x_moment_label,
        "belief_name": x_belief_name,
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
        table_name = "belief_plan_healerunit_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_blrlabo_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_belief_calc_dimen_args("belief_plan_partyunit")
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

    x_moment_label = "amy23"
    x_belief_name = "Sue"
    x_rope = 1
    x_party_title = 2
    x_solo = 4
    x__belief_name_is_labor = 3
    values_dict = {
        "moment_label": x_moment_label,
        "belief_name": x_belief_name,
        "plan_rope": x_rope,
        "party_title": x_party_title,
        "solo": x_solo,
        "_belief_name_is_labor": x__belief_name_is_labor,
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
        table_name = "belief_plan_partyunit_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        print("")
        print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_blrpern_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_belief_calc_dimen_args("belief_voiceunit")
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

    x_moment_label = "amy23"
    x_belief_name = "Sue"
    x_voice_name = 1
    x_voice_cred_points = 2
    x_voice_debt_points = 3
    x_credor_pool = 4
    x_debtor_pool = 5
    x_fund_give = 6
    x_fund_take = 7
    x_fund_agenda_give = 8
    x_fund_agenda_take = 9
    x_fund_agenda_ratio_give = 10
    x_fund_agenda_ratio_take = 11
    x_inallocable_voice_debt_points = 12
    x_irrational_voice_debt_points = 13
    values_dict = {
        "moment_label": x_moment_label,
        "belief_name": x_belief_name,
        "voice_name": x_voice_name,
        "voice_cred_points": x_voice_cred_points,
        "voice_debt_points": x_voice_debt_points,
        "credor_pool": x_credor_pool,
        "debtor_pool": x_debtor_pool,
        "fund_give": x_fund_give,
        "fund_take": x_fund_take,
        "fund_agenda_give": x_fund_agenda_give,
        "fund_agenda_take": x_fund_agenda_take,
        "fund_agenda_ratio_give": x_fund_agenda_ratio_give,
        "fund_agenda_ratio_take": x_fund_agenda_ratio_take,
        "inallocable_voice_debt_points": x_inallocable_voice_debt_points,
        "irrational_voice_debt_points": x_irrational_voice_debt_points,
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
        table_name = "belief_voiceunit_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_blrmemb_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_belief_calc_dimen_args("belief_voice_membership")
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

    x_moment_label = "amy23"
    x_belief_name = "Sue"
    x_voice_name = 1
    x_group_title = 2
    x_group_cred_points = 3
    x_group_debt_points = 4
    x_credor_pool = 5
    x_debtor_pool = 6
    x_fund_give = 7
    x_fund_take = 8
    x_fund_agenda_give = 9
    x_fund_agenda_take = 10
    x_fund_agenda_ratio_give = 11
    x_fund_agenda_ratio_take = 12
    values_dict = {
        "moment_label": x_moment_label,
        "belief_name": x_belief_name,
        "voice_name": x_voice_name,
        "group_title": x_group_title,
        "group_cred_points": x_group_cred_points,
        "group_debt_points": x_group_debt_points,
        "credor_pool": x_credor_pool,
        "debtor_pool": x_debtor_pool,
        "fund_give": x_fund_give,
        "fund_take": x_fund_take,
        "fund_agenda_give": x_fund_agenda_give,
        "fund_agenda_take": x_fund_agenda_take,
        "fund_agenda_ratio_give": x_fund_agenda_ratio_give,
        "fund_agenda_ratio_take": x_fund_agenda_ratio_take,
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
        table_name = "belief_voice_membership_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_blrgrou_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_belief_calc_dimen_args("belief_groupunit")
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

    x_moment_label = "amy23"
    x_belief_name = "Sue"
    x_group_title = 1
    x_credor_pool = 2
    x_debtor_pool = 3
    x_fund_grain = 4
    x_fund_give = 5
    x_fund_take = 6
    x_fund_agenda_give = 7
    x_fund_agenda_take = 8
    x_knot = 9
    values_dict = {
        "moment_label": x_moment_label,
        "belief_name": x_belief_name,
        "group_title": x_group_title,
        "credor_pool": x_credor_pool,
        "debtor_pool": x_debtor_pool,
        "fund_grain": x_fund_grain,
        "fund_give": x_fund_give,
        "fund_take": x_fund_take,
        "fund_agenda_give": x_fund_agenda_give,
        "fund_agenda_take": x_fund_agenda_take,
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
        table_name = "belief_groupunit_job"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr
