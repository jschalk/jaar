from src.a06_bud_logic._test_util.a06_str import acct_name_str, bud_acctunit_str
from src.a06_bud_logic.bud import budunit_shop
from src.a08_bud_atom_logic._test_util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a08_bud_atom_logic.atom import budatom_shop
from src.a09_pack_logic.delta import buddelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_acctunit_INSERT():
    # ESTABLISH
    dimen = bud_acctunit_str()
    credit_belief_str = "credit_belief"
    debtit_belief_str = "debtit_belief"
    credit_belief_value = 81
    debtit_belief_value = 43
    yao_str = "Yao"
    yao_budatom = budatom_shop(dimen, INSERT_str())
    yao_budatom.set_arg(acct_name_str(), yao_str)
    yao_budatom.set_arg(credit_belief_str, credit_belief_value)
    yao_budatom.set_arg(debtit_belief_str, debtit_belief_value)
    # print(f"{yao_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(yao_budatom)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"{yao_str} was added with {credit_belief_value} belief credit and {debtit_belief_value} belief debtit"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_INSERT_belief():
    # ESTABLISH
    dimen = bud_acctunit_str()
    credit_belief_str = "credit_belief"
    debtit_belief_str = "debtit_belief"
    credit_belief_value = 81
    debtit_belief_value = 43
    yao_str = "Yao"
    yao_budatom = budatom_shop(dimen, INSERT_str())
    yao_budatom.set_arg(acct_name_str(), yao_str)
    yao_budatom.set_arg(credit_belief_str, credit_belief_value)
    yao_budatom.set_arg(debtit_belief_str, debtit_belief_value)
    # print(f"{yao_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(yao_budatom)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"{yao_str} was added with {credit_belief_value} belief credit and {debtit_belief_value} belief debtit"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_UPDATE_credit_belief_debtit_belief():
    # ESTABLISH
    dimen = bud_acctunit_str()
    credit_belief_str = "credit_belief"
    debtit_belief_str = "debtit_belief"
    credit_belief_value = 81
    debtit_belief_value = 43
    yao_str = "Yao"
    yao_budatom = budatom_shop(dimen, UPDATE_str())
    yao_budatom.set_arg(acct_name_str(), yao_str)
    yao_budatom.set_arg(credit_belief_str, credit_belief_value)
    yao_budatom.set_arg(debtit_belief_str, debtit_belief_value)
    # print(f"{yao_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(yao_budatom)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"{yao_str} now has {credit_belief_value} belief credit and {debtit_belief_value} belief debtit."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_UPDATE_credit_belief():
    # ESTABLISH
    dimen = bud_acctunit_str()
    credit_belief_str = "credit_belief"
    credit_belief_value = 81
    yao_str = "Yao"
    yao_budatom = budatom_shop(dimen, UPDATE_str())
    yao_budatom.set_arg(acct_name_str(), yao_str)
    yao_budatom.set_arg(credit_belief_str, credit_belief_value)
    # print(f"{yao_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(yao_budatom)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"{yao_str} now has {credit_belief_value} belief credit."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_UPDATE_debtit_belief():
    # ESTABLISH
    dimen = bud_acctunit_str()
    debtit_belief_str = "debtit_belief"
    debtit_belief_value = 43
    yao_str = "Yao"
    yao_budatom = budatom_shop(dimen, UPDATE_str())
    yao_budatom.set_arg(acct_name_str(), yao_str)
    yao_budatom.set_arg(debtit_belief_str, debtit_belief_value)
    # print(f"{yao_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(yao_budatom)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"{yao_str} now has {debtit_belief_value} belief debtit."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_DELETE():
    # ESTABLISH
    dimen = bud_acctunit_str()
    yao_str = "Yao"
    yao_budatom = budatom_shop(dimen, DELETE_str())
    yao_budatom.set_arg(acct_name_str(), yao_str)
    # print(f"{yao_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(yao_budatom)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"{yao_str} was removed from belief accts."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
