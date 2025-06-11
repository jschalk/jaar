from pytest import raises as pytest_raises
from src.a01_term_logic.way import default_bridge_if_None
from src.a02_finance_logic.finance_config import default_RespectBit_if_None
from src.a03_group_logic._test_util.a03_str import (
    _credor_pool_str,
    _debtor_pool_str,
    _fund_agenda_give_str,
    _fund_agenda_ratio_give_str,
    _fund_agenda_ratio_take_str,
    _fund_agenda_take_str,
    _fund_give_str,
    _fund_take_str,
    _inallocable_debt_score_str,
    _irrational_debt_score_str,
    _memberships_str,
    acct_name_str,
    bridge_str,
    credit_score_str,
    debt_score_str,
    respect_bit_str,
)
from src.a03_group_logic.acct import AcctUnit, acctunit_shop


def test_AcctUnit_exists():
    # ESTABLISH
    bob_str = "Bob"

    # WHEN
    bob_acctunit = AcctUnit(bob_str)

    # THEN
    print(f"{bob_str}")
    assert bob_acctunit
    assert bob_acctunit.acct_name
    assert bob_acctunit.acct_name == bob_str
    assert not bob_acctunit.credit_score
    assert not bob_acctunit.debt_score
    # calculated fields
    assert not bob_acctunit._credor_pool
    assert not bob_acctunit._debtor_pool
    assert not bob_acctunit._memberships
    assert not bob_acctunit._irrational_debt_score
    assert not bob_acctunit._inallocable_debt_score
    assert not bob_acctunit._fund_give
    assert not bob_acctunit._fund_take
    assert not bob_acctunit._fund_agenda_give
    assert not bob_acctunit._fund_agenda_take
    assert not bob_acctunit.bridge
    assert not bob_acctunit.respect_bit
    obj_attrs = set(bob_acctunit.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        _credor_pool_str(),
        _debtor_pool_str(),
        _fund_agenda_give_str(),
        _fund_agenda_ratio_give_str(),
        _fund_agenda_ratio_take_str(),
        _fund_agenda_take_str(),
        _fund_give_str(),
        _fund_take_str(),
        _inallocable_debt_score_str(),
        _irrational_debt_score_str(),
        _memberships_str(),
        respect_bit_str(),
        acct_name_str(),
        bridge_str(),
        credit_score_str(),
        debt_score_str(),
    }


def test_AcctUnit_set_nameterm_CorrectlySetsAttr():
    # ESTABLISH
    x_acctunit = AcctUnit()

    # WHEN
    bob_str = "Bob"
    x_acctunit.set_nameterm(bob_str)

    # THEN
    assert x_acctunit.acct_name == bob_str


def test_AcctUnit_set_nameterm_RaisesErrorIfParameterContains_bridge():
    # ESTABLISH
    slash_str = "/"
    texas_str = f"Texas{slash_str}Arkansas"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        acctunit_shop(acct_name=texas_str, bridge=slash_str)
    assert (
        str(excinfo.value)
        == f"'{texas_str}' needs to be a LabelTerm. Cannot contain {bridge_str()}: '{slash_str}'"
    )


def test_acctunit_shop_CorrectlySetsAttributes():
    # WHEN
    yao_str = "Yao"

    # WHEN
    yao_acctunit = acctunit_shop(acct_name=yao_str)

    # THEN
    assert yao_acctunit.acct_name == yao_str
    assert yao_acctunit.credit_score == 1
    assert yao_acctunit.debt_score == 1
    # calculated fields
    assert yao_acctunit._credor_pool == 0
    assert yao_acctunit._debtor_pool == 0
    assert yao_acctunit._memberships == {}
    assert yao_acctunit._irrational_debt_score == 0
    assert yao_acctunit._inallocable_debt_score == 0
    assert yao_acctunit._fund_give == 0
    assert yao_acctunit._fund_take == 0
    assert yao_acctunit._fund_agenda_give == 0
    assert yao_acctunit._fund_agenda_take == 0
    assert yao_acctunit._fund_agenda_ratio_give == 0
    assert yao_acctunit._fund_agenda_ratio_take == 0
    assert yao_acctunit.bridge == default_bridge_if_None()
    assert yao_acctunit.respect_bit == default_RespectBit_if_None()


