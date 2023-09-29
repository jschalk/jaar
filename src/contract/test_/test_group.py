from src.contract.party import PartyName, partylink_shop
from src.contract.group import (
    Groupline,
    groupunit_shop,
    GroupName,
    grouplink_shop,
    grouplinks_get_from_json,
    groupheir_shop,
    get_from_json as groupunits_get_from_json,
)
from src.contract.road import get_default_economy_root_label as root_label
from src.contract.x_func import x_is_json, x_get_json
from pytest import raises as pytest_raises


def test_groupName_exists():
    bikers_name = GroupName("bikers")
    assert bikers_name != None
    assert str(type(bikers_name)).find(".group.GroupName") > 0


def test_groupunit_exists():
    # GIVEN
    swimmers = "swimmers"
    usa_road = f"{root_label()},nation-states,USA"

    # WHEN
    swimmers_group = groupunit_shop(
        name=swimmers,
        _contract_credit=0.33,
        _contract_debt=0.44,
        _contract_agenda_credit=0.66,
        _contract_agenda_debt=0.77,
        _partylinks_set_by_economy_road=usa_road,
    )

    # THEN
    print(f"{swimmers}")
    assert swimmers_group != None
    assert swimmers_group.name != None
    assert swimmers_group.name == swimmers
    assert swimmers_group._contract_credit != None
    assert swimmers_group._contract_debt != None
    assert swimmers_group._contract_agenda_credit != None
    assert swimmers_group._contract_agenda_debt != None
    assert swimmers_group._partylinks_set_by_economy_road == usa_road


def test_groupunit_set_name_WorksCorrectly():
    # GIVEN
    swim_text = "swimmers"
    swim_group = groupunit_shop(name=swim_text)
    assert swim_group.name == swim_text

    # WHEN
    water_text = "water people"
    swim_group.set_name(name=water_text)

    # THEN
    assert swim_group.name == water_text


def test_groupunit_set_attr_WorksCorrectly():
    # GIVEN
    swim_text = "swimmers"
    swim_group = groupunit_shop(name=swim_text)
    assert swim_group._partylinks_set_by_economy_road is None

    # WHEN
    water_road = f"{root_label()},sports,water"
    swim_group.set_attr(_partylinks_set_by_economy_road=water_road)

    # THEN
    assert swim_group._partylinks_set_by_economy_road == water_road


def test_groupunit_shop_WhenSinglePartyCorrectlyRemoves_partylinks_set_by_economy_road():
    # GIVEN
    swimmers = "swimmers"
    usa_road = f"{root_label()},nation-states,USA"

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        swimmers_group = groupunit_shop(
            name=swimmers,
            _single_party=True,
            _partylinks_set_by_economy_road=usa_road,
        )
    assert (
        str(excinfo.value)
        == f"_partylinks_set_by_economy_road cannot be '{usa_road}' for a single_party GroupUnit. It must have no value."
    )


def test_groupunit_set_partylink_worksCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_party = partylink_shop(name=todd_text, creditor_weight=13, debtor_weight=7)
    mery_party = partylink_shop(name=mery_text, creditor_weight=23, debtor_weight=5)

    swimmers_group = groupunit_shop(name="swimmers", _partys={})

    # WHEN
    swimmers_group.set_partylink(todd_party)
    swimmers_group.set_partylink(mery_party)

    # THEN
    swimmers_partys = {todd_party.name: todd_party, mery_party.name: mery_party}
    assert swimmers_group._partys == swimmers_partys


def test_groupunit_del_partylink_worksCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_party = partylink_shop(name=todd_text)
    mery_party = partylink_shop(name=mery_text)
    swimmers_partys = {todd_party.name: todd_party, mery_party.name: mery_party}
    swimmers_group = groupunit_shop(name="swimmers", _partys={})
    swimmers_group.set_partylink(todd_party)
    swimmers_group.set_partylink(mery_party)
    assert len(swimmers_group._partys) == 2
    assert swimmers_group._partys == swimmers_partys

    # WHEN
    swimmers_group.del_partylink(name=todd_text)

    # THEN
    assert len(swimmers_group._partys) == 1
    assert swimmers_group._partys.get(todd_text) is None


