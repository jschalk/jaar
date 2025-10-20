from src.ch11_bud._ref.ch11_semantic_types import SparkInt
from src.ch11_bud.bud_main import (
    BeliefBudHistory,
    beliefbudhistory_shop,
    budunit_shop,
    get_beliefbudhistory_from_dict,
)
from src.ref.keywords import Ch11Keywords as kw


def test_SparkInt_Exists():
    # ESTABLISH / WHEN / THEN
    assert SparkInt(13) == 13
    assert SparkInt(13.5) == 13


def test_BeliefBudHistory_Exists():
    # ESTABLISH / WHEN
    x_beliefbudhistory = BeliefBudHistory()

    # THEN
    assert x_beliefbudhistory
    assert not x_beliefbudhistory.belief_name
    assert not x_beliefbudhistory.buds
    assert not x_beliefbudhistory._sum_budunit_quota
    assert not x_beliefbudhistory._sum_voice_bud_nets
    assert not x_beliefbudhistory._bud_time_min
    assert not x_beliefbudhistory._bud_time_max


def test_beliefbudhistory_shop_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"

    # WHEN
    x_beliefbudhistory = beliefbudhistory_shop(sue_str)

    # THEN
    assert x_beliefbudhistory
    assert x_beliefbudhistory.belief_name == sue_str
    assert x_beliefbudhistory.buds == {}
    assert not x_beliefbudhistory._sum_budunit_quota
    assert x_beliefbudhistory._sum_voice_bud_nets == {}
    assert not x_beliefbudhistory._bud_time_min
    assert not x_beliefbudhistory._bud_time_max


def test_BeliefBudHistory_set_bud_SetsAttr():
    # ESTABLISH
    sue_beliefbudhistory = beliefbudhistory_shop("sue")
    assert sue_beliefbudhistory.buds == {}

    # WHEN
    t1_int = 145
    t1_budunit = budunit_shop(t1_int, 0)
    sue_beliefbudhistory.set_bud(t1_budunit)

    # THEN
    assert sue_beliefbudhistory.buds != {}
    assert sue_beliefbudhistory.buds.get(t1_int) == t1_budunit


def test_BeliefBudHistory_bud_exists_ReturnsObj():
    # ESTABLISH
    sue_beliefbudhistory = beliefbudhistory_shop("Sue")
    t1_int = 145
    assert sue_beliefbudhistory.bud_exists(t1_int) is False

    # WHEN
    t1_budunit = budunit_shop(t1_int, 0)
    sue_beliefbudhistory.set_bud(t1_budunit)

    # THEN
    assert sue_beliefbudhistory.bud_exists(t1_int)


def test_BeliefBudHistory_get_bud_ReturnsObj():
    # ESTABLISH
    sue_beliefbudhistory = beliefbudhistory_shop("sue")
    t1_int = 145
    t1_stat_budunit = budunit_shop(t1_int, 0)
    sue_beliefbudhistory.set_bud(t1_stat_budunit)

    # WHEN
    t1_gen_budunit = sue_beliefbudhistory.get_bud(t1_int)

    # THEN
    assert t1_gen_budunit
    assert t1_gen_budunit == t1_stat_budunit


def test_BeliefBudHistory_del_bud_SetsAttr():
    # ESTABLISH
    sue_beliefbudhistory = beliefbudhistory_shop("Sue")
    t1_int = 145
    t1_stat_budunit = budunit_shop(t1_int, 0)
    sue_beliefbudhistory.set_bud(t1_stat_budunit)
    assert sue_beliefbudhistory.bud_exists(t1_int)

    # WHEN
    sue_beliefbudhistory.del_bud(t1_int)

    # THEN
    assert sue_beliefbudhistory.bud_exists(t1_int) is False


def test_BeliefBudHistory_add_bud_SetsAttr():
    # ESTABLISH
    sue_beliefbudhistory = beliefbudhistory_shop("sue")
    assert sue_beliefbudhistory.buds == {}

    # WHEN
    t1_int = 145
    t1_quota = 500
    sue_beliefbudhistory.add_bud(t1_int, x_quota=t1_quota)

    # THEN
    assert sue_beliefbudhistory.buds != {}
    t1_budunit = budunit_shop(t1_int, t1_quota)
    assert sue_beliefbudhistory.buds.get(t1_int) == t1_budunit


