from src._world.lobby import (
    LobbyCore,
    LobbyID,
    lobbylink_shop,
    LobbyLink,
    lobbylink_get_from_dict,
    lobbylinks_get_from_dict,
)
from pytest import raises as pytest_raises


def test_LobbyID_exists():
    ohio_lobby_id = LobbyID(",ohio")
    assert ohio_lobby_id != None


def test_LobbyCore_exists():
    # GIVEN
    swim_text = ",swimmers"
    # WHEN
    swim_lobbycore = LobbyCore(lobby_id=swim_text)
    # THEN
    assert swim_lobbycore != None
    assert swim_lobbycore.lobby_id == swim_text


def test_LobbyLink_exists():
    # GIVEN
    swim_text = ",swim"

    # WHEN
    swim_lobbylink = LobbyLink(lobby_id=swim_text)

    # THEN
    assert swim_lobbylink.lobby_id == swim_text
    assert swim_lobbylink.credor_weight == 1.0
    assert swim_lobbylink.debtor_weight == 1.0
    assert swim_lobbylink._credor_pool is None
    assert swim_lobbylink._debtor_pool is None
    assert swim_lobbylink._world_cred is None
    assert swim_lobbylink._world_debt is None
    assert swim_lobbylink._world_agenda_cred is None
    assert swim_lobbylink._world_agenda_debt is None
    assert swim_lobbylink._world_agenda_ratio_cred is None
    assert swim_lobbylink._world_agenda_ratio_debt is None
    assert swim_lobbylink._char_id is None


def test_lobbylink_shop_ReturnsCorrectObj():
    # GIVEN
    swim_text = ",swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0

    # WHEN
    swim_lobbylink = lobbylink_shop(
        lobby_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
    )

    # THEN
    assert swim_lobbylink.credor_weight == swim_credor_weight
    assert swim_lobbylink.debtor_weight == swim_debtor_weight
    assert swim_lobbylink._credor_pool == 0
    assert swim_lobbylink._debtor_pool == 0
    assert swim_lobbylink._world_cred is None
    assert swim_lobbylink._world_debt is None
    assert swim_lobbylink._world_agenda_cred is None
    assert swim_lobbylink._world_agenda_debt is None
    assert swim_lobbylink._world_agenda_ratio_cred is None
    assert swim_lobbylink._world_agenda_ratio_debt is None
    assert swim_lobbylink._char_id is None


def test_lobbylink_shop_ReturnsCorrectObjAttr_char_id():
    # GIVEN
    swim_text = ",swim"
    yao_text = "Yao"

    # WHEN
    swim_lobbylink = lobbylink_shop(swim_text, _char_id=yao_text)

    # THEN
    assert swim_lobbylink._char_id == yao_text


# def test_LobbyLink_set_lobby_id_RaisesErrorIf_lobby_id_IsNotCharIDAndIsRoadNode():
#     # GIVEN
#     slash_text = "/"
#     # bob_text = f"Bob{slash_text}Texas"
#     bob_text = "Bob"
#     # swim_text = f"{slash_text}swim"
#     swim_text = ",swim"

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         lobbylink_shop(swim_text, _char_id=bob_text, _road_delimiter=slash_text)
#     assert (
#         str(excinfo.value)
#         == f"'{swim_text}' needs to not be a RoadNode. Must contain delimiter: '{slash_text}'"
#     )


def test_LobbyLink_set_credor_weight_SetsAttr():
    # GIVEN
    swim_text = ",swim"
    old_credor_weight = 3.0
    swim_debtor_weight = 5.0
    swim_lobbylink = lobbylink_shop(swim_text, old_credor_weight, swim_debtor_weight)
    assert swim_lobbylink.credor_weight == old_credor_weight
    assert swim_lobbylink.debtor_weight == swim_debtor_weight

    # WHEN
    new_swim_credor_weight = 44
    swim_lobbylink.set_credor_weight(new_swim_credor_weight)

    # THEN
    assert swim_lobbylink.credor_weight == new_swim_credor_weight
    assert swim_lobbylink.debtor_weight == swim_debtor_weight


def test_LobbyLink_set_credor_weight_SetsAttr():
    # GIVEN
    swim_text = ",swim"
    old_credor_weight = 3.0
    swim_debtor_weight = 5.0
    swim_lobbylink = lobbylink_shop(swim_text, old_credor_weight, swim_debtor_weight)
    assert swim_lobbylink.credor_weight == old_credor_weight
    assert swim_lobbylink.debtor_weight == swim_debtor_weight

    # WHEN
    swim_lobbylink.set_credor_weight(None)

    # THEN
    assert swim_lobbylink.credor_weight == old_credor_weight
    assert swim_lobbylink.debtor_weight == swim_debtor_weight


def test_LobbyLink_set_debtor_weight_SetsAttr():
    # GIVEN
    swim_text = ",swim"
    swim_credor_weight = 3.0
    old_debtor_weight = 5.0
    swim_lobbylink = lobbylink_shop(swim_text, swim_credor_weight, old_debtor_weight)
    assert swim_lobbylink.credor_weight == swim_credor_weight
    assert swim_lobbylink.debtor_weight == old_debtor_weight

    # WHEN
    new_debtor_weight = 55
    swim_lobbylink.set_debtor_weight(new_debtor_weight)

    # THEN
    assert swim_lobbylink.credor_weight == swim_credor_weight
    assert swim_lobbylink.debtor_weight == new_debtor_weight


