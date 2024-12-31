from src.f01_road.finance import default_fund_pool
from src.f01_road.finance_tran import (
    quota_str,
    time_int_str,
    bridge_str,
    BankEpisode,
    bankepisode_shop,
    BankLog,
    banklog_shop,
    get_bankepisode_from_dict,
    get_bankepisode_from_json,
    get_banklog_from_dict,
)
from pytest import raises as pytest_raises


def test_str_functions_ReturnObj():
    assert bridge_str() == "bridge"
    assert time_int_str() == "time_int"
    assert quota_str() == "quota"


def test_BankEpisode_Exists():
    # ESTABLISH / WHEN
    x_bankepisode = BankEpisode()

    # THEN
    assert x_bankepisode
    assert not x_bankepisode.time_int
    assert not x_bankepisode.quota
    assert not x_bankepisode._net_banks
    assert not x_bankepisode._magnitude


def test_bankepisode_shop_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4

    # WHEN
    t4_bankepisode = bankepisode_shop(t4_time_int)

    # THEN
    assert t4_bankepisode
    assert t4_bankepisode.time_int == t4_time_int
    assert t4_bankepisode.quota == default_fund_pool()
    assert t4_bankepisode._magnitude == 0
    assert not t4_bankepisode._net_banks


def test_bankepisode_shop_ReturnsObjWith_net_banks():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_net_banks = {"Sue": -4}
    t4_magnitude = 677

    # WHEN
    x_bankepisode = bankepisode_shop(
        x_time_int=t4_time_int,
        x_quota=t4_quota,
        net_banks=t4_net_banks,
        x_magnitude=t4_magnitude,
    )

    # THEN
    assert x_bankepisode
    assert x_bankepisode.time_int == t4_time_int
    assert x_bankepisode.quota == t4_quota
    assert x_bankepisode._magnitude == 677
    assert x_bankepisode._net_banks == t4_net_banks


def test_BankEpisode_set_net_bank_SetsAttr():
    # ESTABLISH
    yao_bankepisode = bankepisode_shop("yao", 33)
    assert yao_bankepisode._net_banks == {}

    # WHEN
    sue_str = "Sue"
    sue_bank = -44
    yao_bankepisode.set_net_bank(sue_str, sue_bank)

    # THEN
    assert yao_bankepisode._net_banks != {}
    assert yao_bankepisode._net_banks.get(sue_str) == sue_bank


def test_BankEpisode_net_bank_exists_ReturnsObj():
    # ESTABLISH
    yao_bankepisode = bankepisode_shop("yao", 33)
    sue_str = "Sue"
    sue_bank = -44
    assert yao_bankepisode.net_bank_exists(sue_str) is False

    # WHEN
    yao_bankepisode.set_net_bank(sue_str, sue_bank)

    # THEN
    assert yao_bankepisode.net_bank_exists(sue_str)


def test_BankEpisode_get_net_bank_ReturnsObj():
    # ESTABLISH
    yao_bankepisode = bankepisode_shop("yao", 33)
    sue_str = "Sue"
    sue_bank = -44
    yao_bankepisode.set_net_bank(sue_str, sue_bank)

    # WHEN / THEN
    assert yao_bankepisode.get_net_bank(sue_str)
    assert yao_bankepisode.get_net_bank(sue_str) == sue_bank


def test_BankEpisode_del_net_bank_SetsAttr():
    # ESTABLISH
    yao_bankepisode = bankepisode_shop("yao", 33)
    sue_str = "Sue"
    sue_bank = -44
    yao_bankepisode.set_net_bank(sue_str, sue_bank)
    assert yao_bankepisode.net_bank_exists(sue_str)

    # WHEN
    yao_bankepisode.del_net_bank(sue_str)

    # THEN
    assert yao_bankepisode.net_bank_exists(sue_str) is False


