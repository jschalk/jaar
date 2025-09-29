from pytest import raises as pytest_raises
from src.ch02_rope_logic.rope import default_knot_if_None
from src.ch03_finance_logic.finance_config import default_RespectBit_if_None
from src.ch04_voice_logic._ref.ch04_keywords import (
    Ch02Keywords as wx,
    Ch04Keywords as wx,
)
from src.ch04_voice_logic.voice import VoiceUnit, voiceunit_shop


def test_VoiceUnit_Exists():
    # ESTABLISH
    bob_str = "Bob"

    # WHEN
    bob_voiceunit = VoiceUnit(bob_str)

    # THEN
    print(f"{bob_str}")
    assert bob_voiceunit
    assert bob_voiceunit.voice_name
    assert bob_voiceunit.voice_name == bob_str
    assert not bob_voiceunit.voice_cred_points
    assert not bob_voiceunit.voice_debt_points
    # calculated fields
    assert not bob_voiceunit.credor_pool
    assert not bob_voiceunit.debtor_pool
    assert not bob_voiceunit.memberships
    assert not bob_voiceunit.irrational_voice_debt_points
    assert not bob_voiceunit.inallocable_voice_debt_points
    assert not bob_voiceunit.fund_give
    assert not bob_voiceunit.fund_take
    assert not bob_voiceunit.fund_agenda_give
    assert not bob_voiceunit.fund_agenda_take
    assert not bob_voiceunit.knot
    assert not bob_voiceunit.respect_bit
    obj_attrs = set(bob_voiceunit.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        wx.credor_pool,
        wx.debtor_pool,
        wx.fund_agenda_give,
        wx.fund_agenda_ratio_give,
        wx.fund_agenda_ratio_take,
        wx.fund_agenda_take,
        wx.fund_give,
        wx.fund_take,
        wx.inallocable_voice_debt_points,
        wx.irrational_voice_debt_points,
        wx.memberships,
        wx.respect_bit,
        wx.voice_name,
        wx.knot,
        wx.voice_cred_points,
        wx.voice_debt_points,
    }


def test_VoiceUnit_set_nameterm_SetsAttr():
    # ESTABLISH
    x_voiceunit = VoiceUnit()

    # WHEN
    bob_str = "Bob"
    x_voiceunit.set_name(bob_str)

    # THEN
    assert x_voiceunit.voice_name == bob_str


def test_VoiceUnit_set_nameterm_RaisesErrorIfParameterContains_knot():
    # ESTABLISH
    slash_str = "/"
    texas_str = f"Texas{slash_str}Arkansas"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        voiceunit_shop(voice_name=texas_str, knot=slash_str)
    assert (
        str(excinfo.value)
        == f"'{texas_str}' needs to be a LabelTerm. Cannot contain {wx.knot}: '{slash_str}'"
    )


def test_voiceunit_shop_SetsAttributes():
    # ESTABLISH
    yao_str = "Yao"

    # WHEN
    yao_voiceunit = voiceunit_shop(voice_name=yao_str)

    # THEN
    assert yao_voiceunit.voice_name == yao_str
    assert yao_voiceunit.voice_cred_points == 1
    assert yao_voiceunit.voice_debt_points == 1
    # calculated fields
    assert yao_voiceunit.credor_pool == 0
    assert yao_voiceunit.debtor_pool == 0
    assert yao_voiceunit.memberships == {}
    assert yao_voiceunit.irrational_voice_debt_points == 0
    assert yao_voiceunit.inallocable_voice_debt_points == 0
    assert yao_voiceunit.fund_give == 0
    assert yao_voiceunit.fund_take == 0
    assert yao_voiceunit.fund_agenda_give == 0
    assert yao_voiceunit.fund_agenda_take == 0
    assert yao_voiceunit.fund_agenda_ratio_give == 0
    assert yao_voiceunit.fund_agenda_ratio_take == 0
    assert yao_voiceunit.knot == default_knot_if_None()
    assert yao_voiceunit.respect_bit == default_RespectBit_if_None()


def test_voiceunit_shop_SetsAttributes_knot():
    # ESTABLISH
    slash_str = "/"

    # WHEN
    yao_voiceunit = voiceunit_shop("Yao", knot=slash_str)

    # THEN
    assert yao_voiceunit.knot == slash_str


def test_voiceunit_shop_SetsAttributes_respect_bit():
    # ESTABLISH
    respect_bit_float = 00.45

    # WHEN
    yao_voiceunit = voiceunit_shop("Yao", respect_bit=respect_bit_float)

    # THEN
    assert yao_voiceunit.respect_bit == 1


def test_VoiceUnit_set_respect_bit_SetsAttribute():
    # ESTABLISH
    bob_voiceunit = voiceunit_shop("Bob")
    assert bob_voiceunit.respect_bit == 1

    # WHEN
    x_respect_bit = 5
    bob_voiceunit.set_respect_bit(x_respect_bit)

    # THEN
    assert bob_voiceunit.respect_bit == x_respect_bit


