from src.f01_road.deal import (
    quota_str,
    dealunit_shop,
    BrokerUnit,
    brokerunit_shop,
    get_brokerunit_from_dict,
    time_int_str,
    celldepth_str,
    owner_name_str,
    deal_net_str,
)


def test_BrokerUnit_Exists():
    # ESTABLISH / WHEN
    x_brokerunit = BrokerUnit()

    # THEN
    assert x_brokerunit
    assert not x_brokerunit.owner_name
    assert not x_brokerunit.deals
    assert not x_brokerunit._sum_dealunit_quota
    assert not x_brokerunit._sum_acct_deal_nets
    assert not x_brokerunit._time_int_min
    assert not x_brokerunit._time_int_max


def test_brokerunit_shop_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"

    # WHEN
    x_brokerunit = brokerunit_shop(sue_str)

    # THEN
    assert x_brokerunit
    assert x_brokerunit.owner_name == sue_str
    assert x_brokerunit.deals == {}
    assert not x_brokerunit._sum_dealunit_quota
    assert x_brokerunit._sum_acct_deal_nets == {}
    assert not x_brokerunit._time_int_min
    assert not x_brokerunit._time_int_max


def test_BrokerUnit_set_deal_SetsAttr():
    # ESTABLISH
    sue_brokerunit = brokerunit_shop("sue")
    assert sue_brokerunit.deals == {}

    # WHEN
    t1_int = 145
    t1_dealunit = dealunit_shop(t1_int, 0)
    sue_brokerunit.set_deal(t1_dealunit)

    # THEN
    assert sue_brokerunit.deals != {}
    assert sue_brokerunit.deals.get(t1_int) == t1_dealunit


def test_BrokerUnit_deal_exists_ReturnsObj():
    # ESTABLISH
    sue_brokerunit = brokerunit_shop("Sue")
    t1_int = 145
    assert sue_brokerunit.deal_exists(t1_int) is False

    # WHEN
    t1_dealunit = dealunit_shop(t1_int, 0)
    sue_brokerunit.set_deal(t1_dealunit)

    # THEN
    assert sue_brokerunit.deal_exists(t1_int)


def test_BrokerUnit_get_deal_ReturnsObj():
    # ESTABLISH
    sue_brokerunit = brokerunit_shop("sue")
    t1_int = 145
    t1_stat_dealunit = dealunit_shop(t1_int, 0)
    sue_brokerunit.set_deal(t1_stat_dealunit)

    # WHEN
    t1_gen_dealunit = sue_brokerunit.get_deal(t1_int)

    # THEN
    assert t1_gen_dealunit
    assert t1_gen_dealunit == t1_stat_dealunit


def test_BrokerUnit_del_deal_SetsAttr():
    # ESTABLISH
    sue_brokerunit = brokerunit_shop("Sue")
    t1_int = 145
    t1_stat_dealunit = dealunit_shop(t1_int, 0)
    sue_brokerunit.set_deal(t1_stat_dealunit)
    assert sue_brokerunit.deal_exists(t1_int)

    # WHEN
    sue_brokerunit.del_deal(t1_int)

    # THEN
    assert sue_brokerunit.deal_exists(t1_int) is False


def test_BrokerUnit_add_deal_SetsAttr():
    # ESTABLISH
    sue_brokerunit = brokerunit_shop("sue")
    assert sue_brokerunit.deals == {}

    # WHEN
    t1_int = 145
    t1_quota = 500
    sue_brokerunit.add_deal(t1_int, x_quota=t1_quota)

    # THEN
    assert sue_brokerunit.deals != {}
    t1_dealunit = dealunit_shop(t1_int, t1_quota)
    assert sue_brokerunit.deals.get(t1_int) == t1_dealunit


def test_BrokerUnit_add_deal_SetsAttr_celldepth():
    # ESTABLISH
    sue_brokerunit = brokerunit_shop("sue")
    assert sue_brokerunit.deals == {}

    # WHEN
    t1_int = 145
    t1_quota = 500
    t1_celldepth = 3
    sue_brokerunit.add_deal(t1_int, t1_quota, t1_celldepth)

    # THEN
    assert sue_brokerunit.deals != {}
    t1_dealunit = dealunit_shop(t1_int, t1_quota, celldepth=t1_celldepth)
    assert sue_brokerunit.deals.get(t1_int) == t1_dealunit


def test_BrokerUnit_get_2d_array_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)

    # WHEN
    sue_deals_2d_array = sue_brokerunit.get_2d_array()

    # THEN
    assert sue_deals_2d_array == []


def test_BrokerUnit_get_2d_array_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_brokerunit.add_deal(x4_time_int, x4_quota)
    sue_brokerunit.add_deal(x7_time_int, x7_quota)

    # WHEN
    sue_deals_2d_array = sue_brokerunit.get_2d_array()

    # THEN
    assert sue_deals_2d_array == [
        [sue_str, x4_time_int, x4_quota],
        [sue_str, x7_time_int, x7_quota],
    ]


def test_BrokerUnit_get_time_ints_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    assert sue_brokerunit.get_time_ints() == set()

    # WHEN
    sue_brokerunit.add_deal(x4_time_int, x4_quota)
    sue_brokerunit.add_deal(x7_time_int, x7_quota)

    # THEN
    assert sue_brokerunit.get_time_ints() == {x4_time_int, x7_time_int}


def test_BrokerUnit_get_headers_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_brokerunit.add_deal(x4_time_int, x4_quota)
    sue_brokerunit.add_deal(x7_time_int, x7_quota)

    # WHEN
    sue_headers_list = sue_brokerunit.get_headers()

    # THEN
    assert sue_headers_list == [owner_name_str(), time_int_str(), quota_str()]