def test_acctunit_shop_CorrectlySetsAttributes_bridge():
    # ESTABLISH
    slash_str = "/"

    # WHEN
    yao_acctunit = acctunit_shop("Yao", bridge=slash_str)

    # THEN
    assert yao_acctunit.bridge == slash_str


def test_acctunit_shop_CorrectlySetsAttributes_respect_bit():
    # ESTABLISH
    respect_bit_float = 00.45

    # WHEN
    yao_acctunit = acctunit_shop("Yao", respect_bit=respect_bit_float)

    # THEN
    assert yao_acctunit.respect_bit == 1


def test_AcctUnit_set_respect_bit_CorrectlySetsAttribute():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    assert bob_acctunit.respect_bit == 1

    # WHEN
    x_respect_bit = 5
    bob_acctunit.set_respect_bit(x_respect_bit)

    # THEN
    assert bob_acctunit.respect_bit == x_respect_bit


def test_AcctUnit_set_credit_score_CorrectlySetsAttribute():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")

    # WHEN
    x_credit_score = 23
    bob_acctunit.set_credit_score(x_credit_score)

    # THEN
    assert bob_acctunit.credit_score == x_credit_score


def test_AcctUnit_set_debt_score_CorrectlySetsAttribute():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")

    # WHEN
    x_debt_score = 23
    bob_acctunit.set_debt_score(x_debt_score)

    # THEN
    assert bob_acctunit.debt_score == x_debt_score


def test_AcctUnit_set_credor_debt_score_SetsAttr_Scenario0():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    assert bob_acctunit.credit_score == 1
    assert bob_acctunit.debt_score == 1

    # WHEN
    bob_acctunit.set_credor_debt_score(credit_score=23, debt_score=34)

    # THEN
    assert bob_acctunit.credit_score == 23
    assert bob_acctunit.debt_score == 34


def test_AcctUnit_set_credor_debt_score_IgnoresNoneArgs_Scenario0():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob", credit_score=45, debt_score=56)
    assert bob_acctunit.credit_score == 45
    assert bob_acctunit.debt_score == 56

    # WHEN
    bob_acctunit.set_credor_debt_score(credit_score=None, debt_score=None)

    # THEN
    assert bob_acctunit.credit_score == 45
    assert bob_acctunit.debt_score == 56


def test_AcctUnit_set_credor_debt_score_IgnoresNoneArgs_Scenario1():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    assert bob_acctunit.credit_score == 1
    assert bob_acctunit.debt_score == 1

    # WHEN
    bob_acctunit.set_credor_debt_score(credit_score=None, debt_score=None)

    # THEN
    assert bob_acctunit.credit_score == 1
    assert bob_acctunit.debt_score == 1


def test_AcctUnit_add_irrational_debt_score_SetsAttrCorrectly():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    assert bob_acctunit._irrational_debt_score == 0

    # WHEN
    bob_int1 = 11
    bob_acctunit.add_irrational_debt_score(bob_int1)

    # THEN
    assert bob_acctunit._irrational_debt_score == bob_int1

    # WHEN
    bob_int2 = 22
    bob_acctunit.add_irrational_debt_score(bob_int2)

    # THEN
    assert bob_acctunit._irrational_debt_score == bob_int1 + bob_int2


def test_AcctUnit_add_inallocable_debt_score_SetsAttrCorrectly():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    assert bob_acctunit._inallocable_debt_score == 0

    # WHEN
    bob_int1 = 11
    bob_acctunit.add_inallocable_debt_score(bob_int1)

    # THEN
    assert bob_acctunit._inallocable_debt_score == bob_int1

    # WHEN
    bob_int2 = 22
    bob_acctunit.add_inallocable_debt_score(bob_int2)

    # THEN
    assert bob_acctunit._inallocable_debt_score == bob_int1 + bob_int2


def test_AcctUnit_reset_listen_calculated_attrs_SetsAttrCorrectly():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    bob_int1 = 11
    bob_int2 = 22
    bob_acctunit.add_irrational_debt_score(bob_int1)
    bob_acctunit.add_inallocable_debt_score(bob_int2)
    assert bob_acctunit._irrational_debt_score == bob_int1
    assert bob_acctunit._inallocable_debt_score == bob_int2

    # WHEN
    bob_acctunit.reset_listen_calculated_attrs()

    # THEN
    assert bob_acctunit._irrational_debt_score == 0
    assert bob_acctunit._inallocable_debt_score == 0


