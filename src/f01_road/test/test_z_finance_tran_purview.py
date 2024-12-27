from src.f01_road.finance import default_fund_pool
from src.f01_road.finance_tran import (
    quota_str,
    time_id_str,
    wall_str,
    PurviewEpisode,
    purviewepisode_shop,
    PurviewLog,
    purviewlog_shop,
    get_purviewepisode_from_dict,
    get_purviewepisode_from_json,
    get_purviewlog_from_dict,
)
from pytest import raises as pytest_raises


def test_str_functions_ReturnObj():
    assert wall_str() == "wall"
    assert time_id_str() == "time_id"
    assert quota_str() == "quota"


def test_PurviewEpisode_Exists():
    # ESTABLISH / WHEN
    x_purviewepisode = PurviewEpisode()

    # THEN
    assert x_purviewepisode
    assert not x_purviewepisode.time_id
    assert not x_purviewepisode.quota
    assert not x_purviewepisode._net_purviews
    assert not x_purviewepisode._magnitude


def test_purviewepisode_shop_ReturnsObj():
    # ESTABLISH
    t4_time_id = 4

    # WHEN
    t4_purviewepisode = purviewepisode_shop(t4_time_id)

    # THEN
    assert t4_purviewepisode
    assert t4_purviewepisode.time_id == t4_time_id
    assert t4_purviewepisode.quota == default_fund_pool()
    assert t4_purviewepisode._magnitude == 0
    assert not t4_purviewepisode._net_purviews


def test_purviewepisode_shop_ReturnsObjWith_net_purviews():
    # ESTABLISH
    t4_time_id = 4
    t4_quota = 55
    t4_net_purviews = {"Sue": -4}
    t4_magnitude = 677

    # WHEN
    x_purviewepisode = purviewepisode_shop(
        x_time_id=t4_time_id,
        x_quota=t4_quota,
        net_purviews=t4_net_purviews,
        x_magnitude=t4_magnitude,
    )

    # THEN
    assert x_purviewepisode
    assert x_purviewepisode.time_id == t4_time_id
    assert x_purviewepisode.quota == t4_quota
    assert x_purviewepisode._magnitude == 677
    assert x_purviewepisode._net_purviews == t4_net_purviews


def test_PurviewEpisode_set_net_purview_SetsAttr():
    # ESTABLISH
    yao_purviewepisode = purviewepisode_shop("yao", 33)
    assert yao_purviewepisode._net_purviews == {}

    # WHEN
    sue_str = "Sue"
    sue_purview = -44
    yao_purviewepisode.set_net_purview(sue_str, sue_purview)

    # THEN
    assert yao_purviewepisode._net_purviews != {}
    assert yao_purviewepisode._net_purviews.get(sue_str) == sue_purview


def test_PurviewEpisode_net_purview_exists_ReturnsObj():
    # ESTABLISH
    yao_purviewepisode = purviewepisode_shop("yao", 33)
    sue_str = "Sue"
    sue_purview = -44
    assert yao_purviewepisode.net_purview_exists(sue_str) is False

    # WHEN
    yao_purviewepisode.set_net_purview(sue_str, sue_purview)

    # THEN
    assert yao_purviewepisode.net_purview_exists(sue_str)


def test_PurviewEpisode_get_net_purview_ReturnsObj():
    # ESTABLISH
    yao_purviewepisode = purviewepisode_shop("yao", 33)
    sue_str = "Sue"
    sue_purview = -44
    yao_purviewepisode.set_net_purview(sue_str, sue_purview)

    # WHEN / THEN
    assert yao_purviewepisode.get_net_purview(sue_str)
    assert yao_purviewepisode.get_net_purview(sue_str) == sue_purview


def test_PurviewEpisode_del_net_purview_SetsAttr():
    # ESTABLISH
    yao_purviewepisode = purviewepisode_shop("yao", 33)
    sue_str = "Sue"
    sue_purview = -44
    yao_purviewepisode.set_net_purview(sue_str, sue_purview)
    assert yao_purviewepisode.net_purview_exists(sue_str)

    # WHEN
    yao_purviewepisode.del_net_purview(sue_str)

    # THEN
    assert yao_purviewepisode.net_purview_exists(sue_str) is False


