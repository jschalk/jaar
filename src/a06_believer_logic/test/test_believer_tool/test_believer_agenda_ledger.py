from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.believer_tool import (
    get_believer_partner_agenda_award_array,
    get_believer_partner_agenda_award_csv,
    get_credit_ledger,
    get_partner_agenda_net_ledger,
    get_partner_mandate_ledger,
)


def test_get_believer_partner_agenda_award_array_ReturnsObj_ScenarioZeroPartnerUnits():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")

    # WHEN / THEN
    assert get_believer_partner_agenda_award_array(sue_believer) == []


def test_get_believer_partner_agenda_award_array_ReturnsObj_ScenarioSinglePartnerUnit():
    # ESTABLISH
    yao_str = "Yao"
    sue_believer = believerunit_shop("Sue")
    sue_believer.add_partnerunit(yao_str)

    # WHEN / THEN
    assert len(get_believer_partner_agenda_award_array(sue_believer)) == 1


def test_get_believer_partner_agenda_award_array_ReturnsObj_ScenarioMultiplePartnerUnit():
    # ESTABLISH
    yao_str = "Yao"
    yao_fund_agenda_give = 17
    yao_fund_agenda_take = 23
    bob_str = "Bob"
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    zia_str = "Zia"
    sue_believer = believerunit_shop("Sue")
    sue_believer.add_partnerunit(yao_str)
    sue_believer.add_partnerunit(bob_str)
    sue_believer.add_partnerunit(zia_str)
    sue_believer.get_partner(yao_str)._fund_agenda_give = yao_fund_agenda_give
    sue_believer.get_partner(yao_str)._fund_agenda_take = yao_fund_agenda_take
    sue_believer.get_partner(bob_str)._fund_agenda_give = bob_fund_agenda_give
    sue_believer.get_partner(bob_str)._fund_agenda_take = bob_fund_agenda_take

    # WHEN
    believer_partner_agenda_award_array = get_believer_partner_agenda_award_array(
        sue_believer
    )

    # THEN
    assert len(believer_partner_agenda_award_array) == 3
    assert believer_partner_agenda_award_array[0][0] == bob_str
    assert believer_partner_agenda_award_array[1][0] == yao_str
    assert believer_partner_agenda_award_array[2][0] == zia_str
    assert len(believer_partner_agenda_award_array[0]) == 3
    assert len(believer_partner_agenda_award_array[1]) == 3
    assert len(believer_partner_agenda_award_array[2]) == 3
    assert believer_partner_agenda_award_array[0][1] == bob_fund_agenda_take
    assert believer_partner_agenda_award_array[0][2] == bob_fund_agenda_give
    assert believer_partner_agenda_award_array[1][1] == yao_fund_agenda_take
    assert believer_partner_agenda_award_array[1][2] == yao_fund_agenda_give


def test_get_believer_partner_agenda_award_csv_ReturnsObj_ScenarioMultiplePartnerUnit():
    # ESTABLISH
    yao_str = "Yao"
    yao_fund_agenda_give = 17
    yao_fund_agenda_take = 23
    bob_str = "Bob"
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    zia_str = "Zia"
    sue_believer = believerunit_shop("Sue")
    sue_believer.add_partnerunit(yao_str)
    sue_believer.add_partnerunit(bob_str)
    sue_believer.add_partnerunit(zia_str)
    sue_believer.get_partner(yao_str)._fund_agenda_give = yao_fund_agenda_give
    sue_believer.get_partner(yao_str)._fund_agenda_take = yao_fund_agenda_take
    sue_believer.get_partner(bob_str)._fund_agenda_give = bob_fund_agenda_give
    sue_believer.get_partner(bob_str)._fund_agenda_take = bob_fund_agenda_take

    # WHEN
    believer_partner_agenda_award_csv_str = get_believer_partner_agenda_award_csv(
        sue_believer
    )

    # THEN
    print(f"{believer_partner_agenda_award_csv_str=}")
    print("")
    example_csv_str = f"""partner_name,fund_agenda_take,fund_agenda_give
{bob_str},{bob_fund_agenda_take},{bob_fund_agenda_give}
{yao_str},{yao_fund_agenda_take},{yao_fund_agenda_give}
{zia_str},0,0
"""
    print(f"{example_csv_str=}")
    assert believer_partner_agenda_award_csv_str == example_csv_str


