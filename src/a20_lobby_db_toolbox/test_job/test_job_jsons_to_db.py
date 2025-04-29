from src.a00_data_toolbox.db_toolbox import get_row_count
from src.a03_group_logic.acct import acctunit_shop
from src.a03_group_logic.group import (
    awardlink_shop,
    awardheir_shop,
    groupunit_shop,
    membership_shop,
)
from src.a05_item_logic.healer import healerlink_shop
from src.a04_reason_logic.reason_team import teamheir_shop, teamunit_shop
from src.a04_reason_logic.reason_item import (
    reasonheir_shop,
    premiseunit_shop,
    factheir_shop,
)
from src.a05_item_logic.item import itemunit_shop
from src.a06_bud_logic.bud import budunit_shop

from src.a06_bud_logic.bud_tool import (
    bud_acct_membership_str,
    bud_acctunit_str,
    bud_groupunit_str,
    bud_item_awardlink_str,
    bud_item_factunit_str,
    bud_item_healerlink_str,
    bud_item_reason_premiseunit_str,
    bud_item_reasonunit_str,
    bud_item_teamlink_str,
    bud_itemunit_str,
    budunit_str,
)
from src.a12_hub_tools.hub_tool import save_job_file
from src.a20_lobby_db_toolbox.lobby_path import create_fisc_mstr_dir_path
from src.a20_lobby_db_toolbox.lobby_sqlstrs import create_job_tables
from src.a20_lobby_db_toolbox.lobby_tranformers import (
    etl_fisc_jobs_json_to_db,
    etl_fiscs_jobs_json_to_db,
    ObjKeysHolder,
    insert_job_budmemb,
    insert_job_budacct,
    insert_job_budgrou,
    insert_job_budawar,
    insert_job_budfact,
    insert_job_budheal,
    insert_job_budprem,
    insert_job_budreas,
    insert_job_budteam,
    insert_job_buditem,
    insert_job_budunit,
    insert_job_obj,
)
from src.a20_lobby_db_toolbox._utils.env_utils import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from sqlite3 import connect as sqlite3_connect


def test_ObjKeysHolder_Exists():
    # ESTABLISH / WHEN
    x_objkeyholder = ObjKeysHolder()

    # THEN
    assert not x_objkeyholder.world_id
    assert not x_objkeyholder.fisc_tag
    assert not x_objkeyholder.owner_name
    assert not x_objkeyholder.road
    assert not x_objkeyholder.base
    assert not x_objkeyholder.acct_name
    assert not x_objkeyholder.membership
    assert not x_objkeyholder.group_name
    assert not x_objkeyholder.fact_road


def test_insert_job_budunit_CreatesTableRowsFor_budunit_job():
    # sourcery skip: extract-method
    # ESTABLISH
    x_world_id = "music23"
    x_fisc_tag = "accord23"
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
    sue_bud = budunit_shop(owner_name=x_owner_name, fisc_tag=x_fisc_tag)
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
        objkeysholder = ObjKeysHolder(world_id=x_world_id)

        # WHEN
        insert_job_budunit(cursor, objkeysholder, sue_bud)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            x_world_id,
            x_fisc_tag,
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


