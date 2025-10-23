from src.ch03_voice.group import (
    AwardHeir,
    AwardLine,
    AwardUnit,
    GroupCore,
    GroupTitle,
    MemberShip,
    awardheir_shop,
    awardline_shop,
    awardunit_shop,
    get_awardunits_from_dict,
    membership_get_from_dict,
    membership_shop,
    memberships_get_from_dict,
)
from src.ref.keywords import Ch03Keywords as kw


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
    assert swim_membership.group_cred_lumen == 1.0
    assert swim_membership.group_debt_lumen == 1.0
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
        kw.voice_name,
        kw.group_title,
        kw.group_cred_lumen,
        kw.group_debt_lumen,
        kw.credor_pool,
        kw.debtor_pool,
        kw.fund_agenda_give,
        kw.fund_agenda_ratio_give,
        kw.fund_agenda_ratio_take,
        kw.fund_agenda_take,
        kw.fund_give,
        kw.fund_take,
    }


def test_membership_shop_ReturnsObj():
    # ESTABLISH
    swim_str = ",swim"
    swim_group_cred_lumen = 3.0
    swim_group_debt_lumen = 5.0

    # WHEN
    swim_membership = membership_shop(
        group_title=swim_str,
        group_cred_lumen=swim_group_cred_lumen,
        group_debt_lumen=swim_group_debt_lumen,
    )

    # THEN
    assert swim_membership.group_cred_lumen == swim_group_cred_lumen
    assert swim_membership.group_debt_lumen == swim_group_debt_lumen
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


def test_MemberShip_set_group_cred_lumen_SetsAttr():
    # ESTABLISH
    swim_str = ",swim"
    old_group_cred_lumen = 3.0
    swim_group_debt_lumen = 5.0
    swim_membership = membership_shop(
        swim_str, old_group_cred_lumen, swim_group_debt_lumen
    )
    assert swim_membership.group_cred_lumen == old_group_cred_lumen
    assert swim_membership.group_debt_lumen == swim_group_debt_lumen

    # WHEN
    new_swim_group_cred_lumen = 44
    swim_membership.set_group_cred_lumen(new_swim_group_cred_lumen)

    # THEN
    assert swim_membership.group_cred_lumen == new_swim_group_cred_lumen
    assert swim_membership.group_debt_lumen == swim_group_debt_lumen


def test_MemberShip_set_group_cred_lumen_NoneParameter():
    # ESTABLISH
    swim_str = ",swim"
    old_group_cred_lumen = 3.0
    swim_group_debt_lumen = 5.0
    swim_membership = membership_shop(
        swim_str, old_group_cred_lumen, swim_group_debt_lumen
    )
    assert swim_membership.group_cred_lumen == old_group_cred_lumen
    assert swim_membership.group_debt_lumen == swim_group_debt_lumen

    # WHEN
    swim_membership.set_group_cred_lumen(None)

    # THEN
    assert swim_membership.group_cred_lumen == old_group_cred_lumen
    assert swim_membership.group_debt_lumen == swim_group_debt_lumen


def test_MemberShip_set_group_debt_lumen_SetsAttr():
    # ESTABLISH
    swim_str = ",swim"
    swim_group_cred_lumen = 3.0
    old_group_debt_lumen = 5.0
    swim_membership = membership_shop(
        swim_str, swim_group_cred_lumen, old_group_debt_lumen
    )
    assert swim_membership.group_cred_lumen == swim_group_cred_lumen
    assert swim_membership.group_debt_lumen == old_group_debt_lumen

    # WHEN
    new_group_debt_lumen = 55
    swim_membership.set_group_debt_lumen(new_group_debt_lumen)

    # THEN
    assert swim_membership.group_cred_lumen == swim_group_cred_lumen
    assert swim_membership.group_debt_lumen == new_group_debt_lumen


def test_MemberShip_set_group_debt_lumen_DoesNotSetsAttrNone():
    # ESTABLISH
    swim_str = ",swim"
    swim_group_cred_lumen = 3.0
    old_group_debt_lumen = 5.0
    swim_membership = membership_shop(
        swim_str, swim_group_cred_lumen, old_group_debt_lumen
    )
    assert swim_membership.group_cred_lumen == swim_group_cred_lumen
    assert swim_membership.group_debt_lumen == old_group_debt_lumen

    # WHEN
    swim_membership.set_group_debt_lumen(None)

    # THEN
    assert swim_membership.group_cred_lumen == swim_group_cred_lumen
    assert swim_membership.group_debt_lumen == old_group_debt_lumen


def test_MemberShip_to_dict_ReturnsDictWithNecessaryDataForJSON():
    # ESTABLISH
    swim_str = ",swim"
    swim_group_cred_lumen = 3.0
    swim_group_debt_lumen = 5.0
    swim_membership = membership_shop(
        group_title=swim_str,
        group_cred_lumen=swim_group_cred_lumen,
        group_debt_lumen=swim_group_debt_lumen,
    )

    print(f"{swim_membership}")

    # WHEN
    swim_dict = swim_membership.to_dict()

    # THEN
    assert swim_dict is not None
    assert swim_dict == {
        kw.group_title: swim_membership.group_title,
        kw.group_cred_lumen: swim_membership.group_cred_lumen,
        kw.group_debt_lumen: swim_membership.group_debt_lumen,
    }


def test_membership_to_dict_ReturnsObj():
    # ESTABLISH
    swim_str = ",swim"
    swim_group_cred_lumen = 3.0
    swim_group_debt_lumen = 5.0
    yao_str = "Yao"
    before_swim_membership = membership_shop(
        group_title=swim_str,
        group_cred_lumen=swim_group_cred_lumen,
        group_debt_lumen=swim_group_debt_lumen,
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
    swim_group_cred_lumen = 3.0
    swim_group_debt_lumen = 5.0
    yao_str = "Yao"
    before_swim_membership = membership_shop(
        group_title=swim_str,
        group_cred_lumen=swim_group_cred_lumen,
        group_debt_lumen=swim_group_debt_lumen,
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


def test_MemberShip_clear_membership_fund_give_take_SetsAttr():
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
    bob_membership.clear_membership_fund_give_take()

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
    assert x_awardheir.__dict__ == {
        kw.awardee_title: None,
        kw.give_force: 1,
        kw.take_force: 1,
        kw.fund_give: None,
        kw.fund_take: None,
    }


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
        kw.awardee_title: bikers_awardunit.awardee_title,
        kw.give_force: bikers_awardunit.give_force,
        kw.take_force: bikers_awardunit.take_force,
    }


def test_get_awardunits_from_dict_ReturnsObj_SimpleExample():
    # ESTABLISH
    teacher_str = "teachers"
    teacher_awardunit = awardunit_shop(
        awardee_title=teacher_str, give_force=103, take_force=155
    )
    teacher_dict = teacher_awardunit.to_dict()
    awards_dict = {teacher_awardunit.awardee_title: teacher_dict}

    # WHEN
    awardunits_obj_dict = get_awardunits_from_dict(awards_dict)

    # THEN
    assert awardunits_obj_dict is not None
    expected_dict = {teacher_awardunit.awardee_title: teacher_awardunit}
    print(f"{awardunits_obj_dict=}")
    print(f"      {expected_dict=}")
    assert awardunits_obj_dict == expected_dict


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
    assert bikers_awardline.__dict__ == {
        kw.awardee_title: bikers_str,
        kw.fund_give: bikers_fund_give,
        kw.fund_take: bikers_fund_take,
    }


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
