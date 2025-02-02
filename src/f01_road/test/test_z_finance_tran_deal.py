from src.f01_road.finance import default_fund_pool
from src.f01_road.finance_tran import (
    quota_str,
    time_int_str,
    bridge_str,
    search_depth_str,
    DealEpisode,
    dealepisode_shop,
    DealLog,
    deallog_shop,
    get_dealepisode_from_dict,
    get_dealepisode_from_json,
    get_deallog_from_dict,
)
from pytest import raises as pytest_raises


def test_str_functions_ReturnObj():
    assert bridge_str() == "bridge"
    assert search_depth_str() == "search_depth"
    assert time_int_str() == "time_int"
    assert quota_str() == "quota"


def test_DealEpisode_Exists():
    # ESTABLISH / WHEN
    x_dealepisode = DealEpisode()

    # THEN
    assert x_dealepisode
    assert not x_dealepisode.time_int
    assert not x_dealepisode.quota
    assert not x_dealepisode.search_depth
    assert not x_dealepisode._net_deals
    assert not x_dealepisode._magnitude


def test_dealepisode_shop_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4

    # WHEN
    t4_dealepisode = dealepisode_shop(t4_time_int)

    # THEN
    assert t4_dealepisode
    assert t4_dealepisode.time_int == t4_time_int
    assert t4_dealepisode.quota == default_fund_pool()
    assert t4_dealepisode._magnitude == 0
    assert t4_dealepisode.search_depth == 3
    assert not t4_dealepisode._net_deals


def test_dealepisode_shop_ReturnsObjWith_net_deals():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_net_deals = {"Sue": -4}
    t4_magnitude = 677
    t4_search_depth = 88

    # WHEN
    x_dealepisode = dealepisode_shop(
        time_int=t4_time_int,
        quota=t4_quota,
        net_deals=t4_net_deals,
        magnitude=t4_magnitude,
        search_depth=t4_search_depth,
    )

    # THEN
    assert x_dealepisode
    assert x_dealepisode.time_int == t4_time_int
    assert x_dealepisode.quota == t4_quota
    assert x_dealepisode.search_depth == t4_search_depth
    assert x_dealepisode._magnitude == 677
    assert x_dealepisode._net_deals == t4_net_deals


def test_DealEpisode_set_net_deal_SetsAttr():
    # ESTABLISH
    yao_dealepisode = dealepisode_shop("yao", 33)
    assert yao_dealepisode._net_deals == {}

    # WHEN
    sue_str = "Sue"
    sue_deal = -44
    yao_dealepisode.set_net_deal(sue_str, sue_deal)

    # THEN
    assert yao_dealepisode._net_deals != {}
    assert yao_dealepisode._net_deals.get(sue_str) == sue_deal


def test_DealEpisode_net_deal_exists_ReturnsObj():
    # ESTABLISH
    yao_dealepisode = dealepisode_shop("yao", 33)
    sue_str = "Sue"
    sue_deal = -44
    assert yao_dealepisode.net_deal_exists(sue_str) is False

    # WHEN
    yao_dealepisode.set_net_deal(sue_str, sue_deal)

    # THEN
    assert yao_dealepisode.net_deal_exists(sue_str)


def test_DealEpisode_get_net_deal_ReturnsObj():
    # ESTABLISH
    yao_dealepisode = dealepisode_shop("yao", 33)
    sue_str = "Sue"
    sue_deal = -44
    yao_dealepisode.set_net_deal(sue_str, sue_deal)

    # WHEN / THEN
    assert yao_dealepisode.get_net_deal(sue_str)
    assert yao_dealepisode.get_net_deal(sue_str) == sue_deal


def test_DealEpisode_del_net_deal_SetsAttr():
    # ESTABLISH
    yao_dealepisode = dealepisode_shop("yao", 33)
    sue_str = "Sue"
    sue_deal = -44
    yao_dealepisode.set_net_deal(sue_str, sue_deal)
    assert yao_dealepisode.net_deal_exists(sue_str)

    # WHEN
    yao_dealepisode.del_net_deal(sue_str)

    # THEN
    assert yao_dealepisode.net_deal_exists(sue_str) is False


