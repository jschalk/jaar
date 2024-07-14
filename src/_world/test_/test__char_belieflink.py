from src._world.belieflink import belieflink_shop
from src._world.char import charunit_shop


def test_CharUnit_set_belieflink_CorrectlySetsAttr():
    # GIVEN
    run_text = ",run"
    fly_text = ",fly"
    run_belieflink = belieflink_shop(run_text, credor_weight=13, debtor_weight=7)
    fly_belieflink = belieflink_shop(fly_text, credor_weight=23, debtor_weight=5)
    yao_charunit = charunit_shop("Yao")
    assert yao_charunit._belieflinks == {}

    # WHEN
    yao_charunit.set_belieflink(run_belieflink)
    yao_charunit.set_belieflink(fly_belieflink)

    # THEN
    yao_belieflinks = {
        run_belieflink.belief_id: run_belieflink,
        fly_belieflink.belief_id: fly_belieflink,
    }
    assert yao_charunit._belieflinks == yao_belieflinks


def test_CharUnit_get_belieflink_ReturnsCorrectObj():
    # GIVEN
    run_text = ",run"
    fly_text = ",fly"
    yao_charunit = charunit_shop("Yao")
    yao_charunit.set_belieflink(belieflink_shop(run_text, 13, 7))
    yao_charunit.set_belieflink(belieflink_shop(fly_text, 23, 5))

    # WHEN / THEN
    assert yao_charunit.get_belieflink(run_text) != None
    assert yao_charunit.get_belieflink(fly_text) != None
    climb_text = ",climbers"
    assert yao_charunit.get_belieflink(climb_text) is None


def test_belieflink_exists_ReturnsCorrectObj():
    # GIVEN
    run_text = ",run"
    fly_text = ",fly"
    yao_charunit = charunit_shop("Yao")
    yao_charunit.set_belieflink(belieflink_shop(run_text, 13, 7))
    yao_charunit.set_belieflink(belieflink_shop(fly_text, 23, 5))

    # WHEN / THEN
    assert yao_charunit.belieflink_exists(run_text)
    assert yao_charunit.belieflink_exists(fly_text)
    climb_text = ",climbers"
    assert yao_charunit.belieflink_exists(climb_text) is False


def test_CharUnit_del_belieflink_SetsAttrCorrectly():
    # GIVEN
    run_text = ",run"
    fly_text = ",fly"
    run_belieflink = belieflink_shop(run_text)
    fly_belieflink = belieflink_shop(fly_text)
    yao_belieflinks = {
        run_belieflink.belief_id: run_belieflink,
        fly_belieflink.belief_id: fly_belieflink,
    }
    yao_charunit = charunit_shop("Yao")
    yao_charunit.set_belieflink(run_belieflink)
    yao_charunit.set_belieflink(fly_belieflink)
    assert len(yao_charunit._belieflinks) == 2
    assert yao_charunit._belieflinks == yao_belieflinks

    # WHEN
    yao_charunit.delete_belieflink(run_text)

    # THEN
    assert len(yao_charunit._belieflinks) == 1
    assert yao_charunit._belieflinks.get(run_text) is None


def test_CharUnit_clear_belieflinks_SetsAttrCorrectly():
    # GIVEN
    run_text = ",run"
    fly_text = ",fly"
    run_belieflink = belieflink_shop(run_text)
    fly_belieflink = belieflink_shop(fly_text)
    yao_belieflinks = {
        run_belieflink.belief_id: run_belieflink,
        fly_belieflink.belief_id: fly_belieflink,
    }
    yao_charunit = charunit_shop("Yao")
    yao_charunit.set_belieflink(run_belieflink)
    yao_charunit.set_belieflink(fly_belieflink)
    assert len(yao_charunit._belieflinks) == 2
    assert yao_charunit._belieflinks == yao_belieflinks

    # WHEN
    yao_charunit.clear_belieflinks()

    # THEN
    assert len(yao_charunit._belieflinks) == 0
    assert yao_charunit._belieflinks.get(run_text) is None
