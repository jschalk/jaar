from pytest import raises as pytest_raises
from src.a02_finance_logic.finance_config import default_fund_pool
from src.a11_bud_logic.bud import (
    DEFAULT_CELLDEPTH,
    BudUnit,
    budunit_shop,
    get_budunit_from_dict,
    get_budunit_from_json,
)
from src.a11_bud_logic.test._util.a11_terms import (
    bud_time_str,
    bud_voice_nets_str,
    celldepth_str,
    magnitude_str,
    quota_str,
)


def test_DEFAULT_CELLDEPTH():
    # ESTABLISH / WHEN / THEN
    assert DEFAULT_CELLDEPTH == 2


def test_BudUnit_Exists():
    # ESTABLISH / WHEN
    x_budunit = BudUnit()

    # THEN
    assert x_budunit
    assert not x_budunit.bud_time
    assert not x_budunit.quota
    assert not x_budunit.celldepth
    assert not x_budunit._bud_voice_nets
    assert not x_budunit._magnitude


def test_budunit_shop_ReturnsObj():
    # ESTABLISH
    t4_bud_time = 4

    # WHEN
    t4_budunit = budunit_shop(t4_bud_time)

    # THEN
    assert t4_budunit
    assert t4_budunit.bud_time == t4_bud_time
    assert t4_budunit.quota == default_fund_pool()
    assert t4_budunit._magnitude == 0
    assert t4_budunit.celldepth == 2
    assert not t4_budunit._bud_voice_nets


def test_budunit_shop_ReturnsObjWith_bud_voice_net():
    # ESTABLISH
    t4_bud_time = 4
    t4_quota = 55
    t4_bud_voice_nets = {"Sue": -4}
    t4_magnitude = 677
    t4_celldepth = 88

    # WHEN
    x_budunit = budunit_shop(
        bud_time=t4_bud_time,
        quota=t4_quota,
        bud_voice_nets=t4_bud_voice_nets,
        magnitude=t4_magnitude,
        celldepth=t4_celldepth,
    )

    # THEN
    assert x_budunit
    assert x_budunit.bud_time == t4_bud_time
    assert x_budunit.quota == t4_quota
    assert x_budunit.celldepth == t4_celldepth
    assert x_budunit._magnitude == 677
    assert x_budunit._bud_voice_nets == t4_bud_voice_nets


def test_BudUnit_set_bud_voice_net_SetsAttr():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao", 33)
    assert yao_budunit._bud_voice_nets == {}

    # WHEN
    sue_str = "Sue"
    sue_bud_voice_net = -44
    yao_budunit.set_bud_voice_net(sue_str, sue_bud_voice_net)

    # THEN
    assert yao_budunit._bud_voice_nets != {}
    assert yao_budunit._bud_voice_nets.get(sue_str) == sue_bud_voice_net


def test_BudUnit_bud_voice_net_exists_ReturnsObj():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao", 33)
    sue_str = "Sue"
    sue_bud_voice_net = -44
    assert yao_budunit.bud_voice_net_exists(sue_str) is False

    # WHEN
    yao_budunit.set_bud_voice_net(sue_str, sue_bud_voice_net)

    # THEN
    assert yao_budunit.bud_voice_net_exists(sue_str)


def test_BudUnit_get_bud_voice_net_ReturnsObj():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao", 33)
    sue_str = "Sue"
    sue_bud_voice_net = -44
    yao_budunit.set_bud_voice_net(sue_str, sue_bud_voice_net)

    # WHEN / THEN
    assert yao_budunit.get_bud_voice_net(sue_str)
    assert yao_budunit.get_bud_voice_net(sue_str) == sue_bud_voice_net


def test_BudUnit_del_bud_voice_net_SetsAttr():
    # ESTABLISH
    yao_budunit = budunit_shop("Yao", 33)
    sue_str = "Sue"
    sue_bud_voice_net = -44
    yao_budunit.set_bud_voice_net(sue_str, sue_bud_voice_net)
    assert yao_budunit.bud_voice_net_exists(sue_str)

    # WHEN
    yao_budunit.del_bud_voice_net(sue_str)

    # THEN
    assert yao_budunit.bud_voice_net_exists(sue_str) is False


def test_BudUnit_to_dict_ReturnsObj():
    # ESTABLISH
    t4_bud_time = 4
    t4_quota = 55
    t4_budunit = budunit_shop(t4_bud_time, t4_quota)

    # WHEN
    t4_dict = t4_budunit.to_dict()

    # THEN
    assert t4_dict == {bud_time_str(): t4_bud_time, quota_str(): t4_quota}


def test_BudUnit_calc_magnitude_SetsAttr_Scenario0():
    # ESTABLISH
    t4_bud_time = 4
    t4_budunit = budunit_shop(t4_bud_time)
    assert t4_budunit._magnitude == 0

    # WHEN
    t4_budunit.calc_magnitude()

    # THEN
    assert t4_budunit._magnitude == 0


def test_BudUnit_calc_magnitude_SetsAttr_Scenario1():
    # ESTABLISH
    t4_bud_time = 4
    t4_bud_voice_nets = {"Sue": -4, "Yao": 2, "Zia": 2}

    t4_budunit = budunit_shop(t4_bud_time, bud_voice_nets=t4_bud_voice_nets)
    assert t4_budunit._magnitude == 0

    # WHEN
    t4_budunit.calc_magnitude()

    # THEN
    assert t4_budunit._magnitude == 4


