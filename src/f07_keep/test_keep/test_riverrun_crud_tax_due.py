from src.f02_bud.bud import budunit_shop
from src.f06_listen.hubunit import hubunit_shop
from src.f07_keep.rivercycle import get_credorledger, get_debtorledger
from src.f07_keep.riverrun import riverrun_shop
from src.f07_keep.examples.keep_env import temp_fisc_mstr_dir
from src.f07_keep.examples.example_credorledgers import example_yao_hubunit


def test_get_credorledger_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_credit_belief = 8
    bob_credit_belief = 48
    sue_credit_belief = 66
    yao_bud = budunit_shop(yao_str)
    yao_bud.add_acctunit(bob_str, yao_credit_belief)
    yao_bud.add_acctunit(sue_str, bob_credit_belief)
    yao_bud.add_acctunit(yao_str, sue_credit_belief)

    # WHEN
    yao_credorledger = get_credorledger(yao_bud)

    # THEN
    assert len(yao_credorledger) == 3
    assert yao_credorledger.get(bob_str) == yao_credit_belief
    assert yao_credorledger.get(sue_str) == bob_credit_belief
    assert yao_credorledger.get(yao_str) == sue_credit_belief


def test_get_credorledger_ReturnsObjWithNoEmpty_credit_belief():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_credit_belief = 8
    bob_credit_belief = 0
    sue_credit_belief = 66
    yao_bud = budunit_shop(yao_str)
    yao_bud.add_acctunit(bob_str, bob_credit_belief)
    yao_bud.add_acctunit(sue_str, sue_credit_belief)
    yao_bud.add_acctunit(yao_str, yao_credit_belief)

    # WHEN
    yao_credorledger = get_credorledger(yao_bud)

    # THEN
    assert yao_credorledger.get(bob_str) is None
    assert yao_credorledger.get(sue_str) == sue_credit_belief
    assert yao_credorledger.get(yao_str) == yao_credit_belief
    assert len(yao_credorledger) == 2


def test_get_debtorledger_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_debtit_belief = 8
    bob_debtit_belief = 48
    sue_debtit_belief = 66
    yao_bud = budunit_shop(yao_str)
    yao_bud.add_acctunit(bob_str, 2, bob_debtit_belief)
    yao_bud.add_acctunit(sue_str, 2, sue_debtit_belief)
    yao_bud.add_acctunit(yao_str, 2, yao_debtit_belief)

    # WHEN
    yao_debtorledger = get_debtorledger(yao_bud)

    # THEN
    assert len(yao_debtorledger) == 3
    assert yao_debtorledger.get(bob_str) == bob_debtit_belief
    assert yao_debtorledger.get(sue_str) == sue_debtit_belief
    assert yao_debtorledger.get(yao_str) == yao_debtit_belief


def test_get_debtorledger_ReturnsObjWithNoEmpty_debtit_belief():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_debtit_belief = 8
    bob_debtit_belief = 48
    sue_debtit_belief = 0
    yao_bud = budunit_shop(yao_str)
    yao_bud.add_acctunit(bob_str, 2, bob_debtit_belief)
    yao_bud.add_acctunit(sue_str, 2, sue_debtit_belief)
    yao_bud.add_acctunit(yao_str, 2, yao_debtit_belief)

    # WHEN
    yao_debtorledger = get_debtorledger(yao_bud)

    # THEN
    assert yao_debtorledger.get(bob_str) == bob_debtit_belief
    assert yao_debtorledger.get(sue_str) is None
    assert yao_debtorledger.get(yao_str) == yao_debtit_belief
    assert len(yao_debtorledger) == 2


def test_RiverRun_set_acct_tax_due_SetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    x_fisc_mstr_dir = temp_fisc_mstr_dir()
    bob_hubunit = hubunit_shop(x_fisc_mstr_dir, None, bob_str)
    bob_riverrun = riverrun_shop(bob_hubunit)
    yao_str = "Yao"
    assert bob_riverrun.tax_dues.get(yao_str) is None

    # WHEN
    yao_tax_due = 7
    bob_riverrun.set_acct_tax_due(yao_str, yao_tax_due)

    # THEN
    assert bob_riverrun.tax_dues.get(yao_str) == yao_tax_due


