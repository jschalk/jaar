from src.a01_way_logic.way import default_bridge_if_None
from src.a02_finance_logic.finance_config import default_respect_bit_if_None
from src.a03_group_logic.acct import AcctUnit, acctunit_shop
from pytest import raises as pytest_raises


def test_AcctUnit_exists():
    # ESTABLISH
    bob_str = "Bob"

    # WHEN
    bob_acctunit = AcctUnit(bob_str)

    # THEN
    print(f"{bob_str}")
    assert bob_acctunit is not None
    assert bob_acctunit.acct_name is not None
    assert bob_acctunit.acct_name == bob_str
    assert bob_acctunit.credit_belief is None
    assert bob_acctunit.debtit_belief is None
    # calculated fields
    assert bob_acctunit._credor_pool is None
    assert bob_acctunit._debtor_pool is None
    assert bob_acctunit._memberships is None
    assert bob_acctunit._irrational_debtit_belief is None
    assert bob_acctunit._inallocable_debtit_belief is None
    assert bob_acctunit._fund_give is None
    assert bob_acctunit._fund_take is None
    assert bob_acctunit._fund_agenda_give is None
    assert bob_acctunit._fund_agenda_take is None
    assert bob_acctunit.bridge is None
    assert bob_acctunit._respect_bit is None


def test_AcctUnit_set_namestr_CorrectlySetsAttr():
    # ESTABLISH
    x_acctunit = AcctUnit()

    # WHEN
    bob_str = "Bob"
    x_acctunit.set_namestr(bob_str)

    # THEN
    assert x_acctunit.acct_name == bob_str


def test_AcctUnit_set_namestr_RaisesErrorIfParameterContains_bridge():
    # ESTABLISH
    slash_str = "/"
    texas_str = f"Texas{slash_str}Arkansas"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        acctunit_shop(acct_name=texas_str, bridge=slash_str)
    assert (
        str(excinfo.value)
        == f"'{texas_str}' needs to be a LabelStr. Cannot contain bridge: '{slash_str}'"
    )


def test_acctunit_shop_CorrectlySetsAttributes():
    # WHEN
    yao_str = "Yao"

    # WHEN
    yao_acctunit = acctunit_shop(acct_name=yao_str)

    # THEN
    assert yao_acctunit.acct_name == yao_str
    assert yao_acctunit.credit_belief == 1
    assert yao_acctunit.debtit_belief == 1
    # calculated fields
    assert yao_acctunit._credor_pool == 0
    assert yao_acctunit._debtor_pool == 0
    assert yao_acctunit._memberships == {}
    assert yao_acctunit._irrational_debtit_belief == 0
    assert yao_acctunit._inallocable_debtit_belief == 0
    assert yao_acctunit._fund_give == 0
    assert yao_acctunit._fund_take == 0
    assert yao_acctunit._fund_agenda_give == 0
    assert yao_acctunit._fund_agenda_take == 0
    assert yao_acctunit._fund_agenda_ratio_give == 0
    assert yao_acctunit._fund_agenda_ratio_take == 0
    assert yao_acctunit.bridge == default_bridge_if_None()
    assert yao_acctunit._respect_bit == default_respect_bit_if_None()


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
    yao_acctunit = acctunit_shop("Yao", _respect_bit=respect_bit_float)

    # THEN
    assert yao_acctunit._respect_bit == 1


def test_AcctUnit_set_respect_bit_CorrectlySetsAttribute():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    assert bob_acctunit._respect_bit == 1

    # WHEN
    x_respect_bit = 5
    bob_acctunit.set_respect_bit(x_respect_bit)

    # THEN
    assert bob_acctunit._respect_bit == x_respect_bit


def test_AcctUnit_set_credit_belief_CorrectlySetsAttribute():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")

    # WHEN
    x_credit_belief = 23
    bob_acctunit.set_credit_belief(x_credit_belief)

    # THEN
    assert bob_acctunit.credit_belief == x_credit_belief


def test_AcctUnit_set_debtit_belief_CorrectlySetsAttribute():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")

    # WHEN
    x_debtit_belief = 23
    bob_acctunit.set_debtit_belief(x_debtit_belief)

    # THEN
    assert bob_acctunit.debtit_belief == x_debtit_belief


