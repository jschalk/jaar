from src._world.lobby import lobbylink_shop
from src._world.char import (
    charunit_shop,
    charunits_get_from_json,
    charunit_get_from_dict,
    charunits_get_from_dict,
)
from src._instrument.python import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_CharUnit_get_lobbylinks_dict_ReturnObj():
    # GIVEN
    sue_text = "Sue"
    sue_credor_weight = 11
    sue_debtor_weight = 13
    run_text = ",Run"
    run_credor_weight = 17
    run_debtor_weight = 23
    sue_lobbylink = lobbylink_shop(sue_text, sue_credor_weight, sue_debtor_weight)
    run_lobbylink = lobbylink_shop(run_text, run_credor_weight, run_debtor_weight)
    sue_charunit = charunit_shop(sue_text)
    sue_charunit.set_lobbylink(sue_lobbylink)
    sue_charunit.set_lobbylink(run_lobbylink)

    # WHEN
    sue_lobbylinks_dict = sue_charunit.get_lobbylinks_dict()

    # THEN
    assert sue_lobbylinks_dict.get(sue_text) != None
    assert sue_lobbylinks_dict.get(run_text) != None
    sue_lobbylink_dict = sue_lobbylinks_dict.get(sue_text)
    run_lobbylink_dict = sue_lobbylinks_dict.get(run_text)
    assert sue_lobbylink_dict == {
        "lobby_id": sue_text,
        "credor_weight": sue_credor_weight,
        "debtor_weight": sue_debtor_weight,
    }
    assert run_lobbylink_dict == {
        "lobby_id": run_text,
        "credor_weight": run_credor_weight,
        "debtor_weight": run_debtor_weight,
    }


def test_CharUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    bob_text = "Bob"
    bob_charunit = charunit_shop(bob_text)

    bob_credor_weight = 13
    bob_debtor_weight = 17
    bob_charunit.set_credor_weight(bob_credor_weight)
    bob_charunit.set_debtor_weight(bob_debtor_weight)

    print(f"{bob_text}")

    bob_charunit.set_lobbylink(lobbylink_shop(bob_text))
    run_text = ",Run"
    bob_charunit.set_lobbylink(lobbylink_shop(run_text))

    # WHEN
    x_dict = bob_charunit.get_dict()

    # THEN
    bl_dict = x_dict.get("_lobbylinks")
    print(f"{bl_dict=}")
    assert x_dict != None
    assert x_dict == {
        "char_id": bob_text,
        "credor_weight": bob_credor_weight,
        "debtor_weight": bob_debtor_weight,
        "_lobbylinks": {
            bob_text: {"lobby_id": bob_text, "credor_weight": 1, "debtor_weight": 1},
            run_text: {"lobby_id": run_text, "credor_weight": 1, "debtor_weight": 1},
        },
    }


def test_CharUnit_get_dict_ReturnsDictWithAllAttrDataForJSON():
    # GIVEN
    bob_text = "Bob"
    bob_charunit = charunit_shop(bob_text)

    bob_credor_weight = 13
    bob_debtor_weight = 17
    bob_charunit.set_credor_weight(bob_credor_weight)
    bob_charunit.set_debtor_weight(bob_debtor_weight)
    bob_irrational_debtor_weight = 87
    bob_inallocable_debtor_weight = 97
    bob_charunit.add_irrational_debtor_weight(bob_irrational_debtor_weight)
    bob_charunit.add_inallocable_debtor_weight(bob_inallocable_debtor_weight)

    bob_world_cred = 55
    bob_world_debt = 47
    bob_world_agenda_cred = 51
    bob_world_agenda_debt = 67
    bob_world_agenda_ratio_cred = 71
    bob_world_agenda_ratio_debt = 73

    bob_charunit._world_cred = bob_world_cred
    bob_charunit._world_debt = bob_world_debt
    bob_charunit._world_agenda_cred = bob_world_agenda_cred
    bob_charunit._world_agenda_debt = bob_world_agenda_debt
    bob_charunit._world_agenda_ratio_cred = bob_world_agenda_ratio_cred
    bob_charunit._world_agenda_ratio_debt = bob_world_agenda_ratio_debt

    bob_charunit.set_lobbylink(lobbylink_shop(bob_text))
    run_text = ",Run"
    bob_charunit.set_lobbylink(lobbylink_shop(run_text))

    print(f"{bob_text}")

    # WHEN
    x_dict = bob_charunit.get_dict(all_attrs=True)

    # THEN
    print(f"{x_dict=}")
    assert x_dict != None
    assert x_dict == {
        "char_id": bob_text,
        "credor_weight": bob_credor_weight,
        "debtor_weight": bob_debtor_weight,
        "_lobbylinks": bob_charunit.get_lobbylinks_dict(),
        "_irrational_debtor_weight": bob_irrational_debtor_weight,
        "_inallocable_debtor_weight": bob_inallocable_debtor_weight,
        "_world_cred": bob_world_cred,
        "_world_debt": bob_world_debt,
        "_world_agenda_cred": bob_world_agenda_cred,
        "_world_agenda_debt": bob_world_agenda_debt,
        "_world_agenda_ratio_cred": bob_world_agenda_ratio_cred,
        "_world_agenda_ratio_debt": bob_world_agenda_ratio_debt,
    }


