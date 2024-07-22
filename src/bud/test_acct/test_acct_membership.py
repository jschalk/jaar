from src.bud.group import membership_shop
from src.bud.acct import acctunit_shop
from pytest import raises as pytest_raises


def test_AcctUnit_set_membership_SetsAttr_memberships():
    # ESTABLISH
    run_text = ",run"
    yao_text = "Yao"
    run_credit_score = 66
    run_debtit_score = 85
    yao_acctunit = acctunit_shop(yao_text)
    assert yao_acctunit._memberships == {}

    # WHEN
    yao_acctunit.set_membership(
        membership_shop(run_text, run_credit_score, run_debtit_score)
    )

    # THEN
    assert len(yao_acctunit._memberships) == 1
    run_membership = yao_acctunit._memberships.get(run_text)
    assert run_membership.group_id == run_text
    assert run_membership.credit_score == run_credit_score
    assert run_membership.debtit_score == run_debtit_score
    assert run_membership._acct_id == yao_text


def test_AcctUnit_set_membership_SetsMultipleAttr():
    # ESTABLISH
    run_text = ",run"
    fly_text = ",fly"
    run_membership = membership_shop(run_text, credit_score=13, debtit_score=7)
    fly_membership = membership_shop(fly_text, credit_score=23, debtit_score=5)
    yao_acctunit = acctunit_shop("Yao")
    assert yao_acctunit._memberships == {}

    # WHEN
    yao_acctunit.set_membership(run_membership)
    yao_acctunit.set_membership(fly_membership)

    # THEN
    yao_memberships = {
        run_membership.group_id: run_membership,
        fly_membership.group_id: fly_membership,
    }
    assert yao_acctunit._memberships == yao_memberships


def test_AcctUnit_set_membership_RaisesErrorIf_group_idIsAcctIDAndNotAcctUnit_acct_id():
    # ESTABLISH
    yao_text = "Yao"
    yao_acctunit = acctunit_shop(yao_text)
    bob_text = "Bob"
    bob_membership = membership_shop(bob_text)

    with pytest_raises(Exception) as excinfo:
        yao_acctunit.set_membership(bob_membership)
    assert (
        str(excinfo.value)
        == f"AcctUnit with acct_id='{yao_text}' cannot have link to '{bob_text}'."
    )


def test_AcctUnit_get_membership_ReturnsCorrectObj():
    # ESTABLISH
    run_text = ",run"
    fly_text = ",fly"
    yao_acctunit = acctunit_shop("Yao")
    yao_acctunit.set_membership(membership_shop(run_text, 13, 7))
    yao_acctunit.set_membership(membership_shop(fly_text, 23, 5))

    # WHEN / THEN
    assert yao_acctunit.get_membership(run_text) is not None
    assert yao_acctunit.get_membership(fly_text) is not None
    climb_text = ",climbers"
    assert yao_acctunit.get_membership(climb_text) is None


def test_membership_exists_ReturnsCorrectObj():
    # ESTABLISH
    run_text = ",run"
    fly_text = ",fly"
    yao_acctunit = acctunit_shop("Yao")
    yao_acctunit.set_membership(membership_shop(run_text, 13, 7))
    yao_acctunit.set_membership(membership_shop(fly_text, 23, 5))

    # WHEN / THEN
    assert yao_acctunit.membership_exists(run_text)
    assert yao_acctunit.membership_exists(fly_text)
    climb_text = ",climbers"
    assert yao_acctunit.membership_exists(climb_text) is False


def test_memberships_exist_ReturnsCorrectObj():
    # ESTABLISH
    run_text = ",run"
    fly_text = ",fly"
    yao_acctunit = acctunit_shop("Yao")
    assert yao_acctunit.memberships_exist() is False

    # WHEN
    yao_acctunit.set_membership(membership_shop(run_text))
    # THEN
    assert yao_acctunit.memberships_exist()

    # WHEN
    yao_acctunit.set_membership(membership_shop(fly_text))
    # THEN
    assert yao_acctunit.memberships_exist()

    # WHEN
    yao_acctunit.delete_membership(fly_text)
    # THEN
    assert yao_acctunit.memberships_exist()

    # WHEN
    yao_acctunit.delete_membership(run_text)
    # THEN
    assert yao_acctunit.memberships_exist() is False


