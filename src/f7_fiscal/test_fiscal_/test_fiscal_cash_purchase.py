from src.f1_road.finance_tran import tranbook_shop, tranunit_shop
from src.f7_fiscal.fiscal import fiscalunit_shop
from pytest import raises as pytest_raises


def test_FiscalUnit_set_cashpurchase_SetsAttr():
    # ESTABLISH
    t6606_current_time = 6606
    x_fiscal = fiscalunit_shop(current_time=t6606_current_time)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_amount = 37
    sue_bob_t55_tranunit = tranunit_shop(sue_str, bob_str, t55_t, t55_amount)
    assert x_fiscal.cashbook.tranunit_exists(sue_str, bob_str, t55_t) is False

    # WHEN
    x_fiscal.set_cashpurchase(sue_bob_t55_tranunit)

    # THEN
    assert x_fiscal.cashbook.tranunit_exists(sue_str, bob_str, t55_t)


def test_FiscalUnit_set_cashpurchase_RaisesErrorWhen_tranunit_timestamp_GreaterThanOrEqual_current_time():
    # ESTABLISH
    t6606_current_time = 6606
    x_fiscal = fiscalunit_shop(current_time=t6606_current_time)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_amount = 37
    sue_bob_t55_tranunit = tranunit_shop(sue_str, bob_str, t55_t, t55_amount)
    assert x_fiscal.current_time == t6606_current_time
    assert sue_bob_t55_tranunit.timestamp == t55_t
    assert sue_bob_t55_tranunit.timestamp < x_fiscal.current_time

    # WHEN
    x_fiscal.set_cashpurchase(sue_bob_t55_tranunit)
    # THEN
    assert x_fiscal.cashbook.tranunit_exists(sue_str, bob_str, t55_t)

    # ESTABLISH
    t77_t = 7707
    t77_amount = 30
    sue_bob_t77_tranunit = tranunit_shop(sue_str, bob_str, t77_t, t77_amount)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x_fiscal.set_cashpurchase(sue_bob_t77_tranunit)
    exception_str = f"Cannot set tranunit for timestamp={t77_t}, timelinepoint is greater than current time={t6606_current_time}"
    assert str(excinfo.value) == exception_str

    # WHEN/THEN
    sue_bob_t6606 = tranunit_shop(sue_str, bob_str, t6606_current_time, t77_amount)
    with pytest_raises(Exception) as excinfo:
        x_fiscal.set_cashpurchase(sue_bob_t6606)
    exception_str = f"Cannot set tranunit for timestamp={t6606_current_time}, timelinepoint is greater than current time={t6606_current_time}"
    assert str(excinfo.value) == exception_str


def test_FiscalUnit_set_cashpurchase_RaisesErrorWhenPurviewEpisodeHas_timestamp():
    # ESTABLISH
    x_fiscal = fiscalunit_shop(current_time=0)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_money_magnitude = 100
    x_fiscal.add_purviewepisode("yao", t55_t, t55_money_magnitude)
    t55_amount = 37
    t6606_current_time = 6606
    x_fiscal.current_time = t6606_current_time
    sue_bob_t55_tranunit = tranunit_shop(sue_str, bob_str, t55_t, t55_amount)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_fiscal.set_cashpurchase(sue_bob_t55_tranunit)
    exception_str = (
        f"Cannot set tranunit for timestamp={t55_t}, timelinepoint is blocked"
    )
    assert str(excinfo.value) == exception_str


def test_FiscalUnit_cashpurchase_exists_ReturnsObj():
    # ESTABLISH
    x_fiscal = fiscalunit_shop(current_time=6606)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    assert x_fiscal.cashpurchase_exists(sue_str, bob_str, t55_t) is False

    # WHEN
    t55_amount = 37
    x_fiscal.set_cashpurchase(tranunit_shop(sue_str, bob_str, t55_t, t55_amount))

    # THEN
    assert x_fiscal.cashpurchase_exists(sue_str, bob_str, t55_t)


def test_FiscalUnit_get_cashpurchase_ReturnsObj():
    # ESTABLISH
    x_fiscal = fiscalunit_shop(current_time=6606)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_amount = 37
    x_fiscal.set_cashpurchase(tranunit_shop(sue_str, bob_str, t55_t, t55_amount))
    assert x_fiscal.cashpurchase_exists(sue_str, bob_str, t55_t)

    # WHEN
    sue_gen_cashpurchase = x_fiscal.get_cashpurchase(sue_str, bob_str, t55_t)

    # THEN
    assert sue_gen_cashpurchase
    sue_bob_t55_tranunit = tranunit_shop(sue_str, bob_str, t55_t, t55_amount)
    assert sue_gen_cashpurchase == sue_bob_t55_tranunit


def test_FiscalUnit_del_cashpurchase_SetsAttr():
    # ESTABLISH
    x_fiscal = fiscalunit_shop(current_time=6606)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_amount = 37
    x_fiscal.set_cashpurchase(tranunit_shop(sue_str, bob_str, t55_t, t55_amount))
    assert x_fiscal.cashpurchase_exists(sue_str, bob_str, t55_t)

    # WHEN
    x_fiscal.del_cashpurchase(sue_str, bob_str, t55_t)

    # THEN
    assert x_fiscal.cashpurchase_exists(sue_str, bob_str, t55_t) is False


def test_FiscalUnit_set_current_time_SetsAttr():
    # ESTABLISH
    t6606_current_time = 6606
    x_fiscal = fiscalunit_shop(current_time=t6606_current_time)
    sue_str = "Sue"
    bob_str = "Bob"
    t22_t = 2202
    t22_amount = 27
    x_fiscal.set_cashpurchase(tranunit_shop(sue_str, bob_str, t22_t, t22_amount))
    assert x_fiscal.current_time == t6606_current_time

    # WHEN
    t4404_current_time = 4404
    x_fiscal.set_current_time(t4404_current_time)

    # THEN
    assert x_fiscal.current_time == t4404_current_time


def test_FiscalUnit_set_current_time_RaisesErrorWhen_cashpurchase_ExistsWithGreaterTimestamp():
    # ESTABLISH
    t6606_current_time = 6606
    x_fiscal = fiscalunit_shop(current_time=t6606_current_time)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_amount = 37
    x_fiscal.set_cashpurchase(tranunit_shop(sue_str, bob_str, t55_t, t55_amount))
    assert x_fiscal.current_time == t6606_current_time

    # WHEN / THEN
    t4404_current_time = 4404
    with pytest_raises(Exception) as excinfo:
        x_fiscal.set_current_time(t4404_current_time)
    exception_str = f"Cannot set current_time {t4404_current_time}, cashpurchase with greater timestamp exists"
    assert str(excinfo.value) == exception_str

    # THEN
    assert x_fiscal.current_time == t6606_current_time
