from src.a06_plan_logic._test_util.a06_str import acct_name_str, plan_acctunit_str
from src.a06_plan_logic.plan import planunit_shop
from src.a08_plan_atom_logic._test_util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a08_plan_atom_logic.atom import planatom_shop
from src.a09_pack_logic.delta import plandelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_acctunit_INSERT():
    # ESTABLISH
    dimen = plan_acctunit_str()
    credit_score_str = "credit_score"
    debtit_score_str = "debtit_score"
    credit_score_value = 81
    debtit_score_value = 43
    yao_str = "Yao"
    yao_planatom = planatom_shop(dimen, INSERT_str())
    yao_planatom.set_arg(acct_name_str(), yao_str)
    yao_planatom.set_arg(credit_score_str, credit_score_value)
    yao_planatom.set_arg(debtit_score_str, debtit_score_value)
    # print(f"{yao_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(yao_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{yao_str} was added with {credit_score_value} score credit and {debtit_score_value} score debtit"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_INSERT_score():
    # ESTABLISH
    dimen = plan_acctunit_str()
    credit_score_str = "credit_score"
    debtit_score_str = "debtit_score"
    credit_score_value = 81
    debtit_score_value = 43
    yao_str = "Yao"
    yao_planatom = planatom_shop(dimen, INSERT_str())
    yao_planatom.set_arg(acct_name_str(), yao_str)
    yao_planatom.set_arg(credit_score_str, credit_score_value)
    yao_planatom.set_arg(debtit_score_str, debtit_score_value)
    # print(f"{yao_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(yao_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{yao_str} was added with {credit_score_value} score credit and {debtit_score_value} score debtit"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_UPDATE_credit_score_debtit_score():
    # ESTABLISH
    dimen = plan_acctunit_str()
    credit_score_str = "credit_score"
    debtit_score_str = "debtit_score"
    credit_score_value = 81
    debtit_score_value = 43
    yao_str = "Yao"
    yao_planatom = planatom_shop(dimen, UPDATE_str())
    yao_planatom.set_arg(acct_name_str(), yao_str)
    yao_planatom.set_arg(credit_score_str, credit_score_value)
    yao_planatom.set_arg(debtit_score_str, debtit_score_value)
    # print(f"{yao_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(yao_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{yao_str} now has {credit_score_value} score credit and {debtit_score_value} score debtit."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_UPDATE_credit_score():
    # ESTABLISH
    dimen = plan_acctunit_str()
    credit_score_str = "credit_score"
    credit_score_value = 81
    yao_str = "Yao"
    yao_planatom = planatom_shop(dimen, UPDATE_str())
    yao_planatom.set_arg(acct_name_str(), yao_str)
    yao_planatom.set_arg(credit_score_str, credit_score_value)
    # print(f"{yao_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(yao_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{yao_str} now has {credit_score_value} score credit."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_UPDATE_debtit_score():
    # ESTABLISH
    dimen = plan_acctunit_str()
    debtit_score_str = "debtit_score"
    debtit_score_value = 43
    yao_str = "Yao"
    yao_planatom = planatom_shop(dimen, UPDATE_str())
    yao_planatom.set_arg(acct_name_str(), yao_str)
    yao_planatom.set_arg(debtit_score_str, debtit_score_value)
    # print(f"{yao_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(yao_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{yao_str} now has {debtit_score_value} score debtit."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_DELETE():
    # ESTABLISH
    dimen = plan_acctunit_str()
    yao_str = "Yao"
    yao_planatom = planatom_shop(dimen, DELETE_str())
    yao_planatom.set_arg(acct_name_str(), yao_str)
    # print(f"{yao_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(yao_planatom)
    sue_plan = planunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"{yao_str} was removed from score accts."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
