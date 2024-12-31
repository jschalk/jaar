from src.f01_road.finance import default_fund_pool
from src.f01_road.finance_tran import (
    quota_str,
    time_int_str,
    bridge_str,
    TurnEpisode,
    turnepisode_shop,
    TurnLog,
    turnlog_shop,
    get_turnepisode_from_dict,
    get_turnepisode_from_json,
    get_turnlog_from_dict,
)
from pytest import raises as pytest_raises


def test_str_functions_ReturnObj():
    assert bridge_str() == "bridge"
    assert time_int_str() == "time_int"
    assert quota_str() == "quota"


def test_TurnEpisode_Exists():
    # ESTABLISH / WHEN
    x_turnepisode = TurnEpisode()

    # THEN
    assert x_turnepisode
    assert not x_turnepisode.time_int
    assert not x_turnepisode.quota
    assert not x_turnepisode._net_turns
    assert not x_turnepisode._magnitude


def test_turnepisode_shop_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4

    # WHEN
    t4_turnepisode = turnepisode_shop(t4_time_int)

    # THEN
    assert t4_turnepisode
    assert t4_turnepisode.time_int == t4_time_int
    assert t4_turnepisode.quota == default_fund_pool()
    assert t4_turnepisode._magnitude == 0
    assert not t4_turnepisode._net_turns


def test_turnepisode_shop_ReturnsObjWith_net_turns():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_net_turns = {"Sue": -4}
    t4_magnitude = 677

    # WHEN
    x_turnepisode = turnepisode_shop(
        x_time_int=t4_time_int,
        x_quota=t4_quota,
        net_turns=t4_net_turns,
        x_magnitude=t4_magnitude,
    )

    # THEN
    assert x_turnepisode
    assert x_turnepisode.time_int == t4_time_int
    assert x_turnepisode.quota == t4_quota
    assert x_turnepisode._magnitude == 677
    assert x_turnepisode._net_turns == t4_net_turns


def test_TurnEpisode_set_net_turn_SetsAttr():
    # ESTABLISH
    yao_turnepisode = turnepisode_shop("yao", 33)
    assert yao_turnepisode._net_turns == {}

    # WHEN
    sue_str = "Sue"
    sue_turn = -44
    yao_turnepisode.set_net_turn(sue_str, sue_turn)

    # THEN
    assert yao_turnepisode._net_turns != {}
    assert yao_turnepisode._net_turns.get(sue_str) == sue_turn


def test_TurnEpisode_net_turn_exists_ReturnsObj():
    # ESTABLISH
    yao_turnepisode = turnepisode_shop("yao", 33)
    sue_str = "Sue"
    sue_turn = -44
    assert yao_turnepisode.net_turn_exists(sue_str) is False

    # WHEN
    yao_turnepisode.set_net_turn(sue_str, sue_turn)

    # THEN
    assert yao_turnepisode.net_turn_exists(sue_str)


def test_TurnEpisode_get_net_turn_ReturnsObj():
    # ESTABLISH
    yao_turnepisode = turnepisode_shop("yao", 33)
    sue_str = "Sue"
    sue_turn = -44
    yao_turnepisode.set_net_turn(sue_str, sue_turn)

    # WHEN / THEN
    assert yao_turnepisode.get_net_turn(sue_str)
    assert yao_turnepisode.get_net_turn(sue_str) == sue_turn


def test_TurnEpisode_del_net_turn_SetsAttr():
    # ESTABLISH
    yao_turnepisode = turnepisode_shop("yao", 33)
    sue_str = "Sue"
    sue_turn = -44
    yao_turnepisode.set_net_turn(sue_str, sue_turn)
    assert yao_turnepisode.net_turn_exists(sue_str)

    # WHEN
    yao_turnepisode.del_net_turn(sue_str)

    # THEN
    assert yao_turnepisode.net_turn_exists(sue_str) is False


