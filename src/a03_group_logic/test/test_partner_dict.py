from src.a00_data_toolbox.dict_toolbox import get_json_from_dict, x_is_json
from src.a03_group_logic.group import membership_shop
from src.a03_group_logic.partner import (
    partnerunit_get_from_dict,
    partnerunit_shop,
    partnerunits_get_from_dict,
    partnerunits_get_from_json,
)


def test_PartnerUnit_get_memberships_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_group_cred_points = 11
    sue_group_debt_points = 13
    run_str = ";Run"
    run_group_cred_points = 17
    run_group_debt_points = 23
    sue_membership = membership_shop(
        sue_str, sue_group_cred_points, sue_group_debt_points
    )
    run_membership = membership_shop(
        run_str, run_group_cred_points, run_group_debt_points
    )
    sue_partnerunit = partnerunit_shop(sue_str)
    sue_partnerunit.set_membership(sue_membership)
    sue_partnerunit.set_membership(run_membership)

    # WHEN
    sue_memberships_dict = sue_partnerunit.get_memberships_dict()

    # THEN
    assert sue_memberships_dict.get(sue_str) is not None
    assert sue_memberships_dict.get(run_str) is not None
    sue_membership_dict = sue_memberships_dict.get(sue_str)
    run_membership_dict = sue_memberships_dict.get(run_str)
    assert sue_membership_dict == {
        "group_title": sue_str,
        "group_cred_points": sue_group_cred_points,
        "group_debt_points": sue_group_debt_points,
    }
    assert run_membership_dict == {
        "group_title": run_str,
        "group_cred_points": run_group_cred_points,
        "group_debt_points": run_group_debt_points,
    }


def test_PartnerUnit_to_dict_ReturnsDictWithNecessaryDataForJSON():
    # ESTABLISH
    bob_str = "Bob"
    bob_partnerunit = partnerunit_shop(bob_str)

    bob_partner_cred_points = 13
    bob_partner_debt_points = 17
    bob_partnerunit.set_partner_cred_points(bob_partner_cred_points)
    bob_partnerunit.set_partner_debt_points(bob_partner_debt_points)

    print(f"{bob_str}")

    bob_partnerunit.set_membership(membership_shop(bob_str))
    run_str = ";Run"
    bob_partnerunit.set_membership(membership_shop(run_str))

    # WHEN
    x_dict = bob_partnerunit.to_dict()

    # THEN
    bl_dict = x_dict.get("_memberships")
    print(f"{bl_dict=}")
    assert x_dict is not None
    assert x_dict == {
        "partner_name": bob_str,
        "partner_cred_points": bob_partner_cred_points,
        "partner_debt_points": bob_partner_debt_points,
        "_memberships": {
            bob_str: {
                "group_title": bob_str,
                "group_cred_points": 1,
                "group_debt_points": 1,
            },
            run_str: {
                "group_title": run_str,
                "group_cred_points": 1,
                "group_debt_points": 1,
            },
        },
    }


