from src.a02_finance_toolboxs.deal import tranbook_shop, tranunit_shop
from src.a15_fisc_logic.fisc import fiscunit_shop
from pytest import raises as pytest_raises


def test_FiscUnit_set_cashpurchase_SetsAttr():
    # ESTABLISH
    t6606_offi_time_max = 6606
    x_fisc = fiscunit_shop("accord23")
    x_fisc._offi_time_max = t6606_offi_time_max
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_amount = 37
    sue_bob_t55_tranunit = tranunit_shop(sue_str, bob_str, t55_t, t55_amount)
    assert x_fisc.cashbook.tranunit_exists(sue_str, bob_str, t55_t) is False

    # WHEN
    x_fisc.set_cashpurchase(sue_bob_t55_tranunit)

    # THEN
    assert x_fisc.cashbook.tranunit_exists(sue_str, bob_str, t55_t)


def test_FiscUnit_add_cashpurchase_SetsAttr():
    # ESTABLISH
    t6606_offi_time_max = 6606
    x_fisc = fiscunit_shop("accord23")
    x_fisc._offi_time_max = t6606_offi_time_max
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_amount = 37
    assert x_fisc.cashbook.tranunit_exists(sue_str, bob_str, t55_t) is False

    # WHEN
    x_fisc.add_cashpurchase(sue_str, bob_str, tran_time=t55_t, amount=t55_amount)

    # THEN
    assert x_fisc.cashbook.tranunit_exists(sue_str, bob_str, t55_t)


def test_FiscUnit_set_cashpurchase_RaisesErrorWhen_tranunit_tran_time_GreaterThanOrEqual_offi_time_max():
    # ESTABLISH
    t6606_offi_time_max = 6606
    x_fisc = fiscunit_shop("accord23")
    x_fisc._offi_time_max = t6606_offi_time_max
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_amount = 37
    sue_bob_t55_tranunit = tranunit_shop(sue_str, bob_str, t55_t, t55_amount)
    assert x_fisc._offi_time_max == t6606_offi_time_max
    assert sue_bob_t55_tranunit.tran_time == t55_t
    assert sue_bob_t55_tranunit.tran_time < x_fisc._offi_time_max

    # WHEN
    x_fisc.set_cashpurchase(sue_bob_t55_tranunit)
    # THEN
    assert x_fisc.cashbook.tranunit_exists(sue_str, bob_str, t55_t)

    # ESTABLISH
    t77_t = 7707
    t77_amount = 30
    sue_bob_t77_tranunit = tranunit_shop(sue_str, bob_str, t77_t, t77_amount)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_fisc.set_cashpurchase(sue_bob_t77_tranunit)
    exception_str = f"Cannot set tranunit for tran_time={t77_t}, timelinepoint is greater than current time={t6606_offi_time_max}"
    assert str(excinfo.value) == exception_str

    # WHEN / THEN
    sue_bob_t6606 = tranunit_shop(sue_str, bob_str, t6606_offi_time_max, t77_amount)
    with pytest_raises(Exception) as excinfo:
        x_fisc.set_cashpurchase(sue_bob_t6606)
    exception_str = f"Cannot set tranunit for tran_time={t6606_offi_time_max}, timelinepoint is greater than current time={t6606_offi_time_max}"
    assert str(excinfo.value) == exception_str


def test_FiscUnit_set_cashpurchase_RaisesErrorWhenDealUnitHas_tran_time():
    # ESTABLISH
    x_fisc = fiscunit_shop("accord23")
    x_fisc._offi_time_max = 0
    x_fisc._offi_time_max = 0
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_quota = 100
    x_fisc.add_dealunit("yao", t55_t, t55_quota)
    t55_amount = 37
    t6606_offi_time_max = 6606
    x_fisc._offi_time_max = t6606_offi_time_max
    sue_bob_t55_tranunit = tranunit_shop(sue_str, bob_str, t55_t, t55_amount)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_fisc.set_cashpurchase(sue_bob_t55_tranunit)
    exception_str = (
        f"Cannot set tranunit for tran_time={t55_t}, timelinepoint is blocked"
    )
    assert str(excinfo.value) == exception_str


def test_FiscUnit_cashpurchase_exists_ReturnsObj():
    # ESTABLISH
    x_fisc = fiscunit_shop("accord23")
    x_fisc._offi_time_max = 6606
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    assert x_fisc.cashpurchase_exists(sue_str, bob_str, t55_t) is False

    # WHEN
    t55_amount = 37
    x_fisc.set_cashpurchase(tranunit_shop(sue_str, bob_str, t55_t, t55_amount))

    # THEN
    assert x_fisc.cashpurchase_exists(sue_str, bob_str, t55_t)


def test_FiscUnit_get_cashpurchase_ReturnsObj():
    # ESTABLISH
    x_fisc = fiscunit_shop("accord23")
    x_fisc._offi_time_max = 6606
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_amount = 37
    x_fisc.set_cashpurchase(tranunit_shop(sue_str, bob_str, t55_t, t55_amount))
    assert x_fisc.cashpurchase_exists(sue_str, bob_str, t55_t)

    # WHEN
    sue_gen_cashpurchase = x_fisc.get_cashpurchase(sue_str, bob_str, t55_t)

    # THEN
    assert sue_gen_cashpurchase
    sue_bob_t55_tranunit = tranunit_shop(sue_str, bob_str, t55_t, t55_amount)
    assert sue_gen_cashpurchase == sue_bob_t55_tranunit


