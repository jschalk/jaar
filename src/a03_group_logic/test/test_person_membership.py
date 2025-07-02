from pytest import raises as pytest_raises
from src.a03_group_logic.group import membership_shop
from src.a03_group_logic.person import personunit_shop


def test_PersonUnit_set_membership_SetsAttr_memberships():
    # ESTABLISH
    run_str = ";run"
    yao_str = "Yao"
    run_group_cred_points = 66
    run_group_debt_points = 85
    yao_personunit = personunit_shop(yao_str)
    assert yao_personunit._memberships == {}

    # WHEN
    yao_personunit.set_membership(
        membership_shop(run_str, run_group_cred_points, run_group_debt_points)
    )

    # THEN
    assert len(yao_personunit._memberships) == 1
    run_membership = yao_personunit._memberships.get(run_str)
    assert run_membership.group_title == run_str
    assert run_membership.group_cred_points == run_group_cred_points
    assert run_membership.group_debt_points == run_group_debt_points
    assert run_membership.person_name == yao_str


def test_PersonUnit_set_membership_SetsMultipleAttr():
    # ESTABLISH
    run_str = ";run"
    fly_str = ";fly"
    run_membership = membership_shop(run_str, group_cred_points=13, group_debt_points=7)
    fly_membership = membership_shop(fly_str, group_cred_points=23, group_debt_points=5)
    yao_personunit = personunit_shop("Yao")
    assert yao_personunit._memberships == {}

    # WHEN
    yao_personunit.set_membership(run_membership)
    yao_personunit.set_membership(fly_membership)

    # THEN
    yao_memberships = {
        run_membership.group_title: run_membership,
        fly_membership.group_title: fly_membership,
    }
    assert yao_personunit._memberships == yao_memberships


def test_PersonUnit_set_membership_RaisesErrorIf_group_titleIsPersonNameAndNotPersonUnit_person_name():
    # ESTABLISH
    yao_str = "Yao"
    yao_personunit = personunit_shop(yao_str)
    bob_str = "Bob"
    bob_membership = membership_shop(bob_str)

    with pytest_raises(Exception) as excinfo:
        yao_personunit.set_membership(bob_membership)
    assert (
        str(excinfo.value)
        == f"PersonUnit with person_name='{yao_str}' cannot have link to '{bob_str}'."
    )


def test_PersonUnit_get_membership_ReturnsObj():
    # ESTABLISH
    run_str = ";run"
    fly_str = ";fly"
    yao_personunit = personunit_shop("Yao")
    yao_personunit.set_membership(membership_shop(run_str, 13, 7))
    yao_personunit.set_membership(membership_shop(fly_str, 23, 5))

    # WHEN / THEN
    assert yao_personunit.get_membership(run_str) is not None
    assert yao_personunit.get_membership(fly_str) is not None
    climb_str = ",climbers"
    assert yao_personunit.get_membership(climb_str) is None


def test_membership_exists_ReturnsObj():
    # ESTABLISH
    run_str = ";run"
    fly_str = ";fly"
    yao_personunit = personunit_shop("Yao")
    yao_personunit.set_membership(membership_shop(run_str, 13, 7))
    yao_personunit.set_membership(membership_shop(fly_str, 23, 5))

    # WHEN / THEN
    assert yao_personunit.membership_exists(run_str)
    assert yao_personunit.membership_exists(fly_str)
    climb_str = ",climbers"
    assert yao_personunit.membership_exists(climb_str) is False


def test_memberships_exist_ReturnsObj():
    # ESTABLISH
    run_str = ";run"
    fly_str = ";fly"
    yao_personunit = personunit_shop("Yao")
    assert not yao_personunit.memberships_exist()

    # WHEN
    yao_personunit.set_membership(membership_shop(run_str))
    # THEN
    assert yao_personunit.memberships_exist()

    # WHEN
    yao_personunit.set_membership(membership_shop(fly_str))
    # THEN
    assert yao_personunit.memberships_exist()

    # WHEN
    yao_personunit.delete_membership(fly_str)
    # THEN
    assert yao_personunit.memberships_exist()

    # WHEN
    yao_personunit.delete_membership(run_str)
    # THEN
    assert not yao_personunit.memberships_exist()


