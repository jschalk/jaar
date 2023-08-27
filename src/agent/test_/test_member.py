from src.agent.member import (
    MemberUnit,
    MemberName,
    memberlink_shop,
    memberunit_shop,
    memberlinks_get_from_json,
    memberunits_get_from_json,
    memberrings_get_from_json,
    MemberRing,
)
from src.agent.x_func import x_is_json, x_get_json
from pytest import raises as pytest_raises


def test_MemberName_exists():
    cersei_name = MemberName("Cersei")
    assert cersei_name != None
    assert str(type(cersei_name)).find(".member.MemberName") > 0


def test_memberrings_exists():
    cersei_name = MemberName("Cersei")
    friend_link = MemberRing(name=cersei_name)
    assert friend_link.name == cersei_name


def test_memberrings_get_dict_ReturnsDictWithNecessaryDataForJSON():
    member_name = MemberName("bob")
    member_ring = MemberRing(name=member_name)
    print(f"{member_ring}")
    x_dict = member_ring.get_dict()
    assert x_dict != None
    assert x_dict == {"name": str(member_name)}


def test_memberrings_get_from_JSON_SimpleExampleWorks():
    marie_str = "Marie"
    marie_json_dict = {marie_str: {"name": marie_str}}
    # marie_json_dict = {marie_str: {"name": marie_str, "external_name": marie_str}}
    marie_json_str = x_get_json(dict_x=marie_json_dict)
    assert x_is_json(json_x=marie_json_str)

    marie_obj_dict = memberrings_get_from_json(memberrings_json=marie_json_str)
    assert marie_obj_dict != None

    marie_name = MemberName(marie_str)
    marie_memberring = MemberRing(name=marie_name)
    memberrings_dict = {marie_memberring.name: marie_memberring}
    assert marie_obj_dict == memberrings_dict


def test_MemberUnit_exists():
    # GIVEN
    bob_name = "bob"

    # WHEN
    bob_member = MemberUnit(name=bob_name)

    # THEN
    print(f"{bob_name}")
    assert bob_member != None
    assert bob_member.name != None
    assert bob_member.name == bob_name
    assert bob_member.creditor_weight is None
    assert bob_member.debtor_weight is None
    assert bob_member._agent_credit is None
    assert bob_member._agent_debt is None
    assert bob_member._agent_agenda_credit is None
    assert bob_member._agent_agenda_debt is None
    assert bob_member._creditor_active is None
    assert bob_member._debtor_active is None
    assert bob_member._memberrings is None
    assert bob_member.external_name == bob_name
    assert bob_member._bank_tax_paid is None
    assert bob_member._bank_tax_diff is None


def test_MemberUnit_set_empty_agent_credit_debt_to_zero_CorrectlySetsZero():
    # GIVEN
    bob_name = "bob"
    bob_member = memberunit_shop(name=bob_name)
    assert bob_member._agent_credit is None
    assert bob_member._agent_debt is None
    assert bob_member._agent_agenda_credit is None
    assert bob_member._agent_agenda_debt is None
    assert bob_member._agent_agenda_ratio_credit is None
    assert bob_member._agent_agenda_ratio_debt is None

    # WHEN
    bob_member.set_empty_agent_credit_debt_to_zero()

    # THEN
    assert bob_member._agent_credit == 0
    assert bob_member._agent_debt == 0
    assert bob_member._agent_agenda_credit == 0
    assert bob_member._agent_agenda_debt == 0
    assert bob_member._agent_agenda_ratio_credit == 0
    assert bob_member._agent_agenda_ratio_debt == 0

    # GIVEN
    bob_member._agent_credit = 0.27
    bob_member._agent_debt = 0.37
    bob_member._agent_agenda_credit = 0.41
    bob_member._agent_agenda_debt = 0.51
    bob_member._agent_agenda_ratio_credit = 0.23
    bob_member._agent_agenda_ratio_debt = 0.87
    assert bob_member._agent_credit == 0.27
    assert bob_member._agent_debt == 0.37
    assert bob_member._agent_agenda_credit == 0.41
    assert bob_member._agent_agenda_debt == 0.51
    assert bob_member._agent_agenda_ratio_credit == 0.23
    assert bob_member._agent_agenda_ratio_debt == 0.87

    # WHEN
    bob_member.set_empty_agent_credit_debt_to_zero()

    # THEN
    assert bob_member._agent_credit == 0.27
    assert bob_member._agent_debt == 0.37
    assert bob_member._agent_agenda_credit == 0.41
    assert bob_member._agent_agenda_debt == 0.51
    assert bob_member._agent_agenda_ratio_credit == 0.23
    assert bob_member._agent_agenda_ratio_debt == 0.87


