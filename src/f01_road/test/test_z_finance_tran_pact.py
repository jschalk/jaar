from src.f01_road.finance import default_fund_pool
from src.f01_road.finance_tran import (
    quota_str,
    time_int_str,
    bridge_str,
    PactEpisode,
    pactepisode_shop,
    PactLog,
    pactlog_shop,
    get_pactepisode_from_dict,
    get_pactepisode_from_json,
    get_pactlog_from_dict,
)
from pytest import raises as pytest_raises


def test_str_functions_ReturnObj():
    assert bridge_str() == "bridge"
    assert time_int_str() == "time_int"
    assert quota_str() == "quota"


def test_PactEpisode_Exists():
    # ESTABLISH / WHEN
    x_pactepisode = PactEpisode()

    # THEN
    assert x_pactepisode
    assert not x_pactepisode.time_int
    assert not x_pactepisode.quota
    assert not x_pactepisode._net_pacts
    assert not x_pactepisode._magnitude


def test_pactepisode_shop_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4

    # WHEN
    t4_pactepisode = pactepisode_shop(t4_time_int)

    # THEN
    assert t4_pactepisode
    assert t4_pactepisode.time_int == t4_time_int
    assert t4_pactepisode.quota == default_fund_pool()
    assert t4_pactepisode._magnitude == 0
    assert not t4_pactepisode._net_pacts


def test_pactepisode_shop_ReturnsObjWith_net_pacts():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_net_pacts = {"Sue": -4}
    t4_magnitude = 677

    # WHEN
    x_pactepisode = pactepisode_shop(
        x_time_int=t4_time_int,
        x_quota=t4_quota,
        net_pacts=t4_net_pacts,
        x_magnitude=t4_magnitude,
    )

    # THEN
    assert x_pactepisode
    assert x_pactepisode.time_int == t4_time_int
    assert x_pactepisode.quota == t4_quota
    assert x_pactepisode._magnitude == 677
    assert x_pactepisode._net_pacts == t4_net_pacts


def test_PactEpisode_set_net_pact_SetsAttr():
    # ESTABLISH
    yao_pactepisode = pactepisode_shop("yao", 33)
    assert yao_pactepisode._net_pacts == {}

    # WHEN
    sue_str = "Sue"
    sue_pact = -44
    yao_pactepisode.set_net_pact(sue_str, sue_pact)

    # THEN
    assert yao_pactepisode._net_pacts != {}
    assert yao_pactepisode._net_pacts.get(sue_str) == sue_pact


def test_PactEpisode_net_pact_exists_ReturnsObj():
    # ESTABLISH
    yao_pactepisode = pactepisode_shop("yao", 33)
    sue_str = "Sue"
    sue_pact = -44
    assert yao_pactepisode.net_pact_exists(sue_str) is False

    # WHEN
    yao_pactepisode.set_net_pact(sue_str, sue_pact)

    # THEN
    assert yao_pactepisode.net_pact_exists(sue_str)


def test_PactEpisode_get_net_pact_ReturnsObj():
    # ESTABLISH
    yao_pactepisode = pactepisode_shop("yao", 33)
    sue_str = "Sue"
    sue_pact = -44
    yao_pactepisode.set_net_pact(sue_str, sue_pact)

    # WHEN / THEN
    assert yao_pactepisode.get_net_pact(sue_str)
    assert yao_pactepisode.get_net_pact(sue_str) == sue_pact


def test_PactEpisode_del_net_pact_SetsAttr():
    # ESTABLISH
    yao_pactepisode = pactepisode_shop("yao", 33)
    sue_str = "Sue"
    sue_pact = -44
    yao_pactepisode.set_net_pact(sue_str, sue_pact)
    assert yao_pactepisode.net_pact_exists(sue_str)

    # WHEN
    yao_pactepisode.del_net_pact(sue_str)

    # THEN
    assert yao_pactepisode.net_pact_exists(sue_str) is False


