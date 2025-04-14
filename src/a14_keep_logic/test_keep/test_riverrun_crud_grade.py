from src.a14_keep_logic.rivercycle import rivergrade_shop
from src.a14_keep_logic.riverrun import riverrun_shop
from src.a14_keep_logic.examples.example_credorledgers import example_yao_hubunit


def test_RiverRun_set_initial_rivergrade_SetsAttr():
    # ESTABLISH
    yao_hubunit = example_yao_hubunit()
    yao_number = 8
    yao_riverrun = riverrun_shop(yao_hubunit, yao_number)
    x_debtor_count = 5
    x_credor_count = 8
    yao_riverrun._debtor_count = x_debtor_count
    yao_riverrun._credor_count = x_credor_count
    bob_str = "Bob"
    assert yao_riverrun._rivergrades.get(bob_str) is None

    # WHEN
    yao_riverrun.set_initial_rivergrade(bob_str)

    # THEN
    bob_rivergrade = rivergrade_shop(
        yao_hubunit, bob_str, yao_number, x_debtor_count, x_credor_count
    )
    bob_rivergrade.grant_amount = 0
    assert yao_riverrun._rivergrades.get(bob_str) is not None
    gen_rivergrade = yao_riverrun._rivergrades.get(bob_str)
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
    bob_str = "Bob"
    yao_riverrun.set_initial_rivergrade(bob_str)

    # THEN
    assert yao_riverrun._rivergrades_is_empty() is False


def test_RiverRun_rivergrade_exists_ReturnsObj():
    # ESTABLISH
    yao_hubunit = example_yao_hubunit()
    yao_number = 8
    yao_riverrun = riverrun_shop(yao_hubunit, yao_number)
    yao_riverrun.set_initial_rivergrade("Yao")

    bob_str = "Bob"
    assert yao_riverrun.rivergrade_exists(bob_str) is False
    assert yao_riverrun._rivergrades_is_empty() is False

    # WHEN
    yao_riverrun.set_initial_rivergrade(bob_str)

    # THEN
    assert yao_riverrun.rivergrade_exists(bob_str)
    assert yao_riverrun._rivergrades_is_empty() is False


def test_RiverRun_set_all_initial_rivergrades_CorrectlySetsAttr():
    # ESTABLISH
    yao_hubunit = example_yao_hubunit()
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    zia_str = "Zia"
    xio_str = "Xio"
    x_riverrun = riverrun_shop(yao_hubunit)
    x_riverrun.set_keep_credorledger(yao_str, yao_str, 1)
    x_riverrun.set_keep_credorledger(yao_str, bob_str, 1)
    x_riverrun.set_keep_credorledger(zia_str, bob_str, 1)
    x_riverrun.set_keep_credorledger(xio_str, sue_str, 1)
    all_accts_ids = x_riverrun.get_all_keep_credorledger_acct_names()
    assert all_accts_ids == {yao_str, bob_str, zia_str, xio_str, sue_str}
    assert x_riverrun._rivergrades_is_empty()
    assert x_riverrun.rivergrade_exists(yao_str) is False
    assert x_riverrun.rivergrade_exists(bob_str) is False
    assert x_riverrun.rivergrade_exists(zia_str) is False

    # WHEN
    x_riverrun.set_all_initial_rivergrades()

    # THEN
    assert x_riverrun._rivergrades_is_empty() is False
    assert x_riverrun.rivergrade_exists(yao_str)
    assert x_riverrun.rivergrade_exists(bob_str)
    assert x_riverrun.rivergrade_exists(zia_str)


def test_RiverRun_set_all_initial_rivergrades_CorrectlyOverWritesPrevious():
    # ESTABLISH
    yao_hubunit = example_yao_hubunit()
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    zia_str = "Zia"
    xio_str = "Xio"
    x_riverrun = riverrun_shop(yao_hubunit)
    x_riverrun.set_keep_credorledger(yao_str, yao_str, 1)
    x_riverrun.set_keep_credorledger(yao_str, bob_str, 1)
    x_riverrun.set_keep_credorledger(zia_str, bob_str, 1)
    x_riverrun.set_keep_credorledger(xio_str, sue_str, 1)
    x_riverrun.set_all_initial_rivergrades()
    assert x_riverrun.rivergrade_exists(yao_str)
    assert x_riverrun.rivergrade_exists(bob_str)
    assert x_riverrun.rivergrade_exists(zia_str)
    assert x_riverrun.rivergrade_exists(xio_str)
    assert x_riverrun.rivergrade_exists(sue_str)

    # WHEN
    x_riverrun.delete_keep_credorledgers_owner(xio_str)
    x_riverrun.set_all_initial_rivergrades()

    # THEN
    assert x_riverrun.rivergrade_exists(yao_str)
    assert x_riverrun.rivergrade_exists(bob_str)
    assert x_riverrun.rivergrade_exists(zia_str)
    assert x_riverrun.rivergrade_exists(xio_str) is False
    assert x_riverrun.rivergrade_exists(sue_str) is False
