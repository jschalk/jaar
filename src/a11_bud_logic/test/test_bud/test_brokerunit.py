from src.a11_bud_logic.bud import (
    BrokerUnit,
    brokerunit_shop,
    budunit_shop,
    get_brokerunit_from_dict,
)
from src.a11_bud_logic.test._util.a11_str import (
    belief_name_str,
    bud_partner_nets_str,
    bud_time_str,
    celldepth_str,
    quota_str,
)


def test_BrokerUnit_Exists():
    # ESTABLISH / WHEN
    x_brokerunit = BrokerUnit()

    # THEN
    assert x_brokerunit
    assert not x_brokerunit.belief_name
    assert not x_brokerunit.buds
    assert not x_brokerunit._sum_budunit_quota
    assert not x_brokerunit._sum_partner_bud_nets
    assert not x_brokerunit._bud_time_min
    assert not x_brokerunit._bud_time_max


def test_brokerunit_shop_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"

    # WHEN
    x_brokerunit = brokerunit_shop(sue_str)

    # THEN
    assert x_brokerunit
    assert x_brokerunit.belief_name == sue_str
    assert x_brokerunit.buds == {}
    assert not x_brokerunit._sum_budunit_quota
    assert x_brokerunit._sum_partner_bud_nets == {}
    assert not x_brokerunit._bud_time_min
    assert not x_brokerunit._bud_time_max


def test_BrokerUnit_set_bud_SetsAttr():
    # ESTABLISH
    sue_brokerunit = brokerunit_shop("sue")
    assert sue_brokerunit.buds == {}

    # WHEN
    t1_int = 145
    t1_budunit = budunit_shop(t1_int, 0)
    sue_brokerunit.set_bud(t1_budunit)

    # THEN
    assert sue_brokerunit.buds != {}
    assert sue_brokerunit.buds.get(t1_int) == t1_budunit


def test_BrokerUnit_bud_exists_ReturnsObj():
    # ESTABLISH
    sue_brokerunit = brokerunit_shop("Sue")
    t1_int = 145
    assert sue_brokerunit.bud_exists(t1_int) is False

    # WHEN
    t1_budunit = budunit_shop(t1_int, 0)
    sue_brokerunit.set_bud(t1_budunit)

    # THEN
    assert sue_brokerunit.bud_exists(t1_int)


def test_BrokerUnit_get_bud_ReturnsObj():
    # ESTABLISH
    sue_brokerunit = brokerunit_shop("sue")
    t1_int = 145
    t1_stat_budunit = budunit_shop(t1_int, 0)
    sue_brokerunit.set_bud(t1_stat_budunit)

    # WHEN
    t1_gen_budunit = sue_brokerunit.get_bud(t1_int)

    # THEN
    assert t1_gen_budunit
    assert t1_gen_budunit == t1_stat_budunit


def test_BrokerUnit_del_bud_SetsAttr():
    # ESTABLISH
    sue_brokerunit = brokerunit_shop("Sue")
    t1_int = 145
    t1_stat_budunit = budunit_shop(t1_int, 0)
    sue_brokerunit.set_bud(t1_stat_budunit)
    assert sue_brokerunit.bud_exists(t1_int)

    # WHEN
    sue_brokerunit.del_bud(t1_int)

    # THEN
    assert sue_brokerunit.bud_exists(t1_int) is False


def test_BrokerUnit_add_bud_SetsAttr():
    # ESTABLISH
    sue_brokerunit = brokerunit_shop("sue")
    assert sue_brokerunit.buds == {}

    # WHEN
    t1_int = 145
    t1_quota = 500
    sue_brokerunit.add_bud(t1_int, x_quota=t1_quota)

    # THEN
    assert sue_brokerunit.buds != {}
    t1_budunit = budunit_shop(t1_int, t1_quota)
    assert sue_brokerunit.buds.get(t1_int) == t1_budunit