def test_FiscUnit_del_cashpurchase_SetsAttr():
    # ESTABLISH
    x_fisc = fiscunit_shop("accord23")
    x_fisc._offi_time_max = 6606
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_amount = 37
    x_fisc.set_cashpurchase(tranunit_shop(sue_str, bob_str, t55_t, t55_amount))
    assert x_fisc.cashpurchase_exists(sue_str, bob_str, t55_t)

    # WHEN
    x_fisc.del_cashpurchase(sue_str, bob_str, t55_t)

    # THEN
    assert x_fisc.cashpurchase_exists(sue_str, bob_str, t55_t) is False


def test_FiscUnit_set_offi_time_max_SetsAttr():
    # ESTABLISH
    t6606_offi_time_max = 6606
    x_fisc = fiscunit_shop("accord23")
    x_fisc._offi_time_max = t6606_offi_time_max
    sue_str = "Sue"
    bob_str = "Bob"
    t22_t = 2202
    t22_amount = 27
    x_fisc.set_cashpurchase(tranunit_shop(sue_str, bob_str, t22_t, t22_amount))
    assert x_fisc._offi_time_max == t6606_offi_time_max

    # WHEN
    t4404_offi_time_max = 4404
    x_fisc.set_offi_time_max(t4404_offi_time_max)

    # THEN
    assert x_fisc._offi_time_max == t4404_offi_time_max


def test_FiscUnit_set_offi_time_max_RaisesErrorWhen_cashpurchase_ExistsWithGreatertran_time():
    # ESTABLISH
    t6606_offi_time_max = 6606
    x_fisc = fiscunit_shop("accord23")
    x_fisc._offi_time_max = t6606_offi_time_max
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_amount = 37
    x_fisc.set_cashpurchase(tranunit_shop(sue_str, bob_str, t55_t, t55_amount))
    assert x_fisc._offi_time_max == t6606_offi_time_max

    # WHEN / THEN
    t4404_offi_time_max = 4404
    with pytest_raises(Exception) as excinfo:
        x_fisc.set_offi_time_max(t4404_offi_time_max)
    exception_str = f"Cannot set _offi_time_max {t4404_offi_time_max}, cashpurchase with greater tran_time exists"
    assert str(excinfo.value) == exception_str

    # THEN
    assert x_fisc._offi_time_max == t6606_offi_time_max


def test_FiscUnit_set_all_tranbook_SetsAttr():
    # ESTABLISH
    x_fisc = fiscunit_shop("accord23")
    x_fisc._offi_time_max = 10101
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    t55_t = 5505
    t66_t = 6606
    t77_t = 7707
    t88_t = 8808
    t99_t = 9909
    t55_amount = 50
    t66_amount = 60
    t77_amount = 70
    t88_amount = 80
    t99_amount = 90
    t55_tranunit = tranunit_shop(sue_str, bob_str, t55_t, t55_amount)
    t66_tranunit = tranunit_shop(yao_str, bob_str, t66_t, t66_amount)
    t77_tranunit = tranunit_shop(yao_str, sue_str, t77_t, t77_amount)
    t88_tranunit = tranunit_shop(sue_str, yao_str, t88_t, t88_amount)
    t99_tranunit = tranunit_shop(bob_str, sue_str, t99_t, t99_amount)
    x_fisc.set_cashpurchase(t55_tranunit)
    x_fisc.set_cashpurchase(t66_tranunit)
    x_fisc.set_cashpurchase(t77_tranunit)
    x_fisc.set_cashpurchase(t88_tranunit)
    x_fisc.set_cashpurchase(t99_tranunit)

    x40000_tran_time = 40000
    x70000_tran_time = 70000
    x_fisc.add_dealunit(sue_str, x40000_tran_time, 1)
    x_fisc.add_dealunit(sue_str, x70000_tran_time, 1)
    bob_str = "Bob"
    zia_str = "Zia"
    zia_deal_net = 887
    bob_deal_net = 445
    sue_x40000_deal = x_fisc.get_brokerunit(sue_str).get_deal(x40000_tran_time)
    sue_x70000_deal = x_fisc.get_brokerunit(sue_str).get_deal(x70000_tran_time)
    sue_x40000_deal.set_deal_acct_net(bob_str, bob_deal_net)
    sue_x70000_deal.set_deal_acct_net(zia_str, zia_deal_net)

    assert x_fisc._all_tranbook == tranbook_shop(x_fisc.fisc_title)
    assert x_fisc.cashpurchase_exists(sue_str, bob_str, t55_t)
    assert x_fisc.cashpurchase_exists(yao_str, bob_str, t66_t)
    assert x_fisc.cashpurchase_exists(yao_str, sue_str, t77_t)
    assert x_fisc.cashpurchase_exists(sue_str, yao_str, t88_t)
    assert x_fisc.cashpurchase_exists(bob_str, sue_str, t99_t)

    assert sue_x40000_deal.deal_acct_net_exists(bob_str)
    assert sue_x70000_deal.deal_acct_net_exists(zia_str)
    # x_fisc.add_dealunit()

    # WHEN
    x_fisc.set_all_tranbook()

    # THEN
    assert x_fisc._all_tranbook.tranunit_exists(sue_str, bob_str, t55_t)
    assert x_fisc._all_tranbook.tranunit_exists(yao_str, bob_str, t66_t)
    assert x_fisc._all_tranbook.tranunit_exists(yao_str, sue_str, t77_t)
    assert x_fisc._all_tranbook.tranunit_exists(sue_str, yao_str, t88_t)
    assert x_fisc._all_tranbook.tranunit_exists(bob_str, sue_str, t99_t)
    assert x_fisc._all_tranbook.tranunit_exists(sue_str, bob_str, x40000_tran_time)
    assert x_fisc._all_tranbook.tranunit_exists(sue_str, zia_str, x70000_tran_time)
