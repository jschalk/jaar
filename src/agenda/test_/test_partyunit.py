from src._prime.road import validate_roadnode, default_road_delimiter_if_none
from src.agenda.party import (
    PartyUnit,
    PartyID,
    partyunit_shop,
    partyunits_get_from_json,
    get_default_depotlink_type,
)
from src.instrument.python import x_is_json, x_get_json
from pytest import raises as pytest_raises


def test_PartyUnit_exists():
    # GIVEN
    bob_party_id = "Bob"

    # WHEN
    bob_partyunit = PartyUnit(party_id=bob_party_id)

    # THEN
    print(f"{bob_party_id}")
    assert bob_partyunit != None
    assert bob_partyunit.party_id != None
    assert bob_partyunit.party_id == bob_party_id
    assert bob_partyunit.creditor_weight is None
    assert bob_partyunit.debtor_weight is None
    assert bob_partyunit.depotlink_type is None
    assert bob_partyunit._agenda_credit is None
    assert bob_partyunit._agenda_debt is None
    assert bob_partyunit._agenda_intent_credit is None
    assert bob_partyunit._agenda_intent_debt is None
    assert bob_partyunit._creditor_live is None
    assert bob_partyunit._debtor_live is None
    assert bob_partyunit._bank_tax_paid is None
    assert bob_partyunit._bank_tax_diff is None
    assert bob_partyunit._bank_credit_score is None
    assert bob_partyunit._bank_voice_rank is None
    assert bob_partyunit._bank_voice_hx_lowest_rank is None
    assert bob_partyunit._output_agenda_meld_order is None
    assert bob_partyunit._road_delimiter is None


def test_PartyUnit_set_party_id_CorrectlySetsAttr():
    # GIVEN
    x_partyunit = PartyUnit()

    # WHEN
    bob_party_id = "Bob"
    x_partyunit.set_party_id(bob_party_id)

    # THEN
    assert x_partyunit.party_id == bob_party_id