def test_BankEpisode_get_dict_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_bankepisode = bankepisode_shop(t4_time_int, t4_quota)

    # WHEN
    t4_dict = t4_bankepisode.get_dict()

    # THEN
    assert t4_dict == {"time_int": t4_time_int, quota_str(): t4_quota}


def test_BankEpisode_calc_magnitude_SetsAttr_Scenario0():
    # ESTABLISH
    t4_time_int = 4
    t4_bankepisode = bankepisode_shop(t4_time_int)
    assert t4_bankepisode._magnitude == 0

    # WHEN
    t4_bankepisode.calc_magnitude()

    # THEN
    assert t4_bankepisode._magnitude == 0


def test_BankEpisode_calc_magnitude_SetsAttr_Scenario1():
    # ESTABLISH
    t4_time_int = 4
    t4_net_banks = {"Sue": -4, "Yao": 2, "Zia": 2}

    t4_bankepisode = bankepisode_shop(t4_time_int, net_banks=t4_net_banks)
    assert t4_bankepisode._magnitude == 0

    # WHEN
    t4_bankepisode.calc_magnitude()

    # THEN
    assert t4_bankepisode._magnitude == 4


def test_BankEpisode_calc_magnitude_SetsAttr_Scenario2():
    # ESTABLISH
    t4_time_int = 4
    t4_net_banks = {"Bob": -13, "Sue": -7, "Yao": 18, "Zia": 2}

    t4_bankepisode = bankepisode_shop(t4_time_int, net_banks=t4_net_banks)
    assert t4_bankepisode._magnitude == 0

    # WHEN
    t4_bankepisode.calc_magnitude()

    # THEN
    assert t4_bankepisode._magnitude == 20


def test_BankEpisode_calc_magnitude_SetsAttr_Scenario3_RaisesError():
    # ESTABLISH
    t4_time_int = 4
    bob_bank = -13
    sue_bank = -3
    yao_bank = 100
    t4_net_banks = {"Bob": bob_bank, "Sue": sue_bank, "Yao": yao_bank}
    t4_bankepisode = bankepisode_shop(t4_time_int, net_banks=t4_net_banks)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        t4_bankepisode.calc_magnitude()
    exception_str = f"magnitude cannot be calculated: debt_bank={bob_bank+sue_bank}, cred_bank={yao_bank}"
    assert str(excinfo.value) == exception_str


def test_BankEpisode_get_dict_ReturnsObjWith_net_banks():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_net_banks = {"Sue": -4}
    t4_magnitude = 67
    t4_bankepisode = bankepisode_shop(t4_time_int, t4_quota, t4_net_banks)
    t4_bankepisode._magnitude = 67

    # WHEN
    t4_dict = t4_bankepisode.get_dict()

    # THEN
    assert t4_dict == {
        "time_int": t4_time_int,
        quota_str(): t4_quota,
        "magnitude": t4_magnitude,
        "net_banks": t4_net_banks,
    }


def test_BankEpisode_get_json_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_net_banks = {"Sue": -77}
    t4_bankepisode = bankepisode_shop(t4_time_int, t4_quota, t4_net_banks)
    t4_bankepisode._magnitude = 67

    # WHEN
    t4_json = t4_bankepisode.get_json()

    # THEN
    static_t4_json = """{
  "magnitude": 67,
  "net_banks": {
    "Sue": -77
  },
  "quota": 55,
  "time_int": 4
}"""
    print(f"{t4_json=}")
    assert t4_json == static_t4_json


def test_get_bankepisode_from_dict_ReturnsObj_Sccenario0():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_bankepisode = bankepisode_shop(t4_time_int, t4_quota)
    t4_dict = t4_bankepisode.get_dict()
    assert t4_dict == {"time_int": t4_time_int, quota_str(): t4_quota}

    # WHEN
    x_bankepisode = get_bankepisode_from_dict(t4_dict)

    # THEN
    assert x_bankepisode
    assert x_bankepisode.time_int == t4_time_int
    assert x_bankepisode.quota == t4_quota
    assert x_bankepisode._magnitude == 0
    assert x_bankepisode == t4_bankepisode