def test_CharUnit_get_dict_ReturnsDictWith_irrational_missing_job_ValuesIsZerp():
    # GIVEN
    bob_text = "Bob"
    bob_charunit = charunit_shop(bob_text)
    assert bob_charunit._irrational_debtor_weight == 0
    assert bob_charunit._inallocable_debtor_weight == 0

    # WHEN
    x_dict = bob_charunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtor_weight = "_irrational_debtor_weight"
    x_inallocable_debtor_weight = "_inallocable_debtor_weight"
    assert x_dict.get(x_irrational_debtor_weight) is None
    assert x_dict.get(x_inallocable_debtor_weight) is None
    assert len(x_dict.keys()) == 10


def test_CharUnit_get_dict_ReturnsDictWith_irrational_missing_job_ValuesIsNumber():
    # GIVEN
    bob_text = "Bob"
    bob_charunit = charunit_shop(bob_text)
    bob_irrational_debtor_weight = 87
    bob_inallocable_debtor_weight = 97
    bob_charunit.add_irrational_debtor_weight(bob_irrational_debtor_weight)
    bob_charunit.add_inallocable_debtor_weight(bob_inallocable_debtor_weight)

    # WHEN
    x_dict = bob_charunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtor_weight = "_irrational_debtor_weight"
    x_inallocable_debtor_weight = "_inallocable_debtor_weight"
    assert x_dict.get(x_irrational_debtor_weight) == bob_irrational_debtor_weight
    assert x_dict.get(x_inallocable_debtor_weight) == bob_inallocable_debtor_weight
    assert len(x_dict.keys()) == 12


def test_CharUnit_get_dict_ReturnsDictWith_irrational_missing_job_ValuesIsNone():
    # GIVEN
    bob_text = "Bob"
    bob_charunit = charunit_shop(bob_text)
    bob_charunit._irrational_debtor_weight = None
    bob_charunit._inallocable_debtor_weight = None

    # WHEN
    x_dict = bob_charunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtor_weight = "_irrational_debtor_weight"
    x_inallocable_debtor_weight = "_inallocable_debtor_weight"
    assert x_dict.get(x_irrational_debtor_weight) is None
    assert x_dict.get(x_inallocable_debtor_weight) is None
    assert len(x_dict.keys()) == 10


def test_charunit_get_from_dict_ReturnsCorrectObjWith_road_delimiter():
    # GIVEN
    yao_text = ",Yao"
    slash_text = "/"
    before_yao_charunit = charunit_shop(yao_text, _road_delimiter=slash_text)
    yao_dict = before_yao_charunit.get_dict()

    # WHEN
    after_yao_charunit = charunit_get_from_dict(yao_dict, slash_text)

    # THEN
    assert before_yao_charunit == after_yao_charunit
    assert after_yao_charunit._road_delimiter == slash_text


def test_charunit_get_from_dict_Returns_lobbylinks():
    # GIVEN
    yao_text = ",Yao"
    slash_text = "/"
    before_yao_charunit = charunit_shop(yao_text, _road_delimiter=slash_text)
    ohio_text = f"{slash_text}ohio"
    iowa_text = f"{slash_text}iowa"
    before_yao_charunit.set_lobbylink(lobbylink_shop(ohio_text))
    before_yao_charunit.set_lobbylink(lobbylink_shop(iowa_text))
    yao_dict = before_yao_charunit.get_dict()

    # WHEN
    after_yao_charunit = charunit_get_from_dict(yao_dict, slash_text)

    # THEN
    assert before_yao_charunit._lobbylinks == after_yao_charunit._lobbylinks
    assert before_yao_charunit == after_yao_charunit
    assert after_yao_charunit._road_delimiter == slash_text


def test_charunits_get_from_dict_ReturnsCorrectObjWith_road_delimiter():
    # GIVEN
    yao_text = ",Yao"
    slash_text = "/"
    yao_charunit = charunit_shop(yao_text, _road_delimiter=slash_text)
    yao_dict = yao_charunit.get_dict()
    x_charunits_dict = {yao_text: yao_dict}

    # WHEN
    x_charunits_objs = charunits_get_from_dict(x_charunits_dict, slash_text)

    # THEN
    assert x_charunits_objs.get(yao_text) == yao_charunit
    assert x_charunits_objs.get(yao_text)._road_delimiter == slash_text


def test_charunits_get_from_json_ReturnsCorrectObj_SimpleExampleWithIncompleteData():
    # GIVEN
    yao_text = "Yao"
    yao_credor_weight = 13
    yao_debtor_weight = 17
    yao_irrational_debtor_weight = 87
    yao_inallocable_debtor_weight = 97
    yao_json_dict = {
        yao_text: {
            "char_id": yao_text,
            "credor_weight": yao_credor_weight,
            "debtor_weight": yao_debtor_weight,
            "_lobbylinks": {},
            "_irrational_debtor_weight": yao_irrational_debtor_weight,
            "_inallocable_debtor_weight": yao_inallocable_debtor_weight,
        }
    }
    yao_json_text = get_json_from_dict(dict_x=yao_json_dict)
    assert x_is_json(json_x=yao_json_text)

    # WHEN
    yao_obj_dict = charunits_get_from_json(charunits_json=yao_json_text)

    # THEN
    assert yao_obj_dict[yao_text] != None
    yao_charunit = yao_obj_dict[yao_text]

    assert yao_charunit.char_id == yao_text
    assert yao_charunit.credor_weight == yao_credor_weight
    assert yao_charunit.debtor_weight == yao_debtor_weight
    assert yao_charunit._irrational_debtor_weight == yao_irrational_debtor_weight
    assert yao_charunit._inallocable_debtor_weight == yao_inallocable_debtor_weight
