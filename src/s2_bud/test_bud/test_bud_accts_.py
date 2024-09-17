from src.s2_bud.acct import acctunit_shop
from src.s2_bud.bud import budunit_shop
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy


def test_BudUnit_set_acctunit_SetObjCorrectly():
    # ESTABLISH
    yao_str = "Yao"
    yao_acctunit = acctunit_shop(yao_str)
    yao_acctunit.add_membership(yao_str)
    deepcopy_yao_acctunit = copy_deepcopy(yao_acctunit)
    slash_str = "/"
    bob_bud = budunit_shop("Bob", _road_delimiter=slash_str)

    # WHEN
    bob_bud.set_acctunit(yao_acctunit)

    # THEN
    assert bob_bud._accts.get(yao_str)._road_delimiter == slash_str
    x_accts = {yao_acctunit.acct_id: deepcopy_yao_acctunit}
    assert bob_bud._accts != x_accts
    deepcopy_yao_acctunit._road_delimiter = bob_bud._road_delimiter
    assert bob_bud._accts == x_accts


def test_BudUnit_set_acct_DoesNotSet_acct_id_membership():
    # ESTABLISH
    x_respect_bit = 5
    yao_bud = budunit_shop("Yao", respect_bit=x_respect_bit)
    zia_str = "Zia"

    # WHEN
    yao_bud.set_acctunit(acctunit_shop(zia_str), auto_set_membership=False)

    # THEN
    assert yao_bud.get_acct(zia_str).get_membership(zia_str) is None


def test_BudUnit_set_acct_DoesSet_acct_id_membership():
    # ESTABLISH
    x_respect_bit = 5
    yao_bud = budunit_shop("Yao", respect_bit=x_respect_bit)
    zia_str = "Zia"

    # WHEN
    yao_bud.set_acctunit(acctunit_shop(zia_str))

    # THEN
    zia_zia_membership = yao_bud.get_acct(zia_str).get_membership(zia_str)
    assert zia_zia_membership is not None
    assert zia_zia_membership.credit_vote == 1
    assert zia_zia_membership.debtit_vote == 1


def test_BudUnit_set_acct_DoesNotOverRide_acct_id_membership():
    # ESTABLISH
    x_respect_bit = 5
    yao_bud = budunit_shop("Yao", respect_bit=x_respect_bit)
    zia_str = "Zia"
    ohio_str = ";Ohio"
    zia_ohio_credit_w = 33
    zia_ohio_debtit_w = 44
    zia_acctunit = acctunit_shop(zia_str)
    zia_acctunit.add_membership(ohio_str, zia_ohio_credit_w, zia_ohio_debtit_w)

    # WHEN
    yao_bud.set_acctunit(zia_acctunit)

    # THEN
    zia_ohio_membership = yao_bud.get_acct(zia_str).get_membership(ohio_str)
    assert zia_ohio_membership is not None
    assert zia_ohio_membership.credit_vote == zia_ohio_credit_w
    assert zia_ohio_membership.debtit_vote == zia_ohio_debtit_w
    zia_zia_membership = yao_bud.get_acct(zia_str).get_membership(zia_str)
    assert zia_zia_membership is None


def test_BudUnit_add_acctunit_CorrectlySets_accts():
    # ESTABLISH
    x_respect_bit = 6
    yao_bud = budunit_shop("Yao", respect_bit=x_respect_bit)
    zia_str = "Zia"
    sue_str = "Sue"
    xio_str = "Xio"

    # WHEN
    yao_bud.add_acctunit(zia_str, credit_belief=13, debtit_belief=8)
    yao_bud.add_acctunit(sue_str, debtit_belief=5)
    yao_bud.add_acctunit(xio_str, credit_belief=17)

    # THEN
    assert len(yao_bud._accts) == 3
    assert len(yao_bud.get_acctunit_group_ids_dict()) == 3
    assert yao_bud._accts.get(xio_str).credit_belief == 17
    assert yao_bud._accts.get(sue_str).debtit_belief == 5
    assert yao_bud._accts.get(xio_str)._respect_bit == x_respect_bit


def test_BudUnit_acct_exists_ReturnsObj():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    yao_str = "Yao"

    # WHEN / THEN
    assert bob_bud.acct_exists(yao_str) is False

    # ESTABLISH
    bob_bud.add_acctunit(yao_str)

    # WHEN / THEN
    assert bob_bud.acct_exists(yao_str)


def test_BudUnit_set_acct_Creates_membership():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    zia_str = "Zia"
    before_zia_credit = 7
    before_zia_debtit = 17
    yao_bud.add_acctunit(zia_str, before_zia_credit, before_zia_debtit)
    zia_acctunit = yao_bud.get_acct(zia_str)
    zia_membership = zia_acctunit.get_membership(zia_str)
    assert zia_membership.credit_vote != before_zia_credit
    assert zia_membership.debtit_vote != before_zia_debtit
    assert zia_membership.credit_vote == 1
    assert zia_membership.debtit_vote == 1

    # WHEN
    after_zia_credit = 11
    after_zia_debtit = 13
    yao_bud.set_acctunit(acctunit_shop(zia_str, after_zia_credit, after_zia_debtit))

    # THEN
    assert zia_membership.credit_vote != after_zia_credit
    assert zia_membership.debtit_vote != after_zia_debtit
    assert zia_membership.credit_vote == 1
    assert zia_membership.debtit_vote == 1


def test_BudUnit_edit_acct_RaiseExceptionWhenAcctDoesNotExist():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    zia_str = "Zia"
    zia_credit_belief = 55

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_bud.edit_acctunit(zia_str, credit_belief=zia_credit_belief)
    assert str(excinfo.value) == f"AcctUnit '{zia_str}' does not exist."


def test_BudUnit_edit_acct_CorrectlyUpdatesObj():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    zia_str = "Zia"
    old_zia_credit_belief = 55
    old_zia_debtit_belief = 66
    yao_bud.set_acctunit(
        acctunit_shop(
            zia_str,
            old_zia_credit_belief,
            old_zia_debtit_belief,
        )
    )
    zia_acctunit = yao_bud.get_acct(zia_str)
    assert zia_acctunit.credit_belief == old_zia_credit_belief
    assert zia_acctunit.debtit_belief == old_zia_debtit_belief

    # WHEN
    new_zia_credit_belief = 22
    new_zia_debtit_belief = 33
    yao_bud.edit_acctunit(
        acct_id=zia_str,
        credit_belief=new_zia_credit_belief,
        debtit_belief=new_zia_debtit_belief,
    )

    # THEN
    assert zia_acctunit.credit_belief == new_zia_credit_belief
    assert zia_acctunit.debtit_belief == new_zia_debtit_belief


def test_BudUnit_get_acct_ReturnsCorrectObj():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    zia_str = "Zia"
    sue_str = "Sue"
    yao_bud.add_acctunit(zia_str)
    yao_bud.add_acctunit(sue_str)

    # WHEN
    zia_acct = yao_bud.get_acct(zia_str)
    sue_acct = yao_bud.get_acct(sue_str)

    # THEN
    assert zia_acct == yao_bud._accts.get(zia_str)
    assert sue_acct == yao_bud._accts.get(sue_str)
