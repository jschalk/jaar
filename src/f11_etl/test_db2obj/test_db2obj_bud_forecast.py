from src.f00_instrument.db_toolbox import (
    get_row_count,
    create_insert_query,
    create_select_query,
)
from src.f01_road.deal import fisc_title_str
from src.f02_bud.item import itemunit_shop
from src.f02_bud.bud import budunit_shop
from src.f05_fund_metric.fund_metric_config import (
    get_fund_metric_config_dict,
    get_fund_metric_dimen_args,
)
from src.f08_fisc.fisc import fiscunit_shop, get_from_dict as fiscunit_get_from_dict
from src.f08_fisc.fisc_config import cashbook_str, brokerunits_str, timeline_str
from src.f10_idea.idea_config import get_default_sorted_list
from src.f11_etl.tran_sqlstrs import create_forecast_tables
from src.f11_etl.db_obj_tool import (
    get_fisc_dict_from_db,
    insert_forecast_obj,
    create_budmemb_metrics_insert_sqlstr,
    create_budacct_metrics_insert_sqlstr,
    create_budgrou_metrics_insert_sqlstr,
    create_budawar_metrics_insert_sqlstr,
    create_budfact_metrics_insert_sqlstr,
    create_budheal_metrics_insert_sqlstr,
    create_budprem_metrics_insert_sqlstr,
    create_budreas_metrics_insert_sqlstr,
    create_budteam_metrics_insert_sqlstr,
    create_buditem_metrics_insert_sqlstr,
    create_budunit_metrics_insert_sqlstr,
)
from sqlite3 import connect as sqlite3_connect