def test_DealEpisode_get_dict_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_dealepisode = dealepisode_shop(t4_time_int, t4_quota)

    # WHEN
    t4_dict = t4_dealepisode.get_dict()

    # THEN
    assert t4_dict == {"time_int": t4_time_int, quota_str(): t4_quota}


def test_DealEpisode_calc_magnitude_SetsAttr_Scenario0():
    # ESTABLISH
    t4_time_int = 4
    t4_dealepisode = dealepisode_shop(t4_time_int)
    assert t4_dealepisode._magnitude == 0

    # WHEN
    t4_dealepisode.calc_magnitude()

    # THEN
    assert t4_dealepisode._magnitude == 0


def test_DealEpisode_calc_magnitude_SetsAttr_Scenario1():
    # ESTABLISH
    t4_time_int = 4
    t4_net_deals = {"Sue": -4, "Yao": 2, "Zia": 2}

    t4_dealepisode = dealepisode_shop(t4_time_int, net_deals=t4_net_deals)
    assert t4_dealepisode._magnitude == 0

    # WHEN
    t4_dealepisode.calc_magnitude()

    # THEN
    assert t4_dealepisode._magnitude == 4


def test_DealEpisode_calc_magnitude_SetsAttr_Scenario2():
    # ESTABLISH
    t4_time_int = 4
    t4_net_deals = {"Bob": -13, "Sue": -7, "Yao": 18, "Zia": 2}

    t4_dealepisode = dealepisode_shop(t4_time_int, net_deals=t4_net_deals)
    assert t4_dealepisode._magnitude == 0

    # WHEN
    t4_dealepisode.calc_magnitude()

    # THEN
    assert t4_dealepisode._magnitude == 20


def test_DealEpisode_calc_magnitude_SetsAttr_Scenario3_RaisesError():
    # ESTABLISH
    t4_time_int = 4
    bob_deal = -13
    sue_deal = -3
    yao_deal = 100
    t4_net_deals = {"Bob": bob_deal, "Sue": sue_deal, "Yao": yao_deal}
    t4_dealepisode = dealepisode_shop(t4_time_int, net_deals=t4_net_deals)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        t4_dealepisode.calc_magnitude()
    exception_str = f"magnitude cannot be calculated: debt_deal={bob_deal+sue_deal}, cred_deal={yao_deal}"
    assert str(excinfo.value) == exception_str


def test_DealEpisode_get_dict_ReturnsObjWith_net_deals():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_net_deals = {"Sue": -4}
    t4_magnitude = 67
    t4_dealepisode = dealepisode_shop(t4_time_int, t4_quota, t4_net_deals)
    t4_dealepisode._magnitude = 67

    # WHEN
    t4_dict = t4_dealepisode.get_dict()

    # THEN
    assert t4_dict == {
        "time_int": t4_time_int,
        quota_str(): t4_quota,
        "magnitude": t4_magnitude,
        "net_deals": t4_net_deals,
    }


def test_DealEpisode_get_json_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_net_deals = {"Sue": -77}
    t4_dealepisode = dealepisode_shop(t4_time_int, t4_quota, t4_net_deals)
    t4_dealepisode._magnitude = 67

    # WHEN
    t4_json = t4_dealepisode.get_json()

    # THEN
    static_t4_json = """{
  "magnitude": 67,
  "net_deals": {
    "Sue": -77
  },
  "quota": 55,
  "time_int": 4
}"""
    print(f"{t4_json=}")
    assert t4_json == static_t4_json


