from src.money.examples.example_credorledgers import example_yao_hubunit
from src.money.riverrun import riverrun_shop


def test_RiverRun_levy_tax_dues_Transforms_cycleledger_Scenario01():
    # ESTABLISH / WHEN
    yao_hubunit = example_yao_hubunit()
    yao_text = "Yao"
    yao_tax_due = 222
    x_riverrun = riverrun_shop(yao_hubunit)
    x_riverrun.set_char_tax_due(yao_text, yao_tax_due)

    yao_paid = 500
    x_cycleledger = {yao_text: yao_paid}
    assert x_riverrun.get_char_tax_due(yao_text) == yao_tax_due
    assert x_cycleledger.get(yao_text) == yao_paid

    # WHEN
    y_cycleledger, tax_got = x_riverrun.levy_tax_dues(x_cycleledger)

    # THEN
    assert x_riverrun.get_char_tax_due(yao_text) == 0
    assert tax_got == 222
    assert y_cycleledger.get(yao_text) == yao_paid - yao_tax_due


def test_RiverRun_levy_tax_dues_Transforms_cycleledger_Scenario02():
    # ESTABLISH / WHEN
    yao_hubunit = example_yao_hubunit()
    yao_text = "Yao"
    bob_text = "Bob"
    yao_tax_due = 222
    bob_tax_due = 127
    x_riverrun = riverrun_shop(yao_hubunit)
    x_riverrun.set_char_tax_due(yao_text, yao_tax_due)
    x_riverrun.set_char_tax_due(bob_text, bob_tax_due)

    yao_paid = 500
    bob_paid = 100
    x_cycleledger = {yao_text: yao_paid, bob_text: bob_paid}
    assert x_riverrun.get_char_tax_due(yao_text) == yao_tax_due
    assert x_riverrun.get_char_tax_due(bob_text) == bob_tax_due
    assert x_cycleledger.get(yao_text) == yao_paid
    assert x_cycleledger.get(bob_text) == bob_paid

    # WHEN
    y_cycleledger, tax_got = x_riverrun.levy_tax_dues(x_cycleledger)

    # THEN
    assert x_riverrun.get_char_tax_due(yao_text) == 0
    assert x_riverrun.get_char_tax_due(bob_text) == 27
    assert y_cycleledger.get(yao_text) == yao_paid - yao_tax_due
    assert y_cycleledger.get(bob_text) is None
    assert tax_got == 322


def test_RiverRun_cycle_payees_vary_ReturnsCorrectObj():
    # ESTABLISH
    yao_text = "Yao"
    x_riverrun = riverrun_shop(example_yao_hubunit())
    # WHEN / THEN
    assert x_riverrun._cycle_payees_vary() == False

    x_riverrun._cycle_payees_prev = {yao_text}
    assert x_riverrun._cycle_payees_prev == {yao_text}
    assert x_riverrun._cycle_payees_curr == set()

    # WHEN / THEN
    assert x_riverrun._cycle_payees_vary()


def test_RiverRun_cycles_vary_ReturnsCorrectObj():
    # ESTABLISH
    yao_text = "Yao"
    yao_tax_got = 5
    x_riverrun = riverrun_shop(example_yao_hubunit())
    assert x_riverrun._cycle_payees_vary() == False
    assert x_riverrun._tax_gotten() == False
    assert x_riverrun.cycles_vary() == False

    # WHEN
    x_riverrun._cycle_payees_prev = {yao_text}
    # THEN
    assert x_riverrun._cycle_payees_vary()
    assert x_riverrun._tax_gotten() == False
    assert x_riverrun.cycles_vary()

    # WHEN
    x_riverrun._set_tax_got_attrs(yao_tax_got)
    # THEN
    assert x_riverrun._cycle_payees_vary()
    assert x_riverrun._tax_gotten()
    assert x_riverrun.cycles_vary()

    # WHEN
    x_riverrun._cycle_payees_curr = {yao_text}
    # THEN
    assert x_riverrun._cycle_payees_vary() == False
    assert x_riverrun._tax_gotten()
    assert x_riverrun.cycles_vary()