def test_get_believer_partner_agenda_award_csv_ReturnsObj_settle_believer_True():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    yao_str = "Yao"
    bob_str = "Bob"
    xio_str = "Xio"
    zia_str = "Zia"
    sue_believer.add_partnerunit(yao_str)
    sue_believer.add_partnerunit(bob_str)
    sue_believer.add_partnerunit(xio_str)
    sue_believer.add_partnerunit(zia_str)
    empty_partner_agenda_award = f"""partner_name,fund_agenda_take,fund_agenda_give
{bob_str},0,0
{xio_str},0,0
{yao_str},0,0
{zia_str},0,0
"""
    assert empty_partner_agenda_award == get_believer_partner_agenda_award_csv(
        sue_believer
    )

    # WHEN
    believer_partner_agenda_award_csv_str = get_believer_partner_agenda_award_csv(
        sue_believer, settle_believer=True
    )

    # THEN
    print(f"{believer_partner_agenda_award_csv_str=}")
    print("")
    q_fund_agenda_give = int(sue_believer.fund_pool * 0.25)
    q_fund_agenda_take = int(sue_believer.fund_pool * 0.25)
    example_csv_str = f"""partner_name,fund_agenda_take,fund_agenda_give
{bob_str},{q_fund_agenda_take},{q_fund_agenda_give}
{xio_str},{q_fund_agenda_take},{q_fund_agenda_give}
{yao_str},{q_fund_agenda_take},{q_fund_agenda_give}
{zia_str},{q_fund_agenda_take},{q_fund_agenda_give}
"""
    print(f"{example_csv_str=}")
    assert believer_partner_agenda_award_csv_str == example_csv_str


def test_get_partner_mandate_ledger_ReturnsObj_Scenario0_MultiplePartnerUnit():
    # ESTABLISH
    yao_str = "Yao"
    yao_fund_agenda_give = 42
    yao_fund_agenda_take = 23
    bob_str = "Bob"
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    zia_str = "Zia"
    sue_believer = believerunit_shop("Sue", fund_pool=200)
    sue_believer.add_partnerunit(yao_str)
    sue_believer.add_partnerunit(bob_str)
    sue_believer.add_partnerunit(zia_str)
    sue_believer.get_partner(yao_str)._fund_agenda_give = yao_fund_agenda_give
    sue_believer.get_partner(yao_str)._fund_agenda_take = yao_fund_agenda_take
    sue_believer.get_partner(bob_str)._fund_agenda_give = bob_fund_agenda_give
    sue_believer.get_partner(bob_str)._fund_agenda_take = bob_fund_agenda_take

    # WHEN
    believer_bud_net_dict = get_partner_mandate_ledger(sue_believer)

    # THEN
    print(f"{believer_bud_net_dict=}")
    print("")
    example_bud_net_dict = {
        bob_str: 58,
        yao_str: 142,
        zia_str: 0,
    }
    print(f"{example_bud_net_dict=}")
    assert example_bud_net_dict == believer_bud_net_dict


