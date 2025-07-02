from pytest import raises as pytest_raises
from src.a01_term_logic.rope import default_knot_if_None
from src.a02_finance_logic.finance_config import default_RespectBit_if_None
from src.a03_group_logic.person import PersonUnit, personunit_shop
from src.a03_group_logic.test._util.a03_str import (
    _credor_pool_str,
    _debtor_pool_str,
    _fund_agenda_give_str,
    _fund_agenda_ratio_give_str,
    _fund_agenda_ratio_take_str,
    _fund_agenda_take_str,
    _fund_give_str,
    _fund_take_str,
    _inallocable_person_debt_points_str,
    _irrational_person_debt_points_str,
    _memberships_str,
    knot_str,
    person_cred_points_str,
    person_debt_points_str,
    person_name_str,
    respect_bit_str,
)


def test_PersonUnit_exists():
    # ESTABLISH
    bob_str = "Bob"

    # WHEN
    bob_personunit = PersonUnit(bob_str)

    # THEN
    print(f"{bob_str}")
    assert bob_personunit
    assert bob_personunit.person_name
    assert bob_personunit.person_name == bob_str
    assert not bob_personunit.person_cred_points
    assert not bob_personunit.person_debt_points
    # calculated fields
    assert not bob_personunit._credor_pool
    assert not bob_personunit._debtor_pool
    assert not bob_personunit._memberships
    assert not bob_personunit._irrational_person_debt_points
    assert not bob_personunit._inallocable_person_debt_points
    assert not bob_personunit._fund_give
    assert not bob_personunit._fund_take
    assert not bob_personunit._fund_agenda_give
    assert not bob_personunit._fund_agenda_take
    assert not bob_personunit.knot
    assert not bob_personunit.respect_bit
    obj_attrs = set(bob_personunit.__dict__.keys())
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
        _inallocable_person_debt_points_str(),
        _irrational_person_debt_points_str(),
        _memberships_str(),
        respect_bit_str(),
        person_name_str(),
        knot_str(),
        person_cred_points_str(),
        person_debt_points_str(),
    }


def test_PersonUnit_set_nameterm_CorrectlySetsAttr():
    # ESTABLISH
    x_personunit = PersonUnit()

    # WHEN
    bob_str = "Bob"
    x_personunit.set_nameterm(bob_str)

    # THEN
    assert x_personunit.person_name == bob_str


def test_PersonUnit_set_nameterm_RaisesErrorIfParameterContains_knot():
    # ESTABLISH
    slash_str = "/"
    texas_str = f"Texas{slash_str}Arkansas"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        personunit_shop(person_name=texas_str, knot=slash_str)
    assert (
        str(excinfo.value)
        == f"'{texas_str}' needs to be a LabelTerm. Cannot contain {knot_str()}: '{slash_str}'"
    )


def test_personunit_shop_CorrectlySetsAttributes():
    # WHEN
    yao_str = "Yao"

    # WHEN
    yao_personunit = personunit_shop(person_name=yao_str)

    # THEN
    assert yao_personunit.person_name == yao_str
    assert yao_personunit.person_cred_points == 1
    assert yao_personunit.person_debt_points == 1
    # calculated fields
    assert yao_personunit._credor_pool == 0
    assert yao_personunit._debtor_pool == 0
    assert yao_personunit._memberships == {}
    assert yao_personunit._irrational_person_debt_points == 0
    assert yao_personunit._inallocable_person_debt_points == 0
    assert yao_personunit._fund_give == 0
    assert yao_personunit._fund_take == 0
    assert yao_personunit._fund_agenda_give == 0
    assert yao_personunit._fund_agenda_take == 0
    assert yao_personunit._fund_agenda_ratio_give == 0
    assert yao_personunit._fund_agenda_ratio_take == 0
    assert yao_personunit.knot == default_knot_if_None()
    assert yao_personunit.respect_bit == default_RespectBit_if_None()


def test_personunit_shop_CorrectlySetsAttributes_knot():
    # ESTABLISH
    slash_str = "/"

    # WHEN
    yao_personunit = personunit_shop("Yao", knot=slash_str)

    # THEN
    assert yao_personunit.knot == slash_str


