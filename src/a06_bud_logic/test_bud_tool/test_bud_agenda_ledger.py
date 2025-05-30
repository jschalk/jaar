from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic.bud_tool import (
    get_acct_agenda_net_ledger,
    get_acct_mandate_ledger,
    get_bud_acct_agenda_award_array,
    get_bud_acct_agenda_award_csv,
    get_credit_ledger,
)


def test_get_bud_acct_agenda_award_array_ReturnsObj_ScenarioZeroAcctUnits():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")

    # WHEN / THEN
    assert get_bud_acct_agenda_award_array(sue_bud) == []


def test_get_bud_acct_agenda_award_array_ReturnsObj_ScenarioSingleAcctUnit():
    # ESTABLISH
    yao_str = "Yao"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(yao_str)

    # WHEN / THEN
    assert len(get_bud_acct_agenda_award_array(sue_bud)) == 1


def test_get_bud_acct_agenda_award_array_ReturnsObj_ScenarioMultipleAcctUnit():
    # ESTABLISH
    yao_str = "Yao"
    yao_fund_agenda_give = 17
    yao_fund_agenda_take = 23
    bob_str = "Bob"
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    zia_str = "Zia"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(yao_str)
    sue_bud.add_acctunit(bob_str)
    sue_bud.add_acctunit(zia_str)
    sue_bud.get_acct(yao_str)._fund_agenda_give = yao_fund_agenda_give
    sue_bud.get_acct(yao_str)._fund_agenda_take = yao_fund_agenda_take
    sue_bud.get_acct(bob_str)._fund_agenda_give = bob_fund_agenda_give
    sue_bud.get_acct(bob_str)._fund_agenda_take = bob_fund_agenda_take

    # WHEN
    bud_acct_agenda_award_array = get_bud_acct_agenda_award_array(sue_bud)

    # THEN
    assert len(bud_acct_agenda_award_array) == 3
    assert bud_acct_agenda_award_array[0][0] == bob_str
    assert bud_acct_agenda_award_array[1][0] == yao_str
    assert bud_acct_agenda_award_array[2][0] == zia_str
    assert len(bud_acct_agenda_award_array[0]) == 3
    assert len(bud_acct_agenda_award_array[1]) == 3
    assert len(bud_acct_agenda_award_array[2]) == 3
    assert bud_acct_agenda_award_array[0][1] == bob_fund_agenda_take
    assert bud_acct_agenda_award_array[0][2] == bob_fund_agenda_give
    assert bud_acct_agenda_award_array[1][1] == yao_fund_agenda_take
    assert bud_acct_agenda_award_array[1][2] == yao_fund_agenda_give


def test_get_bud_acct_agenda_award_csv_ReturnsObj_ScenarioMultipleAcctUnit():
    # ESTABLISH
    yao_str = "Yao"
    yao_fund_agenda_give = 17
    yao_fund_agenda_take = 23
    bob_str = "Bob"
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    zia_str = "Zia"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(yao_str)
    sue_bud.add_acctunit(bob_str)
    sue_bud.add_acctunit(zia_str)
    sue_bud.get_acct(yao_str)._fund_agenda_give = yao_fund_agenda_give
    sue_bud.get_acct(yao_str)._fund_agenda_take = yao_fund_agenda_take
    sue_bud.get_acct(bob_str)._fund_agenda_give = bob_fund_agenda_give
    sue_bud.get_acct(bob_str)._fund_agenda_take = bob_fund_agenda_take

    # WHEN
    bud_acct_agenda_award_csv_str = get_bud_acct_agenda_award_csv(sue_bud)

    # THEN
    print(f"{bud_acct_agenda_award_csv_str=}")
    print("")
    example_csv_str = f"""acct_name,fund_agenda_take,fund_agenda_give
{bob_str},{bob_fund_agenda_take},{bob_fund_agenda_give}
{yao_str},{yao_fund_agenda_take},{yao_fund_agenda_give}
{zia_str},0,0
"""
    print(f"{example_csv_str=}")
    assert bud_acct_agenda_award_csv_str == example_csv_str


