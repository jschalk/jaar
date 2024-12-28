from src.f02_bud.bud_tool import bud_acctunit_str
from src.f04_gift.atom_config import (
    atom_update,
    atom_insert,
    atom_delete,
    acct_name_str,
)
from src.f04_gift.atom import atomunit_shop
from src.f04_gift.delta import deltaunit_shop
from src.f04_gift.legible import create_legible_list
from src.f02_bud.bud import budunit_shop


def test_create_legible_list_ReturnsObj_acctunit_INSERT():
    # ESTABLISH
    category = bud_acctunit_str()
    credit_belief_str = "credit_belief"
    debtit_belief_str = "debtit_belief"
    credit_belief_value = 81
    debtit_belief_value = 43
    yao_str = "Yao"
    yao_atomunit = atomunit_shop(category, atom_insert())
    yao_atomunit.set_arg(acct_name_str(), yao_str)
    yao_atomunit.set_arg(credit_belief_str, credit_belief_value)
    yao_atomunit.set_arg(debtit_belief_str, debtit_belief_value)
    # print(f"{yao_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(yao_atomunit)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"{yao_str} was added with {credit_belief_value} belief credit and {debtit_belief_value} belief debtit"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_INSERT_belief():
    # ESTABLISH
    category = bud_acctunit_str()
    credit_belief_str = "credit_belief"
    debtit_belief_str = "debtit_belief"
    credit_belief_value = 81
    debtit_belief_value = 43
    yao_str = "Yao"
    yao_atomunit = atomunit_shop(category, atom_insert())
    yao_atomunit.set_arg(acct_name_str(), yao_str)
    yao_atomunit.set_arg(credit_belief_str, credit_belief_value)
    yao_atomunit.set_arg(debtit_belief_str, debtit_belief_value)
    # print(f"{yao_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(yao_atomunit)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"{yao_str} was added with {credit_belief_value} belief credit and {debtit_belief_value} belief debtit"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_UPDATE_credit_belief_debtit_belief():
    # ESTABLISH
    category = bud_acctunit_str()
    credit_belief_str = "credit_belief"
    debtit_belief_str = "debtit_belief"
    credit_belief_value = 81
    debtit_belief_value = 43
    yao_str = "Yao"
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(acct_name_str(), yao_str)
    yao_atomunit.set_arg(credit_belief_str, credit_belief_value)
    yao_atomunit.set_arg(debtit_belief_str, debtit_belief_value)
    # print(f"{yao_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(yao_atomunit)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"{yao_str} now has {credit_belief_value} belief credit and {debtit_belief_value} belief debtit."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_UPDATE_credit_belief():
    # ESTABLISH
    category = bud_acctunit_str()
    credit_belief_str = "credit_belief"
    credit_belief_value = 81
    yao_str = "Yao"
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(acct_name_str(), yao_str)
    yao_atomunit.set_arg(credit_belief_str, credit_belief_value)
    # print(f"{yao_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(yao_atomunit)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"{yao_str} now has {credit_belief_value} belief credit."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_UPDATE_debtit_belief():
    # ESTABLISH
    category = bud_acctunit_str()
    debtit_belief_str = "debtit_belief"
    debtit_belief_value = 43
    yao_str = "Yao"
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(acct_name_str(), yao_str)
    yao_atomunit.set_arg(debtit_belief_str, debtit_belief_value)
    # print(f"{yao_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(yao_atomunit)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"{yao_str} now has {debtit_belief_value} belief debtit."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_DELETE():
    # ESTABLISH
    category = bud_acctunit_str()
    yao_str = "Yao"
    yao_atomunit = atomunit_shop(category, atom_delete())
    yao_atomunit.set_arg(acct_name_str(), yao_str)
    # print(f"{yao_atomunit=}")
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(yao_atomunit)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_deltaunit, sue_bud)

    # THEN
    x_str = f"{yao_str} was removed from belief accts."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
