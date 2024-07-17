from src._world.lobby import (
    LobbyCore,
    LobbyID,
    lobbyship_shop,
    LobbyShip,
    lobbyship_get_from_dict,
    lobbyships_get_from_dict,
    AwardLine,
    awardline_shop,
    AwardLink,
    awardlink_shop,
    awardlinks_get_from_json,
    awardheir_shop,
    LobbyBox,
    lobbybox_shop,
)
from src._road.road import (
    get_default_real_id_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from src._instrument.python import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_LobbyID_exists():
    ohio_lobby_id = LobbyID(",ohio")
    assert ohio_lobby_id != None


def test_LobbyCore_exists():
    # ESTABLISH
    swim_text = ",swimmers"
    # WHEN
    swim_lobbycore = LobbyCore(lobby_id=swim_text)
    # THEN
    assert swim_lobbycore != None
    assert swim_lobbycore.lobby_id == swim_text


def test_LobbyShip_exists():
    # ESTABLISH
    swim_text = ",swim"

    # WHEN
    swim_lobbyship = LobbyShip(lobby_id=swim_text)

    # THEN
    assert swim_lobbyship.lobby_id == swim_text
    assert swim_lobbyship.credor_weight == 1.0
    assert swim_lobbyship.debtor_weight == 1.0
    assert swim_lobbyship._credor_pool is None
    assert swim_lobbyship._debtor_pool is None
    assert swim_lobbyship._bud_give is None
    assert swim_lobbyship._bud_take is None
    assert swim_lobbyship._bud_agenda_give is None
    assert swim_lobbyship._bud_agenda_take is None
    assert swim_lobbyship._bud_agenda_ratio_give is None
    assert swim_lobbyship._bud_agenda_ratio_take is None
    assert swim_lobbyship._char_id is None


def test_lobbyship_shop_ReturnsCorrectObj():
    # ESTABLISH
    swim_text = ",swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0

    # WHEN
    swim_lobbyship = lobbyship_shop(
        lobby_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
    )

    # THEN
    assert swim_lobbyship.credor_weight == swim_credor_weight
    assert swim_lobbyship.debtor_weight == swim_debtor_weight
    assert swim_lobbyship._credor_pool == 0
    assert swim_lobbyship._debtor_pool == 0
    assert swim_lobbyship._bud_give is None
    assert swim_lobbyship._bud_take is None
    assert swim_lobbyship._bud_agenda_give is None
    assert swim_lobbyship._bud_agenda_take is None
    assert swim_lobbyship._bud_agenda_ratio_give is None
    assert swim_lobbyship._bud_agenda_ratio_take is None
    assert swim_lobbyship._char_id is None


def test_lobbyship_shop_ReturnsCorrectObjAttr_char_id():
    # ESTABLISH
    swim_text = ",swim"
    yao_text = "Yao"

    # WHEN
    swim_lobbyship = lobbyship_shop(swim_text, _char_id=yao_text)

    # THEN
    assert swim_lobbyship._char_id == yao_text


# def test_LobbyShip_set_lobby_id_RaisesErrorIf_lobby_id_IsNotCharIDAndIsRoadNode():
#     # ESTABLISH
#     slash_text = "/"
#     # bob_text = f"Bob{slash_text}Texas"
#     bob_text = "Bob"
#     # swim_text = f"{slash_text}swim"
#     swim_text = ",swim"

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         lobbyship_shop(swim_text, _char_id=bob_text, _road_delimiter=slash_text)
#     assert (
#         str(excinfo.value)
#         == f"'{swim_text}' needs to not be a RoadNode. Must contain delimiter: '{slash_text}'"
#     )


def test_LobbyShip_set_credor_weight_SetsAttr():
    # ESTABLISH
    swim_text = ",swim"
    old_credor_weight = 3.0
    swim_debtor_weight = 5.0
    swim_lobbyship = lobbyship_shop(swim_text, old_credor_weight, swim_debtor_weight)
    assert swim_lobbyship.credor_weight == old_credor_weight
    assert swim_lobbyship.debtor_weight == swim_debtor_weight

    # WHEN
    new_swim_credor_weight = 44
    swim_lobbyship.set_credor_weight(new_swim_credor_weight)

    # THEN
    assert swim_lobbyship.credor_weight == new_swim_credor_weight
    assert swim_lobbyship.debtor_weight == swim_debtor_weight


def test_LobbyShip_set_credor_weight_SetsAttr():
    # ESTABLISH
    swim_text = ",swim"
    old_credor_weight = 3.0
    swim_debtor_weight = 5.0
    swim_lobbyship = lobbyship_shop(swim_text, old_credor_weight, swim_debtor_weight)
    assert swim_lobbyship.credor_weight == old_credor_weight
    assert swim_lobbyship.debtor_weight == swim_debtor_weight

    # WHEN
    swim_lobbyship.set_credor_weight(None)

    # THEN
    assert swim_lobbyship.credor_weight == old_credor_weight
    assert swim_lobbyship.debtor_weight == swim_debtor_weight


def test_LobbyShip_set_debtor_weight_SetsAttr():
    # ESTABLISH
    swim_text = ",swim"
    swim_credor_weight = 3.0
    old_debtor_weight = 5.0
    swim_lobbyship = lobbyship_shop(swim_text, swim_credor_weight, old_debtor_weight)
    assert swim_lobbyship.credor_weight == swim_credor_weight
    assert swim_lobbyship.debtor_weight == old_debtor_weight

    # WHEN
    new_debtor_weight = 55
    swim_lobbyship.set_debtor_weight(new_debtor_weight)

    # THEN
    assert swim_lobbyship.credor_weight == swim_credor_weight
    assert swim_lobbyship.debtor_weight == new_debtor_weight


def test_LobbyShip_set_debtor_weight_SetsAttr():
    # ESTABLISH
    swim_text = ",swim"
    swim_credor_weight = 3.0
    old_debtor_weight = 5.0
    swim_lobbyship = lobbyship_shop(swim_text, swim_credor_weight, old_debtor_weight)
    assert swim_lobbyship.credor_weight == swim_credor_weight
    assert swim_lobbyship.debtor_weight == old_debtor_weight

    # WHEN
    swim_lobbyship.set_debtor_weight(None)

    # THEN
    assert swim_lobbyship.credor_weight == swim_credor_weight
    assert swim_lobbyship.debtor_weight == old_debtor_weight


def test_LobbyShip_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # ESTABLISH
    swim_text = ",swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0
    swim_lobbyship = lobbyship_shop(
        lobby_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
    )

    print(f"{swim_lobbyship}")

    # WHEN
    swim_dict = swim_lobbyship.get_dict()

    # THEN
    assert swim_dict != None
    assert swim_dict == {
        "lobby_id": swim_lobbyship.lobby_id,
        "credor_weight": swim_lobbyship.credor_weight,
        "debtor_weight": swim_lobbyship.debtor_weight,
    }


def test_lobbyship_get_from_dict_ReturnsObj():
    # ESTABLISH
    swim_text = ",swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0
    yao_text = "Yao"
    before_swim_lobbyship = lobbyship_shop(
        lobby_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
        _char_id=yao_text,
    )
    swim_lobbyship_dict = before_swim_lobbyship.get_dict()

    # WHEN
    after_swim_lobbyship = lobbyship_get_from_dict(swim_lobbyship_dict, yao_text)

    # THEN
    assert before_swim_lobbyship == after_swim_lobbyship
    assert after_swim_lobbyship.lobby_id == swim_text


def test_lobbyships_get_from_dict_ReturnsObj():
    # ESTABLISH
    swim_text = ",swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0
    yao_text = "Yao"
    before_swim_lobbyship = lobbyship_shop(
        lobby_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
        _char_id=yao_text,
    )
    before_swim_lobbyships_objs = {swim_text: before_swim_lobbyship}
    swim_lobbyships_dict = {swim_text: before_swim_lobbyship.get_dict()}

    # WHEN
    after_swim_lobbyships_objs = lobbyships_get_from_dict(
        swim_lobbyships_dict, yao_text
    )

    # THEN
    assert before_swim_lobbyships_objs == after_swim_lobbyships_objs
    assert after_swim_lobbyships_objs.get(swim_text) == before_swim_lobbyship


def test_LobbyShip_reset_bud_give_take_SetsAttrCorrectly():
    # ESTABLISH
    bob_lobbyship = lobbyship_shop("Bob")
    bob_lobbyship._bud_give = 0.27
    bob_lobbyship._bud_take = 0.37
    bob_lobbyship._bud_agenda_give = 0.41
    bob_lobbyship._bud_agenda_take = 0.51
    bob_lobbyship._bud_agenda_ratio_give = 0.433
    bob_lobbyship._bud_agenda_ratio_take = 0.533
    assert bob_lobbyship._bud_give == 0.27
    assert bob_lobbyship._bud_take == 0.37
    assert bob_lobbyship._bud_agenda_give == 0.41
    assert bob_lobbyship._bud_agenda_take == 0.51
    assert bob_lobbyship._bud_agenda_ratio_give == 0.433
    assert bob_lobbyship._bud_agenda_ratio_take == 0.533

    # WHEN
    bob_lobbyship.reset_bud_give_take()

    # THEN
    assert bob_lobbyship._bud_give == 0
    assert bob_lobbyship._bud_take == 0
    assert bob_lobbyship._bud_agenda_give == 0
    assert bob_lobbyship._bud_agenda_take == 0
    assert bob_lobbyship._bud_agenda_ratio_give == 0
    assert bob_lobbyship._bud_agenda_ratio_take == 0


def test_LobbyShip_set_bud_give_take_SetsAttrCorrectly():
    # ESTABLISH
    yao_text = "Yao"
    ohio_text = ",Ohio"
    ohio_credor_weight = 3.0
    lobbyships_sum_credor_weight = 60
    lobby_bud_give = 0.5
    lobby_bud_agenda_give = 0.98

    ohio_debtor_weight = 13.0
    lobbyships_sum_debtor_weight = 26.0
    lobby_bud_take = 0.9
    lobby_bud_agenda_take = 0.5151

    ohio_yao_lobbyship = lobbyship_shop(
        ohio_text, ohio_credor_weight, ohio_debtor_weight
    )
    assert ohio_yao_lobbyship._bud_give is None
    assert ohio_yao_lobbyship._bud_take is None
    assert ohio_yao_lobbyship._bud_agenda_give is None
    assert ohio_yao_lobbyship._bud_agenda_take is None

    # WHEN
    ohio_yao_lobbyship.set_bud_give_take(
        lobbyships_credor_weight_sum=lobbyships_sum_credor_weight,
        lobbyships_debtor_weight_sum=lobbyships_sum_debtor_weight,
        lobby_bud_give=lobby_bud_give,
        lobby_bud_take=lobby_bud_take,
        lobby_bud_agenda_give=lobby_bud_agenda_give,
        lobby_bud_agenda_take=lobby_bud_agenda_take,
    )

    # THEN
    assert ohio_yao_lobbyship._bud_give == 0.025
    assert ohio_yao_lobbyship._bud_take == 0.45
    assert ohio_yao_lobbyship._bud_agenda_give == 0.049
    assert ohio_yao_lobbyship._bud_agenda_take == 0.25755


def test_AwardLink_exists():
    # ESTABLISH
    bikers_text = "bikers"

    # WHEN
    bikers_awardlink = AwardLink(lobby_id=bikers_text)

    # THEN
    assert bikers_awardlink.lobby_id == bikers_text
    assert bikers_awardlink.give_weight == 1.0
    assert bikers_awardlink.take_weight == 1.0


def test_awardlink_shop_ReturnsCorrectObj():
    # ESTABLISH
    bikers_text = "bikers"
    bikers_give_weight = 3.0
    bikers_take_weight = 5.0

    # WHEN
    bikers_awardlink = awardlink_shop(
        lobby_id=bikers_text,
        give_weight=bikers_give_weight,
        take_weight=bikers_take_weight,
    )

    # THEN
    assert bikers_awardlink.give_weight == bikers_give_weight
    assert bikers_awardlink.take_weight == bikers_take_weight


def test_AwardHeir_set_bud_attr_CorrectlySetsAttr():
    # ESTABLISH
    bikers_text = "bikers"
    bikers_give_weight = 3.0
    bikers_debt_weight = 6.0
    awardlinks_sum_give_weight = 60
    awardlinks_sum_take_weight = 60
    idea_bud_share = 1
    lobby_heir_x = awardheir_shop(
        lobby_id=bikers_text,
        give_weight=bikers_give_weight,
        take_weight=bikers_debt_weight,
    )

    # WHEN
    lobby_heir_x.set_bud_give_take(
        idea_bud_share=idea_bud_share,
        awardheirs_give_weight_sum=awardlinks_sum_give_weight,
        awardheirs_take_weight_sum=awardlinks_sum_take_weight,
    )

    # THEN
    assert lobby_heir_x._bud_give == 0.05
    assert lobby_heir_x._bud_take == 0.1


def test_AwardLink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # ESTABLISH
    bikers_text = "bikers"
    bikers_give_weight = 3.0
    bikers_take_weight = 5.0
    bikers_awardlink = awardlink_shop(
        lobby_id=bikers_text,
        give_weight=bikers_give_weight,
        take_weight=bikers_take_weight,
    )

    print(f"{bikers_awardlink}")

    # WHEN
    biker_dict = bikers_awardlink.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "lobby_id": bikers_awardlink.lobby_id,
        "give_weight": bikers_awardlink.give_weight,
        "take_weight": bikers_awardlink.take_weight,
    }


