from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import get_row_count
from src.a01_term_logic.rope import create_rope
from src.a03_group_logic.group import (
    awardheir_shop,
    awardlink_shop,
    groupunit_shop,
    membership_shop,
)
from src.a03_group_logic.partner import partnerunit_shop
from src.a04_reason_logic.reason_labor import laborheir_shop, laborunit_shop
from src.a04_reason_logic.reason_plan import (
    caseunit_shop,
    factheir_shop,
    reasonheir_shop,
)
from src.a05_plan_logic.healer import healerlink_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a18_etl_toolbox.db_obj_believer_tool import (
    ObjKeysHolder,
    insert_job_blrawar,
    insert_job_blrfact,
    insert_job_blrgrou,
    insert_job_blrheal,
    insert_job_blrlabo,
    insert_job_blrmemb,
    insert_job_blrpern,
    insert_job_blrplan,
    insert_job_blrprem,
    insert_job_blrreas,
    insert_job_blrunit,
    insert_job_obj,
)
from src.a18_etl_toolbox.test._util.a18_env import env_dir_setup_cleanup
from src.a18_etl_toolbox.tran_sqlstrs import create_job_tables


def test_ObjKeysHolder_Exists():
    # ESTABLISH / WHEN
    x_objkeyholder = ObjKeysHolder()

    # THEN
    assert not x_objkeyholder.belief_label
    assert not x_objkeyholder.believer_name
    assert not x_objkeyholder.rope
    assert not x_objkeyholder.reason_context
    assert not x_objkeyholder.partner_name
    assert not x_objkeyholder.membership
    assert not x_objkeyholder.group_title
    assert not x_objkeyholder.fact_rope


def test_insert_job_blrunit_CreatesTableRowsFor_believerunit_job():
    # sourcery skip: extract-method
    # ESTABLISH
    x_belief_label = "amy23"
    x_believer_name = "Sue"
    x__keeps_buildable = 99
    x__keeps_justified = 77
    x__offtrack_fund = 55.5
    x__rational = 92
    x__sum_healerlink_share = 66.6
    x__tree_traverse_count = 7
    x_credor_respect = 88.2
    x_debtor_respect = 88.4
    x_fund_iota = 3.0
    x_fund_pool = 3000.0
    x_max_tree_traverse = 22
    x_penny = 4.0
    x_respect_bit = 0.2
    x_tally = 6
    sue_believer = believerunit_shop(
        believer_name=x_believer_name, belief_label=x_belief_label
    )
    sue_believer.fund_pool = x_fund_pool
    sue_believer.fund_iota = x_fund_iota
    sue_believer.penny = x_penny
    sue_believer.tally = x_tally
    sue_believer.respect_bit = x_respect_bit
    sue_believer.max_tree_traverse = x_max_tree_traverse
    sue_believer._keeps_buildable = x__keeps_buildable
    sue_believer._keeps_justified = x__keeps_justified
    sue_believer._offtrack_fund = x__offtrack_fund
    sue_believer._rational = x__rational
    sue_believer._sum_healerlink_share = x__sum_healerlink_share
    sue_believer._tree_traverse_count = x__tree_traverse_count
    sue_believer.credor_respect = x_credor_respect
    sue_believer.debtor_respect = x_debtor_respect

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "believerunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        objkeysholder = ObjKeysHolder()

        # WHEN
        insert_job_blrunit(cursor, objkeysholder, sue_believer)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            x_belief_label,
            x_believer_name,
            x_credor_respect,
            x_debtor_respect,
            x_fund_pool,
            x_max_tree_traverse,
            x_tally,
            x_fund_iota,
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


