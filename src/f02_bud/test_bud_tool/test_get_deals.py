from src.f02_bud.bud import budunit_shop
from src.f02_bud.bud_tool import (
    get_bud_deal_array,
    get_bud_deal_csv,
    get_bud_settle_acct_net_dict,
)


def test_get_bud_deal_array_ReturnsObj_ScenarioZeroAcctUnits():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")

    # WHEN / THEN
    assert get_bud_deal_array(sue_bud) == []


def test_get_bud_deal_array_ReturnsObj_ScenarioSingleAcctUnit():
    # ESTABLISH
    yao_str = "Yao"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(yao_str)

    # WHEN / THEN
    assert len(get_bud_deal_array(sue_bud)) == 1


def test_get_bud_deal_array_ReturnsObj_ScenarioMultipleAcctUnit():
    # ESTABLISH
    yao_str = "Yao"
    yao_fund_give = 17
    yao_fund_take = 23
    bob_str = "Bob"
    bob_fund_give = 17
    bob_fund_take = 23
    zia_str = "Zia"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(yao_str)
    sue_bud.add_acctunit(bob_str)
    sue_bud.add_acctunit(zia_str)
    sue_bud.get_acct(yao_str)._fund_give = yao_fund_give
    sue_bud.get_acct(yao_str)._fund_take = yao_fund_take
    sue_bud.get_acct(bob_str)._fund_give = bob_fund_give
    sue_bud.get_acct(bob_str)._fund_take = bob_fund_take

    # WHEN
    bud_deal_array = get_bud_deal_array(sue_bud)

    # THEN
    assert len(bud_deal_array) == 3
    assert bud_deal_array[0][0] == bob_str
    assert bud_deal_array[1][0] == yao_str
    assert bud_deal_array[2][0] == zia_str
    assert len(bud_deal_array[0]) == 3
    assert len(bud_deal_array[1]) == 3
    assert len(bud_deal_array[2]) == 3
    assert bud_deal_array[0][1] == bob_fund_take
    assert bud_deal_array[0][2] == bob_fund_give
    assert bud_deal_array[1][1] == yao_fund_take
    assert bud_deal_array[1][2] == yao_fund_give


def test_get_bud_deal_csv_ReturnsObj_ScenarioMultipleAcctUnit():
    # ESTABLISH
    yao_str = "Yao"
    yao_fund_give = 17
    yao_fund_take = 23
    bob_str = "Bob"
    bob_fund_give = 17
    bob_fund_take = 23
    zia_str = "Zia"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(yao_str)
    sue_bud.add_acctunit(bob_str)
    sue_bud.add_acctunit(zia_str)
    sue_bud.get_acct(yao_str)._fund_give = yao_fund_give
    sue_bud.get_acct(yao_str)._fund_take = yao_fund_take
    sue_bud.get_acct(bob_str)._fund_give = bob_fund_give
    sue_bud.get_acct(bob_str)._fund_take = bob_fund_take

    # WHEN
    bud_deal_csv_str = get_bud_deal_csv(sue_bud)

    # THEN
    print(f"{bud_deal_csv_str=}")
    print("")
    example_csv_str = f"""acct_name,fund_take,fund_give
{bob_str},{bob_fund_take},{bob_fund_give}
{yao_str},{yao_fund_take},{yao_fund_give}
{zia_str},0,0
"""
    print(f"{example_csv_str=}")
    assert bud_deal_csv_str == example_csv_str


def test_get_bud_deal_csv_ReturnsObj_settle_bud_True():
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
    empty_deal = f"""acct_name,fund_take,fund_give
{bob_str},0,0
{xio_str},0,0
{yao_str},0,0
{zia_str},0,0
"""
    assert empty_deal == get_bud_deal_csv(sue_bud)

    # WHEN
    bud_deal_csv_str = get_bud_deal_csv(sue_bud, settle_bud=True)

    # THEN
    print(f"{bud_deal_csv_str=}")
    print("")
    q_fund_give = int(sue_bud.fund_pool * 0.25)
    q_fund_take = int(sue_bud.fund_pool * 0.25)
    example_csv_str = f"""acct_name,fund_take,fund_give
{bob_str},{q_fund_take},{q_fund_give}
{xio_str},{q_fund_take},{q_fund_give}
{yao_str},{q_fund_take},{q_fund_give}
{zia_str},{q_fund_take},{q_fund_give}
"""
    print(f"{example_csv_str=}")
    assert bud_deal_csv_str == example_csv_str


def test_get_bud_net_deal_dict_ReturnsObj_ScenarioMultipleAcctUnit():
    # ESTABLISH
    yao_str = "Yao"
    yao_fund_give = 42
    yao_fund_take = 23
    bob_str = "Bob"
    bob_fund_give = 17
    bob_fund_take = 23
    zia_str = "Zia"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(yao_str)
    sue_bud.add_acctunit(bob_str)
    sue_bud.add_acctunit(zia_str)
    sue_bud.get_acct(yao_str)._fund_give = yao_fund_give
    sue_bud.get_acct(yao_str)._fund_take = yao_fund_take
    sue_bud.get_acct(bob_str)._fund_give = bob_fund_give
    sue_bud.get_acct(bob_str)._fund_take = bob_fund_take

    # WHEN
    bud_net_deal_dict = get_bud_settle_acct_net_dict(sue_bud)

    # THEN
    print(f"{bud_net_deal_dict=}")
    print("")
    example_net_deal_dict = {
        bob_str: bob_fund_give - bob_fund_take,
        yao_str: yao_fund_give - yao_fund_take,
    }
    print(f"{example_net_deal_dict=}")
    assert example_net_deal_dict == bud_net_deal_dict


def test_get_bud_deal_csv_ReturnsObj_settle_bud_True():
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
    assert get_bud_settle_acct_net_dict(sue_bud) == {}

    # WHEN
    sue_bud_settle_net_dict = get_bud_settle_acct_net_dict(sue_bud, settle_bud=True)

    # THEN
    print(f"{sue_bud_settle_net_dict=}")
    print("")
    example_net_deal_dict = {
        bob_str: -216666667,
        yao_str: 316666667,
        xio_str: -100000000,
    }
    print(f"{example_net_deal_dict=}")
    assert sue_bud_settle_net_dict.get(yao_str) != None
    assert sue_bud_settle_net_dict.get(bob_str) != None
    assert sue_bud_settle_net_dict.get(xio_str) != None
    assert sue_bud_settle_net_dict.get(zia_str) is None
    assert sue_bud_settle_net_dict == example_net_deal_dict