def test_PactEpisode_get_dict_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_pactepisode = pactepisode_shop(t4_time_int, t4_quota)

    # WHEN
    t4_dict = t4_pactepisode.get_dict()

    # THEN
    assert t4_dict == {"time_int": t4_time_int, quota_str(): t4_quota}


def test_PactEpisode_calc_magnitude_SetsAttr_Scenario0():
    # ESTABLISH
    t4_time_int = 4
    t4_pactepisode = pactepisode_shop(t4_time_int)
    assert t4_pactepisode._magnitude == 0

    # WHEN
    t4_pactepisode.calc_magnitude()

    # THEN
    assert t4_pactepisode._magnitude == 0


def test_PactEpisode_calc_magnitude_SetsAttr_Scenario1():
    # ESTABLISH
    t4_time_int = 4
    t4_net_pacts = {"Sue": -4, "Yao": 2, "Zia": 2}

    t4_pactepisode = pactepisode_shop(t4_time_int, net_pacts=t4_net_pacts)
    assert t4_pactepisode._magnitude == 0

    # WHEN
    t4_pactepisode.calc_magnitude()

    # THEN
    assert t4_pactepisode._magnitude == 4


def test_PactEpisode_calc_magnitude_SetsAttr_Scenario2():
    # ESTABLISH
    t4_time_int = 4
    t4_net_pacts = {"Bob": -13, "Sue": -7, "Yao": 18, "Zia": 2}

    t4_pactepisode = pactepisode_shop(t4_time_int, net_pacts=t4_net_pacts)
    assert t4_pactepisode._magnitude == 0

    # WHEN
    t4_pactepisode.calc_magnitude()

    # THEN
    assert t4_pactepisode._magnitude == 20


def test_PactEpisode_calc_magnitude_SetsAttr_Scenario3_RaisesError():
    # ESTABLISH
    t4_time_int = 4
    bob_pact = -13
    sue_pact = -3
    yao_pact = 100
    t4_net_pacts = {"Bob": bob_pact, "Sue": sue_pact, "Yao": yao_pact}
    t4_pactepisode = pactepisode_shop(t4_time_int, net_pacts=t4_net_pacts)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        t4_pactepisode.calc_magnitude()
    exception_str = f"magnitude cannot be calculated: debt_pact={bob_pact+sue_pact}, cred_pact={yao_pact}"
    assert str(excinfo.value) == exception_str


def test_PactEpisode_get_dict_ReturnsObjWith_net_pacts():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_net_pacts = {"Sue": -4}
    t4_magnitude = 67
    t4_pactepisode = pactepisode_shop(t4_time_int, t4_quota, t4_net_pacts)
    t4_pactepisode._magnitude = 67

    # WHEN
    t4_dict = t4_pactepisode.get_dict()

    # THEN
    assert t4_dict == {
        "time_int": t4_time_int,
        quota_str(): t4_quota,
        "magnitude": t4_magnitude,
        "net_pacts": t4_net_pacts,
    }


def test_PactEpisode_get_json_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_net_pacts = {"Sue": -77}
    t4_pactepisode = pactepisode_shop(t4_time_int, t4_quota, t4_net_pacts)
    t4_pactepisode._magnitude = 67

    # WHEN
    t4_json = t4_pactepisode.get_json()

    # THEN
    static_t4_json = """{
  "magnitude": 67,
  "net_pacts": {
    "Sue": -77
  },
  "quota": 55,
  "time_int": 4
}"""
    print(f"{t4_json=}")
    assert t4_json == static_t4_json


def test_get_pactepisode_from_dict_ReturnsObj_Sccenario0():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_pactepisode = pactepisode_shop(t4_time_int, t4_quota)
    t4_dict = t4_pactepisode.get_dict()
    assert t4_dict == {"time_int": t4_time_int, quota_str(): t4_quota}

    # WHEN
    x_pactepisode = get_pactepisode_from_dict(t4_dict)

    # THEN
    assert x_pactepisode
    assert x_pactepisode.time_int == t4_time_int
    assert x_pactepisode.quota == t4_quota
    assert x_pactepisode._magnitude == 0
    assert x_pactepisode == t4_pactepisode