def test_VoiceUnit_set_voice_cred_points_SetsAttribute():
    # ESTABLISH
    bob_voiceunit = voiceunit_shop("Bob")

    # WHEN
    x_voice_cred_points = 23
    bob_voiceunit.set_voice_cred_points(x_voice_cred_points)

    # THEN
    assert bob_voiceunit.voice_cred_points == x_voice_cred_points


def test_VoiceUnit_set_voice_debt_points_SetsAttribute():
    # ESTABLISH
    bob_voiceunit = voiceunit_shop("Bob")

    # WHEN
    x_voice_debt_points = 23
    bob_voiceunit.set_voice_debt_points(x_voice_debt_points)

    # THEN
    assert bob_voiceunit.voice_debt_points == x_voice_debt_points


def test_VoiceUnit_set_credor_voice_debt_points_SetsAttr_Scenario0():
    # ESTABLISH
    bob_voiceunit = voiceunit_shop("Bob")
    assert bob_voiceunit.voice_cred_points == 1
    assert bob_voiceunit.voice_debt_points == 1

    # WHEN
    bob_voiceunit.set_credor_voice_debt_points(
        voice_cred_points=23, voice_debt_points=34
    )

    # THEN
    assert bob_voiceunit.voice_cred_points == 23
    assert bob_voiceunit.voice_debt_points == 34


def test_VoiceUnit_set_credor_voice_debt_points_IgnoresNoneArgs_Scenario0():
    # ESTABLISH
    bob_voiceunit = voiceunit_shop("Bob", voice_cred_points=45, voice_debt_points=56)
    assert bob_voiceunit.voice_cred_points == 45
    assert bob_voiceunit.voice_debt_points == 56

    # WHEN
    bob_voiceunit.set_credor_voice_debt_points(
        voice_cred_points=None, voice_debt_points=None
    )

    # THEN
    assert bob_voiceunit.voice_cred_points == 45
    assert bob_voiceunit.voice_debt_points == 56


def test_VoiceUnit_set_credor_voice_debt_points_IgnoresNoneArgs_Scenario1():
    # ESTABLISH
    bob_voiceunit = voiceunit_shop("Bob")
    assert bob_voiceunit.voice_cred_points == 1
    assert bob_voiceunit.voice_debt_points == 1

    # WHEN
    bob_voiceunit.set_credor_voice_debt_points(
        voice_cred_points=None, voice_debt_points=None
    )

    # THEN
    assert bob_voiceunit.voice_cred_points == 1
    assert bob_voiceunit.voice_debt_points == 1


def test_VoiceUnit_add_irrational_voice_debt_points_SetsAttr():
    # ESTABLISH
    bob_voiceunit = voiceunit_shop("Bob")
    assert bob_voiceunit.irrational_voice_debt_points == 0

    # WHEN
    bob_int1 = 11
    bob_voiceunit.add_irrational_voice_debt_points(bob_int1)

    # THEN
    assert bob_voiceunit.irrational_voice_debt_points == bob_int1

    # WHEN
    bob_int2 = 22
    bob_voiceunit.add_irrational_voice_debt_points(bob_int2)

    # THEN
    assert bob_voiceunit.irrational_voice_debt_points == bob_int1 + bob_int2


def test_VoiceUnit_add_inallocable_voice_debt_points_SetsAttr():
    # ESTABLISH
    bob_voiceunit = voiceunit_shop("Bob")
    assert bob_voiceunit.inallocable_voice_debt_points == 0

    # WHEN
    bob_int1 = 11
    bob_voiceunit.add_inallocable_voice_debt_points(bob_int1)

    # THEN
    assert bob_voiceunit.inallocable_voice_debt_points == bob_int1

    # WHEN
    bob_int2 = 22
    bob_voiceunit.add_inallocable_voice_debt_points(bob_int2)

    # THEN
    assert bob_voiceunit.inallocable_voice_debt_points == bob_int1 + bob_int2


def test_VoiceUnit_reset_listen_calculated_attrs_SetsAttr():
    # ESTABLISH
    bob_voiceunit = voiceunit_shop("Bob")
    bob_int1 = 11
    bob_int2 = 22
    bob_voiceunit.add_irrational_voice_debt_points(bob_int1)
    bob_voiceunit.add_inallocable_voice_debt_points(bob_int2)
    assert bob_voiceunit.irrational_voice_debt_points == bob_int1
    assert bob_voiceunit.inallocable_voice_debt_points == bob_int2

    # WHEN
    bob_voiceunit.reset_listen_calculated_attrs()

    # THEN
    assert bob_voiceunit.irrational_voice_debt_points == 0
    assert bob_voiceunit.inallocable_voice_debt_points == 0


