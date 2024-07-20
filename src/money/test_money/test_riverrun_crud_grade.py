from src.money.rivercycle import rivergrade_shop
from src.money.riverrun import riverrun_shop
from src.money.examples.example_credorledgers import example_yao_hubunit


def test_RiverRun_set_initial_rivergrade_SetsAttr():
    # ESTABLISH
    yao_hubunit = example_yao_hubunit()
    yao_number = 8
    yao_riverrun = riverrun_shop(yao_hubunit, yao_number)
    x_debtor_count = 5
    x_credor_count = 8
    yao_riverrun._debtor_count = x_debtor_count
    yao_riverrun._credor_count = x_credor_count
    bob_text = "Bob"
    assert yao_riverrun._rivergrades.get(bob_text) is None

    # WHEN
    yao_riverrun.set_initial_rivergrade(bob_text)

    # THEN
    bob_rivergrade = rivergrade_shop(
        yao_hubunit, bob_text, yao_number, x_debtor_count, x_credor_count
    )
    bob_rivergrade.grant_amount = 0
    assert yao_riverrun._rivergrades.get(bob_text) is not None
    gen_rivergrade = yao_riverrun._rivergrades.get(bob_text)
    assert gen_rivergrade.debtor_count == x_debtor_count
    assert gen_rivergrade.credor_count == x_credor_count
    assert gen_rivergrade == bob_rivergrade


def test_RiverRun_rivergrades_is_empty_ReturnsObj():
    # ESTABLISH
    yao_hubunit = example_yao_hubunit()
    yao_number = 8
    yao_riverrun = riverrun_shop(yao_hubunit, yao_number)

    assert yao_riverrun._rivergrades_is_empty()

    # WHEN
    bob_text = "Bob"
    yao_riverrun.set_initial_rivergrade(bob_text)

    # THEN
    assert yao_riverrun._rivergrades_is_empty() == False


def test_RiverRun_rivergrade_exists_ReturnsObj():
    # ESTABLISH
    yao_hubunit = example_yao_hubunit()
    yao_number = 8
    yao_riverrun = riverrun_shop(yao_hubunit, yao_number)
    yao_riverrun.set_initial_rivergrade("Yao")

    bob_text = "Bob"
    assert yao_riverrun.rivergrade_exists(bob_text) == False
    assert yao_riverrun._rivergrades_is_empty() == False

    # WHEN
    yao_riverrun.set_initial_rivergrade(bob_text)

    # THEN
    assert yao_riverrun.rivergrade_exists(bob_text)
    assert yao_riverrun._rivergrades_is_empty() == False


def test_RiverRun_set_all_initial_rivergrades_CorrectlySetsAttr():
    # ESTABLISH
    yao_hubunit = example_yao_hubunit()
    yao_text = "Yao"
    bob_text = "Bob"
    sue_text = "Sue"
    zia_text = "Zia"
    xio_text = "Xio"
    x_riverrun = riverrun_shop(yao_hubunit)
    x_riverrun.set_econ_credorledger(yao_text, yao_text, 1)
    x_riverrun.set_econ_credorledger(yao_text, bob_text, 1)
    x_riverrun.set_econ_credorledger(zia_text, bob_text, 1)
    x_riverrun.set_econ_credorledger(xio_text, sue_text, 1)
    all_accts_ids = x_riverrun.get_all_econ_credorledger_acct_ids()
    assert all_accts_ids == {yao_text, bob_text, zia_text, xio_text, sue_text}
    assert x_riverrun._rivergrades_is_empty()
    assert x_riverrun.rivergrade_exists(yao_text) == False
    assert x_riverrun.rivergrade_exists(bob_text) == False
    assert x_riverrun.rivergrade_exists(zia_text) == False

    # WHEN
    x_riverrun.set_all_initial_rivergrades()

    # THEN
    assert x_riverrun._rivergrades_is_empty() == False
    assert x_riverrun.rivergrade_exists(yao_text)
    assert x_riverrun.rivergrade_exists(bob_text)
    assert x_riverrun.rivergrade_exists(zia_text)


def test_RiverRun_set_all_initial_rivergrades_CorrectlyOverWritesPrevious():
    # ESTABLISH
    yao_hubunit = example_yao_hubunit()
    yao_text = "Yao"
    bob_text = "Bob"
    sue_text = "Sue"
    zia_text = "Zia"
    xio_text = "Xio"
    x_riverrun = riverrun_shop(yao_hubunit)
    x_riverrun.set_econ_credorledger(yao_text, yao_text, 1)
    x_riverrun.set_econ_credorledger(yao_text, bob_text, 1)
    x_riverrun.set_econ_credorledger(zia_text, bob_text, 1)
    x_riverrun.set_econ_credorledger(xio_text, sue_text, 1)
    x_riverrun.set_all_initial_rivergrades()
    assert x_riverrun.rivergrade_exists(yao_text)
    assert x_riverrun.rivergrade_exists(bob_text)
    assert x_riverrun.rivergrade_exists(zia_text)
    assert x_riverrun.rivergrade_exists(xio_text)
    assert x_riverrun.rivergrade_exists(sue_text)

    # WHEN
    x_riverrun.delete_econ_credorledgers_owner(xio_text)
    x_riverrun.set_all_initial_rivergrades()

    # THEN
    assert x_riverrun.rivergrade_exists(yao_text)
    assert x_riverrun.rivergrade_exists(bob_text)
    assert x_riverrun.rivergrade_exists(zia_text)
    assert x_riverrun.rivergrade_exists(xio_text) == False
    assert x_riverrun.rivergrade_exists(sue_text) == False
