from src._world.beliefunit import beliefunit_shop
from src._world.char import charlink_shop


def test_BeliefUnit_set_charlink_CorrectlySetsAttr():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    yao_charlink = charlink_shop(yao_text, credor_weight=13, debtor_weight=7)
    sue_charlink = charlink_shop(sue_text, credor_weight=23, debtor_weight=5)
    swimmers_beliefunit = beliefunit_shop(",swimmers")

    # WHEN
    swimmers_beliefunit.set_charlink(yao_charlink)
    swimmers_beliefunit.set_charlink(sue_charlink)

    # THEN
    swimmers_chars = {
        yao_charlink.char_id: yao_charlink,
        sue_charlink.char_id: sue_charlink,
    }
    assert swimmers_beliefunit._chars == swimmers_chars


def test_BeliefUnit_get_charlink_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    swimmers_beliefunit = beliefunit_shop(",swimmers")
    swimmers_beliefunit.set_charlink(charlink_shop(yao_text, 13, 7))
    swimmers_beliefunit.set_charlink(charlink_shop(sue_text, 23, 5))

    # WHEN / THEN
    assert swimmers_beliefunit.get_charlink(yao_text) != None
    assert swimmers_beliefunit.get_charlink(sue_text) != None
    assert swimmers_beliefunit.get_charlink("Bob") is None


def test_BeliefUnit_edit_charlink_CorrectlySetsAttr():
    # GIVEN
    yao_text = "Yao"
    old_yao_credor_weight = 13
    yao_debtor_weight = 7
    swimmers_beliefunit = beliefunit_shop(",swimmers")
    swimmers_beliefunit.set_charlink(
        charlink_shop(yao_text, old_yao_credor_weight, yao_debtor_weight)
    )
    yao_charlink = swimmers_beliefunit.get_charlink(yao_text)
    assert yao_charlink.credor_weight == old_yao_credor_weight

    # WHEN
    new_yao_credor_weight = 17
    swimmers_beliefunit.edit_charlink(yao_text, credor_weight=new_yao_credor_weight)

    # THEN
    assert yao_charlink.credor_weight == new_yao_credor_weight


def test_charlink_exists_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    swimmers_beliefunit = beliefunit_shop(",swimmers")
    swimmers_beliefunit.set_charlink(charlink_shop(yao_text, 13, 7))
    swimmers_beliefunit.set_charlink(charlink_shop(sue_text, 23, 5))

    # WHEN / THEN
    assert swimmers_beliefunit.charlink_exists(yao_text)
    assert swimmers_beliefunit.charlink_exists(sue_text)
    assert swimmers_beliefunit.charlink_exists("yao") is False


def test_BeliefUnit_del_charlink_SetsAttrCorrectly():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    yao_charlink = charlink_shop(yao_text)
    sue_charlink = charlink_shop(sue_text)
    swimmers_chars = {
        yao_charlink.char_id: yao_charlink,
        sue_charlink.char_id: sue_charlink,
    }
    swimmers_beliefunit = beliefunit_shop(",swimmers")
    swimmers_beliefunit.set_charlink(yao_charlink)
    swimmers_beliefunit.set_charlink(sue_charlink)
    assert len(swimmers_beliefunit._chars) == 2
    assert swimmers_beliefunit._chars == swimmers_chars

    # WHEN
    swimmers_beliefunit.del_charlink(yao_text)

    # THEN
    assert len(swimmers_beliefunit._chars) == 1
    assert swimmers_beliefunit._chars.get(yao_text) is None


def test_BeliefUnit_clear_charlinks_SetsAttrCorrectly():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    yao_charlink = charlink_shop(yao_text)
    sue_charlink = charlink_shop(sue_text)
    swimmers_chars = {
        yao_charlink.char_id: yao_charlink,
        sue_charlink.char_id: sue_charlink,
    }
    swimmers_beliefunit = beliefunit_shop(",swimmers")
    swimmers_beliefunit.set_charlink(yao_charlink)
    swimmers_beliefunit.set_charlink(sue_charlink)
    assert len(swimmers_beliefunit._chars) == 2
    assert swimmers_beliefunit._chars == swimmers_chars

    # WHEN
    swimmers_beliefunit.clear_charlinks()

    # THEN
    assert len(swimmers_beliefunit._chars) == 0
    assert swimmers_beliefunit._chars.get(yao_text) is None


