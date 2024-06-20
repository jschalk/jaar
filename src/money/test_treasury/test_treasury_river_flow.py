from src.agenda.agenda import agendaunit_shop
from src.money.money import moneyunit_shop
from src.money.examples.econ_env import env_dir_setup_cleanup, get_texas_userhub
from src._instrument.sqlite import get_single_result, get_row_count_sqlstr
from src.money.treasury_sqlstr import (
    get_othertreasuryunit_dict,
    get_river_block_dict,
)


def get_agenda_otherunit_table_treasurying_attr_set_count_sqlstr():
    # def get_agenda_otherunit_table_treasurying_attr_set_count_sqlstr(cash_master:):
    #     return f"""
    # SELECT COUNT(*)
    # FROM agenda_otherunit
    # WHERE _treasury_due_paid IS NOT NULL
    #     AND owner_id = {cash_master}
    # """
    return """
SELECT COUNT(*) 
FROM agenda_otherunit
WHERE _treasury_due_paid IS NOT NULL
;
"""


def test_MoneyUnit_set_cred_flow_for_agenda_CorrectlyPopulatesothertreasuryunitTable01(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())

    bob_text = "Bob"
    tom_text = "Tom"
    sal_text = "Sal"

    sal_agentunit = agendaunit_shop(_owner_id=sal_text)
    sal_agentunit.add_otherunit(other_id=bob_text, credor_weight=1)
    sal_agentunit.add_otherunit(other_id=tom_text, credor_weight=3)
    x_money.userhub.save_job_agenda(sal_agentunit)

    bob_agentunit = agendaunit_shop(_owner_id=bob_text)
    bob_agentunit.add_otherunit(other_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_agenda(bob_agentunit)

    tom_agentunit = agendaunit_shop(_owner_id=tom_text)
    tom_agentunit.add_otherunit(other_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_agenda(tom_agentunit)

    x_money.refresh_treasury_job_agendas_data()
    otherunit_count_sqlstr = get_row_count_sqlstr("agenda_otherunit")
    assert get_single_result(x_money.get_treasury_conn(), otherunit_count_sqlstr) == 4

    othertreasuryunit_count_sqlstr = (
        get_agenda_otherunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_money.get_treasury_conn(), othertreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_money.set_cred_flow_for_agenda(owner_id=sal_text)

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 4
    with x_money.get_treasury_conn() as treasury_conn:
        river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)

    block_0 = river_blocks.get(0)
    block_1 = river_blocks.get(1)
    assert block_1.src_owner_id == sal_text and block_1.dst_owner_id == tom_text
    assert block_1.river_tree_level == 1
    assert block_1.cash_start == 0.25
    assert block_1.cash_close == 1
    assert block_1.parent_block_num is None
    block_2 = river_blocks.get(2)
    block_3 = river_blocks.get(3)
    assert block_3.src_owner_id == tom_text and block_3.dst_owner_id == sal_text
    assert block_3.river_tree_level == 2
    assert block_3.parent_block_num == 1

    assert (
        get_single_result(x_money.get_treasury_conn(), othertreasuryunit_count_sqlstr)
        == 2
    )

    with x_money.get_treasury_conn() as treasury_conn:
        othertreasuryunits = get_othertreasuryunit_dict(treasury_conn, sal_text)
    assert len(othertreasuryunits) == 2
    river_sal_due_bob = othertreasuryunits.get(bob_text)
    river_sal_due_tom = othertreasuryunits.get(tom_text)

    print(f"{river_sal_due_bob=}")
    print(f"{river_sal_due_tom=}")

    assert river_sal_due_bob.due_total == 0.25
    assert river_sal_due_tom.due_total == 0.75


def test_MoneyUnit_set_cred_flow_for_agenda_CorrectlyPopulatesothertreasuryunitTable03(
    env_dir_setup_cleanup,
):
    # GIVEN 4 agendas, 85% of river blocks to sal
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_otherunit(other_id=bob_text, credor_weight=2)
    sal_agenda.add_otherunit(other_id=tom_text, credor_weight=7)
    sal_agenda.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_otherunit(other_id=sal_text, credor_weight=3)
    bob_agenda.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_otherunit(other_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    x_money.userhub.save_job_agenda(ava_agenda)
    x_money.refresh_treasury_job_agendas_data()

    otherunit_count_sqlstr = get_row_count_sqlstr("agenda_otherunit")
    assert get_single_result(x_money.get_treasury_conn(), otherunit_count_sqlstr) == 6

    othertreasuryunit_count_sqlstr = (
        get_agenda_otherunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_money.get_treasury_conn(), othertreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_money.set_cred_flow_for_agenda(owner_id=sal_text)

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 6
    with x_money.get_treasury_conn() as treasury_conn:
        river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_money.get_treasury_conn(), othertreasuryunit_count_sqlstr)
        == 2
    )

    with x_money.get_treasury_conn() as treasury_conn:
        othertreasuryunits = get_othertreasuryunit_dict(treasury_conn, sal_text)
    assert len(othertreasuryunits) == 2
    assert othertreasuryunits.get(bob_text) != None
    assert othertreasuryunits.get(tom_text) != None
    assert othertreasuryunits.get(ava_text) is None

    river_sal_due_bob = othertreasuryunits.get(bob_text)
    print(f"{river_sal_due_bob=}")
    river_sal_due_tom = othertreasuryunits.get(tom_text)
    print(f"{river_sal_due_tom=}")

    assert round(river_sal_due_bob.due_total, 15) == 0.15
    assert river_sal_due_tom.due_total == 0.7


def test_MoneyUnit_set_cred_flow_for_agenda_CorrectlyPopulatesothertreasuryunitTable04(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_otherunit(other_id=bob_text, credor_weight=2)
    sal_agenda.add_otherunit(other_id=tom_text, credor_weight=7)
    sal_agenda.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_otherunit(other_id=sal_text, credor_weight=3)
    bob_agenda.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_otherunit(other_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_otherunit(other_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_otherunit(other_id=ava_text, credor_weight=2)
    x_money.userhub.save_job_agenda(elu_agenda)

    x_money.refresh_treasury_job_agendas_data()

    otherunit_count_sqlstr = get_row_count_sqlstr("agenda_otherunit")
    assert get_single_result(x_money.get_treasury_conn(), otherunit_count_sqlstr) == 8

    othertreasuryunit_count_sqlstr = (
        get_agenda_otherunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_money.get_treasury_conn(), othertreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_money.set_cred_flow_for_agenda(owner_id=sal_text)

    # THEN
    assert (
        get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 40
    )
    # with x_money.get_treasury_conn() as treasury_conn:
    #     river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_money.get_treasury_conn(), othertreasuryunit_count_sqlstr)
        == 2
    )

    with x_money.get_treasury_conn() as treasury_conn:
        othertreasuryunits = get_othertreasuryunit_dict(treasury_conn, sal_text)
    assert len(othertreasuryunits) == 2
    assert othertreasuryunits.get(bob_text) != None
    assert othertreasuryunits.get(tom_text) != None
    assert othertreasuryunits.get(ava_text) is None

    river_sal_due_bob = othertreasuryunits.get(bob_text)
    print(f"{river_sal_due_bob=}")
    river_sal_due_tom = othertreasuryunits.get(tom_text)
    print(f"{river_sal_due_tom=}")

    assert round(river_sal_due_bob.due_total, 15) == 0.15
    assert river_sal_due_tom.due_total == 0.7


def test_MoneyUnit_set_cred_flow_for_agenda_CorrectlyPopulatesothertreasuryunitTable05_v1(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_otherunit(other_id=bob_text, credor_weight=2)
    sal_agenda.add_otherunit(other_id=tom_text, credor_weight=7)
    sal_agenda.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_otherunit(other_id=sal_text, credor_weight=3)
    bob_agenda.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_otherunit(other_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_otherunit(other_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_otherunit(other_id=ava_text, credor_weight=19)
    elu_agenda.add_otherunit(other_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_agenda(elu_agenda)

    x_money.refresh_treasury_job_agendas_data()

    otherunit_count_sqlstr = get_row_count_sqlstr("agenda_otherunit")
    assert get_single_result(x_money.get_treasury_conn(), otherunit_count_sqlstr) == 9

    othertreasuryunit_count_sqlstr = (
        get_agenda_otherunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_money.get_treasury_conn(), othertreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_money.set_cred_flow_for_agenda(owner_id=sal_text)

    # THEN
    assert (
        get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 40
    )
    # with x_money.get_treasury_conn() as treasury_conn:
    #     river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_money.get_treasury_conn(), othertreasuryunit_count_sqlstr)
        == 2
    )

    with x_money.get_treasury_conn() as treasury_conn:
        othertreasuryunits = get_othertreasuryunit_dict(treasury_conn, sal_text)
    assert len(othertreasuryunits) == 2
    assert othertreasuryunits.get(bob_text) != None
    assert othertreasuryunits.get(tom_text) != None
    assert othertreasuryunits.get(elu_text) is None
    assert othertreasuryunits.get(ava_text) is None

    river_sal_due_bob = othertreasuryunits.get(bob_text)
    river_sal_due_tom = othertreasuryunits.get(tom_text)
    river_sal_due_elu = othertreasuryunits.get(elu_text)
    print(f"{river_sal_due_bob=}")
    print(f"{river_sal_due_tom=}")
    print(f"{river_sal_due_elu=}")

    assert round(river_sal_due_bob.due_total, 15) == 0.15
    assert round(river_sal_due_tom.due_total, 15) == 0.7


def test_MoneyUnit_set_cred_flow_for_agenda_CorrectlyUsesMaxblocksCount(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_otherunit(other_id=bob_text, credor_weight=2)
    sal_agenda.add_otherunit(other_id=tom_text, credor_weight=7)
    sal_agenda.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_otherunit(other_id=sal_text, credor_weight=3)
    bob_agenda.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_otherunit(other_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_otherunit(other_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_otherunit(other_id=ava_text, credor_weight=19)
    elu_agenda.add_otherunit(other_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_agenda(elu_agenda)

    x_money.refresh_treasury_job_agendas_data()

    otherunit_count_sqlstr = get_row_count_sqlstr("agenda_otherunit")
    assert get_single_result(x_money.get_treasury_conn(), otherunit_count_sqlstr) == 9

    othertreasuryunit_count_sqlstr = (
        get_agenda_otherunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_money.get_treasury_conn(), othertreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    mbc = 13
    x_money.set_cred_flow_for_agenda(owner_id=sal_text, max_blocks_count=mbc)

    # THEN
    # with x_money.get_treasury_conn() as treasury_conn:
    #     river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == mbc
    )


def test_MoneyUnit_set_cred_flow_for_agenda_CorrectlyPopulatesothertreasuryunitTable05(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_otherunit(other_id=bob_text, credor_weight=2)
    sal_agenda.add_otherunit(other_id=tom_text, credor_weight=7)
    sal_agenda.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_otherunit(other_id=sal_text, credor_weight=3)
    bob_agenda.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_otherunit(other_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_otherunit(other_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_otherunit(other_id=ava_text, credor_weight=19)
    elu_agenda.add_otherunit(other_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_agenda(elu_agenda)

    x_money.refresh_treasury_job_agendas_data()

    otherunit_count_sqlstr = get_row_count_sqlstr("agenda_otherunit")
    assert get_single_result(x_money.get_treasury_conn(), otherunit_count_sqlstr) == 9

    othertreasuryunit_count_sqlstr = (
        get_agenda_otherunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_money.get_treasury_conn(), othertreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_money.set_cred_flow_for_agenda(owner_id=sal_text)

    # THEN
    assert (
        get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 40
    )
    with x_money.get_treasury_conn() as treasury_conn:
        river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_money.get_treasury_conn(), othertreasuryunit_count_sqlstr)
        == 2
    )

    with x_money.get_treasury_conn() as treasury_conn:
        othertreasuryunits = get_othertreasuryunit_dict(treasury_conn, sal_text)
    othertreasuryunits = x_money.get_othertreasuryunits(sal_text)
    assert len(othertreasuryunits) == 2
    assert othertreasuryunits.get(bob_text) != None
    assert othertreasuryunits.get(tom_text) != None
    assert othertreasuryunits.get(elu_text) is None
    assert othertreasuryunits.get(ava_text) is None

    river_sal_due_bob = othertreasuryunits.get(bob_text)
    river_sal_due_tom = othertreasuryunits.get(tom_text)
    river_sal_due_elu = othertreasuryunits.get(elu_text)
    print(f"{river_sal_due_bob=}")
    print(f"{river_sal_due_tom=}")
    print(f"{river_sal_due_elu=}")

    assert round(river_sal_due_bob.due_total, 15) == 0.15
    assert round(river_sal_due_tom.due_total, 15) == 0.7


def test_MoneyUnit_set_cred_flow_for_agenda_CorrectlyBuildsASingle_ContinuousRange(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_otherunit(other_id=bob_text, credor_weight=2)
    sal_agenda.add_otherunit(other_id=tom_text, credor_weight=7)
    sal_agenda.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_otherunit(other_id=sal_text, credor_weight=3)
    bob_agenda.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_otherunit(other_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_otherunit(other_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_otherunit(other_id=ava_text, credor_weight=19)
    elu_agenda.add_otherunit(other_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_agenda(elu_agenda)

    x_money.refresh_treasury_job_agendas_data()

    # WHEN
    x_money.set_cred_flow_for_agenda(owner_id=sal_text, max_blocks_count=100)

    # THEN
    count_range_fails_sql = """
    SELECT COUNT(*)
    FROM (
        SELECT 
            rt1.cash_start x_row_start
        , lag(cash_close) OVER (ORDER BY cash_start, cash_close) AS prev_close
        , lag(cash_close) OVER (ORDER BY cash_start, cash_close) - rt1.cash_start prev_diff
        , rt1.block_num or_block_num
        , lag(block_num) OVER (ORDER BY cash_start, cash_close) AS prev_block_num
        , rt1.parent_block_num or_parent_block_num
        , lag(parent_block_num) OVER (ORDER BY cash_start, cash_close) AS prev_parent_block_num
        , river_tree_level
        , lag(river_tree_level) OVER (ORDER BY cash_start, cash_close) AS prev_parent_river_tree_level
        FROM river_block rt1
        --  WHERE dst_owner_id = 'sal' and cash_master = dst_owner_id
        ORDER BY rt1.cash_start, rt1.cash_close
    ) x
    WHERE x.prev_diff <> 0
        AND ABS(x.prev_diff) < 0.0000000000000001
    ;
    
    """
    with x_money.get_treasury_conn() as treasury_conn:
        assert get_single_result(treasury_conn, count_range_fails_sql) == 0


def test_MoneyUnit_set_cred_flow_for_agenda_CorrectlyUpatesAgendaOtherUnits(
    env_dir_setup_cleanup,
):
    """GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal"""
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda_src = agendaunit_shop(_owner_id=sal_text)
    sal_agenda_src.add_otherunit(other_id=bob_text, credor_weight=2, debtor_weight=2)
    sal_agenda_src.add_otherunit(other_id=tom_text, credor_weight=2, debtor_weight=1)
    sal_agenda_src.add_otherunit(other_id=ava_text, credor_weight=2, debtor_weight=2)
    x_money.userhub.save_job_agenda(sal_agenda_src)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_otherunit(other_id=sal_text, credor_weight=3)
    bob_agenda.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_otherunit(other_id=sal_text)
    x_money.userhub.save_job_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_otherunit(other_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_otherunit(other_id=ava_text, credor_weight=8)
    elu_agenda.add_otherunit(other_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_agenda(elu_agenda)

    x_money.refresh_treasury_job_agendas_data()
    sal_agenda_before = x_money.userhub.get_job_agenda(owner_id=sal_text)

    x_money.set_cred_flow_for_agenda(owner_id=sal_text, max_blocks_count=100)
    assert len(sal_agenda_before._others) == 3
    print(f"{len(sal_agenda_before._others)=}")
    bob_other = sal_agenda_before._others.get(bob_text)
    tom_other = sal_agenda_before._others.get(tom_text)
    ava_other = sal_agenda_before._others.get(ava_text)
    assert bob_other._treasury_due_paid is None
    assert tom_other._treasury_due_paid is None
    assert ava_other._treasury_due_paid is None
    assert bob_other._treasury_due_diff is None
    assert tom_other._treasury_due_diff is None
    assert ava_other._treasury_due_diff is None
    assert bob_other._treasury_voice_rank is None
    assert tom_other._treasury_voice_rank is None
    assert ava_other._treasury_voice_rank is None
    assert bob_other._treasury_voice_hx_lowest_rank is None
    assert tom_other._treasury_voice_hx_lowest_rank is None
    assert ava_other._treasury_voice_hx_lowest_rank is None

    # WHEN
    x_money.set_cred_flow_for_agenda(owner_id=sal_text)

    # THEN
    sal_othertreasuryunits = x_money.get_othertreasuryunits(owner_id=sal_text)
    assert len(sal_othertreasuryunits) == 2
    bob_othertreasury = sal_othertreasuryunits.get(bob_text)
    tom_othertreasury = sal_othertreasuryunits.get(tom_text)
    assert bob_othertreasury.due_owner_id == bob_text
    assert tom_othertreasury.due_owner_id == tom_text
    assert bob_othertreasury.cash_master == sal_text
    assert tom_othertreasury.cash_master == sal_text

    sal_agenda_after = x_money.userhub.get_job_agenda(owner_id=sal_text)
    bob_other = sal_agenda_after._others.get(bob_text)
    tom_other = sal_agenda_after._others.get(tom_text)
    ava_other = sal_agenda_after._others.get(ava_text)
    elu_other = sal_agenda_after._others.get(elu_text)

    assert bob_othertreasury.due_total == bob_other._treasury_due_paid
    assert bob_othertreasury.due_diff == bob_other._treasury_due_diff
    assert tom_othertreasury.due_total == tom_other._treasury_due_paid
    assert tom_othertreasury.due_diff == tom_other._treasury_due_diff
    assert elu_other is None

    # for othertreasury_uid, sal_othertreasuryunit in sal_othertreasuryunits.items():
    #     print(f"{othertreasury_uid=} {sal_othertreasuryunit=}")
    #     assert sal_othertreasuryunit.cash_master == sal_text
    #     assert sal_othertreasuryunit.due_owner_id in [bob_text, tom_text, elu_text]
    #     x_otherunit = sal_agenda_after._others.get(sal_othertreasuryunit.due_owner_id)
    #     if x_otherunit != None:
    #         # print(
    #         #     f"{sal_othertreasuryunit.cash_master=} {sal_othertreasuryunit.due_owner_id=} {x_otherunit.other_id=} due_total: {sal_othertreasuryunit.due_total} _Due_ Paid: {x_otherunit._treasury_due_paid}"
    #         # )
    #         # print(
    #         #     f"{sal_othertreasuryunit.cash_master=} {sal_othertreasuryunit.due_owner_id=} {x_otherunit.other_id=} due_diff:  {sal_othertreasuryunit.due_diff} _Due_ Paid: {x_otherunit._treasury_due_diff}"
    #         # )
    #         assert sal_othertreasuryunit.due_total == x_otherunit._treasury_due_paid
    #         assert sal_othertreasuryunit.due_diff == x_otherunit._treasury_due_diff

    assert sal_othertreasuryunits.get(ava_text) is None
    assert ava_other._treasury_due_paid is None
    assert ava_other._treasury_due_diff is None

    # for x_otherunit in sal_agenda_after._others.values():
    #     print(f"sal_agenda_after {x_otherunit.other_id=} {x_otherunit._treasury_due_paid=}")
    #     othertreasuryunit_x = sal_othertreasuryunits.get(x_otherunit.other_id)
    #     if othertreasuryunit_x is None:
    #         assert x_otherunit._treasury_due_paid is None
    #         assert x_otherunit._treasury_due_diff is None
    #     else:
    #         assert x_otherunit._treasury_due_paid != None
    #         assert x_otherunit._treasury_due_diff != None
    # assert sal_agenda_after != sal_agenda_before