def test_MemberUnit_reset_agent_credit_debt_MethodWorkCorrectly():
    # GIVEN
    bob_name = "bob"
    bob_member = memberunit_shop(name=bob_name)
    bob_member._agent_credit = 0.27
    bob_member._agent_debt = 0.37
    bob_member._agent_agenda_credit = 0.41
    bob_member._agent_agenda_debt = 0.51
    bob_member._agent_agenda_ratio_credit = 0.433
    bob_member._agent_agenda_ratio_debt = 0.533
    assert bob_member._agent_credit == 0.27
    assert bob_member._agent_debt == 0.37
    assert bob_member._agent_agenda_credit == 0.41
    assert bob_member._agent_agenda_debt == 0.51
    assert bob_member._agent_agenda_ratio_credit == 0.433
    assert bob_member._agent_agenda_ratio_debt == 0.533

    # WHEN
    bob_member.reset_agent_credit_debt()

    # THEN
    assert bob_member._agent_credit == 0
    assert bob_member._agent_debt == 0
    assert bob_member._agent_agenda_credit == 0
    assert bob_member._agent_agenda_debt == 0
    assert bob_member._agent_agenda_ratio_credit == 0
    assert bob_member._agent_agenda_ratio_debt == 0


def test_MemberUnit_add_agent_credit_debt_MethodWorkCorrectly():
    # GIVEN
    bob_name = "bob"
    bob_member = memberunit_shop(name=bob_name)
    bob_member._agent_credit = 0.4106
    bob_member._agent_debt = 0.1106
    bob_member._agent_agenda_credit = 0.41
    bob_member._agent_agenda_debt = 0.51
    assert bob_member._agent_agenda_credit == 0.41
    assert bob_member._agent_agenda_debt == 0.51

    # WHEN
    bob_member.add_agent_credit_debt(
        agent_credit=0.33,
        agent_debt=0.055,
        agent_agenda_credit=0.3,
        agent_agenda_debt=0.05,
    )

    # THEN
    assert bob_member._agent_credit == 0.7406
    assert bob_member._agent_debt == 0.1656
    assert bob_member._agent_agenda_credit == 0.71
    assert bob_member._agent_agenda_debt == 0.56


def test_MemberUnit_set_agent_agenda_ratio_credit_debt_MethodWorkCorrectly():
    # GIVEN
    bob_name = "bob"
    bob_member = memberunit_shop(
        name=bob_name,
        creditor_weight=15,
        debtor_weight=7,
        _agent_credit=0.4106,
        _agent_debt=0.1106,
        _agent_agenda_credit=0.041,
        _agent_agenda_debt=0.051,
        _agent_agenda_ratio_credit=0,
        _agent_agenda_ratio_debt=0,
    )
    assert bob_member._agent_agenda_ratio_credit == 0
    assert bob_member._agent_agenda_ratio_debt == 0

    # WHEN
    bob_member.set_agent_agenda_ratio_credit_debt(
        agent_agenda_ratio_credit_sum=0.2,
        agent_agenda_ratio_debt_sum=0.5,
        agent_memberunit_total_creditor_weight=20,
        agent_memberunit_total_debtor_weight=14,
    )

    # THEN
    assert bob_member._agent_agenda_ratio_credit == 0.205
    assert bob_member._agent_agenda_ratio_debt == 0.102

    # WHEN
    bob_member.set_agent_agenda_ratio_credit_debt(
        agent_agenda_ratio_credit_sum=0,
        agent_agenda_ratio_debt_sum=0,
        agent_memberunit_total_creditor_weight=20,
        agent_memberunit_total_debtor_weight=14,
    )

    # THEN
    assert bob_member._agent_agenda_ratio_credit == 0.75
    assert bob_member._agent_agenda_ratio_debt == 0.5