def test_awardlinks_get_from_JSON_ReturnsCorrectObj_SimpleExample():
    # ESTABLISH
    teacher_text = "teachers"
    teacher_awardlink = awardlink_shop(
        lobby_id=teacher_text, give_weight=103, take_weight=155
    )
    teacher_dict = teacher_awardlink.get_dict()
    awardlinks_dict = {teacher_awardlink.lobby_id: teacher_dict}

    teachers_json = get_json_from_dict(dict_x=awardlinks_dict)
    assert teachers_json != None
    assert x_is_json(json_x=teachers_json)

    # WHEN
    awardlinks_obj_dict = awardlinks_get_from_json(awardlinks_json=teachers_json)

    # THEN
    assert awardlinks_obj_dict != None
    teachers_obj_check_dict = {teacher_awardlink.lobby_id: teacher_awardlink}
    print(f"    {awardlinks_obj_dict=}")
    print(f"{teachers_obj_check_dict=}")
    assert awardlinks_obj_dict == teachers_obj_check_dict


def test_AwardLine_exists():
    # ESTABLISH
    bikers_text = "bikers"
    bikers_bud_give = 0.33
    bikers_bud_take = 0.55

    # WHEN
    bikers_awardline = AwardLine(
        lobby_id=bikers_text,
        _bud_give=bikers_bud_give,
        _bud_take=bikers_bud_take,
    )

    # THEN
    assert bikers_awardline.lobby_id == bikers_text
    assert bikers_awardline._bud_give == bikers_bud_give
    assert bikers_awardline._bud_take == bikers_bud_take


