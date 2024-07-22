from src.bud.group import (
    GroupCore,
    GroupID,
    membership_shop,
    MemberShip,
    membership_get_from_dict,
    memberships_get_from_dict,
    AwardLine,
    awardline_shop,
    AwardLink,
    awardlink_shop,
    awardlinks_get_from_json,
    AwardHeir,
    awardheir_shop,
)
from src._instrument.python import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_GroupID_exists():
    ohio_group_id = GroupID(",ohio")
    assert ohio_group_id is not None


def test_GroupCore_exists():
    # ESTABLISH
    swim_text = ",swimmers"
    # WHEN
    swim_groupcore = GroupCore(group_id=swim_text)
    # THEN
    assert swim_groupcore is not None
    assert swim_groupcore.group_id == swim_text


def test_MemberShip_exists():
    # ESTABLISH
    swim_text = ",swim"

    # WHEN
    swim_membership = MemberShip(group_id=swim_text)

    # THEN
    assert swim_membership.group_id == swim_text
    assert swim_membership.credit_weight == 1.0
    assert swim_membership.debtit_weight == 1.0
    assert swim_membership._credor_pool is None
    assert swim_membership._debtor_pool is None
    assert swim_membership._fund_give is None
    assert swim_membership._fund_take is None
    assert swim_membership._fund_agenda_give is None
    assert swim_membership._fund_agenda_take is None
    assert swim_membership._fund_agenda_ratio_give is None
    assert swim_membership._fund_agenda_ratio_take is None
    assert swim_membership._acct_id is None


def test_membership_shop_ReturnsCorrectObj():
    # ESTABLISH
    swim_text = ",swim"
    swim_credit_weight = 3.0
    swim_debtit_weight = 5.0

    # WHEN
    swim_membership = membership_shop(
        group_id=swim_text,
        credit_weight=swim_credit_weight,
        debtit_weight=swim_debtit_weight,
    )

    # THEN
    assert swim_membership.credit_weight == swim_credit_weight
    assert swim_membership.debtit_weight == swim_debtit_weight
    assert swim_membership._credor_pool == 0
    assert swim_membership._debtor_pool == 0
    assert swim_membership._fund_give is None
    assert swim_membership._fund_take is None
    assert swim_membership._fund_agenda_give is None
    assert swim_membership._fund_agenda_take is None
    assert swim_membership._fund_agenda_ratio_give is None
    assert swim_membership._fund_agenda_ratio_take is None
    assert swim_membership._acct_id is None


def test_membership_shop_ReturnsCorrectObjAttr_acct_id():
    # ESTABLISH
    swim_text = ",swim"
    yao_text = "Yao"

    # WHEN
    swim_membership = membership_shop(swim_text, _acct_id=yao_text)

    # THEN
    assert swim_membership._acct_id == yao_text


# def test_MemberShip_set_group_id_RaisesErrorIf_group_id_IsNotAcctIDAndIsRoadNode():
#     # ESTABLISH
#     slash_text = "/"
#     # bob_text = f"Bob{slash_text}Texas"
#     bob_text = "Bob"
#     # swim_text = f"{slash_text}swim"
#     swim_text = ",swim"

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         membership_shop(swim_text, _acct_id=bob_text, _road_delimiter=slash_text)
#     assert (
#         str(excinfo.value)
#         == f"'{swim_text}' needs to not be a RoadNode. Must contain delimiter: '{slash_text}'"
#     )


def test_MemberShip_set_credit_weight_SetsAttr():
    # ESTABLISH
    swim_text = ",swim"
    old_credit_weight = 3.0
    swim_debtit_weight = 5.0
    swim_membership = membership_shop(swim_text, old_credit_weight, swim_debtit_weight)
    assert swim_membership.credit_weight == old_credit_weight
    assert swim_membership.debtit_weight == swim_debtit_weight

    # WHEN
    new_swim_credit_weight = 44
    swim_membership.set_credit_weight(new_swim_credit_weight)

    # THEN
    assert swim_membership.credit_weight == new_swim_credit_weight
    assert swim_membership.debtit_weight == swim_debtit_weight


