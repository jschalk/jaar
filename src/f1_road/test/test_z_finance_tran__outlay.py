from src.f1_road.finance import default_fund_pool
from src.f1_road.finance_tran import (
    OutlayEpisode,
    outlayepisode_shop,
    OutlayLog,
    outlaylog_shop,
    get_outlayepisode_from_dict,
    get_outlayepisode_from_json,
    get_outlaylog_from_dict,
)
from pytest import raises as pytest_raises


def test_OutlayEpisode_Exists():
    # ESTABLISH / WHEN
    x_outlayepisode = OutlayEpisode()

    # THEN
    assert x_outlayepisode
    assert not x_outlayepisode.timestamp
    assert not x_outlayepisode.purview
    assert not x_outlayepisode._net_outlays
    assert not x_outlayepisode._magnitude
    assert not x_outlayepisode._tender_desc


def test_outlayepisode_shop_ReturnsObj():
    # ESTABLISH
    t4_timestamp = 4

    # WHEN
    t4_outlayepisode = outlayepisode_shop(t4_timestamp)

    # THEN
    assert t4_outlayepisode
    assert t4_outlayepisode.timestamp == t4_timestamp
    assert t4_outlayepisode.purview == default_fund_pool()
    assert t4_outlayepisode._magnitude == 0
    assert not t4_outlayepisode._net_outlays
    assert not t4_outlayepisode._tender_desc


def test_outlayepisode_shop_ReturnsObjWith_net_outlays():
    # ESTABLISH
    t4_timestamp = 4
    t4_purview = 55
    t4_net_outlays = {"Sue": -4}
    t4_magnitude = 677

    # WHEN
    x_outlayepisode = outlayepisode_shop(
        x_timestamp=t4_timestamp,
        x_purview=t4_purview,
        net_outlays=t4_net_outlays,
        x_magnitude=t4_magnitude,
    )

    # THEN
    assert x_outlayepisode
    assert x_outlayepisode.timestamp == t4_timestamp
    assert x_outlayepisode.purview == t4_purview
    assert x_outlayepisode._magnitude == 677
    assert x_outlayepisode._net_outlays == t4_net_outlays
    assert not x_outlayepisode._tender_desc


def test_OutlayEpisode_set_net_outlay_SetsAttr():
    # ESTABLISH
    yao_outlayepisode = outlayepisode_shop("yao", 33)
    assert yao_outlayepisode._net_outlays == {}

    # WHEN
    sue_text = "Sue"
    sue_outlay = -44
    yao_outlayepisode.set_net_outlay(sue_text, sue_outlay)

    # THEN
    assert yao_outlayepisode._net_outlays != {}
    assert yao_outlayepisode._net_outlays.get(sue_text) == sue_outlay


def test_OutlayEpisode_net_outlay_exists_ReturnsObj():
    # ESTABLISH
    yao_outlayepisode = outlayepisode_shop("yao", 33)
    sue_text = "Sue"
    sue_outlay = -44
    assert yao_outlayepisode.net_outlay_exists(sue_text) is False

    # WHEN
    yao_outlayepisode.set_net_outlay(sue_text, sue_outlay)

    # THEN
    assert yao_outlayepisode.net_outlay_exists(sue_text)


def test_OutlayEpisode_get_net_outlay_ReturnsObj():
    # ESTABLISH
    yao_outlayepisode = outlayepisode_shop("yao", 33)
    sue_text = "Sue"
    sue_outlay = -44
    yao_outlayepisode.set_net_outlay(sue_text, sue_outlay)

    # WHEN / THEN
    assert yao_outlayepisode.get_net_outlay(sue_text)
    assert yao_outlayepisode.get_net_outlay(sue_text) == sue_outlay


def test_OutlayEpisode_del_net_outlay_SetsAttr():
    # ESTABLISH
    yao_outlayepisode = outlayepisode_shop("yao", 33)
    sue_text = "Sue"
    sue_outlay = -44
    yao_outlayepisode.set_net_outlay(sue_text, sue_outlay)
    assert yao_outlayepisode.net_outlay_exists(sue_text)

    # WHEN
    yao_outlayepisode.del_net_outlay(sue_text)

    # THEN
    assert yao_outlayepisode.net_outlay_exists(sue_text) is False


