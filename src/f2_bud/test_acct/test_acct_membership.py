from src.f2_bud.group import membership_shop
from src.f2_bud.acct import acctunit_shop
from pytest import raises as pytest_raises


def test_AcctUnit_set_membership_SetsAttr_memberships():
    # ESTABLISH
    run_str = ";run"
    yao_str = "Yao"
    run_credit_vote = 66
    run_debtit_vote = 85
    yao_acctunit = acctunit_shop(yao_str)
    assert yao_acctunit._memberships == {}

    # WHEN
    yao_acctunit.set_membership(
        membership_shop(run_str, run_credit_vote, run_debtit_vote)
    )

    # THEN
    assert len(yao_acctunit._memberships) == 1
    run_membership = yao_acctunit._memberships.get(run_str)
    assert run_membership.group_id == run_str
    assert run_membership.credit_vote == run_credit_vote
    assert run_membership.debtit_vote == run_debtit_vote
    assert run_membership._acct_id == yao_str


def test_AcctUnit_set_membership_SetsMultipleAttr():
    # ESTABLISH
    run_str = ";run"
    fly_str = ";fly"
    run_membership = membership_shop(run_str, credit_vote=13, debtit_vote=7)
    fly_membership = membership_shop(fly_str, credit_vote=23, debtit_vote=5)
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
    yao_str = "Yao"
    yao_acctunit = acctunit_shop(yao_str)
    bob_str = "Bob"
    bob_membership = membership_shop(bob_str)

    with pytest_raises(Exception) as excinfo:
        yao_acctunit.set_membership(bob_membership)
    assert (
        str(excinfo.value)
        == f"AcctUnit with acct_id='{yao_str}' cannot have link to '{bob_str}'."
    )


def test_AcctUnit_get_membership_ReturnsCorrectObj():
    # ESTABLISH
    run_str = ";run"
    fly_str = ";fly"
    yao_acctunit = acctunit_shop("Yao")
    yao_acctunit.set_membership(membership_shop(run_str, 13, 7))
    yao_acctunit.set_membership(membership_shop(fly_str, 23, 5))

    # WHEN / THEN
    assert yao_acctunit.get_membership(run_str) is not None
    assert yao_acctunit.get_membership(fly_str) is not None
    climb_str = ",climbers"
    assert yao_acctunit.get_membership(climb_str) is None


def test_membership_exists_ReturnsCorrectObj():
    # ESTABLISH
    run_str = ";run"
    fly_str = ";fly"
    yao_acctunit = acctunit_shop("Yao")
    yao_acctunit.set_membership(membership_shop(run_str, 13, 7))
    yao_acctunit.set_membership(membership_shop(fly_str, 23, 5))

    # WHEN / THEN
    assert yao_acctunit.membership_exists(run_str)
    assert yao_acctunit.membership_exists(fly_str)
    climb_str = ",climbers"
    assert yao_acctunit.membership_exists(climb_str) is False


def test_memberships_exist_ReturnsCorrectObj():
    # ESTABLISH
    run_str = ";run"
    fly_str = ";fly"
    yao_acctunit = acctunit_shop("Yao")
    assert not yao_acctunit.memberships_exist()

    # WHEN
    yao_acctunit.set_membership(membership_shop(run_str))
    # THEN
    assert yao_acctunit.memberships_exist()

    # WHEN
    yao_acctunit.set_membership(membership_shop(fly_str))
    # THEN
    assert yao_acctunit.memberships_exist()

    # WHEN
    yao_acctunit.delete_membership(fly_str)
    # THEN
    assert yao_acctunit.memberships_exist()

    # WHEN
    yao_acctunit.delete_membership(run_str)
    # THEN
    assert not yao_acctunit.memberships_exist()


def test_AcctUnit_del_membership_SetsAttrCorrectly():
    # ESTABLISH
    run_str = ";run"
    fly_str = ";fly"
    run_membership = membership_shop(run_str)
    fly_membership = membership_shop(fly_str)
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
    yao_acctunit.delete_membership(run_str)

    # THEN
    assert len(yao_acctunit._memberships) == 1
    assert yao_acctunit._memberships.get(run_str) is None


def test_AcctUnit_clear_memberships_SetsAttrCorrectly():
    # ESTABLISH
    run_str = ";run"
    fly_str = ";fly"
    run_membership = membership_shop(run_str)
    fly_membership = membership_shop(fly_str)
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
    assert yao_acctunit._memberships.get(run_str) is None


def test_AcctUnit_add_membership_SetsAttrCorrectly():
    # ESTABLISH
    run_str = ";run"
    run_credit_vote = 78
    run_debtit_vote = 99
    yao_acctunit = acctunit_shop("Yao")
    assert yao_acctunit.get_membership(run_str) is None

    # WHEN
    yao_acctunit.add_membership(run_str, run_credit_vote, run_debtit_vote)

    # THEN
    assert yao_acctunit.get_membership(run_str) is not None
    run_membership = yao_acctunit.get_membership(run_str)
    assert run_membership.credit_vote == run_credit_vote
    assert run_membership.debtit_vote == run_debtit_vote


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
    ohio_str = ";Ohio"
    iowa_str = ";Iowa"
    sue_credit_vote = 1
    yao_credit_vote = 4
    bob_acctunit = acctunit_shop("Bob")
    bob_acctunit.add_membership(ohio_str, sue_credit_vote)
    bob_acctunit.add_membership(iowa_str, yao_credit_vote)
    assert bob_acctunit._credor_pool == 0
    sue_membership = bob_acctunit.get_membership(ohio_str)
    yao_membership = bob_acctunit.get_membership(iowa_str)
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
    ohio_str = ";Ohio"
    iowa_str = ";Iowa"
    sue_debtit_vote = 1
    yao_debtit_vote = 4
    bob_acctunit = acctunit_shop("Bob")
    bob_acctunit.add_membership(ohio_str, 2, sue_debtit_vote)
    bob_acctunit.add_membership(iowa_str, 2, yao_debtit_vote)
    assert bob_acctunit._debtor_pool == 0
    sue_membership = bob_acctunit.get_membership(ohio_str)
    yao_membership = bob_acctunit.get_membership(iowa_str)
    assert sue_membership._debtor_pool == 0
    assert yao_membership._debtor_pool == 0

    # WHEN
    bob_debtor_pool = 54
    bob_acctunit.set_debtor_pool(bob_debtor_pool)

    # THEN
    assert bob_acctunit._debtor_pool == bob_debtor_pool
    assert sue_membership._debtor_pool == 11
    assert yao_membership._debtor_pool == 43