def test_groupunit_clear_partylinks_worksCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_party = partylink_shop(name=todd_text)
    mery_party = partylink_shop(name=mery_text)
    swimmers_partys = {todd_party.name: todd_party, mery_party.name: mery_party}
    swimmers_group = groupunit_shop(name="swimmers", _partys={})
    swimmers_group.set_partylink(todd_party)
    swimmers_group.set_partylink(mery_party)
    assert len(swimmers_group._partys) == 2
    assert swimmers_group._partys == swimmers_partys

    # WHEN
    swimmers_group.clear_partylinks()

    # THEN
    assert len(swimmers_group._partys) == 0
    assert swimmers_group._partys.get(todd_text) is None


def test_Groupunit_reset_contract_importance_WorkCorrectly():
    # GIVEN
    maria_name = "maria"
    maria_group = groupunit_shop(
        name=maria_name,
        _contract_credit=0.33,
        _contract_debt=0.44,
        _contract_agenda_credit=0.13,
        _contract_agenda_debt=0.23,
    )
    print(f"{maria_group}")
    assert maria_group._contract_credit == 0.33
    assert maria_group._contract_debt == 0.44
    assert maria_group._contract_agenda_credit == 0.13
    assert maria_group._contract_agenda_debt == 0.23

    # WHEN
    maria_group.reset_contract_credit_debt()

    # THEN
    assert maria_group._contract_credit == 0
    assert maria_group._contract_debt == 0
    assert maria_group._contract_agenda_credit == 0
    assert maria_group._contract_agenda_debt == 0


def test_Groupunit_reset_contract_importance_reset_partylinks():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_party = partylink_shop(
        name=todd_text,
        _contract_credit=0.13,
        _contract_debt=0.7,
        _contract_agenda_credit=0.53,
        _contract_agenda_debt=0.77,
    )
    mery_party = partylink_shop(
        name=mery_text,
        _contract_credit=0.23,
        _contract_debt=0.5,
        _contract_agenda_credit=0.54,
        _contract_agenda_debt=0.57,
    )
    bikers_partys = {todd_party.name: todd_party, mery_party.name: mery_party}
    bikers_name = "bikers"
    bikers_group = groupunit_shop(
        name=bikers_name,
        _partys={},
        _contract_credit=0.33,
        _contract_debt=0.44,
        _contract_agenda_credit=0.1,
        _contract_agenda_debt=0.2,
    )
    bikers_group.set_partylink(partylink=todd_party)
    bikers_group.set_partylink(partylink=mery_party)
    print(f"{bikers_group}")
    biker_partylink_todd = bikers_group._partys.get(todd_text)
    assert biker_partylink_todd._contract_credit == 0.13
    assert biker_partylink_todd._contract_debt == 0.7
    assert biker_partylink_todd._contract_agenda_credit == 0.53
    assert biker_partylink_todd._contract_agenda_debt == 0.77

    biker_partylink_mery = bikers_group._partys.get(mery_text)
    assert biker_partylink_mery._contract_credit == 0.23
    assert biker_partylink_mery._contract_debt == 0.5
    assert biker_partylink_mery._contract_agenda_credit == 0.54
    assert biker_partylink_mery._contract_agenda_debt == 0.57

    # WHEN
    bikers_group.reset_contract_credit_debt()

    # THEN
    assert biker_partylink_todd._contract_credit == 0
    assert biker_partylink_todd._contract_debt == 0
    assert biker_partylink_todd._contract_agenda_credit == 0
    assert biker_partylink_todd._contract_agenda_debt == 0
    assert biker_partylink_mery._contract_credit == 0
    assert biker_partylink_mery._contract_debt == 0
    assert biker_partylink_mery._contract_agenda_credit == 0
    assert biker_partylink_mery._contract_agenda_debt == 0


def test_GroupUnit_partylink_meld_BaseScenarioWorks():
    # GIVEN
    todd_party = partylink_shop(name="Todd")
    merry_party = partylink_shop(name="Merry")
    x1_name = "bikers"
    x1_group = groupunit_shop(name=x1_name, _partys={})
    x1_group.set_partylink(partylink=todd_party)
    x1_group.set_partylink(partylink=merry_party)

    x2_group = groupunit_shop(name=x1_name, _partys={})

    # WHEN
    x1_group.meld(other_group=x2_group)
    print(f"{x1_group.name=} {x2_group.name=}")

    # THEN
    assert len(x1_group._partys) == 2