def test_OutlayEpisode_get_dict_ReturnsObj():
    # ESTABLISH
    t4_timestamp = 4
    t4_purview = 55
    t4_outlayepisode = outlayepisode_shop(t4_timestamp, t4_purview)

    # WHEN
    t4_dict = t4_outlayepisode.get_dict()

    # THEN
    assert t4_dict == {"timestamp": t4_timestamp, "purview": t4_purview}


def test_OutlayEpisode_calc_magnitude_SetsAttr_Scenario0():
    # ESTABLISH
    t4_timestamp = 4
    t4_outlayepisode = outlayepisode_shop(t4_timestamp)
    assert t4_outlayepisode._magnitude == 0

    # WHEN
    t4_outlayepisode.calc_magnitude()

    # THEN
    assert t4_outlayepisode._magnitude == 0


def test_OutlayEpisode_calc_magnitude_SetsAttr_Scenario1():
    # ESTABLISH
    t4_timestamp = 4
    t4_net_outlays = {"Sue": -4, "Yao": 2, "Zia": 2}

    t4_outlayepisode = outlayepisode_shop(t4_timestamp, net_outlays=t4_net_outlays)
    assert t4_outlayepisode._magnitude == 0

    # WHEN
    t4_outlayepisode.calc_magnitude()

    # THEN
    assert t4_outlayepisode._magnitude == 4


def test_OutlayEpisode_calc_magnitude_SetsAttr_Scenario2():
    # ESTABLISH
    t4_timestamp = 4
    t4_net_outlays = {"Bob": -13, "Sue": -7, "Yao": 18, "Zia": 2}

    t4_outlayepisode = outlayepisode_shop(t4_timestamp, net_outlays=t4_net_outlays)
    assert t4_outlayepisode._magnitude == 0

    # WHEN
    t4_outlayepisode.calc_magnitude()

    # THEN
    assert t4_outlayepisode._magnitude == 20


def test_OutlayEpisode_calc_magnitude_SetsAttr_Scenario3_RaisesError():
    # ESTABLISH
    t4_timestamp = 4
    bob_outlay = -13
    sue_outlay = -3
    yao_outlay = 100
    t4_net_outlays = {"Bob": bob_outlay, "Sue": sue_outlay, "Yao": yao_outlay}
    t4_outlayepisode = outlayepisode_shop(t4_timestamp, net_outlays=t4_net_outlays)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        t4_outlayepisode.calc_magnitude()
    exception_str = f"magnitude cannot be calculated: debt_outlay={bob_outlay+sue_outlay}, cred_outlay={yao_outlay}"
    assert str(excinfo.value) == exception_str


def test_OutlayEpisode_get_dict_ReturnsObjWith_net_outlays():
    # ESTABLISH
    t4_timestamp = 4
    t4_purview = 55
    t4_net_outlays = {"Sue": -4}
    t4_magnitude = 67
    t4_outlayepisode = outlayepisode_shop(t4_timestamp, t4_purview, t4_net_outlays)
    t4_outlayepisode._magnitude = 67

    # WHEN
    t4_dict = t4_outlayepisode.get_dict()

    # THEN
    assert t4_dict == {
        "timestamp": t4_timestamp,
        "purview": t4_purview,
        "magnitude": t4_magnitude,
        "net_outlays": t4_net_outlays,
    }


def test_OutlayEpisode_get_json_ReturnsObj():
    # ESTABLISH
    t4_timestamp = 4
    t4_purview = 55
    t4_net_outlays = {"Sue": -77}
    t4_outlayepisode = outlayepisode_shop(t4_timestamp, t4_purview, t4_net_outlays)
    t4_outlayepisode._magnitude = 67

    # WHEN
    t4_json = t4_outlayepisode.get_json()

    # THEN
    static_t4_json = """{
  "magnitude": 67,
  "net_outlays": {
    "Sue": -77
  },
  "purview": 55,
  "timestamp": 4
}"""
    print(f"{t4_json=}")
    assert t4_json == static_t4_json