def test_get_partner_mandate_ledger_ReturnsObj_Scenario1_settle_believer_True():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    yao_str = "Yao"
    bob_str = "Bob"
    xio_str = "Xio"
    zia_str = "Zia"
    sue_believer.add_partnerunit(yao_str, 13, 5)
    sue_believer.add_partnerunit(bob_str, 5, 7)
    sue_believer.add_partnerunit(xio_str, 2, 3)
    sue_believer.add_partnerunit(zia_str, 0, 0)
    pool4th = sue_believer.fund_pool / 4
    pre_settle_partner_mandate_ledger = {
        bob_str: pool4th,
        xio_str: pool4th,
        yao_str: pool4th,
        zia_str: pool4th,
    }
    assert get_partner_mandate_ledger(sue_believer) == pre_settle_partner_mandate_ledger

    # WHEN
    sue_believer_settle_net_dict = get_partner_mandate_ledger(
        sue_believer, settle_believer=True
    )

    # THEN
    assert sue_believer_settle_net_dict != pre_settle_partner_mandate_ledger
    print(f"{sue_believer_settle_net_dict=}")
    print("")
    example_bud_net_dict = {
        yao_str: 650000000,
        bob_str: 250000000,
        xio_str: 100000000,
        zia_str: 0,
    }
    print(f"{example_bud_net_dict=}")
    assert sue_believer_settle_net_dict.get(yao_str) != None
    assert sue_believer_settle_net_dict.get(bob_str) != None
    assert sue_believer_settle_net_dict.get(xio_str) != None
    assert sue_believer_settle_net_dict.get(zia_str) != None
    assert sue_believer_settle_net_dict == example_bud_net_dict


def test_get_partner_mandate_ledger_ReturnsObj_Scenario2_No_partnerunits():
    # ESTABLISH
    sue_str = "Sue"
    sue_believer = believerunit_shop(sue_str)
    empty_partner_mandate_ledger = {sue_str: sue_believer.fund_pool}

    # WHEN / THEN
    assert get_partner_mandate_ledger(sue_believer) == empty_partner_mandate_ledger


def test_get_partner_mandate_ledger_ReturnsObj_Scenario3_No_believerunit():
    # ESTABLISH / WHEN / THEN
    assert get_partner_mandate_ledger(None) == {}


def test_get_partner_mandate_ledger_ReturnsObj_Scenario4_MandateSumEqual_fund_pool():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    yao_str = "Yao"
    bob_str = "Bob"
    xio_str = "Xio"
    zia_str = "Zia"
    sue_believer.add_partnerunit(yao_str, 13, 5)
    sue_believer.add_partnerunit(bob_str, 5, 7)
    sue_believer.add_partnerunit(xio_str, 2, 3)
    sue_believer.add_partnerunit(zia_str, 0, 0)
    pool4th = sue_believer.fund_pool / 4
    pre_settle_partner_mandate_ledger = {
        bob_str: pool4th,
        xio_str: pool4th,
        yao_str: pool4th,
        zia_str: pool4th,
    }
    assert get_partner_mandate_ledger(sue_believer) == pre_settle_partner_mandate_ledger

    # WHEN
    sue_believer_settle_net_dict = get_partner_mandate_ledger(
        sue_believer, settle_believer=True
    )

    # THEN
    assert sue_believer_settle_net_dict != pre_settle_partner_mandate_ledger
    print(f"{sue_believer_settle_net_dict=}")
    print("")
    example_bud_net_dict = {
        yao_str: 650000000,
        bob_str: 250000000,
        xio_str: 100000000,
        zia_str: 0,
    }
    print(f"{example_bud_net_dict=}")
    assert sue_believer_settle_net_dict.get(yao_str) != None
    assert sue_believer_settle_net_dict.get(bob_str) != None
    assert sue_believer_settle_net_dict.get(xio_str) != None
    assert sue_believer_settle_net_dict.get(zia_str) != None
    assert sue_believer_settle_net_dict == example_bud_net_dict


def test_get_partner_mandate_ledger_ReturnsObj_Scenario5_Zero_fund_agenda_give():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    sue_fund_pool = 800
    sue_believer.set_fund_pool(sue_fund_pool)
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    floor_rope = sue_believer.make_rope(casa_rope, floor_str)
    clean_rope = sue_believer.make_rope(floor_rope, clean_str)
    dirty_rope = sue_believer.make_rope(floor_rope, dirty_str)
    mop_rope = sue_believer.make_rope(casa_rope, mop_str)
    sue_believer.add_plan(floor_rope)
    sue_believer.add_plan(clean_rope)
    sue_believer.add_plan(dirty_rope)
    sue_believer.add_plan(mop_rope, task=True)
    sue_believer.edit_plan_attr(
        mop_rope, reason_context=floor_rope, reason_case=clean_rope
    )
    yao_str = "Yao"
    sue_believer.add_partnerunit(yao_str, 13, 5)

    # WHEN
    sue_believer_settle_net_dict = get_partner_mandate_ledger(
        sue_believer, settle_believer=True
    )

    # THEN
    assert sue_believer_settle_net_dict == {yao_str: sue_fund_pool}


