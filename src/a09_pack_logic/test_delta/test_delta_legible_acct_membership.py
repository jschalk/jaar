from src.a06_plan_logic._test_util.a06_str import (
    acct_name_str,
    credit_vote_str,
    debt_vote_str,
    group_title_str,
    plan_acct_membership_str,
)
from src.a06_plan_logic.plan import planunit_shop
from src.a08_plan_atom_logic._test_util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a08_plan_atom_logic.atom import planatom_shop
from src.a09_pack_logic.delta import plandelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_acct_membership_INSERT():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_acct_membership_str()
    swim_str = f"{sue_plan.knot}Swimmers"
    yao_str = "Yao"
    credit_vote_value = 81
    debt_vote_value = 43
    yao_planatom = planatom_shop(dimen, INSERT_str())
    yao_planatom.set_arg(group_title_str(), swim_str)
    yao_planatom.set_arg(acct_name_str(), yao_str)
    yao_planatom.set_arg(credit_vote_str(), credit_vote_value)
    yao_planatom.set_arg(debt_vote_str(), debt_vote_value)
    # print(f"{yao_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(yao_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"Group '{swim_str}' has new membership {yao_str} with credit_vote_value{credit_vote_value} and debt_vote_value={debt_vote_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_UPDATE_credit_vote_debt_vote():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_acct_membership_str()
    credit_vote_str = "credit_vote"
    debt_vote_str = "debt_vote"
    swim_str = f"{sue_plan.knot}Swimmers"
    yao_str = "Yao"
    credit_vote_value = 81
    debt_vote_value = 43
    yao_planatom = planatom_shop(dimen, UPDATE_str())
    yao_planatom.set_arg(group_title_str(), swim_str)
    yao_planatom.set_arg(acct_name_str(), yao_str)
    yao_planatom.set_arg(credit_vote_str, credit_vote_value)
    yao_planatom.set_arg(debt_vote_str, debt_vote_value)
    # print(f"{yao_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(yao_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"Group '{swim_str}' membership {yao_str} has new credit_vote_value{credit_vote_value} and debt_vote_value={debt_vote_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_UPDATE_credit_vote():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_acct_membership_str()
    credit_vote_str = "credit_vote"
    swim_str = f"{sue_plan.knot}Swimmers"
    yao_str = "Yao"
    credit_vote_value = 81
    yao_planatom = planatom_shop(dimen, UPDATE_str())
    yao_planatom.set_arg(group_title_str(), swim_str)
    yao_planatom.set_arg(acct_name_str(), yao_str)
    yao_planatom.set_arg(credit_vote_str, credit_vote_value)
    # print(f"{yao_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(yao_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"Group '{swim_str}' membership {yao_str} has new credit_vote_value{credit_vote_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_UPDATE_debt_vote():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_acct_membership_str()
    debt_vote_str = "debt_vote"
    swim_str = f"{sue_plan.knot}Swimmers"
    yao_str = "Yao"
    debt_vote_value = 43
    yao_planatom = planatom_shop(dimen, UPDATE_str())
    yao_planatom.set_arg(group_title_str(), swim_str)
    yao_planatom.set_arg(acct_name_str(), yao_str)
    yao_planatom.set_arg(debt_vote_str, debt_vote_value)
    # print(f"{yao_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(yao_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"Group '{swim_str}' membership {yao_str} has new debt_vote_value={debt_vote_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_DELETE():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    dimen = plan_acct_membership_str()
    swim_str = f"{sue_plan.knot}Swimmers"
    yao_str = "Yao"
    yao_planatom = planatom_shop(dimen, DELETE_str())
    yao_planatom.set_arg(group_title_str(), swim_str)
    yao_planatom.set_arg(acct_name_str(), yao_str)
    # print(f"{yao_planatom=}")
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(yao_planatom)

    # WHEN
    legible_list = create_legible_list(x_plandelta, sue_plan)

    # THEN
    x_str = f"Group '{swim_str}' no longer has membership {yao_str}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