def test_BeliefBudHistory_add_bud_SetsAttr_celldepth():
    # ESTABLISH
    sue_beliefbudhistory = beliefbudhistory_shop("sue")
    assert sue_beliefbudhistory.buds == {}

    # WHEN
    t1_int = 145
    t1_quota = 500
    t1_celldepth = 3
    sue_beliefbudhistory.add_bud(t1_int, t1_quota, t1_celldepth)

    # THEN
    assert sue_beliefbudhistory.buds != {}
    t1_budunit = budunit_shop(t1_int, t1_quota, celldepth=t1_celldepth)
    assert sue_beliefbudhistory.buds.get(t1_int) == t1_budunit


def test_BeliefBudHistory_get_2d_array_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_beliefbudhistory = beliefbudhistory_shop(sue_str)

    # WHEN
    sue_buds_2d_array = sue_beliefbudhistory.get_2d_array()

    # THEN
    assert sue_buds_2d_array == []


def test_BeliefBudHistory_get_2d_array_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_beliefbudhistory = beliefbudhistory_shop(sue_str)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    sue_beliefbudhistory.add_bud(x4_bud_time, x4_quota)
    sue_beliefbudhistory.add_bud(x7_bud_time, x7_quota)

    # WHEN
    sue_buds_2d_array = sue_beliefbudhistory.get_2d_array()

    # THEN
    assert sue_buds_2d_array == [
        [sue_str, x4_bud_time, x4_quota],
        [sue_str, x7_bud_time, x7_quota],
    ]


def test_BeliefBudHistory_get_bud_times_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_beliefbudhistory = beliefbudhistory_shop(sue_str)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    assert sue_beliefbudhistory.get_bud_times() == set()

    # WHEN
    sue_beliefbudhistory.add_bud(x4_bud_time, x4_quota)
    sue_beliefbudhistory.add_bud(x7_bud_time, x7_quota)

    # THEN
    assert sue_beliefbudhistory.get_bud_times() == {x4_bud_time, x7_bud_time}


def test_BeliefBudHistory_get_headers_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_beliefbudhistory = beliefbudhistory_shop(sue_str)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    sue_beliefbudhistory.add_bud(x4_bud_time, x4_quota)
    sue_beliefbudhistory.add_bud(x7_bud_time, x7_quota)

    # WHEN
    sue_headers_list = sue_beliefbudhistory.get_headers()

    # THEN
    assert sue_headers_list == [kw.belief_name, kw.bud_time, kw.quota]


def test_BeliefBudHistory_to_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_beliefbudhistory = beliefbudhistory_shop(sue_str)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    x7_celldepth = 22
    sue_beliefbudhistory.add_bud(x4_bud_time, x4_quota)
    sue_beliefbudhistory.add_bud(x7_bud_time, x7_quota, celldepth=x7_celldepth)

    # WHEN
    sue_buds_dict = sue_beliefbudhistory.to_dict()

    # THEN
    assert sue_buds_dict == {
        kw.belief_name: sue_str,
        "buds": {
            x4_bud_time: {kw.quota: x4_quota, kw.bud_time: x4_bud_time},
            x7_bud_time: {
                kw.quota: x7_quota,
                kw.bud_time: x7_bud_time,
                kw.celldepth: x7_celldepth,
            },
        },
    }


def test_get_beliefbudhistory_from_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_beliefbudhistory = beliefbudhistory_shop(sue_str)
    sue_buds_dict = sue_beliefbudhistory.to_dict()
    assert sue_buds_dict == {kw.belief_name: sue_str, "buds": {}}

    # WHEN
    x_beliefbudhistory = get_beliefbudhistory_from_dict(sue_buds_dict)

    # THEN
    assert x_beliefbudhistory
    assert x_beliefbudhistory.belief_name == sue_str
    assert x_beliefbudhistory.buds == {}
    assert x_beliefbudhistory.buds == sue_beliefbudhistory.buds
    assert x_beliefbudhistory == sue_beliefbudhistory


def test_get_beliefbudhistory_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_beliefbudhistory = beliefbudhistory_shop(sue_str)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    sue_beliefbudhistory.add_bud(x4_bud_time, x4_quota)
    sue_beliefbudhistory.add_bud(x7_bud_time, x7_quota)
    sue_buds_dict = sue_beliefbudhistory.to_dict()
    assert sue_buds_dict == {
        kw.belief_name: sue_str,
        "buds": {
            x4_bud_time: {kw.bud_time: x4_bud_time, kw.quota: x4_quota},
            x7_bud_time: {kw.bud_time: x7_bud_time, kw.quota: x7_quota},
        },
    }

    # WHEN
    x_beliefbudhistory = get_beliefbudhistory_from_dict(sue_buds_dict)

    # THEN
    assert x_beliefbudhistory
    assert x_beliefbudhistory.belief_name == sue_str
    assert x_beliefbudhistory.get_bud(x4_bud_time) != None
    assert x_beliefbudhistory.get_bud(x7_bud_time) != None
    assert x_beliefbudhistory.buds == sue_beliefbudhistory.buds
    assert x_beliefbudhistory == sue_beliefbudhistory