def test_PartnerUnit_to_dict_ReturnsDictWithAllAttrDataForJSON():
    # ESTABLISH
    bob_str = "Bob"
    bob_partnerunit = partnerunit_shop(bob_str)

    bob_partner_cred_points = 13
    bob_partner_debt_points = 17
    bob_partnerunit.set_partner_cred_points(bob_partner_cred_points)
    bob_partnerunit.set_partner_debt_points(bob_partner_debt_points)
    bob_irrational_partner_debt_points = 87
    bob_inallocable_partner_debt_points = 97
    bob_partnerunit.add_irrational_partner_debt_points(
        bob_irrational_partner_debt_points
    )
    bob_partnerunit.add_inallocable_partner_debt_points(
        bob_inallocable_partner_debt_points
    )

    bob_fund_give = 55
    bob_fund_take = 47
    bob_fund_agenda_give = 51
    bob_fund_agenda_take = 67
    bob_fund_agenda_ratio_give = 71
    bob_fund_agenda_ratio_take = 73

    bob_partnerunit._fund_give = bob_fund_give
    bob_partnerunit._fund_take = bob_fund_take
    bob_partnerunit._fund_agenda_give = bob_fund_agenda_give
    bob_partnerunit._fund_agenda_take = bob_fund_agenda_take
    bob_partnerunit._fund_agenda_ratio_give = bob_fund_agenda_ratio_give
    bob_partnerunit._fund_agenda_ratio_take = bob_fund_agenda_ratio_take

    bob_partnerunit.set_membership(membership_shop(bob_str))
    run_str = ";Run"
    bob_partnerunit.set_membership(membership_shop(run_str))

    print(f"{bob_str}")

    # WHEN
    x_dict = bob_partnerunit.to_dict(all_attrs=True)

    # THEN
    print(f"{x_dict=}")
    assert x_dict is not None
    assert x_dict == {
        "partner_name": bob_str,
        "partner_cred_points": bob_partner_cred_points,
        "partner_debt_points": bob_partner_debt_points,
        "_memberships": bob_partnerunit.get_memberships_dict(),
        "_irrational_partner_debt_points": bob_irrational_partner_debt_points,
        "_inallocable_partner_debt_points": bob_inallocable_partner_debt_points,
        "_fund_give": bob_fund_give,
        "_fund_take": bob_fund_take,
        "_fund_agenda_give": bob_fund_agenda_give,
        "_fund_agenda_take": bob_fund_agenda_take,
        "_fund_agenda_ratio_give": bob_fund_agenda_ratio_give,
        "_fund_agenda_ratio_take": bob_fund_agenda_ratio_take,
    }


def test_PartnerUnit_to_dict_ReturnsDictWith__irrational_partner_debt_points_ValuesIsZero():
    # ESTABLISH
    bob_str = "Bob"
    bob_partnerunit = partnerunit_shop(bob_str)
    assert bob_partnerunit._irrational_partner_debt_points == 0
    assert bob_partnerunit._inallocable_partner_debt_points == 0

    # WHEN
    x_dict = bob_partnerunit.to_dict(all_attrs=True)

    # THEN
    x_irrational_partner_debt_points = "_irrational_partner_debt_points"
    x_inallocable_partner_debt_points = "_inallocable_partner_debt_points"
    assert x_dict.get(x_irrational_partner_debt_points) is None
    assert x_dict.get(x_inallocable_partner_debt_points) is None
    assert len(x_dict.keys()) == 10


def test_PartnerUnit_to_dict_ReturnsDictWith__irrational_partner_debt_points_ValuesIsNumber():
    # ESTABLISH
    bob_str = "Bob"
    bob_partnerunit = partnerunit_shop(bob_str)
    bob_irrational_partner_debt_points = 87
    bob_inallocable_partner_debt_points = 97
    bob_partnerunit.add_irrational_partner_debt_points(
        bob_irrational_partner_debt_points
    )
    bob_partnerunit.add_inallocable_partner_debt_points(
        bob_inallocable_partner_debt_points
    )

    # WHEN
    x_dict = bob_partnerunit.to_dict(all_attrs=True)

    # THEN
    x_irrational_partner_debt_points = "_irrational_partner_debt_points"
    x_inallocable_partner_debt_points = "_inallocable_partner_debt_points"
    assert (
        x_dict.get(x_irrational_partner_debt_points)
        == bob_irrational_partner_debt_points
    )
    assert (
        x_dict.get(x_inallocable_partner_debt_points)
        == bob_inallocable_partner_debt_points
    )
    assert len(x_dict.keys()) == 12


def test_PartnerUnit_to_dict_ReturnsDictWith__irrational_partner_debt_points_ValuesIsNone():
    # ESTABLISH
    bob_str = "Bob"
    bob_partnerunit = partnerunit_shop(bob_str)
    bob_partnerunit._irrational_partner_debt_points = None
    bob_partnerunit._inallocable_partner_debt_points = None

    # WHEN
    x_dict = bob_partnerunit.to_dict(all_attrs=True)

    # THEN
    x_irrational_partner_debt_points = "_irrational_partner_debt_points"
    x_inallocable_partner_debt_points = "_inallocable_partner_debt_points"
    assert x_dict.get(x_irrational_partner_debt_points) is None
    assert x_dict.get(x_inallocable_partner_debt_points) is None
    assert len(x_dict.keys()) == 10