def test_get_outlayepisode_from_dict_ReturnsObj_Sccenario0():
    # ESTABLISH
    t4_timestamp = 4
    t4_purview = 55
    t4_outlayepisode = outlayepisode_shop(t4_timestamp, t4_purview)
    t4_dict = t4_outlayepisode.get_dict()
    assert t4_dict == {"timestamp": t4_timestamp, "purview": t4_purview}

    # WHEN
    x_outlayepisode = get_outlayepisode_from_dict(t4_dict)

    # THEN
    assert x_outlayepisode
    assert x_outlayepisode.timestamp == t4_timestamp
    assert x_outlayepisode.purview == t4_purview
    assert x_outlayepisode._magnitude == 0
    assert x_outlayepisode == t4_outlayepisode


def test_get_outlayepisode_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    t4_timestamp = 4
    t4_purview = 55
    t4_magnitude = 65
    t4_net_outlays = {"Sue": -77}
    t4_outlayepisode = outlayepisode_shop(t4_timestamp, t4_purview, t4_net_outlays)
    t4_outlayepisode._magnitude = t4_magnitude
    t4_dict = t4_outlayepisode.get_dict()

    # WHEN
    x_outlayepisode = get_outlayepisode_from_dict(t4_dict)

    # THEN
    assert x_outlayepisode
    assert x_outlayepisode.timestamp == t4_timestamp
    assert x_outlayepisode.purview == t4_purview
    assert x_outlayepisode._magnitude == t4_magnitude
    assert x_outlayepisode._net_outlays == t4_net_outlays
    assert x_outlayepisode == t4_outlayepisode


def test_get_outlayepisode_from_json_ReturnsObj():
    # ESTABLISH
    t4_timestamp = 4
    t4_purview = 55
    t4_net_outlays = {"Sue": -57}
    t4_outlayepisode = outlayepisode_shop(t4_timestamp, t4_purview, t4_net_outlays)
    t4_json = t4_outlayepisode.get_json()

    # WHEN
    x_outlayepisode = get_outlayepisode_from_json(t4_json)

    # THEN
    assert x_outlayepisode
    assert x_outlayepisode.timestamp == t4_timestamp
    assert x_outlayepisode.purview == t4_purview
    assert x_outlayepisode._net_outlays == t4_net_outlays
    assert x_outlayepisode == t4_outlayepisode


def test_OutlayLog_Exists():
    # ESTABLISH / WHEN
    x_outlaylog = OutlayLog()

    # THEN
    assert x_outlaylog
    assert not x_outlaylog.owner_id
    assert not x_outlaylog.episodes
    assert not x_outlaylog._sum_outlayepisode_purview
    assert not x_outlaylog._sum_acct_outlays
    assert not x_outlaylog._timestamp_min
    assert not x_outlaylog._timestamp_max


def test_outlaylog_shop_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"

    # WHEN
    x_outlaylog = outlaylog_shop(sue_str)

    # THEN
    assert x_outlaylog
    assert x_outlaylog.owner_id == sue_str
    assert x_outlaylog.episodes == {}
    assert not x_outlaylog._sum_outlayepisode_purview
    assert x_outlaylog._sum_acct_outlays == {}
    assert not x_outlaylog._timestamp_min
    assert not x_outlaylog._timestamp_max


def test_OutlayLog_set_episode_SetsAttr():
    # ESTABLISH
    sue_outlaylog = outlaylog_shop("sue")
    assert sue_outlaylog.episodes == {}

    # WHEN
    t1_int = 145
    t1_outlayepisode = outlayepisode_shop(t1_int, 0)
    sue_outlaylog.set_episode(t1_outlayepisode)

    # THEN
    assert sue_outlaylog.episodes != {}
    assert sue_outlaylog.episodes.get(t1_int) == t1_outlayepisode


