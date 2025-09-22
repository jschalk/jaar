from src.ch01_data_toolbox.dict_toolbox import get_json_from_dict, x_is_json
from src.ch04_group_logic._ref.ch04_terms import (
    credor_pool_str,
    debtor_pool_str,
    fund_agenda_give_str,
    fund_agenda_ratio_give_str,
    fund_agenda_ratio_take_str,
    fund_agenda_take_str,
    fund_give_str,
    fund_take_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    voice_name_str,
)
from src.ch04_group_logic.group import (
    AwardHeir,
    AwardLine,
    AwardUnit,
    GroupCore,
    GroupTitle,
    MemberShip,
    awardheir_shop,
    awardline_shop,
    awardunit_shop,
    awardunits_get_from_json,
    membership_get_from_dict,
    membership_shop,
    memberships_get_from_dict,
)


def test_GroupCore_Exists():
    # ESTABLISH
    swim_str = ";swimmers"
    # WHEN
    swim_groupcore = GroupCore(group_title=swim_str)
    # THEN
    assert swim_groupcore is not None
    assert swim_groupcore.group_title == swim_str


def test_MemberShip_Exists():
    # ESTABLISH
    swim_str = ",swim"

    # WHEN
    swim_membership = MemberShip(group_title=swim_str)

    # THEN
    assert swim_membership.group_title == swim_str
    assert swim_membership.group_cred_points == 1.0
    assert swim_membership.group_debt_points == 1.0
    assert not swim_membership.credor_pool
    assert not swim_membership.debtor_pool
    assert not swim_membership.fund_give
    assert not swim_membership.fund_take
    assert not swim_membership.fund_agenda_give
    assert not swim_membership.fund_agenda_take
    assert not swim_membership.fund_agenda_ratio_give
    assert not swim_membership.fund_agenda_ratio_take
    assert not swim_membership.voice_name
    obj_attrs = set(swim_membership.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        voice_name_str(),
        group_title_str(),
        group_cred_points_str(),
        group_debt_points_str(),
        credor_pool_str(),
        debtor_pool_str(),
        fund_agenda_give_str(),
        fund_agenda_ratio_give_str(),
        fund_agenda_ratio_take_str(),
        fund_agenda_take_str(),
        fund_give_str(),
        fund_take_str(),
    }


def test_membership_shop_ReturnsObj():
    # ESTABLISH
    swim_str = ",swim"
    swim_group_cred_points = 3.0
    swim_group_debt_points = 5.0

    # WHEN
    swim_membership = membership_shop(
        group_title=swim_str,
        group_cred_points=swim_group_cred_points,
        group_debt_points=swim_group_debt_points,
    )

    # THEN
    assert swim_membership.group_cred_points == swim_group_cred_points
    assert swim_membership.group_debt_points == swim_group_debt_points
    assert swim_membership.credor_pool == 0
    assert swim_membership.debtor_pool == 0
    assert not swim_membership.fund_give
    assert not swim_membership.fund_take
    assert not swim_membership.fund_agenda_give
    assert not swim_membership.fund_agenda_take
    assert not swim_membership.fund_agenda_ratio_give
    assert not swim_membership.fund_agenda_ratio_take
    assert not swim_membership.voice_name


def test_membership_shop_ReturnsObjAttr_voice_name():
    # ESTABLISH
    swim_str = ",swim"
    yao_str = "Yao"

    # WHEN
    swim_membership = membership_shop(swim_str, voice_name=yao_str)

    # THEN
    assert swim_membership.voice_name == yao_str


# def test_MemberShip_set_group_title_RaisesErrorIf_group_title_IsNotVoiceNameAndIsLabelTerm():
#     # ESTABLISH
#     slash_str = "/"
#     # bob_str = f"Bob{slash_str}Texas"
#     bob_str = "Bob"
#     # swim_str = f"{slash_str}swim"
#     swim_str = ",swim"

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         membership_shop(swim_str, voice_name=bob_str, knot=slash_str)
#     assert (
#         str(excinfo.value)
#         == f"'{swim_str}' needs to not be a LabelTerm. Must contain knot: '{slash_str}'"
#     )


