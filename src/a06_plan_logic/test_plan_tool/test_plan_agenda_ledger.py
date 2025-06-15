from src.a06_plan_logic.plan import planunit_shop
from src.a06_plan_logic.plan_tool import (
    get_acct_agenda_net_ledger,
    get_acct_mandate_ledger,
    get_credit_ledger,
    get_plan_acct_agenda_award_array,
    get_plan_acct_agenda_award_csv,
)


def test_get_plan_acct_agenda_award_array_ReturnsObj_ScenarioZeroAcctUnits():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")

    # WHEN / THEN
    assert get_plan_acct_agenda_award_array(sue_plan) == []


def test_get_plan_acct_agenda_award_array_ReturnsObj_ScenarioSingleAcctUnit():
    # ESTABLISH
    yao_str = "Yao"
    sue_plan = planunit_shop("Sue")
    sue_plan.add_acctunit(yao_str)

    # WHEN / THEN
    assert len(get_plan_acct_agenda_award_array(sue_plan)) == 1


def test_get_plan_acct_agenda_award_array_ReturnsObj_ScenarioMultipleAcctUnit():
    # ESTABLISH
    yao_str = "Yao"
    yao_fund_agenda_give = 17
    yao_fund_agenda_take = 23
    bob_str = "Bob"
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    zia_str = "Zia"
    sue_plan = planunit_shop("Sue")
    sue_plan.add_acctunit(yao_str)
    sue_plan.add_acctunit(bob_str)
    sue_plan.add_acctunit(zia_str)
    sue_plan.get_acct(yao_str)._fund_agenda_give = yao_fund_agenda_give
    sue_plan.get_acct(yao_str)._fund_agenda_take = yao_fund_agenda_take
    sue_plan.get_acct(bob_str)._fund_agenda_give = bob_fund_agenda_give
    sue_plan.get_acct(bob_str)._fund_agenda_take = bob_fund_agenda_take

    # WHEN
    plan_acct_agenda_award_array = get_plan_acct_agenda_award_array(sue_plan)

    # THEN
    assert len(plan_acct_agenda_award_array) == 3
    assert plan_acct_agenda_award_array[0][0] == bob_str
    assert plan_acct_agenda_award_array[1][0] == yao_str
    assert plan_acct_agenda_award_array[2][0] == zia_str
    assert len(plan_acct_agenda_award_array[0]) == 3
    assert len(plan_acct_agenda_award_array[1]) == 3
    assert len(plan_acct_agenda_award_array[2]) == 3
    assert plan_acct_agenda_award_array[0][1] == bob_fund_agenda_take
    assert plan_acct_agenda_award_array[0][2] == bob_fund_agenda_give
    assert plan_acct_agenda_award_array[1][1] == yao_fund_agenda_take
    assert plan_acct_agenda_award_array[1][2] == yao_fund_agenda_give


def test_get_plan_acct_agenda_award_csv_ReturnsObj_ScenarioMultipleAcctUnit():
    # ESTABLISH
    yao_str = "Yao"
    yao_fund_agenda_give = 17
    yao_fund_agenda_take = 23
    bob_str = "Bob"
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    zia_str = "Zia"
    sue_plan = planunit_shop("Sue")
    sue_plan.add_acctunit(yao_str)
    sue_plan.add_acctunit(bob_str)
    sue_plan.add_acctunit(zia_str)
    sue_plan.get_acct(yao_str)._fund_agenda_give = yao_fund_agenda_give
    sue_plan.get_acct(yao_str)._fund_agenda_take = yao_fund_agenda_take
    sue_plan.get_acct(bob_str)._fund_agenda_give = bob_fund_agenda_give
    sue_plan.get_acct(bob_str)._fund_agenda_take = bob_fund_agenda_take

    # WHEN
    plan_acct_agenda_award_csv_str = get_plan_acct_agenda_award_csv(sue_plan)

    # THEN
    print(f"{plan_acct_agenda_award_csv_str=}")
    print("")
    example_csv_str = f"""acct_name,fund_agenda_take,fund_agenda_give
{bob_str},{bob_fund_agenda_take},{bob_fund_agenda_give}
{yao_str},{yao_fund_agenda_take},{yao_fund_agenda_give}
{zia_str},0,0
"""
    print(f"{example_csv_str=}")
    assert plan_acct_agenda_award_csv_str == example_csv_str


