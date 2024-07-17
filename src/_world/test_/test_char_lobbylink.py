from src._world.lobbylink import lobbylink_shop
from src._world.char import charunit_shop
from pytest import raises as pytest_raises


def test_CharUnit_set_lobbylink_SetsAttr():
    # GIVEN
    run_text = ",run"
    yao_text = "Yao"
    run_credor_weight = 66
    run_debtor_weight = 85
    yao_charunit = charunit_shop(yao_text)
    assert yao_charunit._lobbylinks == {}

    # WHEN
    yao_charunit.set_lobbylink(
        lobbylink_shop(run_text, run_credor_weight, run_debtor_weight)
    )

    # THEN
    assert len(yao_charunit._lobbylinks) == 1
    run_lobbylink = yao_charunit._lobbylinks.get(run_text)
    assert run_lobbylink.lobby_id == run_text
    assert run_lobbylink.credor_weight == run_credor_weight
    assert run_lobbylink.debtor_weight == run_debtor_weight
    assert run_lobbylink._char_id == yao_text


def test_CharUnit_set_lobbylink_SetsMultipleAttr():
    # GIVEN
    run_text = ",run"
    fly_text = ",fly"
    run_lobbylink = lobbylink_shop(run_text, credor_weight=13, debtor_weight=7)
    fly_lobbylink = lobbylink_shop(fly_text, credor_weight=23, debtor_weight=5)
    yao_charunit = charunit_shop("Yao")
    assert yao_charunit._lobbylinks == {}

    # WHEN
    yao_charunit.set_lobbylink(run_lobbylink)
    yao_charunit.set_lobbylink(fly_lobbylink)

    # THEN
    yao_lobbylinks = {
        run_lobbylink.lobby_id: run_lobbylink,
        fly_lobbylink.lobby_id: fly_lobbylink,
    }
    assert yao_charunit._lobbylinks == yao_lobbylinks


def test_CharUnit_set_lobbylink_RaisesErrorIf_lobby_idIsCharIDAndNotCharUnit_char_id():
    # GIVEN
    yao_text = "Yao"
    yao_charunit = charunit_shop(yao_text)
    bob_text = "Bob"
    bob_lobbylink = lobbylink_shop(bob_text)

    with pytest_raises(Exception) as excinfo:
        yao_charunit.set_lobbylink(bob_lobbylink)
    assert (
        str(excinfo.value)
        == f"CharUnit with char_id='{yao_text}' cannot have link to '{bob_text}'."
    )


def test_CharUnit_get_lobbylink_ReturnsCorrectObj():
    # GIVEN
    run_text = ",run"
    fly_text = ",fly"
    yao_charunit = charunit_shop("Yao")
    yao_charunit.set_lobbylink(lobbylink_shop(run_text, 13, 7))
    yao_charunit.set_lobbylink(lobbylink_shop(fly_text, 23, 5))

    # WHEN / THEN
    assert yao_charunit.get_lobbylink(run_text) != None
    assert yao_charunit.get_lobbylink(fly_text) != None
    climb_text = ",climbers"
    assert yao_charunit.get_lobbylink(climb_text) is None


def test_lobbylink_exists_ReturnsCorrectObj():
    # GIVEN
    run_text = ",run"
    fly_text = ",fly"
    yao_charunit = charunit_shop("Yao")
    yao_charunit.set_lobbylink(lobbylink_shop(run_text, 13, 7))
    yao_charunit.set_lobbylink(lobbylink_shop(fly_text, 23, 5))

    # WHEN / THEN
    assert yao_charunit.lobbylink_exists(run_text)
    assert yao_charunit.lobbylink_exists(fly_text)
    climb_text = ",climbers"
    assert yao_charunit.lobbylink_exists(climb_text) is False


def test_lobbylinks_exist_ReturnsCorrectObj():
    # GIVEN
    run_text = ",run"
    fly_text = ",fly"
    yao_charunit = charunit_shop("Yao")
    assert yao_charunit.lobbylinks_exist() is False

    # WHEN
    yao_charunit.set_lobbylink(lobbylink_shop(run_text))
    # THEN
    assert yao_charunit.lobbylinks_exist()

    # WHEN
    yao_charunit.set_lobbylink(lobbylink_shop(fly_text))
    # THEN
    assert yao_charunit.lobbylinks_exist()

    # WHEN
    yao_charunit.delete_lobbylink(fly_text)
    # THEN
    assert yao_charunit.lobbylinks_exist()

    # WHEN
    yao_charunit.delete_lobbylink(run_text)
    # THEN
    assert yao_charunit.lobbylinks_exist() is False


