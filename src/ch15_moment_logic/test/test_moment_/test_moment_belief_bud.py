from pytest import raises as pytest_raises
from src.ch11_bud_logic.bud import beliefbudhistory_shop
from src.ch15_moment_logic.moment_main import momentunit_shop
from src.ch15_moment_logic.test._util.ch15_env import get_chapter_temp_dir


def test_MomentUnit_set_beliefbudhistory_SetsAttr():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_chapter_temp_dir())
    assert amy_moment.beliefbudhistorys == {}

    # WHEN
    sue_str = "Sue"
    sue_beliefbudhistory = beliefbudhistory_shop(sue_str)
    amy_moment.set_beliefbudhistory(sue_beliefbudhistory)

    # THEN
    assert amy_moment.beliefbudhistorys != {}
    assert amy_moment.beliefbudhistorys.get(sue_str) == sue_beliefbudhistory


def test_MomentUnit_beliefbudhistory_exists_ReturnsObj():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_chapter_temp_dir())
    sue_str = "Sue"
    assert amy_moment.beliefbudhistory_exists(sue_str) is False

    # WHEN
    sue_beliefbudhistory = beliefbudhistory_shop(sue_str)
    amy_moment.set_beliefbudhistory(sue_beliefbudhistory)

    # THEN
    assert amy_moment.beliefbudhistory_exists(sue_str)


def test_MomentUnit_get_beliefbudhistory_ReturnsObj():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_chapter_temp_dir())
    sue_str = "Sue"
    sue_beliefbudhistory = beliefbudhistory_shop(sue_str)
    amy_moment.set_beliefbudhistory(sue_beliefbudhistory)
    assert amy_moment.beliefbudhistory_exists(sue_str)

    # WHEN
    sue_gen_beliefbudhistory = amy_moment.get_beliefbudhistory(sue_str)

    # THEN
    assert sue_beliefbudhistory
    assert sue_beliefbudhistory == sue_gen_beliefbudhistory


def test_MomentUnit_del_beliefbudhistory_SetsAttr():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_chapter_temp_dir())
    sue_str = "Sue"
    sue_beliefbudhistory = beliefbudhistory_shop(sue_str)
    amy_moment.set_beliefbudhistory(sue_beliefbudhistory)
    assert amy_moment.beliefbudhistory_exists(sue_str)

    # WHEN
    amy_moment.del_beliefbudhistory(sue_str)

    # THEN
    assert amy_moment.beliefbudhistory_exists(sue_str) is False


def test_MomentUnit_add_budunit_SetsAttr():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_chapter_temp_dir())
    assert amy_moment.beliefbudhistorys == {}

    # WHEN
    bob_str = "Bob"
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    amy_moment.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    amy_moment.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    amy_moment.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)

    # THEN
    assert amy_moment.beliefbudhistorys != {}
    sue_beliefbudhistory = beliefbudhistory_shop(sue_str)
    sue_beliefbudhistory.add_bud(sue_x4_bud_time, sue_x4_quota)
    sue_beliefbudhistory.add_bud(sue_x7_bud_time, sue_x7_quota)
    bob_beliefbudhistory = beliefbudhistory_shop(bob_str)
    bob_beliefbudhistory.add_bud(bob_x0_bud_time, bob_x0_quota)
    assert amy_moment.get_beliefbudhistory(sue_str) == sue_beliefbudhistory
    assert amy_moment.get_beliefbudhistory(bob_str) == bob_beliefbudhistory


def test_MomentUnit_get_budunit_ReturnsObj_Scenario0_BrokerDoesNotExist():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_chapter_temp_dir())
    sue_str = "Sue"
    sue_x7_bud_time = 7

    # WHEN
    gen_sue_x7_budunit = amy_moment.get_budunit(sue_str, sue_x7_bud_time)

    # THEN
    assert amy_moment.beliefbudhistorys == {}
    assert not gen_sue_x7_budunit


def test_MomentUnit_get_budunit_ReturnsObj_Scenario1_BudDoesNotExist():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_chapter_temp_dir())
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 66
    amy_moment.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)

    # WHEN
    sue_x7_bud_time = 7
    gen_sue_x7_budunit = amy_moment.get_budunit(sue_str, sue_x7_bud_time)

    # THEN
    assert amy_moment.beliefbudhistorys != {}
    assert not gen_sue_x7_budunit


def test_MomentUnit_get_budunit_ReturnsObj_Scenario2_BudExists():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_chapter_temp_dir())
    bob_str = "Bob"
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    amy_moment.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    amy_moment.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    amy_moment.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)

    # WHEN
    gen_sue_x7_budunit = amy_moment.get_budunit(sue_str, sue_x7_bud_time)

    # THEN
    assert amy_moment.beliefbudhistorys != {}
    sue_broker = amy_moment.beliefbudhistorys.get(sue_str)
    assert gen_sue_x7_budunit == sue_broker.get_bud(sue_x7_bud_time)


