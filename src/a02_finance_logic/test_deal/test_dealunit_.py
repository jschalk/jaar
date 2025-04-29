from src.a02_finance_logic.finance_config import default_fund_pool
from src.a02_finance_logic.deal import (
    DealUnit,
    dealunit_shop,
    get_dealunit_from_dict,
    get_dealunit_from_json,
    DEFAULT_CELLDEPTH,
)
from src.a02_finance_logic._utils.str_helpers import (
    quota_str,
    deal_time_str,
    tran_time_str,
    bridge_str,
    celldepth_str,
    magnitude_str,
    deal_acct_nets_str,
    world_id_str,
)

from pytest import raises as pytest_raises


def test_str_functions_ReturnObj():
    assert bridge_str() == "bridge"
    assert celldepth_str() == "celldepth"
    assert deal_time_str() == "deal_time"
    assert tran_time_str() == "tran_time"
    assert quota_str() == "quota"
    assert magnitude_str() == "magnitude"
    assert deal_acct_nets_str() == "deal_acct_nets"
    assert world_id_str() == "world_id"


def test_DEFAULT_CELLDEPTH():
    # ESTABLISH / WHEN / THEN
    assert DEFAULT_CELLDEPTH == 2


def test_DealUnit_Exists():
    # ESTABLISH / WHEN
    x_dealunit = DealUnit()

    # THEN
    assert x_dealunit
    assert not x_dealunit.deal_time
    assert not x_dealunit.quota
    assert not x_dealunit.celldepth
    assert not x_dealunit._deal_acct_nets
    assert not x_dealunit._magnitude


def test_dealunit_shop_ReturnsObj():
    # ESTABLISH
    t4_deal_time = 4

    # WHEN
    t4_dealunit = dealunit_shop(t4_deal_time)

    # THEN
    assert t4_dealunit
    assert t4_dealunit.deal_time == t4_deal_time
    assert t4_dealunit.quota == default_fund_pool()
    assert t4_dealunit._magnitude == 0
    assert t4_dealunit.celldepth == 2
    assert not t4_dealunit._deal_acct_nets


def test_dealunit_shop_ReturnsObjWith_deal_acct_net():
    # ESTABLISH
    t4_deal_time = 4
    t4_quota = 55
    t4_deal_acct_nets = {"Sue": -4}
    t4_magnitude = 677
    t4_celldepth = 88

    # WHEN
    x_dealunit = dealunit_shop(
        deal_time=t4_deal_time,
        quota=t4_quota,
        deal_acct_nets=t4_deal_acct_nets,
        magnitude=t4_magnitude,
        celldepth=t4_celldepth,
    )

    # THEN
    assert x_dealunit
    assert x_dealunit.deal_time == t4_deal_time
    assert x_dealunit.quota == t4_quota
    assert x_dealunit.celldepth == t4_celldepth
    assert x_dealunit._magnitude == 677
    assert x_dealunit._deal_acct_nets == t4_deal_acct_nets


def test_DealUnit_set_deal_acct_net_SetsAttr():
    # ESTABLISH
    yao_dealunit = dealunit_shop("yao", 33)
    assert yao_dealunit._deal_acct_nets == {}

    # WHEN
    sue_str = "Sue"
    sue_deal_acct_net = -44
    yao_dealunit.set_deal_acct_net(sue_str, sue_deal_acct_net)

    # THEN
    assert yao_dealunit._deal_acct_nets != {}
    assert yao_dealunit._deal_acct_nets.get(sue_str) == sue_deal_acct_net


def test_DealUnit_deal_acct_net_exists_ReturnsObj():
    # ESTABLISH
    yao_dealunit = dealunit_shop("yao", 33)
    sue_str = "Sue"
    sue_deal_acct_net = -44
    assert yao_dealunit.deal_acct_net_exists(sue_str) is False

    # WHEN
    yao_dealunit.set_deal_acct_net(sue_str, sue_deal_acct_net)

    # THEN
    assert yao_dealunit.deal_acct_net_exists(sue_str)


