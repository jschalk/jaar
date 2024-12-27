from src.f01_road.finance_tran import tranbook_shop, tranunit_shop
from src.f07_deal.deal import dealunit_shop
from pytest import raises as pytest_raises


def test_dealUnit_set_cashpurchase_SetsAttr():
    # ESTABLISH
    t6606_current_time = 6606
    x_deal = dealunit_shop(current_time=t6606_current_time)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_amount = 37
    sue_bob_t55_tranunit = tranunit_shop(sue_str, bob_str, t55_t, t55_amount)
    assert x_deal.cashbook.tranunit_exists(sue_str, bob_str, t55_t) is False

    # WHEN
    x_deal.set_cashpurchase(sue_bob_t55_tranunit)

    # THEN
    assert x_deal.cashbook.tranunit_exists(sue_str, bob_str, t55_t)


def test_dealUnit_add_cashpurchase_SetsAttr():
    # ESTABLISH
    t6606_current_time = 6606
    x_deal = dealunit_shop(current_time=t6606_current_time)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_amount = 37
    assert x_deal.cashbook.tranunit_exists(sue_str, bob_str, t55_t) is False

    # WHEN
    x_deal.add_cashpurchase(sue_str, bob_str, x_time_id=t55_t, x_amount=t55_amount)

    # THEN
    assert x_deal.cashbook.tranunit_exists(sue_str, bob_str, t55_t)


def test_dealUnit_set_cashpurchase_RaisesErrorWhen_tranunit_time_id_GreaterThanOrEqual_current_time():
    # ESTABLISH
    t6606_current_time = 6606
    x_deal = dealunit_shop(current_time=t6606_current_time)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_amount = 37
    sue_bob_t55_tranunit = tranunit_shop(sue_str, bob_str, t55_t, t55_amount)
    assert x_deal.current_time == t6606_current_time
    assert sue_bob_t55_tranunit.time_id == t55_t
    assert sue_bob_t55_tranunit.time_id < x_deal.current_time

    # WHEN
    x_deal.set_cashpurchase(sue_bob_t55_tranunit)
    # THEN
    assert x_deal.cashbook.tranunit_exists(sue_str, bob_str, t55_t)

    # ESTABLISH
    t77_t = 7707
    t77_amount = 30
    sue_bob_t77_tranunit = tranunit_shop(sue_str, bob_str, t77_t, t77_amount)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_deal.set_cashpurchase(sue_bob_t77_tranunit)
    exception_str = f"Cannot set tranunit for time_id={t77_t}, timelinepoint is greater than current time={t6606_current_time}"
    assert str(excinfo.value) == exception_str

    # WHEN / THEN
    sue_bob_t6606 = tranunit_shop(sue_str, bob_str, t6606_current_time, t77_amount)
    with pytest_raises(Exception) as excinfo:
        x_deal.set_cashpurchase(sue_bob_t6606)
    exception_str = f"Cannot set tranunit for time_id={t6606_current_time}, timelinepoint is greater than current time={t6606_current_time}"
    assert str(excinfo.value) == exception_str


def test_dealUnit_set_cashpurchase_RaisesErrorWhenPurviewEpisodeHas_time_id():
    # ESTABLISH
    x_deal = dealunit_shop(current_time=0)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_money_magnitude = 100
    x_deal.add_purviewepisode("yao", t55_t, t55_money_magnitude)
    t55_amount = 37
    t6606_current_time = 6606
    x_deal.current_time = t6606_current_time
    sue_bob_t55_tranunit = tranunit_shop(sue_str, bob_str, t55_t, t55_amount)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_deal.set_cashpurchase(sue_bob_t55_tranunit)
    exception_str = f"Cannot set tranunit for time_id={t55_t}, timelinepoint is blocked"
    assert str(excinfo.value) == exception_str


def test_dealUnit_cashpurchase_exists_ReturnsObj():
    # ESTABLISH
    x_deal = dealunit_shop(current_time=6606)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    assert x_deal.cashpurchase_exists(sue_str, bob_str, t55_t) is False

    # WHEN
    t55_amount = 37
    x_deal.set_cashpurchase(tranunit_shop(sue_str, bob_str, t55_t, t55_amount))

    # THEN
    assert x_deal.cashpurchase_exists(sue_str, bob_str, t55_t)


def test_dealUnit_get_cashpurchase_ReturnsObj():
    # ESTABLISH
    x_deal = dealunit_shop(current_time=6606)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_amount = 37
    x_deal.set_cashpurchase(tranunit_shop(sue_str, bob_str, t55_t, t55_amount))
    assert x_deal.cashpurchase_exists(sue_str, bob_str, t55_t)

    # WHEN
    sue_gen_cashpurchase = x_deal.get_cashpurchase(sue_str, bob_str, t55_t)

    # THEN
    assert sue_gen_cashpurchase
    sue_bob_t55_tranunit = tranunit_shop(sue_str, bob_str, t55_t, t55_amount)
    assert sue_gen_cashpurchase == sue_bob_t55_tranunit


