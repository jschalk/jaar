from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises
from src.a03_group_logic.acct import acctunit_shop
from src.a06_plan_logic.plan import planunit_shop


def test_PlanUnit_set_acctunit_SetObjCorrectly():
    # ESTABLISH
    yao_str = "Yao"
    yao_acctunit = acctunit_shop(yao_str)
    yao_acctunit.add_membership(yao_str)
    deepcopy_yao_acctunit = copy_deepcopy(yao_acctunit)
    slash_str = "/"
    bob_plan = planunit_shop("Bob", bridge=slash_str)

    # WHEN
    bob_plan.set_acctunit(yao_acctunit)

    # THEN
    assert bob_plan.accts.get(yao_str).bridge == slash_str
    x_accts = {yao_acctunit.acct_name: deepcopy_yao_acctunit}
    assert bob_plan.accts != x_accts
    deepcopy_yao_acctunit.bridge = bob_plan.bridge
    assert bob_plan.accts == x_accts


def test_PlanUnit_set_acct_DoesNotSet_acct_name_membership():
    # ESTABLISH
    x_respect_bit = 5
    yao_plan = planunit_shop("Yao", respect_bit=x_respect_bit)
    zia_str = "Zia"

    # WHEN
    yao_plan.set_acctunit(acctunit_shop(zia_str), auto_set_membership=False)

    # THEN
    assert yao_plan.get_acct(zia_str).get_membership(zia_str) is None


def test_PlanUnit_set_acct_DoesSet_acct_name_membership():
    # ESTABLISH
    x_respect_bit = 5
    yao_plan = planunit_shop("Yao", respect_bit=x_respect_bit)
    zia_str = "Zia"

    # WHEN
    yao_plan.set_acctunit(acctunit_shop(zia_str))

    # THEN
    zia_zia_membership = yao_plan.get_acct(zia_str).get_membership(zia_str)
    assert zia_zia_membership is not None
    assert zia_zia_membership.credit_vote == 1
    assert zia_zia_membership.debt_vote == 1


def test_PlanUnit_set_acct_DoesNotOverRide_acct_name_membership():
    # ESTABLISH
    x_respect_bit = 5
    yao_plan = planunit_shop("Yao", respect_bit=x_respect_bit)
    zia_str = "Zia"
    ohio_str = ";Ohio"
    zia_ohio_credit_w = 33
    zia_ohio_debt_w = 44
    zia_acctunit = acctunit_shop(zia_str)
    zia_acctunit.add_membership(ohio_str, zia_ohio_credit_w, zia_ohio_debt_w)

    # WHEN
    yao_plan.set_acctunit(zia_acctunit)

    # THEN
    zia_ohio_membership = yao_plan.get_acct(zia_str).get_membership(ohio_str)
    assert zia_ohio_membership is not None
    assert zia_ohio_membership.credit_vote == zia_ohio_credit_w
    assert zia_ohio_membership.debt_vote == zia_ohio_debt_w
    zia_zia_membership = yao_plan.get_acct(zia_str).get_membership(zia_str)
    assert zia_zia_membership is None


def test_PlanUnit_add_acctunit_CorrectlySets_accts():
    # ESTABLISH
    x_respect_bit = 6
    yao_plan = planunit_shop("Yao", respect_bit=x_respect_bit)
    zia_str = "Zia"
    sue_str = "Sue"
    xio_str = "Xio"

    # WHEN
    yao_plan.add_acctunit(zia_str, credit_score=13, debt_score=8)
    yao_plan.add_acctunit(sue_str, debt_score=5)
    yao_plan.add_acctunit(xio_str, credit_score=17)

    # THEN
    assert len(yao_plan.accts) == 3
    assert len(yao_plan.get_acctunit_group_titles_dict()) == 3
    assert yao_plan.accts.get(xio_str).credit_score == 17
    assert yao_plan.accts.get(sue_str).debt_score == 5
    assert yao_plan.accts.get(xio_str).respect_bit == x_respect_bit


def test_PlanUnit_acct_exists_ReturnsObj():
    # ESTABLISH
    bob_plan = planunit_shop("Bob")
    yao_str = "Yao"

    # WHEN / THEN
    assert bob_plan.acct_exists(yao_str) is False

    # ESTABLISH
    bob_plan.add_acctunit(yao_str)

    # WHEN / THEN
    assert bob_plan.acct_exists(yao_str)


def test_PlanUnit_set_acct_Creates_membership():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    zia_str = "Zia"
    before_zia_credit = 7
    before_zia_debt = 17
    yao_plan.add_acctunit(zia_str, before_zia_credit, before_zia_debt)
    zia_acctunit = yao_plan.get_acct(zia_str)
    zia_membership = zia_acctunit.get_membership(zia_str)
    assert zia_membership.credit_vote != before_zia_credit
    assert zia_membership.debt_vote != before_zia_debt
    assert zia_membership.credit_vote == 1
    assert zia_membership.debt_vote == 1

    # WHEN
    after_zia_credit = 11
    after_zia_debt = 13
    yao_plan.set_acctunit(acctunit_shop(zia_str, after_zia_credit, after_zia_debt))

    # THEN
    assert zia_membership.credit_vote != after_zia_credit
    assert zia_membership.debt_vote != after_zia_debt
    assert zia_membership.credit_vote == 1
    assert zia_membership.debt_vote == 1


def test_PlanUnit_edit_acct_RaiseExceptionWhenAcctDoesNotExist():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    zia_str = "Zia"
    zia_credit_score = 55

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_plan.edit_acctunit(zia_str, credit_score=zia_credit_score)
    assert str(excinfo.value) == f"AcctUnit '{zia_str}' does not exist."


def test_PlanUnit_edit_acct_CorrectlyUpdatesObj():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    zia_str = "Zia"
    old_zia_credit_score = 55
    old_zia_debt_score = 66
    yao_plan.set_acctunit(
        acctunit_shop(
            zia_str,
            old_zia_credit_score,
            old_zia_debt_score,
        )
    )
    zia_acctunit = yao_plan.get_acct(zia_str)
    assert zia_acctunit.credit_score == old_zia_credit_score
    assert zia_acctunit.debt_score == old_zia_debt_score

    # WHEN
    new_zia_credit_score = 22
    new_zia_debt_score = 33
    yao_plan.edit_acctunit(
        acct_name=zia_str,
        credit_score=new_zia_credit_score,
        debt_score=new_zia_debt_score,
    )

    # THEN
    assert zia_acctunit.credit_score == new_zia_credit_score
    assert zia_acctunit.debt_score == new_zia_debt_score


def test_PlanUnit_get_acct_ReturnsObj():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    zia_str = "Zia"
    sue_str = "Sue"
    yao_plan.add_acctunit(zia_str)
    yao_plan.add_acctunit(sue_str)

    # WHEN
    zia_acct = yao_plan.get_acct(zia_str)
    sue_acct = yao_plan.get_acct(sue_str)

    # THEN
    assert zia_acct == yao_plan.accts.get(zia_str)
    assert sue_acct == yao_plan.accts.get(sue_str)