def test_get_bankepisode_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_magnitude = 65
    t4_net_banks = {"Sue": -77}
    t4_bankepisode = bankepisode_shop(t4_time_int, t4_quota, t4_net_banks)
    t4_bankepisode._magnitude = t4_magnitude
    t4_dict = t4_bankepisode.get_dict()

    # WHEN
    x_bankepisode = get_bankepisode_from_dict(t4_dict)

    # THEN
    assert x_bankepisode
    assert x_bankepisode.time_int == t4_time_int
    assert x_bankepisode.quota == t4_quota
    assert x_bankepisode._magnitude == t4_magnitude
    assert x_bankepisode._net_banks == t4_net_banks
    assert x_bankepisode == t4_bankepisode


def test_get_bankepisode_from_json_ReturnsObj():
    # ESTABLISH
    t4_time_int = 4
    t4_quota = 55
    t4_net_banks = {"Sue": -57}
    t4_bankepisode = bankepisode_shop(t4_time_int, t4_quota, t4_net_banks)
    t4_json = t4_bankepisode.get_json()

    # WHEN
    x_bankepisode = get_bankepisode_from_json(t4_json)

    # THEN
    assert x_bankepisode
    assert x_bankepisode.time_int == t4_time_int
    assert x_bankepisode.quota == t4_quota
    assert x_bankepisode._net_banks == t4_net_banks
    assert x_bankepisode == t4_bankepisode


def test_BankLog_Exists():
    # ESTABLISH / WHEN
    x_banklog = BankLog()

    # THEN
    assert x_banklog
    assert not x_banklog.owner_name
    assert not x_banklog.episodes
    assert not x_banklog._sum_bankepisode_quota
    assert not x_banklog._sum_acct_banks
    assert not x_banklog._time_int_min
    assert not x_banklog._time_int_max


def test_banklog_shop_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"

    # WHEN
    x_banklog = banklog_shop(sue_str)

    # THEN
    assert x_banklog
    assert x_banklog.owner_name == sue_str
    assert x_banklog.episodes == {}
    assert not x_banklog._sum_bankepisode_quota
    assert x_banklog._sum_acct_banks == {}
    assert not x_banklog._time_int_min
    assert not x_banklog._time_int_max


def test_BankLog_set_episode_SetsAttr():
    # ESTABLISH
    sue_banklog = banklog_shop("sue")
    assert sue_banklog.episodes == {}

    # WHEN
    t1_int = 145
    t1_bankepisode = bankepisode_shop(t1_int, 0)
    sue_banklog.set_episode(t1_bankepisode)

    # THEN
    assert sue_banklog.episodes != {}
    assert sue_banklog.episodes.get(t1_int) == t1_bankepisode


def test_BankLog_episode_exists_ReturnsObj():
    # ESTABLISH
    sue_banklog = banklog_shop("Sue")
    t1_int = 145
    assert sue_banklog.episode_exists(t1_int) is False

    # WHEN
    t1_bankepisode = bankepisode_shop(t1_int, 0)
    sue_banklog.set_episode(t1_bankepisode)

    # THEN
    assert sue_banklog.episode_exists(t1_int)


def test_BankLog_get_episode_ReturnsObj():
    # ESTABLISH
    sue_banklog = banklog_shop("sue")
    t1_int = 145
    t1_stat_bankepisode = bankepisode_shop(t1_int, 0)
    sue_banklog.set_episode(t1_stat_bankepisode)

    # WHEN
    t1_gen_bankepisode = sue_banklog.get_episode(t1_int)

    # THEN
    assert t1_gen_bankepisode
    assert t1_gen_bankepisode == t1_stat_bankepisode


