from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import get_row_count
from src.ch03_voice.group import (
    awardheir_shop,
    awardunit_shop,
    groupunit_shop,
    membership_shop,
)
from src.ch03_voice.labor import laborheir_shop, laborunit_shop, partyheir_shop
from src.ch03_voice.voice import voiceunit_shop
from src.ch04_rope.rope import create_rope
from src.ch05_reason.reason import caseunit_shop, factheir_shop, reasonheir_shop
from src.ch06_plan.healer import healerunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch18_world_etl.db_obj_belief_tool import (
    ObjKeysHolder,
    insert_job_blfvoce,
    insert_job_blrawar,
    insert_job_blrcase,
    insert_job_blrfact,
    insert_job_blrgrou,
    insert_job_blrheal,
    insert_job_blrlabo,
    insert_job_blrmemb,
    insert_job_blrplan,
    insert_job_blrreas,
    insert_job_blrunit,
    insert_job_obj,
)
from src.ch18_world_etl.test._util.ch18_env import temp_dir_setup
from src.ch18_world_etl.tran_sqlstrs import create_job_tables
from src.ref.keywords import Ch18Keywords as kw


def test_ObjKeysHolder_Exists():
    # ESTABLISH / WHEN
    x_objkeyholder = ObjKeysHolder()

    # THEN
    assert not x_objkeyholder.moment_label
    assert not x_objkeyholder.belief_name
    assert not x_objkeyholder.rope
    assert not x_objkeyholder.reason_context
    assert not x_objkeyholder.voice_name
    assert not x_objkeyholder.membership
    assert not x_objkeyholder.group_title
    assert not x_objkeyholder.fact_rope