def test_MemberShip_set_group_cred_points_SetsAttr():
    # ESTABLISH
    swim_str = ",swim"
    old_group_cred_points = 3.0
    swim_group_debt_points = 5.0
    swim_membership = membership_shop(
        swim_str, old_group_cred_points, swim_group_debt_points
    )
    assert swim_membership.group_cred_points == old_group_cred_points
    assert swim_membership.group_debt_points == swim_group_debt_points

    # WHEN
    new_swim_group_cred_points = 44
    swim_membership.set_group_cred_points(new_swim_group_cred_points)

    # THEN
    assert swim_membership.group_cred_points == new_swim_group_cred_points
    assert swim_membership.group_debt_points == swim_group_debt_points


def test_MemberShip_set_group_cred_points_NoneParameter():
    # ESTABLISH
    swim_str = ",swim"
    old_group_cred_points = 3.0
    swim_group_debt_points = 5.0
    swim_membership = membership_shop(
        swim_str, old_group_cred_points, swim_group_debt_points
    )
    assert swim_membership.group_cred_points == old_group_cred_points
    assert swim_membership.group_debt_points == swim_group_debt_points

    # WHEN
    swim_membership.set_group_cred_points(None)

    # THEN
    assert swim_membership.group_cred_points == old_group_cred_points
    assert swim_membership.group_debt_points == swim_group_debt_points


def test_MemberShip_set_group_debt_points_SetsAttr():
    # ESTABLISH
    swim_str = ",swim"
    swim_group_cred_points = 3.0
    old_group_debt_points = 5.0
    swim_membership = membership_shop(
        swim_str, swim_group_cred_points, old_group_debt_points
    )
    assert swim_membership.group_cred_points == swim_group_cred_points
    assert swim_membership.group_debt_points == old_group_debt_points

    # WHEN
    new_group_debt_points = 55
    swim_membership.set_group_debt_points(new_group_debt_points)

    # THEN
    assert swim_membership.group_cred_points == swim_group_cred_points
    assert swim_membership.group_debt_points == new_group_debt_points


def test_MemberShip_set_group_debt_points_DoesNotSetsAttrNone():
    # ESTABLISH
    swim_str = ",swim"
    swim_group_cred_points = 3.0
    old_group_debt_points = 5.0
    swim_membership = membership_shop(
        swim_str, swim_group_cred_points, old_group_debt_points
    )
    assert swim_membership.group_cred_points == swim_group_cred_points
    assert swim_membership.group_debt_points == old_group_debt_points

    # WHEN
    swim_membership.set_group_debt_points(None)

    # THEN
    assert swim_membership.group_cred_points == swim_group_cred_points
    assert swim_membership.group_debt_points == old_group_debt_points


def test_MemberShip_to_dict_ReturnsDictWithNecessaryDataForJSON():
    # ESTABLISH
    swim_str = ",swim"
    swim_group_cred_points = 3.0
    swim_group_debt_points = 5.0
    swim_membership = membership_shop(
        group_title=swim_str,
        group_cred_points=swim_group_cred_points,
        group_debt_points=swim_group_debt_points,
    )

    print(f"{swim_membership}")

    # WHEN
    swim_dict = swim_membership.to_dict()

    # THEN
    assert swim_dict is not None
    assert swim_dict == {
        "group_title": swim_membership.group_title,
        "group_cred_points": swim_membership.group_cred_points,
        "group_debt_points": swim_membership.group_debt_points,
    }


