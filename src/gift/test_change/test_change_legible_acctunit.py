from src.gift.atom import atomunit_shop, atom_update, atom_insert, atom_delete
from src.gift.change import changeunit_shop
from src.gift.legible import create_legible_list
from src.bud.bud import budunit_shop


def test_create_legible_list_ReturnsObj_acctunit_INSERT():
    # ESTABLISH
    category = "bud_acctunit"
    acct_id_text = "acct_id"
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    credor_weight_value = 81
    debtor_weight_value = 43
    yao_text = "Yao"
    yao_atomunit = atomunit_shop(category, atom_insert())
    yao_atomunit.set_arg(acct_id_text, yao_text)
    yao_atomunit.set_arg(credor_weight_text, credor_weight_value)
    yao_atomunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)
    sue_bud = budunit_shop("Sue")
    sue_monetary_desc = "dragon dollars"
    sue_bud.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"{yao_text} was added with {credor_weight_value} {sue_bud._monetary_desc} cred and {debtor_weight_value} {sue_bud._monetary_desc} debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_INSERT_monetary_desc_IsNone():
    # ESTABLISH
    category = "bud_acctunit"
    acct_id_text = "acct_id"
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    credor_weight_value = 81
    debtor_weight_value = 43
    yao_text = "Yao"
    yao_atomunit = atomunit_shop(category, atom_insert())
    yao_atomunit.set_arg(acct_id_text, yao_text)
    yao_atomunit.set_arg(credor_weight_text, credor_weight_value)
    yao_atomunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)
    sue_bud = budunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"{yao_text} was added with {credor_weight_value} monetary_desc cred and {debtor_weight_value} monetary_desc debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_UPDATE_credor_weight_debtor_weight():
    # ESTABLISH
    category = "bud_acctunit"
    acct_id_text = "acct_id"
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    credor_weight_value = 81
    debtor_weight_value = 43
    yao_text = "Yao"
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(acct_id_text, yao_text)
    yao_atomunit.set_arg(credor_weight_text, credor_weight_value)
    yao_atomunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)
    sue_bud = budunit_shop("Sue")
    sue_monetary_desc = "dragon dollars"
    sue_bud.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"{yao_text} now has {credor_weight_value} {sue_bud._monetary_desc} cred and {debtor_weight_value} {sue_bud._monetary_desc} debt."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_UPDATE_credor_weight():
    # ESTABLISH
    category = "bud_acctunit"
    acct_id_text = "acct_id"
    credor_weight_text = "credor_weight"
    credor_weight_value = 81
    yao_text = "Yao"
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(acct_id_text, yao_text)
    yao_atomunit.set_arg(credor_weight_text, credor_weight_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)
    sue_bud = budunit_shop("Sue")
    sue_monetary_desc = "dragon dollars"
    sue_bud.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"{yao_text} now has {credor_weight_value} {sue_bud._monetary_desc} cred."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_UPDATE_debtor_weight():
    # ESTABLISH
    category = "bud_acctunit"
    acct_id_text = "acct_id"
    debtor_weight_text = "debtor_weight"
    debtor_weight_value = 43
    yao_text = "Yao"
    yao_atomunit = atomunit_shop(category, atom_update())
    yao_atomunit.set_arg(acct_id_text, yao_text)
    yao_atomunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)
    sue_bud = budunit_shop("Sue")
    sue_monetary_desc = "dragon dollars"
    sue_bud.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"{yao_text} now has {debtor_weight_value} {sue_bud._monetary_desc} debt."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_DELETE():
    # ESTABLISH
    category = "bud_acctunit"
    acct_id_text = "acct_id"
    yao_text = "Yao"
    yao_atomunit = atomunit_shop(category, atom_delete())
    yao_atomunit.set_arg(acct_id_text, yao_text)
    # print(f"{yao_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(yao_atomunit)
    sue_bud = budunit_shop("Sue")
    sue_monetary_desc = "dragon dollars"
    sue_bud.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_bud)

    # THEN
    x_str = f"{yao_text} was removed from {sue_bud._monetary_desc} accts."
    print(f"{x_str=}")
    assert legible_list[0] == x_str