from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import get_row_count
from src.a01_term_logic.way import create_way
from src.a03_group_logic.acct import acctunit_shop
from src.a03_group_logic.group import (
    awardheir_shop,
    awardlink_shop,
    groupunit_shop,
    membership_shop,
)
from src.a04_reason_logic.reason_concept import (
    factheir_shop,
    premiseunit_shop,
    reasonheir_shop,
)
from src.a04_reason_logic.reason_labor import laborheir_shop, laborunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a05_concept_logic.healer import healerlink_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a18_etl_toolbox._test_util.a18_env import env_dir_setup_cleanup
from src.a18_etl_toolbox.db_obj_bud_tool import (
    ObjKeysHolder,
    insert_job_budacct,
    insert_job_budawar,
    insert_job_budconc,
    insert_job_budfact,
    insert_job_budgrou,
    insert_job_budheal,
    insert_job_budlabo,
    insert_job_budmemb,
    insert_job_budprem,
    insert_job_budreas,
    insert_job_budunit,
    insert_job_obj,
)
from src.a18_etl_toolbox.tran_sqlstrs import create_job_tables


def test_ObjKeysHolder_Exists():
    # ESTABLISH / WHEN
    x_objkeyholder = ObjKeysHolder()

    # THEN
    assert not x_objkeyholder.fisc_label
    assert not x_objkeyholder.owner_name
    assert not x_objkeyholder.way
    assert not x_objkeyholder.rcontext
    assert not x_objkeyholder.acct_name
    assert not x_objkeyholder.membership
    assert not x_objkeyholder.group_title
    assert not x_objkeyholder.fact_way


def test_insert_job_budunit_CreatesTableRowsFor_budunit_job():
    # sourcery skip: extract-method
    # ESTABLISH
    x_fisc_label = "accord23"
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
    sue_bud = budunit_shop(owner_name=x_owner_name, fisc_label=x_fisc_label)
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
        create_job_tables(cursor)
        x_table_name = "budunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        objkeysholder = ObjKeysHolder()

        # WHEN
        insert_job_budunit(cursor, objkeysholder, sue_bud)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            x_fisc_label,
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