def test_CharUnit_del_lobbylink_SetsAttrCorrectly():
    # GIVEN
    run_text = ",run"
    fly_text = ",fly"
    run_lobbylink = lobbylink_shop(run_text)
    fly_lobbylink = lobbylink_shop(fly_text)
    yao_lobbylinks = {
        run_lobbylink.lobby_id: run_lobbylink,
        fly_lobbylink.lobby_id: fly_lobbylink,
    }
    yao_charunit = charunit_shop("Yao")
    yao_charunit.set_lobbylink(run_lobbylink)
    yao_charunit.set_lobbylink(fly_lobbylink)
    assert len(yao_charunit._lobbylinks) == 2
    assert yao_charunit._lobbylinks == yao_lobbylinks

    # WHEN
    yao_charunit.delete_lobbylink(run_text)

    # THEN
    assert len(yao_charunit._lobbylinks) == 1
    assert yao_charunit._lobbylinks.get(run_text) is None


def test_CharUnit_clear_lobbylinks_SetsAttrCorrectly():
    # GIVEN
    run_text = ",run"
    fly_text = ",fly"
    run_lobbylink = lobbylink_shop(run_text)
    fly_lobbylink = lobbylink_shop(fly_text)
    yao_lobbylinks = {
        run_lobbylink.lobby_id: run_lobbylink,
        fly_lobbylink.lobby_id: fly_lobbylink,
    }
    yao_charunit = charunit_shop("Yao")
    yao_charunit.set_lobbylink(run_lobbylink)
    yao_charunit.set_lobbylink(fly_lobbylink)
    assert len(yao_charunit._lobbylinks) == 2
    assert yao_charunit._lobbylinks == yao_lobbylinks

    # WHEN
    yao_charunit.clear_lobbylinks()

    # THEN
    assert len(yao_charunit._lobbylinks) == 0
    assert yao_charunit._lobbylinks.get(run_text) is None


def test_CharUnit_add_lobbylink_SetsAttrCorrectly():
    # GIVEN
    run_text = ",run"
    run_credor_weight = ",run"
    run_debtor_weight = ",run"
    yao_charunit = charunit_shop("Yao")
    assert yao_charunit.get_lobbylink(run_text) is None

    # WHEN
    yao_charunit.add_lobbylink(run_text, run_credor_weight, run_debtor_weight)

    # THEN
    assert yao_charunit.get_lobbylink(run_text) != None
    run_lobbylink = yao_charunit.get_lobbylink(run_text)
    assert run_lobbylink.credor_weight == run_credor_weight
    assert run_lobbylink.debtor_weight == run_debtor_weight


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


def test_CharUnit_set_credor_pool_Sets_lobbylinks():
    # GIVEN
    ohio_text = ",Ohio"
    iowa_text = ",Iowa"
    sue_credor_weight = 1
    yao_credor_weight = 4
    bob_charunit = charunit_shop("Bob")
    bob_charunit.add_lobbylink(ohio_text, sue_credor_weight)
    bob_charunit.add_lobbylink(iowa_text, yao_credor_weight)
    assert bob_charunit._credor_pool == 0
    sue_lobbylink = bob_charunit.get_lobbylink(ohio_text)
    yao_lobbylink = bob_charunit.get_lobbylink(iowa_text)
    assert sue_lobbylink._credor_pool == 0
    assert yao_lobbylink._credor_pool == 0

    # WHEN
    bob_credor_pool = 51
    bob_charunit.set_credor_pool(bob_credor_pool)

    # THEN
    assert bob_charunit._credor_pool == bob_credor_pool
    assert sue_lobbylink._credor_pool == 10
    assert yao_lobbylink._credor_pool == 41


def test_CharUnit_set_debtor_pool_Sets_lobbylinks():
    # GIVEN
    ohio_text = ",Ohio"
    iowa_text = ",Iowa"
    sue_debtor_weight = 1
    yao_debtor_weight = 4
    bob_charunit = charunit_shop("Bob")
    bob_charunit.add_lobbylink(ohio_text, 2, sue_debtor_weight)
    bob_charunit.add_lobbylink(iowa_text, 2, yao_debtor_weight)
    assert bob_charunit._debtor_pool == 0
    sue_lobbylink = bob_charunit.get_lobbylink(ohio_text)
    yao_lobbylink = bob_charunit.get_lobbylink(iowa_text)
    assert sue_lobbylink._debtor_pool == 0
    assert yao_lobbylink._debtor_pool == 0

    # WHEN
    bob_debtor_pool = 54
    bob_charunit.set_debtor_pool(bob_debtor_pool)

    # THEN
    assert bob_charunit._debtor_pool == bob_debtor_pool
    assert sue_lobbylink._debtor_pool == 11
    assert yao_lobbylink._debtor_pool == 43