def test_get_dealepisode_from_dict_ReturnsObj_Sccenario0():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_dealepisode = dealepisode_shop(t4_time_int, t4_quota)
    t4_dict = t4_dealepisode.get_dict()
    assert t4_dict == {"time_int": t4_time_int, quota_str(): t4_quota}

    # WHEN
    x_dealepisode = get_dealepisode_from_dict(t4_dict)

    # THEN
    assert x_dealepisode
    assert x_dealepisode.time_int == t4_time_int
    assert x_dealepisode.quota == t4_quota
    assert x_dealepisode._magnitude == 0
    assert x_dealepisode == t4_dealepisode


def test_get_dealepisode_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_magnitude = 65
    t4_net_deals = {"Sue": -77}
    t4_dealepisode = dealepisode_shop(t4_time_int, t4_quota, t4_net_deals)
    t4_dealepisode._magnitude = t4_magnitude
    t4_dict = t4_dealepisode.get_dict()

    # WHEN
    x_dealepisode = get_dealepisode_from_dict(t4_dict)

    # THEN
    assert x_dealepisode
    assert x_dealepisode.time_int == t4_time_int
    assert x_dealepisode.quota == t4_quota
    assert x_dealepisode._magnitude == t4_magnitude
    assert x_dealepisode._net_deals == t4_net_deals
    assert x_dealepisode == t4_dealepisode


def test_get_dealepisode_from_json_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_net_deals = {"Sue": -57}
    t4_dealepisode = dealepisode_shop(t4_time_int, t4_quota, t4_net_deals)
    t4_json = t4_dealepisode.get_json()

    # WHEN
    x_dealepisode = get_dealepisode_from_json(t4_json)

    # THEN
    assert x_dealepisode
    assert x_dealepisode.time_int == t4_time_int
    assert x_dealepisode.quota == t4_quota
    assert x_dealepisode._net_deals == t4_net_deals
    assert x_dealepisode == t4_dealepisode


def test_DealLog_Exists():
    # ESTABLISH / WHEN
    x_deallog = DealLog()

    # THEN
    assert x_deallog
    assert not x_deallog.owner_name
    assert not x_deallog.episodes
    assert not x_deallog._sum_dealepisode_quota
    assert not x_deallog._sum_acct_deals
    assert not x_deallog._time_int_min
    assert not x_deallog._time_int_max


def test_deallog_shop_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"

    # WHEN
    x_deallog = deallog_shop(sue_str)

    # THEN
    assert x_deallog
    assert x_deallog.owner_name == sue_str
    assert x_deallog.episodes == {}
    assert not x_deallog._sum_dealepisode_quota
    assert x_deallog._sum_acct_deals == {}
    assert not x_deallog._time_int_min
    assert not x_deallog._time_int_max


def test_DealLog_set_episode_SetsAttr():
    # ESTABLISH
    sue_deallog = deallog_shop("sue")
    assert sue_deallog.episodes == {}

    # WHEN
    t1_int = 145
    t1_dealepisode = dealepisode_shop(t1_int, 0)
    sue_deallog.set_episode(t1_dealepisode)

    # THEN
    assert sue_deallog.episodes != {}
    assert sue_deallog.episodes.get(t1_int) == t1_dealepisode


def test_DealLog_episode_exists_ReturnsObj():
    # ESTABLISH
    sue_deallog = deallog_shop("Sue")
    t1_int = 145
    assert sue_deallog.episode_exists(t1_int) is False

    # WHEN
    t1_dealepisode = dealepisode_shop(t1_int, 0)
    sue_deallog.set_episode(t1_dealepisode)

    # THEN
    assert sue_deallog.episode_exists(t1_int)


def test_DealLog_get_episode_ReturnsObj():
    # ESTABLISH
    sue_deallog = deallog_shop("sue")
    t1_int = 145
    t1_stat_dealepisode = dealepisode_shop(t1_int, 0)
    sue_deallog.set_episode(t1_stat_dealepisode)

    # WHEN
    t1_gen_dealepisode = sue_deallog.get_episode(t1_int)

    # THEN
    assert t1_gen_dealepisode
    assert t1_gen_dealepisode == t1_stat_dealepisode


