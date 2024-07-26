from src.bud.acct import acctunit_shop
from src.bud.bud import budunit_shop
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy


def test_BudUnit_set_acctunit_SetObjCorrectly():
    # ESTABLISH
    yao_text = "Yao"
    yao_acctunit = acctunit_shop(yao_text)
    yao_acctunit.add_membership(yao_text)
    deepcopy_yao_acctunit = copy_deepcopy(yao_acctunit)
    slash_text = "/"
    bob_bud = budunit_shop("Bob", _road_delimiter=slash_text)

    # WHEN
    bob_bud.set_acctunit(yao_acctunit)

    # THEN
    assert bob_bud._accts.get(yao_text)._road_delimiter == slash_text
    x_accts = {yao_acctunit.acct_id: deepcopy_yao_acctunit}
    assert bob_bud._accts != x_accts
    deepcopy_yao_acctunit._road_delimiter = bob_bud._road_delimiter
    assert bob_bud._accts == x_accts


def test_BudUnit_set_acct_DoesNotSet_acct_id_membership():
    # ESTABLISH
    x_bit = 5
    yao_bud = budunit_shop("Yao", _bit=x_bit)
    zia_text = "Zia"

    # WHEN
    yao_bud.set_acctunit(acctunit_shop(zia_text), auto_set_membership=False)

    # THEN
    assert yao_bud.get_acct(zia_text).get_membership(zia_text) is None


def test_BudUnit_set_acct_DoesSet_acct_id_membership():
    # ESTABLISH
    x_bit = 5
    yao_bud = budunit_shop("Yao", _bit=x_bit)
    zia_text = "Zia"

    # WHEN
    yao_bud.set_acctunit(acctunit_shop(zia_text))

    # THEN
    zia_zia_membership = yao_bud.get_acct(zia_text).get_membership(zia_text)
    assert zia_zia_membership is not None
    assert zia_zia_membership.credit_vote == 1
    assert zia_zia_membership.debtit_vote == 1


def test_BudUnit_set_acct_DoesNotOverRide_acct_id_membership():
    # ESTABLISH
    x_bit = 5
    yao_bud = budunit_shop("Yao", _bit=x_bit)
    zia_text = "Zia"
    ohio_text = ";Ohio"
    zia_ohio_credit_w = 33
    zia_ohio_debtit_w = 44
    zia_acctunit = acctunit_shop(zia_text)
    zia_acctunit.add_membership(ohio_text, zia_ohio_credit_w, zia_ohio_debtit_w)

    # WHEN
    yao_bud.set_acctunit(zia_acctunit)

    # THEN
    zia_ohio_membership = yao_bud.get_acct(zia_text).get_membership(ohio_text)
    assert zia_ohio_membership is not None
    assert zia_ohio_membership.credit_vote == zia_ohio_credit_w
    assert zia_ohio_membership.debtit_vote == zia_ohio_debtit_w
    zia_zia_membership = yao_bud.get_acct(zia_text).get_membership(zia_text)
    assert zia_zia_membership is None


def test_BudUnit_add_acctunit_CorrectlySets_accts():
    # ESTABLISH
    x_bit = 6
    yao_bud = budunit_shop("Yao", _bit=x_bit)
    zia_text = "Zia"
    sue_text = "Sue"
    xio_text = "Xio"

    # WHEN
    yao_bud.add_acctunit(zia_text, credit_score=13, debtit_score=8)
    yao_bud.add_acctunit(sue_text, debtit_score=5)
    yao_bud.add_acctunit(xio_text, credit_score=17)

    # THEN
    assert len(yao_bud._accts) == 3
    assert len(yao_bud.get_acctunit_group_ids_dict()) == 3
    assert yao_bud._accts.get(xio_text).credit_score == 17
    assert yao_bud._accts.get(sue_text).debtit_score == 5
    assert yao_bud._accts.get(xio_text)._bit == x_bit


def test_BudUnit_acct_exists_ReturnsObj():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    yao_text = "Yao"

    # WHEN / THEN
    assert bob_bud.acct_exists(yao_text) is False

    # ESTABLISH
    bob_bud.add_acctunit(yao_text)

    # WHEN / THEN
    assert bob_bud.acct_exists(yao_text)


def test_BudUnit_set_acct_Creates_membership():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    zia_text = "Zia"
    before_zia_credit = 7
    before_zia_debtit = 17
    yao_bud.add_acctunit(zia_text, before_zia_credit, before_zia_debtit)
    zia_acctunit = yao_bud.get_acct(zia_text)
    zia_membership = zia_acctunit.get_membership(zia_text)
    assert zia_membership.credit_vote != before_zia_credit
    assert zia_membership.debtit_vote != before_zia_debtit
    assert zia_membership.credit_vote == 1
    assert zia_membership.debtit_vote == 1

    # WHEN
    after_zia_credit = 11
    after_zia_debtit = 13
    yao_bud.set_acctunit(acctunit_shop(zia_text, after_zia_credit, after_zia_debtit))

    # THEN
    assert zia_membership.credit_vote != after_zia_credit
    assert zia_membership.debtit_vote != after_zia_debtit
    assert zia_membership.credit_vote == 1
    assert zia_membership.debtit_vote == 1


def test_BudUnit_edit_acct_RaiseExceptionWhenAcctDoesNotExist():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    zia_text = "Zia"
    zia_credit_score = 55

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_bud.edit_acctunit(zia_text, credit_score=zia_credit_score)
    assert str(excinfo.value) == f"AcctUnit '{zia_text}' does not exist."


def test_BudUnit_edit_acct_CorrectlyUpdatesObj():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    zia_text = "Zia"
    old_zia_credit_score = 55
    old_zia_debtit_score = 66
    yao_bud.set_acctunit(
        acctunit_shop(
            zia_text,
            old_zia_credit_score,
            old_zia_debtit_score,
        )
    )
    zia_acctunit = yao_bud.get_acct(zia_text)
    assert zia_acctunit.credit_score == old_zia_credit_score
    assert zia_acctunit.debtit_score == old_zia_debtit_score

    # WHEN
    new_zia_credit_score = 22
    new_zia_debtit_score = 33
    yao_bud.edit_acctunit(
        acct_id=zia_text,
        credit_score=new_zia_credit_score,
        debtit_score=new_zia_debtit_score,
    )

    # THEN
    assert zia_acctunit.credit_score == new_zia_credit_score
    assert zia_acctunit.debtit_score == new_zia_debtit_score


def test_BudUnit_get_acct_ReturnsCorrectObj():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    zia_text = "Zia"
    sue_text = "Sue"
    yao_bud.add_acctunit(zia_text)
    yao_bud.add_acctunit(sue_text)

    # WHEN
    zia_acct = yao_bud.get_acct(zia_text)
    sue_acct = yao_bud.get_acct(sue_text)

    # THEN
    assert zia_acct == yao_bud._accts.get(zia_text)
    assert sue_acct == yao_bud._accts.get(sue_text)
