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
    credit_weight_text = "credit_weight"
    debtit_weight_text = "debtit_weight"
    swim_text = f"{sue_bud._road_delimiter}Swimmers"
    yao_text = "Yao"
    credit_weight_value = 81
    debtit_weight_value = 43
    yao_atomunit = atomunit_shop(category, atom_insert())
    yao_atomunit.set_arg(group_id_text, swim_text)
    yao_atomunit.set_arg(acct_id_text, yao_text)
    yao_atomunit.set_arg(credit_weight_text, credit_weight_value)
    yao_atomunit.set_arg(debtit_weight_text, debtit_weight_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Group '{swim_text}' has new membership {yao_text} with credit_weight_value{credit_weight_value} and debtit_weight_value={debtit_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_UPDATE_credit_weight_debtit_weight():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = "bud_acct_membership"
    group_id_text = "group_id"
    acct_id_text = "acct_id"
    credit_weight_text = "credit_weight"
    debtit_weight_text = "debtit_weight"
    swim_text = f"{sue_bud._road_delimiter}Swimmers"
    yao_text = "Yao"
    credit_weight_value = 81
    debtit_weight_value = 43
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(group_id_text, swim_text)
    yao_atomunit.set_arg(acct_id_text, yao_text)
    yao_atomunit.set_arg(credit_weight_text, credit_weight_value)
    yao_atomunit.set_arg(debtit_weight_text, debtit_weight_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Group '{swim_text}' membership {yao_text} has new credit_weight_value{credit_weight_value} and debtit_weight_value={debtit_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_UPDATE_credit_weight():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = "bud_acct_membership"
    group_id_text = "group_id"
    acct_id_text = "acct_id"
    credit_weight_text = "credit_weight"
    swim_text = f"{sue_bud._road_delimiter}Swimmers"
    yao_text = "Yao"
    credit_weight_value = 81
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(group_id_text, swim_text)
    yao_atomunit.set_arg(acct_id_text, yao_text)
    yao_atomunit.set_arg(credit_weight_text, credit_weight_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Group '{swim_text}' membership {yao_text} has new credit_weight_value{credit_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_UPDATE_debtit_weight():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    category = "bud_acct_membership"
    group_id_text = "group_id"
    acct_id_text = "acct_id"
    debtit_weight_text = "debtit_weight"
    swim_text = f"{sue_bud._road_delimiter}Swimmers"
    yao_text = "Yao"
    debtit_weight_value = 43
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(group_id_text, swim_text)
    yao_atomunit.set_arg(acct_id_text, yao_text)
    yao_atomunit.set_arg(debtit_weight_text, debtit_weight_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"Group '{swim_text}' membership {yao_text} has new debtit_weight_value={debtit_weight_value}."
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
