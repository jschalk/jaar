from src.f01_road.deal import (
    quota_str,
    dealepisode_shop,
    BrokerUnit,
    brokerunit_shop,
    get_brokerunit_from_dict,
    time_int_str,
    ledger_depth_str,
    owner_name_str,
    episode_net_str,
)


def test_BrokerUnit_Exists():
    # ESTABLISH / WHEN
    x_brokerunit = BrokerUnit()

    # THEN
    assert x_brokerunit
    assert not x_brokerunit.owner_name
    assert not x_brokerunit.episodes
    assert not x_brokerunit._sum_dealepisode_quota
    assert not x_brokerunit._sum_acct_deals
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
    assert x_brokerunit.episodes == {}
    assert not x_brokerunit._sum_dealepisode_quota
    assert x_brokerunit._sum_acct_deals == {}
    assert not x_brokerunit._time_int_min
    assert not x_brokerunit._time_int_max


def test_BrokerUnit_set_episode_SetsAttr():
    # ESTABLISH
    sue_brokerunit = brokerunit_shop("sue")
    assert sue_brokerunit.episodes == {}

    # WHEN
    t1_int = 145
    t1_dealepisode = dealepisode_shop(t1_int, 0)
    sue_brokerunit.set_episode(t1_dealepisode)

    # THEN
    assert sue_brokerunit.episodes != {}
    assert sue_brokerunit.episodes.get(t1_int) == t1_dealepisode


def test_BrokerUnit_episode_exists_ReturnsObj():
    # ESTABLISH
    sue_brokerunit = brokerunit_shop("Sue")
    t1_int = 145
    assert sue_brokerunit.episode_exists(t1_int) is False

    # WHEN
    t1_dealepisode = dealepisode_shop(t1_int, 0)
    sue_brokerunit.set_episode(t1_dealepisode)

    # THEN
    assert sue_brokerunit.episode_exists(t1_int)


def test_BrokerUnit_get_episode_ReturnsObj():
    # ESTABLISH
    sue_brokerunit = brokerunit_shop("sue")
    t1_int = 145
    t1_stat_dealepisode = dealepisode_shop(t1_int, 0)
    sue_brokerunit.set_episode(t1_stat_dealepisode)

    # WHEN
    t1_gen_dealepisode = sue_brokerunit.get_episode(t1_int)

    # THEN
    assert t1_gen_dealepisode
    assert t1_gen_dealepisode == t1_stat_dealepisode


def test_BrokerUnit_del_episode_SetsAttr():
    # ESTABLISH
    sue_brokerunit = brokerunit_shop("Sue")
    t1_int = 145
    t1_stat_dealepisode = dealepisode_shop(t1_int, 0)
    sue_brokerunit.set_episode(t1_stat_dealepisode)
    assert sue_brokerunit.episode_exists(t1_int)

    # WHEN
    sue_brokerunit.del_episode(t1_int)

    # THEN
    assert sue_brokerunit.episode_exists(t1_int) is False


def test_BrokerUnit_add_episode_SetsAttr():
    # ESTABLISH
    sue_brokerunit = brokerunit_shop("sue")
    assert sue_brokerunit.episodes == {}

    # WHEN
    t1_int = 145
    t1_quota = 500
    sue_brokerunit.add_episode(t1_int, x_quota=t1_quota)

    # THEN
    assert sue_brokerunit.episodes != {}
    t1_dealepisode = dealepisode_shop(t1_int, t1_quota)
    assert sue_brokerunit.episodes.get(t1_int) == t1_dealepisode


def test_BrokerUnit_add_episode_SetsAttr_ledger_depth():
    # ESTABLISH
    sue_brokerunit = brokerunit_shop("sue")
    assert sue_brokerunit.episodes == {}

    # WHEN
    t1_int = 145
    t1_quota = 500
    t1_ledger_depth = 3
    sue_brokerunit.add_episode(t1_int, t1_quota, t1_ledger_depth)

    # THEN
    assert sue_brokerunit.episodes != {}
    t1_dealepisode = dealepisode_shop(t1_int, t1_quota, ledger_depth=t1_ledger_depth)
    assert sue_brokerunit.episodes.get(t1_int) == t1_dealepisode


def test_BrokerUnit_get_2d_array_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)

    # WHEN
    sue_episodes_2d_array = sue_brokerunit.get_2d_array()

    # THEN
    assert sue_episodes_2d_array == []