def test_BrokerUnit_add_bud_SetsAttr_celldepth():
    # ESTABLISH
    sue_brokerunit = brokerunit_shop("sue")
    assert sue_brokerunit.buds == {}

    # WHEN
    t1_int = 145
    t1_quota = 500
    t1_celldepth = 3
    sue_brokerunit.add_bud(t1_int, t1_quota, t1_celldepth)

    # THEN
    assert sue_brokerunit.buds != {}
    t1_budunit = budunit_shop(t1_int, t1_quota, celldepth=t1_celldepth)
    assert sue_brokerunit.buds.get(t1_int) == t1_budunit


def test_BrokerUnit_get_2d_array_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)

    # WHEN
    sue_buds_2d_array = sue_brokerunit.get_2d_array()

    # THEN
    assert sue_buds_2d_array == []


def test_BrokerUnit_get_2d_array_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    sue_brokerunit.add_bud(x4_bud_time, x4_quota)
    sue_brokerunit.add_bud(x7_bud_time, x7_quota)

    # WHEN
    sue_buds_2d_array = sue_brokerunit.get_2d_array()

    # THEN
    assert sue_buds_2d_array == [
        [sue_str, x4_bud_time, x4_quota],
        [sue_str, x7_bud_time, x7_quota],
    ]


def test_BrokerUnit_get_bud_times_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    assert sue_brokerunit.get_bud_times() == set()

    # WHEN
    sue_brokerunit.add_bud(x4_bud_time, x4_quota)
    sue_brokerunit.add_bud(x7_bud_time, x7_quota)

    # THEN
    assert sue_brokerunit.get_bud_times() == {x4_bud_time, x7_bud_time}


def test_BrokerUnit_get_headers_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    sue_brokerunit.add_bud(x4_bud_time, x4_quota)
    sue_brokerunit.add_bud(x7_bud_time, x7_quota)

    # WHEN
    sue_headers_list = sue_brokerunit.get_headers()

    # THEN
    assert sue_headers_list == [belief_name_str(), bud_time_str(), quota_str()]


def test_BrokerUnit_to_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    x7_celldepth = 22
    sue_brokerunit.add_bud(x4_bud_time, x4_quota)
    sue_brokerunit.add_bud(x7_bud_time, x7_quota, celldepth=x7_celldepth)

    # WHEN
    sue_buds_dict = sue_brokerunit.to_dict()

    # THEN
    assert sue_buds_dict == {
        belief_name_str(): sue_str,
        "buds": {
            x4_bud_time: {quota_str(): x4_quota, bud_time_str(): x4_bud_time},
            x7_bud_time: {
                quota_str(): x7_quota,
                bud_time_str(): x7_bud_time,
                celldepth_str(): x7_celldepth,
            },
        },
    }


def test_get_brokerunit_from_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    sue_buds_dict = sue_brokerunit.to_dict()
    assert sue_buds_dict == {belief_name_str(): sue_str, "buds": {}}

    # WHEN
    x_brokerunit = get_brokerunit_from_dict(sue_buds_dict)

    # THEN
    assert x_brokerunit
    assert x_brokerunit.belief_name == sue_str
    assert x_brokerunit.buds == {}
    assert x_brokerunit.buds == sue_brokerunit.buds
    assert x_brokerunit == sue_brokerunit


def test_get_brokerunit_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    sue_brokerunit.add_bud(x4_bud_time, x4_quota)
    sue_brokerunit.add_bud(x7_bud_time, x7_quota)
    sue_buds_dict = sue_brokerunit.to_dict()
    assert sue_buds_dict == {
        belief_name_str(): sue_str,
        "buds": {
            x4_bud_time: {bud_time_str(): x4_bud_time, quota_str(): x4_quota},
            x7_bud_time: {bud_time_str(): x7_bud_time, quota_str(): x7_quota},
        },
    }

    # WHEN
    x_brokerunit = get_brokerunit_from_dict(sue_buds_dict)

    # THEN
    assert x_brokerunit
    assert x_brokerunit.belief_name == sue_str
    assert x_brokerunit.get_bud(x4_bud_time) != None
    assert x_brokerunit.get_bud(x7_bud_time) != None
    assert x_brokerunit.buds == sue_brokerunit.buds
    assert x_brokerunit == sue_brokerunit


