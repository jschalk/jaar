from src.a14_keep_logic._test_util.example_credorledgers import example_yao_hubunit
from src.a14_keep_logic.riverrun import riverrun_shop


def test_RiverRun_calc_metrics_SetsAttrsScenario01():
    # ESTABLISH / WHEN
    yao_hubunit = example_yao_hubunit()
    yao_str = "Yao"
    yao_credit_belief = 500
    x_riverrun = riverrun_shop(yao_hubunit)
    x_riverrun.set_keep_credorledger(yao_str, yao_str, yao_credit_belief)
    assert x_riverrun.get_acct_tax_due(yao_str) == 0

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_acct_tax_due(yao_str) == 0
    assert x_riverrun._cycle_count == 1
    assert x_riverrun._debtor_count == 0
    assert x_riverrun._credor_count == 1
    yao_rivergrade = x_riverrun.get_rivergrade(yao_str)
    assert yao_rivergrade is not None
    assert yao_rivergrade.hubunit == yao_hubunit
    assert yao_rivergrade.number == 0
    assert yao_rivergrade.grant_amount == yao_hubunit.keep_point_magnitude
    assert yao_rivergrade.tax_bill_amount == 0
    assert yao_rivergrade.tax_paid_amount == 0
    assert yao_rivergrade.tax_paid_bool
    # assert yao_rivergrade.tax_paid_rank_num == 1
    # assert yao_rivergrade.tax_paid_rank_percent == 1.0
    # assert yao_rivergrade.debtor_rank_num is None
    # assert yao_rivergrade.credor_rank_num == 1
    # assert yao_rivergrade.debtor_rank_percent == 1.0
    # assert yao_rivergrade.debtor_count == 0
    # assert yao_rivergrade.credor_count == 1
    # assert yao_rivergrade.credor_rank_percent == 1.0
    # assert yao_rivergrade.rewards_count == 1
    # assert yao_rivergrade.rewards_magnitude == 500


def test_RiverRun_calc_metrics_SetsAttrsScenario02():
    # ESTABLISH / WHEN
    yao_hubunit = example_yao_hubunit()
    yao_str = "Yao"
    yao_credit_belief = 500
    bob_str = "Bob"
    bob_debtit_belief = 350
    x_riverrun = riverrun_shop(yao_hubunit)
    x_riverrun.set_keep_credorledger(yao_str, yao_str, yao_credit_belief)
    x_riverrun.set_tax_dues({bob_str: bob_debtit_belief})
    assert x_riverrun.get_acct_tax_due(yao_str) == 0
    keep_money_amount = x_riverrun.hubunit.keep_point_magnitude
    assert x_riverrun.get_acct_tax_due(bob_str) == keep_money_amount

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_acct_tax_due(yao_str) == 0
    assert x_riverrun.get_acct_tax_due(bob_str) == keep_money_amount
    assert x_riverrun._cycle_count == 1
    assert x_riverrun._debtor_count == 1
    assert x_riverrun._credor_count == 1
    yao_rivergrade = x_riverrun.get_rivergrade(yao_str)
    assert yao_rivergrade is not None
    assert yao_rivergrade.hubunit == yao_hubunit
    assert yao_rivergrade.number == 0
    assert yao_rivergrade.grant_amount == yao_hubunit.keep_point_magnitude
    assert yao_rivergrade.tax_bill_amount == 0
    assert yao_rivergrade.tax_paid_amount == 0
    assert yao_rivergrade.tax_paid_bool
    # assert yao_rivergrade.tax_paid_rank_num == 1
    # assert yao_rivergrade.tax_paid_rank_percent == 1.0
    # assert yao_rivergrade.debtor_rank_num is None
    # assert yao_rivergrade.credor_rank_num == 1
    # assert yao_rivergrade.debtor_rank_percent == 1.0
    # assert yao_rivergrade.debtor_count == 0
    # assert yao_rivergrade.credor_count == 1
    # assert yao_rivergrade.credor_rank_percent == 1.0
    # assert yao_rivergrade.rewards_count == 1
    # assert yao_rivergrade.rewards_magnitude == 500


