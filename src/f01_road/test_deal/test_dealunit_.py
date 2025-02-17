from src.f01_road.finance import default_fund_pool
from src.f01_road.deal import (
    quota_str,
    time_int_str,
    bridge_str,
    dealdepth_str,
    magnitude_str,
    deal_net_str,
    DealUnit,
    dealunit_shop,
    get_dealunit_from_dict,
    get_dealunit_from_json,
    DEFAULT_DEALDEPTH,
)
from pytest import raises as pytest_raises


def test_str_functions_ReturnObj():
    assert bridge_str() == "bridge"
    assert dealdepth_str() == "dealdepth"
    assert time_int_str() == "time_int"
    assert quota_str() == "quota"
    assert magnitude_str() == "magnitude"
    assert deal_net_str() == "deal_net"


def test_DEFAULT_DEALDEPTH():
    # ESTABLISH / WHEN / THEN
    assert DEFAULT_DEALDEPTH == 2


def test_DealUnit_Exists():
    # ESTABLISH / WHEN
    x_dealunit = DealUnit()

    # THEN
    assert x_dealunit
    assert not x_dealunit.time_int
    assert not x_dealunit.quota
    assert not x_dealunit.dealdepth
    assert not x_dealunit._deal_net
    assert not x_dealunit._magnitude


def test_dealunit_shop_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4

    # WHEN
    t4_dealunit = dealunit_shop(t4_time_int)

    # THEN
    assert t4_dealunit
    assert t4_dealunit.time_int == t4_time_int
    assert t4_dealunit.quota == default_fund_pool()
    assert t4_dealunit._magnitude == 0
    assert t4_dealunit.dealdepth == 2
    assert not t4_dealunit._deal_net


def test_dealunit_shop_ReturnsObjWith_deal_net():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_deal_net = {"Sue": -4}
    t4_magnitude = 677
    t4_dealdepth = 88

    # WHEN
    x_dealunit = dealunit_shop(
        time_int=t4_time_int,
        quota=t4_quota,
        deal_net=t4_deal_net,
        magnitude=t4_magnitude,
        dealdepth=t4_dealdepth,
    )

    # THEN
    assert x_dealunit
    assert x_dealunit.time_int == t4_time_int
    assert x_dealunit.quota == t4_quota
    assert x_dealunit.dealdepth == t4_dealdepth
    assert x_dealunit._magnitude == 677
    assert x_dealunit._deal_net == t4_deal_net


def test_DealUnit_set_deal_net_SetsAttr():
    # ESTABLISH
    yao_dealunit = dealunit_shop("yao", 33)
    assert yao_dealunit._deal_net == {}

    # WHEN
    sue_str = "Sue"
    sue_deal_net = -44
    yao_dealunit.set_deal_net(sue_str, sue_deal_net)

    # THEN
    assert yao_dealunit._deal_net != {}
    assert yao_dealunit._deal_net.get(sue_str) == sue_deal_net


def test_DealUnit_deal_net_exists_ReturnsObj():
    # ESTABLISH
    yao_dealunit = dealunit_shop("yao", 33)
    sue_str = "Sue"
    sue_deal_net = -44
    assert yao_dealunit.deal_net_exists(sue_str) is False

    # WHEN
    yao_dealunit.set_deal_net(sue_str, sue_deal_net)

    # THEN
    assert yao_dealunit.deal_net_exists(sue_str)


def test_DealUnit_get_deal_net_ReturnsObj():
    # ESTABLISH
    yao_dealunit = dealunit_shop("yao", 33)
    sue_str = "Sue"
    sue_deal_net = -44
    yao_dealunit.set_deal_net(sue_str, sue_deal_net)

    # WHEN / THEN
    assert yao_dealunit.get_deal_net(sue_str)
    assert yao_dealunit.get_deal_net(sue_str) == sue_deal_net


def test_DealUnit_del_deal_net_SetsAttr():
    # ESTABLISH
    yao_dealunit = dealunit_shop("yao", 33)
    sue_str = "Sue"
    sue_deal_net = -44
    yao_dealunit.set_deal_net(sue_str, sue_deal_net)
    assert yao_dealunit.deal_net_exists(sue_str)

    # WHEN
    yao_dealunit.del_deal_net(sue_str)

    # THEN
    assert yao_dealunit.deal_net_exists(sue_str) is False


def test_DealUnit_get_dict_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_dealunit = dealunit_shop(t4_time_int, t4_quota)

    # WHEN
    t4_dict = t4_dealunit.get_dict()

    # THEN
    assert t4_dict == {time_int_str(): t4_time_int, quota_str(): t4_quota}


def test_DealUnit_calc_magnitude_SetsAttr_Scenario0():
    # ESTABLISH
    t4_time_int = 4
    t4_dealunit = dealunit_shop(t4_time_int)
    assert t4_dealunit._magnitude == 0

    # WHEN
    t4_dealunit.calc_magnitude()

    # THEN
    assert t4_dealunit._magnitude == 0