def test_insert_job_blrplan_CreatesTableRowsFor_blrplan_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_believer_calc_dimen_args("believer_planunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_plan.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")
    # print("")
    x_belief_label = "amy23"
    x_believer_name = 2
    casa_rope = create_rope(x_belief_label, "casa")
    x_parent_rope = casa_rope
    x_plan_label = "clean"
    x_begin = 5.0
    x_close = 6.0
    x_addin = 7.0
    x_numor = 8
    x_denom = 9
    x_morph = 10
    x_gogo_want = 11.0
    x_stop_want = 12.0
    x_mass = 13
    x_task = 14
    x_problem_bool = 15
    x__active = 16
    x__chore = 17
    x_fund_iota = 18.0
    x__fund_onset = 19.0
    x__fund_cease = 20.0
    x__fund_ratio = 21.0
    x__gogo_calc = 22.0
    x__stop_calc = 23.0
    x__level = 24
    x__range_evaluated = 25
    x__descendant_task_count = 26
    x__healerlink_ratio = 27.0
    x__all_partner_cred = 28
    x__all_partner_debt = 29
    x_plan = planunit_shop()
    x_plan.belief_label = x_belief_label
    x_plan.parent_rope = x_parent_rope
    x_plan.plan_label = x_plan_label
    x_plan.begin = x_begin
    x_plan.close = x_close
    x_plan.addin = x_addin
    x_plan.numor = x_numor
    x_plan.denom = x_denom
    x_plan.morph = x_morph
    x_plan.gogo_want = x_gogo_want
    x_plan.stop_want = x_stop_want
    x_plan.mass = x_mass
    x_plan.task = x_task
    x_plan.problem_bool = x_problem_bool
    x_plan._active = x__active
    x_plan._chore = x__chore
    x_plan.fund_iota = x_fund_iota
    x_plan._fund_onset = x__fund_onset
    x_plan._fund_cease = x__fund_cease
    x_plan._fund_ratio = x__fund_ratio
    x_plan._gogo_calc = x__gogo_calc
    x_plan._stop_calc = x__stop_calc
    x_plan._level = x__level
    x_plan._range_evaluated = x__range_evaluated
    x_plan._descendant_task_count = x__descendant_task_count
    x_plan._healerlink_ratio = x__healerlink_ratio
    x_plan._all_partner_cred = x__all_partner_cred
    x_plan._all_partner_debt = x__all_partner_debt
    x_plan.begin = x_begin
    x_plan.close = x_close
    x_plan.addin = x_addin
    x_plan.numor = x_numor
    x_plan.denom = x_denom
    x_plan.morph = x_morph
    x_plan.gogo_want = x_gogo_want
    x_plan.stop_want = x_stop_want
    x_plan.mass = x_mass
    x_plan.task = x_task
    x_plan.problem_bool = x_problem_bool
    x_plan._active = x__active
    x_plan._chore = x__chore
    x_plan.fund_iota = x_fund_iota
    x_plan._fund_onset = x__fund_onset
    x_plan._fund_cease = x__fund_cease
    x_plan._fund_ratio = x__fund_ratio
    x_plan._gogo_calc = x__gogo_calc
    x_plan._stop_calc = x__stop_calc
    x_plan._level = x__level
    x_plan._range_evaluated = x__range_evaluated
    x_plan._descendant_task_count = x__descendant_task_count
    x_plan._healerlink_ratio = x__healerlink_ratio
    x_plan._all_partner_cred = x__all_partner_cred
    x_plan._all_partner_debt = x__all_partner_debt

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "believer_planunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_belief_label, x_believer_name)

        # WHEN
        insert_job_blrplan(cursor, x_objkeysholder, x_plan)

        # THEN
        clean_rope = create_rope(casa_rope, "clean")
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            x_belief_label,
            str(x_believer_name),
            clean_rope,
            x_begin,
            x_close,
            x_addin,
            x_numor,
            x_denom,
            x_morph,
            x_gogo_want,
            x_stop_want,
            x_mass,
            x_task,
            x_problem_bool,
            x_fund_iota,
            x__active,
            x__chore,
            x__fund_onset,
            x__fund_cease,
            x__fund_ratio,
            x__gogo_calc,
            x__stop_calc,
            x__level,
            x__range_evaluated,
            x__descendant_task_count,
            x__healerlink_ratio,
            x__all_partner_cred,
            x__all_partner_debt,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blrreas_CreatesTableRowsFor_blrreas_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_believer_calc_dimen_args("believer_plan_reasonunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_reasonunit.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")
    # print("")

    x_belief_label = 1
    x_believer_name = 2
    x_rope = 3
    x_reason_context = 4
    x_reason_active_requisite = 5
    x__chore = 6
    x__status = 7
    x__rplan_active_value = 8
    x_reasonheir = reasonheir_shop(reason_context=x_reason_context)
    x_reasonheir.reason_context = x_reason_context
    x_reasonheir.reason_active_requisite = x_reason_active_requisite
    x_reasonheir._chore = x__chore
    x_reasonheir._status = x__status
    x_reasonheir._rplan_active_value = x__rplan_active_value

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "believer_plan_reasonunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_belief_label, x_believer_name, x_rope)

        # WHEN
        insert_job_blrreas(cursor, x_objkeysholder, x_reasonheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_belief_label),
            str(x_believer_name),
            str(x_rope),
            str(x_reason_context),
            x_reason_active_requisite,
            x__chore,
            x__status,
            x__rplan_active_value,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blrprem_CreatesTableRowsFor_blrprem_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_believer_calc_dimen_args("believer_plan_reason_caseunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_caseunit.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_belief_label = 1
    x_believer_name = 2
    x_rope = 3
    x_reason_context = 4
    x_reason_state = 5
    x_reason_upper = 6.0
    x_reason_lower = 7.0
    x_reason_divisor = 8
    x__chore = 9
    x__status = 10
    x_caseunit = caseunit_shop(reason_state=x_reason_state)
    x_caseunit.reason_state = x_reason_state
    x_caseunit.reason_upper = x_reason_upper
    x_caseunit.reason_lower = x_reason_lower
    x_caseunit.reason_divisor = x_reason_divisor
    x_caseunit._chore = x__chore
    x_caseunit._status = x__status

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "believer_plan_reason_caseunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            x_belief_label, x_believer_name, x_rope, x_reason_context
        )

        # WHEN
        insert_job_blrprem(cursor, x_objkeysholder, x_caseunit)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_belief_label),
            str(x_believer_name),
            str(x_rope),
            str(x_reason_context),
            str(x_reason_state),
            x_reason_upper,
            x_reason_lower,
            x_reason_divisor,
            x__chore,
            x__status,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blrmemb_CreatesTableRowsFor_blrmemb_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_believer_calc_dimen_args("believer_partner_membership")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_membership.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_belief_label = 1
    x_believer_name = 2
    x_partner_name = 3
    x_group_title = 4
    x_group_cred_points = 5.0
    x_group_debt_points = 6.0
    x__credor_pool = 7.0
    x__debtor_pool = 8.0
    x__fund_give = 9.0
    x__fund_take = 10.0
    x__fund_agenda_give = 11.0
    x__fund_agenda_take = 12.0
    x__fund_agenda_ratio_give = 13.0
    x__fund_agenda_ratio_take = 14.0
    x_membership = membership_shop(x_group_title)
    x_membership.partner_name = x_partner_name
    x_membership.group_cred_points = x_group_cred_points
    x_membership.group_debt_points = x_group_debt_points
    x_membership._credor_pool = x__credor_pool
    x_membership._debtor_pool = x__debtor_pool
    x_membership._fund_give = x__fund_give
    x_membership._fund_take = x__fund_take
    x_membership._fund_agenda_give = x__fund_agenda_give
    x_membership._fund_agenda_take = x__fund_agenda_take
    x_membership._fund_agenda_ratio_give = x__fund_agenda_ratio_give
    x_membership._fund_agenda_ratio_take = x__fund_agenda_ratio_take

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "believer_partner_membership_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_belief_label, x_believer_name)

        # WHEN
        insert_job_blrmemb(cursor, x_objkeysholder, x_membership)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_belief_label),
            str(x_believer_name),
            str(x_partner_name),
            str(x_group_title),
            x_group_cred_points,
            x_group_debt_points,
            x__credor_pool,
            x__debtor_pool,
            x__fund_give,
            x__fund_take,
            x__fund_agenda_give,
            x__fund_agenda_take,
            x__fund_agenda_ratio_give,
            x__fund_agenda_ratio_take,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blrpern_CreatesTableRowsFor_blrpern_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_believer_calc_dimen_args("believer_partnerunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_partner.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_belief_label = 1
    x_believer_name = 2
    x_partner_name = 3
    x_partner_cred_points = 4
    x_partner_debt_points = 5
    x__credor_pool = 6
    x__debtor_pool = 7
    x__fund_give = 8
    x__fund_take = 9
    x__fund_agenda_give = 10
    x__fund_agenda_take = 11
    x__fund_agenda_ratio_give = 12
    x__fund_agenda_ratio_take = 13
    x__inallocable_partner_debt_points = 14
    x__irrational_partner_debt_points = 15
    x_partner = partnerunit_shop(x_partner_name)
    x_partner.partner_name = x_partner_name
    x_partner.partner_cred_points = x_partner_cred_points
    x_partner.partner_debt_points = x_partner_debt_points
    x_partner._credor_pool = x__credor_pool
    x_partner._debtor_pool = x__debtor_pool
    x_partner._fund_give = x__fund_give
    x_partner._fund_take = x__fund_take
    x_partner._fund_agenda_give = x__fund_agenda_give
    x_partner._fund_agenda_take = x__fund_agenda_take
    x_partner._fund_agenda_ratio_give = x__fund_agenda_ratio_give
    x_partner._fund_agenda_ratio_take = x__fund_agenda_ratio_take
    x_partner._inallocable_partner_debt_points = x__inallocable_partner_debt_points
    x_partner._irrational_partner_debt_points = x__irrational_partner_debt_points

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "believer_partnerunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_belief_label, x_believer_name)

        # WHEN
        insert_job_blrpern(cursor, x_objkeysholder, x_partner)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_belief_label),
            str(x_believer_name),
            str(x_partner_name),
            x_partner_cred_points,
            x_partner_debt_points,
            x__credor_pool,
            x__debtor_pool,
            x__fund_give,
            x__fund_take,
            x__fund_agenda_give,
            x__fund_agenda_take,
            x__fund_agenda_ratio_give,
            x__fund_agenda_ratio_take,
            x__inallocable_partner_debt_points,
            x__irrational_partner_debt_points,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blrgrou_CreatesTableRowsFor_blrgrou_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_believer_calc_dimen_args("believer_groupunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_group.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_belief_label = 1
    x_believer_name = 2
    x_group_title = 3
    x_fund_iota = 4
    x_knot = 5
    x__credor_pool = 6
    x__debtor_pool = 7
    x__fund_give = 8
    x__fund_take = 9
    x__fund_agenda_give = 10
    x__fund_agenda_take = 11
    x_group = groupunit_shop(x_group_title)
    x_group.group_title = x_group_title
    x_group.fund_iota = x_fund_iota
    x_group.knot = x_knot
    x_group._credor_pool = x__credor_pool
    x_group._debtor_pool = x__debtor_pool
    x_group._fund_give = x__fund_give
    x_group._fund_take = x__fund_take
    x_group._fund_agenda_give = x__fund_agenda_give
    x_group._fund_agenda_take = x__fund_agenda_take

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "believer_groupunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_belief_label, x_believer_name)

        # WHEN
        insert_job_blrgrou(cursor, x_objkeysholder, x_group)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_belief_label),
            str(x_believer_name),
            str(x_group_title),
            x_fund_iota,
            str(x_knot),
            x__credor_pool,
            x__debtor_pool,
            x__fund_give,
            x__fund_take,
            x__fund_agenda_give,
            x__fund_agenda_take,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blrawar_CreatesTableRowsFor_blrawar_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_believer_calc_dimen_args("believer_plan_awardlink")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_awardheir.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_belief_label = 1
    x_believer_name = 2
    x_rope = 3
    x_awardee_title = 4
    x_give_force = 5
    x_take_force = 6
    x__fund_give = 7
    x__fund_take = 8
    x_awardheir = awardheir_shop(x_awardee_title)
    x_awardheir.awardee_title = x_awardee_title
    x_awardheir.give_force = x_give_force
    x_awardheir.take_force = x_take_force
    x_awardheir._fund_give = x__fund_give
    x_awardheir._fund_take = x__fund_take

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "believer_plan_awardlink_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_belief_label, x_believer_name, x_rope)

        # WHEN
        insert_job_blrawar(cursor, x_objkeysholder, x_awardheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_belief_label),
            str(x_believer_name),
            str(x_rope),
            str(x_awardee_title),
            x_give_force,
            x_take_force,
            x__fund_give,
            x__fund_take,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blrfact_CreatesTableRowsFor_blrfact_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_believer_calc_dimen_args("believer_plan_factunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_factheir.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_belief_label = 1
    x_believer_name = 2
    x_rope = 3
    x_reason_context = 4
    x_fact_state = 5
    x_fact_lower = 6
    x_fact_upper = 7
    x_factheir = factheir_shop()
    x_factheir.fact_context = x_reason_context
    x_factheir.fact_state = x_fact_state
    x_factheir.fact_lower = x_fact_lower
    x_factheir.fact_upper = x_fact_upper

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "believer_plan_factunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_belief_label, x_believer_name, x_rope)

        # WHEN
        insert_job_blrfact(cursor, x_objkeysholder, x_factheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_belief_label),
            str(x_believer_name),
            str(x_rope),
            str(x_reason_context),
            str(x_fact_state),
            x_fact_lower,
            x_fact_upper,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blrheal_CreatesTableRowsFor_blrheal_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_believer_calc_dimen_args("believer_plan_healerlink")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_healerlink.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_belief_label = 1
    x_believer_name = 2
    x_rope = 3
    bob_str = "Bob"
    sue_str = "Sue"
    x_healerlink = healerlink_shop()
    x_healerlink.set_healer_name(bob_str)
    x_healerlink.set_healer_name(sue_str)

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "believer_plan_healerlink_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_belief_label, x_believer_name, x_rope)

        # WHEN
        insert_job_blrheal(cursor, x_objkeysholder, x_healerlink)

        # THEN
        assert get_row_count(cursor, x_table_name) == 2
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_belief_label),
            str(x_believer_name),
            str(x_rope),
            bob_str,
        )
        expected_row2 = (
            str(x_belief_label),
            str(x_believer_name),
            str(x_rope),
            sue_str,
        )
        expected_data = [expected_row1, expected_row2]
        assert rows == expected_data


