from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a06_belief_logic.belief_tool import (
    get_belief_partner_agenda_award_array,
    get_belief_partner_agenda_award_csv,
    get_credit_ledger,
    get_partner_agenda_net_ledger,
    get_partner_mandate_ledger,
)


def test_get_belief_partner_agenda_award_array_ReturnsObj_ScenarioZeroPartnerUnits():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")

    # WHEN / THEN
    assert get_belief_partner_agenda_award_array(sue_belief) == []


def test_get_belief_partner_agenda_award_array_ReturnsObj_ScenarioSinglePartnerUnit():
    # ESTABLISH
    yao_str = "Yao"
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_partnerunit(yao_str)

    # WHEN / THEN
    assert len(get_belief_partner_agenda_award_array(sue_belief)) == 1


def test_get_belief_partner_agenda_award_array_ReturnsObj_ScenarioMultiplePartnerUnit():
    # ESTABLISH
    yao_str = "Yao"
    yao_fund_agenda_give = 17
    yao_fund_agenda_take = 23
    bob_str = "Bob"
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    zia_str = "Zia"
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_partnerunit(yao_str)
    sue_belief.add_partnerunit(bob_str)
    sue_belief.add_partnerunit(zia_str)
    sue_belief.get_partner(yao_str)._fund_agenda_give = yao_fund_agenda_give
    sue_belief.get_partner(yao_str)._fund_agenda_take = yao_fund_agenda_take
    sue_belief.get_partner(bob_str)._fund_agenda_give = bob_fund_agenda_give
    sue_belief.get_partner(bob_str)._fund_agenda_take = bob_fund_agenda_take

    # WHEN
    belief_partner_agenda_award_array = get_belief_partner_agenda_award_array(
        sue_belief
    )

    # THEN
    assert len(belief_partner_agenda_award_array) == 3
    assert belief_partner_agenda_award_array[0][0] == bob_str
    assert belief_partner_agenda_award_array[1][0] == yao_str
    assert belief_partner_agenda_award_array[2][0] == zia_str
    assert len(belief_partner_agenda_award_array[0]) == 3
    assert len(belief_partner_agenda_award_array[1]) == 3
    assert len(belief_partner_agenda_award_array[2]) == 3
    assert belief_partner_agenda_award_array[0][1] == bob_fund_agenda_take
    assert belief_partner_agenda_award_array[0][2] == bob_fund_agenda_give
    assert belief_partner_agenda_award_array[1][1] == yao_fund_agenda_take
    assert belief_partner_agenda_award_array[1][2] == yao_fund_agenda_give


def test_get_belief_partner_agenda_award_csv_ReturnsObj_ScenarioMultiplePartnerUnit():
    # ESTABLISH
    yao_str = "Yao"
    yao_fund_agenda_give = 17
    yao_fund_agenda_take = 23
    bob_str = "Bob"
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    zia_str = "Zia"
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_partnerunit(yao_str)
    sue_belief.add_partnerunit(bob_str)
    sue_belief.add_partnerunit(zia_str)
    sue_belief.get_partner(yao_str)._fund_agenda_give = yao_fund_agenda_give
    sue_belief.get_partner(yao_str)._fund_agenda_take = yao_fund_agenda_take
    sue_belief.get_partner(bob_str)._fund_agenda_give = bob_fund_agenda_give
    sue_belief.get_partner(bob_str)._fund_agenda_take = bob_fund_agenda_take

    # WHEN
    belief_partner_agenda_award_csv_str = get_belief_partner_agenda_award_csv(
        sue_belief
    )

    # THEN
    print(f"{belief_partner_agenda_award_csv_str=}")
    print("")
    example_csv_str = f"""partner_name,fund_agenda_take,fund_agenda_give
{bob_str},{bob_fund_agenda_take},{bob_fund_agenda_give}
{yao_str},{yao_fund_agenda_take},{yao_fund_agenda_give}
{zia_str},0,0
"""
    print(f"{example_csv_str=}")
    assert belief_partner_agenda_award_csv_str == example_csv_str