def test_get_pactepisode_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_magnitude = 65
    t4_net_pacts = {"Sue": -77}
    t4_pactepisode = pactepisode_shop(t4_time_int, t4_quota, t4_net_pacts)
    t4_pactepisode._magnitude = t4_magnitude
    t4_dict = t4_pactepisode.get_dict()

    # WHEN
    x_pactepisode = get_pactepisode_from_dict(t4_dict)

    # THEN
    assert x_pactepisode
    assert x_pactepisode.time_int == t4_time_int
    assert x_pactepisode.quota == t4_quota
    assert x_pactepisode._magnitude == t4_magnitude
    assert x_pactepisode._net_pacts == t4_net_pacts
    assert x_pactepisode == t4_pactepisode


def test_get_pactepisode_from_json_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_net_pacts = {"Sue": -57}
    t4_pactepisode = pactepisode_shop(t4_time_int, t4_quota, t4_net_pacts)
    t4_json = t4_pactepisode.get_json()

    # WHEN
    x_pactepisode = get_pactepisode_from_json(t4_json)

    # THEN
    assert x_pactepisode
    assert x_pactepisode.time_int == t4_time_int
    assert x_pactepisode.quota == t4_quota
    assert x_pactepisode._net_pacts == t4_net_pacts
    assert x_pactepisode == t4_pactepisode


def test_PactLog_Exists():
    # ESTABLISH / WHEN
    x_pactlog = PactLog()

    # THEN
    assert x_pactlog
    assert not x_pactlog.owner_name
    assert not x_pactlog.episodes
    assert not x_pactlog._sum_pactepisode_quota
    assert not x_pactlog._sum_acct_pacts
    assert not x_pactlog._time_int_min
    assert not x_pactlog._time_int_max


def test_pactlog_shop_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"

    # WHEN
    x_pactlog = pactlog_shop(sue_str)

    # THEN
    assert x_pactlog
    assert x_pactlog.owner_name == sue_str
    assert x_pactlog.episodes == {}
    assert not x_pactlog._sum_pactepisode_quota
    assert x_pactlog._sum_acct_pacts == {}
    assert not x_pactlog._time_int_min
    assert not x_pactlog._time_int_max


def test_PactLog_set_episode_SetsAttr():
    # ESTABLISH
    sue_pactlog = pactlog_shop("sue")
    assert sue_pactlog.episodes == {}

    # WHEN
    t1_int = 145
    t1_pactepisode = pactepisode_shop(t1_int, 0)
    sue_pactlog.set_episode(t1_pactepisode)

    # THEN
    assert sue_pactlog.episodes != {}
    assert sue_pactlog.episodes.get(t1_int) == t1_pactepisode


def test_PactLog_episode_exists_ReturnsObj():
    # ESTABLISH
    sue_pactlog = pactlog_shop("Sue")
    t1_int = 145
    assert sue_pactlog.episode_exists(t1_int) is False

    # WHEN
    t1_pactepisode = pactepisode_shop(t1_int, 0)
    sue_pactlog.set_episode(t1_pactepisode)

    # THEN
    assert sue_pactlog.episode_exists(t1_int)


def test_PactLog_get_episode_ReturnsObj():
    # ESTABLISH
    sue_pactlog = pactlog_shop("sue")
    t1_int = 145
    t1_stat_pactepisode = pactepisode_shop(t1_int, 0)
    sue_pactlog.set_episode(t1_stat_pactepisode)

    # WHEN
    t1_gen_pactepisode = sue_pactlog.get_episode(t1_int)

    # THEN
    assert t1_gen_pactepisode
    assert t1_gen_pactepisode == t1_stat_pactepisode