def test_DealUnit_calc_magnitude_SetsAttr_Scenario1():
    # ESTABLISH
    t4_time_int = 4
    t4_deal_net = {"Sue": -4, "Yao": 2, "Zia": 2}

    t4_dealunit = dealunit_shop(t4_time_int, deal_net=t4_deal_net)
    assert t4_dealunit._magnitude == 0

    # WHEN
    t4_dealunit.calc_magnitude()

    # THEN
    assert t4_dealunit._magnitude == 4


def test_DealUnit_calc_magnitude_SetsAttr_Scenario2():
    # ESTABLISH
    t4_time_int = 4
    t4_deal_net = {"Bob": -13, "Sue": -7, "Yao": 18, "Zia": 2}

    t4_dealunit = dealunit_shop(t4_time_int, deal_net=t4_deal_net)
    assert t4_dealunit._magnitude == 0

    # WHEN
    t4_dealunit.calc_magnitude()

    # THEN
    assert t4_dealunit._magnitude == 20


def test_DealUnit_calc_magnitude_SetsAttr_Scenario3_RaisesError():
    # ESTABLISH
    t4_time_int = 4
    bob_deal_net = -13
    sue_deal_net = -3
    yao_deal_net = 100
    t4_deal_net = {
        "Bob": bob_deal_net,
        "Sue": sue_deal_net,
        "Yao": yao_deal_net,
    }
    t4_dealunit = dealunit_shop(t4_time_int, deal_net=t4_deal_net)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        t4_dealunit.calc_magnitude()
    exception_str = f"magnitude cannot be calculated: debt_deal_net={bob_deal_net+sue_deal_net}, cred_deal_net={yao_deal_net}"
    assert str(excinfo.value) == exception_str


def test_DealUnit_get_dict_ReturnsObjWith_deal_net():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_deal_net = {"Sue": -4}
    t4_magnitude = 67
    t4_dealdepth = 5
    t4_dealunit = dealunit_shop(
        t4_time_int, t4_quota, t4_deal_net, t4_magnitude, t4_dealdepth
    )

    # WHEN
    t4_dict = t4_dealunit.get_dict()

    # THEN
    assert t4_dict == {
        time_int_str(): t4_time_int,
        quota_str(): t4_quota,
        magnitude_str(): t4_magnitude,
        deal_net_str(): t4_deal_net,
        dealdepth_str(): t4_dealdepth,
    }


def test_DealUnit_get_json_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_deal_net = {"Sue": -77}
    t4_dealunit = dealunit_shop(t4_time_int, t4_quota, t4_deal_net)
    t4_dealunit._magnitude = 67

    # WHEN
    t4_json = t4_dealunit.get_json()

    # THEN
    static_t4_json = """{
  "deal_net": {
    "Sue": -77
  },
  "magnitude": 67,
  "quota": 55,
  "time_int": 4
}"""
    print(f"{t4_json=}")
    assert t4_json == static_t4_json


def test_get_dealunit_from_dict_ReturnsObj_Sccenario0():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_dealunit = dealunit_shop(t4_time_int, t4_quota)
    t4_dict = t4_dealunit.get_dict()
    assert t4_dict == {time_int_str(): t4_time_int, quota_str(): t4_quota}

    # WHEN
    x_dealunit = get_dealunit_from_dict(t4_dict)

    # THEN
    assert x_dealunit
    assert x_dealunit.time_int == t4_time_int
    assert x_dealunit.quota == t4_quota
    assert x_dealunit._magnitude == 0
    assert x_dealunit == t4_dealunit


def test_get_dealunit_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_magnitude = 65
    t4_dealdepth = 33
    t4_deal_net = {"Sue": -77}
    t4_dealunit = dealunit_shop(
        t4_time_int,
        t4_quota,
        t4_deal_net,
        t4_magnitude,
        dealdepth=t4_dealdepth,
    )
    t4_dict = t4_dealunit.get_dict()

    # WHEN
    x_dealunit = get_dealunit_from_dict(t4_dict)

    # THEN
    assert x_dealunit
    assert x_dealunit.time_int == t4_time_int
    assert x_dealunit.quota == t4_quota
    assert x_dealunit._magnitude == t4_magnitude
    assert x_dealunit._deal_net == t4_deal_net
    assert x_dealunit.dealdepth == t4_dealdepth
    assert x_dealunit == t4_dealunit


def test_get_dealunit_from_json_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_deal_net = {"Sue": -57}
    t4_dealunit = dealunit_shop(t4_time_int, t4_quota, t4_deal_net)
    t4_json = t4_dealunit.get_json()

    # WHEN
    x_dealunit = get_dealunit_from_json(t4_json)

    # THEN
    assert x_dealunit
    assert x_dealunit.time_int == t4_time_int
    assert x_dealunit.quota == t4_quota
    assert x_dealunit._deal_net == t4_deal_net
    assert x_dealunit == t4_dealunit