def test_TurnEpisode_get_dict_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_turnepisode = turnepisode_shop(t4_time_int, t4_quota)

    # WHEN
    t4_dict = t4_turnepisode.get_dict()

    # THEN
    assert t4_dict == {"time_int": t4_time_int, quota_str(): t4_quota}


def test_TurnEpisode_calc_magnitude_SetsAttr_Scenario0():
    # ESTABLISH
    t4_time_int = 4
    t4_turnepisode = turnepisode_shop(t4_time_int)
    assert t4_turnepisode._magnitude == 0

    # WHEN
    t4_turnepisode.calc_magnitude()

    # THEN
    assert t4_turnepisode._magnitude == 0


def test_TurnEpisode_calc_magnitude_SetsAttr_Scenario1():
    # ESTABLISH
    t4_time_int = 4
    t4_net_turns = {"Sue": -4, "Yao": 2, "Zia": 2}

    t4_turnepisode = turnepisode_shop(t4_time_int, net_turns=t4_net_turns)
    assert t4_turnepisode._magnitude == 0

    # WHEN
    t4_turnepisode.calc_magnitude()

    # THEN
    assert t4_turnepisode._magnitude == 4


def test_TurnEpisode_calc_magnitude_SetsAttr_Scenario2():
    # ESTABLISH
    t4_time_int = 4
    t4_net_turns = {"Bob": -13, "Sue": -7, "Yao": 18, "Zia": 2}

    t4_turnepisode = turnepisode_shop(t4_time_int, net_turns=t4_net_turns)
    assert t4_turnepisode._magnitude == 0

    # WHEN
    t4_turnepisode.calc_magnitude()

    # THEN
    assert t4_turnepisode._magnitude == 20


def test_TurnEpisode_calc_magnitude_SetsAttr_Scenario3_RaisesError():
    # ESTABLISH
    t4_time_int = 4
    bob_turn = -13
    sue_turn = -3
    yao_turn = 100
    t4_net_turns = {"Bob": bob_turn, "Sue": sue_turn, "Yao": yao_turn}
    t4_turnepisode = turnepisode_shop(t4_time_int, net_turns=t4_net_turns)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        t4_turnepisode.calc_magnitude()
    exception_str = f"magnitude cannot be calculated: debt_turn={bob_turn+sue_turn}, cred_turn={yao_turn}"
    assert str(excinfo.value) == exception_str


def test_TurnEpisode_get_dict_ReturnsObjWith_net_turns():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_net_turns = {"Sue": -4}
    t4_magnitude = 67
    t4_turnepisode = turnepisode_shop(t4_time_int, t4_quota, t4_net_turns)
    t4_turnepisode._magnitude = 67

    # WHEN
    t4_dict = t4_turnepisode.get_dict()

    # THEN
    assert t4_dict == {
        "time_int": t4_time_int,
        quota_str(): t4_quota,
        "magnitude": t4_magnitude,
        "net_turns": t4_net_turns,
    }


def test_TurnEpisode_get_json_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_net_turns = {"Sue": -77}
    t4_turnepisode = turnepisode_shop(t4_time_int, t4_quota, t4_net_turns)
    t4_turnepisode._magnitude = 67

    # WHEN
    t4_json = t4_turnepisode.get_json()

    # THEN
    static_t4_json = """{
  "magnitude": 67,
  "net_turns": {
    "Sue": -77
  },
  "quota": 55,
  "time_int": 4
}"""
    print(f"{t4_json=}")
    assert t4_json == static_t4_json


def test_get_turnepisode_from_dict_ReturnsObj_Sccenario0():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_turnepisode = turnepisode_shop(t4_time_int, t4_quota)
    t4_dict = t4_turnepisode.get_dict()
    assert t4_dict == {"time_int": t4_time_int, quota_str(): t4_quota}

    # WHEN
    x_turnepisode = get_turnepisode_from_dict(t4_dict)

    # THEN
    assert x_turnepisode
    assert x_turnepisode.time_int == t4_time_int
    assert x_turnepisode.quota == t4_quota
    assert x_turnepisode._magnitude == 0
    assert x_turnepisode == t4_turnepisode