def test_PactLog_del_episode_SetsAttr():
    # ESTABLISH
    sue_pactlog = pactlog_shop("Sue")
    t1_int = 145
    t1_stat_pactepisode = pactepisode_shop(t1_int, 0)
    sue_pactlog.set_episode(t1_stat_pactepisode)
    assert sue_pactlog.episode_exists(t1_int)

    # WHEN
    sue_pactlog.del_episode(t1_int)

    # THEN
    assert sue_pactlog.episode_exists(t1_int) is False


def test_PactLog_add_episode_SetsAttr():
    # ESTABLISH
    sue_pactlog = pactlog_shop("sue")
    assert sue_pactlog.episodes == {}

    # WHEN
    t1_int = 145
    t1_quota = 500
    sue_pactlog.add_episode(t1_int, x_quota=t1_quota)

    # THEN
    assert sue_pactlog.episodes != {}
    t1_pactepisode = pactepisode_shop(t1_int, t1_quota)
    assert sue_pactlog.episodes.get(t1_int) == t1_pactepisode


def test_PactLog_get_2d_array_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_pactlog = pactlog_shop(sue_str)

    # WHEN
    sue_episodes_2d_array = sue_pactlog.get_2d_array()

    # THEN
    assert sue_episodes_2d_array == []


def test_PactLog_get_2d_array_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_pactlog = pactlog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_pactlog.add_episode(x4_time_int, x4_quota)
    sue_pactlog.add_episode(x7_time_int, x7_quota)

    # WHEN
    sue_episodes_2d_array = sue_pactlog.get_2d_array()

    # THEN
    assert sue_episodes_2d_array == [
        [sue_str, x4_time_int, x4_quota],
        [sue_str, x7_time_int, x7_quota],
    ]


def test_PactLog_get_time_ints_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pactlog = pactlog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    assert sue_pactlog.get_time_ints() == set()

    # WHEN
    sue_pactlog.add_episode(x4_time_int, x4_quota)
    sue_pactlog.add_episode(x7_time_int, x7_quota)

    # THEN
    assert sue_pactlog.get_time_ints() == {x4_time_int, x7_time_int}


def test_PactLog_get_headers_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pactlog = pactlog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_pactlog.add_episode(x4_time_int, x4_quota)
    sue_pactlog.add_episode(x7_time_int, x7_quota)

    # WHEN
    sue_headers_list = sue_pactlog.get_headers()

    # THEN
    assert sue_headers_list == ["owner_name", "time_int", quota_str()]


def test_PactLog_get_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_pactlog = pactlog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_pactlog.add_episode(x4_time_int, x4_quota)
    sue_pactlog.add_episode(x7_time_int, x7_quota)

    # WHEN
    sue_episodes_dict = sue_pactlog.get_dict()

    # THEN
    assert sue_episodes_dict == {
        "owner_name": sue_str,
        "episodes": {
            x4_time_int: {quota_str(): x4_quota, "time_int": x4_time_int},
            x7_time_int: {quota_str(): x7_quota, "time_int": x7_time_int},
        },
    }


def test_get_pactlog_from_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_pactlog = pactlog_shop(sue_str)
    sue_episodes_dict = sue_pactlog.get_dict()
    assert sue_episodes_dict == {"owner_name": sue_str, "episodes": {}}

    # WHEN
    x_pactlog = get_pactlog_from_dict(sue_episodes_dict)

    # THEN
    assert x_pactlog
    assert x_pactlog.owner_name == sue_str
    assert x_pactlog.episodes == {}
    assert x_pactlog.episodes == sue_pactlog.episodes
    assert x_pactlog == sue_pactlog


