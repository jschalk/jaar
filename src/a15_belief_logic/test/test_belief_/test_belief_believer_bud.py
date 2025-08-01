from pytest import raises as pytest_raises
from src.a11_bud_logic.bud import brokerunit_shop
from src.a15_belief_logic.belief_main import beliefunit_shop
from src.a15_belief_logic.test._util.a15_env import get_module_temp_dir


def test_BeliefUnit_set_brokerunit_SetsAttr():
    # ESTABLISH
    amy45_str = "amy45"
    amy_belief = beliefunit_shop(amy45_str, get_module_temp_dir())
    assert amy_belief.brokerunits == {}

    # WHEN
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    amy_belief.set_brokerunit(sue_brokerunit)

    # THEN
    assert amy_belief.brokerunits != {}
    assert amy_belief.brokerunits.get(sue_str) == sue_brokerunit


def test_BeliefUnit_brokerunit_exists_ReturnsObj():
    # ESTABLISH
    amy45_str = "amy45"
    amy_belief = beliefunit_shop(amy45_str, get_module_temp_dir())
    sue_str = "Sue"
    assert amy_belief.brokerunit_exists(sue_str) is False

    # WHEN
    sue_brokerunit = brokerunit_shop(sue_str)
    amy_belief.set_brokerunit(sue_brokerunit)

    # THEN
    assert amy_belief.brokerunit_exists(sue_str)


def test_BeliefUnit_get_brokerunit_ReturnsObj():
    # ESTABLISH
    amy45_str = "amy45"
    amy_belief = beliefunit_shop(amy45_str, get_module_temp_dir())
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    amy_belief.set_brokerunit(sue_brokerunit)
    assert amy_belief.brokerunit_exists(sue_str)

    # WHEN
    sue_gen_brokerunit = amy_belief.get_brokerunit(sue_str)

    # THEN
    assert sue_brokerunit
    assert sue_brokerunit == sue_gen_brokerunit


def test_BeliefUnit_del_brokerunit_SetsAttr():
    # ESTABLISH
    amy45_str = "amy45"
    amy_belief = beliefunit_shop(amy45_str, get_module_temp_dir())
    sue_str = "Sue"
    sue_brokerunit = brokerunit_shop(sue_str)
    amy_belief.set_brokerunit(sue_brokerunit)
    assert amy_belief.brokerunit_exists(sue_str)

    # WHEN
    amy_belief.del_brokerunit(sue_str)

    # THEN
    assert amy_belief.brokerunit_exists(sue_str) is False


def test_BeliefUnit_add_budunit_SetsAttr():
    # ESTABLISH
    amy45_str = "amy45"
    amy_belief = beliefunit_shop(amy45_str, get_module_temp_dir())
    assert amy_belief.brokerunits == {}

    # WHEN
    bob_str = "Bob"
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    amy_belief.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    amy_belief.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    amy_belief.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)

    # THEN
    assert amy_belief.brokerunits != {}
    sue_brokerunit = brokerunit_shop(sue_str)
    sue_brokerunit.add_bud(sue_x4_bud_time, sue_x4_quota)
    sue_brokerunit.add_bud(sue_x7_bud_time, sue_x7_quota)
    bob_brokerunit = brokerunit_shop(bob_str)
    bob_brokerunit.add_bud(bob_x0_bud_time, bob_x0_quota)
    assert amy_belief.get_brokerunit(sue_str) == sue_brokerunit
    assert amy_belief.get_brokerunit(bob_str) == bob_brokerunit


def test_BeliefUnit_get_budunit_ReturnsObj_Scenario0_BrokerDoesNotExist():
    # ESTABLISH
    amy45_str = "amy45"
    amy_belief = beliefunit_shop(amy45_str, get_module_temp_dir())
    sue_str = "Sue"
    sue_x7_bud_time = 7

    # WHEN
    gen_sue_x7_budunit = amy_belief.get_budunit(sue_str, sue_x7_bud_time)

    # THEN
    assert amy_belief.brokerunits == {}
    assert not gen_sue_x7_budunit


def test_BeliefUnit_get_budunit_ReturnsObj_Scenario1_BudDoesNotExist():
    # ESTABLISH
    amy45_str = "amy45"
    amy_belief = beliefunit_shop(amy45_str, get_module_temp_dir())
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 66
    amy_belief.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)

    # WHEN
    sue_x7_bud_time = 7
    gen_sue_x7_budunit = amy_belief.get_budunit(sue_str, sue_x7_bud_time)

    # THEN
    assert amy_belief.brokerunits != {}
    assert not gen_sue_x7_budunit


