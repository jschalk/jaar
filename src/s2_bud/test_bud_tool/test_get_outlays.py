from src.s2_bud.bud import budunit_shop
from src.s2_bud.bud_tool import get_bud_outlay_array, get_bud_outlay_csv


def test_get_bud_outlay_array_ReturnsObj_ScenarioZeroAcctUnits():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")

    # WHEN / THEN
    assert get_bud_outlay_array(sue_bud) == []


def test_get_bud_outlay_array_ReturnsObj_ScenarioSingleAcctUnit():
    # ESTABLISH
    yao_str = "Yao"
    sue_bud = budunit_shop("Sue")
    sue_bud.add_acctunit(yao_str)

    # WHEN / THEN
    assert len(get_bud_outlay_array(sue_bud)) == 1


def test_get_bud_outlay_array_ReturnsObj_ScenarioMultipleAcctUnit():
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
    bud_outlay_array = get_bud_outlay_array(sue_bud)

    # THEN
    assert len(bud_outlay_array) == 3
    assert bud_outlay_array[0][0] == bob_str
    assert bud_outlay_array[1][0] == yao_str
    assert bud_outlay_array[2][0] == zia_str
    assert len(bud_outlay_array[0]) == 3
    assert len(bud_outlay_array[1]) == 3
    assert len(bud_outlay_array[2]) == 3
    assert bud_outlay_array[0][1] == bob_fund_take
    assert bud_outlay_array[0][2] == bob_fund_give
    assert bud_outlay_array[1][1] == yao_fund_take
    assert bud_outlay_array[1][2] == yao_fund_give


def test_get_bud_outlay_csv_ReturnsObj_ScenarioMultipleAcctUnit():
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
    bud_outlay_csv_str = get_bud_outlay_csv(sue_bud)

    # THEN
    print(f"{bud_outlay_csv_str=}")
    print("")
    example_csv_str = f"""acct_id,fund_take,fund_give
{bob_str},{bob_fund_take},{bob_fund_give}
{yao_str},{yao_fund_take},{yao_fund_give}
{zia_str},0,0
"""
    print(f"{example_csv_str=}")
    assert bud_outlay_csv_str == example_csv_str
