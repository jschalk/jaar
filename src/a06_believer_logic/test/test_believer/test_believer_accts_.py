from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises
from src.a03_group_logic.acct import acctunit_shop
from src.a06_believer_logic.believer import believerunit_shop


def test_BelieverUnit_set_acctunit_SetObjCorrectly():
    # ESTABLISH
    yao_str = "Yao"
    yao_acctunit = acctunit_shop(yao_str)
    yao_acctunit.add_membership(yao_str)
    deepcopy_yao_acctunit = copy_deepcopy(yao_acctunit)
    slash_str = "/"
    bob_believer = believerunit_shop("Bob", knot=slash_str)

    # WHEN
    bob_believer.set_acctunit(yao_acctunit)

    # THEN
    assert bob_believer.accts.get(yao_str).knot == slash_str
    x_accts = {yao_acctunit.acct_name: deepcopy_yao_acctunit}
    assert bob_believer.accts != x_accts
    deepcopy_yao_acctunit.knot = bob_believer.knot
    assert bob_believer.accts == x_accts


def test_BelieverUnit_set_acct_DoesNotSet_acct_name_membership():
    # ESTABLISH
    x_respect_bit = 5
    yao_believer = believerunit_shop("Yao", respect_bit=x_respect_bit)
    zia_str = "Zia"

    # WHEN
    yao_believer.set_acctunit(acctunit_shop(zia_str), auto_set_membership=False)

    # THEN
    assert yao_believer.get_acct(zia_str).get_membership(zia_str) is None


def test_BelieverUnit_set_acct_DoesSet_acct_name_membership():
    # ESTABLISH
    x_respect_bit = 5
    yao_believer = believerunit_shop("Yao", respect_bit=x_respect_bit)
    zia_str = "Zia"

    # WHEN
    yao_believer.set_acctunit(acctunit_shop(zia_str))

    # THEN
    zia_zia_membership = yao_believer.get_acct(zia_str).get_membership(zia_str)
    assert zia_zia_membership is not None
    assert zia_zia_membership.group_cred_points == 1
    assert zia_zia_membership.group_debt_points == 1


def test_BelieverUnit_set_acct_DoesNotOverRide_acct_name_membership():
    # ESTABLISH
    x_respect_bit = 5
    yao_believer = believerunit_shop("Yao", respect_bit=x_respect_bit)
    zia_str = "Zia"
    ohio_str = ";Ohio"
    zia_ohio_credit_w = 33
    zia_ohio_debt_w = 44
    zia_acctunit = acctunit_shop(zia_str)
    zia_acctunit.add_membership(ohio_str, zia_ohio_credit_w, zia_ohio_debt_w)

    # WHEN
    yao_believer.set_acctunit(zia_acctunit)

    # THEN
    zia_ohio_membership = yao_believer.get_acct(zia_str).get_membership(ohio_str)
    assert zia_ohio_membership is not None
    assert zia_ohio_membership.group_cred_points == zia_ohio_credit_w
    assert zia_ohio_membership.group_debt_points == zia_ohio_debt_w
    zia_zia_membership = yao_believer.get_acct(zia_str).get_membership(zia_str)
    assert zia_zia_membership is None


def test_BelieverUnit_add_acctunit_CorrectlySets_accts():
    # ESTABLISH
    x_respect_bit = 6
    yao_believer = believerunit_shop("Yao", respect_bit=x_respect_bit)
    zia_str = "Zia"
    sue_str = "Sue"
    xio_str = "Xio"

    # WHEN
    yao_believer.add_acctunit(zia_str, acct_cred_points=13, acct_debt_points=8)
    yao_believer.add_acctunit(sue_str, acct_debt_points=5)
    yao_believer.add_acctunit(xio_str, acct_cred_points=17)

    # THEN
    assert len(yao_believer.accts) == 3
    assert len(yao_believer.get_acctunit_group_titles_dict()) == 3
    assert yao_believer.accts.get(xio_str).acct_cred_points == 17
    assert yao_believer.accts.get(sue_str).acct_debt_points == 5
    assert yao_believer.accts.get(xio_str).respect_bit == x_respect_bit


