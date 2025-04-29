from src.a03_group_logic.group import membership_shop
from src.a03_group_logic.acct import (
    acctunit_shop,
    acctunits_get_from_json,
    acctunit_get_from_dict,
    acctunits_get_from_dict,
)
from src.a00_data_toolbox.dict_toolbox import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_AcctUnit_get_memberships_dict_ReturnObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_credit_vote = 11
    sue_debtit_vote = 13
    run_str = ";Run"
    run_credit_vote = 17
    run_debtit_vote = 23
    sue_membership = membership_shop(sue_str, sue_credit_vote, sue_debtit_vote)
    run_membership = membership_shop(run_str, run_credit_vote, run_debtit_vote)
    sue_acctunit = acctunit_shop(sue_str)
    sue_acctunit.set_membership(sue_membership)
    sue_acctunit.set_membership(run_membership)

    # WHEN
    sue_memberships_dict = sue_acctunit.get_memberships_dict()

    # THEN
    assert sue_memberships_dict.get(sue_str) is not None
    assert sue_memberships_dict.get(run_str) is not None
    sue_membership_dict = sue_memberships_dict.get(sue_str)
    run_membership_dict = sue_memberships_dict.get(run_str)
    assert sue_membership_dict == {
        "group_label": sue_str,
        "credit_vote": sue_credit_vote,
        "debtit_vote": sue_debtit_vote,
    }
    assert run_membership_dict == {
        "group_label": run_str,
        "credit_vote": run_credit_vote,
        "debtit_vote": run_debtit_vote,
    }


def test_AcctUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # ESTABLISH
    bob_str = "Bob"
    bob_acctunit = acctunit_shop(bob_str)

    bob_credit_belief = 13
    bob_debtit_belief = 17
    bob_acctunit.set_credit_belief(bob_credit_belief)
    bob_acctunit.set_debtit_belief(bob_debtit_belief)

    print(f"{bob_str}")

    bob_acctunit.set_membership(membership_shop(bob_str))
    run_str = ";Run"
    bob_acctunit.set_membership(membership_shop(run_str))

    # WHEN
    x_dict = bob_acctunit.get_dict()

    # THEN
    bl_dict = x_dict.get("_memberships")
    print(f"{bl_dict=}")
    assert x_dict is not None
    assert x_dict == {
        "acct_name": bob_str,
        "credit_belief": bob_credit_belief,
        "debtit_belief": bob_debtit_belief,
        "_memberships": {
            bob_str: {"group_label": bob_str, "credit_vote": 1, "debtit_vote": 1},
            run_str: {"group_label": run_str, "credit_vote": 1, "debtit_vote": 1},
        },
    }


def test_AcctUnit_get_dict_ReturnsDictWithAllAttrDataForJSON():
    # ESTABLISH
    bob_str = "Bob"
    bob_acctunit = acctunit_shop(bob_str)

    bob_credit_belief = 13
    bob_debtit_belief = 17
    bob_acctunit.set_credit_belief(bob_credit_belief)
    bob_acctunit.set_debtit_belief(bob_debtit_belief)
    bob_irrational_debtit_belief = 87
    bob_inallocable_debtit_belief = 97
    bob_acctunit.add_irrational_debtit_belief(bob_irrational_debtit_belief)
    bob_acctunit.add_inallocable_debtit_belief(bob_inallocable_debtit_belief)

    bob_fund_give = 55
    bob_fund_take = 47
    bob_fund_agenda_give = 51
    bob_fund_agenda_take = 67
    bob_fund_agenda_ratio_give = 71
    bob_fund_agenda_ratio_take = 73

    bob_acctunit._fund_give = bob_fund_give
    bob_acctunit._fund_take = bob_fund_take
    bob_acctunit._fund_agenda_give = bob_fund_agenda_give
    bob_acctunit._fund_agenda_take = bob_fund_agenda_take
    bob_acctunit._fund_agenda_ratio_give = bob_fund_agenda_ratio_give
    bob_acctunit._fund_agenda_ratio_take = bob_fund_agenda_ratio_take

    bob_acctunit.set_membership(membership_shop(bob_str))
    run_str = ";Run"
    bob_acctunit.set_membership(membership_shop(run_str))

    print(f"{bob_str}")

    # WHEN
    x_dict = bob_acctunit.get_dict(all_attrs=True)

    # THEN
    print(f"{x_dict=}")
    assert x_dict is not None
    assert x_dict == {
        "acct_name": bob_str,
        "credit_belief": bob_credit_belief,
        "debtit_belief": bob_debtit_belief,
        "_memberships": bob_acctunit.get_memberships_dict(),
        "_irrational_debtit_belief": bob_irrational_debtit_belief,
        "_inallocable_debtit_belief": bob_inallocable_debtit_belief,
        "_fund_give": bob_fund_give,
        "_fund_take": bob_fund_take,
        "_fund_agenda_give": bob_fund_agenda_give,
        "_fund_agenda_take": bob_fund_agenda_take,
        "_fund_agenda_ratio_give": bob_fund_agenda_ratio_give,
        "_fund_agenda_ratio_take": bob_fund_agenda_ratio_take,
    }


def test_AcctUnit_get_dict_ReturnsDictWith_irrational_missing_plan_ValuesIsZerp():
    # ESTABLISH
    bob_str = "Bob"
    bob_acctunit = acctunit_shop(bob_str)
    assert bob_acctunit._irrational_debtit_belief == 0
    assert bob_acctunit._inallocable_debtit_belief == 0

    # WHEN
    x_dict = bob_acctunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtit_belief = "_irrational_debtit_belief"
    x_inallocable_debtit_belief = "_inallocable_debtit_belief"
    assert x_dict.get(x_irrational_debtit_belief) is None
    assert x_dict.get(x_inallocable_debtit_belief) is None
    assert len(x_dict.keys()) == 10