def test_PartyUnit_set_party_id_RaisesErrorIfParameterContains_road_delimiter():
    # GIVEN
    slash_text = "/"
    texas_text = f"Texas{slash_text}Arkansas"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        partyunit_shop(party_id=texas_text, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{texas_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_partyunit_shop_CorrectlySetsAttributes():
    # WHEN
    todd_text = "Todd"

    # WHEN
    todd_partyunit = partyunit_shop(party_id=todd_text)

    # THEN
    assert todd_partyunit._agenda_credit == 0
    assert todd_partyunit._agenda_debt == 0
    assert todd_partyunit._agenda_intent_credit == 0
    assert todd_partyunit._agenda_intent_debt == 0
    assert todd_partyunit._agenda_intent_ratio_credit == 0
    assert todd_partyunit._agenda_intent_ratio_debt == 0
    assert todd_partyunit._road_delimiter == default_road_delimiter_if_none()


def test_partyunit_shop_CorrectlySetsAttributes_road_delimiter():
    # WHEN
    todd_text = "Todd"
    slash_text = "/"

    # WHEN
    todd_partyunit = partyunit_shop(party_id=todd_text, _road_delimiter=slash_text)

    # THEN
    assert todd_partyunit._road_delimiter == slash_text


def test_PartyUnit_set_output_agenda_meld_order_CorrectlySetsAttribute():
    # GIVEN
    bob_party_id = "Bob"
    bob_partyunit = partyunit_shop(party_id=bob_party_id)
    assert bob_partyunit._output_agenda_meld_order is None

    # WHEN
    x_output_agenda_meld_order = 5
    bob_partyunit.set_output_agenda_meld_order(x_output_agenda_meld_order)

    # THEN
    assert bob_partyunit._output_agenda_meld_order == x_output_agenda_meld_order


def test_PartyUnit_clear_output_agenda_meld_order_CorrectlySetsAttribute():
    # GIVEN
    bob_party_id = "Bob"
    bob_partyunit = partyunit_shop(party_id=bob_party_id)
    x_output_agenda_meld_order = 5
    bob_partyunit.set_output_agenda_meld_order(x_output_agenda_meld_order)
    assert bob_partyunit._output_agenda_meld_order == x_output_agenda_meld_order

    # WHEN
    bob_partyunit.clear_output_agenda_meld_order()

    # THEN
    assert bob_partyunit._output_agenda_meld_order is None


def test_PartyUnit_set_depotlink_type_CorrectlySetsAttributeNoNulls():
    # GIVEN
    bob_party_id = "Bob"
    bob_partyunit = partyunit_shop(party_id=bob_party_id)

    # WHEN
    depotlink_type_x = "assignment"
    bob_partyunit.set_depotlink_type(
        depotlink_type=depotlink_type_x, creditor_weight=23, debtor_weight=34
    )

    # THEN
    assert bob_partyunit.depotlink_type == depotlink_type_x
    assert bob_partyunit.creditor_weight == 23
    assert bob_partyunit.debtor_weight == 34


def test_PartyUnit_set_depotlink_type_CorrectlySetsAttributeWithNullsAndStartingValues():
    # GIVEN
    bob_party_id = "Bob"
    bob_partyunit = partyunit_shop(
        party_id=bob_party_id, creditor_weight=45, debtor_weight=56
    )

    # WHEN
    depotlink_type_x = "assignment"
    bob_partyunit.set_depotlink_type(
        depotlink_type=depotlink_type_x, creditor_weight=None, debtor_weight=None
    )

    # THEN
    assert bob_partyunit.depotlink_type == depotlink_type_x
    assert bob_partyunit.creditor_weight == 45
    assert bob_partyunit.debtor_weight == 56


def test_PartyUnit_set_depotlink_type_CorrectlySetsAttributeWithNullsAndNoStartingValues():
    # GIVEN
    bob_party_id = "Bob"
    bob_partyunit = partyunit_shop(party_id=bob_party_id)

    # WHEN
    depotlink_type_x = "assignment"
    bob_partyunit.set_depotlink_type(
        depotlink_type=depotlink_type_x, creditor_weight=None, debtor_weight=None
    )

    # THEN
    assert bob_partyunit.depotlink_type == depotlink_type_x
    assert bob_partyunit.creditor_weight == 1
    assert bob_partyunit.debtor_weight == 1


def test_PartyUnit_del_depotlink_type_CorrectlySetsAttributeToNone():
    # GIVEN
    bob_party_id = "Bob"
    bob_partyunit = partyunit_shop(
        party_id=bob_party_id, creditor_weight=45, debtor_weight=56
    )
    depotlink_type_x = "assignment"
    bob_partyunit.set_depotlink_type(depotlink_type=depotlink_type_x)
    assert bob_partyunit.depotlink_type == depotlink_type_x
    assert bob_partyunit.creditor_weight == 45
    assert bob_partyunit.debtor_weight == 56

    # WHEN
    bob_partyunit.del_depotlink_type()

    # THEN
    assert bob_partyunit.depotlink_type is None
    assert bob_partyunit.creditor_weight == 45
    assert bob_partyunit.debtor_weight == 56


def test_PartyUnit_set_depotlink_type_raisesErrorIfByTypeIsEntered():
    # GIVEN
    unacceptable_type_text = "unacceptable"
    bob_party_id = "Bob"
    bob_partyunit = partyunit_shop(party_id=bob_party_id)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_partyunit.set_depotlink_type(depotlink_type=unacceptable_type_text)
    assert (
        str(excinfo.value)
        == f"PartyUnit '{bob_partyunit.party_id}' cannot have type '{unacceptable_type_text}'."
    )


def test_get_default_depotlink_type_ReturnsCorrectObj():
    # GIVEN / WHEN
    assert get_default_depotlink_type() == "assignment"


def test_PartyUnit_reset_agenda_credit_debt_MethodWorkCorrectly():
    # GIVEN
    bob_party_id = "Bob"
    bob_partyunit = partyunit_shop(party_id=bob_party_id)
    bob_partyunit._agenda_credit = 0.27
    bob_partyunit._agenda_debt = 0.37
    bob_partyunit._agenda_intent_credit = 0.41
    bob_partyunit._agenda_intent_debt = 0.51
    bob_partyunit._agenda_intent_ratio_credit = 0.433
    bob_partyunit._agenda_intent_ratio_debt = 0.533
    assert bob_partyunit._agenda_credit == 0.27
    assert bob_partyunit._agenda_debt == 0.37
    assert bob_partyunit._agenda_intent_credit == 0.41
    assert bob_partyunit._agenda_intent_debt == 0.51
    assert bob_partyunit._agenda_intent_ratio_credit == 0.433
    assert bob_partyunit._agenda_intent_ratio_debt == 0.533

    # WHEN
    bob_partyunit.reset_agenda_credit_debt()

    # THEN
    assert bob_partyunit._agenda_credit == 0
    assert bob_partyunit._agenda_debt == 0
    assert bob_partyunit._agenda_intent_credit == 0
    assert bob_partyunit._agenda_intent_debt == 0
    assert bob_partyunit._agenda_intent_ratio_credit == 0
    assert bob_partyunit._agenda_intent_ratio_debt == 0


def test_PartyUnit_add_agenda_credit_debt_MethodWorkCorrectly():
    # GIVEN
    bob_party_id = "Bob"
    bob_partyunit = partyunit_shop(party_id=bob_party_id)
    bob_partyunit._agenda_credit = 0.4106
    bob_partyunit._agenda_debt = 0.1106
    bob_partyunit._agenda_intent_credit = 0.41
    bob_partyunit._agenda_intent_debt = 0.51
    assert bob_partyunit._agenda_intent_credit == 0.41
    assert bob_partyunit._agenda_intent_debt == 0.51

    # WHEN
    bob_partyunit.add_agenda_credit_debt(
        agenda_credit=0.33,
        agenda_debt=0.055,
        agenda_intent_credit=0.3,
        agenda_intent_debt=0.05,
    )

    # THEN
    assert bob_partyunit._agenda_credit == 0.7406
    assert bob_partyunit._agenda_debt == 0.1656
    assert bob_partyunit._agenda_intent_credit == 0.71
    assert bob_partyunit._agenda_intent_debt == 0.56


def test_PartyUnit_set_agenda_intent_ratio_credit_debt_MethodWorkCorrectly():
    # GIVEN
    bob_party_id = "Bob"
    bob_partyunit = partyunit_shop(bob_party_id, creditor_weight=15, debtor_weight=7)
    bob_partyunit._agenda_credit = 0.4106
    bob_partyunit._agenda_debt = 0.1106
    bob_partyunit._agenda_intent_credit = 0.041
    bob_partyunit._agenda_intent_debt = 0.051
    bob_partyunit._agenda_intent_ratio_credit = 0
    bob_partyunit._agenda_intent_ratio_debt = 0
    assert bob_partyunit._agenda_intent_ratio_credit == 0
    assert bob_partyunit._agenda_intent_ratio_debt == 0

    # WHEN
    bob_partyunit.set_agenda_intent_ratio_credit_debt(
        agenda_intent_ratio_credit_sum=0.2,
        agenda_intent_ratio_debt_sum=0.5,
        agenda_partyunit_total_creditor_weight=20,
        agenda_partyunit_total_debtor_weight=14,
    )

    # THEN
    assert bob_partyunit._agenda_intent_ratio_credit == 0.205
    assert bob_partyunit._agenda_intent_ratio_debt == 0.102

    # WHEN
    bob_partyunit.set_agenda_intent_ratio_credit_debt(
        agenda_intent_ratio_credit_sum=0,
        agenda_intent_ratio_debt_sum=0,
        agenda_partyunit_total_creditor_weight=20,
        agenda_partyunit_total_debtor_weight=14,
    )

    # THEN
    assert bob_partyunit._agenda_intent_ratio_credit == 0.75
    assert bob_partyunit._agenda_intent_ratio_debt == 0.5


def test_PartyUnit_set_banking_data_MethodWorkCorrectly():
    # GIVEN
    bob_party_id = "Bob"
    x_agenda_intent_ratio_credit = 0.077
    x_agenda_intent_ratio_debt = 0.066

    bob_partyunit = partyunit_shop(party_id=bob_party_id)
    bob_partyunit._agenda_intent_ratio_credit = x_agenda_intent_ratio_credit
    bob_partyunit._agenda_intent_ratio_debt = x_agenda_intent_ratio_debt
    assert bob_partyunit._agenda_intent_ratio_credit == 0.077
    assert bob_partyunit._agenda_intent_ratio_debt == 0.066
    assert bob_partyunit._bank_tax_paid is None
    assert bob_partyunit._bank_tax_diff is None
    assert bob_partyunit._bank_credit_score is None
    assert bob_partyunit._bank_voice_rank is None
    assert bob_partyunit._bank_voice_hx_lowest_rank is None

    # WHEN
    x_tax_paid = 0.2
    x_tax_diff = 0.123
    x_bank_credit_score = 900
    x_bank_voice_rank = 45
    bob_partyunit.set_banking_data(
        tax_paid=x_tax_paid,
        tax_diff=x_tax_diff,
        credit_score=x_bank_credit_score,
        voice_rank=x_bank_voice_rank,
    )
    # THEN
    assert bob_partyunit._agenda_intent_ratio_credit == x_agenda_intent_ratio_credit
    assert bob_partyunit._agenda_intent_ratio_debt == x_agenda_intent_ratio_debt
    assert bob_partyunit._bank_tax_paid == x_tax_paid
    assert bob_partyunit._bank_tax_diff == x_tax_diff
    assert bob_partyunit._bank_credit_score == x_bank_credit_score
    assert bob_partyunit._bank_voice_rank == x_bank_voice_rank
    assert bob_partyunit._bank_voice_hx_lowest_rank == x_bank_voice_rank


def test_PartyUnit_set_banking_data_CorrectlyDecreasesOrIgnores_bank_voice_hx_lowest_rank():
    # GIVEN
    bob_party_id = "Bob"
    x_agenda_intent_ratio_credit = 0.077
    x_agenda_intent_ratio_debt = 0.066
    bob_partyunit = partyunit_shop(bob_party_id)
    bob_partyunit._agenda_intent_ratio_credit = x_agenda_intent_ratio_credit
    bob_partyunit._agenda_intent_ratio_debt = x_agenda_intent_ratio_debt
    x_tax_paid = 0.2
    x_tax_diff = 0.123
    x_bank_credit_score = 900
    old_x_bank_voice_rank = 45
    bob_partyunit.set_banking_data(
        tax_paid=x_tax_paid,
        tax_diff=x_tax_diff,
        credit_score=x_bank_credit_score,
        voice_rank=old_x_bank_voice_rank,
    )
    assert bob_partyunit._bank_voice_hx_lowest_rank == old_x_bank_voice_rank

    # WHEN
    new_x_bank_voice_rank = 33
    bob_partyunit.set_banking_data(
        tax_paid=x_tax_paid,
        tax_diff=x_tax_diff,
        credit_score=x_bank_credit_score,
        voice_rank=new_x_bank_voice_rank,
    )
    # THEN
    assert bob_partyunit._bank_voice_hx_lowest_rank == new_x_bank_voice_rank

    # WHEN
    not_lower_x_bank_voice_rank = 60
    bob_partyunit.set_banking_data(
        tax_paid=x_tax_paid,
        tax_diff=x_tax_diff,
        credit_score=x_bank_credit_score,
        voice_rank=not_lower_x_bank_voice_rank,
    )
    # THEN
    assert bob_partyunit._bank_voice_hx_lowest_rank == new_x_bank_voice_rank


def test_PartyUnit_clear_banking_data_MethodWorkCorrectly():
    # GIVEN
    bob_party_id = "Bob"
    bob_partyunit = partyunit_shop(bob_party_id)
    bob_partyunit._agenda_intent_ratio_credit = 0.355
    bob_partyunit._agenda_intent_ratio_debt = 0.066
    x_bank_credit_score = 900
    x_bank_voice_rank = 45
    bob_partyunit.set_banking_data(
        tax_paid=0.399,
        tax_diff=0.044,
        credit_score=x_bank_credit_score,
        voice_rank=x_bank_voice_rank,
    )
    assert bob_partyunit._bank_tax_paid == 0.399
    assert bob_partyunit._bank_tax_diff == 0.044
    assert bob_partyunit._bank_credit_score == x_bank_credit_score
    assert bob_partyunit._bank_voice_rank == x_bank_voice_rank

    # WHEN
    bob_partyunit.clear_banking_data()

    # THEN
    assert bob_partyunit._bank_tax_paid is None
    assert bob_partyunit._bank_tax_diff is None
    assert bob_partyunit._bank_credit_score is None
    assert bob_partyunit._bank_voice_rank is None


def test_PartyUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    bob_text = "Bob"
    bob_bank_tax_paid = 0.55
    bob_bank_tax_diff = 0.66
    depotlink_type = "assignment"
    bob_partyunit = partyunit_shop(bob_text, depotlink_type=depotlink_type)
    bob_partyunit._bank_tax_paid = bob_bank_tax_paid
    bob_partyunit._bank_tax_diff = bob_bank_tax_diff
    bob_creditor_live = False
    bob_debtor_live = True
    bob_partyunit._creditor_live = bob_creditor_live
    bob_partyunit._debtor_live = bob_debtor_live

    bob_creditor_weight = 13
    bob_debtor_weight = 17
    bob_partyunit.creditor_weight = bob_creditor_weight
    bob_partyunit.debtor_weight = bob_debtor_weight

    bob_bank_credit_score = 7000
    bob_bank_voice_rank = 898
    bob_bank_voice_hx_lowest_rank = 740
    bob_partyunit._bank_credit_score = bob_bank_credit_score
    bob_partyunit._bank_voice_rank = bob_bank_voice_rank
    bob_partyunit._bank_voice_hx_lowest_rank = bob_bank_voice_hx_lowest_rank
    print(f"{bob_text}")

    # WHEN
    x_dict = bob_partyunit.get_dict()

    # THEN
    print(f"{x_dict=}")
    assert x_dict != None
    assert x_dict == {
        "party_id": bob_text,
        "creditor_weight": bob_creditor_weight,
        "debtor_weight": bob_debtor_weight,
        "_creditor_live": bob_creditor_live,
        "_debtor_live": bob_debtor_live,
        "_bank_tax_paid": bob_bank_tax_paid,
        "_bank_tax_diff": bob_bank_tax_diff,
        "_bank_credit_score": bob_bank_credit_score,
        "_bank_voice_rank": bob_bank_voice_rank,
        "_bank_voice_hx_lowest_rank": bob_bank_voice_hx_lowest_rank,
        "depotlink_type": depotlink_type,
    }


def test_partyunits_get_from_json_SimpleExampleWorksWithIncompleteData():
    # GIVEN
    yao_text = "Yao"
    yao_creditor_weight = 13
    yao_debtor_weight = 17
    yao_creditor_live = False
    yao_debtor_live = True
    yao_bank_tax_paid = 0.55
    yao_bank_tax_diff = 0.66
    yao_depotlink_type = "assignment"
    yao_bank_credit_score = 7000
    yao_bank_voice_rank = 898
    yao_bank_voice_hx_lowest_rank = 740
    yao_json_dict = {
        yao_text: {
            "party_id": yao_text,
            "creditor_weight": yao_creditor_weight,
            "debtor_weight": yao_debtor_weight,
            "_creditor_live": yao_creditor_live,
            "_debtor_live": yao_debtor_live,
            "_bank_tax_paid": yao_bank_tax_paid,
            "_bank_tax_diff": yao_bank_tax_diff,
            "_bank_credit_score": yao_bank_credit_score,
            "_bank_voice_rank": yao_bank_voice_rank,
            "_bank_voice_hx_lowest_rank": yao_bank_voice_hx_lowest_rank,
            "depotlink_type": yao_depotlink_type,
        }
    }
    yao_json_text = x_get_json(dict_x=yao_json_dict)
    assert x_is_json(json_x=yao_json_text)

    # WHEN
    yao_obj_dict = partyunits_get_from_json(partyunits_json=yao_json_text)

    # THEN
    assert yao_obj_dict[yao_text] != None
    yao_partyunit = yao_obj_dict[yao_text]

    assert yao_partyunit.party_id == yao_text
    assert yao_partyunit.creditor_weight == yao_creditor_weight
    assert yao_partyunit.debtor_weight == yao_debtor_weight
    assert yao_partyunit._creditor_live == yao_creditor_live
    assert yao_partyunit._debtor_live == yao_debtor_live
    assert yao_partyunit._bank_tax_paid == yao_bank_tax_paid
    assert yao_partyunit._bank_tax_diff == yao_bank_tax_diff
    assert yao_partyunit._bank_credit_score == yao_bank_credit_score
    assert yao_partyunit._bank_voice_rank == yao_bank_voice_rank
    assert (
        yao_partyunit._bank_voice_hx_lowest_rank
        == yao_bank_voice_hx_lowest_rank
    )
    assert yao_partyunit.depotlink_type == yao_depotlink_type


def test_PartyUnit_meld_RaiseSameparty_idException():
    # GIVEN
    todd_text = "Todd"
    todd_party = partyunit_shop(party_id=todd_text)
    mery_text = "Merry"
    mery_party = partyunit_shop(party_id=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_party.meld(mery_party)
    assert (
        str(excinfo.value)
        == f"Meld fail PartyUnit='{todd_party.party_id}' not the same as PartyUnit='{mery_party.party_id}"
    )


def test_PartyUnit_meld_CorrectlySumsWeights():
    # GIVEN
    todd_text = "Todd"
    todd_party1 = partyunit_shop(
        party_id=todd_text, creditor_weight=7, debtor_weight=19
    )
    todd_party2 = partyunit_shop(party_id=todd_text, creditor_weight=5, debtor_weight=3)
    assert todd_party1.creditor_weight == 7
    assert todd_party1.debtor_weight == 19

    # WHEN
    todd_party1.meld(todd_party2)

    # THEN
    assert todd_party1.creditor_weight == 12
    assert todd_party1.debtor_weight == 22
