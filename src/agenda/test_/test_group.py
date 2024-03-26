from src.agenda.party import PartyID, partylink_shop
from src.agenda.group import (
    BalanceLine,
    balanceline_shop,
    GroupUnit,
    groupunit_shop,
    GroupID,
    BalanceLink,
    balancelink_shop,
    balancelinks_get_from_json,
    balanceheir_shop,
    get_from_json as groupunits_get_from_json,
)
from src._road.road import (
    get_default_world_id_roadnode as root_label,
    create_road,
    validate_roadnode,
    default_road_delimiter_if_none,
)
from src.instrument.python import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_GroupID_exists():
    bikers_group_id = GroupID("bikers")
    assert bikers_group_id != None
    assert str(type(bikers_group_id)).find(".group.GroupID") > 0


def test_GroupUnit_exists():
    # GIVEN
    swim_text = ",swimmers"
    # WHEN
    swim_groupunit = GroupUnit(group_id=swim_text)
    # THEN
    assert swim_groupunit != None
    assert swim_groupunit.group_id == swim_text
    assert swim_groupunit._party_mirror is None
    assert swim_groupunit._partys is None
    assert swim_groupunit._agenda_credit is None
    assert swim_groupunit._agenda_debt is None
    assert swim_groupunit._agenda_intent_credit is None
    assert swim_groupunit._agenda_intent_debt is None
    assert swim_groupunit._treasury_partylinks is None
    assert swim_groupunit._road_delimiter is None


def test_groupunit_shop_ReturnsCorrectObj():
    # GIVEN
    swim_text = ",swimmers"
    nation_road = create_road(root_label(), "nation-states")
    usa_road = create_road(nation_road, "USA")

    # WHEN
    swim_groupunit = groupunit_shop(group_id=swim_text, _treasury_partylinks=usa_road)

    # THEN
    print(f"{swim_text}")
    assert swim_groupunit != None
    assert swim_groupunit.group_id != None
    assert swim_groupunit.group_id == swim_text
    assert swim_groupunit._agenda_credit == 0
    assert swim_groupunit._agenda_debt == 0
    assert swim_groupunit._agenda_intent_credit == 0
    assert swim_groupunit._agenda_intent_debt == 0
    assert swim_groupunit._treasury_partylinks == usa_road
    assert swim_groupunit._road_delimiter == default_road_delimiter_if_none()


def test_groupunit_shop_ReturnsCorrectObj_road_delimiter():
    # GIVEN
    swim_text = "/swimmers"
    slash_text = "/"

    # WHEN
    swim_groupunit = groupunit_shop(group_id=swim_text, _road_delimiter=slash_text)

    # THEN
    assert swim_groupunit._road_delimiter == slash_text