def test_AcctUnit_set_credor_debtit_belief_SetsAttr_Scenario0():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    assert bob_acctunit.credit_belief == 1
    assert bob_acctunit.debtit_belief == 1

    # WHEN
    bob_acctunit.set_credor_debtit_belief(credit_belief=23, debtit_belief=34)

    # THEN
    assert bob_acctunit.credit_belief == 23
    assert bob_acctunit.debtit_belief == 34


def test_AcctUnit_set_credor_debtit_belief_IgnoresNoneArgs_Scenario0():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob", credit_belief=45, debtit_belief=56)
    assert bob_acctunit.credit_belief == 45
    assert bob_acctunit.debtit_belief == 56

    # WHEN
    bob_acctunit.set_credor_debtit_belief(credit_belief=None, debtit_belief=None)

    # THEN
    assert bob_acctunit.credit_belief == 45
    assert bob_acctunit.debtit_belief == 56


def test_AcctUnit_set_credor_debtit_belief_IgnoresNoneArgs_Scenario1():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    assert bob_acctunit.credit_belief == 1
    assert bob_acctunit.debtit_belief == 1

    # WHEN
    bob_acctunit.set_credor_debtit_belief(credit_belief=None, debtit_belief=None)

    # THEN
    assert bob_acctunit.credit_belief == 1
    assert bob_acctunit.debtit_belief == 1


def test_AcctUnit_add_irrational_debtit_belief_SetsAttrCorrectly():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    assert bob_acctunit._irrational_debtit_belief == 0

    # WHEN
    bob_int1 = 11
    bob_acctunit.add_irrational_debtit_belief(bob_int1)

    # THEN
    assert bob_acctunit._irrational_debtit_belief == bob_int1

    # WHEN
    bob_int2 = 22
    bob_acctunit.add_irrational_debtit_belief(bob_int2)

    # THEN
    assert bob_acctunit._irrational_debtit_belief == bob_int1 + bob_int2


def test_AcctUnit_add_inallocable_debtit_belief_SetsAttrCorrectly():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    assert bob_acctunit._inallocable_debtit_belief == 0

    # WHEN
    bob_int1 = 11
    bob_acctunit.add_inallocable_debtit_belief(bob_int1)

    # THEN
    assert bob_acctunit._inallocable_debtit_belief == bob_int1

    # WHEN
    bob_int2 = 22
    bob_acctunit.add_inallocable_debtit_belief(bob_int2)

    # THEN
    assert bob_acctunit._inallocable_debtit_belief == bob_int1 + bob_int2


def test_AcctUnit_reset_listen_calculated_attrs_SetsAttrCorrectly():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    bob_int1 = 11
    bob_int2 = 22
    bob_acctunit.add_irrational_debtit_belief(bob_int1)
    bob_acctunit.add_inallocable_debtit_belief(bob_int2)
    assert bob_acctunit._irrational_debtit_belief == bob_int1
    assert bob_acctunit._inallocable_debtit_belief == bob_int2

    # WHEN
    bob_acctunit.reset_listen_calculated_attrs()

    # THEN
    assert bob_acctunit._irrational_debtit_belief == 0
    assert bob_acctunit._inallocable_debtit_belief == 0


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
    bob_acctunit = acctunit_shop("Bob", credit_belief=15, debtit_belief=7)
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
        bud_acctunit_total_credit_belief=20,
        bud_acctunit_total_debtit_belief=14,
    )

    # THEN
    assert bob_acctunit._fund_agenda_ratio_give == 0.205
    assert bob_acctunit._fund_agenda_ratio_take == 0.102

    # WHEN
    bob_acctunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=0,
        fund_agenda_ratio_take_sum=0,
        bud_acctunit_total_credit_belief=20,
        bud_acctunit_total_debtit_belief=14,
    )

    # THEN
    assert bob_acctunit._fund_agenda_ratio_give == 0.75
    assert bob_acctunit._fund_agenda_ratio_take == 0.5