def test_RiverRun_calc_metrics_SetsAttrsScenario03():
    # ESTABLISH / WHEN
    yao_hubunit = example_yao_hubunit()
    yao_str = "Yao"
    yao_credit_belief = 500
    bob_str = "Bob"
    bob_debtit_belief = 25
    sue_str = "Sue"
    sue_debtit_belief = 75
    x_riverrun = riverrun_shop(yao_hubunit)
    x_riverrun.set_keep_credorledger(yao_str, yao_str, yao_credit_belief)
    debtorledger = {bob_str: bob_debtit_belief, sue_str: sue_debtit_belief}
    x_riverrun.set_tax_dues(debtorledger)
    assert x_riverrun.get_acct_tax_due(yao_str) == 0
    keep_money_amount = x_riverrun.hubunit.keep_point_magnitude
    assert x_riverrun.get_acct_tax_due(bob_str) == keep_money_amount * 0.25
    assert x_riverrun.get_acct_tax_due(sue_str) == keep_money_amount * 0.75

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_acct_tax_due(yao_str) == 0
    assert x_riverrun.get_acct_tax_due(bob_str) == keep_money_amount * 0.25
    assert x_riverrun.get_acct_tax_due(sue_str) == keep_money_amount * 0.75
    assert x_riverrun._cycle_count == 1
    assert x_riverrun._debtor_count == 2
    assert x_riverrun._credor_count == 1
    yao_rivergrade = x_riverrun.get_rivergrade(yao_str)
    assert yao_rivergrade is not None
    assert yao_rivergrade.hubunit == yao_hubunit
    assert yao_rivergrade.number == 0
    assert yao_rivergrade.grant_amount == yao_hubunit.keep_point_magnitude
    assert yao_rivergrade.tax_bill_amount == 0
    assert yao_rivergrade.tax_paid_amount == 0
    assert yao_rivergrade.tax_paid_bool
    # assert yao_rivergrade.tax_paid_rank_num == 1
    # assert yao_rivergrade.tax_paid_rank_percent == 1.0
    # assert yao_rivergrade.debtor_rank_num is None
    # assert yao_rivergrade.credor_rank_num == 1
    # assert yao_rivergrade.debtor_rank_percent == 1.0
    # assert yao_rivergrade.debtor_count == 0
    # assert yao_rivergrade.credor_count == 1
    # assert yao_rivergrade.credor_rank_percent == 1.0
    # assert yao_rivergrade.rewards_count == 1
    # assert yao_rivergrade.rewards_magnitude == 500


def test_RiverRun_calc_metrics_SetsAttrsScenario04():
    # ESTABLISH / WHEN
    yao_hubunit = example_yao_hubunit()
    yao_str = "Yao"
    yao_yao_credit_belief = 500
    yao_sue_credit_belief = 2000
    bob_str = "Bob"
    bob_debtit_belief = 25
    sue_str = "Sue"
    sue_debtit_belief = 75
    x_riverrun = riverrun_shop(yao_hubunit)
    x_riverrun.set_keep_credorledger(yao_str, yao_str, yao_yao_credit_belief)
    x_riverrun.set_keep_credorledger(yao_str, sue_str, yao_sue_credit_belief)
    debtorledger = {bob_str: bob_debtit_belief, sue_str: sue_debtit_belief}
    x_riverrun.set_tax_dues(debtorledger)
    assert x_riverrun.get_acct_tax_due(yao_str) == 0
    keep_money_amount = x_riverrun.hubunit.keep_point_magnitude
    assert x_riverrun.get_acct_tax_due(bob_str) == keep_money_amount * 0.25
    assert x_riverrun.get_acct_tax_due(sue_str) == keep_money_amount * 0.75

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_acct_tax_due(yao_str) == 0
    assert x_riverrun.get_acct_tax_due(bob_str) == keep_money_amount * 0.25
    assert x_riverrun.get_acct_tax_due(sue_str) == 0
    assert x_riverrun.get_acct_tax_yield(sue_str) == keep_money_amount * 0.75
    assert x_riverrun._cycle_count == 2
    assert x_riverrun._debtor_count == 2
    assert x_riverrun._credor_count == 2
    yao_rivergrade = x_riverrun.get_rivergrade(yao_str)
    sue_rivergrade = x_riverrun.get_rivergrade(sue_str)
    assert yao_rivergrade.grant_amount == yao_hubunit.keep_point_magnitude * 0.2
    assert sue_rivergrade.grant_amount == yao_hubunit.keep_point_magnitude * 0.8
    assert yao_rivergrade.tax_bill_amount == 0
    assert yao_rivergrade.tax_paid_amount == 0
    assert yao_rivergrade.tax_paid_bool
    # assert yao_rivergrade.tax_paid_rank_num == 1
    # assert yao_rivergrade.tax_paid_rank_percent == 1.0
    # assert yao_rivergrade.debtor_rank_num is None
    # assert yao_rivergrade.credor_rank_num == 1
    # assert yao_rivergrade.debtor_rank_percent == 1.0
    # assert yao_rivergrade.debtor_count == 0
    # assert yao_rivergrade.credor_count == 1
    # assert yao_rivergrade.credor_rank_percent == 1.0
    # assert yao_rivergrade.rewards_count == 1
    # assert yao_rivergrade.rewards_magnitude == 500


