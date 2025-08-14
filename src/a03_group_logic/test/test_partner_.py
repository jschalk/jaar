from pytest import raises as pytest_raises
from src.a01_term_logic.rope import default_knot_if_None
from src.a02_finance_logic.finance_config import default_RespectBit_if_None
from src.a03_group_logic.partner import PartnerUnit, partnerunit_shop
from src.a03_group_logic.test._util.a03_str import (
    _credor_pool_str,
    _debtor_pool_str,
    _fund_agenda_give_str,
    _fund_agenda_ratio_give_str,
    _fund_agenda_ratio_take_str,
    _fund_agenda_take_str,
    _fund_give_str,
    _fund_take_str,
    _inallocable_partner_debt_points_str,
    _irrational_partner_debt_points_str,
    _memberships_str,
    knot_str,
    partner_cred_points_str,
    partner_debt_points_str,
    partner_name_str,
    respect_bit_str,
)


def test_PartnerUnit_Exists():
    # ESTABLISH
    bob_str = "Bob"

    # WHEN
    bob_partnerunit = PartnerUnit(bob_str)

    # THEN
    print(f"{bob_str}")
    assert bob_partnerunit
    assert bob_partnerunit.partner_name
    assert bob_partnerunit.partner_name == bob_str
    assert not bob_partnerunit.partner_cred_points
    assert not bob_partnerunit.partner_debt_points
    # calculated fields
    assert not bob_partnerunit._credor_pool
    assert not bob_partnerunit._debtor_pool
    assert not bob_partnerunit._memberships
    assert not bob_partnerunit._irrational_partner_debt_points
    assert not bob_partnerunit._inallocable_partner_debt_points
    assert not bob_partnerunit._fund_give
    assert not bob_partnerunit._fund_take
    assert not bob_partnerunit._fund_agenda_give
    assert not bob_partnerunit._fund_agenda_take
    assert not bob_partnerunit.knot
    assert not bob_partnerunit.respect_bit
    obj_attrs = set(bob_partnerunit.__dict__.keys())
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
        _inallocable_partner_debt_points_str(),
        _irrational_partner_debt_points_str(),
        _memberships_str(),
        respect_bit_str(),
        partner_name_str(),
        knot_str(),
        partner_cred_points_str(),
        partner_debt_points_str(),
    }


def test_PartnerUnit_set_nameterm_SetsAttr():
    # ESTABLISH
    x_partnerunit = PartnerUnit()

    # WHEN
    bob_str = "Bob"
    x_partnerunit.set_nameterm(bob_str)

    # THEN
    assert x_partnerunit.partner_name == bob_str


def test_PartnerUnit_set_nameterm_RaisesErrorIfParameterContains_knot():
    # ESTABLISH
    slash_str = "/"
    texas_str = f"Texas{slash_str}Arkansas"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        partnerunit_shop(partner_name=texas_str, knot=slash_str)
    assert (
        str(excinfo.value)
        == f"'{texas_str}' needs to be a LabelTerm. Cannot contain {knot_str()}: '{slash_str}'"
    )


def test_partnerunit_shop_SetsAttributes():
    # ESTABLISH
    yao_str = "Yao"

    # WHEN
    yao_partnerunit = partnerunit_shop(partner_name=yao_str)

    # THEN
    assert yao_partnerunit.partner_name == yao_str
    assert yao_partnerunit.partner_cred_points == 1
    assert yao_partnerunit.partner_debt_points == 1
    # calculated fields
    assert yao_partnerunit._credor_pool == 0
    assert yao_partnerunit._debtor_pool == 0
    assert yao_partnerunit._memberships == {}
    assert yao_partnerunit._irrational_partner_debt_points == 0
    assert yao_partnerunit._inallocable_partner_debt_points == 0
    assert yao_partnerunit._fund_give == 0
    assert yao_partnerunit._fund_take == 0
    assert yao_partnerunit._fund_agenda_give == 0
    assert yao_partnerunit._fund_agenda_take == 0
    assert yao_partnerunit._fund_agenda_ratio_give == 0
    assert yao_partnerunit._fund_agenda_ratio_take == 0
    assert yao_partnerunit.knot == default_knot_if_None()
    assert yao_partnerunit.respect_bit == default_RespectBit_if_None()


def test_partnerunit_shop_SetsAttributes_knot():
    # ESTABLISH
    slash_str = "/"

    # WHEN
    yao_partnerunit = partnerunit_shop("Yao", knot=slash_str)

    # THEN
    assert yao_partnerunit.knot == slash_str


def test_partnerunit_shop_SetsAttributes_respect_bit():
    # ESTABLISH
    respect_bit_float = 00.45

    # WHEN
    yao_partnerunit = partnerunit_shop("Yao", respect_bit=respect_bit_float)

    # THEN
    assert yao_partnerunit.respect_bit == 1