def test_insert_job_buditem_CreatesTableRowsFor_buditem_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_bud_calc_dimen_args("bud_itemunit")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_item.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")
    # print("")

    x_world_id = 0
    x_fisc_tag = 1
    x_owner_name = 2
    x_parent_road = 3
    x_item_tag = 4
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
    x_item = itemunit_shop()
    x_item.fisc_tag = x_fisc_tag
    x_item.parent_road = x_parent_road
    x_item.item_tag = x_item_tag
    x_item.begin = x_begin
    x_item.close = x_close
    x_item.addin = x_addin
    x_item.numor = x_numor
    x_item.denom = x_denom
    x_item.morph = x_morph
    x_item.gogo_want = x_gogo_want
    x_item.stop_want = x_stop_want
    x_item.mass = x_mass
    x_item.pledge = x_pledge
    x_item.problem_bool = x_problem_bool
    x_item._active = x__active
    x_item._task = x__task
    x_item.fund_coin = x_fund_coin
    x_item._fund_onset = x__fund_onset
    x_item._fund_cease = x__fund_cease
    x_item._fund_ratio = x__fund_ratio
    x_item._gogo_calc = x__gogo_calc
    x_item._stop_calc = x__stop_calc
    x_item._level = x__level
    x_item._range_evaluated = x__range_evaluated
    x_item._descendant_pledge_count = x__descendant_pledge_count
    x_item._healerlink_ratio = x__healerlink_ratio
    x_item._all_acct_cred = x__all_acct_cred
    x_item._all_acct_debt = x__all_acct_debt
    x_item.begin = x_begin
    x_item.close = x_close
    x_item.addin = x_addin
    x_item.numor = x_numor
    x_item.denom = x_denom
    x_item.morph = x_morph
    x_item.gogo_want = x_gogo_want
    x_item.stop_want = x_stop_want
    x_item.mass = x_mass
    x_item.pledge = x_pledge
    x_item.problem_bool = x_problem_bool
    x_item._active = x__active
    x_item._task = x__task
    x_item.fund_coin = x_fund_coin
    x_item._fund_onset = x__fund_onset
    x_item._fund_cease = x__fund_cease
    x_item._fund_ratio = x__fund_ratio
    x_item._gogo_calc = x__gogo_calc
    x_item._stop_calc = x__stop_calc
    x_item._level = x__level
    x_item._range_evaluated = x__range_evaluated
    x_item._descendant_pledge_count = x__descendant_pledge_count
    x_item._healerlink_ratio = x__healerlink_ratio
    x_item._all_acct_cred = x__all_acct_cred
    x_item._all_acct_debt = x__all_acct_debt

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "bud_itemunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_world_id, x_fisc_tag, x_owner_name)

        # WHEN
        insert_job_buditem(cursor, x_objkeysholder, x_item)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_world_id),
            str(x_fisc_tag),
            str(x_owner_name),
            str(x_parent_road),
            str(x_item_tag),
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
    # x_args = get_bud_calc_dimen_args("bud_item_reasonunit")
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

    x_world_id = 0
    x_fisc_tag = 1
    x_owner_name = 2
    x_road = 3
    x_base = 4
    x_base_item_active_requisite = 5
    x__task = 6
    x__status = 7
    x__base_item_active_value = 8
    x_reasonheir = reasonheir_shop(base=x_base)
    x_reasonheir.base = x_base
    x_reasonheir.base_item_active_requisite = x_base_item_active_requisite
    x_reasonheir._task = x__task
    x_reasonheir._status = x__status
    x_reasonheir._base_item_active_value = x__base_item_active_value

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "bud_item_reasonunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_world_id, x_fisc_tag, x_owner_name, x_road)

        # WHEN
        insert_job_budreas(cursor, x_objkeysholder, x_reasonheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_world_id),
            str(x_fisc_tag),
            str(x_owner_name),
            str(x_road),
            str(x_base),
            x_base_item_active_requisite,
            x__task,
            x__status,
            x__base_item_active_value,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_budprem_CreatesTableRowsFor_budprem_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_bud_calc_dimen_args("bud_item_reason_premiseunit")
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

    x_world_id = 0
    x_fisc_tag = 1
    x_owner_name = 2
    x_road = 3
    x_base = 4
    x_need = 5
    x_nigh = 6.0
    x_open = 7.0
    x_divisor = 8
    x__task = 9
    x__status = 10
    x_premiseunit = premiseunit_shop(need=x_need)
    x_premiseunit.need = x_need
    x_premiseunit.nigh = x_nigh
    x_premiseunit.open = x_open
    x_premiseunit.divisor = x_divisor
    x_premiseunit._task = x__task
    x_premiseunit._status = x__status

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "bud_item_reason_premiseunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(
            x_world_id, x_fisc_tag, x_owner_name, x_road, x_base
        )

        # WHEN
        insert_job_budprem(cursor, x_objkeysholder, x_premiseunit)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_world_id),
            str(x_fisc_tag),
            str(x_owner_name),
            str(x_road),
            str(x_base),
            str(x_need),
            x_nigh,
            x_open,
            x_divisor,
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

    x_world_id = 0
    x_fisc_tag = 1
    x_owner_name = 2
    x_acct_name = 3
    x_group_label = 4
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
    x_membership = membership_shop(x_group_label)
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
        x_objkeysholder = ObjKeysHolder(x_world_id, x_fisc_tag, x_owner_name)

        # WHEN
        insert_job_budmemb(cursor, x_objkeysholder, x_membership)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_world_id),
            str(x_fisc_tag),
            str(x_owner_name),
            str(x_acct_name),
            str(x_group_label),
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

    x_world_id = 0
    x_fisc_tag = 1
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
        x_objkeysholder = ObjKeysHolder(x_world_id, x_fisc_tag, x_owner_name)

        # WHEN
        insert_job_budacct(cursor, x_objkeysholder, x_acct)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_world_id),
            str(x_fisc_tag),
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

    x_world_id = 0
    x_fisc_tag = 1
    x_owner_name = 2
    x_group_label = 3
    x_fund_coin = 4
    x_bridge = 5
    x__credor_pool = 6
    x__debtor_pool = 7
    x__fund_give = 8
    x__fund_take = 9
    x__fund_agenda_give = 10
    x__fund_agenda_take = 11
    x_group = groupunit_shop(x_group_label)
    x_group.group_label = x_group_label
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
        x_objkeysholder = ObjKeysHolder(x_world_id, x_fisc_tag, x_owner_name)

        # WHEN
        insert_job_budgrou(cursor, x_objkeysholder, x_group)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_world_id),
            str(x_fisc_tag),
            str(x_owner_name),
            str(x_group_label),
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
    # x_args = get_bud_calc_dimen_args("bud_item_awardlink")
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

    x_world_id = 0
    x_fisc_tag = 1
    x_owner_name = 2
    x_road = 3
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
        x_table_name = "bud_item_awardlink_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_world_id, x_fisc_tag, x_owner_name, x_road)

        # WHEN
        insert_job_budawar(cursor, x_objkeysholder, x_awardheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_world_id),
            str(x_fisc_tag),
            str(x_owner_name),
            str(x_road),
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
    # x_args = get_bud_calc_dimen_args("bud_item_factunit")
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

    x_world_id = 0
    x_fisc_tag = 1
    x_owner_name = 2
    x_road = 3
    x_base = 4
    x_pick = 5
    x_fopen = 6
    x_fnigh = 7
    x_factheir = factheir_shop()
    x_factheir.base = x_base
    x_factheir.pick = x_pick
    x_factheir.fopen = x_fopen
    x_factheir.fnigh = x_fnigh

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "bud_item_factunit_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_world_id, x_fisc_tag, x_owner_name, x_road)

        # WHEN
        insert_job_budfact(cursor, x_objkeysholder, x_factheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 1
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_world_id),
            str(x_fisc_tag),
            str(x_owner_name),
            str(x_road),
            str(x_base),
            str(x_pick),
            x_fopen,
            x_fnigh,
        )
        expected_data = [expected_row1]
        assert rows == expected_data