def test_insert_job_blrunit_CreatesTableRowsFor_beliefunit_job():
    # sourcery skip: extract-method
    # ESTABLISH
    x_moment_label = "amy23"
    x_belief_name = "Sue"
    x_keeps_buildable = 99
    x_keeps_justified = 77
    x_offtrack_fund = 55.5
    x_rational = 92
    x_sum_healerunit_plans_fund_total = 66.6
    x_tree_traverse_count = 7
    x_credor_respect = 88.2
    x_debtor_respect = 88.4
    x_fund_grain = 3.0
    x_fund_pool = 3000.0
    x_max_tree_traverse = 22
    x_mana_grain = 4.0
    x_respect_grain = 0.2
    x_tally = 6
    sue_belief = beliefunit_shop(x_belief_name, moment_label=x_moment_label)
    sue_belief.fund_pool = x_fund_pool
    sue_belief.fund_grain = x_fund_grain
    sue_belief.mana_grain = x_mana_grain
    sue_belief.tally = x_tally
    sue_belief.respect_grain = x_respect_grain
    sue_belief.max_tree_traverse = x_max_tree_traverse
    sue_belief.keeps_buildable = x_keeps_buildable
    sue_belief.keeps_justified = x_keeps_justified
    sue_belief.offtrack_fund = x_offtrack_fund
    sue_belief.rational = x_rational
    sue_belief.sum_healerunit_plans_fund_total = x_sum_healerunit_plans_fund_total
    sue_belief.tree_traverse_count = x_tree_traverse_count
    sue_belief.credor_respect = x_credor_respect
    sue_belief.debtor_respect = x_debtor_respect

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "beliefunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        objkeysholder = ObjKeysHolder()

        # WHEN
        insert_job_blrunit(cursor, objkeysholder, sue_belief)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            x_moment_label,
            x_belief_name,
            x_credor_respect,
            x_debtor_respect,
            x_fund_pool,
            x_max_tree_traverse,
            x_tally,
            x_fund_grain,
            x_mana_grain,
            x_respect_grain,
            x_rational,
            x_keeps_justified,
            x_offtrack_fund,
            x_sum_healerunit_plans_fund_total,
            x_keeps_buildable,
            x_tree_traverse_count,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blrplan_CreatesTableRowsFor_blrplan_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_belief_calc_dimen_args("belief_planunit")
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
    x_moment_label = "amy23"
    x_belief_name = 2
    casa_rope = create_rope(x_moment_label, "casa")
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
    x_star = 13
    x_pledge = 14
    x_problem_bool = 15
    x_active = 16
    x_task = 17
    x_fund_grain = 18.0
    x_fund_onset = 19.0
    x_fund_cease = 20.0
    x_fund_ratio = 21.0
    x_gogo_calc = 22.0
    x_stop_calc = 23.0
    x_level = 24
    x_range_evaluated = 25
    x_descendant_pledge_count = 26
    x_healerunit_ratio = 27.0
    x_all_voice_cred = 28
    x_all_voice_debt = 29
    casa_str = "casa"
    x_plan = planunit_shop(casa_str)
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
    x_plan.star = x_star
    x_plan.pledge = x_pledge
    x_plan.problem_bool = x_problem_bool
    x_plan.plan_active = x_active
    x_plan.task = x_task
    x_plan.fund_grain = x_fund_grain
    x_plan.fund_onset = x_fund_onset
    x_plan.fund_cease = x_fund_cease
    x_plan.fund_ratio = x_fund_ratio
    x_plan.gogo_calc = x_gogo_calc
    x_plan.stop_calc = x_stop_calc
    x_plan.tree_level = x_level
    x_plan.range_evaluated = x_range_evaluated
    x_plan.descendant_pledge_count = x_descendant_pledge_count
    x_plan.healerunit_ratio = x_healerunit_ratio
    x_plan.all_voice_cred = x_all_voice_cred
    x_plan.all_voice_debt = x_all_voice_debt
    x_plan.begin = x_begin
    x_plan.close = x_close
    x_plan.addin = x_addin
    x_plan.numor = x_numor
    x_plan.denom = x_denom
    x_plan.morph = x_morph
    x_plan.gogo_want = x_gogo_want
    x_plan.stop_want = x_stop_want
    x_plan.star = x_star
    x_plan.pledge = x_pledge
    x_plan.problem_bool = x_problem_bool
    x_plan.plan_active = x_active
    x_plan.task = x_task
    x_plan.fund_grain = x_fund_grain
    x_plan.fund_onset = x_fund_onset
    x_plan.fund_cease = x_fund_cease
    x_plan.fund_ratio = x_fund_ratio
    x_plan.gogo_calc = x_gogo_calc
    x_plan.stop_calc = x_stop_calc
    x_plan.tree_level = x_level
    x_plan.range_evaluated = x_range_evaluated
    x_plan.descendant_pledge_count = x_descendant_pledge_count
    x_plan.healerunit_ratio = x_healerunit_ratio
    x_plan.all_voice_cred = x_all_voice_cred
    x_plan.all_voice_debt = x_all_voice_debt

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "belief_planunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_moment_label, x_belief_name)

        # WHEN
        insert_job_blrplan(cursor, x_objkeysholder, x_plan)

        # THEN
        clean_rope = create_rope(casa_rope, "clean")
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            None,
            str(x_belief_name),
            clean_rope,
            x_begin,
            x_close,
            x_addin,
            x_numor,
            x_denom,
            x_morph,
            x_gogo_want,
            x_stop_want,
            x_star,
            x_pledge,
            x_problem_bool,
            x_fund_grain,
            x_active,
            x_task,
            x_fund_onset,
            x_fund_cease,
            x_fund_ratio,
            x_gogo_calc,
            x_stop_calc,
            x_level,
            x_range_evaluated,
            x_descendant_pledge_count,
            x_healerunit_ratio,
            x_all_voice_cred,
            x_all_voice_debt,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blrreas_CreatesTableRowsFor_blrreas_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_belief_calc_dimen_args("belief_plan_reasonunit")
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

    x_moment_label = 1
    x_belief_name = 2
    x_rope = 3
    x_reason_context = 4
    x_active_requisite = 5
    x_task = 6
    x_reason_active = 7
    x__heir_active = 8
    x_reasonheir = reasonheir_shop(reason_context=x_reason_context)
    x_reasonheir.reason_context = x_reason_context
    x_reasonheir.active_requisite = x_active_requisite
    x_reasonheir.task = x_task
    x_reasonheir.reason_active = x_reason_active
    x_reasonheir.parent_heir_active = x__heir_active

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "belief_plan_reasonunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_moment_label, x_belief_name, x_rope)

        # WHEN
        insert_job_blrreas(cursor, x_objkeysholder, x_reasonheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_moment_label),
            str(x_belief_name),
            str(x_rope),
            str(x_reason_context),
            x_active_requisite,
            x_task,
            x_reason_active,
            x__heir_active,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blrcase_CreatesTableRowsFor_blrcase_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_belief_calc_dimen_args("belief_plan_reason_caseunit")
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

    x_moment_label = 1
    x_belief_name = 2
    x_rope = 3
    x_reason_context = 4
    x_reason_state = 5
    x_reason_upper = 6.0
    x_reason_lower = 7.0
    x_reason_divisor = 8
    x_task = 9
    x_case_active = 10
    x_caseunit = caseunit_shop(reason_state=x_reason_state)
    x_caseunit.reason_state = x_reason_state
    x_caseunit.reason_upper = x_reason_upper
    x_caseunit.reason_lower = x_reason_lower
    x_caseunit.reason_divisor = x_reason_divisor
    x_caseunit.task = x_task
    x_caseunit.case_active = x_case_active

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "belief_plan_reason_caseunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            x_moment_label, x_belief_name, x_rope, x_reason_context
        )

        # WHEN
        insert_job_blrcase(cursor, x_objkeysholder, x_caseunit)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_moment_label),
            str(x_belief_name),
            str(x_rope),
            str(x_reason_context),
            str(x_reason_state),
            x_reason_upper,
            x_reason_lower,
            x_reason_divisor,
            x_task,
            x_case_active,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blrmemb_CreatesTableRowsFor_blrmemb_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_belief_calc_dimen_args("belief_voice_membership")
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

    x_moment_label = 1
    x_belief_name = 2
    x_voice_name = 3
    x_group_title = 4
    x_group_cred_lumen = 5.0
    x_group_debt_lumen = 6.0
    x_credor_pool = 7.0
    x_debtor_pool = 8.0
    x_fund_give = 9.0
    x_fund_take = 10.0
    x_fund_agenda_give = 11.0
    x_fund_agenda_take = 12.0
    x_fund_agenda_ratio_give = 13.0
    x_fund_agenda_ratio_take = 14.0
    x_membership = membership_shop(x_group_title)
    x_membership.voice_name = x_voice_name
    x_membership.group_cred_lumen = x_group_cred_lumen
    x_membership.group_debt_lumen = x_group_debt_lumen
    x_membership.credor_pool = x_credor_pool
    x_membership.debtor_pool = x_debtor_pool
    x_membership.fund_give = x_fund_give
    x_membership.fund_take = x_fund_take
    x_membership.fund_agenda_give = x_fund_agenda_give
    x_membership.fund_agenda_take = x_fund_agenda_take
    x_membership.fund_agenda_ratio_give = x_fund_agenda_ratio_give
    x_membership.fund_agenda_ratio_take = x_fund_agenda_ratio_take

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "belief_voice_membership_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_moment_label, x_belief_name)

        # WHEN
        insert_job_blrmemb(cursor, x_objkeysholder, x_membership)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_moment_label),
            str(x_belief_name),
            str(x_voice_name),
            str(x_group_title),
            x_group_cred_lumen,
            x_group_debt_lumen,
            x_credor_pool,
            x_debtor_pool,
            x_fund_give,
            x_fund_take,
            x_fund_agenda_give,
            x_fund_agenda_take,
            x_fund_agenda_ratio_give,
            x_fund_agenda_ratio_take,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blfvoce_CreatesTableRowsFor_blfvoce_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_belief_calc_dimen_args("belief_voiceunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_voice.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_moment_label = 1
    x_belief_name = 2
    x_voice_name = 3
    x_voice_cred_lumen = 4
    x_voice_debt_lumen = 5
    x_credor_pool = 6
    x_debtor_pool = 7
    x_fund_give = 8
    x_fund_take = 9
    x_fund_agenda_give = 10
    x_fund_agenda_take = 11
    x_fund_agenda_ratio_give = 12
    x_fund_agenda_ratio_take = 13
    x_inallocable_voice_debt_lumen = 14
    x_irrational_voice_debt_lumen = 15
    x_groupmark = 16
    x_voice = voiceunit_shop(x_voice_name)
    x_voice.voice_name = x_voice_name
    x_voice.voice_cred_lumen = x_voice_cred_lumen
    x_voice.voice_debt_lumen = x_voice_debt_lumen
    x_voice.credor_pool = x_credor_pool
    x_voice.debtor_pool = x_debtor_pool
    x_voice.fund_give = x_fund_give
    x_voice.fund_take = x_fund_take
    x_voice.fund_agenda_give = x_fund_agenda_give
    x_voice.fund_agenda_take = x_fund_agenda_take
    x_voice.fund_agenda_ratio_give = x_fund_agenda_ratio_give
    x_voice.fund_agenda_ratio_take = x_fund_agenda_ratio_take
    x_voice.inallocable_voice_debt_lumen = x_inallocable_voice_debt_lumen
    x_voice.irrational_voice_debt_lumen = x_irrational_voice_debt_lumen
    x_voice.groupmark = x_groupmark

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "belief_voiceunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_moment_label, x_belief_name)

        # WHEN
        insert_job_blfvoce(cursor, x_objkeysholder, x_voice)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_moment_label),
            str(x_belief_name),
            str(x_voice_name),
            x_voice_cred_lumen,
            x_voice_debt_lumen,
            str(x_groupmark),
            x_credor_pool,
            x_debtor_pool,
            x_fund_give,
            x_fund_take,
            x_fund_agenda_give,
            x_fund_agenda_take,
            x_fund_agenda_ratio_give,
            x_fund_agenda_ratio_take,
            x_inallocable_voice_debt_lumen,
            x_irrational_voice_debt_lumen,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blrgrou_CreatesTableRowsFor_blrgrou_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_belief_calc_dimen_args("belief_groupunit")
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

    x_moment_label = 1
    x_belief_name = 2
    x_group_title = 3
    x_fund_grain = 4
    x_credor_pool = 6
    x_debtor_pool = 7
    x_fund_give = 8
    x_fund_take = 9
    x_fund_agenda_give = 10
    x_fund_agenda_take = 11
    x_group = groupunit_shop(x_group_title)
    x_group.group_title = x_group_title
    x_group.fund_grain = x_fund_grain
    x_group.credor_pool = x_credor_pool
    x_group.debtor_pool = x_debtor_pool
    x_group.fund_give = x_fund_give
    x_group.fund_take = x_fund_take
    x_group.fund_agenda_give = x_fund_agenda_give
    x_group.fund_agenda_take = x_fund_agenda_take

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "belief_groupunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_moment_label, x_belief_name)

        # WHEN
        insert_job_blrgrou(cursor, x_objkeysholder, x_group)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_moment_label),
            str(x_belief_name),
            str(x_group_title),
            x_fund_grain,
            x_credor_pool,
            x_debtor_pool,
            x_fund_give,
            x_fund_take,
            x_fund_agenda_give,
            x_fund_agenda_take,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blrawar_CreatesTableRowsFor_blrawar_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_belief_calc_dimen_args("belief_plan_awardunit")
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

    x_moment_label = 1
    x_belief_name = 2
    x_rope = 3
    x_awardee_title = 4
    x_give_force = 5
    x_take_force = 6
    x_fund_give = 7
    x_fund_take = 8
    x_awardheir = awardheir_shop(x_awardee_title)
    x_awardheir.awardee_title = x_awardee_title
    x_awardheir.give_force = x_give_force
    x_awardheir.take_force = x_take_force
    x_awardheir.fund_give = x_fund_give
    x_awardheir.fund_take = x_fund_take

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "belief_plan_awardunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_moment_label, x_belief_name, x_rope)

        # WHEN
        insert_job_blrawar(cursor, x_objkeysholder, x_awardheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_moment_label),
            str(x_belief_name),
            str(x_rope),
            str(x_awardee_title),
            x_give_force,
            x_take_force,
            x_fund_give,
            x_fund_take,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_blrfact_CreatesTableRowsFor_blrfact_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_belief_calc_dimen_args("belief_plan_factunit")
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

    x_moment_label = 1
    x_belief_name = 2
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
        x_table_name = "belief_plan_factunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_moment_label, x_belief_name, x_rope)

        # WHEN
        insert_job_blrfact(cursor, x_objkeysholder, x_factheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_moment_label),
            str(x_belief_name),
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
    # x_args = get_belief_calc_dimen_args("belief_plan_healerunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_healerunit.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_moment_label = 1
    x_belief_name = 2
    x_rope = 3
    bob_str = "Bob"
    sue_str = "Sue"
    x_healerunit = healerunit_shop()
    x_healerunit.set_healer_name(bob_str)
    x_healerunit.set_healer_name(sue_str)

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "belief_plan_healerunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_moment_label, x_belief_name, x_rope)

        # WHEN
        insert_job_blrheal(cursor, x_objkeysholder, x_healerunit)

        # THEN
        assert get_row_count(cursor, x_table_name) == 2
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_moment_label),
            str(x_belief_name),
            str(x_rope),
            bob_str,
        )
        expected_row2 = (
            str(x_moment_label),
            str(x_belief_name),
            str(x_rope),
            sue_str,
        )
        expected_data = [expected_row1, expected_row2]
        assert rows == expected_data