def test_VoiceUnit_clear_fund_give_take_SetsAttr():
    # ESTABLISH
    bob_voiceunit = voiceunit_shop("Bob")
    bob_voiceunit.fund_give = 0.27
    bob_voiceunit.fund_take = 0.37
    bob_voiceunit.fund_agenda_give = 0.41
    bob_voiceunit.fund_agenda_take = 0.51
    bob_voiceunit.fund_agenda_ratio_give = 0.433
    bob_voiceunit.fund_agenda_ratio_take = 0.533
    assert bob_voiceunit.fund_give == 0.27
    assert bob_voiceunit.fund_take == 0.37
    assert bob_voiceunit.fund_agenda_give == 0.41
    assert bob_voiceunit.fund_agenda_take == 0.51
    assert bob_voiceunit.fund_agenda_ratio_give == 0.433
    assert bob_voiceunit.fund_agenda_ratio_take == 0.533

    # WHEN
    bob_voiceunit.clear_fund_give_take()

    # THEN
    assert bob_voiceunit.fund_give == 0
    assert bob_voiceunit.fund_take == 0
    assert bob_voiceunit.fund_agenda_give == 0
    assert bob_voiceunit.fund_agenda_take == 0
    assert bob_voiceunit.fund_agenda_ratio_give == 0
    assert bob_voiceunit.fund_agenda_ratio_take == 0


def test_VoiceUnit_add_fund_agenda_give_SetsAttr():
    # ESTABLISH
    bob_voiceunit = voiceunit_shop("Bob")
    bob_voiceunit.fund_agenda_give = 0.41
    assert bob_voiceunit.fund_agenda_give == 0.41

    # WHEN
    bob_voiceunit.add_fund_agenda_give(0.3)

    # THEN
    assert bob_voiceunit.fund_agenda_give == 0.71


def test_VoiceUnit_add_fund_agenda_take_SetsAttr():
    # ESTABLISH
    bob_voiceunit = voiceunit_shop("Bob")
    bob_voiceunit.fund_agenda_take = 0.41
    assert bob_voiceunit.fund_agenda_take == 0.41

    # WHEN
    bob_voiceunit.add_fund_agenda_take(0.3)

    # THEN
    assert bob_voiceunit.fund_agenda_take == 0.71


def test_VoiceUnit_add_fund_give_take_SetsAttr():
    # ESTABLISH
    bob_voiceunit = voiceunit_shop("Bob")
    bob_voiceunit.fund_give = 0.4106
    bob_voiceunit.fund_take = 0.1106
    bob_voiceunit.fund_agenda_give = 0.41
    bob_voiceunit.fund_agenda_take = 0.51
    assert bob_voiceunit.fund_agenda_give == 0.41
    assert bob_voiceunit.fund_agenda_take == 0.51

    # WHEN
    bob_voiceunit.add_fund_give_take(
        fund_give=0.33,
        fund_take=0.055,
        fund_agenda_give=0.3,
        fund_agenda_take=0.05,
    )

    # THEN
    assert bob_voiceunit.fund_give == 0.7406
    assert bob_voiceunit.fund_take == 0.1656
    assert bob_voiceunit.fund_agenda_give == 0.71
    assert bob_voiceunit.fund_agenda_take == 0.56


def test_VoiceUnit_set_voiceunits_fund_agenda_ratios_SetsAttr():
    # ESTABLISH
    bob_voiceunit = voiceunit_shop("Bob", voice_cred_points=15, voice_debt_points=7)
    bob_voiceunit.fund_give = 0.4106
    bob_voiceunit.fund_take = 0.1106
    bob_voiceunit.fund_agenda_give = 0.041
    bob_voiceunit.fund_agenda_take = 0.051
    bob_voiceunit.fund_agenda_ratio_give = 0
    bob_voiceunit.fund_agenda_ratio_take = 0
    assert bob_voiceunit.fund_agenda_ratio_give == 0
    assert bob_voiceunit.fund_agenda_ratio_take == 0

    # WHEN
    bob_voiceunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=0.2,
        fund_agenda_ratio_take_sum=0.5,
        voiceunits_voice_cred_points_sum=20,
        voiceunits_voice_debt_points_sum=14,
    )

    # THEN
    assert bob_voiceunit.fund_agenda_ratio_give == 0.205
    assert bob_voiceunit.fund_agenda_ratio_take == 0.102

    # WHEN
    bob_voiceunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=0,
        fund_agenda_ratio_take_sum=0,
        voiceunits_voice_cred_points_sum=20,
        voiceunits_voice_debt_points_sum=14,
    )

    # THEN
    assert bob_voiceunit.fund_agenda_ratio_give == 0.75
    assert bob_voiceunit.fund_agenda_ratio_take == 0.5
