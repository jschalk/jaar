from src.bud.lobby import lobbyship_shop
from src.bud.acct import (
    acctunit_shop,
    acctunits_get_from_json,
    acctunit_get_from_dict,
    acctunits_get_from_dict,
)
from src._instrument.python import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_AcctUnit_get_lobbyships_dict_ReturnObj():
    # ESTABLISH
    sue_text = "Sue"
    sue_credor_weight = 11
    sue_debtor_weight = 13
    run_text = ",Run"
    run_credor_weight = 17
    run_debtor_weight = 23
    sue_lobbyship = lobbyship_shop(sue_text, sue_credor_weight, sue_debtor_weight)
    run_lobbyship = lobbyship_shop(run_text, run_credor_weight, run_debtor_weight)
    sue_acctunit = acctunit_shop(sue_text)
    sue_acctunit.set_lobbyship(sue_lobbyship)
    sue_acctunit.set_lobbyship(run_lobbyship)

    # WHEN
    sue_lobbyships_dict = sue_acctunit.get_lobbyships_dict()

    # THEN
    assert sue_lobbyships_dict.get(sue_text) is not None
    assert sue_lobbyships_dict.get(run_text) is not None
    sue_lobbyship_dict = sue_lobbyships_dict.get(sue_text)
    run_lobbyship_dict = sue_lobbyships_dict.get(run_text)
    assert sue_lobbyship_dict == {
        "lobby_id": sue_text,
        "credor_weight": sue_credor_weight,
        "debtor_weight": sue_debtor_weight,
    }
    assert run_lobbyship_dict == {
        "lobby_id": run_text,
        "credor_weight": run_credor_weight,
        "debtor_weight": run_debtor_weight,
    }


def test_AcctUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # ESTABLISH
    bob_text = "Bob"
    bob_acctunit = acctunit_shop(bob_text)

    bob_credor_weight = 13
    bob_debtor_weight = 17
    bob_acctunit.set_credor_weight(bob_credor_weight)
    bob_acctunit.set_debtor_weight(bob_debtor_weight)

    print(f"{bob_text}")

    bob_acctunit.set_lobbyship(lobbyship_shop(bob_text))
    run_text = ",Run"
    bob_acctunit.set_lobbyship(lobbyship_shop(run_text))

    # WHEN
    x_dict = bob_acctunit.get_dict()

    # THEN
    bl_dict = x_dict.get("_lobbyships")
    print(f"{bl_dict=}")
    assert x_dict is not None
    assert x_dict == {
        "acct_id": bob_text,
        "credor_weight": bob_credor_weight,
        "debtor_weight": bob_debtor_weight,
        "_lobbyships": {
            bob_text: {"lobby_id": bob_text, "credor_weight": 1, "debtor_weight": 1},
            run_text: {"lobby_id": run_text, "credor_weight": 1, "debtor_weight": 1},
        },
    }


def test_AcctUnit_get_dict_ReturnsDictWithAllAttrDataForJSON():
    # ESTABLISH
    bob_text = "Bob"
    bob_acctunit = acctunit_shop(bob_text)

    bob_credor_weight = 13
    bob_debtor_weight = 17
    bob_acctunit.set_credor_weight(bob_credor_weight)
    bob_acctunit.set_debtor_weight(bob_debtor_weight)
    bob_irrational_debtor_weight = 87
    bob_inallocable_debtor_weight = 97
    bob_acctunit.add_irrational_debtor_weight(bob_irrational_debtor_weight)
    bob_acctunit.add_inallocable_debtor_weight(bob_inallocable_debtor_weight)

    bob_fund_give = 55
    bob_fund_take = 47
    bob_fund_agenda_give = 51
    bob_fund_agenda_take = 67
    bob_fund_agenda_ratio_give = 71
    bob_fund_agenda_ratio_take = 73

    bob_acctunit._fund_give = bob_fund_give
    bob_acctunit._fund_take = bob_fund_take
    bob_acctunit._fund_agenda_give = bob_fund_agenda_give
    bob_acctunit._fund_agenda_take = bob_fund_agenda_take
    bob_acctunit._fund_agenda_ratio_give = bob_fund_agenda_ratio_give
    bob_acctunit._fund_agenda_ratio_take = bob_fund_agenda_ratio_take

    bob_acctunit.set_lobbyship(lobbyship_shop(bob_text))
    run_text = ",Run"
    bob_acctunit.set_lobbyship(lobbyship_shop(run_text))

    print(f"{bob_text}")

    # WHEN
    x_dict = bob_acctunit.get_dict(all_attrs=True)

    # THEN
    print(f"{x_dict=}")
    assert x_dict is not None
    assert x_dict == {
        "acct_id": bob_text,
        "credor_weight": bob_credor_weight,
        "debtor_weight": bob_debtor_weight,
        "_lobbyships": bob_acctunit.get_lobbyships_dict(),
        "_irrational_debtor_weight": bob_irrational_debtor_weight,
        "_inallocable_debtor_weight": bob_inallocable_debtor_weight,
        "_fund_give": bob_fund_give,
        "_fund_take": bob_fund_take,
        "_fund_agenda_give": bob_fund_agenda_give,
        "_fund_agenda_take": bob_fund_agenda_take,
        "_fund_agenda_ratio_give": bob_fund_agenda_ratio_give,
        "_fund_agenda_ratio_take": bob_fund_agenda_ratio_take,
    }


