from src._road.road import default_road_delimiter_if_none
from src._road.finance import default_bit_if_none
from src.bud.acct import AcctUnit, acctunit_shop
from pytest import raises as pytest_raises


def test_AcctUnit_exists():
    # ESTABLISH
    bob_text = "Bob"

    # WHEN
    bob_acctunit = AcctUnit(bob_text)

    # THEN
    print(f"{bob_text}")
    assert bob_acctunit is not None
    assert bob_acctunit.acct_id is not None
    assert bob_acctunit.acct_id == bob_text
    assert bob_acctunit.credor_weight is None
    assert bob_acctunit.debtor_weight is None
    # calculated fields
    assert bob_acctunit._credor_pool is None
    assert bob_acctunit._debtor_pool is None
    assert bob_acctunit._lobbyships is None
    assert bob_acctunit._irrational_debtor_weight is None
    assert bob_acctunit._inallocable_debtor_weight is None
    assert bob_acctunit._fund_give is None
    assert bob_acctunit._fund_take is None
    assert bob_acctunit._fund_agenda_give is None
    assert bob_acctunit._fund_agenda_take is None
    assert bob_acctunit._road_delimiter is None
    assert bob_acctunit._bit is None


def test_AcctUnit_set_acct_id_CorrectlySetsAttr():
    # ESTABLISH
    x_acctunit = AcctUnit()

    # WHEN
    bob_text = "Bob"
    x_acctunit.set_acct_id(bob_text)

    # THEN
    assert x_acctunit.acct_id == bob_text


