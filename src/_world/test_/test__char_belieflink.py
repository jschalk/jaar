from src._world.belieflink import BeliefID, BeliefLink, belieflink_shop
from src._world.char import (
    charunit_shop,
)
from pytest import raises as pytest_raises


def test_CharUnit_set_belieflink_CorrectlySetsAttr():
    # GIVEN
    run_text = ",run"
    fly_text = ",fly"
    run_belieflink = belieflink_shop(run_text, credor_weight=13, debtor_weight=7)
    fly_belieflink = belieflink_shop(fly_text, credor_weight=23, debtor_weight=5)
    yao_char = charunit_shop("Yao")
    assert yao_char._belieflinks == {}

    # WHEN
    yao_char.set_belieflink(run_belieflink)
    yao_char.set_belieflink(fly_belieflink)

    # THEN
    yao_belieflinks = {
        run_belieflink.belief_id: run_belieflink,
        fly_belieflink.belief_id: fly_belieflink,
    }
    assert yao_char._belieflinks == yao_belieflinks


def test_CharUnit_get_belieflink_ReturnsCorrectObj():
    # GIVEN
    run_text = ",run"
    fly_text = ",fly"
    yao_char = charunit_shop("Yao")
    yao_char.set_belieflink(belieflink_shop(run_text, 13, 7))
    yao_char.set_belieflink(belieflink_shop(fly_text, 23, 5))

    # WHEN / THEN
    assert yao_char.get_belieflink(run_text) != None
    assert yao_char.get_belieflink(fly_text) != None
    climb_text = ",climbers"
    assert yao_char.get_belieflink(climb_text) is None


def test_belieflink_exists_ReturnsCorrectObj():
    # GIVEN
    run_text = ",run"
    fly_text = ",fly"
    yao_char = charunit_shop("Yao")
    yao_char.set_belieflink(belieflink_shop(run_text, 13, 7))
    yao_char.set_belieflink(belieflink_shop(fly_text, 23, 5))

    # WHEN / THEN
    assert yao_char.belieflink_exists(run_text)
    assert yao_char.belieflink_exists(fly_text)
    climb_text = ",climbers"
    assert yao_char.belieflink_exists(climb_text) is False


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
    yao_char = charunit_shop("Yao")
    yao_char.set_belieflink(run_belieflink)
    yao_char.set_belieflink(fly_belieflink)
    assert len(yao_char._belieflinks) == 2
    assert yao_char._belieflinks == yao_belieflinks

    # WHEN
    yao_char.delete_belieflink(run_text)

    # THEN
    assert len(yao_char._belieflinks) == 1
    assert yao_char._belieflinks.get(run_text) is None


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
    yao_char = charunit_shop("Yao")
    yao_char.set_belieflink(run_belieflink)
    yao_char.set_belieflink(fly_belieflink)
    assert len(yao_char._belieflinks) == 2
    assert yao_char._belieflinks == yao_belieflinks

    # WHEN
    yao_char.clear_belieflinks()

    # THEN
    assert len(yao_char._belieflinks) == 0
    assert yao_char._belieflinks.get(run_text) is None
