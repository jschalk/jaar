from src.bud.bud import budunit_shop
from src.listen.hubunit import hubunit_shop
from src.money.rivercycle import get_credorledger, get_debtorledger
from src.money.riverrun import riverrun_shop
from src.money.examples.example_credorledgers import example_yao_hubunit


def test_get_credorledger_ReturnsCorrectObj():
    # ESTABLISH
    yao_text = "Yao"
    bob_text = "Bob"
    sue_text = "Sue"
    yao_credor_weight = 8
    bob_credor_weight = 48
    sue_credor_weight = 66
    yao_bud = budunit_shop(yao_text)
    yao_bud.add_charunit(bob_text, yao_credor_weight)
    yao_bud.add_charunit(sue_text, bob_credor_weight)
    yao_bud.add_charunit(yao_text, sue_credor_weight)

    # WHEN
    yao_credorledger = get_credorledger(yao_bud)

    # THEN
    assert len(yao_credorledger) == 3
    assert yao_credorledger.get(bob_text) == yao_credor_weight
    assert yao_credorledger.get(sue_text) == bob_credor_weight
    assert yao_credorledger.get(yao_text) == sue_credor_weight


def test_get_credorledger_ReturnsCorrectObjWithNoEmpty_credor_weight():
    # ESTABLISH
    yao_text = "Yao"
    bob_text = "Bob"
    sue_text = "Sue"
    yao_credor_weight = 8
    bob_credor_weight = 0
    sue_credor_weight = 66
    yao_bud = budunit_shop(yao_text)
    yao_bud.add_charunit(bob_text, bob_credor_weight)
    yao_bud.add_charunit(sue_text, sue_credor_weight)
    yao_bud.add_charunit(yao_text, yao_credor_weight)

    # WHEN
    yao_credorledger = get_credorledger(yao_bud)

    # THEN
    assert yao_credorledger.get(bob_text) is None
    assert yao_credorledger.get(sue_text) == sue_credor_weight
    assert yao_credorledger.get(yao_text) == yao_credor_weight
    assert len(yao_credorledger) == 2


def test_get_debtorledger_ReturnsCorrectObj():
    # ESTABLISH
    yao_text = "Yao"
    bob_text = "Bob"
    sue_text = "Sue"
    yao_debtor_weight = 8
    bob_debtor_weight = 48
    sue_debtor_weight = 66
    yao_bud = budunit_shop(yao_text)
    yao_bud.add_charunit(bob_text, 2, bob_debtor_weight)
    yao_bud.add_charunit(sue_text, 2, sue_debtor_weight)
    yao_bud.add_charunit(yao_text, 2, yao_debtor_weight)

    # WHEN
    yao_debtorledger = get_debtorledger(yao_bud)

    # THEN
    assert len(yao_debtorledger) == 3
    assert yao_debtorledger.get(bob_text) == bob_debtor_weight
    assert yao_debtorledger.get(sue_text) == sue_debtor_weight
    assert yao_debtorledger.get(yao_text) == yao_debtor_weight


def test_get_debtorledger_ReturnsCorrectObjWithNoEmpty_debtor_weight():
    # ESTABLISH
    yao_text = "Yao"
    bob_text = "Bob"
    sue_text = "Sue"
    yao_debtor_weight = 8
    bob_debtor_weight = 48
    sue_debtor_weight = 0
    yao_bud = budunit_shop(yao_text)
    yao_bud.add_charunit(bob_text, 2, bob_debtor_weight)
    yao_bud.add_charunit(sue_text, 2, sue_debtor_weight)
    yao_bud.add_charunit(yao_text, 2, yao_debtor_weight)

    # WHEN
    yao_debtorledger = get_debtorledger(yao_bud)

    # THEN
    assert yao_debtorledger.get(bob_text) == bob_debtor_weight
    assert yao_debtorledger.get(sue_text) is None
    assert yao_debtorledger.get(yao_text) == yao_debtor_weight
    assert len(yao_debtorledger) == 2


def test_RiverRun_set_char_tax_due_SetsAttr():
    # ESTABLISH
    bob_text = "Bob"
    bob_hubunit = hubunit_shop(None, None, bob_text)
    bob_riverrun = riverrun_shop(bob_hubunit)
    yao_text = "Yao"
    assert bob_riverrun.tax_dues.get(yao_text) is None

    # WHEN
    yao_tax_due = 7
    bob_riverrun.set_char_tax_due(yao_text, yao_tax_due)

    # THEN
    assert bob_riverrun.tax_dues.get(yao_text) == yao_tax_due