def test_get_pactlog_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_pactlog = pactlog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_pactlog.add_episode(x4_time_int, x4_quota)
    sue_pactlog.add_episode(x7_time_int, x7_quota)
    sue_episodes_dict = sue_pactlog.get_dict()
    assert sue_episodes_dict == {
        "owner_name": sue_str,
        "episodes": {
            x4_time_int: {"time_int": x4_time_int, quota_str(): x4_quota},
            x7_time_int: {"time_int": x7_time_int, quota_str(): x7_quota},
        },
    }

    # WHEN
    x_pactlog = get_pactlog_from_dict(sue_episodes_dict)

    # THEN
    assert x_pactlog
    assert x_pactlog.owner_name == sue_str
    assert x_pactlog.get_episode(x4_time_int) != None
    assert x_pactlog.get_episode(x7_time_int) != None
    assert x_pactlog.episodes == sue_pactlog.episodes
    assert x_pactlog == sue_pactlog


def test_get_pactlog_from_dict_ReturnsObj_Scenario2():
    # ESTABLISH
    sue_str = "Sue"
    sue_pactlog = pactlog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_pactlog.add_episode(x4_time_int, x4_quota)
    sue_pactlog.add_episode(x7_time_int, x7_quota)
    zia_str = "Zia"
    zia_net_pact = 887
    sue_net_pact = 445
    sue_pactlog.get_episode(x7_time_int).set_net_pact(sue_str, sue_net_pact)
    sue_pactlog.get_episode(x7_time_int).set_net_pact(zia_str, zia_net_pact)
    sue_episodes_dict = sue_pactlog.get_dict()
    assert sue_episodes_dict == {
        "owner_name": sue_str,
        "episodes": {
            x4_time_int: {"time_int": x4_time_int, quota_str(): x4_quota},
            x7_time_int: {
                "time_int": x7_time_int,
                quota_str(): x7_quota,
                "net_pacts": {sue_str: sue_net_pact, zia_str: zia_net_pact},
            },
        },
    }

    # WHEN
    x_pactlog = get_pactlog_from_dict(sue_episodes_dict)

    # THEN
    assert x_pactlog
    assert x_pactlog.owner_name == sue_str
    assert x_pactlog.get_episode(x4_time_int) != None
    assert x_pactlog.get_episode(x7_time_int) != None
    assert x_pactlog.get_episode(x7_time_int)._net_pacts != {}
    assert len(x_pactlog.get_episode(x7_time_int)._net_pacts) == 2
    assert x_pactlog.episodes == sue_pactlog.episodes
    assert x_pactlog == sue_pactlog


def test_PactLog_get_tranbook_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_pactlog = pactlog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_pactlog.add_episode(x4_time_int, x4_quota)
    sue_pactlog.add_episode(x7_time_int, x7_quota)
    bob_str = "Bob"
    zia_str = "Zia"
    zia_net_pact = 887
    bob_net_pact = 445
    sue_pactlog.get_episode(x4_time_int).set_net_pact(bob_str, bob_net_pact)
    sue_pactlog.get_episode(x7_time_int).set_net_pact(zia_str, zia_net_pact)
    sue_episodes_dict = sue_pactlog.get_dict()
    assert sue_episodes_dict == {
        "owner_name": sue_str,
        "episodes": {
            x4_time_int: {
                "time_int": x4_time_int,
                quota_str(): x4_quota,
                "net_pacts": {bob_str: bob_net_pact},
            },
            x7_time_int: {
                "time_int": x7_time_int,
                quota_str(): x7_quota,
                "net_pacts": {zia_str: zia_net_pact},
            },
        },
    }

    # WHEN
    x_gov_idea = "gov_idea_x"
    sue_tranbook = sue_pactlog.get_tranbook(x_gov_idea)

    # THEN
    assert sue_tranbook
    assert sue_tranbook.gov_idea == x_gov_idea
    assert sue_tranbook.tranunit_exists(sue_str, zia_str, x7_time_int)
    assert sue_tranbook.tranunit_exists(sue_str, bob_str, x4_time_int)
    assert sue_tranbook.get_amount(sue_str, zia_str, x7_time_int) == zia_net_pact
    assert sue_tranbook.get_amount(sue_str, bob_str, x4_time_int) == bob_net_pact
