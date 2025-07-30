from src.a00_data_toolbox.dict_toolbox import get_json_from_dict, x_is_json
from src.a03_group_logic.group import (
    AwardHeir,
    AwardLine,
    AwardLink,
    GroupCore,
    GroupTitle,
    MemberShip,
    awardheir_shop,
    awardline_shop,
    awardlink_shop,
    awardlinks_get_from_json,
    membership_get_from_dict,
    membership_shop,
    memberships_get_from_dict,
)
from src.a03_group_logic.test._util.a03_str import (
    _credor_pool_str,
    _debtor_pool_str,
    _fund_agenda_give_str,
    _fund_agenda_ratio_give_str,
    _fund_agenda_ratio_take_str,
    _fund_agenda_take_str,
    _fund_give_str,
    _fund_take_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    partner_name_str,
)


def test_GroupCore_exists():
    # ESTABLISH
    swim_str = ";swimmers"
    # WHEN
    swim_groupcore = GroupCore(group_title=swim_str)
    # THEN
    assert swim_groupcore is not None
    assert swim_groupcore.group_title == swim_str


def test_MemberShip_exists():
    # ESTABLISH
    swim_str = ",swim"

    # WHEN
    swim_membership = MemberShip(group_title=swim_str)

    # THEN
    assert swim_membership.group_title == swim_str
    assert swim_membership.group_cred_points == 1.0
    assert swim_membership.group_debt_points == 1.0
    assert not swim_membership._credor_pool
    assert not swim_membership._debtor_pool
    assert not swim_membership._fund_give
    assert not swim_membership._fund_take
    assert not swim_membership._fund_agenda_give
    assert not swim_membership._fund_agenda_take
    assert not swim_membership._fund_agenda_ratio_give
    assert not swim_membership._fund_agenda_ratio_take
    assert not swim_membership.partner_name
    obj_attrs = set(swim_membership.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        _credor_pool_str(),
        _debtor_pool_str(),
        _fund_agenda_give_str(),
        _fund_agenda_ratio_give_str(),
        _fund_agenda_ratio_take_str(),
        _fund_agenda_take_str(),
        _fund_give_str(),
        _fund_take_str(),
        partner_name_str(),
        group_cred_points_str(),
        group_debt_points_str(),
        group_title_str(),
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
    assert swim_membership._credor_pool == 0
    assert swim_membership._debtor_pool == 0
    assert not swim_membership._fund_give
    assert not swim_membership._fund_take
    assert not swim_membership._fund_agenda_give
    assert not swim_membership._fund_agenda_take
    assert not swim_membership._fund_agenda_ratio_give
    assert not swim_membership._fund_agenda_ratio_take
    assert not swim_membership.partner_name


def test_membership_shop_ReturnsObjAttr_partner_name():
    # ESTABLISH
    swim_str = ",swim"
    yao_str = "Yao"

    # WHEN
    swim_membership = membership_shop(swim_str, partner_name=yao_str)

    # THEN
    assert swim_membership.partner_name == yao_str


# def test_MemberShip_set_group_title_RaisesErrorIf_group_title_IsNotPartnerNameAndIsLabelTerm():
#     # ESTABLISH
#     slash_str = "/"
#     # bob_str = f"Bob{slash_str}Texas"
#     bob_str = "Bob"
#     # swim_str = f"{slash_str}swim"
#     swim_str = ",swim"

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         membership_shop(swim_str, partner_name=bob_str, knot=slash_str)
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


def test_MemberShip_get_dict_ReturnsDictWithNecessaryDataForJSON():
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
        partner_name=yao_str,
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
        partner_name=yao_str,
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


def test_MemberShip_clear_fund_give_take_SetsAttrCorrectly():
    # ESTABLISH
    bob_membership = membership_shop("Bob")
    bob_membership._fund_give = 0.27
    bob_membership._fund_take = 0.37
    bob_membership._fund_agenda_give = 0.41
    bob_membership._fund_agenda_take = 0.51
    bob_membership._fund_agenda_ratio_give = 0.433
    bob_membership._fund_agenda_ratio_take = 0.533
    assert bob_membership._fund_give == 0.27
    assert bob_membership._fund_take == 0.37
    assert bob_membership._fund_agenda_give == 0.41
    assert bob_membership._fund_agenda_take == 0.51
    assert bob_membership._fund_agenda_ratio_give == 0.433
    assert bob_membership._fund_agenda_ratio_take == 0.533

    # WHEN
    bob_membership.clear_fund_give_take()

    # THEN
    assert bob_membership._fund_give == 0
    assert bob_membership._fund_take == 0
    assert bob_membership._fund_agenda_give == 0
    assert bob_membership._fund_agenda_take == 0
    assert bob_membership._fund_agenda_ratio_give == 0
    assert bob_membership._fund_agenda_ratio_take == 0


def test_AwardLink_exists():
    # ESTABLISH
    bikers_str = "bikers"

    # WHEN
    bikers_awardlink = AwardLink(awardee_title=bikers_str)

    # THEN
    assert bikers_awardlink.awardee_title == bikers_str
    assert bikers_awardlink.give_force == 1.0
    assert bikers_awardlink.take_force == 1.0


def test_awardlink_shop_ReturnsObj():
    # ESTABLISH
    bikers_str = "bikers"
    bikers_give_force = 3.0
    bikers_take_force = 5.0

    # WHEN
    bikers_awardlink = awardlink_shop(
        awardee_title=bikers_str,
        give_force=bikers_give_force,
        take_force=bikers_take_force,
    )

    # THEN
    assert bikers_awardlink.give_force == bikers_give_force
    assert bikers_awardlink.take_force == bikers_take_force


def test_AwardHeir_exists():
    # ESTABLISH / WHEN
    x_awardheir = AwardHeir()

    # THEN
    assert not x_awardheir.awardee_title
    assert x_awardheir.give_force == 1.0
    assert x_awardheir.take_force == 1.0
    assert not x_awardheir._fund_give
    assert not x_awardheir._fund_take


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

    # WHEN
    assert x_awardheir.awardee_title == bikers_str
    assert x_awardheir.give_force == bikers_give_force
    assert x_awardheir.take_force == bikers_take_force


def test_AwardLink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # ESTABLISH
    bikers_str = "bikers"
    bikers_give_force = 3.0
    bikers_take_force = 5.0
    bikers_awardlink = awardlink_shop(
        awardee_title=bikers_str,
        give_force=bikers_give_force,
        take_force=bikers_take_force,
    )

    print(f"{bikers_awardlink}")

    # WHEN
    biker_dict = bikers_awardlink.to_dict()

    # THEN
    assert biker_dict is not None
    assert biker_dict == {
        "awardee_title": bikers_awardlink.awardee_title,
        "give_force": bikers_awardlink.give_force,
        "take_force": bikers_awardlink.take_force,
    }


def test_awardlinks_get_from_JSON_ReturnsObj_SimpleExample():
    # ESTABLISH
    teacher_str = "teachers"
    teacher_awardlink = awardlink_shop(
        awardee_title=teacher_str, give_force=103, take_force=155
    )
    teacher_dict = teacher_awardlink.to_dict()
    awardlinks_dict = {teacher_awardlink.awardee_title: teacher_dict}

    teachers_json = get_json_from_dict(awardlinks_dict)
    assert teachers_json is not None
    assert x_is_json(teachers_json)

    # WHEN
    awardlinks_obj_dict = awardlinks_get_from_json(awardlinks_json=teachers_json)

    # THEN
    assert awardlinks_obj_dict is not None
    teachers_obj_check_dict = {teacher_awardlink.awardee_title: teacher_awardlink}
    print(f"    {awardlinks_obj_dict=}")
    print(f"{teachers_obj_check_dict=}")
    assert awardlinks_obj_dict == teachers_obj_check_dict


def test_AwardLine_exists():
    # ESTABLISH
    bikers_str = "bikers"
    bikers_fund_give = 0.33
    bikers_fund_take = 0.55

    # WHEN
    bikers_awardline = AwardLine(
        awardee_title=bikers_str,
        _fund_give=bikers_fund_give,
        _fund_take=bikers_fund_take,
    )

    # THEN
    assert bikers_awardline.awardee_title == bikers_str
    assert bikers_awardline._fund_give == bikers_fund_give
    assert bikers_awardline._fund_take == bikers_fund_take


def test_awardline_shop_ReturnsObj_exists():
    # ESTABLISH
    bikers_str = "bikers"
    bikers_str = bikers_str
    bikers_fund_give = 0.33
    bikers_fund_take = 0.55

    # WHEN
    biker_awardline = awardline_shop(
        awardee_title=bikers_str,
        _fund_give=bikers_fund_give,
        _fund_take=bikers_fund_take,
    )

    assert biker_awardline is not None
    assert biker_awardline.awardee_title == bikers_str
    assert biker_awardline._fund_give == bikers_fund_give
    assert biker_awardline._fund_take == bikers_fund_take


def test_AwardLine_add_fund_give_take_CorrectlyModifiesAttr():
    # ESTABLISH
    bikers_str = "bikers"
    bikers_awardline = awardline_shop(
        awardee_title=bikers_str, _fund_give=0.33, _fund_take=0.55
    )
    assert bikers_awardline.awardee_title == bikers_str
    assert bikers_awardline._fund_give == 0.33
    assert bikers_awardline._fund_take == 0.55

    # WHEN
    bikers_awardline.add_fund_give_take(fund_give=0.11, fund_take=0.2)

    # THEN
    assert bikers_awardline._fund_give == 0.44
    assert bikers_awardline._fund_take == 0.75