def test_GroupUnit_partylink_meld_GainScenarioWorks():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_party = partylink_shop(name=todd_text, creditor_weight=13, debtor_weight=7)
    mery_party = partylink_shop(name=mery_text, creditor_weight=23, debtor_weight=5)
    x1_name = "bikers"
    x1_group = groupunit_shop(name=x1_name, _partys={})

    x2_group = groupunit_shop(name=x1_name, _partys={})
    x2_group.set_partylink(partylink=todd_party)
    x2_group.set_partylink(partylink=mery_party)

    # WHEN
    x1_group.meld(other_group=x2_group)

    # THEN
    assert len(x1_group._partys) == 2
    assert x1_group._partys.get(todd_text) != None


def test_GroupUnit_meld_RaiseSameNameException():
    # GIVEN
    todd_text = "Todd"
    todd_group = groupunit_shop(name=todd_text)
    mery_text = "Merry"
    mery_group = groupunit_shop(name=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_group.meld(mery_group)
    assert (
        str(excinfo.value)
        == f"Meld fail GroupUnit {todd_group.name} .name='{todd_group.name}' not the same as .name='{mery_group.name}"
    )


def test_GroupUnit_meld_RaiseSameUIDException():
    # GIVEN
    todd_text = "Todd"
    todd3_group = groupunit_shop(name=todd_text, uid=3)
    todd5_group = groupunit_shop(name=todd_text, uid=5)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd3_group.meld(todd5_group)
    assert (
        str(excinfo.value)
        == f"Meld fail GroupUnit {todd3_group.name} .uid='{todd3_group.uid}' not the same as .uid='{todd5_group.uid}"
    )


def test_groupUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    swimmers = "swimmers"

    # WHEN
    swimmers_group = groupunit_shop(name=swimmers)
    print(f"{swimmers}")

    # THEN
    ee_dict = swimmers_group.get_dict()
    assert ee_dict != None
    # assert ee_dict == {"name": swimmers, "uid": 2}
    assert ee_dict == {
        "name": swimmers,
        "uid": None,
        "single_party_id": None,
        "_single_party": False,
        "_partys": {},
        "_partylinks_set_by_economy_road": None,
    }

    # GIVEN
    str_name = "Marie"
    marie_name = PartyName(str_name)
    marie_partylink = partylink_shop(
        name=marie_name, creditor_weight=29, debtor_weight=3
    )
    partylinks_dict = {marie_partylink.name: marie_partylink}
    marie_json_dict = {
        marie_name: {"name": marie_name, "creditor_weight": 29, "debtor_weight": 3}
    }

    str_teacher = "teachers"
    swim_road = "swim"
    teachers_group = groupunit_shop(
        name=str_teacher,
        _partys=partylinks_dict,
        _partylinks_set_by_economy_road=swim_road,
    )

    # WHEN
    teachers_dict = teachers_group.get_dict()

    # THEN
    print(f"{marie_json_dict=}")
    assert teachers_dict == {
        "name": str_teacher,
        "uid": None,
        "single_party_id": None,
        "_single_party": False,
        "_partys": marie_json_dict,
        "_partylinks_set_by_economy_road": swim_road,
    }


def test_groupunit_get_from_JSON_SimpleExampleWorks():
    # GIVEN
    str_name = "Marie"
    marie_name = PartyName(str_name)
    marie_partylink = partylink_shop(
        name=marie_name, creditor_weight=29, debtor_weight=3
    )
    partylinks_dict = {marie_partylink.name: marie_partylink}

    str_teacher = "teachers"
    swim_road = "swim"
    teacher_group = groupunit_shop(
        name=str_teacher,
        _partys=partylinks_dict,
        _partylinks_set_by_economy_road=swim_road,
    )
    teacher_dict = teacher_group.get_dict()
    _partylinks_set_by_economy_road_text = "_partylinks_set_by_economy_road"
    print(f"{teacher_dict.get(_partylinks_set_by_economy_road_text)=}")
    groups_dict = {"teachers": teacher_dict}

    teachers_json = x_get_json(dict_x=groups_dict)
    print(f"{teachers_json.find(_partylinks_set_by_economy_road_text)=}")
    assert teachers_json != None
    assert x_is_json(json_x=teachers_json)

    # WHEN
    groupunits_obj_dict = groupunits_get_from_json(groupunits_json=teachers_json)

    # THEN
    assert groupunits_obj_dict != None
    teachers_obj_check_dict = {teacher_group.name: teacher_group}
    print(f"    {groupunits_obj_dict=}")
    partylinks_set_by_economy_road_text = "_partylinks_set_by_economy_road"
    print(f"{teachers_obj_check_dict.get(partylinks_set_by_economy_road_text)=}")
    print(f"{teachers_obj_check_dict=}")
    assert groupunits_obj_dict == teachers_obj_check_dict


def test_brankLink_exists():
    # GIVEN
    bikers_name = GroupName("bikers")

    # WHEN
    group_link_x = grouplink_shop(name=bikers_name)

    # THEN
    assert group_link_x.name == bikers_name
    assert group_link_x.creditor_weight == 1.0
    assert group_link_x.debtor_weight == 1.0

    # WHEN
    bikers_creditor_weight = 3.0
    bikers_debtor_weight = 5.0

    group_link_x = grouplink_shop(
        name=bikers_name,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debtor_weight,
    )

    # THEN
    assert group_link_x.creditor_weight == 3.0
    assert group_link_x.debtor_weight == 5.0


def test_brankLink_set_contract_importanceCorrectly():
    # GIVEN
    bikers_name = GroupName("bikers")
    bikers_creditor_weight = 3.0
    bikers_debt_weight = 6.0
    grouplinks_sum_creditor_weight = 60
    grouplinks_sum_debtor_weight = 60
    idea_contract_importance = 1
    group_heir_x = groupheir_shop(
        name=bikers_name,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debt_weight,
    )

    # WHEN
    group_heir_x.set_contract_credit_debt(
        idea_contract_importance=idea_contract_importance,
        groupheirs_creditor_weight_sum=grouplinks_sum_creditor_weight,
        groupheirs_debtor_weight_sum=grouplinks_sum_debtor_weight,
    )

    # THEN
    assert group_heir_x._contract_credit == 0.05
    assert group_heir_x._contract_debt == 0.1


def test_grouplink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    bikers_name = GroupName("bikers")
    bikers_creditor_weight = 3.0
    bikers_debtor_weight = 5.0
    bikers_link = grouplink_shop(
        name=bikers_name,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debtor_weight,
    )

    print(f"{bikers_link}")

    # WHEN
    biker_dict = bikers_link.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "name": bikers_link.name,
        "creditor_weight": bikers_link.creditor_weight,
        "debtor_weight": bikers_link.debtor_weight,
    }