def test_RiverRun_tax_dues_unpaid_ReturnsObj():
    # ESTABLISH
    yao_hubunit = example_yao_hubunit()
    x_riverrun = riverrun_shop(yao_hubunit)
    assert x_riverrun.tax_dues_unpaid() is False

    # WHEN
    yao_str = "Yao"
    yao_tax_due = 500
    x_riverrun.set_acct_tax_due(yao_str, yao_tax_due)
    # THEN
    assert x_riverrun.tax_dues_unpaid()

    # WHEN
    x_riverrun.delete_tax_due(yao_str)
    # THEN
    assert x_riverrun.tax_dues_unpaid() is False

    # WHEN
    bob_str = "Yao"
    bob_tax_due = 300
    x_riverrun.set_acct_tax_due(bob_str, bob_tax_due)
    x_riverrun.set_acct_tax_due(yao_str, yao_tax_due)
    # THEN
    assert x_riverrun.tax_dues_unpaid()

    # WHEN
    x_riverrun.delete_tax_due(yao_str)
    # THEN
    assert x_riverrun.tax_dues_unpaid() is False


def test_RiverRun_set_tax_dues_CorrectlySetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_hubunit = hubunit_shop(
        None, None, bob_str, penny=bob_penny, keep_point_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_hubunit)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_debtit_belief = 38
    sue_debtit_belief = 56
    yao_debtit_belief = 6
    bob_bud = budunit_shop(bob_str)
    bob_bud.add_acctunit(bob_str, 2, bob_debtit_belief)
    bob_bud.add_acctunit(sue_str, 2, sue_debtit_belief)
    bob_bud.add_acctunit(yao_str, 2, yao_debtit_belief)
    bob_debtorledger = get_debtorledger(bob_bud)
    assert bob_riverrun.tax_dues_unpaid() is False

    # WHEN
    bob_riverrun.set_tax_dues(bob_debtorledger)

    # THEN
    assert bob_riverrun.tax_dues_unpaid()
    bob_riverrun = bob_riverrun.tax_dues
    assert bob_riverrun.get(bob_str) == 380
    assert bob_riverrun.get(sue_str) == 560
    assert bob_riverrun.get(yao_str) == 60


def test_RiverRun_acct_has_tax_due_ReturnsCorrectBool():
    # ESTABLISH
    bob_str = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_hubunit = hubunit_shop(
        None, None, bob_str, penny=bob_penny, keep_point_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_hubunit)
    yao_str = "Yao"
    sue_str = "Sue"
    zia_str = "Zia"
    yao_debtit_belief = 6
    bob_debtit_belief = 38
    sue_debtit_belief = 56
    bob_bud = budunit_shop(bob_str)
    bob_bud.add_acctunit(bob_str, 2, bob_debtit_belief)
    bob_bud.add_acctunit(sue_str, 2, sue_debtit_belief)
    bob_bud.add_acctunit(yao_str, 2, yao_debtit_belief)
    bob_debtorledger = get_debtorledger(bob_bud)
    assert bob_riverrun.acct_has_tax_due(bob_str) is False
    assert bob_riverrun.acct_has_tax_due(sue_str) is False
    assert bob_riverrun.acct_has_tax_due(yao_str) is False
    assert bob_riverrun.acct_has_tax_due(zia_str) is False

    # WHEN
    bob_riverrun.set_tax_dues(bob_debtorledger)

    # THEN
    assert bob_riverrun.acct_has_tax_due(bob_str)
    assert bob_riverrun.acct_has_tax_due(sue_str)
    assert bob_riverrun.acct_has_tax_due(yao_str)
    assert bob_riverrun.acct_has_tax_due(zia_str) is False