def test_get_bud_acct_agenda_award_csv_ReturnsObj_settle_bud_True():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_str = "Yao"
    bob_str = "Bob"
    xio_str = "Xio"
    zia_str = "Zia"
    sue_bud.add_acctunit(yao_str)
    sue_bud.add_acctunit(bob_str)
    sue_bud.add_acctunit(xio_str)
    sue_bud.add_acctunit(zia_str)
    empty_acct_agenda_award = f"""acct_name,fund_agenda_take,fund_agenda_give
{bob_str},0,0
{xio_str},0,0
{yao_str},0,0
{zia_str},0,0
"""
    assert empty_acct_agenda_award == get_bud_acct_agenda_award_csv(sue_bud)

    # WHEN
    bud_acct_agenda_award_csv_str = get_bud_acct_agenda_award_csv(
        sue_bud, settle_bud=True
    )

    # THEN
    print(f"{bud_acct_agenda_award_csv_str=}")
    print("")
    q_fund_agenda_give = int(sue_bud.fund_pool * 0.25)
    q_fund_agenda_take = int(sue_bud.fund_pool * 0.25)
    example_csv_str = f"""acct_name,fund_agenda_take,fund_agenda_give
{bob_str},{q_fund_agenda_take},{q_fund_agenda_give}
{xio_str},{q_fund_agenda_take},{q_fund_agenda_give}
{yao_str},{q_fund_agenda_take},{q_fund_agenda_give}
{zia_str},{q_fund_agenda_take},{q_fund_agenda_give}
"""
    print(f"{example_csv_str=}")
    assert bud_acct_agenda_award_csv_str == example_csv_str


def test_get_acct_mandate_ledger_ReturnsObj_Scenario0_MultipleAcctUnit():
    # ESTABLISH
    yao_str = "Yao"
    yao_fund_agenda_give = 42
    yao_fund_agenda_take = 23
    bob_str = "Bob"
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    zia_str = "Zia"
    sue_bud = budunit_shop("Sue", fund_pool=200)
    sue_bud.add_acctunit(yao_str)
    sue_bud.add_acctunit(bob_str)
    sue_bud.add_acctunit(zia_str)
    sue_bud.get_acct(yao_str)._fund_agenda_give = yao_fund_agenda_give
    sue_bud.get_acct(yao_str)._fund_agenda_take = yao_fund_agenda_take
    sue_bud.get_acct(bob_str)._fund_agenda_give = bob_fund_agenda_give
    sue_bud.get_acct(bob_str)._fund_agenda_take = bob_fund_agenda_take

    # WHEN
    bud_deal_net_dict = get_acct_mandate_ledger(sue_bud)

    # THEN
    print(f"{bud_deal_net_dict=}")
    print("")
    example_deal_net_dict = {
        bob_str: 58,
        yao_str: 142,
        zia_str: 0,
    }
    print(f"{example_deal_net_dict=}")
    assert example_deal_net_dict == bud_deal_net_dict


def test_get_acct_mandate_ledger_ReturnsObj_Scenario1_settle_bud_True():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_str = "Yao"
    bob_str = "Bob"
    xio_str = "Xio"
    zia_str = "Zia"
    sue_bud.add_acctunit(yao_str, 13, 5)
    sue_bud.add_acctunit(bob_str, 5, 7)
    sue_bud.add_acctunit(xio_str, 2, 3)
    sue_bud.add_acctunit(zia_str, 0, 0)
    pool4th = sue_bud.fund_pool / 4
    pre_settle_acct_mandate_ledger = {
        bob_str: pool4th,
        xio_str: pool4th,
        yao_str: pool4th,
        zia_str: pool4th,
    }
    assert get_acct_mandate_ledger(sue_bud) == pre_settle_acct_mandate_ledger

    # WHEN
    sue_bud_settle_net_dict = get_acct_mandate_ledger(sue_bud, settle_bud=True)

    # THEN
    assert sue_bud_settle_net_dict != pre_settle_acct_mandate_ledger
    print(f"{sue_bud_settle_net_dict=}")
    print("")
    example_deal_net_dict = {
        yao_str: 650000000,
        bob_str: 250000000,
        xio_str: 100000000,
        zia_str: 0,
    }
    print(f"{example_deal_net_dict=}")
    assert sue_bud_settle_net_dict.get(yao_str) != None
    assert sue_bud_settle_net_dict.get(bob_str) != None
    assert sue_bud_settle_net_dict.get(xio_str) != None
    assert sue_bud_settle_net_dict.get(zia_str) != None
    assert sue_bud_settle_net_dict == example_deal_net_dict


