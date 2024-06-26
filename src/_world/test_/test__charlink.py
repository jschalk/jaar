from src._world.char import charlink_shop, charlinks_get_from_json
from src._instrument.python import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_CharLink_exists():
    # GIVEN
    yao_text = "Yao"

    # WHEN
    yao_charlink = charlink_shop(yao_text)

    # THEN
    assert yao_charlink.char_id == yao_text
    assert yao_charlink.credor_weight == 1.0
    assert yao_charlink.debtor_weight == 1.0

    # WHEN
    bikers_credor_weight = 3.0
    bikers_debtor_weight = 5.0
    yao_charlink = charlink_shop(
        char_id=yao_text,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debtor_weight,
        _world_cred=0.7,
        _world_debt=0.51,
        _world_agenda_cred=0.66,
        _world_agenda_debt=0.55,
    )

    # THEN
    assert yao_charlink.credor_weight == bikers_credor_weight
    assert yao_charlink.debtor_weight == bikers_debtor_weight
    assert yao_charlink._world_cred != None
    assert yao_charlink._world_cred == 0.7
    assert yao_charlink._world_debt == 0.51
    assert yao_charlink._world_agenda_cred == 0.66
    assert yao_charlink._world_agenda_debt == 0.55


def test_charlink_shop_set_world_cred_debt_SetsAttrCorrectly():
    # GIVEN
    yao_text = "Yao"
    bikers_credor_weight = 3.0
    charlinks_sum_credor_weight = 60
    belief_world_cred = 0.5
    belief_world_agenda_cred = 0.98

    bikers_debtor_weight = 13.0
    charlinks_sum_debtor_weight = 26.0
    belief_world_debt = 0.9
    belief_world_agenda_debt = 0.5151

    yao_charlink = charlink_shop(
        char_id=yao_text,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debtor_weight,
    )
    assert yao_charlink._world_cred is None
    assert yao_charlink._world_debt is None
    assert yao_charlink._world_agenda_cred is None
    assert yao_charlink._world_agenda_debt is None

    # WHEN
    yao_charlink.set_world_cred_debt(
        charlinks_credor_weight_sum=charlinks_sum_credor_weight,
        charlinks_debtor_weight_sum=charlinks_sum_debtor_weight,
        belief_world_cred=belief_world_cred,
        belief_world_debt=belief_world_debt,
        belief_world_agenda_cred=belief_world_agenda_cred,
        belief_world_agenda_debt=belief_world_agenda_debt,
    )

    # THEN
    assert yao_charlink._world_cred == 0.025
    assert yao_charlink._world_debt == 0.45
    assert yao_charlink._world_agenda_cred == 0.049
    assert yao_charlink._world_agenda_debt == 0.25755


def test_charlink_shop_reset_world_cred_debt():
    # GIVEN
    yao_text = "Yao"
    yao_charlink = charlink_shop(yao_text, _world_cred=0.04, _world_debt=0.7)
    print(f"{yao_text=}")

    assert yao_charlink._world_cred != None
    assert yao_charlink._world_debt != None

    # WHEN
    yao_charlink.reset_world_cred_debt()

    # THEN
    assert yao_charlink._world_cred == 0
    assert yao_charlink._world_debt == 0


def test_CharLink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    yao_text = "Yao"
    yao_charlink = charlink_shop(yao_text, credor_weight=12, debtor_weight=19)
    print(f"{yao_charlink}")

    # WHEN
    biker_dict = yao_charlink.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "char_id": yao_text,
        "credor_weight": 12,
        "debtor_weight": 19,
    }


def test_CharLink_get_from_JSON_ReturnsCorrectObj_SimpleExample():
    # GIVEN
    yao_text = "Yao"
    yao_json_dict = {
        yao_text: {"char_id": yao_text, "credor_weight": 12, "debtor_weight": 19}
    }
    yao_json_text = get_json_from_dict(dict_x=yao_json_dict)
    assert x_is_json(json_x=yao_json_text)

    # WHEN
    yao_obj_dict = charlinks_get_from_json(charlinks_json=yao_json_text)

    # THEN
    assert yao_obj_dict != None

    yao_charlink = charlink_shop(yao_text, credor_weight=12, debtor_weight=19)
    charlinks_dict = {yao_charlink.char_id: yao_charlink}
    assert yao_obj_dict == charlinks_dict


def test_CharLink_meld_RaiseEqualchar_idException():
    # GIVEN
    sue_text = "Sue"
    sue_charlink = charlink_shop(sue_text)
    yao_text = "Yao"
    yao_charlink = charlink_shop(yao_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_charlink.meld(yao_charlink)
    assert (
        str(excinfo.value)
        == f"Meld fail CharLink='{sue_charlink.char_id}' not the equal as CharLink='{yao_charlink.char_id}"
    )


def test_CharLink_meld_CorrectlySumsWeights():
    # GIVEN
    yao_text = "Yao"
    yao_charlink1 = charlink_shop(yao_text, credor_weight=12, debtor_weight=19)
    yao_charlink2 = charlink_shop(yao_text, credor_weight=33, debtor_weight=3)
    assert yao_charlink1.credor_weight == 12
    assert yao_charlink1.debtor_weight == 19

    # WHEN
    yao_charlink1.meld(yao_charlink2)

    # THEN
    assert yao_charlink1.credor_weight == 45
    assert yao_charlink1.debtor_weight == 22