def test_get_belief_partner_agenda_award_csv_ReturnsObj_cash_out_True():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    yao_str = "Yao"
    bob_str = "Bob"
    xio_str = "Xio"
    zia_str = "Zia"
    sue_belief.add_partnerunit(yao_str)
    sue_belief.add_partnerunit(bob_str)
    sue_belief.add_partnerunit(xio_str)
    sue_belief.add_partnerunit(zia_str)
    empty_partner_agenda_award = f"""partner_name,fund_agenda_take,fund_agenda_give
{bob_str},0,0
{xio_str},0,0
{yao_str},0,0
{zia_str},0,0
"""
    assert empty_partner_agenda_award == get_belief_partner_agenda_award_csv(sue_belief)

    # WHEN
    belief_partner_agenda_award_csv_str = get_belief_partner_agenda_award_csv(
        sue_belief, cash_out=True
    )

    # THEN
    print(f"{belief_partner_agenda_award_csv_str=}")
    print("")
    q_fund_agenda_give = int(sue_belief.fund_pool * 0.25)
    q_fund_agenda_take = int(sue_belief.fund_pool * 0.25)
    example_csv_str = f"""partner_name,fund_agenda_take,fund_agenda_give
{bob_str},{q_fund_agenda_take},{q_fund_agenda_give}
{xio_str},{q_fund_agenda_take},{q_fund_agenda_give}
{yao_str},{q_fund_agenda_take},{q_fund_agenda_give}
{zia_str},{q_fund_agenda_take},{q_fund_agenda_give}
"""
    print(f"{example_csv_str=}")
    assert belief_partner_agenda_award_csv_str == example_csv_str


def test_get_partner_mandate_ledger_ReturnsObj_Scenario0_MultiplePartnerUnit():
    # ESTABLISH
    yao_str = "Yao"
    yao_fund_agenda_give = 42
    yao_fund_agenda_take = 23
    bob_str = "Bob"
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    zia_str = "Zia"
    sue_belief = beliefunit_shop("Sue", fund_pool=200)
    sue_belief.add_partnerunit(yao_str)
    sue_belief.add_partnerunit(bob_str)
    sue_belief.add_partnerunit(zia_str)
    sue_belief.get_partner(yao_str)._fund_agenda_give = yao_fund_agenda_give
    sue_belief.get_partner(yao_str)._fund_agenda_take = yao_fund_agenda_take
    sue_belief.get_partner(bob_str)._fund_agenda_give = bob_fund_agenda_give
    sue_belief.get_partner(bob_str)._fund_agenda_take = bob_fund_agenda_take

    # WHEN
    belief_bud_net_dict = get_partner_mandate_ledger(sue_belief)

    # THEN
    print(f"{belief_bud_net_dict=}")
    print("")
    example_bud_net_dict = {
        bob_str: 58,
        yao_str: 142,
        zia_str: 0,
    }
    print(f"{example_bud_net_dict=}")
    assert example_bud_net_dict == belief_bud_net_dict


def test_get_partner_mandate_ledger_ReturnsObj_Scenario1_cash_out_True():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    yao_str = "Yao"
    bob_str = "Bob"
    xio_str = "Xio"
    zia_str = "Zia"
    sue_belief.add_partnerunit(yao_str, 13, 5)
    sue_belief.add_partnerunit(bob_str, 5, 7)
    sue_belief.add_partnerunit(xio_str, 2, 3)
    sue_belief.add_partnerunit(zia_str, 0, 0)
    pool4th = sue_belief.fund_pool / 4
    pre_settle_partner_mandate_ledger = {
        bob_str: pool4th,
        xio_str: pool4th,
        yao_str: pool4th,
        zia_str: pool4th,
    }
    assert get_partner_mandate_ledger(sue_belief) == pre_settle_partner_mandate_ledger

    # WHEN
    sue_belief_settle_net_dict = get_partner_mandate_ledger(sue_belief, cash_out=True)

    # THEN
    assert sue_belief_settle_net_dict != pre_settle_partner_mandate_ledger
    print(f"{sue_belief_settle_net_dict=}")
    print("")
    example_bud_net_dict = {
        yao_str: 650000000,
        bob_str: 250000000,
        xio_str: 100000000,
        zia_str: 0,
    }
    print(f"{example_bud_net_dict=}")
    assert sue_belief_settle_net_dict.get(yao_str) != None
    assert sue_belief_settle_net_dict.get(bob_str) != None
    assert sue_belief_settle_net_dict.get(xio_str) != None
    assert sue_belief_settle_net_dict.get(zia_str) != None
    assert sue_belief_settle_net_dict == example_bud_net_dict