def test_PurviewEpisode_get_dict_ReturnsObj():
    # ESTABLISH
    t4_time_id = 4
    t4_quota = 55
    t4_purviewepisode = purviewepisode_shop(t4_time_id, t4_quota)

    # WHEN
    t4_dict = t4_purviewepisode.get_dict()

    # THEN
    assert t4_dict == {"time_id": t4_time_id, quota_str(): t4_quota}


def test_PurviewEpisode_calc_magnitude_SetsAttr_Scenario0():
    # ESTABLISH
    t4_time_id = 4
    t4_purviewepisode = purviewepisode_shop(t4_time_id)
    assert t4_purviewepisode._magnitude == 0

    # WHEN
    t4_purviewepisode.calc_magnitude()

    # THEN
    assert t4_purviewepisode._magnitude == 0


def test_PurviewEpisode_calc_magnitude_SetsAttr_Scenario1():
    # ESTABLISH
    t4_time_id = 4
    t4_net_purviews = {"Sue": -4, "Yao": 2, "Zia": 2}

    t4_purviewepisode = purviewepisode_shop(t4_time_id, net_purviews=t4_net_purviews)
    assert t4_purviewepisode._magnitude == 0

    # WHEN
    t4_purviewepisode.calc_magnitude()

    # THEN
    assert t4_purviewepisode._magnitude == 4


def test_PurviewEpisode_calc_magnitude_SetsAttr_Scenario2():
    # ESTABLISH
    t4_time_id = 4
    t4_net_purviews = {"Bob": -13, "Sue": -7, "Yao": 18, "Zia": 2}

    t4_purviewepisode = purviewepisode_shop(t4_time_id, net_purviews=t4_net_purviews)
    assert t4_purviewepisode._magnitude == 0

    # WHEN
    t4_purviewepisode.calc_magnitude()

    # THEN
    assert t4_purviewepisode._magnitude == 20


def test_PurviewEpisode_calc_magnitude_SetsAttr_Scenario3_RaisesError():
    # ESTABLISH
    t4_time_id = 4
    bob_purview = -13
    sue_purview = -3
    yao_purview = 100
    t4_net_purviews = {"Bob": bob_purview, "Sue": sue_purview, "Yao": yao_purview}
    t4_purviewepisode = purviewepisode_shop(t4_time_id, net_purviews=t4_net_purviews)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        t4_purviewepisode.calc_magnitude()
    exception_str = f"magnitude cannot be calculated: debt_purview={bob_purview+sue_purview}, cred_purview={yao_purview}"
    assert str(excinfo.value) == exception_str


def test_PurviewEpisode_get_dict_ReturnsObjWith_net_purviews():
    # ESTABLISH
    t4_time_id = 4
    t4_quota = 55
    t4_net_purviews = {"Sue": -4}
    t4_magnitude = 67
    t4_purviewepisode = purviewepisode_shop(t4_time_id, t4_quota, t4_net_purviews)
    t4_purviewepisode._magnitude = 67

    # WHEN
    t4_dict = t4_purviewepisode.get_dict()

    # THEN
    assert t4_dict == {
        "time_id": t4_time_id,
        quota_str(): t4_quota,
        "magnitude": t4_magnitude,
        "net_purviews": t4_net_purviews,
    }


def test_PurviewEpisode_get_json_ReturnsObj():
    # ESTABLISH
    t4_time_id = 4
    t4_quota = 55
    t4_net_purviews = {"Sue": -77}
    t4_purviewepisode = purviewepisode_shop(t4_time_id, t4_quota, t4_net_purviews)
    t4_purviewepisode._magnitude = 67

    # WHEN
    t4_json = t4_purviewepisode.get_json()

    # THEN
    static_t4_json = """{
  "magnitude": 67,
  "net_purviews": {
    "Sue": -77
  },
  "quota": 55,
  "time_id": 4
}"""
    print(f"{t4_json=}")
    assert t4_json == static_t4_json


def test_get_purviewepisode_from_dict_ReturnsObj_Sccenario0():
    # ESTABLISH
    t4_time_id = 4
    t4_quota = 55
    t4_purviewepisode = purviewepisode_shop(t4_time_id, t4_quota)
    t4_dict = t4_purviewepisode.get_dict()
    assert t4_dict == {"time_id": t4_time_id, quota_str(): t4_quota}

    # WHEN
    x_purviewepisode = get_purviewepisode_from_dict(t4_dict)

    # THEN
    assert x_purviewepisode
    assert x_purviewepisode.time_id == t4_time_id
    assert x_purviewepisode.quota == t4_quota
    assert x_purviewepisode._magnitude == 0
    assert x_purviewepisode == t4_purviewepisode