def test_RiverRun_delete_tax_due_SetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    bob_money_amount = 88
    bob_penny = 11
    bob_hubunit = hubunit_shop(
        None, None, bob_str, penny=bob_penny, keep_point_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_hubunit)
    yao_str = "Yao"
    bob_riverrun.set_acct_tax_due(yao_str, 5)
    assert bob_riverrun.acct_has_tax_due(yao_str)

    # WHEN
    bob_riverrun.delete_tax_due(yao_str)

    # THEN
    assert bob_riverrun.acct_has_tax_due(yao_str) is False


def test_RiverRun_get_acct_tax_due_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_hubunit = hubunit_shop(
        None, None, bob_str, penny=bob_penny, keep_point_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_hubunit)
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    bob_debtit_belief = 38
    sue_debtit_belief = 56
    yao_debtit_belief = 6
    bob_bud = budunit_shop(bob_str)
    bob_bud.add_acctunit(bob_str, 2, bob_debtit_belief)
    bob_bud.add_acctunit(sue_str, 2, sue_debtit_belief)
    bob_bud.add_acctunit(yao_str, 2, yao_debtit_belief)
    bob_debtorledger = get_debtorledger(bob_bud)
    assert bob_riverrun.acct_has_tax_due(bob_str) is False
    assert bob_riverrun.get_acct_tax_due(bob_str) == 0
    assert bob_riverrun.acct_has_tax_due(zia_str) is False
    assert bob_riverrun.get_acct_tax_due(zia_str) == 0

    # WHEN
    bob_riverrun.set_tax_dues(bob_debtorledger)

    # THEN
    assert bob_riverrun.acct_has_tax_due(bob_str)
    assert bob_riverrun.get_acct_tax_due(bob_str) == 380
    assert bob_riverrun.acct_has_tax_due(zia_str) is False
    assert bob_riverrun.get_acct_tax_due(zia_str) == 0


def test_RiverRun_levy_tax_due_SetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_hubunit = hubunit_shop(
        None, None, bob_str, penny=bob_penny, keep_point_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_hubunit)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_debtit_belief = 38
    sue_debtit_belief = 56
    yao_debtit_belief = 6
    bob_bud = budunit_shop(bob_str)
    bob_bud.add_acctunit(bob_str, 2, bob_debtit_belief)
    bob_bud.add_acctunit(sue_str, 2, sue_debtit_belief)
    bob_bud.add_acctunit(yao_str, 2, yao_debtit_belief)
    bob_debtorledger = get_debtorledger(bob_bud)
    bob_riverrun.set_tax_dues(bob_debtorledger)
    assert bob_riverrun.get_acct_tax_due(bob_str) == 380, 0

    # WHEN / THEN
    excess_payer_points, tax_got = bob_riverrun.levy_tax_due(bob_str, 5)
    assert excess_payer_points == 0
    assert tax_got == 5
    assert bob_riverrun.get_acct_tax_due(bob_str) == 375

    # WHEN /THEN
    excess_payer_points, tax_got = bob_riverrun.levy_tax_due(bob_str, 375)
    assert excess_payer_points == 0
    assert tax_got == 375
    assert bob_riverrun.get_acct_tax_due(bob_str) == 0
    assert bob_riverrun.acct_has_tax_due(bob_str) is False

    # WHEN / THEN
    assert bob_riverrun.get_acct_tax_due(sue_str) == 560
    excess_payer_points, tax_got = bob_riverrun.levy_tax_due(sue_str, 1000)
    assert excess_payer_points == 440
    assert tax_got == 560
    assert bob_riverrun.get_acct_tax_due(sue_str) == 0
    assert bob_riverrun.tax_dues.get(sue_str) is None

    # WHEN / THEN
    zia_str = "Zia"
    excess_payer_points, tax_got = bob_riverrun.levy_tax_due(zia_str, 1000)
    assert excess_payer_points == 1000
    assert tax_got == 0
    assert bob_riverrun.get_acct_tax_due(zia_str) == 0

    # WHEN / THEN
    assert bob_riverrun.get_acct_tax_due(yao_str) == 60
    excess_payer_points, tax_got = bob_riverrun.levy_tax_due(yao_str, 81)
    assert excess_payer_points == 21
    assert tax_got == 60
    assert bob_riverrun.get_acct_tax_due(yao_str) == 0