def test_BankLog_del_episode_SetsAttr():
    # ESTABLISH
    sue_banklog = banklog_shop("Sue")
    t1_int = 145
    t1_stat_bankepisode = bankepisode_shop(t1_int, 0)
    sue_banklog.set_episode(t1_stat_bankepisode)
    assert sue_banklog.episode_exists(t1_int)

    # WHEN
    sue_banklog.del_episode(t1_int)

    # THEN
    assert sue_banklog.episode_exists(t1_int) is False


def test_BankLog_add_episode_SetsAttr():
    # ESTABLISH
    sue_banklog = banklog_shop("sue")
    assert sue_banklog.episodes == {}

    # WHEN
    t1_int = 145
    t1_quota = 500
    sue_banklog.add_episode(t1_int, x_quota=t1_quota)

    # THEN
    assert sue_banklog.episodes != {}
    t1_bankepisode = bankepisode_shop(t1_int, t1_quota)
    assert sue_banklog.episodes.get(t1_int) == t1_bankepisode


def test_BankLog_get_2d_array_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_banklog = banklog_shop(sue_str)

    # WHEN
    sue_episodes_2d_array = sue_banklog.get_2d_array()

    # THEN
    assert sue_episodes_2d_array == []


def test_BankLog_get_2d_array_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_banklog = banklog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_banklog.add_episode(x4_time_int, x4_quota)
    sue_banklog.add_episode(x7_time_int, x7_quota)

    # WHEN
    sue_episodes_2d_array = sue_banklog.get_2d_array()

    # THEN
    assert sue_episodes_2d_array == [
        [sue_str, x4_time_int, x4_quota],
        [sue_str, x7_time_int, x7_quota],
    ]


def test_BankLog_get_time_ints_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_banklog = banklog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    assert sue_banklog.get_time_ints() == set()

    # WHEN
    sue_banklog.add_episode(x4_time_int, x4_quota)
    sue_banklog.add_episode(x7_time_int, x7_quota)

    # THEN
    assert sue_banklog.get_time_ints() == {x4_time_int, x7_time_int}


def test_BankLog_get_headers_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_banklog = banklog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_banklog.add_episode(x4_time_int, x4_quota)
    sue_banklog.add_episode(x7_time_int, x7_quota)

    # WHEN
    sue_headers_list = sue_banklog.get_headers()

    # THEN
    assert sue_headers_list == ["owner_name", "time_int", quota_str()]


def test_BankLog_get_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_banklog = banklog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_banklog.add_episode(x4_time_int, x4_quota)
    sue_banklog.add_episode(x7_time_int, x7_quota)

    # WHEN
    sue_episodes_dict = sue_banklog.get_dict()

    # THEN
    assert sue_episodes_dict == {
        "owner_name": sue_str,
        "episodes": {
            x4_time_int: {quota_str(): x4_quota, "time_int": x4_time_int},
            x7_time_int: {quota_str(): x7_quota, "time_int": x7_time_int},
        },
    }


def test_get_banklog_from_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_banklog = banklog_shop(sue_str)
    sue_episodes_dict = sue_banklog.get_dict()
    assert sue_episodes_dict == {"owner_name": sue_str, "episodes": {}}

    # WHEN
    x_banklog = get_banklog_from_dict(sue_episodes_dict)

    # THEN
    assert x_banklog
    assert x_banklog.owner_name == sue_str
    assert x_banklog.episodes == {}
    assert x_banklog.episodes == sue_banklog.episodes
    assert x_banklog == sue_banklog