def test_DealLog_del_episode_SetsAttr():
    # ESTABLISH
    sue_deallog = deallog_shop("Sue")
    t1_int = 145
    t1_stat_dealepisode = dealepisode_shop(t1_int, 0)
    sue_deallog.set_episode(t1_stat_dealepisode)
    assert sue_deallog.episode_exists(t1_int)

    # WHEN
    sue_deallog.del_episode(t1_int)

    # THEN
    assert sue_deallog.episode_exists(t1_int) is False


def test_DealLog_add_episode_SetsAttr():
    # ESTABLISH
    sue_deallog = deallog_shop("sue")
    assert sue_deallog.episodes == {}

    # WHEN
    t1_int = 145
    t1_quota = 500
    sue_deallog.add_episode(t1_int, x_quota=t1_quota)

    # THEN
    assert sue_deallog.episodes != {}
    t1_dealepisode = dealepisode_shop(t1_int, t1_quota)
    assert sue_deallog.episodes.get(t1_int) == t1_dealepisode


def test_DealLog_get_2d_array_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_deallog = deallog_shop(sue_str)

    # WHEN
    sue_episodes_2d_array = sue_deallog.get_2d_array()

    # THEN
    assert sue_episodes_2d_array == []


def test_DealLog_get_2d_array_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_deallog = deallog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_deallog.add_episode(x4_time_int, x4_quota)
    sue_deallog.add_episode(x7_time_int, x7_quota)

    # WHEN
    sue_episodes_2d_array = sue_deallog.get_2d_array()

    # THEN
    assert sue_episodes_2d_array == [
        [sue_str, x4_time_int, x4_quota],
        [sue_str, x7_time_int, x7_quota],
    ]


def test_DealLog_get_time_ints_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_deallog = deallog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    assert sue_deallog.get_time_ints() == set()

    # WHEN
    sue_deallog.add_episode(x4_time_int, x4_quota)
    sue_deallog.add_episode(x7_time_int, x7_quota)

    # THEN
    assert sue_deallog.get_time_ints() == {x4_time_int, x7_time_int}


def test_DealLog_get_headers_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_deallog = deallog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_deallog.add_episode(x4_time_int, x4_quota)
    sue_deallog.add_episode(x7_time_int, x7_quota)

    # WHEN
    sue_headers_list = sue_deallog.get_headers()

    # THEN
    assert sue_headers_list == ["owner_name", "time_int", quota_str()]


def test_DealLog_get_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_deallog = deallog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_deallog.add_episode(x4_time_int, x4_quota)
    sue_deallog.add_episode(x7_time_int, x7_quota)

    # WHEN
    sue_episodes_dict = sue_deallog.get_dict()

    # THEN
    assert sue_episodes_dict == {
        "owner_name": sue_str,
        "episodes": {
            x4_time_int: {quota_str(): x4_quota, "time_int": x4_time_int},
            x7_time_int: {quota_str(): x7_quota, "time_int": x7_time_int},
        },
    }


def test_get_deallog_from_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_deallog = deallog_shop(sue_str)
    sue_episodes_dict = sue_deallog.get_dict()
    assert sue_episodes_dict == {"owner_name": sue_str, "episodes": {}}

    # WHEN
    x_deallog = get_deallog_from_dict(sue_episodes_dict)

    # THEN
    assert x_deallog
    assert x_deallog.owner_name == sue_str
    assert x_deallog.episodes == {}
    assert x_deallog.episodes == sue_deallog.episodes
    assert x_deallog == sue_deallog