def test_AcctUnit_clear_fund_give_take_SetsAttrCorrectly():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    bob_acctunit._fund_give = 0.27
    bob_acctunit._fund_take = 0.37
    bob_acctunit._fund_agenda_give = 0.41
    bob_acctunit._fund_agenda_take = 0.51
    bob_acctunit._fund_agenda_ratio_give = 0.433
    bob_acctunit._fund_agenda_ratio_take = 0.533
    assert bob_acctunit._fund_give == 0.27
    assert bob_acctunit._fund_take == 0.37
    assert bob_acctunit._fund_agenda_give == 0.41
    assert bob_acctunit._fund_agenda_take == 0.51
    assert bob_acctunit._fund_agenda_ratio_give == 0.433
    assert bob_acctunit._fund_agenda_ratio_take == 0.533

    # WHEN
    bob_acctunit.clear_fund_give_take()

    # THEN
    assert bob_acctunit._fund_give == 0
    assert bob_acctunit._fund_take == 0
    assert bob_acctunit._fund_agenda_give == 0
    assert bob_acctunit._fund_agenda_take == 0
    assert bob_acctunit._fund_agenda_ratio_give == 0
    assert bob_acctunit._fund_agenda_ratio_take == 0


def test_AcctUnit_add_fund_agenda_give_SetsAttr():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    bob_acctunit._fund_agenda_give = 0.41
    assert bob_acctunit._fund_agenda_give == 0.41

    # WHEN
    bob_acctunit.add_fund_agenda_give(0.3)

    # THEN
    assert bob_acctunit._fund_agenda_give == 0.71


def test_AcctUnit_add_fund_agenda_take_SetsAttr():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    bob_acctunit._fund_agenda_take = 0.41
    assert bob_acctunit._fund_agenda_take == 0.41

    # WHEN
    bob_acctunit.add_fund_agenda_take(0.3)

    # THEN
    assert bob_acctunit._fund_agenda_take == 0.71


def test_AcctUnit_add_fund_give_take_SetsAttrCorrectly():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    bob_acctunit._fund_give = 0.4106
    bob_acctunit._fund_take = 0.1106
    bob_acctunit._fund_agenda_give = 0.41
    bob_acctunit._fund_agenda_take = 0.51
    assert bob_acctunit._fund_agenda_give == 0.41
    assert bob_acctunit._fund_agenda_take == 0.51

    # WHEN
    bob_acctunit.add_fund_give_take(
        fund_give=0.33,
        fund_take=0.055,
        fund_agenda_give=0.3,
        fund_agenda_take=0.05,
    )

    # THEN
    assert bob_acctunit._fund_give == 0.7406
    assert bob_acctunit._fund_take == 0.1656
    assert bob_acctunit._fund_agenda_give == 0.71
    assert bob_acctunit._fund_agenda_take == 0.56


def test_AcctUnit_set_acctunits_fund_agenda_ratios_SetsAttrCorrectly():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob", credit_score=15, debt_score=7)
    bob_acctunit._fund_give = 0.4106
    bob_acctunit._fund_take = 0.1106
    bob_acctunit._fund_agenda_give = 0.041
    bob_acctunit._fund_agenda_take = 0.051
    bob_acctunit._fund_agenda_ratio_give = 0
    bob_acctunit._fund_agenda_ratio_take = 0
    assert bob_acctunit._fund_agenda_ratio_give == 0
    assert bob_acctunit._fund_agenda_ratio_take == 0

    # WHEN
    bob_acctunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=0.2,
        fund_agenda_ratio_take_sum=0.5,
        acctunits_credit_score_sum=20,
        acctunits_debt_score_sum=14,
    )

    # THEN
    assert bob_acctunit._fund_agenda_ratio_give == 0.205
    assert bob_acctunit._fund_agenda_ratio_take == 0.102

    # WHEN
    bob_acctunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=0,
        fund_agenda_ratio_take_sum=0,
        acctunits_credit_score_sum=20,
        acctunits_debt_score_sum=14,
    )

    # THEN
    assert bob_acctunit._fund_agenda_ratio_give == 0.75
    assert bob_acctunit._fund_agenda_ratio_take == 0.5