def test_PartnerUnit_set_respect_bit_SetsAttribute():
    # ESTABLISH
    bob_partnerunit = partnerunit_shop("Bob")
    assert bob_partnerunit.respect_bit == 1

    # WHEN
    x_respect_bit = 5
    bob_partnerunit.set_respect_bit(x_respect_bit)

    # THEN
    assert bob_partnerunit.respect_bit == x_respect_bit


def test_PartnerUnit_set_partner_cred_points_SetsAttribute():
    # ESTABLISH
    bob_partnerunit = partnerunit_shop("Bob")

    # WHEN
    x_partner_cred_points = 23
    bob_partnerunit.set_partner_cred_points(x_partner_cred_points)

    # THEN
    assert bob_partnerunit.partner_cred_points == x_partner_cred_points


def test_PartnerUnit_set_partner_debt_points_SetsAttribute():
    # ESTABLISH
    bob_partnerunit = partnerunit_shop("Bob")

    # WHEN
    x_partner_debt_points = 23
    bob_partnerunit.set_partner_debt_points(x_partner_debt_points)

    # THEN
    assert bob_partnerunit.partner_debt_points == x_partner_debt_points


def test_PartnerUnit_set_credor_partner_debt_points_SetsAttr_Scenario0():
    # ESTABLISH
    bob_partnerunit = partnerunit_shop("Bob")
    assert bob_partnerunit.partner_cred_points == 1
    assert bob_partnerunit.partner_debt_points == 1

    # WHEN
    bob_partnerunit.set_credor_partner_debt_points(
        partner_cred_points=23, partner_debt_points=34
    )

    # THEN
    assert bob_partnerunit.partner_cred_points == 23
    assert bob_partnerunit.partner_debt_points == 34


def test_PartnerUnit_set_credor_partner_debt_points_IgnoresNoneArgs_Scenario0():
    # ESTABLISH
    bob_partnerunit = partnerunit_shop(
        "Bob", partner_cred_points=45, partner_debt_points=56
    )
    assert bob_partnerunit.partner_cred_points == 45
    assert bob_partnerunit.partner_debt_points == 56

    # WHEN
    bob_partnerunit.set_credor_partner_debt_points(
        partner_cred_points=None, partner_debt_points=None
    )

    # THEN
    assert bob_partnerunit.partner_cred_points == 45
    assert bob_partnerunit.partner_debt_points == 56


def test_PartnerUnit_set_credor_partner_debt_points_IgnoresNoneArgs_Scenario1():
    # ESTABLISH
    bob_partnerunit = partnerunit_shop("Bob")
    assert bob_partnerunit.partner_cred_points == 1
    assert bob_partnerunit.partner_debt_points == 1

    # WHEN
    bob_partnerunit.set_credor_partner_debt_points(
        partner_cred_points=None, partner_debt_points=None
    )

    # THEN
    assert bob_partnerunit.partner_cred_points == 1
    assert bob_partnerunit.partner_debt_points == 1


def test_PartnerUnit_add_irrational_partner_debt_points_SetsAttr():
    # ESTABLISH
    bob_partnerunit = partnerunit_shop("Bob")
    assert bob_partnerunit._irrational_partner_debt_points == 0

    # WHEN
    bob_int1 = 11
    bob_partnerunit.add_irrational_partner_debt_points(bob_int1)

    # THEN
    assert bob_partnerunit._irrational_partner_debt_points == bob_int1

    # WHEN
    bob_int2 = 22
    bob_partnerunit.add_irrational_partner_debt_points(bob_int2)

    # THEN
    assert bob_partnerunit._irrational_partner_debt_points == bob_int1 + bob_int2


def test_PartnerUnit_add_inallocable_partner_debt_points_SetsAttr():
    # ESTABLISH
    bob_partnerunit = partnerunit_shop("Bob")
    assert bob_partnerunit._inallocable_partner_debt_points == 0

    # WHEN
    bob_int1 = 11
    bob_partnerunit.add_inallocable_partner_debt_points(bob_int1)

    # THEN
    assert bob_partnerunit._inallocable_partner_debt_points == bob_int1

    # WHEN
    bob_int2 = 22
    bob_partnerunit.add_inallocable_partner_debt_points(bob_int2)

    # THEN
    assert bob_partnerunit._inallocable_partner_debt_points == bob_int1 + bob_int2


def test_PartnerUnit_reset_listen_calculated_attrs_SetsAttr():
    # ESTABLISH
    bob_partnerunit = partnerunit_shop("Bob")
    bob_int1 = 11
    bob_int2 = 22
    bob_partnerunit.add_irrational_partner_debt_points(bob_int1)
    bob_partnerunit.add_inallocable_partner_debt_points(bob_int2)
    assert bob_partnerunit._irrational_partner_debt_points == bob_int1
    assert bob_partnerunit._inallocable_partner_debt_points == bob_int2

    # WHEN
    bob_partnerunit.reset_listen_calculated_attrs()

    # THEN
    assert bob_partnerunit._irrational_partner_debt_points == 0
    assert bob_partnerunit._inallocable_partner_debt_points == 0