def test_BudUnit_calc_magnitude_SetsAttr_Scenario2():
    # ESTABLISH
    t4_bud_time = 4
    t4_bud_voice_nets = {"Bob": -13, "Sue": -7, "Yao": 18, "Zia": 2}

    t4_budunit = budunit_shop(t4_bud_time, bud_voice_nets=t4_bud_voice_nets)
    assert t4_budunit._magnitude == 0

    # WHEN
    t4_budunit.calc_magnitude()

    # THEN
    assert t4_budunit._magnitude == 20


def test_BudUnit_calc_magnitude_SetsAttr_Scenario3_RaisesError():
    # ESTABLISH
    t4_bud_time = 4
    bob_bud_voice_net = -13
    sue_bud_voice_net = -3
    yao_bud_voice_net = 100
    t4_bud_voice_nets = {
        "Bob": bob_bud_voice_net,
        "Sue": sue_bud_voice_net,
        "Yao": yao_bud_voice_net,
    }
    t4_budunit = budunit_shop(t4_bud_time, bud_voice_nets=t4_bud_voice_nets)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        t4_budunit.calc_magnitude()
    exception_str = f"magnitude cannot be calculated: debt_bud_voice_net={bob_bud_voice_net+sue_bud_voice_net}, cred_bud_voice_net={yao_bud_voice_net}"
    assert str(excinfo.value) == exception_str


def test_BudUnit_to_dict_ReturnsObjWith_bud_voice_net():
    # ESTABLISH
    t4_bud_time = 4
    t4_quota = 55
    t4_bud_voice_nets = {"Sue": -4}
    t4_magnitude = 67
    t4_celldepth = 5
    t4_budunit = budunit_shop(
        t4_bud_time, t4_quota, t4_bud_voice_nets, t4_magnitude, t4_celldepth
    )

    # WHEN
    t4_dict = t4_budunit.to_dict()

    # THEN
    assert t4_dict == {
        bud_time_str(): t4_bud_time,
        quota_str(): t4_quota,
        magnitude_str(): t4_magnitude,
        bud_voice_nets_str(): t4_bud_voice_nets,
        celldepth_str(): t4_celldepth,
    }


def test_BudUnit_get_json_ReturnsObj():
    # ESTABLISH
    t4_bud_time = 4
    t4_quota = 55
    t4_celldepth = 11
    t4_bud_voice_nets = {"Sue": -77}
    t4_budunit = budunit_shop(
        t4_bud_time, t4_quota, t4_bud_voice_nets, celldepth=t4_celldepth
    )
    t4_budunit._magnitude = 67

    # WHEN
    t4_json = t4_budunit.get_json()

    # THEN
    static_t4_json = """{
  "bud_time": 4,
  "bud_voice_nets": {
    "Sue": -77
  },
  "celldepth": 11,
  "magnitude": 67,
  "quota": 55
}"""
    print(f"{t4_json=}")
    assert t4_json == static_t4_json


def test_get_budunit_from_dict_ReturnsObj_Sccenario0():
    # ESTABLISH
    t4_bud_time = 4
    t4_quota = 55
    t4_budunit = budunit_shop(t4_bud_time, t4_quota)
    t4_dict = t4_budunit.to_dict()
    assert t4_dict == {bud_time_str(): t4_bud_time, quota_str(): t4_quota}

    # WHEN
    x_budunit = get_budunit_from_dict(t4_dict)

    # THEN
    assert x_budunit
    assert x_budunit.bud_time == t4_bud_time
    assert x_budunit.quota == t4_quota
    assert x_budunit._magnitude == 0
    assert x_budunit == t4_budunit


def test_get_budunit_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    t4_bud_time = 4
    t4_quota = 55
    t4_magnitude = 65
    t4_celldepth = 33
    t4_bud_voice_nets = {"Sue": -77}
    t4_budunit = budunit_shop(
        t4_bud_time,
        t4_quota,
        t4_bud_voice_nets,
        t4_magnitude,
        celldepth=t4_celldepth,
    )
    t4_dict = t4_budunit.to_dict()

    # WHEN
    x_budunit = get_budunit_from_dict(t4_dict)

    # THEN
    assert x_budunit
    assert x_budunit.bud_time == t4_bud_time
    assert x_budunit.quota == t4_quota
    assert x_budunit._magnitude == t4_magnitude
    assert x_budunit._bud_voice_nets == t4_bud_voice_nets
    assert x_budunit.celldepth == t4_celldepth
    assert x_budunit == t4_budunit


def test_get_budunit_from_json_ReturnsObj():
    # ESTABLISH
    t4_bud_time = 4
    t4_quota = 55
    t4_bud_voice_nets = {"Sue": -57}
    t4_budunit = budunit_shop(t4_bud_time, t4_quota, t4_bud_voice_nets)
    t4_json = t4_budunit.get_json()

    # WHEN
    x_budunit = get_budunit_from_json(t4_json)

    # THEN
    assert x_budunit
    assert x_budunit.bud_time == t4_bud_time
    assert x_budunit.quota == t4_quota
    assert x_budunit._bud_voice_nets == t4_bud_voice_nets
    assert x_budunit == t4_budunit
