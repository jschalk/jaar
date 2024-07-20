from src.bud.lobby import lobbyship_shop
from src.bud.lobby import lobbybox_shop
from pytest import raises as pytest_raises


def test_LobbyBox_set_lobbyship_CorrectlySetsAttr():
    # ESTABLISH
    yao_text = "Yao"
    sue_text = "Sue"
    swim_text = ",swimmers"
    yao_swim_lobbyship = lobbyship_shop(swim_text)
    sue_swim_lobbyship = lobbyship_shop(swim_text)
    yao_swim_lobbyship._acct_id = yao_text
    sue_swim_lobbyship._acct_id = sue_text
    swimmers_lobbybox = lobbybox_shop(swim_text)

    # WHEN
    swimmers_lobbybox.set_lobbyship(yao_swim_lobbyship)
    swimmers_lobbybox.set_lobbyship(sue_swim_lobbyship)

    # THEN
    swimmers_lobbyships = {
        yao_swim_lobbyship._acct_id: yao_swim_lobbyship,
        sue_swim_lobbyship._acct_id: sue_swim_lobbyship,
    }
    assert swimmers_lobbybox._lobbyships == swimmers_lobbyships


def test_LobbyBox_set_lobbyship_SetsAttr_credor_pool_debtor_pool():
    # ESTABLISH
    yao_text = "Yao"
    sue_text = "Sue"
    ohio_text = ",Ohio"
    yao_ohio_lobbyship = lobbyship_shop(ohio_text)
    sue_ohio_lobbyship = lobbyship_shop(ohio_text)
    yao_ohio_lobbyship._acct_id = yao_text
    yao_ohio_lobbyship._acct_id = yao_text
    sue_ohio_lobbyship._acct_id = sue_text
    yao_ohio_lobbyship._credor_pool = 66
    sue_ohio_lobbyship._credor_pool = 22
    yao_ohio_lobbyship._debtor_pool = 6600
    sue_ohio_lobbyship._debtor_pool = 2200
    ohio_lobbybox = lobbybox_shop(ohio_text)
    assert ohio_lobbybox._credor_pool == 0
    assert ohio_lobbybox._debtor_pool == 0

    # WHEN
    ohio_lobbybox.set_lobbyship(yao_ohio_lobbyship)
    # THEN
    assert ohio_lobbybox._credor_pool == 66
    assert ohio_lobbybox._debtor_pool == 6600

    # WHEN
    ohio_lobbybox.set_lobbyship(sue_ohio_lobbyship)
    # THEN
    assert ohio_lobbybox._credor_pool == 88
    assert ohio_lobbybox._debtor_pool == 8800


def test_LobbyBox_set_lobbyship_RaisesErrorIf_lobbyship_lobby_id_IsWrong():
    # ESTABLISH
    yao_text = "Yao"
    ohio_text = ",Ohio"
    iowa_text = ",Iowa"
    yao_ohio_lobbyship = lobbyship_shop(ohio_text)
    yao_ohio_lobbyship._acct_id = yao_text
    yao_ohio_lobbyship._acct_id = yao_text
    yao_ohio_lobbyship._credor_pool = 66
    yao_ohio_lobbyship._debtor_pool = 6600
    iowa_lobbybox = lobbybox_shop(iowa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        iowa_lobbybox.set_lobbyship(yao_ohio_lobbyship)
    assert (
        str(excinfo.value)
        == f"LobbyBox.lobby_id={iowa_text} cannot set lobbyship.lobby_id={ohio_text}"
    )


def test_LobbyBox_set_lobbyship_RaisesErrorIf_acct_id_IsNone():
    # ESTABLISH
    ohio_text = ",Ohio"
    ohio_lobbybox = lobbybox_shop(ohio_text)
    yao_ohio_lobbyship = lobbyship_shop(ohio_text)
    assert yao_ohio_lobbyship._acct_id is None

    with pytest_raises(Exception) as excinfo:
        ohio_lobbybox.set_lobbyship(yao_ohio_lobbyship)
    assert (
        str(excinfo.value)
        == f"lobbyship lobby_id={ohio_text} cannot be set when _acct_id is None."
    )