def test_PartnerUnit_clear_fund_give_take_SetsAttr():
    # ESTABLISH
    bob_partnerunit = partnerunit_shop("Bob")
    bob_partnerunit._fund_give = 0.27
    bob_partnerunit._fund_take = 0.37
    bob_partnerunit._fund_agenda_give = 0.41
    bob_partnerunit._fund_agenda_take = 0.51
    bob_partnerunit._fund_agenda_ratio_give = 0.433
    bob_partnerunit._fund_agenda_ratio_take = 0.533
    assert bob_partnerunit._fund_give == 0.27
    assert bob_partnerunit._fund_take == 0.37
    assert bob_partnerunit._fund_agenda_give == 0.41
    assert bob_partnerunit._fund_agenda_take == 0.51
    assert bob_partnerunit._fund_agenda_ratio_give == 0.433
    assert bob_partnerunit._fund_agenda_ratio_take == 0.533

    # WHEN
    bob_partnerunit.clear_fund_give_take()

    # THEN
    assert bob_partnerunit._fund_give == 0
    assert bob_partnerunit._fund_take == 0
    assert bob_partnerunit._fund_agenda_give == 0
    assert bob_partnerunit._fund_agenda_take == 0
    assert bob_partnerunit._fund_agenda_ratio_give == 0
    assert bob_partnerunit._fund_agenda_ratio_take == 0


def test_PartnerUnit_add_fund_agenda_give_SetsAttr():
    # ESTABLISH
    bob_partnerunit = partnerunit_shop("Bob")
    bob_partnerunit._fund_agenda_give = 0.41
    assert bob_partnerunit._fund_agenda_give == 0.41

    # WHEN
    bob_partnerunit.add_fund_agenda_give(0.3)

    # THEN
    assert bob_partnerunit._fund_agenda_give == 0.71


def test_PartnerUnit_add_fund_agenda_take_SetsAttr():
    # ESTABLISH
    bob_partnerunit = partnerunit_shop("Bob")
    bob_partnerunit._fund_agenda_take = 0.41
    assert bob_partnerunit._fund_agenda_take == 0.41

    # WHEN
    bob_partnerunit.add_fund_agenda_take(0.3)

    # THEN
    assert bob_partnerunit._fund_agenda_take == 0.71


def test_PartnerUnit_add_fund_give_take_SetsAttr():
    # ESTABLISH
    bob_partnerunit = partnerunit_shop("Bob")
    bob_partnerunit._fund_give = 0.4106
    bob_partnerunit._fund_take = 0.1106
    bob_partnerunit._fund_agenda_give = 0.41
    bob_partnerunit._fund_agenda_take = 0.51
    assert bob_partnerunit._fund_agenda_give == 0.41
    assert bob_partnerunit._fund_agenda_take == 0.51

    # WHEN
    bob_partnerunit.add_fund_give_take(
        fund_give=0.33,
        fund_take=0.055,
        fund_agenda_give=0.3,
        fund_agenda_take=0.05,
    )

    # THEN
    assert bob_partnerunit._fund_give == 0.7406
    assert bob_partnerunit._fund_take == 0.1656
    assert bob_partnerunit._fund_agenda_give == 0.71
    assert bob_partnerunit._fund_agenda_take == 0.56


def test_PartnerUnit_set_partnerunits_fund_agenda_ratios_SetsAttr():
    # ESTABLISH
    bob_partnerunit = partnerunit_shop(
        "Bob", partner_cred_points=15, partner_debt_points=7
    )
    bob_partnerunit._fund_give = 0.4106
    bob_partnerunit._fund_take = 0.1106
    bob_partnerunit._fund_agenda_give = 0.041
    bob_partnerunit._fund_agenda_take = 0.051
    bob_partnerunit._fund_agenda_ratio_give = 0
    bob_partnerunit._fund_agenda_ratio_take = 0
    assert bob_partnerunit._fund_agenda_ratio_give == 0
    assert bob_partnerunit._fund_agenda_ratio_take == 0

    # WHEN
    bob_partnerunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=0.2,
        fund_agenda_ratio_take_sum=0.5,
        partnerunits_partner_cred_points_sum=20,
        partnerunits_partner_debt_points_sum=14,
    )

    # THEN
    assert bob_partnerunit._fund_agenda_ratio_give == 0.205
    assert bob_partnerunit._fund_agenda_ratio_take == 0.102

    # WHEN
    bob_partnerunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=0,
        fund_agenda_ratio_take_sum=0,
        partnerunits_partner_cred_points_sum=20,
        partnerunits_partner_debt_points_sum=14,
    )

    # THEN
    assert bob_partnerunit._fund_agenda_ratio_give == 0.75
    assert bob_partnerunit._fund_agenda_ratio_take == 0.5