def test_BeliefUnit_reset_world_share_reset_charlinks():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    yao_charlink = charlink_shop(
        char_id=yao_text,
        _world_cred=0.13,
        _world_debt=0.7,
        _world_agenda_cred=0.53,
        _world_agenda_debt=0.77,
    )
    sue_charlink = charlink_shop(
        char_id=sue_text,
        _world_cred=0.23,
        _world_debt=0.5,
        _world_agenda_cred=0.54,
        _world_agenda_debt=0.57,
    )
    bikers_charlinks = {
        yao_charlink.char_id: yao_charlink,
        sue_charlink.char_id: sue_charlink,
    }
    bikers_belief_id = ",bikers"
    bikers_beliefunit = beliefunit_shop(bikers_belief_id)
    bikers_beliefunit._world_cred = (0.33,)
    bikers_beliefunit._world_debt = (0.44,)
    bikers_beliefunit._world_agenda_cred = (0.1,)
    bikers_beliefunit._world_agenda_debt = (0.2,)
    bikers_beliefunit.set_charlink(yao_charlink)
    bikers_beliefunit.set_charlink(sue_charlink)
    print(f"{bikers_beliefunit}")
    biker_charlink_yao = bikers_beliefunit._chars.get(yao_text)
    assert biker_charlink_yao._world_cred == 0.13
    assert biker_charlink_yao._world_debt == 0.7
    assert biker_charlink_yao._world_agenda_cred == 0.53
    assert biker_charlink_yao._world_agenda_debt == 0.77

    biker_charlink_sue = bikers_beliefunit._chars.get(sue_text)
    assert biker_charlink_sue._world_cred == 0.23
    assert biker_charlink_sue._world_debt == 0.5
    assert biker_charlink_sue._world_agenda_cred == 0.54
    assert biker_charlink_sue._world_agenda_debt == 0.57

    # WHEN
    bikers_beliefunit.reset_world_cred_debt()

    # THEN
    assert biker_charlink_yao._world_cred == 0
    assert biker_charlink_yao._world_debt == 0
    assert biker_charlink_yao._world_agenda_cred == 0
    assert biker_charlink_yao._world_agenda_debt == 0
    assert biker_charlink_sue._world_cred == 0
    assert biker_charlink_sue._world_debt == 0
    assert biker_charlink_sue._world_agenda_cred == 0
    assert biker_charlink_sue._world_agenda_debt == 0


def test_charlink_meld_ReturnsCorrectObj_BaseScenario():
    # GIVEN
    yao_charlink = charlink_shop(char_id="Yao")
    sue_charlink = charlink_shop(char_id="Sue")
    bikers_belief_id = ",bikers"
    bikers_beliefunit = beliefunit_shop(bikers_belief_id)
    bikers_beliefunit.set_charlink(yao_charlink)
    bikers_beliefunit.set_charlink(sue_charlink)

    x2_beliefunit = beliefunit_shop(bikers_belief_id)

    # WHEN
    bikers_beliefunit.meld(exterior_belief=x2_beliefunit)
    print(f"{bikers_beliefunit.belief_id=} {x2_beliefunit.belief_id=}")

    # THEN
    assert len(bikers_beliefunit._chars) == 2


def test_charlink_meld_ReturnsCorrectObj_GainScenario():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    yao_charlink = charlink_shop(yao_text, credor_weight=13, debtor_weight=7)
    sue_charlink = charlink_shop(sue_text, credor_weight=23, debtor_weight=5)
    bikers_belief_id = ",bikers"
    bikers_beliefunit = beliefunit_shop(bikers_belief_id)

    x2_beliefunit = beliefunit_shop(bikers_belief_id)
    x2_beliefunit.set_charlink(yao_charlink)
    x2_beliefunit.set_charlink(sue_charlink)

    # WHEN
    bikers_beliefunit.meld(exterior_belief=x2_beliefunit)

    # THEN
    assert len(bikers_beliefunit._chars) == 2
    assert bikers_beliefunit._chars.get(yao_text) != None
