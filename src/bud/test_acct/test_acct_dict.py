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
    sue_credit_score = 11
    sue_debtit_score = 13
    run_text = ",Run"
    run_credit_score = 17
    run_debtit_score = 23
    sue_lobbyship = lobbyship_shop(sue_text, sue_credit_score, sue_debtit_score)
    run_lobbyship = lobbyship_shop(run_text, run_credit_score, run_debtit_score)
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
        "credit_score": sue_credit_score,
        "debtit_score": sue_debtit_score,
    }
    assert run_lobbyship_dict == {
        "lobby_id": run_text,
        "credit_score": run_credit_score,
        "debtit_score": run_debtit_score,
    }


def test_AcctUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # ESTABLISH
    bob_text = "Bob"
    bob_acctunit = acctunit_shop(bob_text)

    bob_credit_score = 13
    bob_debtit_score = 17
    bob_acctunit.set_credit_score(bob_credit_score)
    bob_acctunit.set_debtit_score(bob_debtit_score)

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
        "credit_score": bob_credit_score,
        "debtit_score": bob_debtit_score,
        "_lobbyships": {
            bob_text: {"lobby_id": bob_text, "credit_score": 1, "debtit_score": 1},
            run_text: {"lobby_id": run_text, "credit_score": 1, "debtit_score": 1},
        },
    }


def test_AcctUnit_get_dict_ReturnsDictWithAllAttrDataForJSON():
    # ESTABLISH
    bob_text = "Bob"
    bob_acctunit = acctunit_shop(bob_text)

    bob_credit_score = 13
    bob_debtit_score = 17
    bob_acctunit.set_credit_score(bob_credit_score)
    bob_acctunit.set_debtit_score(bob_debtit_score)
    bob_irrational_debtit_score = 87
    bob_inallocable_debtit_score = 97
    bob_acctunit.add_irrational_debtit_score(bob_irrational_debtit_score)
    bob_acctunit.add_inallocable_debtit_score(bob_inallocable_debtit_score)

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
        "credit_score": bob_credit_score,
        "debtit_score": bob_debtit_score,
        "_lobbyships": bob_acctunit.get_lobbyships_dict(),
        "_irrational_debtit_score": bob_irrational_debtit_score,
        "_inallocable_debtit_score": bob_inallocable_debtit_score,
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
    assert bob_acctunit._irrational_debtit_score == 0
    assert bob_acctunit._inallocable_debtit_score == 0

    # WHEN
    x_dict = bob_acctunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtit_score = "_irrational_debtit_score"
    x_inallocable_debtit_score = "_inallocable_debtit_score"
    assert x_dict.get(x_irrational_debtit_score) is None
    assert x_dict.get(x_inallocable_debtit_score) is None
    assert len(x_dict.keys()) == 10


def test_AcctUnit_get_dict_ReturnsDictWith_irrational_missing_job_ValuesIsNumber():
    # ESTABLISH
    bob_text = "Bob"
    bob_acctunit = acctunit_shop(bob_text)
    bob_irrational_debtit_score = 87
    bob_inallocable_debtit_score = 97
    bob_acctunit.add_irrational_debtit_score(bob_irrational_debtit_score)
    bob_acctunit.add_inallocable_debtit_score(bob_inallocable_debtit_score)

    # WHEN
    x_dict = bob_acctunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtit_score = "_irrational_debtit_score"
    x_inallocable_debtit_score = "_inallocable_debtit_score"
    assert x_dict.get(x_irrational_debtit_score) == bob_irrational_debtit_score
    assert x_dict.get(x_inallocable_debtit_score) == bob_inallocable_debtit_score
    assert len(x_dict.keys()) == 12


def test_AcctUnit_get_dict_ReturnsDictWith_irrational_missing_job_ValuesIsNone():
    # ESTABLISH
    bob_text = "Bob"
    bob_acctunit = acctunit_shop(bob_text)
    bob_acctunit._irrational_debtit_score = None
    bob_acctunit._inallocable_debtit_score = None

    # WHEN
    x_dict = bob_acctunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtit_score = "_irrational_debtit_score"
    x_inallocable_debtit_score = "_inallocable_debtit_score"
    assert x_dict.get(x_irrational_debtit_score) is None
    assert x_dict.get(x_inallocable_debtit_score) is None
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
    yao_credit_score = 13
    yao_debtit_score = 17
    yao_irrational_debtit_score = 87
    yao_inallocable_debtit_score = 97
    yao_json_dict = {
        yao_text: {
            "acct_id": yao_text,
            "credit_score": yao_credit_score,
            "debtit_score": yao_debtit_score,
            "_lobbyships": {},
            "_irrational_debtit_score": yao_irrational_debtit_score,
            "_inallocable_debtit_score": yao_inallocable_debtit_score,
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
    assert yao_acctunit.credit_score == yao_credit_score
    assert yao_acctunit.debtit_score == yao_debtit_score
    assert yao_acctunit._irrational_debtit_score == yao_irrational_debtit_score
    assert yao_acctunit._inallocable_debtit_score == yao_inallocable_debtit_score
