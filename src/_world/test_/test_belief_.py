from src._world.char import charlink_shop
from src._world.beliefunit import (
    FiscalLine,
    fiscalline_shop,
    BeliefUnit,
    beliefunit_shop,
    BeliefID,
    FiscalLink,
    fiscallink_shop,
    fiscallinks_get_from_json,
    fiscalheir_shop,
    get_from_json as beliefunits_get_from_json,
    get_beliefunit_from_dict,
    get_beliefunits_from_dict,
)
from src._road.road import (
    get_default_real_id_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from src._instrument.python import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_BeliefUnit_exists():
    # GIVEN
    swim_text = ",swimmers"
    # WHEN
    swim_beliefunit = BeliefUnit(belief_id=swim_text)
    # THEN
    assert swim_beliefunit != None
    assert swim_beliefunit.belief_id == swim_text
    assert swim_beliefunit._char_mirror is None
    assert swim_beliefunit._chars is None
    assert swim_beliefunit._world_cred is None
    assert swim_beliefunit._world_debt is None
    assert swim_beliefunit._world_agenda_cred is None
    assert swim_beliefunit._world_agenda_debt is None
    assert swim_beliefunit._road_delimiter is None


def test_beliefunit_shop_ReturnsCorrectObj():
    # GIVEN
    swim_text = ",swimmers"
    nation_road = create_road(root_label(), "nation-states")
    usa_road = create_road(nation_road, "USA")

    # WHEN
    swim_beliefunit = beliefunit_shop(belief_id=swim_text)

    # THEN
    print(f"{swim_text}")
    assert swim_beliefunit != None
    assert swim_beliefunit.belief_id != None
    assert swim_beliefunit.belief_id == swim_text
    assert swim_beliefunit._world_cred == 0
    assert swim_beliefunit._world_debt == 0
    assert swim_beliefunit._world_agenda_cred == 0
    assert swim_beliefunit._world_agenda_debt == 0
    assert swim_beliefunit._road_delimiter == default_road_delimiter_if_none()


def test_beliefunit_shop_ReturnsCorrectObj_road_delimiter():
    # GIVEN
    swim_text = "/swimmers"
    slash_text = "/"

    # WHEN
    swim_beliefunit = beliefunit_shop(belief_id=swim_text, _road_delimiter=slash_text)

    # THEN
    assert swim_beliefunit._road_delimiter == slash_text


def test_BeliefUnit_set_belief_id_RaisesErrorIfParameterContains_road_delimiter_And_char_mirror_True():
    # GIVEN
    slash_text = "/"
    bob_text = f"Bob{slash_text}Texas"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        beliefunit_shop(bob_text, _char_mirror=True, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{bob_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_BeliefUnit_set_belief_id_RaisesErrorIfParameterDoesNotContain_road_delimiter_char_mirror_False():
    # GIVEN
    comma_text = ","
    texas_text = f"Texas{comma_text}Arkansas"

    # WHEN / THEN
    slash_text = "/"
    with pytest_raises(Exception) as excinfo:
        beliefunit_shop(belief_id=texas_text, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{texas_text}' needs to not be a RoadNode. Must contain delimiter: '{slash_text}'"
    )


def test_BeliefUnit_set_belief_id_SetsAttrCorrectly():
    # GIVEN
    swim_text = ",swimmers"
    swim_belief = beliefunit_shop(belief_id=swim_text)
    assert swim_belief.belief_id == swim_text

    # WHEN
    water_text = ",water people"
    swim_belief.set_belief_id(belief_id=water_text)

    # THEN
    assert swim_belief.belief_id == water_text


def test_BeliefUnit_reset_world_importance_SetsAttrCorrectly():
    # GIVEN
    maria_belief_id = "maria"
    maria_beliefunit = beliefunit_shop(belief_id=maria_belief_id, _char_mirror=True)
    maria_beliefunit._world_cred = 0.33
    maria_beliefunit._world_debt = 0.44
    maria_beliefunit._world_agenda_cred = 0.13
    maria_beliefunit._world_agenda_debt = 0.23
    print(f"{maria_beliefunit}")
    assert maria_beliefunit._world_cred == 0.33
    assert maria_beliefunit._world_debt == 0.44
    assert maria_beliefunit._world_agenda_cred == 0.13
    assert maria_beliefunit._world_agenda_debt == 0.23

    # WHEN
    maria_beliefunit.reset_world_cred_debt()

    # THEN
    assert maria_beliefunit._world_cred == 0
    assert maria_beliefunit._world_debt == 0
    assert maria_beliefunit._world_agenda_cred == 0
    assert maria_beliefunit._world_agenda_debt == 0


def test_BeliefUnit_meld_RaiseEqualchar_idException():
    # GIVEN
    sue_text = "Sue"
    sue_belief = beliefunit_shop(belief_id=sue_text, _char_mirror=True)
    yao_text = "Yao"
    yao_belief = beliefunit_shop(belief_id=yao_text, _char_mirror=True)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_belief.meld(yao_belief)
    assert (
        str(excinfo.value)
        == f"Meld fail BeliefUnit {sue_belief.belief_id} .belief_id='{sue_belief.belief_id}' not the equal as .belief_id='{yao_belief.belief_id}"
    )


def test_BeliefUnit_get_dict_ReturnsDictWithAttrsCorrectlySet():
    # GIVEN
    yao_text = "Yao"
    yao_belief = beliefunit_shop(belief_id=yao_text, _char_mirror=True)
    sue_text = "Sue"
    yao_belief.set_charlink(charlink_shop(char_id=sue_text))

    assert yao_belief.belief_id == yao_text
    assert yao_belief._char_mirror
    assert len(yao_belief._chars) == 1

    # WHEN
    yao_dict = yao_belief.get_dict()

    # THEN
    assert yao_dict["belief_id"] == yao_text
    assert yao_dict["_char_mirror"]
    assert len(yao_dict["_chars"]) == 1


def test_BeliefUnit_get_dict_ReturnsDictWithAttrsCorrectlyEmpty():
    # GIVEN
    swim_text = ",Swimmers"
    swim_belief = beliefunit_shop(belief_id=swim_text)
    assert swim_belief._char_mirror is False
    assert swim_belief._chars == {}

    # WHEN
    swim_dict = swim_belief.get_dict()

    # THEN
    assert swim_dict.get("_char_mirror") is None
    assert swim_dict.get("_chars") is None


def test_BeliefUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    swim_text = ",swimmers"

    # WHEN
    swimmers_belief = beliefunit_shop(belief_id=swim_text)
    print(f"{swim_text}")

    # THEN
    ee_dict = swimmers_belief.get_dict()
    assert ee_dict != None
    # assert ee_dict == {"belief_id": swimmers}
    assert ee_dict == {"belief_id": swim_text}

    # GIVEN
    sue_text = "Marie"
    marie_charlink = charlink_shop(char_id=sue_text, credor_weight=29, debtor_weight=3)
    charlinks_dict = {marie_charlink.char_id: marie_charlink}
    marie_json_dict = {
        sue_text: {
            "char_id": sue_text,
            "credor_weight": 29,
            "debtor_weight": 3,
        }
    }

    teacher_text = ",teachers"
    swim_road = "swim"
    teachers_belief = beliefunit_shop(
        belief_id=teacher_text,
        _chars=charlinks_dict,
    )

    # WHEN
    teachers_dict = teachers_belief.get_dict()

    # THEN
    print(f"{marie_json_dict=}")
    assert teachers_dict == {
        "belief_id": teacher_text,
        "_chars": marie_json_dict,
    }


def test_beliefunit_get_from_dict_CorrectlyReturnsBeliefUnitWith_road_delimiter():
    # GIVEN
    slash_text = "/"
    teacher_text = f"{slash_text}teachers"
    before_teacher_beliefunit = beliefunit_shop(
        teacher_text, _road_delimiter=slash_text
    )
    teacher_dict = before_teacher_beliefunit.get_dict()

    # WHEN
    print(f"{teacher_dict=}")
    after_teacher_beliefunit = get_beliefunit_from_dict(teacher_dict, slash_text)

    # THEN
    assert after_teacher_beliefunit == before_teacher_beliefunit


def test_BeliefUnit_get_from_JSON_ReturnsCorrectObj_SimpleExample():
    # GIVEN
    sue_text = "Sue"
    marie_charlink = charlink_shop(char_id=sue_text, credor_weight=29, debtor_weight=3)
    charlinks_dict = {marie_charlink.char_id: marie_charlink}

    teacher_text = ",teachers"
    swim_road = "swim"
    teacher_belief = beliefunit_shop(belief_id=teacher_text, _chars=charlinks_dict)
    teacher_dict = teacher_belief.get_dict()
    beliefs_dict = {teacher_text: teacher_dict}

    teachers_json = get_json_from_dict(dict_x=beliefs_dict)
    assert teachers_json != None
    assert x_is_json(json_x=teachers_json)

    # WHEN
    beliefunits_obj_dict = beliefunits_get_from_json(beliefunits_json=teachers_json)

    # THEN
    assert beliefunits_obj_dict != None
    teachers_obj_check_dict = {teacher_belief.belief_id: teacher_belief}
    print(f"    {beliefunits_obj_dict=}")
    print(f"{teachers_obj_check_dict=}")
    assert beliefunits_obj_dict == teachers_obj_check_dict


def test_BeliefUnit_get_beliefunits_from_dict_ReturnsCorrectObjWith_road_delimiter():
    # GIVEN
    slash_text = "/"
    teacher_text = f"{slash_text}teachers"
    teacher_beliefunit = beliefunit_shop(teacher_text, _road_delimiter=slash_text)
    teacher_dict = teacher_beliefunit.get_dict()

    teacher_dict = teacher_beliefunit.get_dict()
    beliefunits_dict = {teacher_text: teacher_dict}

    # WHEN
    x_beliefunits = get_beliefunits_from_dict(beliefunits_dict, slash_text)

    # THEN
    assert x_beliefunits != None
    teachers_obj_check_dict = {teacher_beliefunit.belief_id: teacher_beliefunit}
    print(f"{teachers_obj_check_dict=}")
    assert x_beliefunits == teachers_obj_check_dict


def test_FiscalLink_exists():
    # GIVEN
    bikers_belief_id = BeliefID("bikers")

    # WHEN
    bikers_fiscallink = FiscalLink(belief_id=bikers_belief_id)

    # THEN
    assert bikers_fiscallink.belief_id == bikers_belief_id
    assert bikers_fiscallink.credor_weight == 1.0
    assert bikers_fiscallink.debtor_weight == 1.0


def test_fiscallink_shop_ReturnsCorrectObj():
    # GIVEN
    bikers_belief_id = BeliefID("bikers")
    bikers_credor_weight = 3.0
    bikers_debtor_weight = 5.0

    # WHEN
    bikers_fiscallink = fiscallink_shop(
        belief_id=bikers_belief_id,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debtor_weight,
    )

    # THEN
    assert bikers_fiscallink.credor_weight == bikers_credor_weight
    assert bikers_fiscallink.debtor_weight == bikers_debtor_weight


def test_FiscalHeir_set_world_importance_CorrectlySetsAttr():
    # GIVEN
    bikers_belief_id = BeliefID("bikers")
    bikers_credor_weight = 3.0
    bikers_debt_weight = 6.0
    fiscallinks_sum_credor_weight = 60
    fiscallinks_sum_debtor_weight = 60
    idea_world_importance = 1
    belief_heir_x = fiscalheir_shop(
        belief_id=bikers_belief_id,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debt_weight,
    )

    # WHEN
    belief_heir_x.set_world_cred_debt(
        idea_world_importance=idea_world_importance,
        fiscalheirs_credor_weight_sum=fiscallinks_sum_credor_weight,
        fiscalheirs_debtor_weight_sum=fiscallinks_sum_debtor_weight,
    )

    # THEN
    assert belief_heir_x._world_cred == 0.05
    assert belief_heir_x._world_debt == 0.1


def test_FiscalLink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    bikers_belief_id = BeliefID("bikers")
    bikers_credor_weight = 3.0
    bikers_debtor_weight = 5.0
    bikers_fiscallink = fiscallink_shop(
        belief_id=bikers_belief_id,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debtor_weight,
    )

    print(f"{bikers_fiscallink}")

    # WHEN
    biker_dict = bikers_fiscallink.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "belief_id": bikers_fiscallink.belief_id,
        "credor_weight": bikers_fiscallink.credor_weight,
        "debtor_weight": bikers_fiscallink.debtor_weight,
    }


def test_fiscallinks_get_from_JSON_ReturnsCorrectObj_SimpleExample():
    # GIVEN
    teacher_text = "teachers"
    teacher_fiscallink = fiscallink_shop(
        belief_id=teacher_text, credor_weight=103, debtor_weight=155
    )
    teacher_dict = teacher_fiscallink.get_dict()
    fiscallinks_dict = {teacher_fiscallink.belief_id: teacher_dict}

    teachers_json = get_json_from_dict(dict_x=fiscallinks_dict)
    assert teachers_json != None
    assert x_is_json(json_x=teachers_json)

    # WHEN
    fiscallinks_obj_dict = fiscallinks_get_from_json(fiscallinks_json=teachers_json)

    # THEN
    assert fiscallinks_obj_dict != None
    teachers_obj_check_dict = {teacher_fiscallink.belief_id: teacher_fiscallink}
    print(f"    {fiscallinks_obj_dict=}")
    print(f"{teachers_obj_check_dict=}")
    assert fiscallinks_obj_dict == teachers_obj_check_dict


def test_FiscalLine_exists():
    # GIVEN
    bikers_belief_id = BeliefID("bikers")
    bikers_world_cred = 0.33
    bikers_world_debt = 0.55

    # WHEN
    bikers_fiscalline = FiscalLine(
        belief_id=bikers_belief_id,
        _world_cred=bikers_world_cred,
        _world_debt=bikers_world_debt,
    )

    # THEN
    assert bikers_fiscalline.belief_id == bikers_belief_id
    assert bikers_fiscalline._world_cred == bikers_world_cred
    assert bikers_fiscalline._world_debt == bikers_world_debt


def test_fiscalline_shop_ReturnsCorrectObj_exists():
    # GIVEN
    bikers_belief_id = BeliefID("bikers")
    bikers_belief_id = bikers_belief_id
    bikers_world_cred = 0.33
    bikers_world_debt = 0.55

    # WHEN
    biker_fiscalline = fiscalline_shop(
        belief_id=bikers_belief_id,
        _world_cred=bikers_world_cred,
        _world_debt=bikers_world_debt,
    )

    assert biker_fiscalline != None
    assert biker_fiscalline.belief_id == bikers_belief_id
    assert biker_fiscalline._world_cred == bikers_world_cred
    assert biker_fiscalline._world_debt == bikers_world_debt


def test_FiscalLine_add_world_cred_debt_CorrectlyModifiesAttr():
    # GIVEN
    bikers_belief_id = BeliefID("bikers")
    bikers_fiscalline = fiscalline_shop(
        belief_id=bikers_belief_id, _world_cred=0.33, _world_debt=0.55
    )
    assert bikers_fiscalline.belief_id == bikers_belief_id
    assert bikers_fiscalline._world_cred == 0.33
    assert bikers_fiscalline._world_debt == 0.55

    # WHEN
    bikers_fiscalline.add_world_cred_debt(world_cred=0.11, world_debt=0.2)

    # THEN
    assert bikers_fiscalline._world_cred == 0.44
    assert bikers_fiscalline._world_debt == 0.75