def test_insert_job_budconc_CreatesTableRowsFor_budconc_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_bud_calc_dimen_args("bud_conceptunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_concept.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")
    # print("")
    x_fisc_label = "accord23"
    x_owner_name = 2
    casa_way = create_way(x_fisc_label, "casa")
    x_parent_way = casa_way
    x_concept_label = "clean"
    x_begin = 5.0
    x_close = 6.0
    x_addin = 7.0
    x_numor = 8
    x_denom = 9
    x_morph = 10
    x_gogo_want = 11.0
    x_stop_want = 12.0
    x_mass = 13
    x_pledge = 14
    x_problem_bool = 15
    x__active = 16
    x__task = 17
    x_fund_coin = 18.0
    x__fund_onset = 19.0
    x__fund_cease = 20.0
    x__fund_ratio = 21.0
    x__gogo_calc = 22.0
    x__stop_calc = 23.0
    x__level = 24
    x__range_evaluated = 25
    x__descendant_pledge_count = 26
    x__healerlink_ratio = 27.0
    x__all_acct_cred = 28
    x__all_acct_debt = 29
    x_concept = conceptunit_shop()
    x_concept.fisc_label = x_fisc_label
    x_concept.parent_way = x_parent_way
    x_concept.concept_label = x_concept_label
    x_concept.begin = x_begin
    x_concept.close = x_close
    x_concept.addin = x_addin
    x_concept.numor = x_numor
    x_concept.denom = x_denom
    x_concept.morph = x_morph
    x_concept.gogo_want = x_gogo_want
    x_concept.stop_want = x_stop_want
    x_concept.mass = x_mass
    x_concept.pledge = x_pledge
    x_concept.problem_bool = x_problem_bool
    x_concept._active = x__active
    x_concept._task = x__task
    x_concept.fund_coin = x_fund_coin
    x_concept._fund_onset = x__fund_onset
    x_concept._fund_cease = x__fund_cease
    x_concept._fund_ratio = x__fund_ratio
    x_concept._gogo_calc = x__gogo_calc
    x_concept._stop_calc = x__stop_calc
    x_concept._level = x__level
    x_concept._range_evaluated = x__range_evaluated
    x_concept._descendant_pledge_count = x__descendant_pledge_count
    x_concept._healerlink_ratio = x__healerlink_ratio
    x_concept._all_acct_cred = x__all_acct_cred
    x_concept._all_acct_debt = x__all_acct_debt
    x_concept.begin = x_begin
    x_concept.close = x_close
    x_concept.addin = x_addin
    x_concept.numor = x_numor
    x_concept.denom = x_denom
    x_concept.morph = x_morph
    x_concept.gogo_want = x_gogo_want
    x_concept.stop_want = x_stop_want
    x_concept.mass = x_mass
    x_concept.pledge = x_pledge
    x_concept.problem_bool = x_problem_bool
    x_concept._active = x__active
    x_concept._task = x__task
    x_concept.fund_coin = x_fund_coin
    x_concept._fund_onset = x__fund_onset
    x_concept._fund_cease = x__fund_cease
    x_concept._fund_ratio = x__fund_ratio
    x_concept._gogo_calc = x__gogo_calc
    x_concept._stop_calc = x__stop_calc
    x_concept._level = x__level
    x_concept._range_evaluated = x__range_evaluated
    x_concept._descendant_pledge_count = x__descendant_pledge_count
    x_concept._healerlink_ratio = x__healerlink_ratio
    x_concept._all_acct_cred = x__all_acct_cred
    x_concept._all_acct_debt = x__all_acct_debt

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "bud_conceptunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_fisc_label, x_owner_name)

        # WHEN
        insert_job_budconc(cursor, x_objkeysholder, x_concept)

        # THEN
        clean_way = create_way(casa_way, "clean")
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            x_fisc_label,
            str(x_owner_name),
            clean_way,
            x_begin,
            x_close,
            x_addin,
            x_numor,
            x_denom,
            x_morph,
            x_gogo_want,
            x_stop_want,
            x_mass,
            x_pledge,
            x_problem_bool,
            x_fund_coin,
            x__active,
            x__task,
            x__fund_onset,
            x__fund_cease,
            x__fund_ratio,
            x__gogo_calc,
            x__stop_calc,
            x__level,
            x__range_evaluated,
            x__descendant_pledge_count,
            x__healerlink_ratio,
            x__all_acct_cred,
            x__all_acct_debt,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_budreas_CreatesTableRowsFor_budreas_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_bud_calc_dimen_args("bud_concept_reasonunit")
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

    x_fisc_label = 1
    x_owner_name = 2
    x_way = 3
    x_rcontext = 4
    x_rconcept_active_requisite = 5
    x__task = 6
    x__status = 7
    x__rconcept_active_value = 8
    x_reasonheir = reasonheir_shop(rcontext=x_rcontext)
    x_reasonheir.rcontext = x_rcontext
    x_reasonheir.rconcept_active_requisite = x_rconcept_active_requisite
    x_reasonheir._task = x__task
    x_reasonheir._status = x__status
    x_reasonheir._rconcept_active_value = x__rconcept_active_value

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "bud_concept_reasonunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_fisc_label, x_owner_name, x_way)

        # WHEN
        insert_job_budreas(cursor, x_objkeysholder, x_reasonheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_fisc_label),
            str(x_owner_name),
            str(x_way),
            str(x_rcontext),
            x_rconcept_active_requisite,
            x__task,
            x__status,
            x__rconcept_active_value,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_budprem_CreatesTableRowsFor_budprem_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_bud_calc_dimen_args("bud_concept_reason_premiseunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_premiseunit.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_fisc_label = 1
    x_owner_name = 2
    x_way = 3
    x_rcontext = 4
    x_pstate = 5
    x_pnigh = 6.0
    x_popen = 7.0
    x_pdivisor = 8
    x__task = 9
    x__status = 10
    x_premiseunit = premiseunit_shop(pstate=x_pstate)
    x_premiseunit.pstate = x_pstate
    x_premiseunit.pnigh = x_pnigh
    x_premiseunit.popen = x_popen
    x_premiseunit.pdivisor = x_pdivisor
    x_premiseunit._task = x__task
    x_premiseunit._status = x__status

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "bud_concept_reason_premiseunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_fisc_label, x_owner_name, x_way, x_rcontext)

        # WHEN
        insert_job_budprem(cursor, x_objkeysholder, x_premiseunit)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_fisc_label),
            str(x_owner_name),
            str(x_way),
            str(x_rcontext),
            str(x_pstate),
            x_pnigh,
            x_popen,
            x_pdivisor,
            x__task,
            x__status,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_budmemb_CreatesTableRowsFor_budmemb_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_bud_calc_dimen_args("bud_acct_membership")
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

    x_fisc_label = 1
    x_owner_name = 2
    x_acct_name = 3
    x_group_title = 4
    x_credit_vote = 5.0
    x_debtit_vote = 6.0
    x__credor_pool = 7.0
    x__debtor_pool = 8.0
    x__fund_give = 9.0
    x__fund_take = 10.0
    x__fund_agenda_give = 11.0
    x__fund_agenda_take = 12.0
    x__fund_agenda_ratio_give = 13.0
    x__fund_agenda_ratio_take = 14.0
    x_membership = membership_shop(x_group_title)
    x_membership.acct_name = x_acct_name
    x_membership.credit_vote = x_credit_vote
    x_membership.debtit_vote = x_debtit_vote
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
        x_table_name = "bud_acct_membership_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_fisc_label, x_owner_name)

        # WHEN
        insert_job_budmemb(cursor, x_objkeysholder, x_membership)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_fisc_label),
            str(x_owner_name),
            str(x_acct_name),
            str(x_group_title),
            x_credit_vote,
            x_debtit_vote,
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