def test_awardline_shop_ReturnsCorrectObj_exists():
    # ESTABLISH
    bikers_text = "bikers"
    bikers_text = bikers_text
    bikers_bud_give = 0.33
    bikers_bud_take = 0.55

    # WHEN
    biker_awardline = awardline_shop(
        lobby_id=bikers_text,
        _bud_give=bikers_bud_give,
        _bud_take=bikers_bud_take,
    )

    assert biker_awardline != None
    assert biker_awardline.lobby_id == bikers_text
    assert biker_awardline._bud_give == bikers_bud_give
    assert biker_awardline._bud_take == bikers_bud_take


def test_AwardLine_add_bud_give_take_CorrectlyModifiesAttr():
    # ESTABLISH
    bikers_text = "bikers"
    bikers_awardline = awardline_shop(
        lobby_id=bikers_text, _bud_give=0.33, _bud_take=0.55
    )
    assert bikers_awardline.lobby_id == bikers_text
    assert bikers_awardline._bud_give == 0.33
    assert bikers_awardline._bud_take == 0.55

    # WHEN
    bikers_awardline.add_bud_give_take(bud_give=0.11, bud_take=0.2)

    # THEN
    assert bikers_awardline._bud_give == 0.44
    assert bikers_awardline._bud_take == 0.75