def test_RiverRun_calc_metrics_SetsAttrsScenario05():
    # ESTABLISH / WHEN
    yao_hubunit = example_yao_hubunit()
    yao_str = "Yao"
    yao_credit_belief = 500
    x_riverrun = riverrun_shop(yao_hubunit)
    x_riverrun.set_keep_credorledger(yao_str, yao_str, yao_credit_belief)
    x_riverrun.set_tax_dues({yao_str: 1})
    keep_money_amount = yao_hubunit.keep_point_magnitude
    assert x_riverrun.get_acct_tax_due(yao_str) == keep_money_amount
    assert x_riverrun.get_acct_tax_yield(yao_str) == 0

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_acct_tax_due(yao_str) == 0
    assert x_riverrun.get_acct_tax_yield(yao_str) == keep_money_amount
    assert x_riverrun._cycle_count == 2
    assert x_riverrun._debtor_count == 1
    assert x_riverrun._credor_count == 1
    yao_rivergrade = x_riverrun.get_rivergrade(yao_str)
    assert yao_rivergrade is not None
    assert yao_rivergrade.hubunit == yao_hubunit
    assert yao_rivergrade.number == 0
    assert yao_rivergrade.grant_amount == keep_money_amount
    assert yao_rivergrade.tax_bill_amount == keep_money_amount
    assert yao_rivergrade.tax_paid_amount == keep_money_amount
    assert yao_rivergrade.tax_paid_bool


def test_RiverRun_calc_metrics_EachTimeResets_tax_yield():
    # ESTABLISH / WHEN
    yao_hubunit = example_yao_hubunit()
    yao_str = "Yao"
    yao_credit_belief = 500
    x_riverrun = riverrun_shop(yao_hubunit)
    x_riverrun.set_keep_credorledger(yao_str, yao_str, yao_credit_belief)
    x_riverrun.set_tax_dues({yao_str: 1})
    keep_money_amount = yao_hubunit.keep_point_magnitude
    x_riverrun.calc_metrics()
    assert x_riverrun.get_acct_tax_due(yao_str) == 0
    assert x_riverrun.get_acct_tax_yield(yao_str) == keep_money_amount

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_acct_tax_due(yao_str) == 0
    assert x_riverrun.get_acct_tax_yield(yao_str) == keep_money_amount


def test_RiverRun_calc_metrics_EndsRiverCycleLoopIfNoDifferencesBetweenCycles():
    # ESTABLISH / WHEN
    x_riverrun = riverrun_shop(example_yao_hubunit())
    yao_str = "Yao"
    bob_str = "Bob"
    x_riverrun.set_keep_credorledger(yao_str, yao_str, 1)
    x_riverrun.set_tax_dues({bob_str: 1})
    keep_money_amount = x_riverrun.hubunit.keep_point_magnitude
    assert x_riverrun.get_acct_tax_due(yao_str) == 0
    assert x_riverrun.get_acct_tax_due(bob_str) == keep_money_amount
    assert x_riverrun._cycle_count == 0
    assert x_riverrun._cycle_payees_prev == set()
    assert x_riverrun._cycle_payees_curr == set()

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun._cycle_payees_prev == {yao_str}
    assert x_riverrun._cycle_payees_curr == {yao_str}
    assert x_riverrun.get_acct_tax_due(yao_str) == 0
    assert x_riverrun.get_acct_tax_due(bob_str) == keep_money_amount
    assert x_riverrun._cycle_count == 1