def test_BeliefUnit_get_budunit_ReturnsObj_Scenario2_BudExists():
    # ESTABLISH
    amy45_str = "amy45"
    amy_belief = beliefunit_shop(amy45_str, get_module_temp_dir())
    bob_str = "Bob"
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    amy_belief.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    amy_belief.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    amy_belief.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)

    # WHEN
    gen_sue_x7_budunit = amy_belief.get_budunit(sue_str, sue_x7_bud_time)

    # THEN
    assert amy_belief.brokerunits != {}
    sue_broker = amy_belief.brokerunits.get(sue_str)
    assert gen_sue_x7_budunit == sue_broker.get_bud(sue_x7_bud_time)


def test_BeliefUnit_get_brokerunits_bud_times_ReturnsObj():
    # ESTABLISH
    amy45_str = "amy45"
    amy_belief = beliefunit_shop(amy45_str, get_module_temp_dir())
    bob_str = "Bob"
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    assert amy_belief.get_brokerunits_bud_times() == set()

    # WHEN
    amy_belief.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    amy_belief.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    amy_belief.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)

    # THEN
    all_bud_times = {bob_x0_bud_time, sue_x4_bud_time, sue_x7_bud_time}
    assert amy_belief.get_brokerunits_bud_times() == all_bud_times


def test_BeliefUnit_add_budunit_RaisesErrorWhen_bud_time_IsLessThan_offi_time_max():
    # ESTABLISH
    amy45_str = "amy45"
    amy_belief = beliefunit_shop(amy45_str, get_module_temp_dir())
    amy_offi_time_max = 606
    amy_belief._offi_time_max = amy_offi_time_max
    bob_str = "Bob"
    bob_x0_bud_time = 707
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 404
    sue_x4_quota = 55
    sue_x7_bud_time = 808
    sue_x7_quota = 66
    assert amy_belief.get_brokerunits_bud_times() == set()
    amy_belief.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    amy_belief.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        amy_belief.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    exception_str = f"Cannot set budunit because bud_time {sue_x4_bud_time} is less than BeliefUnit._offi_time_max {amy_offi_time_max}."
    assert str(excinfo.value) == exception_str


def test_BeliefUnit_add_budunit_DoesNotRaiseError_allow_prev_to_offi_time_max_entry_IsTrue():
    # ESTABLISH
    amy45_str = "amy45"
    amy_belief = beliefunit_shop(amy45_str, get_module_temp_dir())
    amy_offi_time_max = 606
    amy_belief._offi_time_max = amy_offi_time_max
    bob_str = "Bob"
    bob_x0_bud_time = 707
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 404
    sue_x4_quota = 55
    sue_x7_bud_time = 808
    sue_x7_quota = 66
    assert amy_belief.get_brokerunits_bud_times() == set()
    amy_belief.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    amy_belief.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)

    sue_brokerunit = brokerunit_shop(sue_str)
    sue_brokerunit.add_bud(sue_x4_bud_time, sue_x4_quota)
    sue_brokerunit.add_bud(sue_x7_bud_time, sue_x7_quota)
    assert amy_belief.get_brokerunit(sue_str) != sue_brokerunit

    # WHEN
    amy_belief.add_budunit(
        believer_name=sue_str,
        bud_time=sue_x4_bud_time,
        quota=sue_x4_quota,
        allow_prev_to_offi_time_max_entry=True,
    )

    # THEN
    assert amy_belief.brokerunits != {}
    assert amy_belief.get_brokerunit(sue_str) == sue_brokerunit
    bob_brokerunit = brokerunit_shop(bob_str)
    bob_brokerunit.add_bud(bob_x0_bud_time, bob_x0_quota)
    assert amy_belief.get_brokerunit(bob_str) == bob_brokerunit


def test_BeliefUnit_add_budunit_SetsAttr_celldepth():
    # ESTABLISH
    amy45_str = "amy45"
    amy_belief = beliefunit_shop(amy45_str, get_module_temp_dir())
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    sue_x7_celldepth = 5
    assert amy_belief.brokerunits == {}

    # WHEN
    amy_belief.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    amy_belief.add_budunit(
        sue_str, sue_x7_bud_time, sue_x7_quota, celldepth=sue_x7_celldepth
    )

    # THEN
    assert amy_belief.brokerunits != {}
    expected_sue_brokerunit = brokerunit_shop(sue_str)
    expected_sue_brokerunit.add_bud(sue_x4_bud_time, sue_x4_quota)
    expected_sue_brokerunit.add_bud(
        sue_x7_bud_time, sue_x7_quota, celldepth=sue_x7_celldepth
    )
    # print(f"{expected_sue_brokerunit=}")
    gen_sue_brokerunit = amy_belief.get_brokerunit(sue_str)
    gen_sue_x7_bud = gen_sue_brokerunit.get_bud(sue_x7_bud_time)
    print(f"{gen_sue_brokerunit=}")
    assert gen_sue_x7_bud == expected_sue_brokerunit.get_bud(sue_x7_bud_time)
    assert gen_sue_brokerunit.buds == expected_sue_brokerunit.buds
    assert gen_sue_brokerunit == expected_sue_brokerunit
    assert amy_belief.get_brokerunit(sue_str) == expected_sue_brokerunit