def test_OutlayLog_episode_exists_ReturnsObj():
    # ESTABLISH
    sue_outlaylog = outlaylog_shop("Sue")
    t1_int = 145
    assert sue_outlaylog.episode_exists(t1_int) is False

    # WHEN
    t1_outlayepisode = outlayepisode_shop(t1_int, 0)
    sue_outlaylog.set_episode(t1_outlayepisode)

    # THEN
    assert sue_outlaylog.episode_exists(t1_int)


def test_OutlayLog_get_episode_ReturnsObj():
    # ESTABLISH
    sue_outlaylog = outlaylog_shop("sue")
    t1_int = 145
    t1_stat_outlayepisode = outlayepisode_shop(t1_int, 0)
    sue_outlaylog.set_episode(t1_stat_outlayepisode)

    # WHEN
    t1_gen_outlayepisode = sue_outlaylog.get_episode(t1_int)

    # THEN
    assert t1_gen_outlayepisode
    assert t1_gen_outlayepisode == t1_stat_outlayepisode


def test_OutlayLog_del_episode_SetsAttr():
    # ESTABLISH
    sue_outlaylog = outlaylog_shop("Sue")
    t1_int = 145
    t1_stat_outlayepisode = outlayepisode_shop(t1_int, 0)
    sue_outlaylog.set_episode(t1_stat_outlayepisode)
    assert sue_outlaylog.episode_exists(t1_int)

    # WHEN
    sue_outlaylog.del_episode(t1_int)

    # THEN
    assert sue_outlaylog.episode_exists(t1_int) is False


def test_OutlayLog_add_episode_SetsAttr():
    # ESTABLISH
    sue_outlaylog = outlaylog_shop("sue")
    assert sue_outlaylog.episodes == {}

    # WHEN
    t1_int = 145
    t1_purview = 500
    sue_outlaylog.add_episode(t1_int, x_purview=t1_purview)

    # THEN
    assert sue_outlaylog.episodes != {}
    t1_outlayepisode = outlayepisode_shop(t1_int, t1_purview)
    assert sue_outlaylog.episodes.get(t1_int) == t1_outlayepisode


def test_OutlayLog_get_2d_array_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_outlaylog = outlaylog_shop(sue_str)

    # WHEN
    sue_episodes_2d_array = sue_outlaylog.get_2d_array()

    # THEN
    assert sue_episodes_2d_array == []


def test_OutlayLog_get_2d_array_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_outlaylog = outlaylog_shop(sue_str)
    x4_timestamp = 4
    x4_purview = 55
    x7_timestamp = 7
    x7_purview = 66
    sue_outlaylog.add_episode(x4_timestamp, x4_purview)
    sue_outlaylog.add_episode(x7_timestamp, x7_purview)

    # WHEN
    sue_episodes_2d_array = sue_outlaylog.get_2d_array()

    # THEN
    assert sue_episodes_2d_array == [
        [sue_str, x4_timestamp, x4_purview],
        [sue_str, x7_timestamp, x7_purview],
    ]


def test_OutlayLog_get_headers_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_outlaylog = outlaylog_shop(sue_str)
    x4_timestamp = 4
    x4_purview = 55
    x7_timestamp = 7
    x7_purview = 66
    sue_outlaylog.add_episode(x4_timestamp, x4_purview)
    sue_outlaylog.add_episode(x7_timestamp, x7_purview)

    # WHEN
    sue_headers_list = sue_outlaylog.get_headers()

    # THEN
    assert sue_headers_list == ["owner_id", "timestamp", "purview"]


def test_OutlayLog_get_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_outlaylog = outlaylog_shop(sue_str)
    x4_timestamp = 4
    x4_purview = 55
    x7_timestamp = 7
    x7_purview = 66
    sue_outlaylog.add_episode(x4_timestamp, x4_purview)
    sue_outlaylog.add_episode(x7_timestamp, x7_purview)

    # WHEN
    sue_episodes_dict = sue_outlaylog.get_dict()

    # THEN
    assert sue_episodes_dict == {
        "owner_id": sue_str,
        "episodes": {
            x4_timestamp: {"purview": x4_purview, "timestamp": x4_timestamp},
            x7_timestamp: {"purview": x7_purview, "timestamp": x7_timestamp},
        },
    }