def test_membership_get_from_dict_ReturnsObj():
    # ESTABLISH
    swim_str = ",swim"
    swim_group_cred_points = 3.0
    swim_group_debt_points = 5.0
    yao_str = "Yao"
    before_swim_membership = membership_shop(
        group_title=swim_str,
        group_cred_points=swim_group_cred_points,
        group_debt_points=swim_group_debt_points,
        voice_name=yao_str,
    )
    swim_membership_dict = before_swim_membership.to_dict()

    # WHEN
    after_swim_membership = membership_get_from_dict(swim_membership_dict, yao_str)

    # THEN
    assert before_swim_membership == after_swim_membership
    assert after_swim_membership.group_title == swim_str


def test_memberships_get_from_dict_ReturnsObj():
    # ESTABLISH
    swim_str = ",swim"
    swim_group_cred_points = 3.0
    swim_group_debt_points = 5.0
    yao_str = "Yao"
    before_swim_membership = membership_shop(
        group_title=swim_str,
        group_cred_points=swim_group_cred_points,
        group_debt_points=swim_group_debt_points,
        voice_name=yao_str,
    )
    before_swim_memberships_objs = {swim_str: before_swim_membership}
    swim_memberships_dict = {swim_str: before_swim_membership.to_dict()}

    # WHEN
    after_swim_memberships_objs = memberships_get_from_dict(
        swim_memberships_dict, yao_str
    )

    # THEN
    assert before_swim_memberships_objs == after_swim_memberships_objs
    assert after_swim_memberships_objs.get(swim_str) == before_swim_membership


def test_MemberShip_clear_fund_give_take_SetsAttr():
    # ESTABLISH
    bob_membership = membership_shop("Bob")
    bob_membership.fund_give = 0.27
    bob_membership.fund_take = 0.37
    bob_membership.fund_agenda_give = 0.41
    bob_membership.fund_agenda_take = 0.51
    bob_membership.fund_agenda_ratio_give = 0.433
    bob_membership.fund_agenda_ratio_take = 0.533
    assert bob_membership.fund_give == 0.27
    assert bob_membership.fund_take == 0.37
    assert bob_membership.fund_agenda_give == 0.41
    assert bob_membership.fund_agenda_take == 0.51
    assert bob_membership.fund_agenda_ratio_give == 0.433
    assert bob_membership.fund_agenda_ratio_take == 0.533

    # WHEN
    bob_membership.clear_fund_give_take()

    # THEN
    assert bob_membership.fund_give == 0
    assert bob_membership.fund_take == 0
    assert bob_membership.fund_agenda_give == 0
    assert bob_membership.fund_agenda_take == 0
    assert bob_membership.fund_agenda_ratio_give == 0
    assert bob_membership.fund_agenda_ratio_take == 0


def test_AwardUnit_Exists():
    # ESTABLISH
    bikers_str = "bikers"

    # WHEN
    bikers_awardunit = AwardUnit(awardee_title=bikers_str)

    # THEN
    assert bikers_awardunit.awardee_title == bikers_str
    assert bikers_awardunit.give_force == 1.0
    assert bikers_awardunit.take_force == 1.0


def test_awardunit_shop_ReturnsObj():
    # ESTABLISH
    bikers_str = "bikers"
    bikers_give_force = 3.0
    bikers_take_force = 5.0

    # WHEN
    bikers_awardunit = awardunit_shop(
        awardee_title=bikers_str,
        give_force=bikers_give_force,
        take_force=bikers_take_force,
    )

    # THEN
    assert bikers_awardunit.give_force == bikers_give_force
    assert bikers_awardunit.take_force == bikers_take_force


def test_AwardHeir_Exists():
    # ESTABLISH / WHEN
    x_awardheir = AwardHeir()

    # THEN
    assert not x_awardheir.awardee_title
    assert x_awardheir.give_force == 1.0
    assert x_awardheir.take_force == 1.0
    assert not x_awardheir.fund_give
    assert not x_awardheir.fund_take