def test_dealUnit_del_cashpurchase_SetsAttr():
    # ESTABLISH
    x_deal = dealunit_shop(current_time=6606)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_amount = 37
    x_deal.set_cashpurchase(tranunit_shop(sue_str, bob_str, t55_t, t55_amount))
    assert x_deal.cashpurchase_exists(sue_str, bob_str, t55_t)

    # WHEN
    x_deal.del_cashpurchase(sue_str, bob_str, t55_t)

    # THEN
    assert x_deal.cashpurchase_exists(sue_str, bob_str, t55_t) is False


def test_dealUnit_set_current_time_SetsAttr():
    # ESTABLISH
    t6606_current_time = 6606
    x_deal = dealunit_shop(current_time=t6606_current_time)
    sue_str = "Sue"
    bob_str = "Bob"
    t22_t = 2202
    t22_amount = 27
    x_deal.set_cashpurchase(tranunit_shop(sue_str, bob_str, t22_t, t22_amount))
    assert x_deal.current_time == t6606_current_time

    # WHEN
    t4404_current_time = 4404
    x_deal.set_current_time(t4404_current_time)

    # THEN
    assert x_deal.current_time == t4404_current_time


def test_dealUnit_set_current_time_RaisesErrorWhen_cashpurchase_ExistsWithGreatertime_id():
    # ESTABLISH
    t6606_current_time = 6606
    x_deal = dealunit_shop(current_time=t6606_current_time)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_t = 5505
    t55_amount = 37
    x_deal.set_cashpurchase(tranunit_shop(sue_str, bob_str, t55_t, t55_amount))
    assert x_deal.current_time == t6606_current_time

    # WHEN / THEN
    t4404_current_time = 4404
    with pytest_raises(Exception) as excinfo:
        x_deal.set_current_time(t4404_current_time)
    exception_str = f"Cannot set current_time {t4404_current_time}, cashpurchase with greater time_id exists"
    assert str(excinfo.value) == exception_str

    # THEN
    assert x_deal.current_time == t6606_current_time


def test_dealUnit_set_all_tranbook_SetsAttr():
    # ESTABLISH
    x_deal = dealunit_shop(current_time=10101)
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
    x_deal.set_cashpurchase(t55_tranunit)
    x_deal.set_cashpurchase(t66_tranunit)
    x_deal.set_cashpurchase(t77_tranunit)
    x_deal.set_cashpurchase(t88_tranunit)
    x_deal.set_cashpurchase(t99_tranunit)

    x40000_time_id = 40000
    x70000_time_id = 70000
    x_deal.add_purviewepisode(sue_str, x40000_time_id, 1)
    x_deal.add_purviewepisode(sue_str, x70000_time_id, 1)
    bob_str = "Bob"
    zia_str = "Zia"
    zia_net_purview = 887
    bob_net_purview = 445
    sue_x40000_episode = x_deal.get_purviewlog(sue_str).get_episode(x40000_time_id)
    sue_x70000_episode = x_deal.get_purviewlog(sue_str).get_episode(x70000_time_id)
    sue_x40000_episode.set_net_purview(bob_str, bob_net_purview)
    sue_x70000_episode.set_net_purview(zia_str, zia_net_purview)

    assert x_deal._all_tranbook == tranbook_shop(x_deal.deal_id)
    assert x_deal.cashpurchase_exists(sue_str, bob_str, t55_t)
    assert x_deal.cashpurchase_exists(yao_str, bob_str, t66_t)
    assert x_deal.cashpurchase_exists(yao_str, sue_str, t77_t)
    assert x_deal.cashpurchase_exists(sue_str, yao_str, t88_t)
    assert x_deal.cashpurchase_exists(bob_str, sue_str, t99_t)

    assert sue_x40000_episode.net_purview_exists(bob_str)
    assert sue_x70000_episode.net_purview_exists(zia_str)
    # x_deal.add_purviewepisode()

    # WHEN
    x_deal.set_all_tranbook()

    # THEN
    assert x_deal._all_tranbook.tranunit_exists(sue_str, bob_str, t55_t)
    assert x_deal._all_tranbook.tranunit_exists(yao_str, bob_str, t66_t)
    assert x_deal._all_tranbook.tranunit_exists(yao_str, sue_str, t77_t)
    assert x_deal._all_tranbook.tranunit_exists(sue_str, yao_str, t88_t)
    assert x_deal._all_tranbook.tranunit_exists(bob_str, sue_str, t99_t)
    assert x_deal._all_tranbook.tranunit_exists(sue_str, bob_str, x40000_time_id)
    assert x_deal._all_tranbook.tranunit_exists(sue_str, zia_str, x70000_time_id)