def test_insert_job_blrlabo_CreatesTableRowsFor_blrlabo_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_believer_calc_dimen_args("believer_plan_laborlink")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_laborheir.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_belief_label = 1
    x_believer_name = 2
    x_rope = 3
    x__believer_name_labor = 5
    x_laborheir = laborheir_shop()
    x_laborheir._believer_name_labor = x__believer_name_labor
    bob_str = "Bob"
    sue_str = "Sue"
    x_laborheir._laborlinks = {bob_str, sue_str}

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "believer_plan_laborlink_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_belief_label, x_believer_name, x_rope)

        # WHEN
        insert_job_blrlabo(cursor, x_objkeysholder, x_laborheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 2
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_belief_label),
            str(x_believer_name),
            str(x_rope),
            bob_str,
            x__believer_name_labor,
        )
        expected_row2 = (
            str(x_belief_label),
            str(x_believer_name),
            str(x_rope),
            sue_str,
            x__believer_name_labor,
        )
        expected_data = [expected_row1, expected_row2]
        assert rows == expected_data


def test_insert_job_obj_CreatesTableRows_Scenario0():
    # sourcery skip: extract-method
    # ESTABLISH
    a23_str = "amy23"
    sue_str = "Sue"
    bob_str = "Bob"
    run_str = ";run"
    sue_believer = believerunit_shop(sue_str, a23_str)
    sue_believer.add_partnerunit(sue_str)
    sue_believer.add_partnerunit(bob_str)
    sue_believer.get_partner(bob_str).add_membership(run_str)
    casa_rope = sue_believer.make_l1_rope("casa")
    status_rope = sue_believer.make_l1_rope("status")
    clean_rope = sue_believer.make_rope(status_rope, "clean")
    dirty_rope = sue_believer.make_rope(status_rope, "dirty")
    sue_believer.add_plan(casa_rope)
    sue_believer.add_plan(clean_rope)
    sue_believer.add_plan(dirty_rope)
    sue_believer.edit_plan_attr(
        casa_rope, reason_context=status_rope, reason_case=dirty_rope
    )
    sue_believer.edit_plan_attr(casa_rope, awardlink=awardlink_shop(run_str))
    sue_believer.edit_plan_attr(casa_rope, healerlink=healerlink_shop({bob_str}))
    sue_believer.edit_plan_attr(casa_rope, laborunit=laborunit_shop({sue_str}))
    sue_believer.add_fact(status_rope, clean_rope)

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        blrmemb_job_table = "believer_partner_membership_job"
        blrpern_job_table = "believer_partnerunit_job"
        blrgrou_job_table = "believer_groupunit_job"
        blrawar_job_table = "believer_plan_awardlink_job"
        blrfact_job_table = "believer_plan_factunit_job"
        blrheal_job_table = "believer_plan_healerlink_job"
        blrprem_job_table = "believer_plan_reason_caseunit_job"
        blrreas_job_table = "believer_plan_reasonunit_job"
        blrlabo_job_table = "believer_plan_laborlink_job"
        blrplan_job_table = "believer_planunit_job"
        blrunit_job_table = "believerunit_job"
        assert get_row_count(cursor, blrunit_job_table) == 0
        assert get_row_count(cursor, blrplan_job_table) == 0
        assert get_row_count(cursor, blrpern_job_table) == 0
        assert get_row_count(cursor, blrmemb_job_table) == 0
        assert get_row_count(cursor, blrgrou_job_table) == 0
        assert get_row_count(cursor, blrawar_job_table) == 0
        assert get_row_count(cursor, blrfact_job_table) == 0
        assert get_row_count(cursor, blrheal_job_table) == 0
        assert get_row_count(cursor, blrreas_job_table) == 0
        assert get_row_count(cursor, blrprem_job_table) == 0
        assert get_row_count(cursor, blrlabo_job_table) == 0

        # WHEN
        insert_job_obj(cursor, sue_believer)

        # THEN
        assert get_row_count(cursor, blrunit_job_table) == 1
        assert get_row_count(cursor, blrplan_job_table) == 5
        assert get_row_count(cursor, blrpern_job_table) == 2
        assert get_row_count(cursor, blrmemb_job_table) == 3
        assert get_row_count(cursor, blrgrou_job_table) == 3
        assert get_row_count(cursor, blrawar_job_table) == 1
        assert get_row_count(cursor, blrfact_job_table) == 1
        assert get_row_count(cursor, blrheal_job_table) == 1
        assert get_row_count(cursor, blrreas_job_table) == 1
        assert get_row_count(cursor, blrprem_job_table) == 1
        assert get_row_count(cursor, blrlabo_job_table) == 1