def test_get_plan_acct_agenda_award_csv_ReturnsObj_settle_plan_True():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    yao_str = "Yao"
    bob_str = "Bob"
    xio_str = "Xio"
    zia_str = "Zia"
    sue_plan.add_acctunit(yao_str)
    sue_plan.add_acctunit(bob_str)
    sue_plan.add_acctunit(xio_str)
    sue_plan.add_acctunit(zia_str)
    empty_acct_agenda_award = f"""acct_name,fund_agenda_take,fund_agenda_give
{bob_str},0,0
{xio_str},0,0
{yao_str},0,0
{zia_str},0,0
"""
    assert empty_acct_agenda_award == get_plan_acct_agenda_award_csv(sue_plan)

    # WHEN
    plan_acct_agenda_award_csv_str = get_plan_acct_agenda_award_csv(
        sue_plan, settle_plan=True
    )

    # THEN
    print(f"{plan_acct_agenda_award_csv_str=}")
    print("")
    q_fund_agenda_give = int(sue_plan.fund_pool * 0.25)
    q_fund_agenda_take = int(sue_plan.fund_pool * 0.25)
    example_csv_str = f"""acct_name,fund_agenda_take,fund_agenda_give
{bob_str},{q_fund_agenda_take},{q_fund_agenda_give}
{xio_str},{q_fund_agenda_take},{q_fund_agenda_give}
{yao_str},{q_fund_agenda_take},{q_fund_agenda_give}
{zia_str},{q_fund_agenda_take},{q_fund_agenda_give}
"""
    print(f"{example_csv_str=}")
    assert plan_acct_agenda_award_csv_str == example_csv_str


def test_get_acct_mandate_ledger_ReturnsObj_Scenario0_MultipleAcctUnit():
    # ESTABLISH
    yao_str = "Yao"
    yao_fund_agenda_give = 42
    yao_fund_agenda_take = 23
    bob_str = "Bob"
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    zia_str = "Zia"
    sue_plan = planunit_shop("Sue", fund_pool=200)
    sue_plan.add_acctunit(yao_str)
    sue_plan.add_acctunit(bob_str)
    sue_plan.add_acctunit(zia_str)
    sue_plan.get_acct(yao_str)._fund_agenda_give = yao_fund_agenda_give
    sue_plan.get_acct(yao_str)._fund_agenda_take = yao_fund_agenda_take
    sue_plan.get_acct(bob_str)._fund_agenda_give = bob_fund_agenda_give
    sue_plan.get_acct(bob_str)._fund_agenda_take = bob_fund_agenda_take

    # WHEN
    plan_deal_net_dict = get_acct_mandate_ledger(sue_plan)

    # THEN
    print(f"{plan_deal_net_dict=}")
    print("")
    example_deal_net_dict = {
        bob_str: 58,
        yao_str: 142,
        zia_str: 0,
    }
    print(f"{example_deal_net_dict=}")
    assert example_deal_net_dict == plan_deal_net_dict


def test_get_acct_mandate_ledger_ReturnsObj_Scenario1_settle_plan_True():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    yao_str = "Yao"
    bob_str = "Bob"
    xio_str = "Xio"
    zia_str = "Zia"
    sue_plan.add_acctunit(yao_str, 13, 5)
    sue_plan.add_acctunit(bob_str, 5, 7)
    sue_plan.add_acctunit(xio_str, 2, 3)
    sue_plan.add_acctunit(zia_str, 0, 0)
    pool4th = sue_plan.fund_pool / 4
    pre_settle_acct_mandate_ledger = {
        bob_str: pool4th,
        xio_str: pool4th,
        yao_str: pool4th,
        zia_str: pool4th,
    }
    assert get_acct_mandate_ledger(sue_plan) == pre_settle_acct_mandate_ledger

    # WHEN
    sue_plan_settle_net_dict = get_acct_mandate_ledger(sue_plan, settle_plan=True)

    # THEN
    assert sue_plan_settle_net_dict != pre_settle_acct_mandate_ledger
    print(f"{sue_plan_settle_net_dict=}")
    print("")
    example_deal_net_dict = {
        yao_str: 650000000,
        bob_str: 250000000,
        xio_str: 100000000,
        zia_str: 0,
    }
    print(f"{example_deal_net_dict=}")
    assert sue_plan_settle_net_dict.get(yao_str) != None
    assert sue_plan_settle_net_dict.get(bob_str) != None
    assert sue_plan_settle_net_dict.get(xio_str) != None
    assert sue_plan_settle_net_dict.get(zia_str) != None
    assert sue_plan_settle_net_dict == example_deal_net_dict


