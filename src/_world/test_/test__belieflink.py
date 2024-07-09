from src._world.belieflink import (
    BeliefCore,
    BeliefID,
    belieflink_shop,
    BeliefLink,
    belieflink_get_from_dict,
    belieflinks_get_from_dict,
)


def test_BeliefID_exists():
    bikers_belief_id = BeliefID("bikers")
    assert bikers_belief_id != None
    assert str(type(bikers_belief_id)).find(".belieflink.BeliefID") > 0


def test_BeliefUnit_exists():
    # GIVEN
    swim_text = ",swimmers"
    # WHEN
    swim_beliefunit = BeliefCore(belief_id=swim_text)
    # THEN
    assert swim_beliefunit != None
    assert swim_beliefunit.belief_id == swim_text


def test_BeliefLink_exists():
    # GIVEN
    swim_text = "swim"

    # WHEN
    swim_belieflink = BeliefLink(belief_id=swim_text)

    # THEN
    assert swim_belieflink.belief_id == swim_text
    assert swim_belieflink.credor_weight == 1.0
    assert swim_belieflink.debtor_weight == 1.0


def test_belieflink_shop_ReturnsCorrectObj():
    # GIVEN
    swim_text = "swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0

    # WHEN
    swim_belieflink = belieflink_shop(
        belief_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
    )

    # THEN
    assert swim_belieflink.credor_weight == swim_credor_weight
    assert swim_belieflink.debtor_weight == swim_debtor_weight


def test_BeliefLink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    swim_text = "swim"
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
    swim_text = "swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0
    before_swim_belieflink = belieflink_shop(
        belief_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
    )
    swim_belieflink_dict = before_swim_belieflink.get_dict()

    # WHEN
    after_swim_belieflink = belieflink_get_from_dict(swim_belieflink_dict)

    # THEN
    assert before_swim_belieflink == after_swim_belieflink
    assert after_swim_belieflink.belief_id == swim_text


def test_belieflinks_get_from_dict_ReturnsObj():
    # GIVEN
    swim_text = "swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0
    before_swim_belieflink = belieflink_shop(
        belief_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
    )
    before_swim_belieflinks_objs = {swim_text: before_swim_belieflink}
    swim_belieflinks_dict = {swim_text: before_swim_belieflink.get_dict()}

    # WHEN
    after_swim_belieflinks_objs = belieflinks_get_from_dict(swim_belieflinks_dict)

    # THEN
    assert before_swim_belieflinks_objs == after_swim_belieflinks_objs
    assert after_swim_belieflinks_objs.get(swim_text) == before_swim_belieflink