def test_BrokerUnit_get_2d_array_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_brokerunit.add_episode(x4_time_int, x4_quota)
    sue_brokerunit.add_episode(x7_time_int, x7_quota)

    # WHEN
    sue_episodes_2d_array = sue_brokerunit.get_2d_array()

    # THEN
    assert sue_episodes_2d_array == [
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
    sue_brokerunit.add_episode(x4_time_int, x4_quota)
    sue_brokerunit.add_episode(x7_time_int, x7_quota)

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
    sue_brokerunit.add_episode(x4_time_int, x4_quota)
    sue_brokerunit.add_episode(x7_time_int, x7_quota)

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
    x7_ledger_depth = 22
    sue_brokerunit.add_episode(x4_time_int, x4_quota)
    sue_brokerunit.add_episode(x7_time_int, x7_quota, ledger_depth=x7_ledger_depth)

    # WHEN
    sue_episodes_dict = sue_brokerunit.get_dict()

    # THEN
    assert sue_episodes_dict == {
        owner_name_str(): sue_str,
        "episodes": {
            x4_time_int: {quota_str(): x4_quota, time_int_str(): x4_time_int},
            x7_time_int: {
                quota_str(): x7_quota,
                time_int_str(): x7_time_int,
                ledger_depth_str(): x7_ledger_depth,
            },
        },
    }


def test_get_brokerunit_from_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    sue_episodes_dict = sue_brokerunit.get_dict()
    assert sue_episodes_dict == {owner_name_str(): sue_str, "episodes": {}}

    # WHEN
    x_brokerunit = get_brokerunit_from_dict(sue_episodes_dict)

    # THEN
    assert x_brokerunit
    assert x_brokerunit.owner_name == sue_str
    assert x_brokerunit.episodes == {}
    assert x_brokerunit.episodes == sue_brokerunit.episodes
    assert x_brokerunit == sue_brokerunit


def test_get_brokerunit_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_brokerunit.add_episode(x4_time_int, x4_quota)
    sue_brokerunit.add_episode(x7_time_int, x7_quota)
    sue_episodes_dict = sue_brokerunit.get_dict()
    assert sue_episodes_dict == {
        owner_name_str(): sue_str,
        "episodes": {
            x4_time_int: {time_int_str(): x4_time_int, quota_str(): x4_quota},
            x7_time_int: {time_int_str(): x7_time_int, quota_str(): x7_quota},
        },
    }

    # WHEN
    x_brokerunit = get_brokerunit_from_dict(sue_episodes_dict)

    # THEN
    assert x_brokerunit
    assert x_brokerunit.owner_name == sue_str
    assert x_brokerunit.get_episode(x4_time_int) != None
    assert x_brokerunit.get_episode(x7_time_int) != None
    assert x_brokerunit.episodes == sue_brokerunit.episodes
    assert x_brokerunit == sue_brokerunit


def test_get_brokerunit_from_dict_ReturnsObj_Scenario2():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_brokerunit.add_episode(x4_time_int, x4_quota)
    sue_brokerunit.add_episode(x7_time_int, x7_quota)
    zia_str = "Zia"
    zia_net_deal = 887
    sue_net_deal = 445
    sue_brokerunit.get_episode(x7_time_int).set_net_deal(sue_str, sue_net_deal)
    sue_brokerunit.get_episode(x7_time_int).set_net_deal(zia_str, zia_net_deal)
    sue_episodes_dict = sue_brokerunit.get_dict()
    assert sue_episodes_dict == {
        owner_name_str(): sue_str,
        "episodes": {
            x4_time_int: {time_int_str(): x4_time_int, quota_str(): x4_quota},
            x7_time_int: {
                time_int_str(): x7_time_int,
                quota_str(): x7_quota,
                episode_net_str(): {sue_str: sue_net_deal, zia_str: zia_net_deal},
            },
        },
    }

    # WHEN
    x_brokerunit = get_brokerunit_from_dict(sue_episodes_dict)

    # THEN
    assert x_brokerunit
    assert x_brokerunit.owner_name == sue_str
    assert x_brokerunit.get_episode(x4_time_int) != None
    assert x_brokerunit.get_episode(x7_time_int) != None
    assert x_brokerunit.get_episode(x7_time_int)._episode_net != {}
    assert len(x_brokerunit.get_episode(x7_time_int)._episode_net) == 2
    assert x_brokerunit.episodes == sue_brokerunit.episodes
    assert x_brokerunit == sue_brokerunit


def test_BrokerUnit_get_tranbook_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_brokerunit.add_episode(x4_time_int, x4_quota)
    sue_brokerunit.add_episode(x7_time_int, x7_quota)
    bob_str = "Bob"
    zia_str = "Zia"
    zia_net_deal = 887
    bob_net_deal = 445
    sue_brokerunit.get_episode(x4_time_int).set_net_deal(bob_str, bob_net_deal)
    sue_brokerunit.get_episode(x7_time_int).set_net_deal(zia_str, zia_net_deal)
    sue_episodes_dict = sue_brokerunit.get_dict()
    assert sue_episodes_dict == {
        owner_name_str(): sue_str,
        "episodes": {
            x4_time_int: {
                time_int_str(): x4_time_int,
                quota_str(): x4_quota,
                episode_net_str(): {bob_str: bob_net_deal},
            },
            x7_time_int: {
                time_int_str(): x7_time_int,
                quota_str(): x7_quota,
                episode_net_str(): {zia_str: zia_net_deal},
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
    assert sue_tranbook.get_amount(sue_str, zia_str, x7_time_int) == zia_net_deal
    assert sue_tranbook.get_amount(sue_str, bob_str, x4_time_int) == bob_net_deal