def test_get_acct_mandate_ledger_ReturnsObj_Scenario2_No_acctunits():
    # ESTABLISH
    sue_str = "Sue"
    sue_plan = planunit_shop(sue_str)
    empty_acct_mandate_ledger = {sue_str: sue_plan.fund_pool}

    # WHEN / THEN
    assert get_acct_mandate_ledger(sue_plan) == empty_acct_mandate_ledger


def test_get_acct_mandate_ledger_ReturnsObj_Scenario3_No_planunit():
    # ESTABLISH / WHEN / THEN
    assert get_acct_mandate_ledger(None) == {}


def test_get_acct_mandate_ledger_ReturnsObj_Scenario4_MandateSumEqual_fund_pool():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    yao_str = "Yao"
    bob_str = "Bob"
    xio_str = "Xio"
    zia_str = "Zia"
    sue_plan.add_acctunit(yao_str, 13, 5)
    sue_plan.add_acctunit(bob_str, 5, 7)
    sue_plan.add_acctunit(xio_str, 2, 3)
    sue_plan.add_acctunit(zia_str, 0, 0)
    pool4th = sue_plan.fund_pool / 4
    pre_settle_acct_mandate_ledger = {
        bob_str: pool4th,
        xio_str: pool4th,
        yao_str: pool4th,
        zia_str: pool4th,
    }
    assert get_acct_mandate_ledger(sue_plan) == pre_settle_acct_mandate_ledger

    # WHEN
    sue_plan_settle_net_dict = get_acct_mandate_ledger(sue_plan, settle_plan=True)

    # THEN
    assert sue_plan_settle_net_dict != pre_settle_acct_mandate_ledger
    print(f"{sue_plan_settle_net_dict=}")
    print("")
    example_deal_net_dict = {
        yao_str: 650000000,
        bob_str: 250000000,
        xio_str: 100000000,
        zia_str: 0,
    }
    print(f"{example_deal_net_dict=}")
    assert sue_plan_settle_net_dict.get(yao_str) != None
    assert sue_plan_settle_net_dict.get(bob_str) != None
    assert sue_plan_settle_net_dict.get(xio_str) != None
    assert sue_plan_settle_net_dict.get(zia_str) != None
    assert sue_plan_settle_net_dict == example_deal_net_dict


def test_get_acct_mandate_ledger_ReturnsObj_Scenario5_Zero_fund_agenda_give():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_fund_pool = 800
    sue_plan.set_fund_pool(sue_fund_pool)
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    floor_rope = sue_plan.make_rope(casa_rope, floor_str)
    clean_rope = sue_plan.make_rope(floor_rope, clean_str)
    dirty_rope = sue_plan.make_rope(floor_rope, dirty_str)
    mop_rope = sue_plan.make_rope(casa_rope, mop_str)
    sue_plan.add_concept(floor_rope)
    sue_plan.add_concept(clean_rope)
    sue_plan.add_concept(dirty_rope)
    sue_plan.add_concept(mop_rope, task=True)
    sue_plan.edit_concept_attr(
        mop_rope, reason_rcontext=floor_rope, reason_premise=clean_rope
    )
    yao_str = "Yao"
    sue_plan.add_acctunit(yao_str, 13, 5)

    # WHEN
    sue_plan_settle_net_dict = get_acct_mandate_ledger(sue_plan, settle_plan=True)

    # THEN
    assert sue_plan_settle_net_dict == {yao_str: sue_fund_pool}