def test_get_purviewepisode_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    t4_time_id = 4
    t4_quota = 55
    t4_magnitude = 65
    t4_net_purviews = {"Sue": -77}
    t4_purviewepisode = purviewepisode_shop(t4_time_id, t4_quota, t4_net_purviews)
    t4_purviewepisode._magnitude = t4_magnitude
    t4_dict = t4_purviewepisode.get_dict()

    # WHEN
    x_purviewepisode = get_purviewepisode_from_dict(t4_dict)

    # THEN
    assert x_purviewepisode
    assert x_purviewepisode.time_id == t4_time_id
    assert x_purviewepisode.quota == t4_quota
    assert x_purviewepisode._magnitude == t4_magnitude
    assert x_purviewepisode._net_purviews == t4_net_purviews
    assert x_purviewepisode == t4_purviewepisode


def test_get_purviewepisode_from_json_ReturnsObj():
    # ESTABLISH
    t4_time_id = 4
    t4_quota = 55
    t4_net_purviews = {"Sue": -57}
    t4_purviewepisode = purviewepisode_shop(t4_time_id, t4_quota, t4_net_purviews)
    t4_json = t4_purviewepisode.get_json()

    # WHEN
    x_purviewepisode = get_purviewepisode_from_json(t4_json)

    # THEN
    assert x_purviewepisode
    assert x_purviewepisode.time_id == t4_time_id
    assert x_purviewepisode.quota == t4_quota
    assert x_purviewepisode._net_purviews == t4_net_purviews
    assert x_purviewepisode == t4_purviewepisode


def test_PurviewLog_Exists():
    # ESTABLISH / WHEN
    x_purviewlog = PurviewLog()

    # THEN
    assert x_purviewlog
    assert not x_purviewlog.owner_id
    assert not x_purviewlog.episodes
    assert not x_purviewlog._sum_purviewepisode_quota
    assert not x_purviewlog._sum_acct_purviews
    assert not x_purviewlog._time_id_min
    assert not x_purviewlog._time_id_max


def test_purviewlog_shop_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"

    # WHEN
    x_purviewlog = purviewlog_shop(sue_str)

    # THEN
    assert x_purviewlog
    assert x_purviewlog.owner_id == sue_str
    assert x_purviewlog.episodes == {}
    assert not x_purviewlog._sum_purviewepisode_quota
    assert x_purviewlog._sum_acct_purviews == {}
    assert not x_purviewlog._time_id_min
    assert not x_purviewlog._time_id_max


def test_PurviewLog_set_episode_SetsAttr():
    # ESTABLISH
    sue_purviewlog = purviewlog_shop("sue")
    assert sue_purviewlog.episodes == {}

    # WHEN
    t1_int = 145
    t1_purviewepisode = purviewepisode_shop(t1_int, 0)
    sue_purviewlog.set_episode(t1_purviewepisode)

    # THEN
    assert sue_purviewlog.episodes != {}
    assert sue_purviewlog.episodes.get(t1_int) == t1_purviewepisode


def test_PurviewLog_episode_exists_ReturnsObj():
    # ESTABLISH
    sue_purviewlog = purviewlog_shop("Sue")
    t1_int = 145
    assert sue_purviewlog.episode_exists(t1_int) is False

    # WHEN
    t1_purviewepisode = purviewepisode_shop(t1_int, 0)
    sue_purviewlog.set_episode(t1_purviewepisode)

    # THEN
    assert sue_purviewlog.episode_exists(t1_int)


def test_PurviewLog_get_episode_ReturnsObj():
    # ESTABLISH
    sue_purviewlog = purviewlog_shop("sue")
    t1_int = 145
    t1_stat_purviewepisode = purviewepisode_shop(t1_int, 0)
    sue_purviewlog.set_episode(t1_stat_purviewepisode)

    # WHEN
    t1_gen_purviewepisode = sue_purviewlog.get_episode(t1_int)

    # THEN
    assert t1_gen_purviewepisode
    assert t1_gen_purviewepisode == t1_stat_purviewepisode


def test_PurviewLog_del_episode_SetsAttr():
    # ESTABLISH
    sue_purviewlog = purviewlog_shop("Sue")
    t1_int = 145
    t1_stat_purviewepisode = purviewepisode_shop(t1_int, 0)
    sue_purviewlog.set_episode(t1_stat_purviewepisode)
    assert sue_purviewlog.episode_exists(t1_int)

    # WHEN
    sue_purviewlog.del_episode(t1_int)

    # THEN
    assert sue_purviewlog.episode_exists(t1_int) is False


