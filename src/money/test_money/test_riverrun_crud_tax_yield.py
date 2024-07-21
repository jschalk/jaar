from src.bud.bud import budunit_shop
from src.listen.hubunit import hubunit_shop
from src.money.rivercycle import get_debtorledger
from src.money.riverrun import riverrun_shop
from src.money.examples.example_credorledgers import example_yao_hubunit


def test_RiverRun_set_acct_tax_yield_SetsAttr():
    # ESTABLISH
    bob_text = "Bob"
    bob_hubunit = hubunit_shop(None, None, bob_text)
    bob_riverrun = riverrun_shop(bob_hubunit)
    yao_text = "Yao"
    assert bob_riverrun._tax_yields.get(yao_text) is None

    # WHEN
    yao_tax_yield = 7
    bob_riverrun.set_acct_tax_yield(yao_text, yao_tax_yield)

    # THEN
    assert bob_riverrun._tax_yields.get(yao_text) == yao_tax_yield


def test_RiverRun_tax_yields_is_empty_ReturnsObj():
    # ESTABLISH
    yao_hubunit = example_yao_hubunit()
    x_riverrun = riverrun_shop(yao_hubunit)
    assert x_riverrun.tax_yields_is_empty()

    # WHEN
    yao_text = "Yao"
    yao_tax_yield = 500
    x_riverrun.set_acct_tax_yield(yao_text, yao_tax_yield)
    # THEN
    assert x_riverrun.tax_yields_is_empty() is False

    # WHEN
    x_riverrun.delete_tax_yield(yao_text)
    # THEN
    assert x_riverrun.tax_yields_is_empty()

    # WHEN
    bob_text = "Yao"
    bob_tax_yield = 300
    x_riverrun.set_acct_tax_yield(bob_text, bob_tax_yield)
    x_riverrun.set_acct_tax_yield(yao_text, yao_tax_yield)
    # THEN
    assert x_riverrun.tax_yields_is_empty() is False

    # WHEN
    x_riverrun.delete_tax_yield(yao_text)
    # THEN
    assert x_riverrun.tax_yields_is_empty()


def test_RiverRun_reset_tax_yields_CorrectlySetsAttr():
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
    bob_tax_yield = 38
    sue_tax_yield = 56
    yao_tax_yield = 6
    bob_riverrun.set_acct_tax_yield(bob_text, bob_tax_yield)
    bob_riverrun.set_acct_tax_yield(sue_text, sue_tax_yield)
    bob_riverrun.set_acct_tax_yield(yao_text, yao_tax_yield)
    assert bob_riverrun.tax_yields_is_empty() is False

    # WHEN
    bob_riverrun.reset_tax_yields()

    # THEN
    assert bob_riverrun.tax_yields_is_empty()


def test_RiverRun_acct_has_tax_yield_ReturnsCorrectBool():
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
    yao_tax_yield = 6
    bob_tax_yield = 38
    sue_tax_yield = 56
    bob_riverrun.set_acct_tax_yield(bob_text, bob_tax_yield)
    bob_riverrun.set_acct_tax_yield(sue_text, sue_tax_yield)
    bob_riverrun.set_acct_tax_yield(yao_text, yao_tax_yield)
    assert bob_riverrun.acct_has_tax_yield(bob_text)
    assert bob_riverrun.acct_has_tax_yield(sue_text)
    assert bob_riverrun.acct_has_tax_yield(yao_text)
    assert bob_riverrun.acct_has_tax_yield(zia_text) is False

    # WHEN
    bob_riverrun.reset_tax_yields()

    # THEN
    assert bob_riverrun.acct_has_tax_yield(bob_text) is False
    assert bob_riverrun.acct_has_tax_yield(sue_text) is False
    assert bob_riverrun.acct_has_tax_yield(yao_text) is False
    assert bob_riverrun.acct_has_tax_yield(zia_text) is False


