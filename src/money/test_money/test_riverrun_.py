from src.money.examples.example_credorledgers import (
    example_yao_bob_zia_credorledgers,
    example_yao_bob_zia_tax_dues,
    example_yao_hubunit,
)
from src.money.riverrun import RiverRun, riverrun_shop


def test_RiverRun_Exists():
    # ESTABLISH / WHEN
    x_riverrun = RiverRun()

    # THEN
    assert x_riverrun.hubunit is None
    assert x_riverrun.number is None
    assert x_riverrun.econ_credorledgers is None
    assert x_riverrun.tax_dues is None
    assert x_riverrun.cycle_max is None
    # calculated fields
    assert x_riverrun._rivergrades is None
    assert x_riverrun._grants is None
    assert x_riverrun._tax_yields is None
    assert x_riverrun._tax_got_prev is None
    assert x_riverrun._tax_got_curr is None
    assert x_riverrun._cycle_count is None
    assert x_riverrun._cycle_payees_prev is None
    assert x_riverrun._cycle_payees_curr is None
    assert x_riverrun._debtor_count is None
    assert x_riverrun._credor_count is None


def test_RiverRun_set_cycle_max_CorrectlySetsAttr():
    # ESTABLISH
    x_riverrun = RiverRun()
    assert x_riverrun.cycle_max is None

    # WHEN / THEN
    x_riverrun.set_cycle_max(10)
    assert x_riverrun.cycle_max == 10

    # WHEN / THEN
    x_riverrun.set_cycle_max(10.0)
    assert x_riverrun.cycle_max == 10

    # WHEN / THEN
    x_riverrun.set_cycle_max(-10.0)
    assert x_riverrun.cycle_max == 0

    # WHEN / THEN
    x_riverrun.set_cycle_max(10.8)
    assert x_riverrun.cycle_max == 10


def test_riverrun_shop_ReturnsCorrectObjWithArg():
    # ESTABLISH
    ten_int = 10
    yao_hubunit = example_yao_hubunit()
    econ_credorledgers = example_yao_bob_zia_credorledgers()
    x_cycle_max = 10
    x_tax_dues = example_yao_bob_zia_tax_dues()

    # WHEN
    x_riverrun = riverrun_shop(
        hubunit=yao_hubunit,
        number=ten_int,
        econ_credorledgers=econ_credorledgers,
        tax_dues=x_tax_dues,
        cycle_max=x_cycle_max,
    )

    # THEN
    assert x_riverrun.hubunit == yao_hubunit
    assert x_riverrun.number == ten_int
    assert x_riverrun.econ_credorledgers == econ_credorledgers
    assert x_riverrun.tax_dues == x_tax_dues
    assert x_riverrun.cycle_max == x_cycle_max
    assert x_riverrun._rivergrades == {}
    assert x_riverrun._grants == {}
    assert x_riverrun._tax_yields == {}
    assert x_riverrun._tax_got_prev == 0
    assert x_riverrun._tax_got_curr == 0
    assert x_riverrun._cycle_count == 0
    assert x_riverrun._cycle_payees_prev == set()
    assert x_riverrun._cycle_payees_curr == set()


def test_riverrun_shop_ReturnsCorrectObjWithoutArgs():
    # ESTABLISH
    yao_hubunit = example_yao_hubunit()

    # WHEN
    x_riverrun = riverrun_shop(hubunit=yao_hubunit)

    # THEN
    assert x_riverrun.hubunit == yao_hubunit
    assert x_riverrun.number == 0
    assert x_riverrun.econ_credorledgers == {}
    assert x_riverrun.tax_dues == {}
    assert x_riverrun._rivergrades == {}
    assert x_riverrun._grants == {}
    assert x_riverrun._tax_yields == {}
    assert x_riverrun._cycle_count == 0
    assert x_riverrun.cycle_max == 10


def test_RiverRun_set_econ_credorledger_SetsAttr():
    # ESTABLISH
    yao_hubunit = example_yao_hubunit()
    yao_str = "Yao"
    yao_credit_belief = 500
    x_riverrun = riverrun_shop(yao_hubunit)
    assert x_riverrun.econ_credorledgers == {}

    # WHEN
    x_riverrun.set_econ_credorledger(
        owner_id=yao_str, acct_id=yao_str, acct_credit_belief=yao_credit_belief
    )

    # THEN
    assert x_riverrun.econ_credorledgers == {yao_str: {yao_str: yao_credit_belief}}


def test_RiverRun_delete_econ_credorledgers_owner_SetsAttr():
    # ESTABLISH
    yao_hubunit = example_yao_hubunit()
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    x_riverrun = riverrun_shop(yao_hubunit)
    x_riverrun.set_econ_credorledger(yao_str, yao_str, 1)
    x_riverrun.set_econ_credorledger(bob_str, bob_str, 1)
    x_riverrun.set_econ_credorledger(bob_str, sue_str, 1)
    assert x_riverrun.econ_credorledgers == {
        yao_str: {yao_str: 1},
        bob_str: {bob_str: 1, sue_str: 1},
    }

    # WHEN
    x_riverrun.delete_econ_credorledgers_owner(bob_str)

    # THEN
    assert x_riverrun.econ_credorledgers == {yao_str: {yao_str: 1}}


def test_RiverRun_get_all_econ_credorledger_acct_ids_ReturnsCorrectObj():
    # ESTABLISH
    yao_hubunit = example_yao_hubunit()
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    zia_str = "Zia"
    xio_str = "Xio"
    x_riverrun = riverrun_shop(yao_hubunit)

    # WHEN
    all_accts_ids = x_riverrun.get_all_econ_credorledger_acct_ids()
    # THEN
    assert all_accts_ids == set()

    # WHEN
    x_riverrun.set_econ_credorledger(yao_str, yao_str, 1)
    x_riverrun.set_econ_credorledger(yao_str, bob_str, 1)
    all_accts_ids = x_riverrun.get_all_econ_credorledger_acct_ids()
    # THEN
    assert all_accts_ids == {yao_str, bob_str}

    # WHEN
    x_riverrun.set_econ_credorledger(zia_str, bob_str, 1)
    all_accts_ids = x_riverrun.get_all_econ_credorledger_acct_ids()
    # THEN
    assert all_accts_ids == {yao_str, bob_str, zia_str}

    # WHEN
    x_riverrun.set_econ_credorledger(xio_str, sue_str, 1)
    all_accts_ids = x_riverrun.get_all_econ_credorledger_acct_ids()
    # THEN
    assert all_accts_ids == {yao_str, bob_str, zia_str, xio_str, sue_str}
