from src.a06_bud_logic._test_util.a06_str import (
    acct_name_str,
    bud_acct_membership_str,
    credit_vote_str,
    debtit_vote_str,
    group_title_str,
)
from src.a06_bud_logic.bud import budunit_shop
from src.a08_bud_atom_logic._test_util.a08_str import DELETE_str, INSERT_str, UPDATE_str
from src.a08_bud_atom_logic.atom import budatom_shop
from src.a09_pack_logic.delta import buddelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_acct_membership_INSERT():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_acct_membership_str()
    swim_str = f"{sue_bud.bridge}Swimmers"
    yao_str = "Yao"
    credit_vote_value = 81
    debtit_vote_value = 43
    yao_budatom = budatom_shop(dimen, INSERT_str())
    yao_budatom.set_arg(group_title_str(), swim_str)
    yao_budatom.set_arg(acct_name_str(), yao_str)
    yao_budatom.set_arg(credit_vote_str(), credit_vote_value)
    yao_budatom.set_arg(debtit_vote_str(), debtit_vote_value)
    # print(f"{yao_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(yao_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Group '{swim_str}' has new membership {yao_str} with credit_vote_value{credit_vote_value} and debtit_vote_value={debtit_vote_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_UPDATE_credit_vote_debtit_vote():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_acct_membership_str()
    credit_vote_str = "credit_vote"
    debtit_vote_str = "debtit_vote"
    swim_str = f"{sue_bud.bridge}Swimmers"
    yao_str = "Yao"
    credit_vote_value = 81
    debtit_vote_value = 43
    yao_budatom = budatom_shop(dimen, UPDATE_str())
    yao_budatom.set_arg(group_title_str(), swim_str)
    yao_budatom.set_arg(acct_name_str(), yao_str)
    yao_budatom.set_arg(credit_vote_str, credit_vote_value)
    yao_budatom.set_arg(debtit_vote_str, debtit_vote_value)
    # print(f"{yao_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(yao_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Group '{swim_str}' membership {yao_str} has new credit_vote_value{credit_vote_value} and debtit_vote_value={debtit_vote_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_UPDATE_credit_vote():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_acct_membership_str()
    credit_vote_str = "credit_vote"
    swim_str = f"{sue_bud.bridge}Swimmers"
    yao_str = "Yao"
    credit_vote_value = 81
    yao_budatom = budatom_shop(dimen, UPDATE_str())
    yao_budatom.set_arg(group_title_str(), swim_str)
    yao_budatom.set_arg(acct_name_str(), yao_str)
    yao_budatom.set_arg(credit_vote_str, credit_vote_value)
    # print(f"{yao_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(yao_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Group '{swim_str}' membership {yao_str} has new credit_vote_value{credit_vote_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_UPDATE_debtit_vote():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_acct_membership_str()
    debtit_vote_str = "debtit_vote"
    swim_str = f"{sue_bud.bridge}Swimmers"
    yao_str = "Yao"
    debtit_vote_value = 43
    yao_budatom = budatom_shop(dimen, UPDATE_str())
    yao_budatom.set_arg(group_title_str(), swim_str)
    yao_budatom.set_arg(acct_name_str(), yao_str)
    yao_budatom.set_arg(debtit_vote_str, debtit_vote_value)
    # print(f"{yao_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(yao_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Group '{swim_str}' membership {yao_str} has new debtit_vote_value={debtit_vote_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    dimen = bud_acct_membership_str()
    swim_str = f"{sue_bud.bridge}Swimmers"
    yao_str = "Yao"
    yao_budatom = budatom_shop(dimen, DELETE_str())
    yao_budatom.set_arg(group_title_str(), swim_str)
    yao_budatom.set_arg(acct_name_str(), yao_str)
    # print(f"{yao_budatom=}")
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(yao_budatom)

    # WHEN
    legible_list = create_legible_list(x_buddelta, sue_bud)

    # THEN
    x_str = f"Group '{swim_str}' no longer has membership {yao_str}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