def test_get_partner_agenda_net_ledger_ReturnsObj_ScenarioMultiplePartnerUnit():
    # ESTABLISH
    yao_str = "Yao"
    yao_fund_agenda_give = 42
    yao_fund_agenda_take = 23
    bob_str = "Bob"
    bob_fund_agenda_give = 17
    bob_fund_agenda_take = 23
    zia_str = "Zia"
    sue_believer = believerunit_shop("Sue")
    sue_believer.add_partnerunit(yao_str)
    sue_believer.add_partnerunit(bob_str)
    sue_believer.add_partnerunit(zia_str)
    sue_believer.get_partner(yao_str)._fund_agenda_give = yao_fund_agenda_give
    sue_believer.get_partner(yao_str)._fund_agenda_take = yao_fund_agenda_take
    sue_believer.get_partner(bob_str)._fund_agenda_give = bob_fund_agenda_give
    sue_believer.get_partner(bob_str)._fund_agenda_take = bob_fund_agenda_take

    # WHEN
    believer_bud_net_dict = get_partner_agenda_net_ledger(sue_believer)

    # THEN
    print(f"{believer_bud_net_dict=}")
    print("")
    example_bud_net_dict = {
        bob_str: bob_fund_agenda_give - bob_fund_agenda_take,
        yao_str: yao_fund_agenda_give - yao_fund_agenda_take,
    }
    print(f"{example_bud_net_dict=}")
    assert example_bud_net_dict == believer_bud_net_dict


def test_get_partner_agenda_net_ledger_ReturnsObj_settle_believer_True():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    yao_str = "Yao"
    bob_str = "Bob"
    xio_str = "Xio"
    zia_str = "Zia"
    sue_believer.add_partnerunit(yao_str, 13, 5)
    sue_believer.add_partnerunit(bob_str, 5, 7)
    sue_believer.add_partnerunit(xio_str, 2, 3)
    sue_believer.add_partnerunit(zia_str, 0, 0)
    assert get_partner_agenda_net_ledger(sue_believer) == {}

    # WHEN
    sue_believer_settle_net_dict = get_partner_agenda_net_ledger(
        sue_believer, settle_believer=True
    )

    # THEN
    print(f"{sue_believer_settle_net_dict=}")
    print("")
    example_bud_net_dict = {
        bob_str: -216666667,
        yao_str: 316666667,
        xio_str: -100000000,
    }
    print(f"{example_bud_net_dict=}")
    assert sue_believer_settle_net_dict.get(yao_str) != None
    assert sue_believer_settle_net_dict.get(bob_str) != None
    assert sue_believer_settle_net_dict.get(xio_str) != None
    assert sue_believer_settle_net_dict.get(zia_str) is None
    assert sue_believer_settle_net_dict == example_bud_net_dict


def test_get_credit_ledger_ReturnsObj_Scenario0_No_partnerunits():
    # ESTABLISH
    sue_str = "Sue"
    sue_believer = believerunit_shop(sue_str)
    # WHEN / THEN
    assert get_credit_ledger(sue_believer) == {}


def test_get_credit_ledger_ReturnsObj_Scenario1_partnerunits_Exist():
    # ESTABLISH
    sue_str = "Sue"
    sue_believer = believerunit_shop(sue_str)
    yao_str = "Yao"
    bob_str = "Bob"
    xio_str = "Xio"
    zia_str = "Zia"
    bob_partner_cred_points = 11
    yao_partner_cred_points = 13
    xio_partner_cred_points = 17
    sue_believer.add_partnerunit(yao_str, yao_partner_cred_points)
    sue_believer.add_partnerunit(bob_str, bob_partner_cred_points)
    sue_believer.add_partnerunit(xio_str, xio_partner_cred_points)

    # WHEN
    sue_credit_ledger = get_credit_ledger(sue_believer)

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