def test_grouplinks_get_from_JSON_SimpleExampleWorks():
    # GIVEN
    str_teacher = "teachers"
    teacher_grouplink = grouplink_shop(
        name=str_teacher, creditor_weight=103, debtor_weight=155
    )
    teacher_dict = teacher_grouplink.get_dict()
    grouplinks_dict = {teacher_grouplink.name: teacher_dict}

    teachers_json = x_get_json(dict_x=grouplinks_dict)
    assert teachers_json != None
    assert x_is_json(json_x=teachers_json)

    # WHEN
    grouplinks_obj_dict = grouplinks_get_from_json(grouplinks_json=teachers_json)

    # THEN
    assert grouplinks_obj_dict != None
    teachers_obj_check_dict = {teacher_grouplink.name: teacher_grouplink}
    print(f"    {grouplinks_obj_dict=}")
    print(f"{teachers_obj_check_dict=}")
    assert grouplinks_obj_dict == teachers_obj_check_dict


def test_Groupline_exists():
    # GIVEN
    bikers_name = GroupName("bikers")
    groupline_x = Groupline(
        name=bikers_name, _contract_credit=0.33, _contract_debt=0.55
    )
    assert groupline_x.name == bikers_name
    assert groupline_x._contract_credit == 0.33
    assert groupline_x._contract_debt == 0.55

    # WHEN
    groupline_x.add_contract_credit_debt(contract_credit=0.11, contract_debt=0.2)

    # THEN
    assert groupline_x._contract_credit == 0.44
    assert groupline_x._contract_debt == 0.75