def test_insert_job_budheal_CreatesTableRowsFor_budheal_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_bud_calc_dimen_args("bud_item_healerlink")
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

    x_world_id = 0
    x_fisc_tag = 1
    x_owner_name = 2
    x_road = 3
    bob_str = "Bob"
    sue_str = "Sue"
    x_healerlink = healerlink_shop()
    x_healerlink.set_healer_name(bob_str)
    x_healerlink.set_healer_name(sue_str)

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "bud_item_healerlink_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_world_id, x_fisc_tag, x_owner_name, x_road)

        # WHEN
        insert_job_budheal(cursor, x_objkeysholder, x_healerlink)

        # THEN
        assert get_row_count(cursor, x_table_name) == 2
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_world_id),
            str(x_fisc_tag),
            str(x_owner_name),
            str(x_road),
            bob_str,
        )
        expected_row2 = (
            str(x_world_id),
            str(x_fisc_tag),
            str(x_owner_name),
            str(x_road),
            sue_str,
        )
        expected_data = [expected_row1, expected_row2]
        assert rows == expected_data


def test_insert_job_budteam_CreatesTableRowsFor_budteam_job():
    # sourcery skip: extract-method
    # ESTABLISH
    # x_args = get_bud_calc_dimen_args("bud_item_teamlink")
    # x_count = 0
    # for x_arg in get_default_sorted_list(x_args):
    #     x_count += 1
    #     print(f"    x_{x_arg} = {x_count}")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""    x_teamheir.{x_arg} = x_{x_arg}""")
    # print("")
    # for x_arg in get_default_sorted_list(x_args):
    #     print(f"""            x_{x_arg},""")

    x_world_id = 0
    x_fisc_tag = 1
    x_owner_name = 2
    x_road = 3
    x__owner_name_team = 5
    x_teamheir = teamheir_shop()
    x_teamheir._owner_name_team = x__owner_name_team
    bob_str = "Bob"
    sue_str = "Sue"
    x_teamheir._teamlinks = {bob_str, sue_str}

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        x_table_name = "bud_item_teamlink_job"
        assert get_row_count(cursor, x_table_name) == 0
        x_objkeysholder = ObjKeysHolder(x_world_id, x_fisc_tag, x_owner_name, x_road)

        # WHEN
        insert_job_budteam(cursor, x_objkeysholder, x_teamheir)

        # THEN
        assert get_row_count(cursor, x_table_name) == 2
        select_sqlstr = f"SELECT * FROM {x_table_name};"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        expected_row1 = (
            str(x_world_id),
            str(x_fisc_tag),
            str(x_owner_name),
            str(x_road),
            bob_str,
            x__owner_name_team,
        )
        expected_row2 = (
            str(x_world_id),
            str(x_fisc_tag),
            str(x_owner_name),
            str(x_road),
            sue_str,
            x__owner_name_team,
        )
        expected_data = [expected_row1, expected_row2]
        assert rows == expected_data