def test_RiverRun_tax_dues_unpaid_ReturnsObj():
    # ESTABLISH
    yao_hubunit = example_yao_hubunit()
    x_riverrun = riverrun_shop(yao_hubunit)
    assert x_riverrun.tax_dues_unpaid() == False

    # WHEN
    yao_text = "Yao"
    yao_tax_due = 500
    x_riverrun.set_char_tax_due(yao_text, yao_tax_due)
    # THEN
    assert x_riverrun.tax_dues_unpaid()

    # WHEN
    x_riverrun.delete_tax_due(yao_text)
    # THEN
    assert x_riverrun.tax_dues_unpaid() == False

    # WHEN
    bob_text = "Yao"
    bob_tax_due = 300
    x_riverrun.set_char_tax_due(bob_text, bob_tax_due)
    x_riverrun.set_char_tax_due(yao_text, yao_tax_due)
    # THEN
    assert x_riverrun.tax_dues_unpaid()

    # WHEN
    x_riverrun.delete_tax_due(yao_text)
    # THEN
    assert x_riverrun.tax_dues_unpaid() == False


def test_RiverRun_set_tax_dues_CorrectlySetsAttr():
    # ESTABLISH
    bob_text = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_hubunit = hubunit_shop(
        None, None, bob_text, penny=bob_penny, econ_money_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_hubunit)
    sue_text = "Sue"
    yao_text = "Yao"
    bob_debtor_weight = 38
    sue_debtor_weight = 56
    yao_debtor_weight = 6
    bob_bud = budunit_shop(bob_text)
    bob_bud.add_charunit(bob_text, 2, bob_debtor_weight)
    bob_bud.add_charunit(sue_text, 2, sue_debtor_weight)
    bob_bud.add_charunit(yao_text, 2, yao_debtor_weight)
    bob_debtorledger = get_debtorledger(bob_bud)
    assert bob_riverrun.tax_dues_unpaid() == False

    # WHEN
    bob_riverrun.set_tax_dues(bob_debtorledger)

    # THEN
    assert bob_riverrun.tax_dues_unpaid()
    bob_riverrun = bob_riverrun.tax_dues
    assert bob_riverrun.get(bob_text) == 380
    assert bob_riverrun.get(sue_text) == 560
    assert bob_riverrun.get(yao_text) == 60


def test_RiverRun_char_has_tax_due_ReturnsCorrectBool():
    # ESTABLISH
    bob_text = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_hubunit = hubunit_shop(
        None, None, bob_text, penny=bob_penny, econ_money_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_hubunit)
    yao_text = "Yao"
    sue_text = "Sue"
    zia_text = "Zia"
    yao_debtor_weight = 6
    bob_debtor_weight = 38
    sue_debtor_weight = 56
    bob_bud = budunit_shop(bob_text)
    bob_bud.add_charunit(bob_text, 2, bob_debtor_weight)
    bob_bud.add_charunit(sue_text, 2, sue_debtor_weight)
    bob_bud.add_charunit(yao_text, 2, yao_debtor_weight)
    bob_debtorledger = get_debtorledger(bob_bud)
    assert bob_riverrun.char_has_tax_due(bob_text) == False
    assert bob_riverrun.char_has_tax_due(sue_text) == False
    assert bob_riverrun.char_has_tax_due(yao_text) == False
    assert bob_riverrun.char_has_tax_due(zia_text) == False

    # WHEN
    bob_riverrun.set_tax_dues(bob_debtorledger)

    # THEN
    assert bob_riverrun.char_has_tax_due(bob_text)
    assert bob_riverrun.char_has_tax_due(sue_text)
    assert bob_riverrun.char_has_tax_due(yao_text)
    assert bob_riverrun.char_has_tax_due(zia_text) == False