def test_get_acct_mandate_ledger_ReturnsObj_Scenario2_No_acctunits():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    empty_acct_mandate_ledger = {sue_str: sue_bud.fund_pool}

    # WHEN / THEN
    assert get_acct_mandate_ledger(sue_bud) == empty_acct_mandate_ledger


def test_get_acct_mandate_ledger_ReturnsObj_Scenario3_No_budunit():
    # ESTABLISH / WHEN / THEN
    assert get_acct_mandate_ledger(None) == {}


def test_get_acct_mandate_ledger_ReturnsObj_Scenario4_MandateSumEqual_fund_pool():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_str = "Yao"
    bob_str = "Bob"
    xio_str = "Xio"
    zia_str = "Zia"
    sue_bud.add_acctunit(yao_str, 13, 5)
    sue_bud.add_acctunit(bob_str, 5, 7)
    sue_bud.add_acctunit(xio_str, 2, 3)
    sue_bud.add_acctunit(zia_str, 0, 0)
    pool4th = sue_bud.fund_pool / 4
    pre_settle_acct_mandate_ledger = {
        bob_str: pool4th,
        xio_str: pool4th,
        yao_str: pool4th,
        zia_str: pool4th,
    }
    assert get_acct_mandate_ledger(sue_bud) == pre_settle_acct_mandate_ledger

    # WHEN
    sue_bud_settle_net_dict = get_acct_mandate_ledger(sue_bud, settle_bud=True)

    # THEN
    assert sue_bud_settle_net_dict != pre_settle_acct_mandate_ledger
    print(f"{sue_bud_settle_net_dict=}")
    print("")
    example_deal_net_dict = {
        yao_str: 650000000,
        bob_str: 250000000,
        xio_str: 100000000,
        zia_str: 0,
    }
    print(f"{example_deal_net_dict=}")
    assert sue_bud_settle_net_dict.get(yao_str) != None
    assert sue_bud_settle_net_dict.get(bob_str) != None
    assert sue_bud_settle_net_dict.get(xio_str) != None
    assert sue_bud_settle_net_dict.get(zia_str) != None
    assert sue_bud_settle_net_dict == example_deal_net_dict


def test_get_acct_mandate_ledger_ReturnsObj_Scenario5_Zero_fund_agenda_give():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_fund_pool = 800
    sue_bud.set_fund_pool(sue_fund_pool)
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_way = sue_bud.make_l1_way(casa_str)
    floor_way = sue_bud.make_way(casa_way, floor_str)
    clean_way = sue_bud.make_way(floor_way, clean_str)
    dirty_way = sue_bud.make_way(floor_way, dirty_str)
    mop_way = sue_bud.make_way(casa_way, mop_str)
    sue_bud.add_concept(floor_way)
    sue_bud.add_concept(clean_way)
    sue_bud.add_concept(dirty_way)
    sue_bud.add_concept(mop_way, pledge=True)
    sue_bud.edit_concept_attr(
        mop_way, reason_rcontext=floor_way, reason_premise=clean_way
    )
    yao_str = "Yao"
    sue_bud.add_acctunit(yao_str, 13, 5)

    # WHEN
    sue_bud_settle_net_dict = get_acct_mandate_ledger(sue_bud, settle_bud=True)

    # THEN
    assert sue_bud_settle_net_dict == {yao_str: sue_fund_pool}