def test_LobbyBox_exists():
    # ESTABLISH
    swim_text = ",swimmers"
    # WHEN
    swim_lobbybox = LobbyBox(lobby_id=swim_text)
    # THEN
    assert swim_lobbybox != None
    assert swim_lobbybox.lobby_id == swim_text
    assert swim_lobbybox._lobbyships is None
    assert swim_lobbybox._bud_give is None
    assert swim_lobbybox._bud_take is None
    assert swim_lobbybox._bud_agenda_give is None
    assert swim_lobbybox._bud_agenda_take is None
    assert swim_lobbybox._credor_pool is None
    assert swim_lobbybox._debtor_pool is None
    assert swim_lobbybox._road_delimiter is None


def test_lobbybox_shop_ReturnsCorrectObj():
    # ESTABLISH
    swim_text = ",swimmers"
    nation_road = create_road(root_label(), "nation-states")
    usa_road = create_road(nation_road, "USA")

    # WHEN
    swim_lobbybox = lobbybox_shop(lobby_id=swim_text)

    # THEN
    print(f"{swim_text}")
    assert swim_lobbybox != None
    assert swim_lobbybox.lobby_id != None
    assert swim_lobbybox.lobby_id == swim_text
    assert swim_lobbybox._lobbyships == {}
    assert swim_lobbybox._bud_give == 0
    assert swim_lobbybox._bud_take == 0
    assert swim_lobbybox._bud_agenda_give == 0
    assert swim_lobbybox._bud_agenda_take == 0
    assert swim_lobbybox._credor_pool == 0
    assert swim_lobbybox._debtor_pool == 0
    assert swim_lobbybox._road_delimiter == default_road_delimiter_if_none()


def test_lobbybox_shop_ReturnsCorrectObj_road_delimiter():
    # ESTABLISH
    swim_text = "/swimmers"
    slash_text = "/"

    # WHEN
    swim_lobbybox = lobbybox_shop(lobby_id=swim_text, _road_delimiter=slash_text)

    # THEN
    assert swim_lobbybox._road_delimiter == slash_text


# def test_LobbyBox_set_lobby_id_RaisesErrorIfParameterContains_road_delimiter_And_char_mirror_True():
#     # ESTABLISH
#     slash_text = "/"
#     bob_text = f"Bob{slash_text}Texas"

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         lobbybox_shop(bob_text, _char_mirror=True, _road_delimiter=slash_text)
#     assert (
#         str(excinfo.value)
#         == f"'{bob_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
#     )
