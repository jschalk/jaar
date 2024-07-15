from src._world.belieflink import (
    BeliefCore,
    BeliefID,
    belieflink_shop,
    BeliefLink,
    belieflink_get_from_dict,
    belieflinks_get_from_dict,
)
from pytest import raises as pytest_raises


def test_BeliefID_exists():
    bikers_belief_id = BeliefID(",bikers")
    assert bikers_belief_id != None
    assert str(type(bikers_belief_id)).find(".belieflink.BeliefID") > 0


def test_BeliefCore_exists():
    # GIVEN
    swim_text = ",swimmers"
    # WHEN
    swim_beliefcore = BeliefCore(belief_id=swim_text)
    # THEN
    assert swim_beliefcore != None
    assert swim_beliefcore.belief_id == swim_text


def test_BeliefLink_exists():
    # GIVEN
    swim_text = ",swim"

    # WHEN
    swim_belieflink = BeliefLink(belief_id=swim_text)

    # THEN
    assert swim_belieflink.belief_id == swim_text
    assert swim_belieflink.credor_weight == 1.0
    assert swim_belieflink.debtor_weight == 1.0
    assert swim_belieflink._credor_pool is None
    assert swim_belieflink._debtor_pool is None
    assert swim_belieflink._char_id is None


def test_belieflink_shop_ReturnsCorrectObj():
    # GIVEN
    swim_text = ",swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0
    yao_text = "Yao"

    # WHEN
    swim_belieflink = belieflink_shop(
        belief_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
    )

    # THEN
    assert swim_belieflink.credor_weight == swim_credor_weight
    assert swim_belieflink.debtor_weight == swim_debtor_weight
    assert swim_belieflink._credor_pool == 0
    assert swim_belieflink._debtor_pool == 0
    assert swim_belieflink._char_id is None


def test_belieflink_shop_ReturnsCorrectObjAttr_char_id():
    # GIVEN
    swim_text = ",swim"
    yao_text = "Yao"

    # WHEN
    swim_belieflink = belieflink_shop(swim_text, _char_id=yao_text)

    # THEN
    assert swim_belieflink._char_id == yao_text


# def test_BeliefLink_set_belief_id_RaisesErrorIf_belief_id_IsNotCharIDAndIsRoadNode():
#     # GIVEN
#     slash_text = "/"
#     # bob_text = f"Bob{slash_text}Texas"
#     bob_text = "Bob"
#     # swim_text = f"{slash_text}swim"
#     swim_text = ",swim"

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         belieflink_shop(swim_text, _char_id=bob_text, _road_delimiter=slash_text)
#     assert (
#         str(excinfo.value)
#         == f"'{swim_text}' needs to not be a RoadNode. Must contain delimiter: '{slash_text}'"
#     )


def test_BeliefLink_set_credor_weight_SetsAttr():
    # GIVEN
    swim_text = ",swim"
    old_credor_weight = 3.0
    swim_debtor_weight = 5.0
    swim_belieflink = belieflink_shop(swim_text, old_credor_weight, swim_debtor_weight)
    assert swim_belieflink.credor_weight == old_credor_weight
    assert swim_belieflink.debtor_weight == swim_debtor_weight

    # WHEN
    new_swim_credor_weight = 44
    swim_belieflink.set_credor_weight(new_swim_credor_weight)

    # THEN
    assert swim_belieflink.credor_weight == new_swim_credor_weight
    assert swim_belieflink.debtor_weight == swim_debtor_weight


def test_BeliefLink_set_credor_weight_SetsAttr():
    # GIVEN
    swim_text = ",swim"
    old_credor_weight = 3.0
    swim_debtor_weight = 5.0
    swim_belieflink = belieflink_shop(swim_text, old_credor_weight, swim_debtor_weight)
    assert swim_belieflink.credor_weight == old_credor_weight
    assert swim_belieflink.debtor_weight == swim_debtor_weight

    # WHEN
    swim_belieflink.set_credor_weight(None)

    # THEN
    assert swim_belieflink.credor_weight == old_credor_weight
    assert swim_belieflink.debtor_weight == swim_debtor_weight


def test_BeliefLink_set_debtor_weight_SetsAttr():
    # GIVEN
    swim_text = ",swim"
    swim_credor_weight = 3.0
    old_debtor_weight = 5.0
    swim_belieflink = belieflink_shop(swim_text, swim_credor_weight, old_debtor_weight)
    assert swim_belieflink.credor_weight == swim_credor_weight
    assert swim_belieflink.debtor_weight == old_debtor_weight

    # WHEN
    new_debtor_weight = 55
    swim_belieflink.set_debtor_weight(new_debtor_weight)

    # THEN
    assert swim_belieflink.credor_weight == swim_credor_weight
    assert swim_belieflink.debtor_weight == new_debtor_weight


def test_BeliefLink_set_debtor_weight_SetsAttr():
    # GIVEN
    swim_text = ",swim"
    swim_credor_weight = 3.0
    old_debtor_weight = 5.0
    swim_belieflink = belieflink_shop(swim_text, swim_credor_weight, old_debtor_weight)
    assert swim_belieflink.credor_weight == swim_credor_weight
    assert swim_belieflink.debtor_weight == old_debtor_weight

    # WHEN
    swim_belieflink.set_debtor_weight(None)

    # THEN
    assert swim_belieflink.credor_weight == swim_credor_weight
    assert swim_belieflink.debtor_weight == old_debtor_weight


def test_BeliefLink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    swim_text = ",swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0
    swim_belieflink = belieflink_shop(
        belief_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
    )

    print(f"{swim_belieflink}")

    # WHEN
    swim_dict = swim_belieflink.get_dict()

    # THEN
    assert swim_dict != None
    assert swim_dict == {
        "belief_id": swim_belieflink.belief_id,
        "credor_weight": swim_belieflink.credor_weight,
        "debtor_weight": swim_belieflink.debtor_weight,
    }


def test_belieflink_get_from_dict_ReturnsObj():
    # GIVEN
    swim_text = ",swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0
    yao_text = "Yao"
    before_swim_belieflink = belieflink_shop(
        belief_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
        _char_id=yao_text,
    )
    swim_belieflink_dict = before_swim_belieflink.get_dict()

    # WHEN
    after_swim_belieflink = belieflink_get_from_dict(swim_belieflink_dict, yao_text)

    # THEN
    assert before_swim_belieflink == after_swim_belieflink
    assert after_swim_belieflink.belief_id == swim_text


def test_belieflinks_get_from_dict_ReturnsObj():
    # GIVEN
    swim_text = ",swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0
    yao_text = "Yao"
    before_swim_belieflink = belieflink_shop(
        belief_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
        _char_id=yao_text,
    )
    before_swim_belieflinks_objs = {swim_text: before_swim_belieflink}
    swim_belieflinks_dict = {swim_text: before_swim_belieflink.get_dict()}

    # WHEN
    after_swim_belieflinks_objs = belieflinks_get_from_dict(
        swim_belieflinks_dict, yao_text
    )

    # THEN
    assert before_swim_belieflinks_objs == after_swim_belieflinks_objs
    assert after_swim_belieflinks_objs.get(swim_text) == before_swim_belieflink