def test_partnerunit_get_from_dict_ReturnsObjWith_knot():
    # ESTABLISH
    yao_str = ",Yao"
    slash_str = "/"
    before_yao_partnerunit = partnerunit_shop(yao_str, knot=slash_str)
    yao_dict = before_yao_partnerunit.to_dict()

    # WHEN
    after_yao_partnerunit = partnerunit_get_from_dict(yao_dict, slash_str)

    # THEN
    assert before_yao_partnerunit == after_yao_partnerunit
    assert after_yao_partnerunit.knot == slash_str


def test_partnerunit_get_from_dict_Returns_memberships():
    # ESTABLISH
    yao_str = ",Yao"
    slash_str = "/"
    before_yao_partnerunit = partnerunit_shop(yao_str, knot=slash_str)
    ohio_str = f"{slash_str}ohio"
    iowa_str = f"{slash_str}iowa"
    ohio_group_cred_points = 90
    ohio_group_debt_points = 901
    iowa_group_cred_points = 902
    iowa_group_debt_points = 903
    ohio_membership = membership_shop(
        ohio_str, ohio_group_cred_points, ohio_group_debt_points
    )
    iowa_membership = membership_shop(
        iowa_str, iowa_group_cred_points, iowa_group_debt_points
    )
    before_yao_partnerunit.set_membership(ohio_membership)
    before_yao_partnerunit.set_membership(iowa_membership)
    yao_dict = before_yao_partnerunit.to_dict()

    # WHEN
    after_yao_partnerunit = partnerunit_get_from_dict(yao_dict, slash_str)

    # THEN
    assert before_yao_partnerunit._memberships == after_yao_partnerunit._memberships
    assert before_yao_partnerunit == after_yao_partnerunit
    assert after_yao_partnerunit.knot == slash_str


def test_partnerunits_get_from_dict_ReturnsObjWith_knot():
    # ESTABLISH
    yao_str = ",Yao"
    slash_str = "/"
    yao_partnerunit = partnerunit_shop(yao_str, knot=slash_str)
    yao_dict = yao_partnerunit.to_dict()
    x_partnerunits_dict = {yao_str: yao_dict}

    # WHEN
    x_partnerunits_objs = partnerunits_get_from_dict(x_partnerunits_dict, slash_str)

    # THEN
    assert x_partnerunits_objs.get(yao_str) == yao_partnerunit
    assert x_partnerunits_objs.get(yao_str).knot == slash_str


def test_partnerunits_get_from_json_ReturnsObj_SimpleExampleWith_IncompleteData():
    # ESTABLISH
    yao_str = "Yao"
    yao_partner_cred_points = 13
    yao_partner_debt_points = 17
    yao_irrational_partner_debt_points = 87
    yao_inallocable_partner_debt_points = 97
    yao_json_dict = {
        yao_str: {
            "partner_name": yao_str,
            "partner_cred_points": yao_partner_cred_points,
            "partner_debt_points": yao_partner_debt_points,
            "_memberships": {},
            "_irrational_partner_debt_points": yao_irrational_partner_debt_points,
            "_inallocable_partner_debt_points": yao_inallocable_partner_debt_points,
        }
    }
    yao_json_str = get_json_from_dict(yao_json_dict)
    assert x_is_json(yao_json_str)

    # WHEN
    yao_obj_dict = partnerunits_get_from_json(partnerunits_json=yao_json_str)

    # THEN
    assert yao_obj_dict[yao_str] is not None
    yao_partnerunit = yao_obj_dict[yao_str]

    assert yao_partnerunit.partner_name == yao_str
    assert yao_partnerunit.partner_cred_points == yao_partner_cred_points
    assert yao_partnerunit.partner_debt_points == yao_partner_debt_points
    assert (
        yao_partnerunit._irrational_partner_debt_points
        == yao_irrational_partner_debt_points
    )
    assert (
        yao_partnerunit._inallocable_partner_debt_points
        == yao_inallocable_partner_debt_points
    )