def test_get_outlaylog_from_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_outlaylog = outlaylog_shop(sue_str)
    sue_episodes_dict = sue_outlaylog.get_dict()
    assert sue_episodes_dict == {"owner_id": sue_str, "episodes": {}}

    # WHEN
    x_outlaylog = get_outlaylog_from_dict(sue_episodes_dict)

    # THEN
    assert x_outlaylog
    assert x_outlaylog.owner_id == sue_str
    assert x_outlaylog.episodes == {}
    assert x_outlaylog.episodes == sue_outlaylog.episodes
    assert x_outlaylog == sue_outlaylog


def test_get_outlaylog_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_outlaylog = outlaylog_shop(sue_str)
    x4_timestamp = 4
    x4_purview = 55
    x7_timestamp = 7
    x7_purview = 66
    sue_outlaylog.add_episode(x4_timestamp, x4_purview)
    sue_outlaylog.add_episode(x7_timestamp, x7_purview)
    sue_episodes_dict = sue_outlaylog.get_dict()
    assert sue_episodes_dict == {
        "owner_id": sue_str,
        "episodes": {
            x4_timestamp: {"timestamp": x4_timestamp, "purview": x4_purview},
            x7_timestamp: {"timestamp": x7_timestamp, "purview": x7_purview},
        },
    }

    # WHEN
    x_outlaylog = get_outlaylog_from_dict(sue_episodes_dict)

    # THEN
    assert x_outlaylog
    assert x_outlaylog.owner_id == sue_str
    assert x_outlaylog.get_episode(x4_timestamp) != None
    assert x_outlaylog.get_episode(x7_timestamp) != None
    assert x_outlaylog.episodes == sue_outlaylog.episodes
    assert x_outlaylog == sue_outlaylog


def test_get_outlaylog_from_dict_ReturnsObj_Scenario2():
    # ESTABLISH
    sue_str = "Sue"
    sue_outlaylog = outlaylog_shop(sue_str)
    x4_timestamp = 4
    x4_purview = 55
    x7_timestamp = 7
    x7_purview = 66
    sue_outlaylog.add_episode(x4_timestamp, x4_purview)
    sue_outlaylog.add_episode(x7_timestamp, x7_purview)
    zia_str = "Zia"
    zia_net_outlay = 887
    sue_net_outlay = 445
    sue_outlaylog.get_episode(x7_timestamp).set_net_outlay(sue_str, sue_net_outlay)
    sue_outlaylog.get_episode(x7_timestamp).set_net_outlay(zia_str, zia_net_outlay)
    sue_episodes_dict = sue_outlaylog.get_dict()
    assert sue_episodes_dict == {
        "owner_id": sue_str,
        "episodes": {
            x4_timestamp: {"timestamp": x4_timestamp, "purview": x4_purview},
            x7_timestamp: {
                "timestamp": x7_timestamp,
                "purview": x7_purview,
                "net_outlays": {sue_str: sue_net_outlay, zia_str: zia_net_outlay},
            },
        },
    }

    # WHEN
    x_outlaylog = get_outlaylog_from_dict(sue_episodes_dict)

    # THEN
    assert x_outlaylog
    assert x_outlaylog.owner_id == sue_str
    assert x_outlaylog.get_episode(x4_timestamp) != None
    assert x_outlaylog.get_episode(x7_timestamp) != None
    assert x_outlaylog.get_episode(x7_timestamp)._net_outlays != {}
    assert len(x_outlaylog.get_episode(x7_timestamp)._net_outlays) == 2
    assert x_outlaylog.episodes == sue_outlaylog.episodes
    assert x_outlaylog == sue_outlaylog