def test_DealUnit_get_deal_acct_net_ReturnsObj():
    # ESTABLISH
    yao_dealunit = dealunit_shop("yao", 33)
    sue_str = "Sue"
    sue_deal_acct_net = -44
    yao_dealunit.set_deal_acct_net(sue_str, sue_deal_acct_net)

    # WHEN / THEN
    assert yao_dealunit.get_deal_acct_net(sue_str)
    assert yao_dealunit.get_deal_acct_net(sue_str) == sue_deal_acct_net


def test_DealUnit_del_deal_acct_net_SetsAttr():
    # ESTABLISH
    yao_dealunit = dealunit_shop("yao", 33)
    sue_str = "Sue"
    sue_deal_acct_net = -44
    yao_dealunit.set_deal_acct_net(sue_str, sue_deal_acct_net)
    assert yao_dealunit.deal_acct_net_exists(sue_str)

    # WHEN
    yao_dealunit.del_deal_acct_net(sue_str)

    # THEN
    assert yao_dealunit.deal_acct_net_exists(sue_str) is False


def test_DealUnit_get_dict_ReturnsObj():
    # ESTABLISH
    t4_deal_time = 4
    t4_quota = 55
    t4_dealunit = dealunit_shop(t4_deal_time, t4_quota)

    # WHEN
    t4_dict = t4_dealunit.get_dict()

    # THEN
    assert t4_dict == {deal_time_str(): t4_deal_time, quota_str(): t4_quota}


def test_DealUnit_calc_magnitude_SetsAttr_Scenario0():
    # ESTABLISH
    t4_deal_time = 4
    t4_dealunit = dealunit_shop(t4_deal_time)
    assert t4_dealunit._magnitude == 0

    # WHEN
    t4_dealunit.calc_magnitude()

    # THEN
    assert t4_dealunit._magnitude == 0


def test_DealUnit_calc_magnitude_SetsAttr_Scenario1():
    # ESTABLISH
    t4_deal_time = 4
    t4_deal_acct_nets = {"Sue": -4, "Yao": 2, "Zia": 2}

    t4_dealunit = dealunit_shop(t4_deal_time, deal_acct_nets=t4_deal_acct_nets)
    assert t4_dealunit._magnitude == 0

    # WHEN
    t4_dealunit.calc_magnitude()

    # THEN
    assert t4_dealunit._magnitude == 4


def test_DealUnit_calc_magnitude_SetsAttr_Scenario2():
    # ESTABLISH
    t4_deal_time = 4
    t4_deal_acct_nets = {"Bob": -13, "Sue": -7, "Yao": 18, "Zia": 2}

    t4_dealunit = dealunit_shop(t4_deal_time, deal_acct_nets=t4_deal_acct_nets)
    assert t4_dealunit._magnitude == 0

    # WHEN
    t4_dealunit.calc_magnitude()

    # THEN
    assert t4_dealunit._magnitude == 20


def test_DealUnit_calc_magnitude_SetsAttr_Scenario3_RaisesError():
    # ESTABLISH
    t4_deal_time = 4
    bob_deal_acct_net = -13
    sue_deal_acct_net = -3
    yao_deal_acct_net = 100
    t4_deal_acct_nets = {
        "Bob": bob_deal_acct_net,
        "Sue": sue_deal_acct_net,
        "Yao": yao_deal_acct_net,
    }
    t4_dealunit = dealunit_shop(t4_deal_time, deal_acct_nets=t4_deal_acct_nets)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        t4_dealunit.calc_magnitude()
    exception_str = f"magnitude cannot be calculated: debt_deal_acct_net={bob_deal_acct_net+sue_deal_acct_net}, cred_deal_acct_net={yao_deal_acct_net}"
    assert str(excinfo.value) == exception_str