def test_get_partner_mandate_ledger_ReturnsObj_Scenario2_No_partnerunits():
    # ESTABLISH
    sue_str = "Sue"
    sue_belief = beliefunit_shop(sue_str)
    empty_partner_mandate_ledger = {sue_str: sue_belief.fund_pool}

    # WHEN / THEN
    assert get_partner_mandate_ledger(sue_belief) == empty_partner_mandate_ledger


def test_get_partner_mandate_ledger_ReturnsObj_Scenario3_No_beliefunit():
    # ESTABLISH / WHEN / THEN
    assert get_partner_mandate_ledger(None) == {}


def test_get_partner_mandate_ledger_ReturnsObj_Scenario4_MandateSumEqual_fund_pool():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    yao_str = "Yao"
    bob_str = "Bob"
    xio_str = "Xio"
    zia_str = "Zia"
    sue_belief.add_partnerunit(yao_str, 13, 5)
    sue_belief.add_partnerunit(bob_str, 5, 7)
    sue_belief.add_partnerunit(xio_str, 2, 3)
    sue_belief.add_partnerunit(zia_str, 0, 0)
    pool4th = sue_belief.fund_pool / 4
    pre_settle_partner_mandate_ledger = {
        bob_str: pool4th,
        xio_str: pool4th,
        yao_str: pool4th,
        zia_str: pool4th,
    }
    assert get_partner_mandate_ledger(sue_belief) == pre_settle_partner_mandate_ledger

    # WHEN
    sue_belief_settle_net_dict = get_partner_mandate_ledger(sue_belief, cash_out=True)

    # THEN
    assert sue_belief_settle_net_dict != pre_settle_partner_mandate_ledger
    print(f"{sue_belief_settle_net_dict=}")
    print("")
    example_bud_net_dict = {
        yao_str: 650000000,
        bob_str: 250000000,
        xio_str: 100000000,
        zia_str: 0,
    }
    print(f"{example_bud_net_dict=}")
    assert sue_belief_settle_net_dict.get(yao_str) != None
    assert sue_belief_settle_net_dict.get(bob_str) != None
    assert sue_belief_settle_net_dict.get(xio_str) != None
    assert sue_belief_settle_net_dict.get(zia_str) != None
    assert sue_belief_settle_net_dict == example_bud_net_dict


def test_get_partner_mandate_ledger_ReturnsObj_Scenario5_Zero_fund_agenda_give():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_fund_pool = 800
    sue_belief.set_fund_pool(sue_fund_pool)
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    floor_rope = sue_belief.make_rope(casa_rope, floor_str)
    clean_rope = sue_belief.make_rope(floor_rope, clean_str)
    dirty_rope = sue_belief.make_rope(floor_rope, dirty_str)
    mop_rope = sue_belief.make_rope(casa_rope, mop_str)
    sue_belief.add_plan(floor_rope)
    sue_belief.add_plan(clean_rope)
    sue_belief.add_plan(dirty_rope)
    sue_belief.add_plan(mop_rope, task=True)
    sue_belief.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=clean_rope
    )
    yao_str = "Yao"
    sue_belief.add_partnerunit(yao_str, 13, 5)

    # WHEN
    sue_belief_settle_net_dict = get_partner_mandate_ledger(sue_belief, cash_out=True)

    # THEN
    assert sue_belief_settle_net_dict == {yao_str: sue_fund_pool}