def test_BrokerUnit_get_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    x7_celldepth = 22
    sue_brokerunit.add_deal(x4_time_int, x4_quota)
    sue_brokerunit.add_deal(x7_time_int, x7_quota, celldepth=x7_celldepth)

    # WHEN
    sue_deals_dict = sue_brokerunit.get_dict()

    # THEN
    assert sue_deals_dict == {
        owner_name_str(): sue_str,
        "deals": {
            x4_time_int: {quota_str(): x4_quota, time_int_str(): x4_time_int},
            x7_time_int: {
                quota_str(): x7_quota,
                time_int_str(): x7_time_int,
                celldepth_str(): x7_celldepth,
            },
        },
    }


def test_get_brokerunit_from_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    sue_deals_dict = sue_brokerunit.get_dict()
    assert sue_deals_dict == {owner_name_str(): sue_str, "deals": {}}

    # WHEN
    x_brokerunit = get_brokerunit_from_dict(sue_deals_dict)

    # THEN
    assert x_brokerunit
    assert x_brokerunit.owner_name == sue_str
    assert x_brokerunit.deals == {}
    assert x_brokerunit.deals == sue_brokerunit.deals
    assert x_brokerunit == sue_brokerunit


def test_get_brokerunit_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_brokerunit.add_deal(x4_time_int, x4_quota)
    sue_brokerunit.add_deal(x7_time_int, x7_quota)
    sue_deals_dict = sue_brokerunit.get_dict()
    assert sue_deals_dict == {
        owner_name_str(): sue_str,
        "deals": {
            x4_time_int: {time_int_str(): x4_time_int, quota_str(): x4_quota},
            x7_time_int: {time_int_str(): x7_time_int, quota_str(): x7_quota},
        },
    }

    # WHEN
    x_brokerunit = get_brokerunit_from_dict(sue_deals_dict)

    # THEN
    assert x_brokerunit
    assert x_brokerunit.owner_name == sue_str
    assert x_brokerunit.get_deal(x4_time_int) != None
    assert x_brokerunit.get_deal(x7_time_int) != None
    assert x_brokerunit.deals == sue_brokerunit.deals
    assert x_brokerunit == sue_brokerunit


def test_get_brokerunit_from_dict_ReturnsObj_Scenario2():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_brokerunit.add_deal(x4_time_int, x4_quota)
    sue_brokerunit.add_deal(x7_time_int, x7_quota)
    zia_str = "Zia"
    zia_deal_net = 887
    sue_deal_net = 445
    sue_brokerunit.get_deal(x7_time_int).set_deal_net(sue_str, sue_deal_net)
    sue_brokerunit.get_deal(x7_time_int).set_deal_net(zia_str, zia_deal_net)
    sue_deals_dict = sue_brokerunit.get_dict()
    assert sue_deals_dict == {
        owner_name_str(): sue_str,
        "deals": {
            x4_time_int: {time_int_str(): x4_time_int, quota_str(): x4_quota},
            x7_time_int: {
                time_int_str(): x7_time_int,
                quota_str(): x7_quota,
                deal_net_str(): {sue_str: sue_deal_net, zia_str: zia_deal_net},
            },
        },
    }

    # WHEN
    x_brokerunit = get_brokerunit_from_dict(sue_deals_dict)

    # THEN
    assert x_brokerunit
    assert x_brokerunit.owner_name == sue_str
    assert x_brokerunit.get_deal(x4_time_int) != None
    assert x_brokerunit.get_deal(x7_time_int) != None
    assert x_brokerunit.get_deal(x7_time_int)._deal_net != {}
    assert len(x_brokerunit.get_deal(x7_time_int)._deal_net) == 2
    assert x_brokerunit.deals == sue_brokerunit.deals
    assert x_brokerunit == sue_brokerunit


def test_BrokerUnit_get_tranbook_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_brokerunit.add_deal(x4_time_int, x4_quota)
    sue_brokerunit.add_deal(x7_time_int, x7_quota)
    bob_str = "Bob"
    zia_str = "Zia"
    zia_deal_net = 887
    bob_deal_net = 445
    sue_brokerunit.get_deal(x4_time_int).set_deal_net(bob_str, bob_deal_net)
    sue_brokerunit.get_deal(x7_time_int).set_deal_net(zia_str, zia_deal_net)
    sue_deals_dict = sue_brokerunit.get_dict()
    assert sue_deals_dict == {
        owner_name_str(): sue_str,
        "deals": {
            x4_time_int: {
                time_int_str(): x4_time_int,
                quota_str(): x4_quota,
                deal_net_str(): {bob_str: bob_deal_net},
            },
            x7_time_int: {
                time_int_str(): x7_time_int,
                quota_str(): x7_quota,
                deal_net_str(): {zia_str: zia_deal_net},
            },
        },
    }

    # WHEN
    x_fisc_title = "fisc_title_x"
    sue_tranbook = sue_brokerunit.get_tranbook(x_fisc_title)

    # THEN
    assert sue_tranbook
    assert sue_tranbook.fisc_title == x_fisc_title
    assert sue_tranbook.tranunit_exists(sue_str, zia_str, x7_time_int)
    assert sue_tranbook.tranunit_exists(sue_str, bob_str, x4_time_int)
    assert sue_tranbook.get_amount(sue_str, zia_str, x7_time_int) == zia_deal_net
    assert sue_tranbook.get_amount(sue_str, bob_str, x4_time_int) == bob_deal_net