def test_AcctUnit_get_dict_ReturnsDictWith_irrational_missing_plan_ValuesIsNumber():
    # ESTABLISH
    bob_str = "Bob"
    bob_acctunit = acctunit_shop(bob_str)
    bob_irrational_debtit_belief = 87
    bob_inallocable_debtit_belief = 97
    bob_acctunit.add_irrational_debtit_belief(bob_irrational_debtit_belief)
    bob_acctunit.add_inallocable_debtit_belief(bob_inallocable_debtit_belief)

    # WHEN
    x_dict = bob_acctunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtit_belief = "_irrational_debtit_belief"
    x_inallocable_debtit_belief = "_inallocable_debtit_belief"
    assert x_dict.get(x_irrational_debtit_belief) == bob_irrational_debtit_belief
    assert x_dict.get(x_inallocable_debtit_belief) == bob_inallocable_debtit_belief
    assert len(x_dict.keys()) == 12


def test_AcctUnit_get_dict_ReturnsDictWith_irrational_missing_plan_ValuesIsNone():
    # ESTABLISH
    bob_str = "Bob"
    bob_acctunit = acctunit_shop(bob_str)
    bob_acctunit._irrational_debtit_belief = None
    bob_acctunit._inallocable_debtit_belief = None

    # WHEN
    x_dict = bob_acctunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtit_belief = "_irrational_debtit_belief"
    x_inallocable_debtit_belief = "_inallocable_debtit_belief"
    assert x_dict.get(x_irrational_debtit_belief) is None
    assert x_dict.get(x_inallocable_debtit_belief) is None
    assert len(x_dict.keys()) == 10


def test_acctunit_get_from_dict_ReturnsObjWith_bridge():
    # ESTABLISH
    yao_str = ",Yao"
    slash_str = "/"
    before_yao_acctunit = acctunit_shop(yao_str, bridge=slash_str)
    yao_dict = before_yao_acctunit.get_dict()

    # WHEN
    after_yao_acctunit = acctunit_get_from_dict(yao_dict, slash_str)

    # THEN
    assert before_yao_acctunit == after_yao_acctunit
    assert after_yao_acctunit.bridge == slash_str


def test_acctunit_get_from_dict_Returns_memberships():
    # ESTABLISH
    yao_str = ",Yao"
    slash_str = "/"
    before_yao_acctunit = acctunit_shop(yao_str, bridge=slash_str)
    ohio_str = f"{slash_str}ohio"
    iowa_str = f"{slash_str}iowa"
    ohio_credit_vote = 90
    ohio_debtit_vote = 901
    iowa_credit_vote = 902
    iowa_debtit_vote = 903
    ohio_membership = membership_shop(ohio_str, ohio_credit_vote, ohio_debtit_vote)
    iowa_membership = membership_shop(iowa_str, iowa_credit_vote, iowa_debtit_vote)
    before_yao_acctunit.set_membership(ohio_membership)
    before_yao_acctunit.set_membership(iowa_membership)
    yao_dict = before_yao_acctunit.get_dict()

    # WHEN
    after_yao_acctunit = acctunit_get_from_dict(yao_dict, slash_str)

    # THEN
    assert before_yao_acctunit._memberships == after_yao_acctunit._memberships
    assert before_yao_acctunit == after_yao_acctunit
    assert after_yao_acctunit.bridge == slash_str


def test_acctunits_get_from_dict_ReturnsObjWith_bridge():
    # ESTABLISH
    yao_str = ",Yao"
    slash_str = "/"
    yao_acctunit = acctunit_shop(yao_str, bridge=slash_str)
    yao_dict = yao_acctunit.get_dict()
    x_acctunits_dict = {yao_str: yao_dict}

    # WHEN
    x_acctunits_objs = acctunits_get_from_dict(x_acctunits_dict, slash_str)

    # THEN
    assert x_acctunits_objs.get(yao_str) == yao_acctunit
    assert x_acctunits_objs.get(yao_str).bridge == slash_str


def test_acctunits_get_from_json_ReturnsObj_SimpleExampleWithIncompleteData():
    # ESTABLISH
    yao_str = "Yao"
    yao_credit_belief = 13
    yao_debtit_belief = 17
    yao_irrational_debtit_belief = 87
    yao_inallocable_debtit_belief = 97
    yao_json_dict = {
        yao_str: {
            "acct_name": yao_str,
            "credit_belief": yao_credit_belief,
            "debtit_belief": yao_debtit_belief,
            "_memberships": {},
            "_irrational_debtit_belief": yao_irrational_debtit_belief,
            "_inallocable_debtit_belief": yao_inallocable_debtit_belief,
        }
    }
    yao_json_str = get_json_from_dict(yao_json_dict)
    assert x_is_json(yao_json_str)

    # WHEN
    yao_obj_dict = acctunits_get_from_json(acctunits_json=yao_json_str)

    # THEN
    assert yao_obj_dict[yao_str] is not None
    yao_acctunit = yao_obj_dict[yao_str]

    assert yao_acctunit.acct_name == yao_str
    assert yao_acctunit.credit_belief == yao_credit_belief
    assert yao_acctunit.debtit_belief == yao_debtit_belief
    assert yao_acctunit._irrational_debtit_belief == yao_irrational_debtit_belief
    assert yao_acctunit._inallocable_debtit_belief == yao_inallocable_debtit_belief