def test_PersonUnit_del_membership_SetsAttrCorrectly():
    # ESTABLISH
    run_str = ";run"
    fly_str = ";fly"
    run_membership = membership_shop(run_str)
    fly_membership = membership_shop(fly_str)
    yao_memberships = {
        run_membership.group_title: run_membership,
        fly_membership.group_title: fly_membership,
    }
    yao_personunit = personunit_shop("Yao")
    yao_personunit.set_membership(run_membership)
    yao_personunit.set_membership(fly_membership)
    assert len(yao_personunit._memberships) == 2
    assert yao_personunit._memberships == yao_memberships

    # WHEN
    yao_personunit.delete_membership(run_str)

    # THEN
    assert len(yao_personunit._memberships) == 1
    assert yao_personunit._memberships.get(run_str) is None


def test_PersonUnit_clear_memberships_SetsAttrCorrectly():
    # ESTABLISH
    run_str = ";run"
    fly_str = ";fly"
    run_membership = membership_shop(run_str)
    fly_membership = membership_shop(fly_str)
    yao_memberships = {
        run_membership.group_title: run_membership,
        fly_membership.group_title: fly_membership,
    }
    yao_personunit = personunit_shop("Yao")
    yao_personunit.set_membership(run_membership)
    yao_personunit.set_membership(fly_membership)
    assert len(yao_personunit._memberships) == 2
    assert yao_personunit._memberships == yao_memberships

    # WHEN
    yao_personunit.clear_memberships()

    # THEN
    assert len(yao_personunit._memberships) == 0
    assert yao_personunit._memberships.get(run_str) is None


def test_PersonUnit_add_membership_SetsAttrCorrectly():
    # ESTABLISH
    run_str = ";run"
    run_group_cred_points = 78
    run_group_debt_points = 99
    yao_personunit = personunit_shop("Yao")
    assert yao_personunit.get_membership(run_str) is None

    # WHEN
    yao_personunit.add_membership(run_str, run_group_cred_points, run_group_debt_points)

    # THEN
    assert yao_personunit.get_membership(run_str) is not None
    run_membership = yao_personunit.get_membership(run_str)
    assert run_membership.group_cred_points == run_group_cred_points
    assert run_membership.group_debt_points == run_group_debt_points


def test_PersonUnit_set_credor_pool_SetAttr():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    assert bob_personunit._credor_pool == 0

    # WHEN
    bob_credor_pool = 51
    bob_personunit.set_credor_pool(bob_credor_pool)

    # THEN
    assert bob_personunit._credor_pool == bob_credor_pool


def test_PersonUnit_set_debtor_pool_SetAttr():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    assert bob_personunit._debtor_pool == 0

    # WHEN
    bob_debtor_pool = 51
    bob_personunit.set_debtor_pool(bob_debtor_pool)

    # THEN
    assert bob_personunit._debtor_pool == bob_debtor_pool


def test_PersonUnit_set_credor_pool_Sets_memberships():
    # ESTABLISH
    ohio_str = ";Ohio"
    iowa_str = ";Iowa"
    sue_group_cred_points = 1
    yao_group_cred_points = 4
    bob_personunit = personunit_shop("Bob")
    bob_personunit.add_membership(ohio_str, sue_group_cred_points)
    bob_personunit.add_membership(iowa_str, yao_group_cred_points)
    assert bob_personunit._credor_pool == 0
    sue_membership = bob_personunit.get_membership(ohio_str)
    yao_membership = bob_personunit.get_membership(iowa_str)
    assert sue_membership._credor_pool == 0
    assert yao_membership._credor_pool == 0

    # WHEN
    bob_credor_pool = 51
    bob_personunit.set_credor_pool(bob_credor_pool)

    # THEN
    assert bob_personunit._credor_pool == bob_credor_pool
    assert sue_membership._credor_pool == 10
    assert yao_membership._credor_pool == 41


def test_PersonUnit_set_debtor_pool_Sets_memberships():
    # ESTABLISH
    ohio_str = ";Ohio"
    iowa_str = ";Iowa"
    sue_group_debt_points = 1
    yao_group_debt_points = 4
    bob_personunit = personunit_shop("Bob")
    bob_personunit.add_membership(ohio_str, 2, sue_group_debt_points)
    bob_personunit.add_membership(iowa_str, 2, yao_group_debt_points)
    assert bob_personunit._debtor_pool == 0
    sue_membership = bob_personunit.get_membership(ohio_str)
    yao_membership = bob_personunit.get_membership(iowa_str)
    assert sue_membership._debtor_pool == 0
    assert yao_membership._debtor_pool == 0

    # WHEN
    bob_debtor_pool = 54
    bob_personunit.set_debtor_pool(bob_debtor_pool)

    # THEN
    assert bob_personunit._debtor_pool == bob_debtor_pool
    assert sue_membership._debtor_pool == 11
    assert yao_membership._debtor_pool == 43