def test_get_acct_agenda_net_ledger_ReturnsObj_ScenarioMultipleAcctUnit():
    # ESTABLISH
    yao_str = "Yao"
    yao_fund_agenda_give = 42
    yao_fund_agenda_take = 23
    bob_str = "Bob"
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    zia_str = "Zia"
    sue_plan = planunit_shop("Sue")
    sue_plan.add_acctunit(yao_str)
    sue_plan.add_acctunit(bob_str)
    sue_plan.add_acctunit(zia_str)
    sue_plan.get_acct(yao_str)._fund_agenda_give = yao_fund_agenda_give
    sue_plan.get_acct(yao_str)._fund_agenda_take = yao_fund_agenda_take
    sue_plan.get_acct(bob_str)._fund_agenda_give = bob_fund_agenda_give
    sue_plan.get_acct(bob_str)._fund_agenda_take = bob_fund_agenda_take

    # WHEN
    plan_deal_net_dict = get_acct_agenda_net_ledger(sue_plan)

    # THEN
    print(f"{plan_deal_net_dict=}")
    print("")
    example_deal_net_dict = {
        bob_str: bob_fund_agenda_give - bob_fund_agenda_take,
        yao_str: yao_fund_agenda_give - yao_fund_agenda_take,
    }
    print(f"{example_deal_net_dict=}")
    assert example_deal_net_dict == plan_deal_net_dict


def test_get_acct_agenda_net_ledger_ReturnsObj_settle_plan_True():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    yao_str = "Yao"
    bob_str = "Bob"
    xio_str = "Xio"
    zia_str = "Zia"
    sue_plan.add_acctunit(yao_str, 13, 5)
    sue_plan.add_acctunit(bob_str, 5, 7)
    sue_plan.add_acctunit(xio_str, 2, 3)
    sue_plan.add_acctunit(zia_str, 0, 0)
    assert get_acct_agenda_net_ledger(sue_plan) == {}

    # WHEN
    sue_plan_settle_net_dict = get_acct_agenda_net_ledger(sue_plan, settle_plan=True)

    # THEN
    print(f"{sue_plan_settle_net_dict=}")
    print("")
    example_deal_net_dict = {
        bob_str: -216666667,
        yao_str: 316666667,
        xio_str: -100000000,
    }
    print(f"{example_deal_net_dict=}")
    assert sue_plan_settle_net_dict.get(yao_str) != None
    assert sue_plan_settle_net_dict.get(bob_str) != None
    assert sue_plan_settle_net_dict.get(xio_str) != None
    assert sue_plan_settle_net_dict.get(zia_str) is None
    assert sue_plan_settle_net_dict == example_deal_net_dict


def test_get_credit_ledger_ReturnsObj_Scenario0_No_acctunits():
    # ESTABLISH
    sue_str = "Sue"
    sue_plan = planunit_shop(sue_str)
    # WHEN / THEN
    assert get_credit_ledger(sue_plan) == {}


def test_get_credit_ledger_ReturnsObj_Scenario1_acctunits_Exist():
    # ESTABLISH
    sue_str = "Sue"
    sue_plan = planunit_shop(sue_str)
    yao_str = "Yao"
    bob_str = "Bob"
    xio_str = "Xio"
    zia_str = "Zia"
    bob_credit_score = 11
    yao_credit_score = 13
    xio_credit_score = 17
    sue_plan.add_acctunit(yao_str, yao_credit_score)
    sue_plan.add_acctunit(bob_str, bob_credit_score)
    sue_plan.add_acctunit(xio_str, xio_credit_score)

    # WHEN
    sue_credit_ledger = get_credit_ledger(sue_plan)

    # THEN
    print(f"{sue_credit_ledger=}")
    print("")
    expected_sue_credit_ledger = {
        bob_str: bob_credit_score,
        yao_str: yao_credit_score,
        xio_str: xio_credit_score,
    }
    print(f"{expected_sue_credit_ledger=}")
    assert sue_credit_ledger.get(yao_str) != None
    assert sue_credit_ledger.get(bob_str) != None
    assert sue_credit_ledger.get(xio_str) != None
    assert sue_credit_ledger.get(zia_str) is None
    assert sue_credit_ledger == expected_sue_credit_ledger
