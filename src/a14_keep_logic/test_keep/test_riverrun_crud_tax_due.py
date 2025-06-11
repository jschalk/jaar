from src.a06_plan_logic.plan import planunit_shop
from src.a12_hub_tools.hubunit import hubunit_shop
from src.a14_keep_logic._test_util.a14_env import temp_vow_mstr_dir
from src.a14_keep_logic._test_util.example_credorledgers import example_yao_hubunit
from src.a14_keep_logic.rivercycle import get_credorledger, get_debtorledger
from src.a14_keep_logic.riverrun import riverrun_shop


def test_get_credorledger_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_credit_score = 8
    bob_credit_score = 48
    sue_credit_score = 66
    yao_plan = planunit_shop(yao_str)
    yao_plan.add_acctunit(bob_str, yao_credit_score)
    yao_plan.add_acctunit(sue_str, bob_credit_score)
    yao_plan.add_acctunit(yao_str, sue_credit_score)

    # WHEN
    yao_credorledger = get_credorledger(yao_plan)

    # THEN
    assert len(yao_credorledger) == 3
    assert yao_credorledger.get(bob_str) == yao_credit_score
    assert yao_credorledger.get(sue_str) == bob_credit_score
    assert yao_credorledger.get(yao_str) == sue_credit_score


def test_get_credorledger_ReturnsObjWithNoEmpty_credit_score():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_credit_score = 8
    bob_credit_score = 0
    sue_credit_score = 66
    yao_plan = planunit_shop(yao_str)
    yao_plan.add_acctunit(bob_str, bob_credit_score)
    yao_plan.add_acctunit(sue_str, sue_credit_score)
    yao_plan.add_acctunit(yao_str, yao_credit_score)

    # WHEN
    yao_credorledger = get_credorledger(yao_plan)

    # THEN
    assert yao_credorledger.get(bob_str) is None
    assert yao_credorledger.get(sue_str) == sue_credit_score
    assert yao_credorledger.get(yao_str) == yao_credit_score
    assert len(yao_credorledger) == 2


def test_get_debtorledger_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_debt_score = 8
    bob_debt_score = 48
    sue_debt_score = 66
    yao_plan = planunit_shop(yao_str)
    yao_plan.add_acctunit(bob_str, 2, bob_debt_score)
    yao_plan.add_acctunit(sue_str, 2, sue_debt_score)
    yao_plan.add_acctunit(yao_str, 2, yao_debt_score)

    # WHEN
    yao_debtorledger = get_debtorledger(yao_plan)

    # THEN
    assert len(yao_debtorledger) == 3
    assert yao_debtorledger.get(bob_str) == bob_debt_score
    assert yao_debtorledger.get(sue_str) == sue_debt_score
    assert yao_debtorledger.get(yao_str) == yao_debt_score


def test_get_debtorledger_ReturnsObjWithNoEmpty_debt_score():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_debt_score = 8
    bob_debt_score = 48
    sue_debt_score = 0
    yao_plan = planunit_shop(yao_str)
    yao_plan.add_acctunit(bob_str, 2, bob_debt_score)
    yao_plan.add_acctunit(sue_str, 2, sue_debt_score)
    yao_plan.add_acctunit(yao_str, 2, yao_debt_score)

    # WHEN
    yao_debtorledger = get_debtorledger(yao_plan)

    # THEN
    assert yao_debtorledger.get(bob_str) == bob_debt_score
    assert yao_debtorledger.get(sue_str) is None
    assert yao_debtorledger.get(yao_str) == yao_debt_score
    assert len(yao_debtorledger) == 2


def test_RiverRun_set_acct_tax_due_SetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    x_vow_mstr_dir = temp_vow_mstr_dir()
    bob_hubunit = hubunit_shop(x_vow_mstr_dir, None, bob_str)
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
    bob_debt_score = 38
    sue_debt_score = 56
    yao_debt_score = 6
    bob_plan = planunit_shop(bob_str)
    bob_plan.add_acctunit(bob_str, 2, bob_debt_score)
    bob_plan.add_acctunit(sue_str, 2, sue_debt_score)
    bob_plan.add_acctunit(yao_str, 2, yao_debt_score)
    bob_debtorledger = get_debtorledger(bob_plan)
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
    yao_debt_score = 6
    bob_debt_score = 38
    sue_debt_score = 56
    bob_plan = planunit_shop(bob_str)
    bob_plan.add_acctunit(bob_str, 2, bob_debt_score)
    bob_plan.add_acctunit(sue_str, 2, sue_debt_score)
    bob_plan.add_acctunit(yao_str, 2, yao_debt_score)
    bob_debtorledger = get_debtorledger(bob_plan)
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
    bob_debt_score = 38
    sue_debt_score = 56
    yao_debt_score = 6
    bob_plan = planunit_shop(bob_str)
    bob_plan.add_acctunit(bob_str, 2, bob_debt_score)
    bob_plan.add_acctunit(sue_str, 2, sue_debt_score)
    bob_plan.add_acctunit(yao_str, 2, yao_debt_score)
    bob_debtorledger = get_debtorledger(bob_plan)
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
    bob_debt_score = 38
    sue_debt_score = 56
    yao_debt_score = 6
    bob_plan = planunit_shop(bob_str)
    bob_plan.add_acctunit(bob_str, 2, bob_debt_score)
    bob_plan.add_acctunit(sue_str, 2, sue_debt_score)
    bob_plan.add_acctunit(yao_str, 2, yao_debt_score)
    bob_debtorledger = get_debtorledger(bob_plan)
    bob_riverrun.set_tax_dues(bob_debtorledger)
    assert bob_riverrun.get_acct_tax_due(bob_str) == 380, 0

    # WHEN / THEN
    excess_chargeer_points, tax_got = bob_riverrun.levy_tax_due(bob_str, 5)
    assert excess_chargeer_points == 0
    assert tax_got == 5
    assert bob_riverrun.get_acct_tax_due(bob_str) == 375

    # WHEN /THEN
    excess_chargeer_points, tax_got = bob_riverrun.levy_tax_due(bob_str, 375)
    assert excess_chargeer_points == 0
    assert tax_got == 375
    assert bob_riverrun.get_acct_tax_due(bob_str) == 0
    assert bob_riverrun.acct_has_tax_due(bob_str) is False

    # WHEN / THEN
    assert bob_riverrun.get_acct_tax_due(sue_str) == 560
    excess_chargeer_points, tax_got = bob_riverrun.levy_tax_due(sue_str, 1000)
    assert excess_chargeer_points == 440
    assert tax_got == 560
    assert bob_riverrun.get_acct_tax_due(sue_str) == 0
    assert bob_riverrun.tax_dues.get(sue_str) is None

    # WHEN / THEN
    zia_str = "Zia"
    excess_chargeer_points, tax_got = bob_riverrun.levy_tax_due(zia_str, 1000)
    assert excess_chargeer_points == 1000
    assert tax_got == 0
    assert bob_riverrun.get_acct_tax_due(zia_str) == 0

    # WHEN / THEN
    assert bob_riverrun.get_acct_tax_due(yao_str) == 60
    excess_chargeer_points, tax_got = bob_riverrun.levy_tax_due(yao_str, 81)
    assert excess_chargeer_points == 21
    assert tax_got == 60
    assert bob_riverrun.get_acct_tax_due(yao_str) == 0
