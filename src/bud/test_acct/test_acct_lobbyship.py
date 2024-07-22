from src.bud.lobby import lobbyship_shop
from src.bud.acct import acctunit_shop
from pytest import raises as pytest_raises


def test_AcctUnit_set_lobbyship_SetsAttr_lobbyships():
    # ESTABLISH
    run_text = ",run"
    yao_text = "Yao"
    run_credit_score = 66
    run_debtit_score = 85
    yao_acctunit = acctunit_shop(yao_text)
    assert yao_acctunit._lobbyships == {}

    # WHEN
    yao_acctunit.set_lobbyship(
        lobbyship_shop(run_text, run_credit_score, run_debtit_score)
    )

    # THEN
    assert len(yao_acctunit._lobbyships) == 1
    run_lobbyship = yao_acctunit._lobbyships.get(run_text)
    assert run_lobbyship.lobby_id == run_text
    assert run_lobbyship.credit_score == run_credit_score
    assert run_lobbyship.debtit_score == run_debtit_score
    assert run_lobbyship._acct_id == yao_text


def test_AcctUnit_set_lobbyship_SetsMultipleAttr():
    # ESTABLISH
    run_text = ",run"
    fly_text = ",fly"
    run_lobbyship = lobbyship_shop(run_text, credit_score=13, debtit_score=7)
    fly_lobbyship = lobbyship_shop(fly_text, credit_score=23, debtit_score=5)
    yao_acctunit = acctunit_shop("Yao")
    assert yao_acctunit._lobbyships == {}

    # WHEN
    yao_acctunit.set_lobbyship(run_lobbyship)
    yao_acctunit.set_lobbyship(fly_lobbyship)

    # THEN
    yao_lobbyships = {
        run_lobbyship.lobby_id: run_lobbyship,
        fly_lobbyship.lobby_id: fly_lobbyship,
    }
    assert yao_acctunit._lobbyships == yao_lobbyships


def test_AcctUnit_set_lobbyship_RaisesErrorIf_lobby_idIsAcctIDAndNotAcctUnit_acct_id():
    # ESTABLISH
    yao_text = "Yao"
    yao_acctunit = acctunit_shop(yao_text)
    bob_text = "Bob"
    bob_lobbyship = lobbyship_shop(bob_text)

    with pytest_raises(Exception) as excinfo:
        yao_acctunit.set_lobbyship(bob_lobbyship)
    assert (
        str(excinfo.value)
        == f"AcctUnit with acct_id='{yao_text}' cannot have link to '{bob_text}'."
    )


def test_AcctUnit_get_lobbyship_ReturnsCorrectObj():
    # ESTABLISH
    run_text = ",run"
    fly_text = ",fly"
    yao_acctunit = acctunit_shop("Yao")
    yao_acctunit.set_lobbyship(lobbyship_shop(run_text, 13, 7))
    yao_acctunit.set_lobbyship(lobbyship_shop(fly_text, 23, 5))

    # WHEN / THEN
    assert yao_acctunit.get_lobbyship(run_text) is not None
    assert yao_acctunit.get_lobbyship(fly_text) is not None
    climb_text = ",climbers"
    assert yao_acctunit.get_lobbyship(climb_text) is None


def test_lobbyship_exists_ReturnsCorrectObj():
    # ESTABLISH
    run_text = ",run"
    fly_text = ",fly"
    yao_acctunit = acctunit_shop("Yao")
    yao_acctunit.set_lobbyship(lobbyship_shop(run_text, 13, 7))
    yao_acctunit.set_lobbyship(lobbyship_shop(fly_text, 23, 5))

    # WHEN / THEN
    assert yao_acctunit.lobbyship_exists(run_text)
    assert yao_acctunit.lobbyship_exists(fly_text)
    climb_text = ",climbers"
    assert yao_acctunit.lobbyship_exists(climb_text) is False


def test_lobbyships_exist_ReturnsCorrectObj():
    # ESTABLISH
    run_text = ",run"
    fly_text = ",fly"
    yao_acctunit = acctunit_shop("Yao")
    assert yao_acctunit.lobbyships_exist() is False

    # WHEN
    yao_acctunit.set_lobbyship(lobbyship_shop(run_text))
    # THEN
    assert yao_acctunit.lobbyships_exist()

    # WHEN
    yao_acctunit.set_lobbyship(lobbyship_shop(fly_text))
    # THEN
    assert yao_acctunit.lobbyships_exist()

    # WHEN
    yao_acctunit.delete_lobbyship(fly_text)
    # THEN
    assert yao_acctunit.lobbyships_exist()

    # WHEN
    yao_acctunit.delete_lobbyship(run_text)
    # THEN
    assert yao_acctunit.lobbyships_exist() is False