def test_insert_job_budacct_CreatesTableRowsFor_budacct_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_bud_calc_dimen_args("bud_acctunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_acct.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_fisc_label = 1
    x_owner_name = 2
    x_acct_name = 3
    x_credit_belief = 4
    x_debtit_belief = 5
    x__credor_pool = 6
    x__debtor_pool = 7
    x__fund_give = 8
    x__fund_take = 9
    x__fund_agenda_give = 10
    x__fund_agenda_take = 11
    x__fund_agenda_ratio_give = 12
    x__fund_agenda_ratio_take = 13
    x__inallocable_debtit_belief = 14
    x__irrational_debtit_belief = 15
    x_acct = acctunit_shop(x_acct_name)
    x_acct.acct_name = x_acct_name
    x_acct.credit_belief = x_credit_belief
    x_acct.debtit_belief = x_debtit_belief
    x_acct._credor_pool = x__credor_pool
    x_acct._debtor_pool = x__debtor_pool
    x_acct._fund_give = x__fund_give
    x_acct._fund_take = x__fund_take
    x_acct._fund_agenda_give = x__fund_agenda_give
    x_acct._fund_agenda_take = x__fund_agenda_take
    x_acct._fund_agenda_ratio_give = x__fund_agenda_ratio_give
    x_acct._fund_agenda_ratio_take = x__fund_agenda_ratio_take
    x_acct._inallocable_debtit_belief = x__inallocable_debtit_belief
    x_acct._irrational_debtit_belief = x__irrational_debtit_belief

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "bud_acctunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_fisc_label, x_owner_name)

        # WHEN
        insert_job_budacct(cursor, x_objkeysholder, x_acct)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_fisc_label),
            str(x_owner_name),
            str(x_acct_name),
            x_credit_belief,
            x_debtit_belief,
            x__credor_pool,
            x__debtor_pool,
            x__fund_give,
            x__fund_take,
            x__fund_agenda_give,
            x__fund_agenda_take,
            x__fund_agenda_ratio_give,
            x__fund_agenda_ratio_take,
            x__inallocable_debtit_belief,
            x__irrational_debtit_belief,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_budgrou_CreatesTableRowsFor_budgrou_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_bud_calc_dimen_args("bud_groupunit")
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

    x_fisc_label = 1
    x_owner_name = 2
    x_group_title = 3
    x_fund_coin = 4
    x_bridge = 5
    x__credor_pool = 6
    x__debtor_pool = 7
    x__fund_give = 8
    x__fund_take = 9
    x__fund_agenda_give = 10
    x__fund_agenda_take = 11
    x_group = groupunit_shop(x_group_title)
    x_group.group_title = x_group_title
    x_group.fund_coin = x_fund_coin
    x_group.bridge = x_bridge
    x_group._credor_pool = x__credor_pool
    x_group._debtor_pool = x__debtor_pool
    x_group._fund_give = x__fund_give
    x_group._fund_take = x__fund_take
    x_group._fund_agenda_give = x__fund_agenda_give
    x_group._fund_agenda_take = x__fund_agenda_take

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "bud_groupunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_fisc_label, x_owner_name)

        # WHEN
        insert_job_budgrou(cursor, x_objkeysholder, x_group)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_fisc_label),
            str(x_owner_name),
            str(x_group_title),
            x_fund_coin,
            str(x_bridge),
            x__credor_pool,
            x__debtor_pool,
            x__fund_give,
            x__fund_take,
            x__fund_agenda_give,
            x__fund_agenda_take,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_budawar_CreatesTableRowsFor_budawar_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_bud_calc_dimen_args("bud_concept_awardlink")
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

    x_fisc_label = 1
    x_owner_name = 2
    x_way = 3
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
        x_table_name = "bud_concept_awardlink_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_fisc_label, x_owner_name, x_way)

        # WHEN
        insert_job_budawar(cursor, x_objkeysholder, x_awardheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_fisc_label),
            str(x_owner_name),
            str(x_way),
            str(x_awardee_title),
            x_give_force,
            x_take_force,
            x__fund_give,
            x__fund_take,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_budfact_CreatesTableRowsFor_budfact_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_bud_calc_dimen_args("bud_concept_factunit")
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

    x_fisc_label = 1
    x_owner_name = 2
    x_way = 3
    x_rcontext = 4
    x_fstate = 5
    x_fopen = 6
    x_fnigh = 7
    x_factheir = factheir_shop()
    x_factheir.fcontext = x_rcontext
    x_factheir.fstate = x_fstate
    x_factheir.fopen = x_fopen
    x_factheir.fnigh = x_fnigh

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "bud_concept_factunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_fisc_label, x_owner_name, x_way)

        # WHEN
        insert_job_budfact(cursor, x_objkeysholder, x_factheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_fisc_label),
            str(x_owner_name),
            str(x_way),
            str(x_rcontext),
            str(x_fstate),
            x_fopen,
            x_fnigh,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_budheal_CreatesTableRowsFor_budheal_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_bud_calc_dimen_args("bud_concept_healerlink")
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

    x_fisc_label = 1
    x_owner_name = 2
    x_way = 3
    bob_str = "Bob"
    sue_str = "Sue"
    x_healerlink = healerlink_shop()
    x_healerlink.set_healer_name(bob_str)
    x_healerlink.set_healer_name(sue_str)

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "bud_concept_healerlink_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_fisc_label, x_owner_name, x_way)

        # WHEN
        insert_job_budheal(cursor, x_objkeysholder, x_healerlink)

        # THEN
        assert get_row_count(cursor, x_table_name) == 2
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_fisc_label),
            str(x_owner_name),
            str(x_way),
            bob_str,
        )
        expected_row2 = (
            str(x_fisc_label),
            str(x_owner_name),
            str(x_way),
            sue_str,
        )
        expected_data = [expected_row1, expected_row2]
        assert rows == expected_data