def test_get_partner_agenda_net_ledger_ReturnsObj_ScenarioMultiplePartnerUnit():
    # ESTABLISH
    yao_str = "Yao"
    yao_fund_agenda_give = 42
    yao_fund_agenda_take = 23
    bob_str = "Bob"
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    zia_str = "Zia"
    sue_belief = beliefunit_shop("Sue")
    sue_belief.add_partnerunit(yao_str)
    sue_belief.add_partnerunit(bob_str)
    sue_belief.add_partnerunit(zia_str)
    sue_belief.get_partner(yao_str)._fund_agenda_give = yao_fund_agenda_give
    sue_belief.get_partner(yao_str)._fund_agenda_take = yao_fund_agenda_take
    sue_belief.get_partner(bob_str)._fund_agenda_give = bob_fund_agenda_give
    sue_belief.get_partner(bob_str)._fund_agenda_take = bob_fund_agenda_take

    # WHEN
    belief_bud_net_dict = get_partner_agenda_net_ledger(sue_belief)

    # THEN
    print(f"{belief_bud_net_dict=}")
    print("")
    example_bud_net_dict = {
        bob_str: bob_fund_agenda_give - bob_fund_agenda_take,
        yao_str: yao_fund_agenda_give - yao_fund_agenda_take,
    }
    print(f"{example_bud_net_dict=}")
    assert example_bud_net_dict == belief_bud_net_dict


def test_get_partner_agenda_net_ledger_ReturnsObj_cash_out_True():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    yao_str = "Yao"
    bob_str = "Bob"
    xio_str = "Xio"
    zia_str = "Zia"
    sue_belief.add_partnerunit(yao_str, 13, 5)
    sue_belief.add_partnerunit(bob_str, 5, 7)
    sue_belief.add_partnerunit(xio_str, 2, 3)
    sue_belief.add_partnerunit(zia_str, 0, 0)
    assert get_partner_agenda_net_ledger(sue_belief) == {}

    # WHEN
    sue_belief_settle_net_dict = get_partner_agenda_net_ledger(
        sue_belief, cash_out=True
    )

    # THEN
    print(f"{sue_belief_settle_net_dict=}")
    print("")
    example_bud_net_dict = {
        bob_str: -216666667,
        yao_str: 316666667,
        xio_str: -100000000,
    }
    print(f"{example_bud_net_dict=}")
    assert sue_belief_settle_net_dict.get(yao_str) != None
    assert sue_belief_settle_net_dict.get(bob_str) != None
    assert sue_belief_settle_net_dict.get(xio_str) != None
    assert sue_belief_settle_net_dict.get(zia_str) is None
    assert sue_belief_settle_net_dict == example_bud_net_dict


def test_get_credit_ledger_ReturnsObj_Scenario0_No_partnerunits():
    # ESTABLISH
    sue_str = "Sue"
    sue_belief = beliefunit_shop(sue_str)
    # WHEN / THEN
    assert get_credit_ledger(sue_belief) == {}


def test_get_credit_ledger_ReturnsObj_Scenario1_partnerunits_Exist():
    # ESTABLISH
    sue_str = "Sue"
    sue_belief = beliefunit_shop(sue_str)
    yao_str = "Yao"
    bob_str = "Bob"
    xio_str = "Xio"
    zia_str = "Zia"
    bob_partner_cred_points = 11
    yao_partner_cred_points = 13
    xio_partner_cred_points = 17
    sue_belief.add_partnerunit(yao_str, yao_partner_cred_points)
    sue_belief.add_partnerunit(bob_str, bob_partner_cred_points)
    sue_belief.add_partnerunit(xio_str, xio_partner_cred_points)

    # WHEN
    sue_credit_ledger = get_credit_ledger(sue_belief)

    # THEN
    print(f"{sue_credit_ledger=}")
    print("")
    expected_sue_credit_ledger = {
        bob_str: bob_partner_cred_points,
        yao_str: yao_partner_cred_points,
        xio_str: xio_partner_cred_points,
    }
    print(f"{expected_sue_credit_ledger=}")
    assert sue_credit_ledger.get(yao_str) != None
    assert sue_credit_ledger.get(bob_str) != None
    assert sue_credit_ledger.get(xio_str) != None
    assert sue_credit_ledger.get(zia_str) is None
    assert sue_credit_ledger == expected_sue_credit_ledger
