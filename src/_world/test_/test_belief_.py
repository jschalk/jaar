from src._world.beliefstory import (
    AwardLine,
    awardline_shop,
    BeliefBox,
    beliefbox_shop,
    AwardLink,
    awardlink_shop,
    awardlinks_get_from_json,
    awardheir_shop,
    BeliefStory,
    beliefstory_shop,
)
from src._road.road import (
    get_default_real_id_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from src._instrument.python import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_BeliefBox_exists():
    # GIVEN
    swim_text = ",swimmers"
    # WHEN
    swim_beliefbox = BeliefBox(belief_id=swim_text)
    # THEN
    assert swim_beliefbox != None
    assert swim_beliefbox.belief_id == swim_text
    assert swim_beliefbox._char_mirror is None
    assert swim_beliefbox._chars is None
    assert swim_beliefbox._world_cred is None
    assert swim_beliefbox._world_debt is None
    assert swim_beliefbox._world_agenda_cred is None
    assert swim_beliefbox._world_agenda_debt is None
    assert swim_beliefbox._road_delimiter is None


def test_beliefbox_shop_ReturnsCorrectObj():
    # GIVEN
    swim_text = ",swimmers"
    nation_road = create_road(root_label(), "nation-states")
    usa_road = create_road(nation_road, "USA")

    # WHEN
    swim_beliefbox = beliefbox_shop(belief_id=swim_text)

    # THEN
    print(f"{swim_text}")
    assert swim_beliefbox != None
    assert swim_beliefbox.belief_id != None
    assert swim_beliefbox.belief_id == swim_text
    assert swim_beliefbox._chars == {}
    assert swim_beliefbox._world_cred == 0
    assert swim_beliefbox._world_debt == 0
    assert swim_beliefbox._world_agenda_cred == 0
    assert swim_beliefbox._world_agenda_debt == 0
    assert swim_beliefbox._road_delimiter == default_road_delimiter_if_none()


def test_beliefbox_shop_ReturnsCorrectObj_road_delimiter():
    # GIVEN
    swim_text = "/swimmers"
    slash_text = "/"

    # WHEN
    swim_beliefbox = beliefbox_shop(belief_id=swim_text, _road_delimiter=slash_text)

    # THEN
    assert swim_beliefbox._road_delimiter == slash_text


def test_BeliefBox_set_belief_id_RaisesErrorIfParameterContains_road_delimiter_And_char_mirror_True():
    # GIVEN
    slash_text = "/"
    bob_text = f"Bob{slash_text}Texas"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        beliefbox_shop(bob_text, _char_mirror=True, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{bob_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_BeliefBox_set_belief_id_RaisesErrorIfParameterDoesNotContain_road_delimiter_char_mirror_False():
    # GIVEN
    comma_text = ","
    texas_text = f"Texas{comma_text}Arkansas"

    # WHEN / THEN
    slash_text = "/"
    with pytest_raises(Exception) as excinfo:
        beliefbox_shop(belief_id=texas_text, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{texas_text}' needs to not be a RoadNode. Must contain delimiter: '{slash_text}'"
    )


def test_BeliefBox_set_belief_id_SetsAttrCorrectly():
    # GIVEN
    swim_text = ",swimmers"
    swim_belief = beliefbox_shop(belief_id=swim_text)
    assert swim_belief.belief_id == swim_text

    # WHEN
    water_text = ",water people"
    swim_belief.set_belief_id(belief_id=water_text)

    # THEN
    assert swim_belief.belief_id == water_text


def test_BeliefBox_reset_bud_share_SetsAttrCorrectly():
    # GIVEN
    maria_belief_id = "maria"
    maria_beliefbox = beliefbox_shop(maria_belief_id, _char_mirror=True)
    maria_beliefbox._world_cred = 0.33
    maria_beliefbox._world_debt = 0.44
    maria_beliefbox._world_agenda_cred = 0.13
    maria_beliefbox._world_agenda_debt = 0.23
    print(f"{maria_beliefbox}")
    assert maria_beliefbox._world_cred == 0.33
    assert maria_beliefbox._world_debt == 0.44
    assert maria_beliefbox._world_agenda_cred == 0.13
    assert maria_beliefbox._world_agenda_debt == 0.23

    # WHEN
    maria_beliefbox.reset_world_cred_debt()

    # THEN
    assert maria_beliefbox._world_cred == 0
    assert maria_beliefbox._world_debt == 0
    assert maria_beliefbox._world_agenda_cred == 0
    assert maria_beliefbox._world_agenda_debt == 0


def test_AwardLink_exists():
    # GIVEN
    bikers_text = "bikers"

    # WHEN
    bikers_awardlink = AwardLink(belief_id=bikers_text)

    # THEN
    assert bikers_awardlink.belief_id == bikers_text
    assert bikers_awardlink.credor_weight == 1.0
    assert bikers_awardlink.debtor_weight == 1.0


def test_awardlink_shop_ReturnsCorrectObj():
    # GIVEN
    bikers_text = "bikers"
    bikers_credor_weight = 3.0
    bikers_debtor_weight = 5.0

    # WHEN
    bikers_awardlink = awardlink_shop(
        belief_id=bikers_text,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debtor_weight,
    )

    # THEN
    assert bikers_awardlink.credor_weight == bikers_credor_weight
    assert bikers_awardlink.debtor_weight == bikers_debtor_weight


def test_AwardHeir_set_bud_share_CorrectlySetsAttr():
    # GIVEN
    bikers_text = "bikers"
    bikers_credor_weight = 3.0
    bikers_debt_weight = 6.0
    awardlinks_sum_credor_weight = 60
    awardlinks_sum_debtor_weight = 60
    idea_bud_share = 1
    belief_heir_x = awardheir_shop(
        belief_id=bikers_text,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debt_weight,
    )

    # WHEN
    belief_heir_x.set_world_cred_debt(
        idea_bud_share=idea_bud_share,
        awardheirs_credor_weight_sum=awardlinks_sum_credor_weight,
        awardheirs_debtor_weight_sum=awardlinks_sum_debtor_weight,
    )

    # THEN
    assert belief_heir_x._world_cred == 0.05
    assert belief_heir_x._world_debt == 0.1


def test_AwardLink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    bikers_text = "bikers"
    bikers_credor_weight = 3.0
    bikers_debtor_weight = 5.0
    bikers_awardlink = awardlink_shop(
        belief_id=bikers_text,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debtor_weight,
    )

    print(f"{bikers_awardlink}")

    # WHEN
    biker_dict = bikers_awardlink.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "belief_id": bikers_awardlink.belief_id,
        "credor_weight": bikers_awardlink.credor_weight,
        "debtor_weight": bikers_awardlink.debtor_weight,
    }


def test_awardlinks_get_from_JSON_ReturnsCorrectObj_SimpleExample():
    # GIVEN
    teacher_text = "teachers"
    teacher_awardlink = awardlink_shop(
        belief_id=teacher_text, credor_weight=103, debtor_weight=155
    )
    teacher_dict = teacher_awardlink.get_dict()
    awardlinks_dict = {teacher_awardlink.belief_id: teacher_dict}

    teachers_json = get_json_from_dict(dict_x=awardlinks_dict)
    assert teachers_json != None
    assert x_is_json(json_x=teachers_json)

    # WHEN
    awardlinks_obj_dict = awardlinks_get_from_json(awardlinks_json=teachers_json)

    # THEN
    assert awardlinks_obj_dict != None
    teachers_obj_check_dict = {teacher_awardlink.belief_id: teacher_awardlink}
    print(f"    {awardlinks_obj_dict=}")
    print(f"{teachers_obj_check_dict=}")
    assert awardlinks_obj_dict == teachers_obj_check_dict


def test_AwardLine_exists():
    # GIVEN
    bikers_text = "bikers"
    bikers_world_cred = 0.33
    bikers_world_debt = 0.55

    # WHEN
    bikers_awardline = AwardLine(
        belief_id=bikers_text,
        _world_cred=bikers_world_cred,
        _world_debt=bikers_world_debt,
    )

    # THEN
    assert bikers_awardline.belief_id == bikers_text
    assert bikers_awardline._world_cred == bikers_world_cred
    assert bikers_awardline._world_debt == bikers_world_debt


def test_awardline_shop_ReturnsCorrectObj_exists():
    # GIVEN
    bikers_text = "bikers"
    bikers_text = bikers_text
    bikers_world_cred = 0.33
    bikers_world_debt = 0.55

    # WHEN
    biker_awardline = awardline_shop(
        belief_id=bikers_text,
        _world_cred=bikers_world_cred,
        _world_debt=bikers_world_debt,
    )

    assert biker_awardline != None
    assert biker_awardline.belief_id == bikers_text
    assert biker_awardline._world_cred == bikers_world_cred
    assert biker_awardline._world_debt == bikers_world_debt


def test_AwardLine_add_world_cred_debt_CorrectlyModifiesAttr():
    # GIVEN
    bikers_text = "bikers"
    bikers_awardline = awardline_shop(
        belief_id=bikers_text, _world_cred=0.33, _world_debt=0.55
    )
    assert bikers_awardline.belief_id == bikers_text
    assert bikers_awardline._world_cred == 0.33
    assert bikers_awardline._world_debt == 0.55

    # WHEN
    bikers_awardline.add_world_cred_debt(world_cred=0.11, world_debt=0.2)

    # THEN
    assert bikers_awardline._world_cred == 0.44
    assert bikers_awardline._world_debt == 0.75


def test_BeliefStory_exists():
    # GIVEN
    swim_text = ",swimmers"
    # WHEN
    swim_beliefstory = BeliefStory(belief_id=swim_text)
    # THEN
    assert swim_beliefstory != None
    assert swim_beliefstory.belief_id == swim_text
    assert swim_beliefstory._belieflinks is None
    assert swim_beliefstory._world_cred is None
    assert swim_beliefstory._world_debt is None
    assert swim_beliefstory._world_agenda_cred is None
    assert swim_beliefstory._world_agenda_debt is None
    assert swim_beliefstory._credor_pool is None
    assert swim_beliefstory._debtor_pool is None
    assert swim_beliefstory._road_delimiter is None


def test_beliefstory_shop_ReturnsCorrectObj():
    # GIVEN
    swim_text = ",swimmers"
    nation_road = create_road(root_label(), "nation-states")
    usa_road = create_road(nation_road, "USA")

    # WHEN
    swim_beliefstory = beliefstory_shop(belief_id=swim_text)

    # THEN
    print(f"{swim_text}")
    assert swim_beliefstory != None
    assert swim_beliefstory.belief_id != None
    assert swim_beliefstory.belief_id == swim_text
    assert swim_beliefstory._belieflinks == {}
    assert swim_beliefstory._world_cred == 0
    assert swim_beliefstory._world_debt == 0
    assert swim_beliefstory._world_agenda_cred == 0
    assert swim_beliefstory._world_agenda_debt == 0
    assert swim_beliefstory._credor_pool == 0
    assert swim_beliefstory._debtor_pool == 0
    assert swim_beliefstory._road_delimiter == default_road_delimiter_if_none()


def test_beliefstory_shop_ReturnsCorrectObj_road_delimiter():
    # GIVEN
    swim_text = "/swimmers"
    slash_text = "/"

    # WHEN
    swim_beliefstory = beliefstory_shop(belief_id=swim_text, _road_delimiter=slash_text)

    # THEN
    assert swim_beliefstory._road_delimiter == slash_text


# def test_BeliefStory_set_belief_id_RaisesErrorIfParameterContains_road_delimiter_And_char_mirror_True():
#     # GIVEN
#     slash_text = "/"
#     bob_text = f"Bob{slash_text}Texas"

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         beliefstory_shop(bob_text, _char_mirror=True, _road_delimiter=slash_text)
#     assert (
#         str(excinfo.value)
#         == f"'{bob_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
#     )