def test_get_banklog_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_banklog = banklog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_banklog.add_episode(x4_time_int, x4_quota)
    sue_banklog.add_episode(x7_time_int, x7_quota)
    sue_episodes_dict = sue_banklog.get_dict()
    assert sue_episodes_dict == {
        "owner_name": sue_str,
        "episodes": {
            x4_time_int: {"time_int": x4_time_int, quota_str(): x4_quota},
            x7_time_int: {"time_int": x7_time_int, quota_str(): x7_quota},
        },
    }

    # WHEN
    x_banklog = get_banklog_from_dict(sue_episodes_dict)

    # THEN
    assert x_banklog
    assert x_banklog.owner_name == sue_str
    assert x_banklog.get_episode(x4_time_int) != None
    assert x_banklog.get_episode(x7_time_int) != None
    assert x_banklog.episodes == sue_banklog.episodes
    assert x_banklog == sue_banklog


def test_get_banklog_from_dict_ReturnsObj_Scenario2():
    # ESTABLISH
    sue_str = "Sue"
    sue_banklog = banklog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_banklog.add_episode(x4_time_int, x4_quota)
    sue_banklog.add_episode(x7_time_int, x7_quota)
    zia_str = "Zia"
    zia_net_bank = 887
    sue_net_bank = 445
    sue_banklog.get_episode(x7_time_int).set_net_bank(sue_str, sue_net_bank)
    sue_banklog.get_episode(x7_time_int).set_net_bank(zia_str, zia_net_bank)
    sue_episodes_dict = sue_banklog.get_dict()
    assert sue_episodes_dict == {
        "owner_name": sue_str,
        "episodes": {
            x4_time_int: {"time_int": x4_time_int, quota_str(): x4_quota},
            x7_time_int: {
                "time_int": x7_time_int,
                quota_str(): x7_quota,
                "net_banks": {sue_str: sue_net_bank, zia_str: zia_net_bank},
            },
        },
    }

    # WHEN
    x_banklog = get_banklog_from_dict(sue_episodes_dict)

    # THEN
    assert x_banklog
    assert x_banklog.owner_name == sue_str
    assert x_banklog.get_episode(x4_time_int) != None
    assert x_banklog.get_episode(x7_time_int) != None
    assert x_banklog.get_episode(x7_time_int)._net_banks != {}
    assert len(x_banklog.get_episode(x7_time_int)._net_banks) == 2
    assert x_banklog.episodes == sue_banklog.episodes
    assert x_banklog == sue_banklog


def test_BankLog_get_tranbook_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_banklog = banklog_shop(sue_str)
    x4_time_int = 4
    x4_quota = 55
    x7_time_int = 7
    x7_quota = 66
    sue_banklog.add_episode(x4_time_int, x4_quota)
    sue_banklog.add_episode(x7_time_int, x7_quota)
    bob_str = "Bob"
    zia_str = "Zia"
    zia_net_bank = 887
    bob_net_bank = 445
    sue_banklog.get_episode(x4_time_int).set_net_bank(bob_str, bob_net_bank)
    sue_banklog.get_episode(x7_time_int).set_net_bank(zia_str, zia_net_bank)
    sue_episodes_dict = sue_banklog.get_dict()
    assert sue_episodes_dict == {
        "owner_name": sue_str,
        "episodes": {
            x4_time_int: {
                "time_int": x4_time_int,
                quota_str(): x4_quota,
                "net_banks": {bob_str: bob_net_bank},
            },
            x7_time_int: {
                "time_int": x7_time_int,
                quota_str(): x7_quota,
                "net_banks": {zia_str: zia_net_bank},
            },
        },
    }

    # WHEN
    x_deal_idea = "deal_idea_x"
    sue_tranbook = sue_banklog.get_tranbook(x_deal_idea)

    # THEN
    assert sue_tranbook
    assert sue_tranbook.deal_idea == x_deal_idea
    assert sue_tranbook.tranunit_exists(sue_str, zia_str, x7_time_int)
    assert sue_tranbook.tranunit_exists(sue_str, bob_str, x4_time_int)
    assert sue_tranbook.get_amount(sue_str, zia_str, x7_time_int) == zia_net_bank
    assert sue_tranbook.get_amount(sue_str, bob_str, x4_time_int) == bob_net_bank