def test_insert_job_obj_CreatesTableRows_Scenario0():
    # sourcery skip: extract-method
    # ESTABLISH
    x_world_id = "music23"
    a23_str = "accord23"
    sue_str = "Sue"
    bob_str = "Bob"
    run_str = ";run"
    sue_bud = budunit_shop(sue_str, a23_str)
    sue_bud.add_acctunit(sue_str)
    sue_bud.add_acctunit(bob_str)
    sue_bud.get_acct(bob_str).add_membership(run_str)
    casa_road = sue_bud.make_l1_road("casa")
    status_road = sue_bud.make_l1_road("status")
    clean_road = sue_bud.make_road(status_road, "clean")
    dirty_road = sue_bud.make_road(status_road, "dirty")
    sue_bud.add_item(casa_road)
    sue_bud.add_item(clean_road)
    sue_bud.add_item(dirty_road)
    sue_bud.edit_item_attr(
        road=casa_road, reason_base=status_road, reason_premise=dirty_road
    )
    sue_bud.edit_item_attr(road=casa_road, awardlink=awardlink_shop(run_str))
    sue_bud.edit_item_attr(road=casa_road, healerlink=healerlink_shop({bob_str}))
    sue_bud.edit_item_attr(road=casa_road, teamunit=teamunit_shop({sue_str}))
    sue_bud.add_fact(status_road, clean_road)

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        budmemb_job_table = "bud_acct_membership_job"
        budacct_job_table = "bud_acctunit_job"
        budgrou_job_table = "bud_groupunit_job"
        budawar_job_table = "bud_item_awardlink_job"
        budfact_job_table = "bud_item_factunit_job"
        budheal_job_table = "bud_item_healerlink_job"
        budprem_job_table = "bud_item_reason_premiseunit_job"
        budreas_job_table = "bud_item_reasonunit_job"
        budteam_job_table = "bud_item_teamlink_job"
        buditem_job_table = "bud_itemunit_job"
        budunit_job_table = "budunit_job"
        assert get_row_count(cursor, budunit_job_table) == 0
        assert get_row_count(cursor, buditem_job_table) == 0
        assert get_row_count(cursor, budacct_job_table) == 0
        assert get_row_count(cursor, budmemb_job_table) == 0
        assert get_row_count(cursor, budgrou_job_table) == 0
        assert get_row_count(cursor, budawar_job_table) == 0
        assert get_row_count(cursor, budfact_job_table) == 0
        assert get_row_count(cursor, budheal_job_table) == 0
        assert get_row_count(cursor, budreas_job_table) == 0
        assert get_row_count(cursor, budprem_job_table) == 0
        assert get_row_count(cursor, budteam_job_table) == 0

        # WHEN
        insert_job_obj(cursor, x_world_id, sue_bud)

        # THEN
        assert get_row_count(cursor, budunit_job_table) == 1
        assert get_row_count(cursor, buditem_job_table) == 5
        assert get_row_count(cursor, budacct_job_table) == 2
        assert get_row_count(cursor, budmemb_job_table) == 3
        assert get_row_count(cursor, budgrou_job_table) == 3
        assert get_row_count(cursor, budawar_job_table) == 1
        assert get_row_count(cursor, budfact_job_table) == 1
        assert get_row_count(cursor, budheal_job_table) == 1
        assert get_row_count(cursor, budreas_job_table) == 1
        assert get_row_count(cursor, budprem_job_table) == 1
        assert get_row_count(cursor, budteam_job_table) == 1