def test_LobbyLink_set_debtor_weight_SetsAttr():
    # GIVEN
    swim_text = ",swim"
    swim_credor_weight = 3.0
    old_debtor_weight = 5.0
    swim_lobbylink = lobbylink_shop(swim_text, swim_credor_weight, old_debtor_weight)
    assert swim_lobbylink.credor_weight == swim_credor_weight
    assert swim_lobbylink.debtor_weight == old_debtor_weight

    # WHEN
    swim_lobbylink.set_debtor_weight(None)

    # THEN
    assert swim_lobbylink.credor_weight == swim_credor_weight
    assert swim_lobbylink.debtor_weight == old_debtor_weight


def test_LobbyLink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    swim_text = ",swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0
    swim_lobbylink = lobbylink_shop(
        lobby_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
    )

    print(f"{swim_lobbylink}")

    # WHEN
    swim_dict = swim_lobbylink.get_dict()

    # THEN
    assert swim_dict != None
    assert swim_dict == {
        "lobby_id": swim_lobbylink.lobby_id,
        "credor_weight": swim_lobbylink.credor_weight,
        "debtor_weight": swim_lobbylink.debtor_weight,
    }


def test_lobbylink_get_from_dict_ReturnsObj():
    # GIVEN
    swim_text = ",swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0
    yao_text = "Yao"
    before_swim_lobbylink = lobbylink_shop(
        lobby_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
        _char_id=yao_text,
    )
    swim_lobbylink_dict = before_swim_lobbylink.get_dict()

    # WHEN
    after_swim_lobbylink = lobbylink_get_from_dict(swim_lobbylink_dict, yao_text)

    # THEN
    assert before_swim_lobbylink == after_swim_lobbylink
    assert after_swim_lobbylink.lobby_id == swim_text


def test_lobbylinks_get_from_dict_ReturnsObj():
    # GIVEN
    swim_text = ",swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0
    yao_text = "Yao"
    before_swim_lobbylink = lobbylink_shop(
        lobby_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
        _char_id=yao_text,
    )
    before_swim_lobbylinks_objs = {swim_text: before_swim_lobbylink}
    swim_lobbylinks_dict = {swim_text: before_swim_lobbylink.get_dict()}

    # WHEN
    after_swim_lobbylinks_objs = lobbylinks_get_from_dict(
        swim_lobbylinks_dict, yao_text
    )

    # THEN
    assert before_swim_lobbylinks_objs == after_swim_lobbylinks_objs
    assert after_swim_lobbylinks_objs.get(swim_text) == before_swim_lobbylink


def test_LobbyLink_reset_world_cred_debt_SetsAttrCorrectly():
    # GIVEN
    bob_lobbylink = lobbylink_shop("Bob")
    bob_lobbylink._world_cred = 0.27
    bob_lobbylink._world_debt = 0.37
    bob_lobbylink._world_agenda_cred = 0.41
    bob_lobbylink._world_agenda_debt = 0.51
    bob_lobbylink._world_agenda_ratio_cred = 0.433
    bob_lobbylink._world_agenda_ratio_debt = 0.533
    assert bob_lobbylink._world_cred == 0.27
    assert bob_lobbylink._world_debt == 0.37
    assert bob_lobbylink._world_agenda_cred == 0.41
    assert bob_lobbylink._world_agenda_debt == 0.51
    assert bob_lobbylink._world_agenda_ratio_cred == 0.433
    assert bob_lobbylink._world_agenda_ratio_debt == 0.533

    # WHEN
    bob_lobbylink.reset_world_cred_debt()

    # THEN
    assert bob_lobbylink._world_cred == 0
    assert bob_lobbylink._world_debt == 0
    assert bob_lobbylink._world_agenda_cred == 0
    assert bob_lobbylink._world_agenda_debt == 0
    assert bob_lobbylink._world_agenda_ratio_cred == 0
    assert bob_lobbylink._world_agenda_ratio_debt == 0


def test_LobbyLink_set_world_cred_debt_SetsAttrCorrectly():
    # GIVEN
    yao_text = "Yao"
    ohio_text = ",Ohio"
    ohio_credor_weight = 3.0
    lobbylinks_sum_credor_weight = 60
    lobby_world_cred = 0.5
    lobby_world_agenda_cred = 0.98

    ohio_debtor_weight = 13.0
    lobbylinks_sum_debtor_weight = 26.0
    lobby_world_debt = 0.9
    lobby_world_agenda_debt = 0.5151

    ohio_yao_lobbylink = lobbylink_shop(
        ohio_text, ohio_credor_weight, ohio_debtor_weight
    )
    assert ohio_yao_lobbylink._world_cred is None
    assert ohio_yao_lobbylink._world_debt is None
    assert ohio_yao_lobbylink._world_agenda_cred is None
    assert ohio_yao_lobbylink._world_agenda_debt is None

    # WHEN
    ohio_yao_lobbylink.set_world_cred_debt(
        lobbylinks_credor_weight_sum=lobbylinks_sum_credor_weight,
        lobbylinks_debtor_weight_sum=lobbylinks_sum_debtor_weight,
        lobby_world_cred=lobby_world_cred,
        lobby_world_debt=lobby_world_debt,
        lobby_world_agenda_cred=lobby_world_agenda_cred,
        lobby_world_agenda_debt=lobby_world_agenda_debt,
    )

    # THEN
    assert ohio_yao_lobbylink._world_cred == 0.025
    assert ohio_yao_lobbylink._world_debt == 0.45
    assert ohio_yao_lobbylink._world_agenda_cred == 0.049
    assert ohio_yao_lobbylink._world_agenda_debt == 0.25755