def test_MomentUnit_get_beliefbudhistorys_bud_times_ReturnsObj():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_chapter_temp_dir())
    bob_str = "Bob"
    bob_x0_bud_time = 702
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    assert amy_moment.get_beliefbudhistorys_bud_times() == set()

    # WHEN
    amy_moment.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    amy_moment.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    amy_moment.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)

    # THEN
    all_bud_times = {bob_x0_bud_time, sue_x4_bud_time, sue_x7_bud_time}
    assert amy_moment.get_beliefbudhistorys_bud_times() == all_bud_times


def test_MomentUnit_add_budunit_RaisesErrorWhen_bud_time_IsLessThan_offi_time_max():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_chapter_temp_dir())
    amy_offi_time_max = 606
    amy_moment.offi_time_max = amy_offi_time_max
    bob_str = "Bob"
    bob_x0_bud_time = 707
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 404
    sue_x4_quota = 55
    sue_x7_bud_time = 808
    sue_x7_quota = 66
    assert amy_moment.get_beliefbudhistorys_bud_times() == set()
    amy_moment.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    amy_moment.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        amy_moment.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    exception_str = f"Cannot set budunit because bud_time {sue_x4_bud_time} is less than MomentUnit.offi_time_max {amy_offi_time_max}."
    assert str(excinfo.value) == exception_str


def test_MomentUnit_add_budunit_DoesNotRaiseError_allow_prev_to_offi_time_max_entry_IsTrue():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_chapter_temp_dir())
    amy_offi_time_max = 606
    amy_moment.offi_time_max = amy_offi_time_max
    bob_str = "Bob"
    bob_x0_bud_time = 707
    bob_x0_quota = 33
    sue_str = "Sue"
    sue_x4_bud_time = 404
    sue_x4_quota = 55
    sue_x7_bud_time = 808
    sue_x7_quota = 66
    assert amy_moment.get_beliefbudhistorys_bud_times() == set()
    amy_moment.add_budunit(bob_str, bob_x0_bud_time, bob_x0_quota)
    amy_moment.add_budunit(sue_str, sue_x7_bud_time, sue_x7_quota)

    sue_beliefbudhistory = beliefbudhistory_shop(sue_str)
    sue_beliefbudhistory.add_bud(sue_x4_bud_time, sue_x4_quota)
    sue_beliefbudhistory.add_bud(sue_x7_bud_time, sue_x7_quota)
    assert amy_moment.get_beliefbudhistory(sue_str) != sue_beliefbudhistory

    # WHEN
    amy_moment.add_budunit(
        belief_name=sue_str,
        bud_time=sue_x4_bud_time,
        quota=sue_x4_quota,
        allow_prev_to_offi_time_max_entry=True,
    )

    # THEN
    assert amy_moment.beliefbudhistorys != {}
    assert amy_moment.get_beliefbudhistory(sue_str) == sue_beliefbudhistory
    bob_beliefbudhistory = beliefbudhistory_shop(bob_str)
    bob_beliefbudhistory.add_bud(bob_x0_bud_time, bob_x0_quota)
    assert amy_moment.get_beliefbudhistory(bob_str) == bob_beliefbudhistory


def test_MomentUnit_add_budunit_SetsAttr_celldepth():
    # ESTABLISH
    amy45_str = "amy45"
    amy_moment = momentunit_shop(amy45_str, get_chapter_temp_dir())
    sue_str = "Sue"
    sue_x4_bud_time = 4
    sue_x4_quota = 55
    sue_x7_bud_time = 7
    sue_x7_quota = 66
    sue_x7_celldepth = 5
    assert amy_moment.beliefbudhistorys == {}

    # WHEN
    amy_moment.add_budunit(sue_str, sue_x4_bud_time, sue_x4_quota)
    amy_moment.add_budunit(
        sue_str, sue_x7_bud_time, sue_x7_quota, celldepth=sue_x7_celldepth
    )

    # THEN
    assert amy_moment.beliefbudhistorys != {}
    expected_sue_beliefbudhistory = beliefbudhistory_shop(sue_str)
    expected_sue_beliefbudhistory.add_bud(sue_x4_bud_time, sue_x4_quota)
    expected_sue_beliefbudhistory.add_bud(
        sue_x7_bud_time, sue_x7_quota, celldepth=sue_x7_celldepth
    )
    # print(f"{expected_sue_beliefbudhistory=}")
    gen_sue_beliefbudhistory = amy_moment.get_beliefbudhistory(sue_str)
    gen_sue_x7_bud = gen_sue_beliefbudhistory.get_bud(sue_x7_bud_time)
    print(f"{gen_sue_beliefbudhistory=}")
    assert gen_sue_x7_bud == expected_sue_beliefbudhistory.get_bud(sue_x7_bud_time)
    assert gen_sue_beliefbudhistory.buds == expected_sue_beliefbudhistory.buds
    assert gen_sue_beliefbudhistory == expected_sue_beliefbudhistory
    assert amy_moment.get_beliefbudhistory(sue_str) == expected_sue_beliefbudhistory
