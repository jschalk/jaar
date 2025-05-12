from src.a00_data_toolbox.dict_toolbox import x_is_json, get_json_from_dict
from src.a03_group_logic.group import (
    GroupCore,
    GroupLabel,
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


def test_GroupLabel_exists():
    ohio_group_label = GroupLabel(",ohio")
    assert ohio_group_label is not None


def test_GroupCore_exists():
    # ESTABLISH
    swim_str = ";swimmers"
    # WHEN
    swim_groupcore = GroupCore(group_label=swim_str)
    # THEN
    assert swim_groupcore is not None
    assert swim_groupcore.group_label == swim_str


def test_MemberShip_exists():
    # ESTABLISH
    swim_str = ",swim"

    # WHEN
    swim_membership = MemberShip(group_label=swim_str)

    # THEN
    assert swim_membership.group_label == swim_str
    assert swim_membership.credit_vote == 1.0
    assert swim_membership.debtit_vote == 1.0
    assert swim_membership._credor_pool is None
    assert swim_membership._debtor_pool is None
    assert swim_membership._fund_give is None
    assert swim_membership._fund_take is None
    assert swim_membership._fund_agenda_give is None
    assert swim_membership._fund_agenda_take is None
    assert swim_membership._fund_agenda_ratio_give is None
    assert swim_membership._fund_agenda_ratio_take is None
    assert swim_membership.acct_name is None


def test_membership_shop_ReturnsObj():
    # ESTABLISH
    swim_str = ",swim"
    swim_credit_vote = 3.0
    swim_debtit_vote = 5.0

    # WHEN
    swim_membership = membership_shop(
        group_label=swim_str,
        credit_vote=swim_credit_vote,
        debtit_vote=swim_debtit_vote,
    )

    # THEN
    assert swim_membership.credit_vote == swim_credit_vote
    assert swim_membership.debtit_vote == swim_debtit_vote
    assert swim_membership._credor_pool == 0
    assert swim_membership._debtor_pool == 0
    assert swim_membership._fund_give is None
    assert swim_membership._fund_take is None
    assert swim_membership._fund_agenda_give is None
    assert swim_membership._fund_agenda_take is None
    assert swim_membership._fund_agenda_ratio_give is None
    assert swim_membership._fund_agenda_ratio_take is None
    assert swim_membership.acct_name is None


def test_membership_shop_ReturnsObjAttr_acct_name():
    # ESTABLISH
    swim_str = ",swim"
    yao_str = "Yao"

    # WHEN
    swim_membership = membership_shop(swim_str, acct_name=yao_str)

    # THEN
    assert swim_membership.acct_name == yao_str


# def test_MemberShip_set_group_label_RaisesErrorIf_group_label_IsNotAcctNameAndIsTagUnit():
#     # ESTABLISH
#     slash_str = "/"
#     # bob_str = f"Bob{slash_str}Texas"
#     bob_str = "Bob"
#     # swim_str = f"{slash_str}swim"
#     swim_str = ",swim"

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         membership_shop(swim_str, acct_name=bob_str, bridge=slash_str)
#     assert (
#         str(excinfo.value)
#         == f"'{swim_str}' needs to not be a TagUnit. Must contain bridge: '{slash_str}'"
#     )


def test_MemberShip_set_credit_vote_SetsAttr():
    # ESTABLISH
    swim_str = ",swim"
    old_credit_vote = 3.0
    swim_debtit_vote = 5.0
    swim_membership = membership_shop(swim_str, old_credit_vote, swim_debtit_vote)
    assert swim_membership.credit_vote == old_credit_vote
    assert swim_membership.debtit_vote == swim_debtit_vote

    # WHEN
    new_swim_credit_vote = 44
    swim_membership.set_credit_vote(new_swim_credit_vote)

    # THEN
    assert swim_membership.credit_vote == new_swim_credit_vote
    assert swim_membership.debtit_vote == swim_debtit_vote


def test_MemberShip_set_credit_vote_NoneParameter():
    # ESTABLISH
    swim_str = ",swim"
    old_credit_vote = 3.0
    swim_debtit_vote = 5.0
    swim_membership = membership_shop(swim_str, old_credit_vote, swim_debtit_vote)
    assert swim_membership.credit_vote == old_credit_vote
    assert swim_membership.debtit_vote == swim_debtit_vote

    # WHEN
    swim_membership.set_credit_vote(None)

    # THEN
    assert swim_membership.credit_vote == old_credit_vote
    assert swim_membership.debtit_vote == swim_debtit_vote


def test_MemberShip_set_debtit_vote_SetsAttr():
    # ESTABLISH
    swim_str = ",swim"
    swim_credit_vote = 3.0
    old_debtit_vote = 5.0
    swim_membership = membership_shop(swim_str, swim_credit_vote, old_debtit_vote)
    assert swim_membership.credit_vote == swim_credit_vote
    assert swim_membership.debtit_vote == old_debtit_vote

    # WHEN
    new_debtit_vote = 55
    swim_membership.set_debtit_vote(new_debtit_vote)

    # THEN
    assert swim_membership.credit_vote == swim_credit_vote
    assert swim_membership.debtit_vote == new_debtit_vote


def test_MemberShip_set_debtit_vote_DoesNotSetsAttrNone():
    # ESTABLISH
    swim_str = ",swim"
    swim_credit_vote = 3.0
    old_debtit_vote = 5.0
    swim_membership = membership_shop(swim_str, swim_credit_vote, old_debtit_vote)
    assert swim_membership.credit_vote == swim_credit_vote
    assert swim_membership.debtit_vote == old_debtit_vote

    # WHEN
    swim_membership.set_debtit_vote(None)

    # THEN
    assert swim_membership.credit_vote == swim_credit_vote
    assert swim_membership.debtit_vote == old_debtit_vote


def test_MemberShip_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # ESTABLISH
    swim_str = ",swim"
    swim_credit_vote = 3.0
    swim_debtit_vote = 5.0
    swim_membership = membership_shop(
        group_label=swim_str,
        credit_vote=swim_credit_vote,
        debtit_vote=swim_debtit_vote,
    )

    print(f"{swim_membership}")

    # WHEN
    swim_dict = swim_membership.get_dict()

    # THEN
    assert swim_dict is not None
    assert swim_dict == {
        "group_label": swim_membership.group_label,
        "credit_vote": swim_membership.credit_vote,
        "debtit_vote": swim_membership.debtit_vote,
    }


def test_membership_get_from_dict_ReturnsObj():
    # ESTABLISH
    swim_str = ",swim"
    swim_credit_vote = 3.0
    swim_debtit_vote = 5.0
    yao_str = "Yao"
    before_swim_membership = membership_shop(
        group_label=swim_str,
        credit_vote=swim_credit_vote,
        debtit_vote=swim_debtit_vote,
        acct_name=yao_str,
    )
    swim_membership_dict = before_swim_membership.get_dict()

    # WHEN
    after_swim_membership = membership_get_from_dict(swim_membership_dict, yao_str)

    # THEN
    assert before_swim_membership == after_swim_membership
    assert after_swim_membership.group_label == swim_str


def test_memberships_get_from_dict_ReturnsObj():
    # ESTABLISH
    swim_str = ",swim"
    swim_credit_vote = 3.0
    swim_debtit_vote = 5.0
    yao_str = "Yao"
    before_swim_membership = membership_shop(
        group_label=swim_str,
        credit_vote=swim_credit_vote,
        debtit_vote=swim_debtit_vote,
        acct_name=yao_str,
    )
    before_swim_memberships_objs = {swim_str: before_swim_membership}
    swim_memberships_dict = {swim_str: before_swim_membership.get_dict()}

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
    bikers_awardlink = AwardLink(awardee_label=bikers_str)

    # THEN
    assert bikers_awardlink.awardee_label == bikers_str
    assert bikers_awardlink.give_force == 1.0
    assert bikers_awardlink.take_force == 1.0


def test_awardlink_shop_ReturnsObj():
    # ESTABLISH
    bikers_str = "bikers"
    bikers_give_force = 3.0
    bikers_take_force = 5.0

    # WHEN
    bikers_awardlink = awardlink_shop(
        awardee_label=bikers_str,
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
    assert not x_awardheir.awardee_label
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
        awardee_label=bikers_str,
        give_force=bikers_give_force,
        take_force=bikers_take_force,
    )

    # WHEN
    assert x_awardheir.awardee_label == bikers_str
    assert x_awardheir.give_force == bikers_give_force
    assert x_awardheir.take_force == bikers_take_force


def test_AwardLink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # ESTABLISH
    bikers_str = "bikers"
    bikers_give_force = 3.0
    bikers_take_force = 5.0
    bikers_awardlink = awardlink_shop(
        awardee_label=bikers_str,
        give_force=bikers_give_force,
        take_force=bikers_take_force,
    )

    print(f"{bikers_awardlink}")

    # WHEN
    biker_dict = bikers_awardlink.get_dict()

    # THEN
    assert biker_dict is not None
    assert biker_dict == {
        "awardee_label": bikers_awardlink.awardee_label,
        "give_force": bikers_awardlink.give_force,
        "take_force": bikers_awardlink.take_force,
    }


def test_awardlinks_get_from_JSON_ReturnsObj_SimpleExample():
    # ESTABLISH
    teacher_str = "teachers"
    teacher_awardlink = awardlink_shop(
        awardee_label=teacher_str, give_force=103, take_force=155
    )
    teacher_dict = teacher_awardlink.get_dict()
    awardlinks_dict = {teacher_awardlink.awardee_label: teacher_dict}

    teachers_json = get_json_from_dict(awardlinks_dict)
    assert teachers_json is not None
    assert x_is_json(teachers_json)

    # WHEN
    awardlinks_obj_dict = awardlinks_get_from_json(awardlinks_json=teachers_json)

    # THEN
    assert awardlinks_obj_dict is not None
    teachers_obj_check_dict = {teacher_awardlink.awardee_label: teacher_awardlink}
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
        awardee_label=bikers_str,
        _fund_give=bikers_fund_give,
        _fund_take=bikers_fund_take,
    )

    # THEN
    assert bikers_awardline.awardee_label == bikers_str
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
        awardee_label=bikers_str,
        _fund_give=bikers_fund_give,
        _fund_take=bikers_fund_take,
    )

    assert biker_awardline is not None
    assert biker_awardline.awardee_label == bikers_str
    assert biker_awardline._fund_give == bikers_fund_give
    assert biker_awardline._fund_take == bikers_fund_take


def test_AwardLine_add_fund_give_take_CorrectlyModifiesAttr():
    # ESTABLISH
    bikers_str = "bikers"
    bikers_awardline = awardline_shop(
        awardee_label=bikers_str, _fund_give=0.33, _fund_take=0.55
    )
    assert bikers_awardline.awardee_label == bikers_str
    assert bikers_awardline._fund_give == 0.33
    assert bikers_awardline._fund_take == 0.55

    # WHEN
    bikers_awardline.add_fund_give_take(fund_give=0.11, fund_take=0.2)

    # THEN
    assert bikers_awardline._fund_give == 0.44
    assert bikers_awardline._fund_take == 0.75
