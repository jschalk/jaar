from src._world.lobby import lobbylink_shop
from src._world.lobby import lobbybox_shop
from pytest import raises as pytest_raises


def test_LobbyBox_set_lobbylink_CorrectlySetsAttr():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    swim_text = ",swimmers"
    yao_swim_lobbylink = lobbylink_shop(swim_text)
    sue_swim_lobbylink = lobbylink_shop(swim_text)
    yao_swim_lobbylink._char_id = yao_text
    sue_swim_lobbylink._char_id = sue_text
    swimmers_lobbybox = lobbybox_shop(swim_text)

    # WHEN
    swimmers_lobbybox.set_lobbylink(yao_swim_lobbylink)
    swimmers_lobbybox.set_lobbylink(sue_swim_lobbylink)

    # THEN
    swimmers_lobbylinks = {
        yao_swim_lobbylink._char_id: yao_swim_lobbylink,
        sue_swim_lobbylink._char_id: sue_swim_lobbylink,
    }
    assert swimmers_lobbybox._lobbylinks == swimmers_lobbylinks


def test_LobbyBox_set_lobbylink_SetsAttr_credor_pool_debtor_pool():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    ohio_text = ",Ohio"
    yao_ohio_lobbylink = lobbylink_shop(ohio_text)
    sue_ohio_lobbylink = lobbylink_shop(ohio_text)
    yao_ohio_lobbylink._char_id = yao_text
    yao_ohio_lobbylink._char_id = yao_text
    sue_ohio_lobbylink._char_id = sue_text
    yao_ohio_lobbylink._credor_pool = 66
    sue_ohio_lobbylink._credor_pool = 22
    yao_ohio_lobbylink._debtor_pool = 6600
    sue_ohio_lobbylink._debtor_pool = 2200
    ohio_lobbybox = lobbybox_shop(ohio_text)
    assert ohio_lobbybox._credor_pool == 0
    assert ohio_lobbybox._debtor_pool == 0

    # WHEN
    ohio_lobbybox.set_lobbylink(yao_ohio_lobbylink)
    # THEN
    assert ohio_lobbybox._credor_pool == 66
    assert ohio_lobbybox._debtor_pool == 6600

    # WHEN
    ohio_lobbybox.set_lobbylink(sue_ohio_lobbylink)
    # THEN
    assert ohio_lobbybox._credor_pool == 88
    assert ohio_lobbybox._debtor_pool == 8800


def test_LobbyBox_set_lobbylink_RaisesErrorIf_lobbylink_lobby_id_IsWrong():
    # GIVEN
    yao_text = "Yao"
    ohio_text = ",Ohio"
    iowa_text = ",Iowa"
    yao_ohio_lobbylink = lobbylink_shop(ohio_text)
    yao_ohio_lobbylink._char_id = yao_text
    yao_ohio_lobbylink._char_id = yao_text
    yao_ohio_lobbylink._credor_pool = 66
    yao_ohio_lobbylink._debtor_pool = 6600
    iowa_lobbybox = lobbybox_shop(iowa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        iowa_lobbybox.set_lobbylink(yao_ohio_lobbylink)
    assert (
        str(excinfo.value)
        == f"LobbyBox.lobby_id={iowa_text} cannot set lobbylink.lobby_id={ohio_text}"
    )


def test_LobbyBox_set_lobbylink_RaisesErrorIf_char_id_IsNone():
    # GIVEN
    ohio_text = ",Ohio"
    ohio_lobbybox = lobbybox_shop(ohio_text)
    yao_ohio_lobbylink = lobbylink_shop(ohio_text)
    assert yao_ohio_lobbylink._char_id is None

    with pytest_raises(Exception) as excinfo:
        ohio_lobbybox.set_lobbylink(yao_ohio_lobbylink)
    assert (
        str(excinfo.value)
        == f"lobbylink lobby_id={ohio_text} cannot be set when _char_id is None."
    )