def test_create_budunit_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_fund_metric_dimen_args("budunit")
    # for x_arg in sorted(x_args):
    #     print(f"{x_arg=}")
    x_fisc_title = "accord23"
    x_owner_name = "Sue"
    x__keeps_buildable = True
    x__keeps_justified = False
    x__offtrack_fund = 55.5
    x__rational = True
    x__sum_healerlink_share = 66.6
    x__tree_traverse_count = 7
    x_credor_respect = 88.2
    x_debtor_respect = 88.4
    x_fund_coin = 3
    x_fund_pool = 3000
    x_max_tree_traverse = 22
    x_penny = 4
    x_respect_bit = 0.2
    x_tally = 6
    values_dict = {
        "fisc_title": x_fisc_title,
        "owner_name": x_owner_name,
        "_keeps_buildable": x__keeps_buildable,
        "_keeps_justified": x__keeps_justified,
        "_offtrack_fund": x__offtrack_fund,
        "_rational": x__rational,
        "_sum_healerlink_share": x__sum_healerlink_share,
        "_tree_traverse_count": x__tree_traverse_count,
        "credor_respect": x_credor_respect,
        "debtor_respect": x_debtor_respect,
        "fund_coin": x_fund_coin,
        "fund_pool": x_fund_pool,
        "max_tree_traverse": x_max_tree_traverse,
        "penny": x_penny,
        "respect_bit": x_respect_bit,
        "tally": x_tally,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_budunit_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_forecast_tables(cursor)
        table_name = "budunit_forecast"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print(expected_sqlstr)
        print("")
        print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_buditem_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_fund_metric_dimen_args("bud_itemunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     # print(f"    x_{x_arg} = {x_count}")
    #     # print(f"""    "{x_arg}": x_{x_arg},""")
    #     print(f""" {x_arg} = values_dict.get("{x_arg}")""")
    #     # b0_str = "{"
    #     # b1_str = "}"
    #     # print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")
    x_fisc_title = "accord23"
    x_owner_name = "Sue"
    x__active = 1
    x__all_acct_cred = 2
    x__all_acct_debt = 3
    x__descendant_pledge_count = 4
    x__fund_cease = 5
    x__fund_coin = 6
    x__fund_onset = 7
    x__fund_ratio = 8
    x__gogo_calc = 9
    x__healerlink_ratio = 10
    x__level = 11
    x__range_evaluated = 12
    x__stop_calc = 13
    x__task = 14
    x_addin = 15
    x_begin = 16
    x_close = 17
    x_denom = 18
    x_gogo_want = 19
    x_item_title = 20
    x_mass = 21
    x_morph = 22
    x_numor = 23
    x_parent_road = 24
    x_pledge = 25
    x_problem_bool = 26
    x_stop_want = 27
    values_dict = {
        "fisc_title": x_fisc_title,
        "owner_name": x_owner_name,
        "_active": x__active,
        "_all_acct_cred": x__all_acct_cred,
        "_all_acct_debt": x__all_acct_debt,
        "_descendant_pledge_count": x__descendant_pledge_count,
        "_fund_cease": x__fund_cease,
        "_fund_coin": x__fund_coin,
        "_fund_onset": x__fund_onset,
        "_fund_ratio": x__fund_ratio,
        "_gogo_calc": x__gogo_calc,
        "_healerlink_ratio": x__healerlink_ratio,
        "_level": x__level,
        "_range_evaluated": x__range_evaluated,
        "_stop_calc": x__stop_calc,
        "_task": x__task,
        "addin": x_addin,
        "begin": x_begin,
        "close": x_close,
        "denom": x_denom,
        "gogo_want": x_gogo_want,
        "item_title": x_item_title,
        "mass": x_mass,
        "morph": x_morph,
        "numor": x_numor,
        "parent_road": x_parent_road,
        "pledge": x_pledge,
        "problem_bool": x_problem_bool,
        "stop_want": x_stop_want,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_buditem_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_forecast_tables(cursor)
        table_name = "bud_itemunit_forecast"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        # print(expected_sqlstr)
        print("")
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_budreas_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_fund_metric_dimen_args("bud_item_reasonunit")
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
    x_fisc_title = "accord23"
    x_owner_name = "Sue"
    x_road = 1
    x_base = 2
    x_base_item_active_requisite = 3
    x__task = 4
    x__status = 5
    x__base_item_active_value = 6
    values_dict = {
        "fisc_title": x_fisc_title,
        "owner_name": x_owner_name,
        "road": x_road,
        "base": x_base,
        "base_item_active_requisite": x_base_item_active_requisite,
        "_task": x__task,
        "_status": x__status,
        "_base_item_active_value": x__base_item_active_value,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_budreas_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_forecast_tables(cursor)
        table_name = "bud_item_reasonunit_forecast"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print(expected_sqlstr)
        print("")
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_budprem_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_fund_metric_dimen_args("bud_item_reason_premiseunit")
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
    x_fisc_title = "accord23"
    x_owner_name = "Sue"
    x_road = 1
    x_base = 2
    x_need = 3
    x_nigh = 4
    x_open = 5
    x_divisor = 6
    x__task = 7
    x__status = 8
    values_dict = {
        "fisc_title": x_fisc_title,
        "owner_name": x_owner_name,
        "road": x_road,
        "base": x_base,
        "need": x_need,
        "nigh": x_nigh,
        "open": x_open,
        "divisor": x_divisor,
        "_task": x__task,
        "_status": x__status,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_budprem_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_forecast_tables(cursor)
        table_name = "bud_item_reason_premiseunit_forecast"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        # print(expected_sqlstr)
        print("")
        print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_budawar_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_fund_metric_dimen_args("bud_item_awardlink")
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
    x_fisc_title = "accord23"
    x_owner_name = "Sue"
    x_road = 1
    x_awardee_tag = 2
    x_give_force = 3
    x_take_force = 4
    x__fund_give = 5
    x__fund_take = 6
    values_dict = {
        "fisc_title": x_fisc_title,
        "owner_name": x_owner_name,
        "road": x_road,
        "awardee_tag": x_awardee_tag,
        "give_force": x_give_force,
        "take_force": x_take_force,
        "_fund_give": x__fund_give,
        "_fund_take": x__fund_take,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_budawar_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_forecast_tables(cursor)
        table_name = "bud_item_awardlink_forecast"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_budfact_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_fund_metric_dimen_args("bud_item_factunit")
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
    x_fisc_title = "accord23"
    x_owner_name = "Sue"
    x_road = 1
    x_base = 2
    x_pick = 3
    x_fopen = 4
    x_fnigh = 5
    values_dict = {
        "fisc_title": x_fisc_title,
        "owner_name": x_owner_name,
        "road": x_road,
        "base": x_base,
        "pick": x_pick,
        "fopen": x_fopen,
        "fnigh": x_fnigh,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_budfact_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_forecast_tables(cursor)
        table_name = "bud_item_factunit_forecast"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_budheal_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_fund_metric_dimen_args("bud_item_healerlink")
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
    x_fisc_title = "accord23"
    x_owner_name = "Sue"
    x_road = 1
    x_healer_name = 2
    values_dict = {
        "fisc_title": x_fisc_title,
        "owner_name": x_owner_name,
        "road": x_road,
        "healer_name": x_healer_name,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_budheal_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_forecast_tables(cursor)
        table_name = "bud_item_healerlink_forecast"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_budteam_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_fund_metric_dimen_args("bud_item_teamlink")
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
    x_fisc_title = "accord23"
    x_owner_name = "Sue"
    x_road = 1
    x_team_tag = 2
    x__owner_name_team = 3
    values_dict = {
        "fisc_title": x_fisc_title,
        "owner_name": x_owner_name,
        "road": x_road,
        "team_tag": x_team_tag,
        "_owner_name_team": x__owner_name_team,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_budteam_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_forecast_tables(cursor)
        table_name = "bud_item_teamlink_forecast"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_budacct_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_fund_metric_dimen_args("bud_acctunit")
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
    x_fisc_title = "accord23"
    x_owner_name = "Sue"
    x_acct_name = 1
    x_credit_belief = 2
    x_debtit_belief = 3
    x__credor_pool = 4
    x__debtor_pool = 5
    x__fund_give = 6
    x__fund_take = 7
    x__fund_agenda_give = 8
    x__fund_agenda_take = 9
    x__fund_agenda_ratio_give = 10
    x__fund_agenda_ratio_take = 11
    x__inallocable_debtit_belief = 12
    x__irrational_debtit_belief = 13
    values_dict = {
        "fisc_title": x_fisc_title,
        "owner_name": x_owner_name,
        "acct_name": x_acct_name,
        "credit_belief": x_credit_belief,
        "debtit_belief": x_debtit_belief,
        "_credor_pool": x__credor_pool,
        "_debtor_pool": x__debtor_pool,
        "_fund_give": x__fund_give,
        "_fund_take": x__fund_take,
        "_fund_agenda_give": x__fund_agenda_give,
        "_fund_agenda_take": x__fund_agenda_take,
        "_fund_agenda_ratio_give": x__fund_agenda_ratio_give,
        "_fund_agenda_ratio_take": x__fund_agenda_ratio_take,
        "_inallocable_debtit_belief": x__inallocable_debtit_belief,
        "_irrational_debtit_belief": x__irrational_debtit_belief,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_budacct_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_forecast_tables(cursor)
        table_name = "bud_acctunit_forecast"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_budmemb_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_fund_metric_dimen_args("bud_acct_membership")
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
    x_fisc_title = "accord23"
    x_owner_name = "Sue"
    x_acct_name = 1
    x_group_label = 2
    x_credit_vote = 3
    x_debtit_vote = 4
    x__credor_pool = 5
    x__debtor_pool = 6
    x__fund_give = 7
    x__fund_take = 8
    x__fund_agenda_give = 9
    x__fund_agenda_take = 10
    x__fund_agenda_ratio_give = 11
    x__fund_agenda_ratio_take = 12
    values_dict = {
        "fisc_title": x_fisc_title,
        "owner_name": x_owner_name,
        "acct_name": x_acct_name,
        "group_label": x_group_label,
        "credit_vote": x_credit_vote,
        "debtit_vote": x_debtit_vote,
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
    insert_sqlstr = create_budmemb_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_forecast_tables(cursor)
        table_name = "bud_acct_membership_forecast"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


def test_create_budgrou_metrics_insert_sqlstr_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_args = get_fund_metric_dimen_args("bud_groupunit")
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
    x_fisc_title = "accord23"
    x_owner_name = "Sue"
    x_group_label = 1
    x__credor_pool = 2
    x__debtor_pool = 3
    x__fund_coin = 4
    x__fund_give = 5
    x__fund_take = 6
    x__fund_agenda_give = 7
    x__fund_agenda_take = 8
    x_bridge = 9
    values_dict = {
        "fisc_title": x_fisc_title,
        "owner_name": x_owner_name,
        "group_label": x_group_label,
        "_credor_pool": x__credor_pool,
        "_debtor_pool": x__debtor_pool,
        "_fund_coin": x__fund_coin,
        "_fund_give": x__fund_give,
        "_fund_take": x__fund_take,
        "_fund_agenda_give": x__fund_agenda_give,
        "_fund_agenda_take": x__fund_agenda_take,
        "bridge": x_bridge,
    }
    # all args included in values dict
    assert x_args == set(values_dict.keys())

    # WHEN
    insert_sqlstr = create_budgrou_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_forecast_tables(cursor)
        table_name = "bud_groupunit_forecast"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print("")
        print(expected_sqlstr)
        # print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


# # create tests to convert settled budunit to database
# # create budunit object
# # check that row does not exist in database
# # insert obj
# # check that row does exist in database
# # select row
# # prove selected row = obj __dict__


def test_insert_forecast_obj_CreatesTableRowsFor_budunit_forecast():
    # sourcery skip: extract-method
    # ESTABLISH
    x_fisc_title = "accord23"
    x_owner_name = "Sue"
    x__keeps_buildable = 99
    x__keeps_justified = 77
    x__offtrack_fund = 55.5
    x__rational = 92
    x__sum_healerlink_share = 66.6
    x__tree_traverse_count = 7
    x_credor_respect = 88.2
    x_debtor_respect = 88.4
    x_fund_coin = 3.0
    x_fund_pool = 3000.0
    x_max_tree_traverse = 22
    x_penny = 4.0
    x_respect_bit = 0.2
    x_tally = 6
    sue_bud = budunit_shop(owner_name=x_owner_name, fisc_title=x_fisc_title)
    sue_bud.fund_pool = x_fund_pool
    sue_bud.fund_coin = x_fund_coin
    sue_bud.penny = x_penny
    sue_bud.tally = x_tally
    sue_bud.respect_bit = x_respect_bit
    sue_bud.max_tree_traverse = x_max_tree_traverse
    sue_bud._keeps_buildable = x__keeps_buildable
    sue_bud._keeps_justified = x__keeps_justified
    sue_bud._offtrack_fund = x__offtrack_fund
    sue_bud._rational = x__rational
    sue_bud._sum_healerlink_share = x__sum_healerlink_share
    sue_bud._tree_traverse_count = x__tree_traverse_count
    sue_bud.credor_respect = x_credor_respect
    sue_bud.debtor_respect = x_debtor_respect

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_forecast_tables(cursor)
        x_table_name = "budunit_forecast"
        assert get_row_count(cursor, x_table_name) == 0

        # WHEN
        insert_forecast_obj(cursor, sue_bud)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            x_fisc_title,
            x_owner_name,
            x_credor_respect,
            x_debtor_respect,
            x_fund_pool,
            x_max_tree_traverse,
            x_tally,
            x_fund_coin,
            x_penny,
            x_respect_bit,
            x__rational,
            x__keeps_justified,
            x__offtrack_fund,
            x__sum_healerlink_share,
            x__keeps_buildable,
            x__tree_traverse_count,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


# def test_insert_forecast_obj_CreatesTableRowsFor_buditem_forecast():
#     # sourcery skip: extract-method
#     # ESTABLISH
#     x_args = get_fund_metric_dimen_args("bud_itemunit")
#     x_count = 0
#     for x_arg in get_default_sorted_list(x_args):
#         x_count += 1
#         print(f"    x_{x_arg} = {x_count}")
#     print("")
#     x_count = 0
#     for x_arg in get_default_sorted_list(x_args):
#         print(f"""    x_item.{x_arg} = x_{x_arg}""")
#     print("")
#     x_count = 0
#     # for x_arg in get_default_sorted_list(x_args):
#     #     print(f"""    {x_arg} = values_dict.get("{x_arg}")""")
#     # print("")
#     # print("VALUES (")
#     # x_count = 0
#     # for x_arg in get_default_sorted_list(x_args):
#     #     b0_str = "{"
#     #     b1_str = "}"
#     #     print(f""", {b0_str}sqlite_obj_str({x_arg}, real_str){b1_str}""")
#     # print(")")
#     # print(";")

#     x_fisc_title = 1
#     x_owner_name = 2
#     x_parent_road = 3
#     x_item_title = 4
#     x_begin = 5
#     x_close = 6
#     x_addin = 7
#     x_numor = 8
#     x_denom = 9
#     x_morph = 10
#     x_gogo_want = 11
#     x_stop_want = 12
#     x_mass = 13
#     x_pledge = 14
#     x_problem_bool = 15
#     x__active = 16
#     x__task = 17
#     x__fund_coin = 18
#     x__fund_onset = 19
#     x__fund_cease = 20
#     x__fund_ratio = 21
#     x__gogo_calc = 22
#     x__stop_calc = 23
#     x__level = 24
#     x__range_evaluated = 25
#     x__descendant_pledge_count = 26
#     x__healerlink_ratio = 27
#     x__all_acct_cred = 28
#     x__all_acct_debt = 29
#     x_item = itemunit_shop()
#     x_item.parent_road = x_parent_road
#     x_item.item_title = x_item_title
#     x_item.begin = x_begin
#     x_item.close = x_close
#     x_item.addin = x_addin
#     x_item.numor = x_numor
#     x_item.denom = x_denom
#     x_item.morph = x_morph
#     x_item.gogo_want = x_gogo_want
#     x_item.stop_want = x_stop_want
#     x_item.mass = x_mass
#     x_item.pledge = x_pledge
#     x_item.problem_bool = x_problem_bool
#     x_item._active = x__active
#     x_item._task = x__task
#     x_item._fund_coin = x__fund_coin
#     x_item._fund_onset = x__fund_onset
#     x_item._fund_cease = x__fund_cease
#     x_item._fund_ratio = x__fund_ratio
#     x_item._gogo_calc = x__gogo_calc
#     x_item._stop_calc = x__stop_calc
#     x_item._level = x__level
#     x_item._range_evaluated = x__range_evaluated
#     x_item._descendant_pledge_count = x__descendant_pledge_count
#     x_item._healerlink_ratio = x__healerlink_ratio
#     x_item._all_acct_cred = x__all_acct_cred
#     x_item._all_acct_debt = x__all_acct_debt
#     x_item.begin = x_begin
#     x_item.close = x_close
#     x_item.addin = x_addin
#     x_item.numor = x_numor
#     x_item.denom = x_denom
#     x_item.morph = x_morph
#     x_item.gogo_want = x_gogo_want
#     x_item.stop_want = x_stop_want
#     x_item.mass = x_mass
#     x_item.pledge = x_pledge
#     x_item.problem_bool = x_problem_bool
#     x_item._active = x__active
#     x_item._task = x__task
#     x_item._fund_coin = x__fund_coin
#     x_item._fund_onset = x__fund_onset
#     x_item._fund_cease = x__fund_cease
#     x_item._fund_ratio = x__fund_ratio
#     x_item._gogo_calc = x__gogo_calc
#     x_item._stop_calc = x__stop_calc
#     x_item._level = x__level
#     x_item._range_evaluated = x__range_evaluated
#     x_item._descendant_pledge_count = x__descendant_pledge_count
#     x_item._healerlink_ratio = x__healerlink_ratio
#     x_item._all_acct_cred = x__all_acct_cred
#     x_item._all_acct_debt = x__all_acct_debt

#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_forecast_tables(cursor)
#         x_table_name = "budunit_forecast"
#         assert get_row_count(cursor, x_table_name) == 0

#         # WHEN
#         insert_forecast_obj(cursor, sue_bud)

#         # THEN
#         assert get_row_count(cursor, x_table_name) == 1
#         select_sqlstr = f"SELECT * FROM {x_table_name};"
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         expected_row1 = (
#             x_fisc_title,
#             x_owner_name,
#             x_credor_respect,
#             x_debtor_respect,
#             x_fund_pool,
#             x_max_tree_traverse,
#             x_tally,
#             x_fund_coin,
#             x_penny,
#             x_respect_bit,
#             x__rational,
#             x__keeps_justified,
#             x__offtrack_fund,
#             x__sum_healerlink_share,
#             x__keeps_buildable,
#             x__tree_traverse_count,
#         )
#         expected_data = [expected_row1]
#         assert rows == expected_data

#     assert 1 == 2


# "budunit_forecast"
# "bud_acct_membership_forecast"
# "bud_acctunit_forecast"
# "bud_groupunit_forecast"
# "bud_item_awardlink_forecast"
# "bud_item_factunit_forecast"
# "bud_item_healerlink_forecast"
# "bud_item_reason_premiseunit_forecast"
# "bud_item_reasonunit_forecast"
# "bud_item_teamlink_forecast"
# "bud_itemunit_forecast"