def test_RiverRun_delete_tax_yield_SetsAttr():
    # ESTABLISH
    bob_text = "Bob"
    bob_money_amount = 88
    bob_penny = 11
    bob_hubunit = hubunit_shop(
        None, None, bob_text, penny=bob_penny, econ_money_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_hubunit)
    yao_text = "Yao"
    bob_riverrun.set_acct_tax_yield(yao_text, 5)
    assert bob_riverrun.acct_has_tax_yield(yao_text)

    # WHEN
    bob_riverrun.delete_tax_yield(yao_text)

    # THEN
    assert bob_riverrun.acct_has_tax_yield(yao_text) is False


def test_RiverRun_get_acct_tax_yield_ReturnsCorrectObj():
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
    bob_tax_yield = 38
    sue_tax_yield = 56
    yao_tax_yield = 6
    bob_riverrun.set_acct_tax_yield(bob_text, bob_tax_yield)
    bob_riverrun.set_acct_tax_yield(sue_text, sue_tax_yield)
    bob_riverrun.set_acct_tax_yield(yao_text, yao_tax_yield)
    assert bob_riverrun.acct_has_tax_yield(bob_text)
    assert bob_riverrun.get_acct_tax_yield(bob_text) == bob_tax_yield
    assert bob_riverrun.acct_has_tax_yield(zia_text) is False
    assert bob_riverrun.get_acct_tax_yield(zia_text) == 0

    # WHEN
    bob_riverrun.reset_tax_yields()

    # THEN
    assert bob_riverrun.acct_has_tax_yield(bob_text) is False
    assert bob_riverrun.get_acct_tax_yield(bob_text) == 0
    assert bob_riverrun.acct_has_tax_yield(zia_text) is False
    assert bob_riverrun.get_acct_tax_yield(zia_text) == 0


def test_RiverRun_add_acct_tax_yield_ReturnsCorrectObj():
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
    bob_tax_yield = 38
    sue_tax_yield = 56
    yao_tax_yield = 6
    bob_riverrun.set_acct_tax_yield(bob_text, bob_tax_yield)
    bob_riverrun.set_acct_tax_yield(sue_text, sue_tax_yield)
    bob_riverrun.set_acct_tax_yield(yao_text, yao_tax_yield)
    assert bob_riverrun.get_acct_tax_yield(bob_text) == bob_tax_yield
    assert bob_riverrun.get_acct_tax_yield(sue_text) == sue_tax_yield
    assert bob_riverrun.get_acct_tax_yield(zia_text) == 0

    # WHEN
    bob_riverrun.add_acct_tax_yield(sue_text, 5)
    bob_riverrun.add_acct_tax_yield(zia_text, 10)

    # THEN
    assert bob_riverrun.get_acct_tax_yield(bob_text) == bob_tax_yield
    assert bob_riverrun.get_acct_tax_yield(sue_text) == sue_tax_yield + 5
    assert bob_riverrun.get_acct_tax_yield(zia_text) == 10


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
    bob_tax_yield = 38
    sue_tax_yield = 56
    yao_tax_yield = 6
    bob_bud = budunit_shop(bob_text)
    bob_bud.add_acctunit(bob_text, 2, bob_tax_yield)
    bob_bud.add_acctunit(sue_text, 2, sue_tax_yield)
    bob_bud.add_acctunit(yao_text, 2, yao_tax_yield)
    bob_debtorledger = get_debtorledger(bob_bud)
    bob_riverrun.set_tax_dues(bob_debtorledger)
    assert bob_riverrun.get_acct_tax_due(bob_text) == 380
    assert bob_riverrun.get_acct_tax_yield(bob_text) == 0

    # WHEN
    excess_payer_money, tax_got = bob_riverrun.levy_tax_due(bob_text, 5)
    # THEN
    assert excess_payer_money == 0
    assert bob_riverrun.get_acct_tax_due(bob_text) == 375
    assert bob_riverrun.get_acct_tax_yield(bob_text) == 5

    # WHEN
    excess_payer_money, tax_got = bob_riverrun.levy_tax_due(bob_text, 375)
    # THEN
    assert excess_payer_money == 0
    assert bob_riverrun.get_acct_tax_due(bob_text) == 0
    assert bob_riverrun.get_acct_tax_yield(bob_text) == 380

    # ESTABLISH
    assert bob_riverrun.get_acct_tax_due(sue_text) == 560
    assert bob_riverrun.get_acct_tax_yield(sue_text) == 0
    # WHEN
    excess_payer_money, tax_got = bob_riverrun.levy_tax_due(sue_text, 1000)
    # THEN
    assert excess_payer_money == 440
    assert bob_riverrun.get_acct_tax_due(sue_text) == 0
    assert bob_riverrun.get_acct_tax_yield(sue_text) == 560

    # ESTABLISH
    zia_text = "Zia"
    assert bob_riverrun.get_acct_tax_due(zia_text) == 0
    assert bob_riverrun.get_acct_tax_yield(zia_text) == 0
    # WHEN
    excess_payer_money, tax_got = bob_riverrun.levy_tax_due(zia_text, 1000)
    # THEN
    assert excess_payer_money == 1000
    assert bob_riverrun.get_acct_tax_due(zia_text) == 0
    assert bob_riverrun.get_acct_tax_yield(zia_text) == 0

    # ESTABLISH
    assert bob_riverrun.get_acct_tax_due(yao_text) == 60
    assert bob_riverrun.get_acct_tax_yield(yao_text) == 0
    # WHEN
    excess_payer_money, tax_got = bob_riverrun.levy_tax_due(yao_text, 81)
    # THEN
    assert excess_payer_money == 21
    assert bob_riverrun.get_acct_tax_due(yao_text) == 0
    assert bob_riverrun.get_acct_tax_yield(yao_text) == 60


