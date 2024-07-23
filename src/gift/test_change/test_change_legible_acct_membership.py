from src.gift.atom import atomunit_shop, atom_update, atom_insert, atom_delete
from src.gift.change import changeunit_shop
from src.gift.legible import create_legible_list
from src.bud.bud import budunit_shop


def test_create_legible_list_ReturnsObj_acct_membership_INSERT():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = "bud_acct_membership"
    group_id_text = "group_id"
    acct_id_text = "acct_id"
    credit_vote_text = "credit_vote"
    debtit_vote_text = "debtit_vote"
    swim_text = f"{sue_bud._road_delimiter}Swimmers"
    yao_text = "Yao"
    credit_vote_value = 81
    debtit_vote_value = 43
    yao_atomunit = atomunit_shop(category, atom_insert())
    yao_atomunit.set_arg(group_id_text, swim_text)
    yao_atomunit.set_arg(acct_id_text, yao_text)
    yao_atomunit.set_arg(credit_vote_text, credit_vote_value)
    yao_atomunit.set_arg(debtit_vote_text, debtit_vote_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Group '{swim_text}' has new membership {yao_text} with credit_vote_value{credit_vote_value} and debtit_vote_value={debtit_vote_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_UPDATE_credit_vote_debtit_vote():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = "bud_acct_membership"
    group_id_text = "group_id"
    acct_id_text = "acct_id"
    credit_vote_text = "credit_vote"
    debtit_vote_text = "debtit_vote"
    swim_text = f"{sue_bud._road_delimiter}Swimmers"
    yao_text = "Yao"
    credit_vote_value = 81
    debtit_vote_value = 43
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(group_id_text, swim_text)
    yao_atomunit.set_arg(acct_id_text, yao_text)
    yao_atomunit.set_arg(credit_vote_text, credit_vote_value)
    yao_atomunit.set_arg(debtit_vote_text, debtit_vote_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Group '{swim_text}' membership {yao_text} has new credit_vote_value{credit_vote_value} and debtit_vote_value={debtit_vote_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_UPDATE_credit_vote():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = "bud_acct_membership"
    group_id_text = "group_id"
    acct_id_text = "acct_id"
    credit_vote_text = "credit_vote"
    swim_text = f"{sue_bud._road_delimiter}Swimmers"
    yao_text = "Yao"
    credit_vote_value = 81
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(group_id_text, swim_text)
    yao_atomunit.set_arg(acct_id_text, yao_text)
    yao_atomunit.set_arg(credit_vote_text, credit_vote_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Group '{swim_text}' membership {yao_text} has new credit_vote_value{credit_vote_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_UPDATE_debtit_vote():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = "bud_acct_membership"
    group_id_text = "group_id"
    acct_id_text = "acct_id"
    debtit_vote_text = "debtit_vote"
    swim_text = f"{sue_bud._road_delimiter}Swimmers"
    yao_text = "Yao"
    debtit_vote_value = 43
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(group_id_text, swim_text)
    yao_atomunit.set_arg(acct_id_text, yao_text)
    yao_atomunit.set_arg(debtit_vote_text, debtit_vote_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Group '{swim_text}' membership {yao_text} has new debtit_vote_value={debtit_vote_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_DELETE():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = "bud_acct_membership"
    group_id_text = "group_id"
    acct_id_text = "acct_id"
    swim_text = f"{sue_bud._road_delimiter}Swimmers"
    yao_text = "Yao"
    yao_atomunit = atomunit_shop(category, atom_delete())
    yao_atomunit.set_arg(group_id_text, swim_text)
    yao_atomunit.set_arg(acct_id_text, yao_text)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Group '{swim_text}' no longer has membership {yao_text}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