def test_insert_job_blrlabo_CreatesTableRowsFor_blrlabo_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_belief_calc_dimen_args("belief_plan_partyunit")
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

    x_moment_label = 1
    x_belief_name = 2
    x_rope = 3
    x__belief_name_is_labor = 5
    x_laborheir = laborheir_shop()
    x_laborheir.belief_name_is_labor = x__belief_name_is_labor
    bob_str = "Bob"
    bob_solo_bool = 6
    sue_str = "Sue"
    sue_solo_bool = 7
    bob_partyheir = partyheir_shop(bob_str, bob_solo_bool)
    sue_partyheir = partyheir_shop(sue_str, sue_solo_bool)
    x_laborheir.partys = {bob_str: bob_partyheir, sue_str: sue_partyheir}

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "belief_plan_partyunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_moment_label, x_belief_name, x_rope)

        # WHEN
        insert_job_blrlabo(cursor, x_objkeysholder, x_laborheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 2
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_moment_label),
            str(x_belief_name),
            str(x_rope),
            bob_str,
            bob_solo_bool,
            x__belief_name_is_labor,
        )
        expected_row2 = (
            str(x_moment_label),
            str(x_belief_name),
            str(x_rope),
            sue_str,
            sue_solo_bool,
            x__belief_name_is_labor,
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
    sue_belief = beliefunit_shop(sue_str, a23_str)
    sue_belief.add_voiceunit(sue_str)
    sue_belief.add_voiceunit(bob_str)
    sue_belief.get_voice(bob_str).add_membership(run_str)
    casa_rope = sue_belief.make_l1_rope("casa")
    situation_rope = sue_belief.make_l1_rope(kw.reason_active)
    clean_rope = sue_belief.make_rope(situation_rope, "clean")
    dirty_rope = sue_belief.make_rope(situation_rope, "dirty")
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(clean_rope)
    sue_belief.add_plan(dirty_rope)
    sue_belief.edit_plan_attr(
        casa_rope, reason_context=situation_rope, reason_case=dirty_rope
    )
    sue_belief.edit_plan_attr(casa_rope, awardunit=awardunit_shop(run_str))
    sue_belief.edit_plan_attr(casa_rope, healerunit=healerunit_shop({bob_str}))
    casa_laborunit = laborunit_shop()
    casa_laborunit.add_party(sue_str, True)
    sue_belief.edit_plan_attr(casa_rope, laborunit=casa_laborunit)
    sue_belief.add_fact(situation_rope, clean_rope)

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        blrmemb_job_table = f"{kw.belief_voice_membership}_job"
        blfvoce_job_table = f"{kw.belief_voiceunit}_job"
        blrgrou_job_table = f"{kw.belief_groupunit}_job"
        blrawar_job_table = f"{kw.belief_plan_awardunit}_job"
        blrfact_job_table = f"{kw.belief_plan_factunit}_job"
        blrheal_job_table = f"{kw.belief_plan_healerunit}_job"
        blrcase_job_table = f"{kw.belief_plan_reason_caseunit}_job"
        blrreas_job_table = f"{kw.belief_plan_reasonunit}_job"
        blrlabo_job_table = f"{kw.belief_plan_partyunit}_job"
        blrplan_job_table = f"{kw.belief_planunit}_job"
        blrunit_job_table = f"{kw.beliefunit}_job"
        assert get_row_count(cursor, blrunit_job_table) == 0
        assert get_row_count(cursor, blrplan_job_table) == 0
        assert get_row_count(cursor, blfvoce_job_table) == 0
        assert get_row_count(cursor, blrmemb_job_table) == 0
        assert get_row_count(cursor, blrgrou_job_table) == 0
        assert get_row_count(cursor, blrawar_job_table) == 0
        assert get_row_count(cursor, blrfact_job_table) == 0
        assert get_row_count(cursor, blrheal_job_table) == 0
        assert get_row_count(cursor, blrreas_job_table) == 0
        assert get_row_count(cursor, blrcase_job_table) == 0
        assert get_row_count(cursor, blrlabo_job_table) == 0

        # WHEN
        insert_job_obj(cursor, sue_belief)

        # THEN
        assert get_row_count(cursor, blrunit_job_table) == 1
        assert get_row_count(cursor, blrplan_job_table) == 5
        assert get_row_count(cursor, blfvoce_job_table) == 2
        assert get_row_count(cursor, blrmemb_job_table) == 3
        assert get_row_count(cursor, blrgrou_job_table) == 3
        assert get_row_count(cursor, blrawar_job_table) == 1
        assert get_row_count(cursor, blrfact_job_table) == 1
        assert get_row_count(cursor, blrheal_job_table) == 1
        assert get_row_count(cursor, blrreas_job_table) == 1
        assert get_row_count(cursor, blrcase_job_table) == 1
        assert get_row_count(cursor, blrlabo_job_table) == 1