def test_get_turnepisode_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_magnitude = 65
    t4_net_turns = {"Sue": -77}
    t4_turnepisode = turnepisode_shop(t4_time_int, t4_quota, t4_net_turns)
    t4_turnepisode._magnitude = t4_magnitude
    t4_dict = t4_turnepisode.get_dict()

    # WHEN
    x_turnepisode = get_turnepisode_from_dict(t4_dict)

    # THEN
    assert x_turnepisode
    assert x_turnepisode.time_int == t4_time_int
    assert x_turnepisode.quota == t4_quota
    assert x_turnepisode._magnitude == t4_magnitude
    assert x_turnepisode._net_turns == t4_net_turns
    assert x_turnepisode == t4_turnepisode


def test_get_turnepisode_from_json_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_net_turns = {"Sue": -57}
    t4_turnepisode = turnepisode_shop(t4_time_int, t4_quota, t4_net_turns)
    t4_json = t4_turnepisode.get_json()

    # WHEN
    x_turnepisode = get_turnepisode_from_json(t4_json)

    # THEN
    assert x_turnepisode
    assert x_turnepisode.time_int == t4_time_int
    assert x_turnepisode.quota == t4_quota
    assert x_turnepisode._net_turns == t4_net_turns
    assert x_turnepisode == t4_turnepisode


def test_TurnLog_Exists():
    # ESTABLISH / WHEN
    x_turnlog = TurnLog()

    # THEN
    assert x_turnlog
    assert not x_turnlog.owner_name
    assert not x_turnlog.episodes
    assert not x_turnlog._sum_turnepisode_quota
    assert not x_turnlog._sum_acct_turns
    assert not x_turnlog._time_int_min
    assert not x_turnlog._time_int_max


def test_turnlog_shop_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"

    # WHEN
    x_turnlog = turnlog_shop(sue_str)

    # THEN
    assert x_turnlog
    assert x_turnlog.owner_name == sue_str
    assert x_turnlog.episodes == {}
    assert not x_turnlog._sum_turnepisode_quota
    assert x_turnlog._sum_acct_turns == {}
    assert not x_turnlog._time_int_min
    assert not x_turnlog._time_int_max


def test_TurnLog_set_episode_SetsAttr():
    # ESTABLISH
    sue_turnlog = turnlog_shop("sue")
    assert sue_turnlog.episodes == {}

    # WHEN
    t1_int = 145
    t1_turnepisode = turnepisode_shop(t1_int, 0)
    sue_turnlog.set_episode(t1_turnepisode)

    # THEN
    assert sue_turnlog.episodes != {}
    assert sue_turnlog.episodes.get(t1_int) == t1_turnepisode


def test_TurnLog_episode_exists_ReturnsObj():
    # ESTABLISH
    sue_turnlog = turnlog_shop("Sue")
    t1_int = 145
    assert sue_turnlog.episode_exists(t1_int) is False

    # WHEN
    t1_turnepisode = turnepisode_shop(t1_int, 0)
    sue_turnlog.set_episode(t1_turnepisode)

    # THEN
    assert sue_turnlog.episode_exists(t1_int)


def test_TurnLog_get_episode_ReturnsObj():
    # ESTABLISH
    sue_turnlog = turnlog_shop("sue")
    t1_int = 145
    t1_stat_turnepisode = turnepisode_shop(t1_int, 0)
    sue_turnlog.set_episode(t1_stat_turnepisode)

    # WHEN
    t1_gen_turnepisode = sue_turnlog.get_episode(t1_int)

    # THEN
    assert t1_gen_turnepisode
    assert t1_gen_turnepisode == t1_stat_turnepisode