def test_get_beliefbudhistory_from_dict_ReturnsObj_Scenario2():
    # ESTABLISH
    sue_str = "Sue"
    sue_beliefbudhistory = beliefbudhistory_shop(sue_str)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    sue_beliefbudhistory.add_bud(x4_bud_time, x4_quota)
    sue_beliefbudhistory.add_bud(x7_bud_time, x7_quota)
    zia_str = "Zia"
    zia_bud_voice_net = 887
    sue_bud_voice_net = 445
    sue_beliefbudhistory.get_bud(x7_bud_time).set_bud_voice_net(
        sue_str, sue_bud_voice_net
    )
    sue_beliefbudhistory.get_bud(x7_bud_time).set_bud_voice_net(
        zia_str, zia_bud_voice_net
    )
    sue_buds_dict = sue_beliefbudhistory.to_dict()
    assert sue_buds_dict == {
        kw.belief_name: sue_str,
        "buds": {
            x4_bud_time: {kw.bud_time: x4_bud_time, kw.quota: x4_quota},
            x7_bud_time: {
                kw.bud_time: x7_bud_time,
                kw.quota: x7_quota,
                kw.bud_voice_nets: {
                    sue_str: sue_bud_voice_net,
                    zia_str: zia_bud_voice_net,
                },
            },
        },
    }

    # WHEN
    x_beliefbudhistory = get_beliefbudhistory_from_dict(sue_buds_dict)

    # THEN
    assert x_beliefbudhistory
    assert x_beliefbudhistory.belief_name == sue_str
    assert x_beliefbudhistory.get_bud(x4_bud_time) != None
    assert x_beliefbudhistory.get_bud(x7_bud_time) != None
    assert x_beliefbudhistory.get_bud(x7_bud_time)._bud_voice_nets != {}
    assert len(x_beliefbudhistory.get_bud(x7_bud_time)._bud_voice_nets) == 2
    assert x_beliefbudhistory.buds == sue_beliefbudhistory.buds
    assert x_beliefbudhistory == sue_beliefbudhistory


def test_BeliefBudHistory_get_tranbook_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_beliefbudhistory = beliefbudhistory_shop(sue_str)
    x4_bud_time = 4
    x4_quota = 55
    x7_bud_time = 7
    x7_quota = 66
    sue_beliefbudhistory.add_bud(x4_bud_time, x4_quota)
    sue_beliefbudhistory.add_bud(x7_bud_time, x7_quota)
    bob_str = "Bob"
    zia_str = "Zia"
    zia_bud_voice_net = 887
    bob_bud_voice_net = 445
    sue_beliefbudhistory.get_bud(x4_bud_time).set_bud_voice_net(
        bob_str, bob_bud_voice_net
    )
    sue_beliefbudhistory.get_bud(x7_bud_time).set_bud_voice_net(
        zia_str, zia_bud_voice_net
    )
    sue_buds_dict = sue_beliefbudhistory.to_dict()
    assert sue_buds_dict == {
        kw.belief_name: sue_str,
        "buds": {
            x4_bud_time: {
                kw.bud_time: x4_bud_time,
                kw.quota: x4_quota,
                kw.bud_voice_nets: {bob_str: bob_bud_voice_net},
            },
            x7_bud_time: {
                kw.bud_time: x7_bud_time,
                kw.quota: x7_quota,
                kw.bud_voice_nets: {zia_str: zia_bud_voice_net},
            },
        },
    }

    # WHEN
    x_moment_label = "moment_label_x"
    sue_tranbook = sue_beliefbudhistory.get_tranbook(x_moment_label)

    # THEN
    assert sue_tranbook
    assert sue_tranbook.moment_label == x_moment_label
    assert sue_tranbook.tranunit_exists(sue_str, zia_str, x7_bud_time)
    assert sue_tranbook.tranunit_exists(sue_str, bob_str, x4_bud_time)
    assert sue_tranbook.get_amount(sue_str, zia_str, x7_bud_time) == zia_bud_voice_net
    assert sue_tranbook.get_amount(sue_str, bob_str, x4_bud_time) == bob_bud_voice_net