def test_AcctUnit_get_dict_ReturnsDictWith_irrational_missing_job_ValuesIsZerp():
    # ESTABLISH
    bob_text = "Bob"
    bob_acctunit = acctunit_shop(bob_text)
    assert bob_acctunit._irrational_debtor_weight == 0
    assert bob_acctunit._inallocable_debtor_weight == 0

    # WHEN
    x_dict = bob_acctunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtor_weight = "_irrational_debtor_weight"
    x_inallocable_debtor_weight = "_inallocable_debtor_weight"
    assert x_dict.get(x_irrational_debtor_weight) is None
    assert x_dict.get(x_inallocable_debtor_weight) is None
    assert len(x_dict.keys()) == 10


def test_AcctUnit_get_dict_ReturnsDictWith_irrational_missing_job_ValuesIsNumber():
    # ESTABLISH
    bob_text = "Bob"
    bob_acctunit = acctunit_shop(bob_text)
    bob_irrational_debtor_weight = 87
    bob_inallocable_debtor_weight = 97
    bob_acctunit.add_irrational_debtor_weight(bob_irrational_debtor_weight)
    bob_acctunit.add_inallocable_debtor_weight(bob_inallocable_debtor_weight)

    # WHEN
    x_dict = bob_acctunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtor_weight = "_irrational_debtor_weight"
    x_inallocable_debtor_weight = "_inallocable_debtor_weight"
    assert x_dict.get(x_irrational_debtor_weight) == bob_irrational_debtor_weight
    assert x_dict.get(x_inallocable_debtor_weight) == bob_inallocable_debtor_weight
    assert len(x_dict.keys()) == 12


def test_AcctUnit_get_dict_ReturnsDictWith_irrational_missing_job_ValuesIsNone():
    # ESTABLISH
    bob_text = "Bob"
    bob_acctunit = acctunit_shop(bob_text)
    bob_acctunit._irrational_debtor_weight = None
    bob_acctunit._inallocable_debtor_weight = None

    # WHEN
    x_dict = bob_acctunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtor_weight = "_irrational_debtor_weight"
    x_inallocable_debtor_weight = "_inallocable_debtor_weight"
    assert x_dict.get(x_irrational_debtor_weight) is None
    assert x_dict.get(x_inallocable_debtor_weight) is None
    assert len(x_dict.keys()) == 10


def test_acctunit_get_from_dict_ReturnsCorrectObjWith_road_delimiter():
    # ESTABLISH
    yao_text = ",Yao"
    slash_text = "/"
    before_yao_acctunit = acctunit_shop(yao_text, _road_delimiter=slash_text)
    yao_dict = before_yao_acctunit.get_dict()

    # WHEN
    after_yao_acctunit = acctunit_get_from_dict(yao_dict, slash_text)

    # THEN
    assert before_yao_acctunit == after_yao_acctunit
    assert after_yao_acctunit._road_delimiter == slash_text


def test_acctunit_get_from_dict_Returns_lobbyships():
    # ESTABLISH
    yao_text = ",Yao"
    slash_text = "/"
    before_yao_acctunit = acctunit_shop(yao_text, _road_delimiter=slash_text)
    ohio_text = f"{slash_text}ohio"
    iowa_text = f"{slash_text}iowa"
    before_yao_acctunit.set_lobbyship(lobbyship_shop(ohio_text))
    before_yao_acctunit.set_lobbyship(lobbyship_shop(iowa_text))
    yao_dict = before_yao_acctunit.get_dict()

    # WHEN
    after_yao_acctunit = acctunit_get_from_dict(yao_dict, slash_text)

    # THEN
    assert before_yao_acctunit._lobbyships == after_yao_acctunit._lobbyships
    assert before_yao_acctunit == after_yao_acctunit
    assert after_yao_acctunit._road_delimiter == slash_text


def test_acctunits_get_from_dict_ReturnsCorrectObjWith_road_delimiter():
    # ESTABLISH
    yao_text = ",Yao"
    slash_text = "/"
    yao_acctunit = acctunit_shop(yao_text, _road_delimiter=slash_text)
    yao_dict = yao_acctunit.get_dict()
    x_acctunits_dict = {yao_text: yao_dict}

    # WHEN
    x_acctunits_objs = acctunits_get_from_dict(x_acctunits_dict, slash_text)

    # THEN
    assert x_acctunits_objs.get(yao_text) == yao_acctunit
    assert x_acctunits_objs.get(yao_text)._road_delimiter == slash_text


def test_acctunits_get_from_json_ReturnsCorrectObj_SimpleExampleWithIncompleteData():
    # ESTABLISH
    yao_text = "Yao"
    yao_credor_weight = 13
    yao_debtor_weight = 17
    yao_irrational_debtor_weight = 87
    yao_inallocable_debtor_weight = 97
    yao_json_dict = {
        yao_text: {
            "acct_id": yao_text,
            "credor_weight": yao_credor_weight,
            "debtor_weight": yao_debtor_weight,
            "_lobbyships": {},
            "_irrational_debtor_weight": yao_irrational_debtor_weight,
            "_inallocable_debtor_weight": yao_inallocable_debtor_weight,
        }
    }
    yao_json_text = get_json_from_dict(dict_x=yao_json_dict)
    assert x_is_json(json_x=yao_json_text)

    # WHEN
    yao_obj_dict = acctunits_get_from_json(acctunits_json=yao_json_text)

    # THEN
    assert yao_obj_dict[yao_text] is not None
    yao_acctunit = yao_obj_dict[yao_text]

    assert yao_acctunit.acct_id == yao_text
    assert yao_acctunit.credor_weight == yao_credor_weight
    assert yao_acctunit.debtor_weight == yao_debtor_weight
    assert yao_acctunit._irrational_debtor_weight == yao_irrational_debtor_weight
    assert yao_acctunit._inallocable_debtor_weight == yao_inallocable_debtor_weight