def test_TurnLog_del_episode_SetsAttr():
    # ESTABLISH
    sue_turnlog = turnlog_shop("Sue")
    t1_int = 145
    t1_stat_turnepisode = turnepisode_shop(t1_int, 0)
    sue_turnlog.set_episode(t1_stat_turnepisode)
    assert sue_turnlog.episode_exists(t1_int)

    # WHEN
    sue_turnlog.del_episode(t1_int)

    # THEN
    assert sue_turnlog.episode_exists(t1_int) is False


def test_TurnLog_add_episode_SetsAttr():
    # ESTABLISH
    sue_turnlog = turnlog_shop("sue")
    assert sue_turnlog.episodes == {}

    # WHEN
    t1_int = 145
    t1_quota = 500
    sue_turnlog.add_episode(t1_int, x_quota=t1_quota)

    # THEN
    assert sue_turnlog.episodes != {}
    t1_turnepisode = turnepisode_shop(t1_int, t1_quota)
    assert sue_turnlog.episodes.get(t1_int) == t1_turnepisode


def test_TurnLog_get_2d_array_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_turnlog = turnlog_shop(sue_str)

    # WHEN
    sue_episodes_2d_array = sue_turnlog.get_2d_array()

    # THEN
    assert sue_episodes_2d_array == []


def test_TurnLog_get_2d_array_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_turnlog = turnlog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_turnlog.add_episode(x4_time_int, x4_quota)
    sue_turnlog.add_episode(x7_time_int, x7_quota)

    # WHEN
    sue_episodes_2d_array = sue_turnlog.get_2d_array()

    # THEN
    assert sue_episodes_2d_array == [
        [sue_str, x4_time_int, x4_quota],
        [sue_str, x7_time_int, x7_quota],
    ]


def test_TurnLog_get_time_ints_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_turnlog = turnlog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    assert sue_turnlog.get_time_ints() == set()

    # WHEN
    sue_turnlog.add_episode(x4_time_int, x4_quota)
    sue_turnlog.add_episode(x7_time_int, x7_quota)

    # THEN
    assert sue_turnlog.get_time_ints() == {x4_time_int, x7_time_int}


def test_TurnLog_get_headers_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_turnlog = turnlog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_turnlog.add_episode(x4_time_int, x4_quota)
    sue_turnlog.add_episode(x7_time_int, x7_quota)

    # WHEN
    sue_headers_list = sue_turnlog.get_headers()

    # THEN
    assert sue_headers_list == ["owner_name", "time_int", quota_str()]


def test_TurnLog_get_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_turnlog = turnlog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_turnlog.add_episode(x4_time_int, x4_quota)
    sue_turnlog.add_episode(x7_time_int, x7_quota)

    # WHEN
    sue_episodes_dict = sue_turnlog.get_dict()

    # THEN
    assert sue_episodes_dict == {
        "owner_name": sue_str,
        "episodes": {
            x4_time_int: {quota_str(): x4_quota, "time_int": x4_time_int},
            x7_time_int: {quota_str(): x7_quota, "time_int": x7_time_int},
        },
    }


def test_get_turnlog_from_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_turnlog = turnlog_shop(sue_str)
    sue_episodes_dict = sue_turnlog.get_dict()
    assert sue_episodes_dict == {"owner_name": sue_str, "episodes": {}}

    # WHEN
    x_turnlog = get_turnlog_from_dict(sue_episodes_dict)

    # THEN
    assert x_turnlog
    assert x_turnlog.owner_name == sue_str
    assert x_turnlog.episodes == {}
    assert x_turnlog.episodes == sue_turnlog.episodes
    assert x_turnlog == sue_turnlog