def test_DealUnit_get_dict_ReturnsObjWith_deal_acct_net():
    # ESTABLISH
    t4_deal_time = 4
    t4_quota = 55
    t4_deal_acct_nets = {"Sue": -4}
    t4_magnitude = 67
    t4_celldepth = 5
    t4_dealunit = dealunit_shop(
        t4_deal_time, t4_quota, t4_deal_acct_nets, t4_magnitude, t4_celldepth
    )

    # WHEN
    t4_dict = t4_dealunit.get_dict()

    # THEN
    assert t4_dict == {
        deal_time_str(): t4_deal_time,
        quota_str(): t4_quota,
        magnitude_str(): t4_magnitude,
        deal_acct_nets_str(): t4_deal_acct_nets,
        celldepth_str(): t4_celldepth,
    }


def test_DealUnit_get_json_ReturnsObj():
    # ESTABLISH
    t4_deal_time = 4
    t4_quota = 55
    t4_celldepth = 11
    t4_deal_acct_nets = {"Sue": -77}
    t4_dealunit = dealunit_shop(
        t4_deal_time, t4_quota, t4_deal_acct_nets, celldepth=t4_celldepth
    )
    t4_dealunit._magnitude = 67

    # WHEN
    t4_json = t4_dealunit.get_json()

    # THEN
    static_t4_json = """{
  "celldepth": 11,
  "deal_acct_nets": {
    "Sue": -77
  },
  "deal_time": 4,
  "magnitude": 67,
  "quota": 55
}"""
    print(f"{t4_json=}")
    assert t4_json == static_t4_json


def test_get_dealunit_from_dict_ReturnsObj_Sccenario0():
    # ESTABLISH
    t4_deal_time = 4
    t4_quota = 55
    t4_dealunit = dealunit_shop(t4_deal_time, t4_quota)
    t4_dict = t4_dealunit.get_dict()
    assert t4_dict == {deal_time_str(): t4_deal_time, quota_str(): t4_quota}

    # WHEN
    x_dealunit = get_dealunit_from_dict(t4_dict)

    # THEN
    assert x_dealunit
    assert x_dealunit.deal_time == t4_deal_time
    assert x_dealunit.quota == t4_quota
    assert x_dealunit._magnitude == 0
    assert x_dealunit == t4_dealunit


def test_get_dealunit_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    t4_deal_time = 4
    t4_quota = 55
    t4_magnitude = 65
    t4_celldepth = 33
    t4_deal_acct_nets = {"Sue": -77}
    t4_dealunit = dealunit_shop(
        t4_deal_time,
        t4_quota,
        t4_deal_acct_nets,
        t4_magnitude,
        celldepth=t4_celldepth,
    )
    t4_dict = t4_dealunit.get_dict()

    # WHEN
    x_dealunit = get_dealunit_from_dict(t4_dict)

    # THEN
    assert x_dealunit
    assert x_dealunit.deal_time == t4_deal_time
    assert x_dealunit.quota == t4_quota
    assert x_dealunit._magnitude == t4_magnitude
    assert x_dealunit._deal_acct_nets == t4_deal_acct_nets
    assert x_dealunit.celldepth == t4_celldepth
    assert x_dealunit == t4_dealunit


def test_get_dealunit_from_json_ReturnsObj():
    # ESTABLISH
    t4_deal_time = 4
    t4_quota = 55
    t4_deal_acct_nets = {"Sue": -57}
    t4_dealunit = dealunit_shop(t4_deal_time, t4_quota, t4_deal_acct_nets)
    t4_json = t4_dealunit.get_json()

    # WHEN
    x_dealunit = get_dealunit_from_json(t4_json)

    # THEN
    assert x_dealunit
    assert x_dealunit.deal_time == t4_deal_time
    assert x_dealunit.quota == t4_quota
    assert x_dealunit._deal_acct_nets == t4_deal_acct_nets
    assert x_dealunit == t4_dealunit