def test_MemberUnit_set_banking_data_MethodWorkCorrectly():
    # GIVEN
    bob_name = "bob"
    bob_member = memberunit_shop(
        name=bob_name,
        _agent_agenda_ratio_credit=0.077,
        _agent_agenda_ratio_debt=0.066,
    )
    assert bob_member._agent_agenda_ratio_credit == 0.077
    assert bob_member._agent_agenda_ratio_debt == 0.066
    assert bob_member._bank_tax_paid is None
    assert bob_member._bank_tax_diff is None

    # WHEN
    tax_paid_v1 = 0.2
    tax_diff = 0.123
    bob_member.set_banking_data(tax_paid=tax_paid_v1, tax_diff=tax_diff)
    # THEN
    assert bob_member._agent_agenda_ratio_credit == 0.077
    assert bob_member._agent_agenda_ratio_debt == 0.066
    assert bob_member._bank_tax_paid == tax_paid_v1
    assert bob_member._bank_tax_diff == tax_diff

    # tax_paid_v2 = 0.3

    # # WHEN / Then
    # with pytest_raises(Exception) as excinfo:
    #     bob_member.set_banking_data(tax_paid=tax_paid_v2, tax_diff=tax_diff)
    # assert (
    #     str(excinfo.value)
    #     == f"MemberUnit.set_banking_data fail: tax_paid={tax_paid_v2} + tax_diff={tax_diff} not equal to _agent_agenda_ratio_credit={bob_member._agent_agenda_ratio_credit}"
    # )


def test_MemberUnit_clear_banking_data_MethodWorkCorrectly():
    # GIVEN
    bob_name = "bob"
    bob_member = memberunit_shop(
        name=bob_name,
        _agent_agenda_ratio_credit=0.355,
        _agent_agenda_ratio_debt=0.066,
    )
    bob_member.set_banking_data(tax_paid=0.399, tax_diff=0.044)
    assert bob_member._bank_tax_paid == 0.399
    assert bob_member._bank_tax_diff == 0.044

    # WHEN
    bob_member.clear_banking_data()

    # THEN
    assert bob_member._bank_tax_paid is None
    assert bob_member._bank_tax_diff is None


def test_MemberUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    glen_str = "glen"
    glen_ring = MemberRing(name=glen_str)
    member_rings = {glen_ring.name: glen_ring}
    bob_str = "bob"
    bank_tax_paid = 0.55
    bank_tax_diff = 0.66
    bob_member = memberunit_shop(
        name=bob_str,
        uid=652,
        creditor_weight=13,
        debtor_weight=17,
        _creditor_active=False,
        _debtor_active=True,
        _memberrings=member_rings,
        _bank_tax_paid=bank_tax_paid,
        _bank_tax_diff=bank_tax_diff,
    )
    print(f"{bob_str}")
    x_dict = bob_member.get_dict()
    print(f"{x_dict=}")
    assert x_dict != None
    assert x_dict == {
        "name": bob_str,
        "uid": 652,
        "creditor_weight": 13,
        "debtor_weight": 17,
        "_creditor_active": False,
        "_debtor_active": True,
        "_memberrings": {"glen": {"name": "glen"}},
        "external_name": bob_str,
        "_bank_tax_paid": bank_tax_paid,
        "_bank_tax_diff": bank_tax_diff,
    }


def test_MemberUnisshop_get_from_JSON_SimpleExampleWorks():
    cersei_name = MemberName("Cersei")
    cersei_external = "Cersei Lan"
    member_rings = {cersei_name: {"name": cersei_name}}
    marie_str = "Marie"
    bank_tax_paid = 0.55
    bank_tax_diff = 0.66
    marie_json_dict = {
        marie_str: {
            "name": marie_str,
            "uid": 103,
            "creditor_weight": 17,
            "debtor_weight": 17,
            "_creditor_active": False,
            "_debtor_active": True,
            "_memberrings": member_rings,
            "external_name": cersei_external,
            "_bank_tax_paid": bank_tax_paid,
            "_bank_tax_diff": bank_tax_diff,
        }
    }
    marie_json_str = x_get_json(dict_x=marie_json_dict)
    assert x_is_json(json_x=marie_json_str)


