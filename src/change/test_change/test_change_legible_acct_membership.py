from src.bud.bud_tool import bud_acct_membership_str
from src.change.atom import atomunit_shop, atom_update, atom_insert, atom_delete
from src.change.atom_config import acct_id_str, group_id_str
from src.change.change import changeunit_shop
from src.change.legible import create_legible_list
from src.bud.bud import budunit_shop


def test_create_legible_list_ReturnsObj_acct_membership_INSERT():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_acct_membership_str()
    credit_vote_str = "credit_vote"
    debtit_vote_str = "debtit_vote"
    swim_str = f"{sue_bud._road_delimiter}Swimmers"
    yao_str = "Yao"
    credit_vote_value = 81
    debtit_vote_value = 43
    yao_atomunit = atomunit_shop(category, atom_insert())
    yao_atomunit.set_arg(group_id_str(), swim_str)
    yao_atomunit.set_arg(acct_id_str(), yao_str)
    yao_atomunit.set_arg(credit_vote_str, credit_vote_value)
    yao_atomunit.set_arg(debtit_vote_str, debtit_vote_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Group '{swim_str}' has new membership {yao_str} with credit_vote_value{credit_vote_value} and debtit_vote_value={debtit_vote_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_UPDATE_credit_vote_debtit_vote():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_acct_membership_str()
    credit_vote_str = "credit_vote"
    debtit_vote_str = "debtit_vote"
    swim_str = f"{sue_bud._road_delimiter}Swimmers"
    yao_str = "Yao"
    credit_vote_value = 81
    debtit_vote_value = 43
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(group_id_str(), swim_str)
    yao_atomunit.set_arg(acct_id_str(), yao_str)
    yao_atomunit.set_arg(credit_vote_str, credit_vote_value)
    yao_atomunit.set_arg(debtit_vote_str, debtit_vote_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Group '{swim_str}' membership {yao_str} has new credit_vote_value{credit_vote_value} and debtit_vote_value={debtit_vote_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_UPDATE_credit_vote():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_acct_membership_str()
    credit_vote_str = "credit_vote"
    swim_str = f"{sue_bud._road_delimiter}Swimmers"
    yao_str = "Yao"
    credit_vote_value = 81
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(group_id_str(), swim_str)
    yao_atomunit.set_arg(acct_id_str(), yao_str)
    yao_atomunit.set_arg(credit_vote_str, credit_vote_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Group '{swim_str}' membership {yao_str} has new credit_vote_value{credit_vote_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_UPDATE_debtit_vote():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_acct_membership_str()
    debtit_vote_str = "debtit_vote"
    swim_str = f"{sue_bud._road_delimiter}Swimmers"
    yao_str = "Yao"
    debtit_vote_value = 43
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(group_id_str(), swim_str)
    yao_atomunit.set_arg(acct_id_str(), yao_str)
    yao_atomunit.set_arg(debtit_vote_str, debtit_vote_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Group '{swim_str}' membership {yao_str} has new debtit_vote_value={debtit_vote_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = bud_acct_membership_str()
    swim_str = f"{sue_bud._road_delimiter}Swimmers"
    yao_str = "Yao"
    yao_atomunit = atomunit_shop(category, atom_delete())
    yao_atomunit.set_arg(group_id_str(), swim_str)
    yao_atomunit.set_arg(acct_id_str(), yao_str)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Group '{swim_str}' no longer has membership {yao_str}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