def test_personunit_shop_CorrectlySetsAttributes_respect_bit():
    # ESTABLISH
    respect_bit_float = 00.45

    # WHEN
    yao_personunit = personunit_shop("Yao", respect_bit=respect_bit_float)

    # THEN
    assert yao_personunit.respect_bit == 1


def test_PersonUnit_set_respect_bit_CorrectlySetsAttribute():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    assert bob_personunit.respect_bit == 1

    # WHEN
    x_respect_bit = 5
    bob_personunit.set_respect_bit(x_respect_bit)

    # THEN
    assert bob_personunit.respect_bit == x_respect_bit


def test_PersonUnit_set_person_cred_points_CorrectlySetsAttribute():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")

    # WHEN
    x_person_cred_points = 23
    bob_personunit.set_person_cred_points(x_person_cred_points)

    # THEN
    assert bob_personunit.person_cred_points == x_person_cred_points


def test_PersonUnit_set_person_debt_points_CorrectlySetsAttribute():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")

    # WHEN
    x_person_debt_points = 23
    bob_personunit.set_person_debt_points(x_person_debt_points)

    # THEN
    assert bob_personunit.person_debt_points == x_person_debt_points


def test_PersonUnit_set_credor_person_debt_points_SetsAttr_Scenario0():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    assert bob_personunit.person_cred_points == 1
    assert bob_personunit.person_debt_points == 1

    # WHEN
    bob_personunit.set_credor_person_debt_points(
        person_cred_points=23, person_debt_points=34
    )

    # THEN
    assert bob_personunit.person_cred_points == 23
    assert bob_personunit.person_debt_points == 34


def test_PersonUnit_set_credor_person_debt_points_IgnoresNoneArgs_Scenario0():
    # ESTABLISH
    bob_personunit = personunit_shop(
        "Bob", person_cred_points=45, person_debt_points=56
    )
    assert bob_personunit.person_cred_points == 45
    assert bob_personunit.person_debt_points == 56

    # WHEN
    bob_personunit.set_credor_person_debt_points(
        person_cred_points=None, person_debt_points=None
    )

    # THEN
    assert bob_personunit.person_cred_points == 45
    assert bob_personunit.person_debt_points == 56


def test_PersonUnit_set_credor_person_debt_points_IgnoresNoneArgs_Scenario1():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    assert bob_personunit.person_cred_points == 1
    assert bob_personunit.person_debt_points == 1

    # WHEN
    bob_personunit.set_credor_person_debt_points(
        person_cred_points=None, person_debt_points=None
    )

    # THEN
    assert bob_personunit.person_cred_points == 1
    assert bob_personunit.person_debt_points == 1


def test_PersonUnit_add_irrational_person_debt_points_SetsAttrCorrectly():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    assert bob_personunit._irrational_person_debt_points == 0

    # WHEN
    bob_int1 = 11
    bob_personunit.add_irrational_person_debt_points(bob_int1)

    # THEN
    assert bob_personunit._irrational_person_debt_points == bob_int1

    # WHEN
    bob_int2 = 22
    bob_personunit.add_irrational_person_debt_points(bob_int2)

    # THEN
    assert bob_personunit._irrational_person_debt_points == bob_int1 + bob_int2


def test_PersonUnit_add_inallocable_person_debt_points_SetsAttrCorrectly():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    assert bob_personunit._inallocable_person_debt_points == 0

    # WHEN
    bob_int1 = 11
    bob_personunit.add_inallocable_person_debt_points(bob_int1)

    # THEN
    assert bob_personunit._inallocable_person_debt_points == bob_int1

    # WHEN
    bob_int2 = 22
    bob_personunit.add_inallocable_person_debt_points(bob_int2)

    # THEN
    assert bob_personunit._inallocable_person_debt_points == bob_int1 + bob_int2


def test_PersonUnit_reset_listen_calculated_attrs_SetsAttrCorrectly():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    bob_int1 = 11
    bob_int2 = 22
    bob_personunit.add_irrational_person_debt_points(bob_int1)
    bob_personunit.add_inallocable_person_debt_points(bob_int2)
    assert bob_personunit._irrational_person_debt_points == bob_int1
    assert bob_personunit._inallocable_person_debt_points == bob_int2

    # WHEN
    bob_personunit.reset_listen_calculated_attrs()

    # THEN
    assert bob_personunit._irrational_person_debt_points == 0
    assert bob_personunit._inallocable_person_debt_points == 0