def test_etl_fisc_jobs_json_to_db_SetsDB_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    lobby_mstr_dir = get_module_temp_dir()
    c23_str = "Chat23"
    m23_str = "music23"
    m23_fisc_mstr_dir = create_fisc_mstr_dir_path(lobby_mstr_dir, c23_str, m23_str)
    a23_str = "accord23"
    sue_str = "Sue"
    bob_str = "Bob"
    run_str = ";run"
    sue_bud = budunit_shop(sue_str, a23_str)
    sue_bud.add_acctunit(sue_str)
    sue_bud.add_acctunit(bob_str)
    sue_bud.get_acct(bob_str).add_membership(run_str)
    casa_road = sue_bud.make_l1_road("casa")
    status_road = sue_bud.make_l1_road("status")
    clean_road = sue_bud.make_road(status_road, "clean")
    dirty_road = sue_bud.make_road(status_road, "dirty")
    sue_bud.add_item(casa_road)
    sue_bud.add_item(clean_road)
    sue_bud.add_item(dirty_road)
    sue_bud.edit_item_attr(
        road=casa_road, reason_base=status_road, reason_premise=dirty_road
    )
    sue_bud.edit_item_attr(road=casa_road, awardlink=awardlink_shop(run_str))
    sue_bud.edit_item_attr(road=casa_road, healerlink=healerlink_shop({bob_str}))
    sue_bud.edit_item_attr(road=casa_road, teamunit=teamunit_shop({sue_str}))
    sue_bud.add_fact(status_road, clean_road)
    print(f"{sue_bud.get_item_obj(casa_road).teamunit=}")
    print(f"{sue_bud.get_item_obj(casa_road).get_dict()=}")
    save_job_file(m23_fisc_mstr_dir, sue_bud)

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        budmemb_job_table = f"{bud_acct_membership_str()}_job"
        budacct_job_table = f"{bud_acctunit_str()}_job"
        budgrou_job_table = f"{bud_groupunit_str()}_job"
        budawar_job_table = f"{bud_item_awardlink_str()}_job"
        budfact_job_table = f"{bud_item_factunit_str()}_job"
        budheal_job_table = f"{bud_item_healerlink_str()}_job"
        budprem_job_table = f"{bud_item_reason_premiseunit_str()}_job"
        budreas_job_table = f"{bud_item_reasonunit_str()}_job"
        budteam_job_table = f"{bud_item_teamlink_str()}_job"
        buditem_job_table = f"{bud_itemunit_str()}_job"
        budunit_job_table = f"{budunit_str()}_job"
        assert get_row_count(cursor, budunit_job_table) == 0
        assert get_row_count(cursor, buditem_job_table) == 0
        assert get_row_count(cursor, budacct_job_table) == 0
        assert get_row_count(cursor, budmemb_job_table) == 0
        assert get_row_count(cursor, budgrou_job_table) == 0
        assert get_row_count(cursor, budawar_job_table) == 0
        assert get_row_count(cursor, budfact_job_table) == 0
        assert get_row_count(cursor, budheal_job_table) == 0
        assert get_row_count(cursor, budreas_job_table) == 0
        assert get_row_count(cursor, budprem_job_table) == 0
        assert get_row_count(cursor, budteam_job_table) == 0

        # WHEN
        etl_fisc_jobs_json_to_db(cursor, m23_str, m23_fisc_mstr_dir)

        # THEN
        assert get_row_count(cursor, budunit_job_table) == 1
        assert get_row_count(cursor, buditem_job_table) == 5
        assert get_row_count(cursor, budacct_job_table) == 2
        assert get_row_count(cursor, budmemb_job_table) == 3
        assert get_row_count(cursor, budgrou_job_table) == 3
        assert get_row_count(cursor, budawar_job_table) == 1
        assert get_row_count(cursor, budfact_job_table) == 1
        assert get_row_count(cursor, budheal_job_table) == 1
        assert get_row_count(cursor, budreas_job_table) == 1
        assert get_row_count(cursor, budprem_job_table) == 1
        assert get_row_count(cursor, budteam_job_table) == 1


