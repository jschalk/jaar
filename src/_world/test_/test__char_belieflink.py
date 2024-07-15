from src._world.belieflink import belieflink_shop
from src._world.char import charunit_shop


def test_CharUnit_set_belieflink_SetsAttr():
    # GIVEN
    run_text = ",run"
    yao_text = "Yao"
    run_credor_weight = 66
    run_debtor_weight = 85
    yao_charunit = charunit_shop(yao_text)
    assert yao_charunit._belieflinks == {}

    # WHEN
    yao_charunit.set_belieflink(
        belieflink_shop(run_text, run_credor_weight, run_debtor_weight)
    )

    # THEN
    assert len(yao_charunit._belieflinks) == 1
    run_belieflink = yao_charunit._belieflinks.get(run_text)
    assert run_belieflink.belief_id == run_text
    assert run_belieflink.credor_weight == run_credor_weight
    assert run_belieflink.debtor_weight == run_debtor_weight
    assert run_belieflink._char_id == yao_text


def test_CharUnit_set_belieflink_SetsMultipleAttr():
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


def test_belieflinks_exist_ReturnsCorrectObj():
    # GIVEN
    run_text = ",run"
    fly_text = ",fly"
    yao_charunit = charunit_shop("Yao")
    assert yao_charunit.belieflinks_exist() is False

    # WHEN
    yao_charunit.set_belieflink(belieflink_shop(run_text))
    # THEN
    assert yao_charunit.belieflinks_exist()

    # WHEN
    yao_charunit.set_belieflink(belieflink_shop(fly_text))
    # THEN
    assert yao_charunit.belieflinks_exist()

    # WHEN
    yao_charunit.delete_belieflink(fly_text)
    # THEN
    assert yao_charunit.belieflinks_exist()

    # WHEN
    yao_charunit.delete_belieflink(run_text)
    # THEN
    assert yao_charunit.belieflinks_exist() is False


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


def test_CharUnit_add_belieflink_SetsAttrCorrectly():
    # GIVEN
    run_text = ",run"
    run_credor_weight = ",run"
    run_debtor_weight = ",run"
    yao_charunit = charunit_shop("Yao")
    assert yao_charunit.get_belieflink(run_text) is None

    # WHEN
    yao_charunit.add_belieflink(run_text, run_credor_weight, run_debtor_weight)

    # THEN
    assert yao_charunit.get_belieflink(run_text) != None
    run_belieflink = yao_charunit.get_belieflink(run_text)
    assert run_belieflink.credor_weight == run_credor_weight
    assert run_belieflink.debtor_weight == run_debtor_weight


def test_CharUnit_set_credor_pool_SetAttr():
    # GIVEN
    bob_charunit = charunit_shop("Bob")
    assert bob_charunit._credor_pool == 0

    # WHEN
    bob_credor_pool = 51
    bob_charunit.set_credor_pool(bob_credor_pool)

    # THEN
    assert bob_charunit._credor_pool == bob_credor_pool


def test_CharUnit_set_debtor_pool_SetAttr():
    # GIVEN
    bob_charunit = charunit_shop("Bob")
    assert bob_charunit._debtor_pool == 0

    # WHEN
    bob_debtor_pool = 51
    bob_charunit.set_debtor_pool(bob_debtor_pool)

    # THEN
    assert bob_charunit._debtor_pool == bob_debtor_pool


def test_CharUnit_set_credor_pool_Sets_belieflinks():
    # GIVEN
    sue_text = "Sue"
    yao_text = "Yao"
    sue_credor_weight = 1
    yao_credor_weight = 4
    bob_charunit = charunit_shop("Bob")
    bob_charunit.add_belieflink(sue_text, sue_credor_weight)
    bob_charunit.add_belieflink(yao_text, yao_credor_weight)
    assert bob_charunit._credor_pool == 0
    sue_belieflink = bob_charunit.get_belieflink(sue_text)
    yao_belieflink = bob_charunit.get_belieflink(yao_text)
    assert sue_belieflink._credor_pool == 0
    assert yao_belieflink._credor_pool == 0

    # WHEN
    bob_credor_pool = 51
    bob_charunit.set_credor_pool(bob_credor_pool)

    # THEN
    assert bob_charunit._credor_pool == bob_credor_pool
    assert sue_belieflink._credor_pool == 10
    assert yao_belieflink._credor_pool == 41


def test_CharUnit_set_debtor_pool_Sets_belieflinks():
    # GIVEN
    sue_text = "Sue"
    yao_text = "Yao"
    sue_debtor_weight = 1
    yao_debtor_weight = 4
    bob_charunit = charunit_shop("Bob")
    bob_charunit.add_belieflink(sue_text, 2, sue_debtor_weight)
    bob_charunit.add_belieflink(yao_text, 2, yao_debtor_weight)
    assert bob_charunit._debtor_pool == 0
    sue_belieflink = bob_charunit.get_belieflink(sue_text)
    yao_belieflink = bob_charunit.get_belieflink(yao_text)
    assert sue_belieflink._debtor_pool == 0
    assert yao_belieflink._debtor_pool == 0

    # WHEN
    bob_debtor_pool = 54
    bob_charunit.set_debtor_pool(bob_debtor_pool)

    # THEN
    assert bob_charunit._debtor_pool == bob_debtor_pool
    assert sue_belieflink._debtor_pool == 11
    assert yao_belieflink._debtor_pool == 43
