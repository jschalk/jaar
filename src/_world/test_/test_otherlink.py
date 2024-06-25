from src._world.other import (
    OtherID,
    otherlink_shop,
    otherlinks_get_from_json,
)
from src._instrument.python import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_OtherLink_exists():
    # GIVEN
    bikers_other_id = OtherID("Yao")

    # WHEN
    x_otherlink = otherlink_shop(other_id=bikers_other_id)

    # THEN
    assert x_otherlink.other_id == bikers_other_id
    assert x_otherlink.credor_weight == 1.0
    assert x_otherlink.debtor_weight == 1.0

    # WHEN
    bikers_credor_weight = 3.0
    bikers_debtor_weight = 5.0
    x_otherlink = otherlink_shop(
        other_id=bikers_other_id,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debtor_weight,
        _world_cred=0.7,
        _world_debt=0.51,
        _world_agenda_cred=0.66,
        _world_agenda_debt=0.55,
    )

    # THEN
    assert x_otherlink.credor_weight == bikers_credor_weight
    assert x_otherlink.debtor_weight == bikers_debtor_weight
    assert x_otherlink._world_cred != None
    assert x_otherlink._world_cred == 0.7
    assert x_otherlink._world_debt == 0.51
    assert x_otherlink._world_agenda_cred == 0.66
    assert x_otherlink._world_agenda_debt == 0.55


def test_otherlink_shop_set_world_cred_debt_SetsAttrCorrectly():
    # GIVEN
    bikers_other_id = OtherID("Yao")
    bikers_credor_weight = 3.0
    otherlinks_sum_credor_weight = 60
    belief_world_cred = 0.5
    belief_world_agenda_cred = 0.98

    bikers_debtor_weight = 13.0
    otherlinks_sum_debtor_weight = 26.0
    belief_world_debt = 0.9
    belief_world_agenda_debt = 0.5151

    x_otherlink = otherlink_shop(
        other_id=bikers_other_id,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debtor_weight,
    )
    assert x_otherlink._world_cred is None
    assert x_otherlink._world_debt is None
    assert x_otherlink._world_agenda_cred is None
    assert x_otherlink._world_agenda_debt is None

    # WHEN
    x_otherlink.set_world_cred_debt(
        otherlinks_credor_weight_sum=otherlinks_sum_credor_weight,
        otherlinks_debtor_weight_sum=otherlinks_sum_debtor_weight,
        belief_world_cred=belief_world_cred,
        belief_world_debt=belief_world_debt,
        belief_world_agenda_cred=belief_world_agenda_cred,
        belief_world_agenda_debt=belief_world_agenda_debt,
    )

    # THEN
    assert x_otherlink._world_cred == 0.025
    assert x_otherlink._world_debt == 0.45
    assert x_otherlink._world_agenda_cred == 0.049
    assert x_otherlink._world_agenda_debt == 0.25755


def test_otherlink_shop_reset_world_cred_debt():
    # GIVEN
    biker_other_id = "maria"
    biker_other = otherlink_shop(
        other_id=biker_other_id, _world_cred=0.04, _world_debt=0.7
    )
    print(f"{biker_other}")

    assert biker_other._world_cred != None
    assert biker_other._world_debt != None

    # WHEN
    biker_other.reset_world_cred_debt()

    # THEN
    assert biker_other._world_cred == 0
    assert biker_other._world_debt == 0


def test_otherlink_shop_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    str_other_id = "Yao"
    biker_other_id = OtherID(str_other_id)
    biker_other_link = otherlink_shop(
        other_id=biker_other_id, credor_weight=12, debtor_weight=19
    )
    print(f"{biker_other_link}")

    # WHEN
    biker_dict = biker_other_link.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "other_id": biker_other_id,
        "credor_weight": 12,
        "debtor_weight": 19,
    }


def test_otherlink_get_from_JSON_ReturnsCorrectObj_SimpleExample():
    # GIVEN
    yao_text = "Yao"
    yao_json_dict = {
        yao_text: {"other_id": yao_text, "credor_weight": 12, "debtor_weight": 19}
    }
    yao_json_text = get_json_from_dict(dict_x=yao_json_dict)
    assert x_is_json(json_x=yao_json_text)

    # WHEN
    yao_obj_dict = otherlinks_get_from_json(otherlinks_json=yao_json_text)

    # THEN
    assert yao_obj_dict != None

    yao_other_id = OtherID(yao_text)
    yao_otherlink = otherlink_shop(
        other_id=yao_other_id, credor_weight=12, debtor_weight=19
    )
    otherlinks_dict = {yao_otherlink.other_id: yao_otherlink}
    assert yao_obj_dict == otherlinks_dict


def test_otherlink_meld_RaiseEqualother_idException():
    # GIVEN
    todd_text = "Todd"
    todd_other = otherlink_shop(other_id=todd_text)
    mery_text = "Merry"
    mery_other = otherlink_shop(other_id=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_other.meld(mery_other)
    assert (
        str(excinfo.value)
        == f"Meld fail OtherLink='{todd_other.other_id}' not the equal as OtherLink='{mery_other.other_id}"
    )


def test_otherlink_meld_CorrectlySumsWeights():
    # GIVEN
    todd_text = "Todd"
    todd_other1 = otherlink_shop(other_id=todd_text, credor_weight=12, debtor_weight=19)
    todd_other2 = otherlink_shop(other_id=todd_text, credor_weight=33, debtor_weight=3)
    assert todd_other1.credor_weight == 12
    assert todd_other1.debtor_weight == 19

    # WHEN
    todd_other1.meld(todd_other2)

    # THEN
    assert todd_other1.credor_weight == 45
    assert todd_other1.debtor_weight == 22