def test_RiverRun_delete_tax_due_SetsAttr():
    # ESTABLISH
    bob_text = "Bob"
    bob_money_amount = 88
    bob_penny = 11
    bob_hubunit = hubunit_shop(
        None, None, bob_text, penny=bob_penny, econ_money_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_hubunit)
    yao_text = "Yao"
    bob_riverrun.set_char_tax_due(yao_text, 5)
    assert bob_riverrun.char_has_tax_due(yao_text)

    # WHEN
    bob_riverrun.delete_tax_due(yao_text)

    # THEN
    assert bob_riverrun.char_has_tax_due(yao_text) == False


def test_RiverRun_get_char_tax_due_ReturnsCorrectObj():
    # ESTABLISH
    bob_text = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_hubunit = hubunit_shop(
        None, None, bob_text, penny=bob_penny, econ_money_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_hubunit)
    sue_text = "Sue"
    yao_text = "Yao"
    zia_text = "Zia"
    bob_debtor_weight = 38
    sue_debtor_weight = 56
    yao_debtor_weight = 6
    bob_bud = budunit_shop(bob_text)
    bob_bud.add_charunit(bob_text, 2, bob_debtor_weight)
    bob_bud.add_charunit(sue_text, 2, sue_debtor_weight)
    bob_bud.add_charunit(yao_text, 2, yao_debtor_weight)
    bob_debtorledger = get_debtorledger(bob_bud)
    assert bob_riverrun.char_has_tax_due(bob_text) == False
    assert bob_riverrun.get_char_tax_due(bob_text) == 0
    assert bob_riverrun.char_has_tax_due(zia_text) == False
    assert bob_riverrun.get_char_tax_due(zia_text) == 0

    # WHEN
    bob_riverrun.set_tax_dues(bob_debtorledger)

    # THEN
    assert bob_riverrun.char_has_tax_due(bob_text)
    assert bob_riverrun.get_char_tax_due(bob_text) == 380
    assert bob_riverrun.char_has_tax_due(zia_text) == False
    assert bob_riverrun.get_char_tax_due(zia_text) == 0


def test_RiverRun_levy_tax_due_SetsAttr():
    # ESTABLISH
    bob_text = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_hubunit = hubunit_shop(
        None, None, bob_text, penny=bob_penny, econ_money_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_hubunit)
    sue_text = "Sue"
    yao_text = "Yao"
    bob_debtor_weight = 38
    sue_debtor_weight = 56
    yao_debtor_weight = 6
    bob_bud = budunit_shop(bob_text)
    bob_bud.add_charunit(bob_text, 2, bob_debtor_weight)
    bob_bud.add_charunit(sue_text, 2, sue_debtor_weight)
    bob_bud.add_charunit(yao_text, 2, yao_debtor_weight)
    bob_debtorledger = get_debtorledger(bob_bud)
    bob_riverrun.set_tax_dues(bob_debtorledger)
    assert bob_riverrun.get_char_tax_due(bob_text) == 380, 0

    # WHEN / THEN
    excess_payer_money, tax_got = bob_riverrun.levy_tax_due(bob_text, 5)
    assert excess_payer_money == 0
    assert tax_got == 5
    assert bob_riverrun.get_char_tax_due(bob_text) == 375

    # WHEN /THEN
    excess_payer_money, tax_got = bob_riverrun.levy_tax_due(bob_text, 375)
    assert excess_payer_money == 0
    assert tax_got == 375
    assert bob_riverrun.get_char_tax_due(bob_text) == 0
    assert bob_riverrun.char_has_tax_due(bob_text) == False

    # WHEN / THEN
    assert bob_riverrun.get_char_tax_due(sue_text) == 560
    excess_payer_money, tax_got = bob_riverrun.levy_tax_due(sue_text, 1000)
    assert excess_payer_money == 440
    assert tax_got == 560
    assert bob_riverrun.get_char_tax_due(sue_text) == 0
    assert bob_riverrun.tax_dues.get(sue_text) is None

    # WHEN / THEN
    zia_text = "Zia"
    excess_payer_money, tax_got = bob_riverrun.levy_tax_due(zia_text, 1000)
    assert excess_payer_money == 1000
    assert tax_got == 0
    assert bob_riverrun.get_char_tax_due(zia_text) == 0

    # WHEN / THEN
    assert bob_riverrun.get_char_tax_due(yao_text) == 60
    excess_payer_money, tax_got = bob_riverrun.levy_tax_due(yao_text, 81)
    assert excess_payer_money == 21
    assert tax_got == 60
    assert bob_riverrun.get_char_tax_due(yao_text) == 0