def test_MemberUnisshop_get_from_JSON_SimpleExampleWorksWithIncompleteData():
    # GIVEN
    cersei_name = MemberName("Cersei")
    member_rings = {cersei_name: {"name": None}}
    marie_text = "Marie"
    bank_tax_paid = 0.55
    bank_tax_diff = 0.66
    marie_json_dict = {
        marie_text: {
            "name": marie_text,
            "uid": 103,
            "creditor_weight": 17,
            "debtor_weight": 15,
            "_creditor_active": False,
            "_debtor_active": True,
            "_bank_tax_paid": bank_tax_paid,
            "_bank_tax_diff": bank_tax_diff,
        }
    }

    # WHEN
    marie_json_str = x_get_json(dict_x=marie_json_dict)

    # THEN
    assert x_is_json(json_x=marie_json_str)

    marie_obj_dict = memberunits_get_from_json(memberunits_json=marie_json_str)
    assert marie_obj_dict[marie_text] != None
    assert marie_obj_dict[marie_text].creditor_weight == 17
    assert marie_obj_dict[marie_text].debtor_weight == 15
    assert marie_obj_dict[marie_text]._creditor_active == False
    assert marie_obj_dict[marie_text]._debtor_active == True
    assert marie_obj_dict[marie_text]._bank_tax_paid == 0.55
    assert marie_obj_dict[marie_text]._bank_tax_diff == 0.66
    # assert marie_obj_dict[marie_text]._memberrings == member_rings


def test_MemberLink_exists():
    # GIVEN
    bikers_name = MemberName("Marie")

    # WHEN
    member_link_x = memberlink_shop(name=bikers_name)

    # THEN
    assert member_link_x.name == bikers_name
    assert member_link_x.creditor_weight == 1.0
    assert member_link_x.debtor_weight == 1.0

    # WHEN
    bikers_creditor_weight = 3.0
    bikers_debtor_weight = 5.0
    member_link_x = memberlink_shop(
        name=bikers_name,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debtor_weight,
        _agent_credit=0.7,
        _agent_debt=0.51,
        _agent_agenda_credit=0.66,
        _agent_agenda_debt=0.55,
    )

    # THEN
    assert member_link_x.creditor_weight == bikers_creditor_weight
    assert member_link_x.debtor_weight == bikers_debtor_weight
    assert member_link_x._agent_credit != None
    assert member_link_x._agent_credit == 0.7
    assert member_link_x._agent_debt == 0.51
    assert member_link_x._agent_agenda_credit == 0.66
    assert member_link_x._agent_agenda_debt == 0.55


def test_memberlink_shop_set_agent_credit_debt_CorrectlyWorks():
    # GIVEN
    bikers_name = MemberName("Marie")
    bikers_creditor_weight = 3.0
    memberlinks_sum_creditor_weight = 60
    group_agent_credit = 0.5
    group_agent_agenda_credit = 0.98

    bikers_debtor_weight = 13.0
    memberlinks_sum_debtor_weight = 26.0
    group_agent_debt = 0.9
    group_agent_agenda_debt = 0.5151

    member_link_x = memberlink_shop(
        name=bikers_name,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debtor_weight,
    )
    assert member_link_x._agent_credit is None
    assert member_link_x._agent_debt is None
    assert member_link_x._agent_agenda_credit is None
    assert member_link_x._agent_agenda_debt is None

    # WHEN
    member_link_x.set_agent_credit_debt(
        memberlinks_creditor_weight_sum=memberlinks_sum_creditor_weight,
        memberlinks_debtor_weight_sum=memberlinks_sum_debtor_weight,
        group_agent_credit=group_agent_credit,
        group_agent_debt=group_agent_debt,
        group_agent_agenda_credit=group_agent_agenda_credit,
        group_agent_agenda_debt=group_agent_agenda_debt,
    )

    # THEN
    assert member_link_x._agent_credit == 0.025
    assert member_link_x._agent_debt == 0.45
    assert member_link_x._agent_agenda_credit == 0.049
    assert member_link_x._agent_agenda_debt == 0.25755