def test_BelieverUnit_acct_exists_ReturnsObj():
    # ESTABLISH
    bob_believer = believerunit_shop("Bob")
    yao_str = "Yao"

    # WHEN / THEN
    assert bob_believer.acct_exists(yao_str) is False

    # ESTABLISH
    bob_believer.add_acctunit(yao_str)

    # WHEN / THEN
    assert bob_believer.acct_exists(yao_str)


def test_BelieverUnit_set_acct_Creates_membership():
    # ESTABLISH
    yao_believer = believerunit_shop("Yao")
    zia_str = "Zia"
    before_zia_credit = 7
    before_zia_debt = 17
    yao_believer.add_acctunit(zia_str, before_zia_credit, before_zia_debt)
    zia_acctunit = yao_believer.get_acct(zia_str)
    zia_membership = zia_acctunit.get_membership(zia_str)
    assert zia_membership.group_cred_points != before_zia_credit
    assert zia_membership.group_debt_points != before_zia_debt
    assert zia_membership.group_cred_points == 1
    assert zia_membership.group_debt_points == 1

    # WHEN
    after_zia_credit = 11
    after_zia_debt = 13
    yao_believer.set_acctunit(acctunit_shop(zia_str, after_zia_credit, after_zia_debt))

    # THEN
    assert zia_membership.group_cred_points != after_zia_credit
    assert zia_membership.group_debt_points != after_zia_debt
    assert zia_membership.group_cred_points == 1
    assert zia_membership.group_debt_points == 1


def test_BelieverUnit_edit_acct_RaiseExceptionWhenAcctDoesNotExist():
    # ESTABLISH
    yao_believer = believerunit_shop("Yao")
    zia_str = "Zia"
    zia_acct_cred_points = 55

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_believer.edit_acctunit(zia_str, acct_cred_points=zia_acct_cred_points)
    assert str(excinfo.value) == f"AcctUnit '{zia_str}' does not exist."


def test_BelieverUnit_edit_acct_CorrectlyUpdatesObj():
    # ESTABLISH
    yao_believer = believerunit_shop("Yao")
    zia_str = "Zia"
    old_zia_acct_cred_points = 55
    old_zia_acct_debt_points = 66
    yao_believer.set_acctunit(
        acctunit_shop(
            zia_str,
            old_zia_acct_cred_points,
            old_zia_acct_debt_points,
        )
    )
    zia_acctunit = yao_believer.get_acct(zia_str)
    assert zia_acctunit.acct_cred_points == old_zia_acct_cred_points
    assert zia_acctunit.acct_debt_points == old_zia_acct_debt_points

    # WHEN
    new_zia_acct_cred_points = 22
    new_zia_acct_debt_points = 33
    yao_believer.edit_acctunit(
        acct_name=zia_str,
        acct_cred_points=new_zia_acct_cred_points,
        acct_debt_points=new_zia_acct_debt_points,
    )

    # THEN
    assert zia_acctunit.acct_cred_points == new_zia_acct_cred_points
    assert zia_acctunit.acct_debt_points == new_zia_acct_debt_points


def test_BelieverUnit_get_acct_ReturnsObj():
    # ESTABLISH
    yao_believer = believerunit_shop("Yao")
    zia_str = "Zia"
    sue_str = "Sue"
    yao_believer.add_acctunit(zia_str)
    yao_believer.add_acctunit(sue_str)

    # WHEN
    zia_acct = yao_believer.get_acct(zia_str)
    sue_acct = yao_believer.get_acct(sue_str)

    # THEN
    assert zia_acct == yao_believer.accts.get(zia_str)
    assert sue_acct == yao_believer.accts.get(sue_str)