def test_GroupUnit_set_group_id_RaisesErrorIfParameterContains_road_delimiter_And_party_mirror_True():
    # GIVEN
    slash_text = "/"
    bob_text = f"Bob{slash_text}Texas"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        groupunit_shop(bob_text, _party_mirror=True, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{bob_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_GroupUnit_set_group_id_RaisesErrorIfParameterDoesNotContain_road_delimiter_party_mirror_False():
    # GIVEN
    comma_text = ","
    texas_text = f"Texas{comma_text}Arkansas"

    # WHEN / THEN
    slash_text = "/"
    with pytest_raises(Exception) as excinfo:
        groupunit_shop(group_id=texas_text, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{texas_text}' needs to not be a RoadNode. Must contain delimiter: '{slash_text}'"
    )


def test_GroupUnit_set_group_id_SetsAttrCorrectly():
    # GIVEN
    swim_text = ",swimmers"
    swim_group = groupunit_shop(group_id=swim_text)
    assert swim_group.group_id == swim_text

    # WHEN
    water_text = ",water people"
    swim_group.set_group_id(group_id=water_text)

    # THEN
    assert swim_group.group_id == water_text


def test_GroupUnit_set_attr_SetsAttrCorrectly():
    # GIVEN
    swim_text = ",swimmers"
    swim_group = groupunit_shop(group_id=swim_text)
    assert swim_group._treasury_partylinks is None

    # WHEN
    sports_road = create_road(root_label(), "sports")
    water_road = create_road(sports_road, "water")
    swim_group.set_attr(_treasury_partylinks=water_road)

    # THEN
    assert swim_group._treasury_partylinks == water_road


def test_groupunit_shop_WhenSinglePartyCorrectlyDeletes_treasury_partylinks():
    # GIVEN
    swim_text = ",swimmers"
    nation_road = create_road(root_label(), "nation-states")
    usa_road = create_road(nation_road, "USA")

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        swimmers_group = groupunit_shop(
            group_id=swim_text,
            _party_mirror=True,
            _treasury_partylinks=usa_road,
        )
    assert (
        str(excinfo.value)
        == f"_treasury_partylinks cannot be '{usa_road}' for a single_party GroupUnit. It must have no value."
    )


def test_GroupUnit_set_partylink_CorrectlySetsAttr():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_party = partylink_shop(party_id=todd_text, creditor_weight=13, debtor_weight=7)
    mery_party = partylink_shop(party_id=mery_text, creditor_weight=23, debtor_weight=5)

    swimmers_group = groupunit_shop(group_id=",swimmers", _partys={})

    # WHEN
    swimmers_group.set_partylink(todd_party)
    swimmers_group.set_partylink(mery_party)

    # THEN
    swimmers_partys = {todd_party.party_id: todd_party, mery_party.party_id: mery_party}
    assert swimmers_group._partys == swimmers_partys


def test_GroupUnit_get_partylink_ReturnsCorrectObj():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    swimmers_group = groupunit_shop(group_id=",swimmers", _partys={})
    swimmers_group.set_partylink(partylink_shop(todd_text, 13, 7))
    swimmers_group.set_partylink(partylink_shop(mery_text, 23, 5))

    # WHEN / THEN
    assert swimmers_group.get_partylink(todd_text) != None
    assert swimmers_group.get_partylink(mery_text) != None
    assert swimmers_group.get_partylink("todd") is None


def test_GroupUnit_edit_partylink_CorrectlySetsAttr():
    # GIVEN
    todd_text = "Todd"
    old_todd_creditor_weight = 13
    todd_debtor_weight = 7
    swimmers_group = groupunit_shop(group_id=",swimmers")
    swimmers_group.set_partylink(
        partylink_shop(todd_text, old_todd_creditor_weight, todd_debtor_weight)
    )
    todd_partylink = swimmers_group.get_partylink(todd_text)
    assert todd_partylink.creditor_weight == old_todd_creditor_weight

    # WHEN
    new_todd_creditor_weight = 17
    swimmers_group.edit_partylink(
        party_id=todd_text, creditor_weight=new_todd_creditor_weight
    )

    # THEN
    assert todd_partylink.creditor_weight == new_todd_creditor_weight


def test_partylink_exists_ReturnsCorrectObj():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    swimmers_group = groupunit_shop(group_id=",swimmers", _partys={})
    swimmers_group.set_partylink(partylink_shop(todd_text, 13, 7))
    swimmers_group.set_partylink(partylink_shop(mery_text, 23, 5))

    # WHEN / THEN
    assert swimmers_group.partylink_exists(todd_text)
    assert swimmers_group.partylink_exists(mery_text)
    assert swimmers_group.partylink_exists("todd") == False


def test_GroupUnit_del_partylink_SetsAttrCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_party = partylink_shop(party_id=todd_text)
    mery_party = partylink_shop(party_id=mery_text)
    swimmers_partys = {todd_party.party_id: todd_party, mery_party.party_id: mery_party}
    swimmers_group = groupunit_shop(group_id=",swimmers", _partys={})
    swimmers_group.set_partylink(todd_party)
    swimmers_group.set_partylink(mery_party)
    assert len(swimmers_group._partys) == 2
    assert swimmers_group._partys == swimmers_partys

    # WHEN
    swimmers_group.del_partylink(party_id=todd_text)

    # THEN
    assert len(swimmers_group._partys) == 1
    assert swimmers_group._partys.get(todd_text) is None


def test_GroupUnit_clear_partylinks_SetsAttrCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_party = partylink_shop(party_id=todd_text)
    mery_party = partylink_shop(party_id=mery_text)
    swimmers_partys = {todd_party.party_id: todd_party, mery_party.party_id: mery_party}
    swimmers_group = groupunit_shop(group_id=",swimmers", _partys={})
    swimmers_group.set_partylink(todd_party)
    swimmers_group.set_partylink(mery_party)
    assert len(swimmers_group._partys) == 2
    assert swimmers_group._partys == swimmers_partys

    # WHEN
    swimmers_group.clear_partylinks()

    # THEN
    assert len(swimmers_group._partys) == 0
    assert swimmers_group._partys.get(todd_text) is None


def test_GroupUnit_reset_agenda_importance_SetsAttrCorrectly():
    # GIVEN
    maria_group_id = "maria"
    maria_groupunit = groupunit_shop(group_id=maria_group_id, _party_mirror=True)
    maria_groupunit._agenda_credit = 0.33
    maria_groupunit._agenda_debt = 0.44
    maria_groupunit._agenda_intent_credit = 0.13
    maria_groupunit._agenda_intent_debt = 0.23
    print(f"{maria_groupunit}")
    assert maria_groupunit._agenda_credit == 0.33
    assert maria_groupunit._agenda_debt == 0.44
    assert maria_groupunit._agenda_intent_credit == 0.13
    assert maria_groupunit._agenda_intent_debt == 0.23

    # WHEN
    maria_groupunit.reset_agenda_credit_debt()

    # THEN
    assert maria_groupunit._agenda_credit == 0
    assert maria_groupunit._agenda_debt == 0
    assert maria_groupunit._agenda_intent_credit == 0
    assert maria_groupunit._agenda_intent_debt == 0


def test_GroupUnit_reset_agenda_importance_reset_partylinks():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_party = partylink_shop(
        party_id=todd_text,
        _agenda_credit=0.13,
        _agenda_debt=0.7,
        _agenda_intent_credit=0.53,
        _agenda_intent_debt=0.77,
    )
    mery_party = partylink_shop(
        party_id=mery_text,
        _agenda_credit=0.23,
        _agenda_debt=0.5,
        _agenda_intent_credit=0.54,
        _agenda_intent_debt=0.57,
    )
    bikers_partys = {todd_party.party_id: todd_party, mery_party.party_id: mery_party}
    bikers_group_id = ",bikers"
    bikers_groupunit = groupunit_shop(group_id=bikers_group_id)
    bikers_groupunit._agenda_credit = (0.33,)
    bikers_groupunit._agenda_debt = (0.44,)
    bikers_groupunit._agenda_intent_credit = (0.1,)
    bikers_groupunit._agenda_intent_debt = (0.2,)
    bikers_groupunit.set_partylink(partylink=todd_party)
    bikers_groupunit.set_partylink(partylink=mery_party)
    print(f"{bikers_groupunit}")
    biker_partylink_todd = bikers_groupunit._partys.get(todd_text)
    assert biker_partylink_todd._agenda_credit == 0.13
    assert biker_partylink_todd._agenda_debt == 0.7
    assert biker_partylink_todd._agenda_intent_credit == 0.53
    assert biker_partylink_todd._agenda_intent_debt == 0.77

    biker_partylink_mery = bikers_groupunit._partys.get(mery_text)
    assert biker_partylink_mery._agenda_credit == 0.23
    assert biker_partylink_mery._agenda_debt == 0.5
    assert biker_partylink_mery._agenda_intent_credit == 0.54
    assert biker_partylink_mery._agenda_intent_debt == 0.57

    # WHEN
    bikers_groupunit.reset_agenda_credit_debt()

    # THEN
    assert biker_partylink_todd._agenda_credit == 0
    assert biker_partylink_todd._agenda_debt == 0
    assert biker_partylink_todd._agenda_intent_credit == 0
    assert biker_partylink_todd._agenda_intent_debt == 0
    assert biker_partylink_mery._agenda_credit == 0
    assert biker_partylink_mery._agenda_debt == 0
    assert biker_partylink_mery._agenda_intent_credit == 0
    assert biker_partylink_mery._agenda_intent_debt == 0


def test_partylink_merge_ReturnsCorrectObj_BaseScenario():
    # GIVEN
    todd_party = partylink_shop(party_id="Todd")
    merry_party = partylink_shop(party_id="Merry")
    bikers_group_id = ",bikers"
    bikers_group = groupunit_shop(group_id=bikers_group_id, _partys={})
    bikers_group.set_partylink(partylink=todd_party)
    bikers_group.set_partylink(partylink=merry_party)

    x2_group = groupunit_shop(group_id=bikers_group_id, _partys={})

    # WHEN
    bikers_group.merge(other_group=x2_group)
    print(f"{bikers_group.group_id=} {x2_group.group_id=}")

    # THEN
    assert len(bikers_group._partys) == 2


def test_partylink_merge_ReturnsCorrectObj_GainScenario():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_party = partylink_shop(party_id=todd_text, creditor_weight=13, debtor_weight=7)
    mery_party = partylink_shop(party_id=mery_text, creditor_weight=23, debtor_weight=5)
    bikers_group_id = ",bikers"
    bikers_group = groupunit_shop(group_id=bikers_group_id, _partys={})

    x2_group = groupunit_shop(group_id=bikers_group_id, _partys={})
    x2_group.set_partylink(partylink=todd_party)
    x2_group.set_partylink(partylink=mery_party)

    # WHEN
    bikers_group.merge(other_group=x2_group)

    # THEN
    assert len(bikers_group._partys) == 2
    assert bikers_group._partys.get(todd_text) != None


def test_GroupUnit_merge_RaiseSameparty_idException():
    # GIVEN
    todd_text = "Todd"
    todd_group = groupunit_shop(group_id=todd_text, _party_mirror=True)
    mery_text = "Merry"
    mery_group = groupunit_shop(group_id=mery_text, _party_mirror=True)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_group.merge(mery_group)
    assert (
        str(excinfo.value)
        == f"merge fail GroupUnit {todd_group.group_id} .group_id='{todd_group.group_id}' not the same as .group_id='{mery_group.group_id}"
    )


def test_GroupUnit_get_dict_ReturnsDictWithAttrsCorrectlySet():
    # GIVEN
    todd_text = "Todd"
    todd_group = groupunit_shop(group_id=todd_text, _party_mirror=True)
    sue_text = "Sue"
    todd_group.set_partylink(partylink_shop(party_id=sue_text))
    x_treasury_partylinks = 44
    todd_group.set_attr(x_treasury_partylinks)

    assert todd_group.group_id == todd_text
    assert todd_group._party_mirror
    assert len(todd_group._partys) == 1
    assert todd_group._treasury_partylinks == x_treasury_partylinks

    # WHEN
    todd_dict = todd_group.get_dict()

    # THEN
    assert todd_dict["group_id"] == todd_text
    assert todd_dict["_party_mirror"]
    assert len(todd_dict["_partys"]) == 1
    assert todd_dict["_treasury_partylinks"] == x_treasury_partylinks


def test_GroupUnit_get_dict_ReturnsDictWithAttrsCorrectlyEmpty():
    # GIVEN
    swim_text = ",Swimmers"
    swim_group = groupunit_shop(group_id=swim_text)
    assert swim_group._party_mirror is False
    assert swim_group._partys == {}
    assert swim_group._treasury_partylinks is None

    # WHEN
    swim_dict = swim_group.get_dict()

    # THEN
    assert swim_dict.get("_party_mirror") is None
    assert swim_dict.get("_partys") is None
    assert swim_dict.get("_treasury_partylinks") is None


def test_GroupUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    swim_text = ",swimmers"

    # WHEN
    swimmers_group = groupunit_shop(group_id=swim_text)
    print(f"{swim_text}")

    # THEN
    ee_dict = swimmers_group.get_dict()
    assert ee_dict != None
    # assert ee_dict == {"group_id": swimmers}
    assert ee_dict == {"group_id": swim_text}

    # GIVEN
    sue_text = "Marie"
    marie_partylink = partylink_shop(
        party_id=sue_text, creditor_weight=29, debtor_weight=3
    )
    partylinks_dict = {marie_partylink.party_id: marie_partylink}
    marie_json_dict = {
        sue_text: {
            "party_id": sue_text,
            "creditor_weight": 29,
            "debtor_weight": 3,
        }
    }

    teacher_text = ",teachers"
    swim_road = "swim"
    teachers_group = groupunit_shop(
        group_id=teacher_text,
        _partys=partylinks_dict,
        _treasury_partylinks=swim_road,
    )

    # WHEN
    teachers_dict = teachers_group.get_dict()

    # THEN
    print(f"{marie_json_dict=}")
    assert teachers_dict == {
        "group_id": teacher_text,
        "_partys": marie_json_dict,
        "_treasury_partylinks": swim_road,
    }


def test_GroupUnit_get_from_JSON_ReturnsCorrectObj_SimpleExample():
    # GIVEN
    sue_text = "Sue"
    marie_partylink = partylink_shop(
        party_id=sue_text, creditor_weight=29, debtor_weight=3
    )
    partylinks_dict = {marie_partylink.party_id: marie_partylink}

    teacher_text = ",teachers"
    swim_road = "swim"
    teacher_group = groupunit_shop(
        group_id=teacher_text,
        _partys=partylinks_dict,
        _treasury_partylinks=swim_road,
    )
    teacher_dict = teacher_group.get_dict()
    _treasury_partylinks_text = "_treasury_partylinks"
    print(f"{teacher_dict.get(_treasury_partylinks_text)=}")
    groups_dict = {teacher_text: teacher_dict}

    teachers_json = get_json_from_dict(dict_x=groups_dict)
    print(f"{teachers_json.find(_treasury_partylinks_text)=}")
    assert teachers_json != None
    assert x_is_json(json_x=teachers_json)

    # WHEN
    groupunits_obj_dict = groupunits_get_from_json(groupunits_json=teachers_json)

    # THEN
    assert groupunits_obj_dict != None
    teachers_obj_check_dict = {teacher_group.group_id: teacher_group}
    print(f"    {groupunits_obj_dict=}")
    treasury_partylinks_text = "_treasury_partylinks"
    print(f"{teachers_obj_check_dict.get(treasury_partylinks_text)=}")
    print(f"{teachers_obj_check_dict=}")
    assert groupunits_obj_dict == teachers_obj_check_dict


def test_BalanceLink_exists():
    # GIVEN
    bikers_group_id = GroupID("bikers")

    # WHEN
    bikers_balancelink = BalanceLink(group_id=bikers_group_id)

    # THEN
    assert bikers_balancelink.group_id == bikers_group_id
    assert bikers_balancelink.creditor_weight == 1.0
    assert bikers_balancelink.debtor_weight == 1.0


def test_balancelink_shop_ReturnsCorrectObj():
    # GIVEN
    bikers_group_id = GroupID("bikers")
    bikers_creditor_weight = 3.0
    bikers_debtor_weight = 5.0

    # WHEN
    bikers_balancelink = balancelink_shop(
        group_id=bikers_group_id,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debtor_weight,
    )

    # THEN
    assert bikers_balancelink.creditor_weight == bikers_creditor_weight
    assert bikers_balancelink.debtor_weight == bikers_debtor_weight


def test_BalanceHeir_set_agenda_importance_CorrectlySetsAttr():
    # GIVEN
    bikers_group_id = GroupID("bikers")
    bikers_creditor_weight = 3.0
    bikers_debt_weight = 6.0
    balancelinks_sum_creditor_weight = 60
    balancelinks_sum_debtor_weight = 60
    idea_agenda_importance = 1
    group_heir_x = balanceheir_shop(
        group_id=bikers_group_id,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debt_weight,
    )

    # WHEN
    group_heir_x.set_agenda_credit_debt(
        idea_agenda_importance=idea_agenda_importance,
        balanceheirs_creditor_weight_sum=balancelinks_sum_creditor_weight,
        balanceheirs_debtor_weight_sum=balancelinks_sum_debtor_weight,
    )

    # THEN
    assert group_heir_x._agenda_credit == 0.05
    assert group_heir_x._agenda_debt == 0.1


def test_BalanceLink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    bikers_group_id = GroupID("bikers")
    bikers_creditor_weight = 3.0
    bikers_debtor_weight = 5.0
    bikers_link = balancelink_shop(
        group_id=bikers_group_id,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debtor_weight,
    )

    print(f"{bikers_link}")

    # WHEN
    biker_dict = bikers_link.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "group_id": bikers_link.group_id,
        "creditor_weight": bikers_link.creditor_weight,
        "debtor_weight": bikers_link.debtor_weight,
    }


def test_balancelinks_get_from_JSON_ReturnsCorrectObj_SimpleExample():
    # GIVEN
    teacher_text = "teachers"
    teacher_balancelink = balancelink_shop(
        group_id=teacher_text, creditor_weight=103, debtor_weight=155
    )
    teacher_dict = teacher_balancelink.get_dict()
    balancelinks_dict = {teacher_balancelink.group_id: teacher_dict}

    teachers_json = get_json_from_dict(dict_x=balancelinks_dict)
    assert teachers_json != None
    assert x_is_json(json_x=teachers_json)

    # WHEN
    balancelinks_obj_dict = balancelinks_get_from_json(balancelinks_json=teachers_json)

    # THEN
    assert balancelinks_obj_dict != None
    teachers_obj_check_dict = {teacher_balancelink.group_id: teacher_balancelink}
    print(f"    {balancelinks_obj_dict=}")
    print(f"{teachers_obj_check_dict=}")
    assert balancelinks_obj_dict == teachers_obj_check_dict


def test_BalanceLine_exists():
    # GIVEN
    bikers_group_id = GroupID("bikers")
    bikers_agenda_credit = 0.33
    bikers_agenda_debt = 0.55

    # WHEN
    bikers_balanceline = BalanceLine(
        group_id=bikers_group_id,
        _agenda_credit=bikers_agenda_credit,
        _agenda_debt=bikers_agenda_debt,
    )

    # THEN
    assert bikers_balanceline.group_id == bikers_group_id
    assert bikers_balanceline._agenda_credit == bikers_agenda_credit
    assert bikers_balanceline._agenda_debt == bikers_agenda_debt


def test_balanceline_shop_ReturnsCorrectObj_exists():
    # GIVEN
    bikers_group_id = GroupID("bikers")
    bikers_group_id = bikers_group_id
    bikers_agenda_credit = 0.33
    bikers_agenda_debt = 0.55

    # WHEN
    biker_balanceline = balanceline_shop(
        group_id=bikers_group_id,
        _agenda_credit=bikers_agenda_credit,
        _agenda_debt=bikers_agenda_debt,
    )

    assert biker_balanceline != None
    assert biker_balanceline.group_id == bikers_group_id
    assert biker_balanceline._agenda_credit == bikers_agenda_credit
    assert biker_balanceline._agenda_debt == bikers_agenda_debt


def test_BalanceLine_add_agenda_credit_debt_CorrectlyChangesAttr():
    # GIVEN
    bikers_group_id = GroupID("bikers")
    bikers_balanceline = balanceline_shop(
        group_id=bikers_group_id, _agenda_credit=0.33, _agenda_debt=0.55
    )
    assert bikers_balanceline.group_id == bikers_group_id
    assert bikers_balanceline._agenda_credit == 0.33
    assert bikers_balanceline._agenda_debt == 0.55

    # WHEN
    bikers_balanceline.add_agenda_credit_debt(agenda_credit=0.11, agenda_debt=0.2)

    # THEN
    assert bikers_balanceline._agenda_credit == 0.44
    assert bikers_balanceline._agenda_debt == 0.75