def test_MemberShip_set_credit_weight_HandlesNoneParameter():
    # ESTABLISH
    swim_text = ",swim"
    old_credit_weight = 3.0
    swim_debtit_weight = 5.0
    swim_membership = membership_shop(swim_text, old_credit_weight, swim_debtit_weight)
    assert swim_membership.credit_weight == old_credit_weight
    assert swim_membership.debtit_weight == swim_debtit_weight

    # WHEN
    swim_membership.set_credit_weight(None)

    # THEN
    assert swim_membership.credit_weight == old_credit_weight
    assert swim_membership.debtit_weight == swim_debtit_weight


def test_MemberShip_set_debtit_weight_SetsAttr():
    # ESTABLISH
    swim_text = ",swim"
    swim_credit_weight = 3.0
    old_debtit_weight = 5.0
    swim_membership = membership_shop(swim_text, swim_credit_weight, old_debtit_weight)
    assert swim_membership.credit_weight == swim_credit_weight
    assert swim_membership.debtit_weight == old_debtit_weight

    # WHEN
    new_debtit_weight = 55
    swim_membership.set_debtit_weight(new_debtit_weight)

    # THEN
    assert swim_membership.credit_weight == swim_credit_weight
    assert swim_membership.debtit_weight == new_debtit_weight


def test_MemberShip_set_debtit_weight_SetsAttr():
    # ESTABLISH
    swim_text = ",swim"
    swim_credit_weight = 3.0
    old_debtit_weight = 5.0
    swim_membership = membership_shop(swim_text, swim_credit_weight, old_debtit_weight)
    assert swim_membership.credit_weight == swim_credit_weight
    assert swim_membership.debtit_weight == old_debtit_weight

    # WHEN
    swim_membership.set_debtit_weight(None)

    # THEN
    assert swim_membership.credit_weight == swim_credit_weight
    assert swim_membership.debtit_weight == old_debtit_weight


def test_MemberShip_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # ESTABLISH
    swim_text = ",swim"
    swim_credit_weight = 3.0
    swim_debtit_weight = 5.0
    swim_membership = membership_shop(
        group_id=swim_text,
        credit_weight=swim_credit_weight,
        debtit_weight=swim_debtit_weight,
    )

    print(f"{swim_membership}")

    # WHEN
    swim_dict = swim_membership.get_dict()

    # THEN
    assert swim_dict is not None
    assert swim_dict == {
        "group_id": swim_membership.group_id,
        "credit_weight": swim_membership.credit_weight,
        "debtit_weight": swim_membership.debtit_weight,
    }


def test_membership_get_from_dict_ReturnsObj():
    # ESTABLISH
    swim_text = ",swim"
    swim_credit_weight = 3.0
    swim_debtit_weight = 5.0
    yao_text = "Yao"
    before_swim_membership = membership_shop(
        group_id=swim_text,
        credit_weight=swim_credit_weight,
        debtit_weight=swim_debtit_weight,
        _acct_id=yao_text,
    )
    swim_membership_dict = before_swim_membership.get_dict()

    # WHEN
    after_swim_membership = membership_get_from_dict(swim_membership_dict, yao_text)

    # THEN
    assert before_swim_membership == after_swim_membership
    assert after_swim_membership.group_id == swim_text


def test_memberships_get_from_dict_ReturnsObj():
    # ESTABLISH
    swim_text = ",swim"
    swim_credit_weight = 3.0
    swim_debtit_weight = 5.0
    yao_text = "Yao"
    before_swim_membership = membership_shop(
        group_id=swim_text,
        credit_weight=swim_credit_weight,
        debtit_weight=swim_debtit_weight,
        _acct_id=yao_text,
    )
    before_swim_memberships_objs = {swim_text: before_swim_membership}
    swim_memberships_dict = {swim_text: before_swim_membership.get_dict()}

    # WHEN
    after_swim_memberships_objs = memberships_get_from_dict(
        swim_memberships_dict, yao_text
    )

    # THEN
    assert before_swim_memberships_objs == after_swim_memberships_objs
    assert after_swim_memberships_objs.get(swim_text) == before_swim_membership


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
    bikers_text = "bikers"

    # WHEN
    bikers_awardlink = AwardLink(group_id=bikers_text)

    # THEN
    assert bikers_awardlink.group_id == bikers_text
    assert bikers_awardlink.give_force == 1.0
    assert bikers_awardlink.take_force == 1.0