def test_etl_fiscs_jobs_json_to_db_SetsDB_Scenario0_TwoBudsInDifferentFiscUnits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    lobby_mstr_dir = get_module_temp_dir()
    c77_str = "Chat77"
    a23_str = "accord23"
    sue_str = "Sue"
    a23_sue_bud = budunit_shop(sue_str, a23_str)
    a23_sue_bud.add_acctunit(sue_str)
    a23_sue_bud.add_item(a23_sue_bud.make_l1_road("casa"))

    a99_str = "accord99"
    bob_str = "Bob"
    a99_sue_bud = budunit_shop(sue_str, a99_str)
    a99_sue_bud.add_acctunit(sue_str)
    a99_sue_bud.add_acctunit(bob_str)
    a99_sue_bud.add_item(a99_sue_bud.make_l1_road("casa"))
    a99_sue_bud.add_item(a99_sue_bud.make_l1_road("sports"))

    w34_str = "world34"
    w99_str = "world99"
    w34_fisc_mstr_dir = create_fisc_mstr_dir_path(lobby_mstr_dir, c77_str, w34_str)
    w99_fisc_mstr_dir = create_fisc_mstr_dir_path(lobby_mstr_dir, c77_str, w99_str)
    print(f"{w34_fisc_mstr_dir=}")
    print(f"{w99_fisc_mstr_dir=}")
    save_job_file(w34_fisc_mstr_dir, a23_sue_bud)
    save_job_file(w99_fisc_mstr_dir, a99_sue_bud)

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_job_tables(cursor)
        budacct_job_table = f"{bud_acctunit_str()}_job"
        buditem_job_table = f"{bud_itemunit_str()}_job"
        budunit_job_table = f"{budunit_str()}_job"
        assert get_row_count(cursor, budunit_job_table) == 0
        assert get_row_count(cursor, buditem_job_table) == 0
        assert get_row_count(cursor, budacct_job_table) == 0

        # WHEN
        worlds = [w34_str, w99_str]
        etl_fiscs_jobs_json_to_db(cursor, lobby_mstr_dir, c77_str, worlds)

        # THEN
        assert get_row_count(cursor, budunit_job_table) == 2
        assert get_row_count(cursor, buditem_job_table) == 5
        assert get_row_count(cursor, budacct_job_table) == 3