def test_awardheir_shop_ReturnsObj():
    # ESTABLISH
    bikers_str = "bikers"
    bikers_give_force = 3.0
    bikers_take_force = 6.0

    # WHEN
    x_awardheir = awardheir_shop(
        awardee_title=bikers_str,
        give_force=bikers_give_force,
        take_force=bikers_take_force,
    )

    # THEN
    assert x_awardheir.awardee_title == bikers_str
    assert x_awardheir.give_force == bikers_give_force
    assert x_awardheir.take_force == bikers_take_force


def test_AwardUnit_to_dict_ReturnsDictWithNecessaryDataForJSON():
    # ESTABLISH
    bikers_str = "bikers"
    bikers_give_force = 3.0
    bikers_take_force = 5.0
    bikers_awardunit = awardunit_shop(
        awardee_title=bikers_str,
        give_force=bikers_give_force,
        take_force=bikers_take_force,
    )

    print(f"{bikers_awardunit}")

    # WHEN
    biker_dict = bikers_awardunit.to_dict()

    # THEN
    assert biker_dict is not None
    assert biker_dict == {
        "awardee_title": bikers_awardunit.awardee_title,
        "give_force": bikers_awardunit.give_force,
        "take_force": bikers_awardunit.take_force,
    }


def test_awardunits_get_from_JSON_ReturnsObj_SimpleExample():
    # ESTABLISH
    teacher_str = "teachers"
    teacher_awardunit = awardunit_shop(
        awardee_title=teacher_str, give_force=103, take_force=155
    )
    teacher_dict = teacher_awardunit.to_dict()
    awardunits_dict = {teacher_awardunit.awardee_title: teacher_dict}

    teachers_json = get_json_from_dict(awardunits_dict)
    assert teachers_json is not None
    assert x_is_json(teachers_json)

    # WHEN
    awardunits_obj_dict = awardunits_get_from_json(awardunits_json=teachers_json)

    # THEN
    assert awardunits_obj_dict is not None
    teachers_obj_check_dict = {teacher_awardunit.awardee_title: teacher_awardunit}
    print(f"    {awardunits_obj_dict=}")
    print(f"{teachers_obj_check_dict=}")
    assert awardunits_obj_dict == teachers_obj_check_dict


def test_AwardLine_Exists():
    # ESTABLISH
    bikers_str = "bikers"
    bikers_fund_give = 0.33
    bikers_fund_take = 0.55

    # WHEN
    bikers_awardline = AwardLine(
        awardee_title=bikers_str,
        fund_give=bikers_fund_give,
        fund_take=bikers_fund_take,
    )

    # THEN
    assert bikers_awardline.awardee_title == bikers_str
    assert bikers_awardline.fund_give == bikers_fund_give
    assert bikers_awardline.fund_take == bikers_fund_take


def test_awardline_shop_ReturnsObj_Exists():
    # ESTABLISH
    bikers_str = "bikers"
    bikers_str = bikers_str
    bikers_fund_give = 0.33
    bikers_fund_take = 0.55

    # WHEN
    biker_awardline = awardline_shop(
        awardee_title=bikers_str,
        fund_give=bikers_fund_give,
        fund_take=bikers_fund_take,
    )

    # THEN
    assert biker_awardline is not None
    assert biker_awardline.awardee_title == bikers_str
    assert biker_awardline.fund_give == bikers_fund_give
    assert biker_awardline.fund_take == bikers_fund_take


def test_AwardLine_add_fund_give_take_ModifiesAttr():
    # ESTABLISH
    bikers_str = "bikers"
    bikers_awardline = awardline_shop(
        awardee_title=bikers_str, fund_give=0.33, fund_take=0.55
    )
    assert bikers_awardline.awardee_title == bikers_str
    assert bikers_awardline.fund_give == 0.33
    assert bikers_awardline.fund_take == 0.55

    # WHEN
    bikers_awardline.add_fund_give_take(fund_give=0.11, fund_take=0.2)

    # THEN
    assert bikers_awardline.fund_give == 0.44
    assert bikers_awardline.fund_take == 0.75
