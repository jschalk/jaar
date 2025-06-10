from src.a03_group_logic.acct import acctunit_shop
from src.a06_plan_logic._test_util.a06_str import (
    acct_name_str,
    credit_score_str,
    debtit_score_str,
    group_title_str,
    plan_acct_membership_str,
    plan_acctunit_str,
    planunit_str,
)
from src.a08_plan_atom_logic._test_util.a08_str import DELETE_str, INSERT_str
from src.a08_plan_atom_logic.atom import PlanAtom, planatom_shop


def test_PlanAtom_exists():
    # ESTABLISH / WHEN
    x_planatom = PlanAtom()

    # THEN
    assert x_planatom.dimen is None
    assert x_planatom.crud_str is None
    assert x_planatom.jkeys is None
    assert x_planatom.jvalues is None
    assert x_planatom.atom_order is None


def test_planatom_shop_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_credit_score = 55
    bob_debtit_score = 66
    bob_acctunit = acctunit_shop(bob_str, bob_credit_score, bob_debtit_score)
    cw_str = "_credit_score"
    dw_str = "_debtit_score"
    bob_required_dict = {acct_name_str(): "huh"}
    bob_optional_dict = {cw_str: bob_acctunit.get_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_acctunit.get_dict().get(dw_str)
    acctunit_str = plan_acctunit_str()

    # WHEN
    x_planatom = planatom_shop(
        dimen=acctunit_str,
        crud_str=INSERT_str(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    print(f"{x_planatom=}")
    assert x_planatom.dimen == acctunit_str
    assert x_planatom.crud_str == INSERT_str()
    assert x_planatom.jkeys == bob_required_dict
    assert x_planatom.jvalues == bob_optional_dict


def test_PlanAtom_set_jkey_CorrectlySetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    acctunit_str = plan_acctunit_str()
    acctunit_planatom = planatom_shop(acctunit_str, INSERT_str())
    assert acctunit_planatom.jkeys == {}

    # WHEN
    acctunit_planatom.set_jkey(x_key=acct_name_str(), x_value=bob_str)

    # THEN
    assert acctunit_planatom.jkeys == {acct_name_str(): bob_str}


def test_PlanAtom_set_jvalue_CorrectlySetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    acctunit_str = plan_acctunit_str()
    acctunit_planatom = planatom_shop(acctunit_str, INSERT_str())
    assert acctunit_planatom.jvalues == {}

    # WHEN
    acctunit_planatom.set_jvalue(x_key=acct_name_str(), x_value=bob_str)

    # THEN
    assert acctunit_planatom.jvalues == {acct_name_str(): bob_str}


def test_PlanAtom_get_value_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    acctunit_str = plan_acctunit_str()
    acctunit_planatom = planatom_shop(acctunit_str, INSERT_str())
    acctunit_planatom.set_jkey(x_key=acct_name_str(), x_value=bob_str)

    # WHEN / THEN
    assert acctunit_planatom.get_value(acct_name_str()) == bob_str


def test_PlanAtom_is_jvalues_valid_ReturnsCorrectBoolean():
    # WHEN
    acctunit_str = plan_acctunit_str()
    bob_insert_planatom = planatom_shop(acctunit_str, crud_str=INSERT_str())
    assert bob_insert_planatom.is_jvalues_valid()

    # WHEN
    bob_insert_planatom.set_jvalue(credit_score_str(), 55)
    # THEN
    assert len(bob_insert_planatom.jvalues) == 1
    assert bob_insert_planatom.is_jvalues_valid()

    # WHEN
    bob_insert_planatom.set_jvalue(debtit_score_str(), 66)
    # THEN
    assert len(bob_insert_planatom.jvalues) == 2
    assert bob_insert_planatom.is_jvalues_valid()

    # WHEN
    bob_insert_planatom.set_jvalue("x_x_x", 77)
    # THEN
    assert len(bob_insert_planatom.jvalues) == 3
    assert bob_insert_planatom.is_jvalues_valid() is False


def test_PlanAtom_is_valid_ReturnsCorrectBoolean_AcctUnit_INSERT():
    bob_str = "Bob"
    bob_credit_score = 55
    bob_debtit_score = 66
    bob_acctunit = acctunit_shop(bob_str, bob_credit_score, bob_debtit_score)
    acctunit_str = plan_acctunit_str()

    # WHEN
    bob_insert_planatom = planatom_shop(acctunit_str, crud_str=INSERT_str())

    # THEN
    assert bob_insert_planatom.is_jkeys_valid() is False
    assert bob_insert_planatom.is_jvalues_valid()
    assert bob_insert_planatom.is_valid() is False

    # WHEN
    bob_insert_planatom.set_jvalue("x_x_x", 12)

    # THEN
    assert bob_insert_planatom.is_jkeys_valid() is False
    assert bob_insert_planatom.is_jvalues_valid() is False
    assert bob_insert_planatom.is_valid() is False

    # WHEN
    bob_insert_planatom.set_jkey(acct_name_str(), bob_str)

    # THEN
    assert bob_insert_planatom.is_jkeys_valid()
    assert bob_insert_planatom.is_jvalues_valid() is False
    assert bob_insert_planatom.is_valid() is False

    # WHEN
    bob_insert_planatom.jvalues = {}
    cw_str = credit_score_str()
    dw_str = debtit_score_str()
    bob_insert_planatom.set_jvalue(cw_str, bob_acctunit.get_dict().get(cw_str))
    bob_insert_planatom.set_jvalue(dw_str, bob_acctunit.get_dict().get(dw_str))

    # THEN
    assert bob_insert_planatom.is_jkeys_valid()
    assert bob_insert_planatom.is_jvalues_valid()
    assert bob_insert_planatom.is_valid()

    # WHEN
    bob_insert_planatom.crud_str = None

    # THEN
    assert bob_insert_planatom.is_jkeys_valid() is False
    assert bob_insert_planatom.is_valid() is False

    # WHEN
    bob_insert_planatom.crud_str = INSERT_str()

    # THEN
    assert bob_insert_planatom.is_jkeys_valid()
    assert bob_insert_planatom.is_valid()


def test_PlanAtom_get_value_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_credit_score = 55
    bob_debtit_score = 66
    bob_acctunit = acctunit_shop(bob_str, bob_credit_score, bob_debtit_score)
    acctunit_str = plan_acctunit_str()
    bob_insert_planatom = planatom_shop(acctunit_str, INSERT_str())
    cw_str = credit_score_str()
    dw_str = debtit_score_str()
    print(f"{bob_acctunit.get_dict()=}")
    # bob_acctunit_dict = {acct_name_str(): bob_acctunit.get_dict().get(acct_name_str())}
    # print(f"{bob_acctunit_dict=}")
    bob_insert_planatom.set_jkey(acct_name_str(), bob_str)
    bob_insert_planatom.set_jvalue(cw_str, bob_acctunit.get_dict().get(cw_str))
    bob_insert_planatom.set_jvalue(dw_str, bob_acctunit.get_dict().get(dw_str))
    assert bob_insert_planatom.is_valid()

    # WHEN / THEN
    assert bob_insert_planatom.get_value(cw_str) == bob_credit_score
    assert bob_insert_planatom.get_value(dw_str) == bob_debtit_score


def test_PlanAtom_is_valid_ReturnsCorrectBoolean_AcctUnit_DELETE():
    bob_str = "Bob"
    acctunit_str = plan_acctunit_str()
    delete_str = DELETE_str()

    # WHEN
    bob_delete_planatom = planatom_shop(acctunit_str, crud_str=delete_str)

    # THEN
    assert bob_delete_planatom.is_jkeys_valid() is False
    assert bob_delete_planatom.is_valid() is False

    # WHEN
    bob_delete_planatom.set_jkey(acct_name_str(), bob_str)

    # THEN
    assert bob_delete_planatom.is_jkeys_valid()
    assert bob_delete_planatom.is_valid()


def test_PlanAtom_is_valid_ReturnsCorrectBoolean_planunit():
    # ESTABLISH / WHEN
    bob_update_planatom = planatom_shop(planunit_str(), INSERT_str())

    # THEN
    assert bob_update_planatom.is_jkeys_valid()
    assert bob_update_planatom.is_valid() is False

    # WHEN
    bob_update_planatom.set_jvalue("max_tree_traverse", 14)

    # THEN
    assert bob_update_planatom.is_jkeys_valid()
    assert bob_update_planatom.is_valid()


def test_PlanAtom_set_atom_order_SetCorrectAttr():
    # ESTABLISH
    bob_str = "Bob"
    bob_credit_score = 55
    bob_debtit_score = 66
    acctunit_str = plan_acctunit_str()
    bob_insert_planatom = planatom_shop(acctunit_str, INSERT_str())
    cw_str = credit_score_str()
    dw_str = debtit_score_str()
    bob_insert_planatom.set_jkey(acct_name_str(), bob_str)
    bob_insert_planatom.set_jvalue(cw_str, bob_credit_score)
    bob_insert_planatom.set_jvalue(dw_str, bob_debtit_score)
    assert bob_insert_planatom.is_valid()

    # WHEN / THEN
    assert bob_insert_planatom.get_value(cw_str) == bob_credit_score
    assert bob_insert_planatom.get_value(dw_str) == bob_debtit_score


def test_PlanAtom_set_arg_SetsAny_jkey_jvalue():
    # ESTABLISH
    bob_str = "Bob"
    bob_credit_score = 55
    bob_debtit_score = 66
    acctunit_str = plan_acctunit_str()
    bob_insert_planatom = planatom_shop(acctunit_str, INSERT_str())
    cw_str = credit_score_str()
    dw_str = debtit_score_str()

    # WHEN
    bob_insert_planatom.set_arg(acct_name_str(), bob_str)
    bob_insert_planatom.set_arg(cw_str, bob_credit_score)
    bob_insert_planatom.set_arg(dw_str, bob_debtit_score)

    # THEN
    assert bob_insert_planatom.get_value(acct_name_str()) == bob_str
    assert bob_insert_planatom.get_value(cw_str) == bob_credit_score
    assert bob_insert_planatom.get_value(dw_str) == bob_debtit_score
    assert bob_insert_planatom.get_value(acct_name_str()) == bob_str
    assert bob_insert_planatom.is_valid()


def test_PlanAtom_get_nesting_order_args_ReturnsObj_plan_acctunit():
    # ESTABLISH
    sue_str = "Sue"
    sue_insert_planatom = planatom_shop(plan_acctunit_str(), INSERT_str())
    sue_insert_planatom.set_arg(acct_name_str(), sue_str)
    print(f"{sue_insert_planatom.jkeys=}")

    # WHEN / THEN
    ordered_jkeys = [sue_str]
    assert sue_insert_planatom.get_nesting_order_args() == ordered_jkeys


def test_PlanAtom_get_nesting_order_args_ReturnsObj_plan_acct_membership():
    # ESTABLISH
    sue_str = "Sue"
    iowa_str = ";Iowa"
    sue_insert_planatom = planatom_shop(plan_acct_membership_str(), INSERT_str())
    sue_insert_planatom.set_arg(group_title_str(), iowa_str)
    sue_insert_planatom.set_arg(acct_name_str(), sue_str)
    print(f"{sue_insert_planatom.jkeys=}")

    # WHEN / THEN
    ordered_jkeys = [sue_str, iowa_str]
    assert sue_insert_planatom.get_nesting_order_args() == ordered_jkeys
