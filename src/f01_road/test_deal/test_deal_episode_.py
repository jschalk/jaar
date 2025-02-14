from src.f01_road.finance import default_fund_pool
from src.f01_road.deal import (
    quota_str,
    time_int_str,
    bridge_str,
    ledger_depth_str,
    magnitude_str,
    episode_net_str,
    DealEpisode,
    dealepisode_shop,
    get_dealepisode_from_dict,
    get_dealepisode_from_json,
    DEFAULT_DEPTH_LEDGER,
)
from pytest import raises as pytest_raises


def test_str_functions_ReturnObj():
    assert bridge_str() == "bridge"
    assert ledger_depth_str() == "ledger_depth"
    assert time_int_str() == "time_int"
    assert quota_str() == "quota"
    assert magnitude_str() == "magnitude"
    assert episode_net_str() == "episode_net"


def test_DEFAULT_DEPTH_LEDGER():
    # ESTABLISH / WHEN / THEN
    assert DEFAULT_DEPTH_LEDGER == 2


def test_DealEpisode_Exists():
    # ESTABLISH / WHEN
    x_dealepisode = DealEpisode()

    # THEN
    assert x_dealepisode
    assert not x_dealepisode.time_int
    assert not x_dealepisode.quota
    assert not x_dealepisode.ledger_depth
    assert not x_dealepisode._episode_net
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
    assert t4_dealepisode.ledger_depth == 2
    assert not t4_dealepisode._episode_net


def test_dealepisode_shop_ReturnsObjWith_episode_net():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_episode_net = {"Sue": -4}
    t4_magnitude = 677
    t4_ledger_depth = 88

    # WHEN
    x_dealepisode = dealepisode_shop(
        time_int=t4_time_int,
        quota=t4_quota,
        episode_net=t4_episode_net,
        magnitude=t4_magnitude,
        ledger_depth=t4_ledger_depth,
    )

    # THEN
    assert x_dealepisode
    assert x_dealepisode.time_int == t4_time_int
    assert x_dealepisode.quota == t4_quota
    assert x_dealepisode.ledger_depth == t4_ledger_depth
    assert x_dealepisode._magnitude == 677
    assert x_dealepisode._episode_net == t4_episode_net


def test_DealEpisode_set_net_deal_SetsAttr():
    # ESTABLISH
    yao_dealepisode = dealepisode_shop("yao", 33)
    assert yao_dealepisode._episode_net == {}

    # WHEN
    sue_str = "Sue"
    sue_deal = -44
    yao_dealepisode.set_net_deal(sue_str, sue_deal)

    # THEN
    assert yao_dealepisode._episode_net != {}
    assert yao_dealepisode._episode_net.get(sue_str) == sue_deal


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
    t4_episode_net = {"Sue": -4, "Yao": 2, "Zia": 2}

    t4_dealepisode = dealepisode_shop(t4_time_int, episode_net=t4_episode_net)
    assert t4_dealepisode._magnitude == 0

    # WHEN
    t4_dealepisode.calc_magnitude()

    # THEN
    assert t4_dealepisode._magnitude == 4


def test_DealEpisode_calc_magnitude_SetsAttr_Scenario2():
    # ESTABLISH
    t4_time_int = 4
    t4_episode_net = {"Bob": -13, "Sue": -7, "Yao": 18, "Zia": 2}

    t4_dealepisode = dealepisode_shop(t4_time_int, episode_net=t4_episode_net)
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
    t4_episode_net = {"Bob": bob_deal, "Sue": sue_deal, "Yao": yao_deal}
    t4_dealepisode = dealepisode_shop(t4_time_int, episode_net=t4_episode_net)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        t4_dealepisode.calc_magnitude()
    exception_str = f"magnitude cannot be calculated: debt_deal={bob_deal+sue_deal}, cred_deal={yao_deal}"
    assert str(excinfo.value) == exception_str


def test_DealEpisode_get_dict_ReturnsObjWith_episode_net():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_episode_net = {"Sue": -4}
    t4_magnitude = 67
    t4_ledger_depth = 5
    t4_dealepisode = dealepisode_shop(
        t4_time_int, t4_quota, t4_episode_net, t4_magnitude, t4_ledger_depth
    )

    # WHEN
    t4_dict = t4_dealepisode.get_dict()

    # THEN
    assert t4_dict == {
        time_int_str(): t4_time_int,
        quota_str(): t4_quota,
        magnitude_str(): t4_magnitude,
        episode_net_str(): t4_episode_net,
        ledger_depth_str(): t4_ledger_depth,
    }


def test_DealEpisode_get_json_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_episode_net = {"Sue": -77}
    t4_dealepisode = dealepisode_shop(t4_time_int, t4_quota, t4_episode_net)
    t4_dealepisode._magnitude = 67

    # WHEN
    t4_json = t4_dealepisode.get_json()

    # THEN
    static_t4_json = """{
  "episode_net": {
    "Sue": -77
  },
  "magnitude": 67,
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
    t4_ledger_depth = 33
    t4_episode_net = {"Sue": -77}
    t4_dealepisode = dealepisode_shop(
        t4_time_int,
        t4_quota,
        t4_episode_net,
        t4_magnitude,
        ledger_depth=t4_ledger_depth,
    )
    t4_dict = t4_dealepisode.get_dict()

    # WHEN
    x_dealepisode = get_dealepisode_from_dict(t4_dict)

    # THEN
    assert x_dealepisode
    assert x_dealepisode.time_int == t4_time_int
    assert x_dealepisode.quota == t4_quota
    assert x_dealepisode._magnitude == t4_magnitude
    assert x_dealepisode._episode_net == t4_episode_net
    assert x_dealepisode.ledger_depth == t4_ledger_depth
    assert x_dealepisode == t4_dealepisode


def test_get_dealepisode_from_json_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_episode_net = {"Sue": -57}
    t4_dealepisode = dealepisode_shop(t4_time_int, t4_quota, t4_episode_net)
    t4_json = t4_dealepisode.get_json()

    # WHEN
    x_dealepisode = get_dealepisode_from_json(t4_json)

    # THEN
    assert x_dealepisode
    assert x_dealepisode.time_int == t4_time_int
    assert x_dealepisode.quota == t4_quota
    assert x_dealepisode._episode_net == t4_episode_net
    assert x_dealepisode == t4_dealepisode