def test_PurviewLog_add_episode_SetsAttr():
    # ESTABLISH
    sue_purviewlog = purviewlog_shop("sue")
    assert sue_purviewlog.episodes == {}

    # WHEN
    t1_int = 145
    t1_quota = 500
    sue_purviewlog.add_episode(t1_int, x_quota=t1_quota)

    # THEN
    assert sue_purviewlog.episodes != {}
    t1_purviewepisode = purviewepisode_shop(t1_int, t1_quota)
    assert sue_purviewlog.episodes.get(t1_int) == t1_purviewepisode


def test_PurviewLog_get_2d_array_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_purviewlog = purviewlog_shop(sue_str)

    # WHEN
    sue_episodes_2d_array = sue_purviewlog.get_2d_array()

    # THEN
    assert sue_episodes_2d_array == []


def test_PurviewLog_get_2d_array_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_purviewlog = purviewlog_shop(sue_str)
    x4_time_id = 4
    x4_quota = 55
    x7_time_id = 7
    x7_quota = 66
    sue_purviewlog.add_episode(x4_time_id, x4_quota)
    sue_purviewlog.add_episode(x7_time_id, x7_quota)

    # WHEN
    sue_episodes_2d_array = sue_purviewlog.get_2d_array()

    # THEN
    assert sue_episodes_2d_array == [
        [sue_str, x4_time_id, x4_quota],
        [sue_str, x7_time_id, x7_quota],
    ]


def test_PurviewLog_get_time_ids_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_purviewlog = purviewlog_shop(sue_str)
    x4_time_id = 4
    x4_quota = 55
    x7_time_id = 7
    x7_quota = 66
    assert sue_purviewlog.get_time_ids() == set()

    # WHEN
    sue_purviewlog.add_episode(x4_time_id, x4_quota)
    sue_purviewlog.add_episode(x7_time_id, x7_quota)

    # THEN
    assert sue_purviewlog.get_time_ids() == {x4_time_id, x7_time_id}


def test_PurviewLog_get_headers_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_purviewlog = purviewlog_shop(sue_str)
    x4_time_id = 4
    x4_quota = 55
    x7_time_id = 7
    x7_quota = 66
    sue_purviewlog.add_episode(x4_time_id, x4_quota)
    sue_purviewlog.add_episode(x7_time_id, x7_quota)

    # WHEN
    sue_headers_list = sue_purviewlog.get_headers()

    # THEN
    assert sue_headers_list == ["owner_id", "time_id", quota_str()]


def test_PurviewLog_get_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_purviewlog = purviewlog_shop(sue_str)
    x4_time_id = 4
    x4_quota = 55
    x7_time_id = 7
    x7_quota = 66
    sue_purviewlog.add_episode(x4_time_id, x4_quota)
    sue_purviewlog.add_episode(x7_time_id, x7_quota)

    # WHEN
    sue_episodes_dict = sue_purviewlog.get_dict()

    # THEN
    assert sue_episodes_dict == {
        "owner_id": sue_str,
        "episodes": {
            x4_time_id: {quota_str(): x4_quota, "time_id": x4_time_id},
            x7_time_id: {quota_str(): x7_quota, "time_id": x7_time_id},
        },
    }


def test_get_purviewlog_from_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_purviewlog = purviewlog_shop(sue_str)
    sue_episodes_dict = sue_purviewlog.get_dict()
    assert sue_episodes_dict == {"owner_id": sue_str, "episodes": {}}

    # WHEN
    x_purviewlog = get_purviewlog_from_dict(sue_episodes_dict)

    # THEN
    assert x_purviewlog
    assert x_purviewlog.owner_id == sue_str
    assert x_purviewlog.episodes == {}
    assert x_purviewlog.episodes == sue_purviewlog.episodes
    assert x_purviewlog == sue_purviewlog