def test_get_turnlog_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_turnlog = turnlog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_turnlog.add_episode(x4_time_int, x4_quota)
    sue_turnlog.add_episode(x7_time_int, x7_quota)
    sue_episodes_dict = sue_turnlog.get_dict()
    assert sue_episodes_dict == {
        "owner_name": sue_str,
        "episodes": {
            x4_time_int: {"time_int": x4_time_int, quota_str(): x4_quota},
            x7_time_int: {"time_int": x7_time_int, quota_str(): x7_quota},
        },
    }

    # WHEN
    x_turnlog = get_turnlog_from_dict(sue_episodes_dict)

    # THEN
    assert x_turnlog
    assert x_turnlog.owner_name == sue_str
    assert x_turnlog.get_episode(x4_time_int) != None
    assert x_turnlog.get_episode(x7_time_int) != None
    assert x_turnlog.episodes == sue_turnlog.episodes
    assert x_turnlog == sue_turnlog


def test_get_turnlog_from_dict_ReturnsObj_Scenario2():
    # ESTABLISH
    sue_str = "Sue"
    sue_turnlog = turnlog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_turnlog.add_episode(x4_time_int, x4_quota)
    sue_turnlog.add_episode(x7_time_int, x7_quota)
    zia_str = "Zia"
    zia_net_turn = 887
    sue_net_turn = 445
    sue_turnlog.get_episode(x7_time_int).set_net_turn(sue_str, sue_net_turn)
    sue_turnlog.get_episode(x7_time_int).set_net_turn(zia_str, zia_net_turn)
    sue_episodes_dict = sue_turnlog.get_dict()
    assert sue_episodes_dict == {
        "owner_name": sue_str,
        "episodes": {
            x4_time_int: {"time_int": x4_time_int, quota_str(): x4_quota},
            x7_time_int: {
                "time_int": x7_time_int,
                quota_str(): x7_quota,
                "net_turns": {sue_str: sue_net_turn, zia_str: zia_net_turn},
            },
        },
    }

    # WHEN
    x_turnlog = get_turnlog_from_dict(sue_episodes_dict)

    # THEN
    assert x_turnlog
    assert x_turnlog.owner_name == sue_str
    assert x_turnlog.get_episode(x4_time_int) != None
    assert x_turnlog.get_episode(x7_time_int) != None
    assert x_turnlog.get_episode(x7_time_int)._net_turns != {}
    assert len(x_turnlog.get_episode(x7_time_int)._net_turns) == 2
    assert x_turnlog.episodes == sue_turnlog.episodes
    assert x_turnlog == sue_turnlog


def test_TurnLog_get_tranbook_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_turnlog = turnlog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_turnlog.add_episode(x4_time_int, x4_quota)
    sue_turnlog.add_episode(x7_time_int, x7_quota)
    bob_str = "Bob"
    zia_str = "Zia"
    zia_net_turn = 887
    bob_net_turn = 445
    sue_turnlog.get_episode(x4_time_int).set_net_turn(bob_str, bob_net_turn)
    sue_turnlog.get_episode(x7_time_int).set_net_turn(zia_str, zia_net_turn)
    sue_episodes_dict = sue_turnlog.get_dict()
    assert sue_episodes_dict == {
        "owner_name": sue_str,
        "episodes": {
            x4_time_int: {
                "time_int": x4_time_int,
                quota_str(): x4_quota,
                "net_turns": {bob_str: bob_net_turn},
            },
            x7_time_int: {
                "time_int": x7_time_int,
                quota_str(): x7_quota,
                "net_turns": {zia_str: zia_net_turn},
            },
        },
    }

    # WHEN
    x_deal_idea = "deal_idea_x"
    sue_tranbook = sue_turnlog.get_tranbook(x_deal_idea)

    # THEN
    assert sue_tranbook
    assert sue_tranbook.deal_idea == x_deal_idea
    assert sue_tranbook.tranunit_exists(sue_str, zia_str, x7_time_int)
    assert sue_tranbook.tranunit_exists(sue_str, bob_str, x4_time_int)
    assert sue_tranbook.get_amount(sue_str, zia_str, x7_time_int) == zia_net_turn
    assert sue_tranbook.get_amount(sue_str, bob_str, x4_time_int) == bob_net_turn