def test_RiverRun_set_tax_got_attrs_SetsAttrs():
    # ESTABLISH
    six_tax_got = 6
    ten_tax_got = 10
    x_riverrun = riverrun_shop(example_yao_hubunit())
    assert x_riverrun._tax_got_curr == 0
    assert x_riverrun._tax_got_prev == 0

    # WHEN
    x_riverrun._set_tax_got_attrs(six_tax_got)
    # THEN
    assert x_riverrun._tax_got_curr == six_tax_got
    assert x_riverrun._tax_got_prev == 0

    # WHEN
    x_riverrun._set_tax_got_attrs(ten_tax_got)
    # THEN
    assert x_riverrun._tax_got_curr == ten_tax_got
    assert x_riverrun._tax_got_prev == six_tax_got


def test_RiverRun_tax_gotten_ReturnsObj():
    # ESTABLISH
    six_tax_got = 6
    ten_tax_got = 10
    x_riverrun = riverrun_shop(example_yao_hubunit())
    assert x_riverrun._tax_got_prev == 0
    assert x_riverrun._tax_got_curr == 0
    assert x_riverrun._tax_gotten() is False

    # WHEN
    x_riverrun._set_tax_got_attrs(six_tax_got)
    # THEN
    assert x_riverrun._tax_got_prev == 0
    assert x_riverrun._tax_got_curr == six_tax_got
    assert x_riverrun._tax_gotten()

    # ESTABLISH
    x_riverrun._set_tax_got_attrs(six_tax_got)
    # THEN
    assert x_riverrun._tax_got_prev == six_tax_got
    assert x_riverrun._tax_got_curr == six_tax_got
    assert x_riverrun._tax_gotten()

    # WHEN
    x_riverrun._set_tax_got_attrs(0)
    # THEN
    assert x_riverrun._tax_got_prev == six_tax_got
    assert x_riverrun._tax_got_curr == 0
    assert x_riverrun._tax_gotten()

    # WHEN
    x_riverrun._set_tax_got_attrs(0)
    # THEN
    assert x_riverrun._tax_got_prev == 0
    assert x_riverrun._tax_got_curr == 0
    assert x_riverrun._tax_gotten() is False