def test_memberlink_shop_reset_agent_credit_debt():
    # GIVEN
    biker_name = "maria"
    biker_member = memberlink_shop(name=biker_name, _agent_credit=0.04, _agent_debt=0.7)
    print(f"{biker_member}")

    assert biker_member._agent_credit != None
    assert biker_member._agent_debt != None

    # WHEN
    biker_member.reset_agent_credit_debt()

    # THEN
    assert biker_member._agent_credit == 0
    assert biker_member._agent_debt == 0


def test_memberlink_shop_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    str_name = "Marie"
    biker_name = MemberName(str_name)
    biker_member_link = memberlink_shop(
        name=biker_name, creditor_weight=12, debtor_weight=19
    )
    print(f"{biker_member_link}")

    # WHEN
    biker_dict = biker_member_link.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "name": biker_name,
        "creditor_weight": 12,
        "debtor_weight": 19,
    }


def test_memberlink_get_from_JSON_SimpleExampleWorks():
    # GIVEN
    marie_str = "Marie"
    marie_json_dict = {
        marie_str: {"name": marie_str, "creditor_weight": 12, "debtor_weight": 19}
    }
    marie_json_str = x_get_json(dict_x=marie_json_dict)
    assert x_is_json(json_x=marie_json_str)

    # WHEN
    marie_obj_dict = memberlinks_get_from_json(memberlinks_json=marie_json_str)

    # THEN
    assert marie_obj_dict != None

    marie_name = MemberName(marie_str)
    marie_memberlink = memberlink_shop(
        name=marie_name, creditor_weight=12, debtor_weight=19
    )
    memberlinks_dict = {marie_memberlink.name: marie_memberlink}
    assert marie_obj_dict == memberlinks_dict


def test_memberlink_meld_RaiseSameNameException():
    # GIVEN
    todd_text = "Todd"
    todd_member = memberlink_shop(name=todd_text)
    mery_text = "Merry"
    mery_member = memberlink_shop(name=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_member.meld(mery_member)
    assert (
        str(excinfo.value)
        == f"Meld fail MemberLink='{todd_member.name}' not the same as MemberLink='{mery_member.name}"
    )


def test_memberlink_meld_CorrectlySumsWeights():
    # GIVEN
    todd_text = "Todd"
    todd_member1 = memberlink_shop(name=todd_text, creditor_weight=12, debtor_weight=19)
    todd_member2 = memberlink_shop(name=todd_text, creditor_weight=33, debtor_weight=3)
    assert todd_member1.creditor_weight == 12
    assert todd_member1.debtor_weight == 19

    # WHEN
    todd_member1.meld(todd_member2)

    # THEN
    assert todd_member1.creditor_weight == 45
    assert todd_member1.debtor_weight == 22


def test_memberunit_meld_RaiseSameNameException():
    # GIVEN
    todd_text = "Todd"
    todd_member = memberunit_shop(name=todd_text)
    mery_text = "Merry"
    mery_member = memberunit_shop(name=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_member.meld(mery_member)
    assert (
        str(excinfo.value)
        == f"Meld fail MemberUnit='{todd_member.name}' not the same as MemberUnit='{mery_member.name}"
    )


def test_memberunit_meld_CorrectlySumsWeights():
    # GIVEN
    todd_text = "Todd"
    todd_member1 = memberunit_shop(name=todd_text, creditor_weight=7, debtor_weight=19)
    todd_member2 = memberunit_shop(name=todd_text, creditor_weight=5, debtor_weight=3)
    assert todd_member1.creditor_weight == 7
    assert todd_member1.debtor_weight == 19

    # WHEN
    todd_member1.meld(todd_member2)

    # THEN
    assert todd_member1.creditor_weight == 12
    assert todd_member1.debtor_weight == 22