def test_PersonUnit_clear_fund_give_take_SetsAttrCorrectly():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    bob_personunit._fund_give = 0.27
    bob_personunit._fund_take = 0.37
    bob_personunit._fund_agenda_give = 0.41
    bob_personunit._fund_agenda_take = 0.51
    bob_personunit._fund_agenda_ratio_give = 0.433
    bob_personunit._fund_agenda_ratio_take = 0.533
    assert bob_personunit._fund_give == 0.27
    assert bob_personunit._fund_take == 0.37
    assert bob_personunit._fund_agenda_give == 0.41
    assert bob_personunit._fund_agenda_take == 0.51
    assert bob_personunit._fund_agenda_ratio_give == 0.433
    assert bob_personunit._fund_agenda_ratio_take == 0.533

    # WHEN
    bob_personunit.clear_fund_give_take()

    # THEN
    assert bob_personunit._fund_give == 0
    assert bob_personunit._fund_take == 0
    assert bob_personunit._fund_agenda_give == 0
    assert bob_personunit._fund_agenda_take == 0
    assert bob_personunit._fund_agenda_ratio_give == 0
    assert bob_personunit._fund_agenda_ratio_take == 0


def test_PersonUnit_add_fund_agenda_give_SetsAttr():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    bob_personunit._fund_agenda_give = 0.41
    assert bob_personunit._fund_agenda_give == 0.41

    # WHEN
    bob_personunit.add_fund_agenda_give(0.3)

    # THEN
    assert bob_personunit._fund_agenda_give == 0.71


def test_PersonUnit_add_fund_agenda_take_SetsAttr():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    bob_personunit._fund_agenda_take = 0.41
    assert bob_personunit._fund_agenda_take == 0.41

    # WHEN
    bob_personunit.add_fund_agenda_take(0.3)

    # THEN
    assert bob_personunit._fund_agenda_take == 0.71


def test_PersonUnit_add_fund_give_take_SetsAttrCorrectly():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob")
    bob_personunit._fund_give = 0.4106
    bob_personunit._fund_take = 0.1106
    bob_personunit._fund_agenda_give = 0.41
    bob_personunit._fund_agenda_take = 0.51
    assert bob_personunit._fund_agenda_give == 0.41
    assert bob_personunit._fund_agenda_take == 0.51

    # WHEN
    bob_personunit.add_fund_give_take(
        fund_give=0.33,
        fund_take=0.055,
        fund_agenda_give=0.3,
        fund_agenda_take=0.05,
    )

    # THEN
    assert bob_personunit._fund_give == 0.7406
    assert bob_personunit._fund_take == 0.1656
    assert bob_personunit._fund_agenda_give == 0.71
    assert bob_personunit._fund_agenda_take == 0.56


def test_PersonUnit_set_personunits_fund_agenda_ratios_SetsAttrCorrectly():
    # ESTABLISH
    bob_personunit = personunit_shop("Bob", person_cred_points=15, person_debt_points=7)
    bob_personunit._fund_give = 0.4106
    bob_personunit._fund_take = 0.1106
    bob_personunit._fund_agenda_give = 0.041
    bob_personunit._fund_agenda_take = 0.051
    bob_personunit._fund_agenda_ratio_give = 0
    bob_personunit._fund_agenda_ratio_take = 0
    assert bob_personunit._fund_agenda_ratio_give == 0
    assert bob_personunit._fund_agenda_ratio_take == 0

    # WHEN
    bob_personunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=0.2,
        fund_agenda_ratio_take_sum=0.5,
        personunits_person_cred_points_sum=20,
        personunits_person_debt_points_sum=14,
    )

    # THEN
    assert bob_personunit._fund_agenda_ratio_give == 0.205
    assert bob_personunit._fund_agenda_ratio_take == 0.102

    # WHEN
    bob_personunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=0,
        fund_agenda_ratio_take_sum=0,
        personunits_person_cred_points_sum=20,
        personunits_person_debt_points_sum=14,
    )

    # THEN
    assert bob_personunit._fund_agenda_ratio_give == 0.75
    assert bob_personunit._fund_agenda_ratio_take == 0.5
