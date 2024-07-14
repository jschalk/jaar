from src._world.beliefbox import beliefbox_shop
from src._world.char import charlink_shop


def test_BeliefBox_set_charlink_CorrectlySetsAttr():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    yao_charlink = charlink_shop(yao_text, credor_weight=13, debtor_weight=7)
    sue_charlink = charlink_shop(sue_text, credor_weight=23, debtor_weight=5)
    swimmers_beliefbox = beliefbox_shop(",swimmers")

    # WHEN
    swimmers_beliefbox.set_charlink(yao_charlink)
    swimmers_beliefbox.set_charlink(sue_charlink)

    # THEN
    swimmers_chars = {
        yao_charlink.char_id: yao_charlink,
        sue_charlink.char_id: sue_charlink,
    }
    assert swimmers_beliefbox._chars == swimmers_chars


def test_BeliefBox_get_charlink_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    swimmers_beliefbox = beliefbox_shop(",swimmers")
    swimmers_beliefbox.set_charlink(charlink_shop(yao_text, 13, 7))
    swimmers_beliefbox.set_charlink(charlink_shop(sue_text, 23, 5))

    # WHEN / THEN
    assert swimmers_beliefbox.get_charlink(yao_text) != None
    assert swimmers_beliefbox.get_charlink(sue_text) != None
    assert swimmers_beliefbox.get_charlink("Bob") is None


def test_BeliefBox_edit_charlink_CorrectlySetsAttr():
    # GIVEN
    yao_text = "Yao"
    old_yao_credor_weight = 13
    yao_debtor_weight = 7
    swimmers_beliefbox = beliefbox_shop(",swimmers")
    swimmers_beliefbox.set_charlink(
        charlink_shop(yao_text, old_yao_credor_weight, yao_debtor_weight)
    )
    yao_charlink = swimmers_beliefbox.get_charlink(yao_text)
    assert yao_charlink.credor_weight == old_yao_credor_weight

    # WHEN
    new_yao_credor_weight = 17
    swimmers_beliefbox.edit_charlink(yao_text, credor_weight=new_yao_credor_weight)

    # THEN
    assert yao_charlink.credor_weight == new_yao_credor_weight


def test_charlink_exists_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    swimmers_beliefbox = beliefbox_shop(",swimmers")
    swimmers_beliefbox.set_charlink(charlink_shop(yao_text, 13, 7))
    swimmers_beliefbox.set_charlink(charlink_shop(sue_text, 23, 5))

    # WHEN / THEN
    assert swimmers_beliefbox.charlink_exists(yao_text)
    assert swimmers_beliefbox.charlink_exists(sue_text)
    assert swimmers_beliefbox.charlink_exists("yao") is False


def test_BeliefBox_del_charlink_SetsAttrCorrectly():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    yao_charlink = charlink_shop(yao_text)
    sue_charlink = charlink_shop(sue_text)
    swimmers_chars = {
        yao_charlink.char_id: yao_charlink,
        sue_charlink.char_id: sue_charlink,
    }
    swimmers_beliefbox = beliefbox_shop(",swimmers")
    swimmers_beliefbox.set_charlink(yao_charlink)
    swimmers_beliefbox.set_charlink(sue_charlink)
    assert len(swimmers_beliefbox._chars) == 2
    assert swimmers_beliefbox._chars == swimmers_chars

    # WHEN
    swimmers_beliefbox.del_charlink(yao_text)

    # THEN
    assert len(swimmers_beliefbox._chars) == 1
    assert swimmers_beliefbox._chars.get(yao_text) is None


def test_BeliefBox_clear_charlinks_SetsAttrCorrectly():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    yao_charlink = charlink_shop(yao_text)
    sue_charlink = charlink_shop(sue_text)
    swimmers_chars = {
        yao_charlink.char_id: yao_charlink,
        sue_charlink.char_id: sue_charlink,
    }
    swimmers_beliefbox = beliefbox_shop(",swimmers")
    swimmers_beliefbox.set_charlink(yao_charlink)
    swimmers_beliefbox.set_charlink(sue_charlink)
    assert len(swimmers_beliefbox._chars) == 2
    assert swimmers_beliefbox._chars == swimmers_chars

    # WHEN
    swimmers_beliefbox.clear_charlinks()

    # THEN
    assert len(swimmers_beliefbox._chars) == 0
    assert swimmers_beliefbox._chars.get(yao_text) is None


def test_BeliefBox_reset_bud_share_reset_charlinks():
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
    bikers_beliefbox = beliefbox_shop(bikers_belief_id)
    bikers_beliefbox._world_cred = (0.33,)
    bikers_beliefbox._world_debt = (0.44,)
    bikers_beliefbox._world_agenda_cred = (0.1,)
    bikers_beliefbox._world_agenda_debt = (0.2,)
    bikers_beliefbox.set_charlink(yao_charlink)
    bikers_beliefbox.set_charlink(sue_charlink)
    print(f"{bikers_beliefbox}")
    biker_charlink_yao = bikers_beliefbox._chars.get(yao_text)
    assert biker_charlink_yao._world_cred == 0.13
    assert biker_charlink_yao._world_debt == 0.7
    assert biker_charlink_yao._world_agenda_cred == 0.53
    assert biker_charlink_yao._world_agenda_debt == 0.77

    biker_charlink_sue = bikers_beliefbox._chars.get(sue_text)
    assert biker_charlink_sue._world_cred == 0.23
    assert biker_charlink_sue._world_debt == 0.5
    assert biker_charlink_sue._world_agenda_cred == 0.54
    assert biker_charlink_sue._world_agenda_debt == 0.57

    # WHEN
    bikers_beliefbox.reset_world_cred_debt()

    # THEN
    assert biker_charlink_yao._world_cred == 0
    assert biker_charlink_yao._world_debt == 0
    assert biker_charlink_yao._world_agenda_cred == 0
    assert biker_charlink_yao._world_agenda_debt == 0
    assert biker_charlink_sue._world_cred == 0
    assert biker_charlink_sue._world_debt == 0
    assert biker_charlink_sue._world_agenda_cred == 0
    assert biker_charlink_sue._world_agenda_debt == 0