def test_get_deallog_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_deallog = deallog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_deallog.add_episode(x4_time_int, x4_quota)
    sue_deallog.add_episode(x7_time_int, x7_quota)
    sue_episodes_dict = sue_deallog.get_dict()
    assert sue_episodes_dict == {
        "owner_name": sue_str,
        "episodes": {
            x4_time_int: {"time_int": x4_time_int, quota_str(): x4_quota},
            x7_time_int: {"time_int": x7_time_int, quota_str(): x7_quota},
        },
    }

    # WHEN
    x_deallog = get_deallog_from_dict(sue_episodes_dict)

    # THEN
    assert x_deallog
    assert x_deallog.owner_name == sue_str
    assert x_deallog.get_episode(x4_time_int) != None
    assert x_deallog.get_episode(x7_time_int) != None
    assert x_deallog.episodes == sue_deallog.episodes
    assert x_deallog == sue_deallog


def test_get_deallog_from_dict_ReturnsObj_Scenario2():
    # ESTABLISH
    sue_str = "Sue"
    sue_deallog = deallog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_deallog.add_episode(x4_time_int, x4_quota)
    sue_deallog.add_episode(x7_time_int, x7_quota)
    zia_str = "Zia"
    zia_net_deal = 887
    sue_net_deal = 445
    sue_deallog.get_episode(x7_time_int).set_net_deal(sue_str, sue_net_deal)
    sue_deallog.get_episode(x7_time_int).set_net_deal(zia_str, zia_net_deal)
    sue_episodes_dict = sue_deallog.get_dict()
    assert sue_episodes_dict == {
        "owner_name": sue_str,
        "episodes": {
            x4_time_int: {"time_int": x4_time_int, quota_str(): x4_quota},
            x7_time_int: {
                "time_int": x7_time_int,
                quota_str(): x7_quota,
                "net_deals": {sue_str: sue_net_deal, zia_str: zia_net_deal},
            },
        },
    }

    # WHEN
    x_deallog = get_deallog_from_dict(sue_episodes_dict)

    # THEN
    assert x_deallog
    assert x_deallog.owner_name == sue_str
    assert x_deallog.get_episode(x4_time_int) != None
    assert x_deallog.get_episode(x7_time_int) != None
    assert x_deallog.get_episode(x7_time_int)._net_deals != {}
    assert len(x_deallog.get_episode(x7_time_int)._net_deals) == 2
    assert x_deallog.episodes == sue_deallog.episodes
    assert x_deallog == sue_deallog


def test_DealLog_get_tranbook_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_deallog = deallog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_deallog.add_episode(x4_time_int, x4_quota)
    sue_deallog.add_episode(x7_time_int, x7_quota)
    bob_str = "Bob"
    zia_str = "Zia"
    zia_net_deal = 887
    bob_net_deal = 445
    sue_deallog.get_episode(x4_time_int).set_net_deal(bob_str, bob_net_deal)
    sue_deallog.get_episode(x7_time_int).set_net_deal(zia_str, zia_net_deal)
    sue_episodes_dict = sue_deallog.get_dict()
    assert sue_episodes_dict == {
        "owner_name": sue_str,
        "episodes": {
            x4_time_int: {
                "time_int": x4_time_int,
                quota_str(): x4_quota,
                "net_deals": {bob_str: bob_net_deal},
            },
            x7_time_int: {
                "time_int": x7_time_int,
                quota_str(): x7_quota,
                "net_deals": {zia_str: zia_net_deal},
            },
        },
    }

    # WHEN
    x_fiscal_title = "fiscal_title_x"
    sue_tranbook = sue_deallog.get_tranbook(x_fiscal_title)

    # THEN
    assert sue_tranbook
    assert sue_tranbook.fiscal_title == x_fiscal_title
    assert sue_tranbook.tranunit_exists(sue_str, zia_str, x7_time_int)
    assert sue_tranbook.tranunit_exists(sue_str, bob_str, x4_time_int)
    assert sue_tranbook.get_amount(sue_str, zia_str, x7_time_int) == zia_net_deal
    assert sue_tranbook.get_amount(sue_str, bob_str, x4_time_int) == bob_net_deal
