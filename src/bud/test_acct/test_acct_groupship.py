from src.bud.group import groupship_shop
from src.bud.acct import acctunit_shop
from pytest import raises as pytest_raises


def test_AcctUnit_set_groupship_SetsAttr_groupships():
    # ESTABLISH
    run_text = ",run"
    yao_text = "Yao"
    run_credit_score = 66
    run_debtit_score = 85
    yao_acctunit = acctunit_shop(yao_text)
    assert yao_acctunit._groupships == {}

    # WHEN
    yao_acctunit.set_groupship(
        groupship_shop(run_text, run_credit_score, run_debtit_score)
    )

    # THEN
    assert len(yao_acctunit._groupships) == 1
    run_groupship = yao_acctunit._groupships.get(run_text)
    assert run_groupship.group_id == run_text
    assert run_groupship.credit_score == run_credit_score
    assert run_groupship.debtit_score == run_debtit_score
    assert run_groupship._acct_id == yao_text


def test_AcctUnit_set_groupship_SetsMultipleAttr():
    # ESTABLISH
    run_text = ",run"
    fly_text = ",fly"
    run_groupship = groupship_shop(run_text, credit_score=13, debtit_score=7)
    fly_groupship = groupship_shop(fly_text, credit_score=23, debtit_score=5)
    yao_acctunit = acctunit_shop("Yao")
    assert yao_acctunit._groupships == {}

    # WHEN
    yao_acctunit.set_groupship(run_groupship)
    yao_acctunit.set_groupship(fly_groupship)

    # THEN
    yao_groupships = {
        run_groupship.group_id: run_groupship,
        fly_groupship.group_id: fly_groupship,
    }
    assert yao_acctunit._groupships == yao_groupships


def test_AcctUnit_set_groupship_RaisesErrorIf_group_idIsAcctIDAndNotAcctUnit_acct_id():
    # ESTABLISH
    yao_text = "Yao"
    yao_acctunit = acctunit_shop(yao_text)
    bob_text = "Bob"
    bob_groupship = groupship_shop(bob_text)

    with pytest_raises(Exception) as excinfo:
        yao_acctunit.set_groupship(bob_groupship)
    assert (
        str(excinfo.value)
        == f"AcctUnit with acct_id='{yao_text}' cannot have link to '{bob_text}'."
    )


def test_AcctUnit_get_groupship_ReturnsCorrectObj():
    # ESTABLISH
    run_text = ",run"
    fly_text = ",fly"
    yao_acctunit = acctunit_shop("Yao")
    yao_acctunit.set_groupship(groupship_shop(run_text, 13, 7))
    yao_acctunit.set_groupship(groupship_shop(fly_text, 23, 5))

    # WHEN / THEN
    assert yao_acctunit.get_groupship(run_text) is not None
    assert yao_acctunit.get_groupship(fly_text) is not None
    climb_text = ",climbers"
    assert yao_acctunit.get_groupship(climb_text) is None


def test_groupship_exists_ReturnsCorrectObj():
    # ESTABLISH
    run_text = ",run"
    fly_text = ",fly"
    yao_acctunit = acctunit_shop("Yao")
    yao_acctunit.set_groupship(groupship_shop(run_text, 13, 7))
    yao_acctunit.set_groupship(groupship_shop(fly_text, 23, 5))

    # WHEN / THEN
    assert yao_acctunit.groupship_exists(run_text)
    assert yao_acctunit.groupship_exists(fly_text)
    climb_text = ",climbers"
    assert yao_acctunit.groupship_exists(climb_text) is False


def test_groupships_exist_ReturnsCorrectObj():
    # ESTABLISH
    run_text = ",run"
    fly_text = ",fly"
    yao_acctunit = acctunit_shop("Yao")
    assert yao_acctunit.groupships_exist() is False

    # WHEN
    yao_acctunit.set_groupship(groupship_shop(run_text))
    # THEN
    assert yao_acctunit.groupships_exist()

    # WHEN
    yao_acctunit.set_groupship(groupship_shop(fly_text))
    # THEN
    assert yao_acctunit.groupships_exist()

    # WHEN
    yao_acctunit.delete_groupship(fly_text)
    # THEN
    assert yao_acctunit.groupships_exist()

    # WHEN
    yao_acctunit.delete_groupship(run_text)
    # THEN
    assert yao_acctunit.groupships_exist() is False