def test_get_brokerunit_from_dict_ReturnsObj_Scenario2():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    sue_brokerunit.add_bud(x4_bud_time, x4_quota)
    sue_brokerunit.add_bud(x7_bud_time, x7_quota)
    zia_str = "Zia"
    zia_bud_partner_net = 887
    sue_bud_partner_net = 445
    sue_brokerunit.get_bud(x7_bud_time).set_bud_partner_net(
        sue_str, sue_bud_partner_net
    )
    sue_brokerunit.get_bud(x7_bud_time).set_bud_partner_net(
        zia_str, zia_bud_partner_net
    )
    sue_buds_dict = sue_brokerunit.to_dict()
    assert sue_buds_dict == {
        belief_name_str(): sue_str,
        "buds": {
            x4_bud_time: {bud_time_str(): x4_bud_time, quota_str(): x4_quota},
            x7_bud_time: {
                bud_time_str(): x7_bud_time,
                quota_str(): x7_quota,
                bud_partner_nets_str(): {
                    sue_str: sue_bud_partner_net,
                    zia_str: zia_bud_partner_net,
                },
            },
        },
    }

    # WHEN
    x_brokerunit = get_brokerunit_from_dict(sue_buds_dict)

    # THEN
    assert x_brokerunit
    assert x_brokerunit.belief_name == sue_str
    assert x_brokerunit.get_bud(x4_bud_time) != None
    assert x_brokerunit.get_bud(x7_bud_time) != None
    assert x_brokerunit.get_bud(x7_bud_time)._bud_partner_nets != {}
    assert len(x_brokerunit.get_bud(x7_bud_time)._bud_partner_nets) == 2
    assert x_brokerunit.buds == sue_brokerunit.buds
    assert x_brokerunit == sue_brokerunit


def test_BrokerUnit_get_tranbook_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    sue_brokerunit.add_bud(x4_bud_time, x4_quota)
    sue_brokerunit.add_bud(x7_bud_time, x7_quota)
    bob_str = "Bob"
    zia_str = "Zia"
    zia_bud_partner_net = 887
    bob_bud_partner_net = 445
    sue_brokerunit.get_bud(x4_bud_time).set_bud_partner_net(
        bob_str, bob_bud_partner_net
    )
    sue_brokerunit.get_bud(x7_bud_time).set_bud_partner_net(
        zia_str, zia_bud_partner_net
    )
    sue_buds_dict = sue_brokerunit.to_dict()
    assert sue_buds_dict == {
        belief_name_str(): sue_str,
        "buds": {
            x4_bud_time: {
                bud_time_str(): x4_bud_time,
                quota_str(): x4_quota,
                bud_partner_nets_str(): {bob_str: bob_bud_partner_net},
            },
            x7_bud_time: {
                bud_time_str(): x7_bud_time,
                quota_str(): x7_quota,
                bud_partner_nets_str(): {zia_str: zia_bud_partner_net},
            },
        },
    }

    # WHEN
    x_moment_label = "moment_label_x"
    sue_tranbook = sue_brokerunit.get_tranbook(x_moment_label)

    # THEN
    assert sue_tranbook
    assert sue_tranbook.moment_label == x_moment_label
    assert sue_tranbook.tranunit_exists(sue_str, zia_str, x7_bud_time)
    assert sue_tranbook.tranunit_exists(sue_str, bob_str, x4_bud_time)
    assert sue_tranbook.get_amount(sue_str, zia_str, x7_bud_time) == zia_bud_partner_net
    assert sue_tranbook.get_amount(sue_str, bob_str, x4_bud_time) == bob_bud_partner_net