def test_AcctUnit_del_lobbyship_SetsAttrCorrectly():
    # ESTABLISH
    run_text = ",run"
    fly_text = ",fly"
    run_lobbyship = lobbyship_shop(run_text)
    fly_lobbyship = lobbyship_shop(fly_text)
    yao_lobbyships = {
        run_lobbyship.lobby_id: run_lobbyship,
        fly_lobbyship.lobby_id: fly_lobbyship,
    }
    yao_acctunit = acctunit_shop("Yao")
    yao_acctunit.set_lobbyship(run_lobbyship)
    yao_acctunit.set_lobbyship(fly_lobbyship)
    assert len(yao_acctunit._lobbyships) == 2
    assert yao_acctunit._lobbyships == yao_lobbyships

    # WHEN
    yao_acctunit.delete_lobbyship(run_text)

    # THEN
    assert len(yao_acctunit._lobbyships) == 1
    assert yao_acctunit._lobbyships.get(run_text) is None


def test_AcctUnit_clear_lobbyships_SetsAttrCorrectly():
    # ESTABLISH
    run_text = ",run"
    fly_text = ",fly"
    run_lobbyship = lobbyship_shop(run_text)
    fly_lobbyship = lobbyship_shop(fly_text)
    yao_lobbyships = {
        run_lobbyship.lobby_id: run_lobbyship,
        fly_lobbyship.lobby_id: fly_lobbyship,
    }
    yao_acctunit = acctunit_shop("Yao")
    yao_acctunit.set_lobbyship(run_lobbyship)
    yao_acctunit.set_lobbyship(fly_lobbyship)
    assert len(yao_acctunit._lobbyships) == 2
    assert yao_acctunit._lobbyships == yao_lobbyships

    # WHEN
    yao_acctunit.clear_lobbyships()

    # THEN
    assert len(yao_acctunit._lobbyships) == 0
    assert yao_acctunit._lobbyships.get(run_text) is None


def test_AcctUnit_add_lobbyship_SetsAttrCorrectly():
    # ESTABLISH
    run_text = ",run"
    run_credit_score = 78
    run_debtit_score = 99
    yao_acctunit = acctunit_shop("Yao")
    assert yao_acctunit.get_lobbyship(run_text) is None

    # WHEN
    yao_acctunit.add_lobbyship(run_text, run_credit_score, run_debtit_score)

    # THEN
    assert yao_acctunit.get_lobbyship(run_text) is not None
    run_lobbyship = yao_acctunit.get_lobbyship(run_text)
    assert run_lobbyship.credit_score == run_credit_score
    assert run_lobbyship.debtit_score == run_debtit_score


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


def test_AcctUnit_set_credor_pool_Sets_lobbyships():
    # ESTABLISH
    ohio_text = ",Ohio"
    iowa_text = ",Iowa"
    sue_credit_score = 1
    yao_credit_score = 4
    bob_acctunit = acctunit_shop("Bob")
    bob_acctunit.add_lobbyship(ohio_text, sue_credit_score)
    bob_acctunit.add_lobbyship(iowa_text, yao_credit_score)
    assert bob_acctunit._credor_pool == 0
    sue_lobbyship = bob_acctunit.get_lobbyship(ohio_text)
    yao_lobbyship = bob_acctunit.get_lobbyship(iowa_text)
    assert sue_lobbyship._credor_pool == 0
    assert yao_lobbyship._credor_pool == 0

    # WHEN
    bob_credor_pool = 51
    bob_acctunit.set_credor_pool(bob_credor_pool)

    # THEN
    assert bob_acctunit._credor_pool == bob_credor_pool
    assert sue_lobbyship._credor_pool == 10
    assert yao_lobbyship._credor_pool == 41


def test_AcctUnit_set_debtor_pool_Sets_lobbyships():
    # ESTABLISH
    ohio_text = ",Ohio"
    iowa_text = ",Iowa"
    sue_debtit_score = 1
    yao_debtit_score = 4
    bob_acctunit = acctunit_shop("Bob")
    bob_acctunit.add_lobbyship(ohio_text, 2, sue_debtit_score)
    bob_acctunit.add_lobbyship(iowa_text, 2, yao_debtit_score)
    assert bob_acctunit._debtor_pool == 0
    sue_lobbyship = bob_acctunit.get_lobbyship(ohio_text)
    yao_lobbyship = bob_acctunit.get_lobbyship(iowa_text)
    assert sue_lobbyship._debtor_pool == 0
    assert yao_lobbyship._debtor_pool == 0

    # WHEN
    bob_debtor_pool = 54
    bob_acctunit.set_debtor_pool(bob_debtor_pool)

    # THEN
    assert bob_acctunit._debtor_pool == bob_debtor_pool
    assert sue_lobbyship._debtor_pool == 11
    assert yao_lobbyship._debtor_pool == 43