def test_awardlink_shop_ReturnsCorrectObj():
    # ESTABLISH
    bikers_text = "bikers"
    bikers_give_force = 3.0
    bikers_take_force = 5.0

    # WHEN
    bikers_awardlink = awardlink_shop(
        group_id=bikers_text,
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
    assert not x_awardheir.group_id
    assert x_awardheir.give_force == 1.0
    assert x_awardheir.take_force == 1.0
    assert not x_awardheir._fund_give
    assert not x_awardheir._fund_take


def test_awardheir_shop_ReturnsObj():
    # ESTABLISH
    bikers_text = "bikers"
    bikers_give_force = 3.0
    bikers_take_force = 6.0

    # WHEN
    x_awardheir = awardheir_shop(
        group_id=bikers_text,
        give_force=bikers_give_force,
        take_force=bikers_take_force,
    )

    # WHEN
    assert x_awardheir.group_id == bikers_text
    assert x_awardheir.give_force == bikers_give_force
    assert x_awardheir.take_force == bikers_take_force


def test_AwardLink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # ESTABLISH
    bikers_text = "bikers"
    bikers_give_force = 3.0
    bikers_take_force = 5.0
    bikers_awardlink = awardlink_shop(
        group_id=bikers_text,
        give_force=bikers_give_force,
        take_force=bikers_take_force,
    )

    print(f"{bikers_awardlink}")

    # WHEN
    biker_dict = bikers_awardlink.get_dict()

    # THEN
    assert biker_dict is not None
    assert biker_dict == {
        "group_id": bikers_awardlink.group_id,
        "give_force": bikers_awardlink.give_force,
        "take_force": bikers_awardlink.take_force,
    }


def test_awardlinks_get_from_JSON_ReturnsCorrectObj_SimpleExample():
    # ESTABLISH
    teacher_text = "teachers"
    teacher_awardlink = awardlink_shop(
        group_id=teacher_text, give_force=103, take_force=155
    )
    teacher_dict = teacher_awardlink.get_dict()
    awardlinks_dict = {teacher_awardlink.group_id: teacher_dict}

    teachers_json = get_json_from_dict(dict_x=awardlinks_dict)
    assert teachers_json is not None
    assert x_is_json(json_x=teachers_json)

    # WHEN
    awardlinks_obj_dict = awardlinks_get_from_json(awardlinks_json=teachers_json)

    # THEN
    assert awardlinks_obj_dict is not None
    teachers_obj_check_dict = {teacher_awardlink.group_id: teacher_awardlink}
    print(f"    {awardlinks_obj_dict=}")
    print(f"{teachers_obj_check_dict=}")
    assert awardlinks_obj_dict == teachers_obj_check_dict


def test_AwardLine_exists():
    # ESTABLISH
    bikers_text = "bikers"
    bikers_fund_give = 0.33
    bikers_fund_take = 0.55

    # WHEN
    bikers_awardline = AwardLine(
        group_id=bikers_text,
        _fund_give=bikers_fund_give,
        _fund_take=bikers_fund_take,
    )

    # THEN
    assert bikers_awardline.group_id == bikers_text
    assert bikers_awardline._fund_give == bikers_fund_give
    assert bikers_awardline._fund_take == bikers_fund_take


def test_awardline_shop_ReturnsCorrectObj_exists():
    # ESTABLISH
    bikers_text = "bikers"
    bikers_text = bikers_text
    bikers_fund_give = 0.33
    bikers_fund_take = 0.55

    # WHEN
    biker_awardline = awardline_shop(
        group_id=bikers_text,
        _fund_give=bikers_fund_give,
        _fund_take=bikers_fund_take,
    )

    assert biker_awardline is not None
    assert biker_awardline.group_id == bikers_text
    assert biker_awardline._fund_give == bikers_fund_give
    assert biker_awardline._fund_take == bikers_fund_take


def test_AwardLine_add_fund_give_take_CorrectlyModifiesAttr():
    # ESTABLISH
    bikers_text = "bikers"
    bikers_awardline = awardline_shop(
        group_id=bikers_text, _fund_give=0.33, _fund_take=0.55
    )
    assert bikers_awardline.group_id == bikers_text
    assert bikers_awardline._fund_give == 0.33
    assert bikers_awardline._fund_take == 0.55

    # WHEN
    bikers_awardline.add_fund_give_take(fund_give=0.11, fund_take=0.2)

    # THEN
    assert bikers_awardline._fund_give == 0.44
    assert bikers_awardline._fund_take == 0.75