def test_insert_job_budlabo_CreatesTableRowsFor_budlabo_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_bud_calc_dimen_args("bud_concept_laborlink")
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

    x_fisc_label = 1
    x_owner_name = 2
    x_way = 3
    x__owner_name_labor = 5
    x_laborheir = laborheir_shop()
    x_laborheir._owner_name_labor = x__owner_name_labor
    bob_str = "Bob"
    sue_str = "Sue"
    x_laborheir._laborlinks = {bob_str, sue_str}

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "bud_concept_laborlink_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_fisc_label, x_owner_name, x_way)

        # WHEN
        insert_job_budlabo(cursor, x_objkeysholder, x_laborheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 2
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_fisc_label),
            str(x_owner_name),
            str(x_way),
            bob_str,
            x__owner_name_labor,
        )
        expected_row2 = (
            str(x_fisc_label),
            str(x_owner_name),
            str(x_way),
            sue_str,
            x__owner_name_labor,
        )
        expected_data = [expected_row1, expected_row2]
        assert rows == expected_data


def test_insert_job_obj_CreatesTableRows_Scenario0():
    # sourcery skip: extract-method
    # ESTABLISH
    a23_str = "accord23"
    sue_str = "Sue"
    bob_str = "Bob"
    run_str = ";run"
    sue_bud = budunit_shop(sue_str, a23_str)
    sue_bud.add_acctunit(sue_str)
    sue_bud.add_acctunit(bob_str)
    sue_bud.get_acct(bob_str).add_membership(run_str)
    casa_way = sue_bud.make_l1_way("casa")
    status_way = sue_bud.make_l1_way("status")
    clean_way = sue_bud.make_way(status_way, "clean")
    dirty_way = sue_bud.make_way(status_way, "dirty")
    sue_bud.add_concept(casa_way)
    sue_bud.add_concept(clean_way)
    sue_bud.add_concept(dirty_way)
    sue_bud.edit_concept_attr(
        casa_way, reason_rcontext=status_way, reason_premise=dirty_way
    )
    sue_bud.edit_concept_attr(casa_way, awardlink=awardlink_shop(run_str))
    sue_bud.edit_concept_attr(casa_way, healerlink=healerlink_shop({bob_str}))
    sue_bud.edit_concept_attr(casa_way, laborunit=laborunit_shop({sue_str}))
    sue_bud.add_fact(status_way, clean_way)

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        budmemb_job_table = "bud_acct_membership_job"
        budacct_job_table = "bud_acctunit_job"
        budgrou_job_table = "bud_groupunit_job"
        budawar_job_table = "bud_concept_awardlink_job"
        budfact_job_table = "bud_concept_factunit_job"
        budheal_job_table = "bud_concept_healerlink_job"
        budprem_job_table = "bud_concept_reason_premiseunit_job"
        budreas_job_table = "bud_concept_reasonunit_job"
        budlabo_job_table = "bud_concept_laborlink_job"
        budconc_job_table = "bud_conceptunit_job"
        budunit_job_table = "budunit_job"
        assert get_row_count(cursor, budunit_job_table) == 0
        assert get_row_count(cursor, budconc_job_table) == 0
        assert get_row_count(cursor, budacct_job_table) == 0
        assert get_row_count(cursor, budmemb_job_table) == 0
        assert get_row_count(cursor, budgrou_job_table) == 0
        assert get_row_count(cursor, budawar_job_table) == 0
        assert get_row_count(cursor, budfact_job_table) == 0
        assert get_row_count(cursor, budheal_job_table) == 0
        assert get_row_count(cursor, budreas_job_table) == 0
        assert get_row_count(cursor, budprem_job_table) == 0
        assert get_row_count(cursor, budlabo_job_table) == 0

        # WHEN
        insert_job_obj(cursor, sue_bud)

        # THEN
        assert get_row_count(cursor, budunit_job_table) == 1
        assert get_row_count(cursor, budconc_job_table) == 5
        assert get_row_count(cursor, budacct_job_table) == 2
        assert get_row_count(cursor, budmemb_job_table) == 3
        assert get_row_count(cursor, budgrou_job_table) == 3
        assert get_row_count(cursor, budawar_job_table) == 1
        assert get_row_count(cursor, budfact_job_table) == 1
        assert get_row_count(cursor, budheal_job_table) == 1
        assert get_row_count(cursor, budreas_job_table) == 1
        assert get_row_count(cursor, budprem_job_table) == 1
        assert get_row_count(cursor, budlabo_job_table) == 1