def test_get_purviewlog_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_purviewlog = purviewlog_shop(sue_str)
    x4_time_id = 4
    x4_quota = 55
    x7_time_id = 7
    x7_quota = 66
    sue_purviewlog.add_episode(x4_time_id, x4_quota)
    sue_purviewlog.add_episode(x7_time_id, x7_quota)
    sue_episodes_dict = sue_purviewlog.get_dict()
    assert sue_episodes_dict == {
        "owner_id": sue_str,
        "episodes": {
            x4_time_id: {"time_id": x4_time_id, quota_str(): x4_quota},
            x7_time_id: {"time_id": x7_time_id, quota_str(): x7_quota},
        },
    }

    # WHEN
    x_purviewlog = get_purviewlog_from_dict(sue_episodes_dict)

    # THEN
    assert x_purviewlog
    assert x_purviewlog.owner_id == sue_str
    assert x_purviewlog.get_episode(x4_time_id) != None
    assert x_purviewlog.get_episode(x7_time_id) != None
    assert x_purviewlog.episodes == sue_purviewlog.episodes
    assert x_purviewlog == sue_purviewlog


def test_get_purviewlog_from_dict_ReturnsObj_Scenario2():
    # ESTABLISH
    sue_str = "Sue"
    sue_purviewlog = purviewlog_shop(sue_str)
    x4_time_id = 4
    x4_quota = 55
    x7_time_id = 7
    x7_quota = 66
    sue_purviewlog.add_episode(x4_time_id, x4_quota)
    sue_purviewlog.add_episode(x7_time_id, x7_quota)
    zia_str = "Zia"
    zia_net_purview = 887
    sue_net_purview = 445
    sue_purviewlog.get_episode(x7_time_id).set_net_purview(sue_str, sue_net_purview)
    sue_purviewlog.get_episode(x7_time_id).set_net_purview(zia_str, zia_net_purview)
    sue_episodes_dict = sue_purviewlog.get_dict()
    assert sue_episodes_dict == {
        "owner_id": sue_str,
        "episodes": {
            x4_time_id: {"time_id": x4_time_id, quota_str(): x4_quota},
            x7_time_id: {
                "time_id": x7_time_id,
                quota_str(): x7_quota,
                "net_purviews": {sue_str: sue_net_purview, zia_str: zia_net_purview},
            },
        },
    }

    # WHEN
    x_purviewlog = get_purviewlog_from_dict(sue_episodes_dict)

    # THEN
    assert x_purviewlog
    assert x_purviewlog.owner_id == sue_str
    assert x_purviewlog.get_episode(x4_time_id) != None
    assert x_purviewlog.get_episode(x7_time_id) != None
    assert x_purviewlog.get_episode(x7_time_id)._net_purviews != {}
    assert len(x_purviewlog.get_episode(x7_time_id)._net_purviews) == 2
    assert x_purviewlog.episodes == sue_purviewlog.episodes
    assert x_purviewlog == sue_purviewlog


def test_PurviewLog_get_tranbook_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_purviewlog = purviewlog_shop(sue_str)
    x4_time_id = 4
    x4_quota = 55
    x7_time_id = 7
    x7_quota = 66
    sue_purviewlog.add_episode(x4_time_id, x4_quota)
    sue_purviewlog.add_episode(x7_time_id, x7_quota)
    bob_str = "Bob"
    zia_str = "Zia"
    zia_net_purview = 887
    bob_net_purview = 445
    sue_purviewlog.get_episode(x4_time_id).set_net_purview(bob_str, bob_net_purview)
    sue_purviewlog.get_episode(x7_time_id).set_net_purview(zia_str, zia_net_purview)
    sue_episodes_dict = sue_purviewlog.get_dict()
    assert sue_episodes_dict == {
        "owner_id": sue_str,
        "episodes": {
            x4_time_id: {
                "time_id": x4_time_id,
                quota_str(): x4_quota,
                "net_purviews": {bob_str: bob_net_purview},
            },
            x7_time_id: {
                "time_id": x7_time_id,
                quota_str(): x7_quota,
                "net_purviews": {zia_str: zia_net_purview},
            },
        },
    }

    # WHEN
    x_deal_id = "deal_id_x"
    sue_tranbook = sue_purviewlog.get_tranbook(x_deal_id)

    # THEN
    assert sue_tranbook
    assert sue_tranbook.deal_id == x_deal_id
    assert sue_tranbook.tranunit_exists(sue_str, zia_str, x7_time_id)
    assert sue_tranbook.tranunit_exists(sue_str, bob_str, x4_time_id)
    assert sue_tranbook.get_amount(sue_str, zia_str, x7_time_id) == zia_net_purview
    assert sue_tranbook.get_amount(sue_str, bob_str, x4_time_id) == bob_net_purview