def test_AcctUnit_set_acct_id_RaisesErrorIfParameterContains_road_delimiter():
    # ESTABLISH
    slash_text = "/"
    texas_text = f"Texas{slash_text}Arkansas"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        acctunit_shop(acct_id=texas_text, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{texas_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_acctunit_shop_CorrectlySetsAttributes():
    # WHEN
    yao_text = "Yao"

    # WHEN
    yao_acctunit = acctunit_shop(acct_id=yao_text)

    # THEN
    assert yao_acctunit.acct_id == yao_text
    assert yao_acctunit.credor_weight == 1
    assert yao_acctunit.debtor_weight == 1
    # calculated fields
    assert yao_acctunit._credor_pool == 0
    assert yao_acctunit._debtor_pool == 0
    assert yao_acctunit._lobbyships == {}
    assert yao_acctunit._irrational_debtor_weight == 0
    assert yao_acctunit._inallocable_debtor_weight == 0
    assert yao_acctunit._fund_give == 0
    assert yao_acctunit._fund_take == 0
    assert yao_acctunit._fund_agenda_give == 0
    assert yao_acctunit._fund_agenda_take == 0
    assert yao_acctunit._fund_agenda_ratio_give == 0
    assert yao_acctunit._fund_agenda_ratio_take == 0
    assert yao_acctunit._road_delimiter == default_road_delimiter_if_none()
    assert yao_acctunit._bit == default_bit_if_none()


def test_acctunit_shop_CorrectlySetsAttributes_road_delimiter():
    # ESTABLISH
    slash_text = "/"

    # WHEN
    yao_acctunit = acctunit_shop("Yao", _road_delimiter=slash_text)

    # THEN
    assert yao_acctunit._road_delimiter == slash_text


def test_acctunit_shop_CorrectlySetsAttributes_bit():
    # ESTABLISH
    bit_float = 00.45

    # WHEN
    yao_acctunit = acctunit_shop("Yao", _bit=bit_float)

    # THEN
    assert yao_acctunit._bit == 1


def test_AcctUnit_set_bit_CorrectlySetsAttribute():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    assert bob_acctunit._bit == 1

    # WHEN
    x_bit = 5
    bob_acctunit.set_bit(x_bit)

    # THEN
    assert bob_acctunit._bit == x_bit


def test_AcctUnit_set_credor_weight_CorrectlySetsAttribute():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")

    # WHEN
    x_credor_weight = 23
    bob_acctunit.set_credor_weight(x_credor_weight)

    # THEN
    assert bob_acctunit.credor_weight == x_credor_weight


def test_AcctUnit_set_debtor_weight_CorrectlySetsAttribute():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")

    # WHEN
    x_debtor_weight = 23
    bob_acctunit.set_debtor_weight(x_debtor_weight)

    # THEN
    assert bob_acctunit.debtor_weight == x_debtor_weight


def test_AcctUnit_set_credor_debtor_weight_CorrectlySetsAttributeNoNulls():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")

    # WHEN
    bob_acctunit.set_credor_debtor_weight(credor_weight=23, debtor_weight=34)

    # THEN
    assert bob_acctunit.credor_weight == 23
    assert bob_acctunit.debtor_weight == 34


def test_AcctUnit_set_credor_debtor_weight_CorrectlySetsAttributeWithNullsAndStartingValues():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob", credor_weight=45, debtor_weight=56)

    # WHEN
    bob_acctunit.set_credor_debtor_weight(credor_weight=None, debtor_weight=None)

    # THEN
    assert bob_acctunit.credor_weight == 45
    assert bob_acctunit.debtor_weight == 56


def test_AcctUnit_set_credor_debtor_weight_CorrectlySetsAttributeWithNullsAndNoStartingValues():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")

    # WHEN
    bob_acctunit.set_credor_debtor_weight(credor_weight=None, debtor_weight=None)

    # THEN
    assert bob_acctunit.credor_weight == 1
    assert bob_acctunit.debtor_weight == 1


def test_AcctUnit_add_irrational_debtor_weight_SetsAttrCorrectly():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    assert bob_acctunit._irrational_debtor_weight == 0

    # WHEN
    bob_int1 = 11
    bob_acctunit.add_irrational_debtor_weight(bob_int1)

    # THEN
    assert bob_acctunit._irrational_debtor_weight == bob_int1

    # WHEN
    bob_int2 = 22
    bob_acctunit.add_irrational_debtor_weight(bob_int2)

    # THEN
    assert bob_acctunit._irrational_debtor_weight == bob_int1 + bob_int2


def test_AcctUnit_add_inallocable_debtor_weight_SetsAttrCorrectly():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    assert bob_acctunit._inallocable_debtor_weight == 0

    # WHEN
    bob_int1 = 11
    bob_acctunit.add_inallocable_debtor_weight(bob_int1)

    # THEN
    assert bob_acctunit._inallocable_debtor_weight == bob_int1

    # WHEN
    bob_int2 = 22
    bob_acctunit.add_inallocable_debtor_weight(bob_int2)

    # THEN
    assert bob_acctunit._inallocable_debtor_weight == bob_int1 + bob_int2


def test_AcctUnit_reset_listen_calculated_attrs_SetsAttrCorrectly():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob")
    bob_int1 = 11
    bob_int2 = 22
    bob_acctunit.add_irrational_debtor_weight(bob_int1)
    bob_acctunit.add_inallocable_debtor_weight(bob_int2)
    assert bob_acctunit._irrational_debtor_weight == bob_int1
    assert bob_acctunit._inallocable_debtor_weight == bob_int2

    # WHEN
    bob_acctunit.reset_listen_calculated_attrs()

    # THEN
    assert bob_acctunit._irrational_debtor_weight == 0
    assert bob_acctunit._inallocable_debtor_weight == 0


def test_AcctUnit_reset_fund_give_take_SetsAttrCorrectly():
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
    bob_acctunit.reset_fund_give_take()

    # THEN
    assert bob_acctunit._fund_give == 0
    assert bob_acctunit._fund_take == 0
    assert bob_acctunit._fund_agenda_give == 0
    assert bob_acctunit._fund_agenda_take == 0
    assert bob_acctunit._fund_agenda_ratio_give == 0
    assert bob_acctunit._fund_agenda_ratio_take == 0


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
        bud_agenda_cred=0.3,
        bud_agenda_debt=0.05,
    )

    # THEN
    assert bob_acctunit._fund_give == 0.7406
    assert bob_acctunit._fund_take == 0.1656
    assert bob_acctunit._fund_agenda_give == 0.71
    assert bob_acctunit._fund_agenda_take == 0.56


def test_AcctUnit_set_acctunits_fund_ratios_SetsAttrCorrectly():
    # ESTABLISH
    bob_acctunit = acctunit_shop("Bob", credor_weight=15, debtor_weight=7)
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
        bud_acctunit_total_credor_weight=20,
        bud_acctunit_total_debtor_weight=14,
    )

    # THEN
    assert bob_acctunit._fund_agenda_ratio_give == 0.205
    assert bob_acctunit._fund_agenda_ratio_take == 0.102

    # WHEN
    bob_acctunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=0,
        fund_agenda_ratio_take_sum=0,
        bud_acctunit_total_credor_weight=20,
        bud_acctunit_total_debtor_weight=14,
    )

    # THEN
    assert bob_acctunit._fund_agenda_ratio_give == 0.75
    assert bob_acctunit._fund_agenda_ratio_take == 0.5