def test_AcctUnit_del_membership_SetsAttrCorrectly():
    # ESTABLISH
    run_text = ",run"
    fly_text = ",fly"
    run_membership = membership_shop(run_text)
    fly_membership = membership_shop(fly_text)
    yao_memberships = {
        run_membership.group_id: run_membership,
        fly_membership.group_id: fly_membership,
    }
    yao_acctunit = acctunit_shop("Yao")
    yao_acctunit.set_membership(run_membership)
    yao_acctunit.set_membership(fly_membership)
    assert len(yao_acctunit._memberships) == 2
    assert yao_acctunit._memberships == yao_memberships

    # WHEN
    yao_acctunit.delete_membership(run_text)

    # THEN
    assert len(yao_acctunit._memberships) == 1
    assert yao_acctunit._memberships.get(run_text) is None


def test_AcctUnit_clear_memberships_SetsAttrCorrectly():
    # ESTABLISH
    run_text = ",run"
    fly_text = ",fly"
    run_membership = membership_shop(run_text)
    fly_membership = membership_shop(fly_text)
    yao_memberships = {
        run_membership.group_id: run_membership,
        fly_membership.group_id: fly_membership,
    }
    yao_acctunit = acctunit_shop("Yao")
    yao_acctunit.set_membership(run_membership)
    yao_acctunit.set_membership(fly_membership)
    assert len(yao_acctunit._memberships) == 2
    assert yao_acctunit._memberships == yao_memberships

    # WHEN
    yao_acctunit.clear_memberships()

    # THEN
    assert len(yao_acctunit._memberships) == 0
    assert yao_acctunit._memberships.get(run_text) is None


def test_AcctUnit_add_membership_SetsAttrCorrectly():
    # ESTABLISH
    run_text = ",run"
    run_credit_score = 78
    run_debtit_score = 99
    yao_acctunit = acctunit_shop("Yao")
    assert yao_acctunit.get_membership(run_text) is None

    # WHEN
    yao_acctunit.add_membership(run_text, run_credit_score, run_debtit_score)

    # THEN
    assert yao_acctunit.get_membership(run_text) is not None
    run_membership = yao_acctunit.get_membership(run_text)
    assert run_membership.credit_score == run_credit_score
    assert run_membership.debtit_score == run_debtit_score


def test_AcctUnit_set_credor_pool_SetAttr():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    assert bob_acctunit._credor_pool == 0

    # WHEN
    bob_credor_pool = 51
    bob_acctunit.set_credor_pool(bob_credor_pool)

    # THEN
    assert bob_acctunit._credor_pool == bob_credor_pool


def test_AcctUnit_set_debtor_pool_SetAttr():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    assert bob_acctunit._debtor_pool == 0

    # WHEN
    bob_debtor_pool = 51
    bob_acctunit.set_debtor_pool(bob_debtor_pool)

    # THEN
    assert bob_acctunit._debtor_pool == bob_debtor_pool


def test_AcctUnit_set_credor_pool_Sets_memberships():
    # ESTABLISH
    ohio_text = ",Ohio"
    iowa_text = ",Iowa"
    sue_credit_score = 1
    yao_credit_score = 4
    bob_acctunit = acctunit_shop("Bob")
    bob_acctunit.add_membership(ohio_text, sue_credit_score)
    bob_acctunit.add_membership(iowa_text, yao_credit_score)
    assert bob_acctunit._credor_pool == 0
    sue_membership = bob_acctunit.get_membership(ohio_text)
    yao_membership = bob_acctunit.get_membership(iowa_text)
    assert sue_membership._credor_pool == 0
    assert yao_membership._credor_pool == 0

    # WHEN
    bob_credor_pool = 51
    bob_acctunit.set_credor_pool(bob_credor_pool)

    # THEN
    assert bob_acctunit._credor_pool == bob_credor_pool
    assert sue_membership._credor_pool == 10
    assert yao_membership._credor_pool == 41


def test_AcctUnit_set_debtor_pool_Sets_memberships():
    # ESTABLISH
    ohio_text = ",Ohio"
    iowa_text = ",Iowa"
    sue_debtit_score = 1
    yao_debtit_score = 4
    bob_acctunit = acctunit_shop("Bob")
    bob_acctunit.add_membership(ohio_text, 2, sue_debtit_score)
    bob_acctunit.add_membership(iowa_text, 2, yao_debtit_score)
    assert bob_acctunit._debtor_pool == 0
    sue_membership = bob_acctunit.get_membership(ohio_text)
    yao_membership = bob_acctunit.get_membership(iowa_text)
    assert sue_membership._debtor_pool == 0
    assert yao_membership._debtor_pool == 0

    # WHEN
    bob_debtor_pool = 54
    bob_acctunit.set_debtor_pool(bob_debtor_pool)

    # THEN
    assert bob_acctunit._debtor_pool == bob_debtor_pool
    assert sue_membership._debtor_pool == 11
    assert yao_membership._debtor_pool == 43