def test_AcctUnit_del_groupship_SetsAttrCorrectly():
    # ESTABLISH
    run_text = ",run"
    fly_text = ",fly"
    run_groupship = groupship_shop(run_text)
    fly_groupship = groupship_shop(fly_text)
    yao_groupships = {
        run_groupship.group_id: run_groupship,
        fly_groupship.group_id: fly_groupship,
    }
    yao_acctunit = acctunit_shop("Yao")
    yao_acctunit.set_groupship(run_groupship)
    yao_acctunit.set_groupship(fly_groupship)
    assert len(yao_acctunit._groupships) == 2
    assert yao_acctunit._groupships == yao_groupships

    # WHEN
    yao_acctunit.delete_groupship(run_text)

    # THEN
    assert len(yao_acctunit._groupships) == 1
    assert yao_acctunit._groupships.get(run_text) is None


def test_AcctUnit_clear_groupships_SetsAttrCorrectly():
    # ESTABLISH
    run_text = ",run"
    fly_text = ",fly"
    run_groupship = groupship_shop(run_text)
    fly_groupship = groupship_shop(fly_text)
    yao_groupships = {
        run_groupship.group_id: run_groupship,
        fly_groupship.group_id: fly_groupship,
    }
    yao_acctunit = acctunit_shop("Yao")
    yao_acctunit.set_groupship(run_groupship)
    yao_acctunit.set_groupship(fly_groupship)
    assert len(yao_acctunit._groupships) == 2
    assert yao_acctunit._groupships == yao_groupships

    # WHEN
    yao_acctunit.clear_groupships()

    # THEN
    assert len(yao_acctunit._groupships) == 0
    assert yao_acctunit._groupships.get(run_text) is None


def test_AcctUnit_add_groupship_SetsAttrCorrectly():
    # ESTABLISH
    run_text = ",run"
    run_credit_score = 78
    run_debtit_score = 99
    yao_acctunit = acctunit_shop("Yao")
    assert yao_acctunit.get_groupship(run_text) is None

    # WHEN
    yao_acctunit.add_groupship(run_text, run_credit_score, run_debtit_score)

    # THEN
    assert yao_acctunit.get_groupship(run_text) is not None
    run_groupship = yao_acctunit.get_groupship(run_text)
    assert run_groupship.credit_score == run_credit_score
    assert run_groupship.debtit_score == run_debtit_score


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


def test_AcctUnit_set_credor_pool_Sets_groupships():
    # ESTABLISH
    ohio_text = ",Ohio"
    iowa_text = ",Iowa"
    sue_credit_score = 1
    yao_credit_score = 4
    bob_acctunit = acctunit_shop("Bob")
    bob_acctunit.add_groupship(ohio_text, sue_credit_score)
    bob_acctunit.add_groupship(iowa_text, yao_credit_score)
    assert bob_acctunit._credor_pool == 0
    sue_groupship = bob_acctunit.get_groupship(ohio_text)
    yao_groupship = bob_acctunit.get_groupship(iowa_text)
    assert sue_groupship._credor_pool == 0
    assert yao_groupship._credor_pool == 0

    # WHEN
    bob_credor_pool = 51
    bob_acctunit.set_credor_pool(bob_credor_pool)

    # THEN
    assert bob_acctunit._credor_pool == bob_credor_pool
    assert sue_groupship._credor_pool == 10
    assert yao_groupship._credor_pool == 41


def test_AcctUnit_set_debtor_pool_Sets_groupships():
    # ESTABLISH
    ohio_text = ",Ohio"
    iowa_text = ",Iowa"
    sue_debtit_score = 1
    yao_debtit_score = 4
    bob_acctunit = acctunit_shop("Bob")
    bob_acctunit.add_groupship(ohio_text, 2, sue_debtit_score)
    bob_acctunit.add_groupship(iowa_text, 2, yao_debtit_score)
    assert bob_acctunit._debtor_pool == 0
    sue_groupship = bob_acctunit.get_groupship(ohio_text)
    yao_groupship = bob_acctunit.get_groupship(iowa_text)
    assert sue_groupship._debtor_pool == 0
    assert yao_groupship._debtor_pool == 0

    # WHEN
    bob_debtor_pool = 54
    bob_acctunit.set_debtor_pool(bob_debtor_pool)

    # THEN
    assert bob_acctunit._debtor_pool == bob_debtor_pool
    assert sue_groupship._debtor_pool == 11
    assert yao_groupship._debtor_pool == 43