def test_get_acct_agenda_net_ledger_ReturnsObj_ScenarioMultipleAcctUnit():
    # ESTABLISH
    yao_str = "Yao"
    yao_fund_agenda_give = 42
    yao_fund_agenda_take = 23
    bob_str = "Bob"
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    zia_str = "Zia"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(yao_str)
    sue_bud.add_acctunit(bob_str)
    sue_bud.add_acctunit(zia_str)
    sue_bud.get_acct(yao_str)._fund_agenda_give = yao_fund_agenda_give
    sue_bud.get_acct(yao_str)._fund_agenda_take = yao_fund_agenda_take
    sue_bud.get_acct(bob_str)._fund_agenda_give = bob_fund_agenda_give
    sue_bud.get_acct(bob_str)._fund_agenda_take = bob_fund_agenda_take

    # WHEN
    bud_deal_net_dict = get_acct_agenda_net_ledger(sue_bud)

    # THEN
    print(f"{bud_deal_net_dict=}")
    print("")
    example_deal_net_dict = {
        bob_str: bob_fund_agenda_give - bob_fund_agenda_take,
        yao_str: yao_fund_agenda_give - yao_fund_agenda_take,
    }
    print(f"{example_deal_net_dict=}")
    assert example_deal_net_dict == bud_deal_net_dict


def test_get_acct_agenda_net_ledger_ReturnsObj_settle_bud_True():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_str = "Yao"
    bob_str = "Bob"
    xio_str = "Xio"
    zia_str = "Zia"
    sue_bud.add_acctunit(yao_str, 13, 5)
    sue_bud.add_acctunit(bob_str, 5, 7)
    sue_bud.add_acctunit(xio_str, 2, 3)
    sue_bud.add_acctunit(zia_str, 0, 0)
    assert get_acct_agenda_net_ledger(sue_bud) == {}

    # WHEN
    sue_bud_settle_net_dict = get_acct_agenda_net_ledger(sue_bud, settle_bud=True)

    # THEN
    print(f"{sue_bud_settle_net_dict=}")
    print("")
    example_deal_net_dict = {
        bob_str: -216666667,
        yao_str: 316666667,
        xio_str: -100000000,
    }
    print(f"{example_deal_net_dict=}")
    assert sue_bud_settle_net_dict.get(yao_str) != None
    assert sue_bud_settle_net_dict.get(bob_str) != None
    assert sue_bud_settle_net_dict.get(xio_str) != None
    assert sue_bud_settle_net_dict.get(zia_str) is None
    assert sue_bud_settle_net_dict == example_deal_net_dict


def test_get_credit_ledger_ReturnsObj_Scenario0_No_acctunits():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    # WHEN / THEN
    assert get_credit_ledger(sue_bud) == {}


def test_get_credit_ledger_ReturnsObj_Scenario1_acctunits_Exist():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    yao_str = "Yao"
    bob_str = "Bob"
    xio_str = "Xio"
    zia_str = "Zia"
    bob_credit_belief = 11
    yao_credit_belief = 13
    xio_credit_belief = 17
    sue_bud.add_acctunit(yao_str, yao_credit_belief)
    sue_bud.add_acctunit(bob_str, bob_credit_belief)
    sue_bud.add_acctunit(xio_str, xio_credit_belief)

    # WHEN
    sue_acct_credit_ledger = get_credit_ledger(sue_bud)

    # THEN
    print(f"{sue_acct_credit_ledger=}")
    print("")
    expected_sue_acct_credit_ledger = {
        bob_str: bob_credit_belief,
        yao_str: yao_credit_belief,
        xio_str: xio_credit_belief,
    }
    print(f"{expected_sue_acct_credit_ledger=}")
    assert sue_acct_credit_ledger.get(yao_str) != None
    assert sue_acct_credit_ledger.get(bob_str) != None
    assert sue_acct_credit_ledger.get(xio_str) != None
    assert sue_acct_credit_ledger.get(zia_str) is None
    assert sue_acct_credit_ledger == expected_sue_acct_credit_ledger
