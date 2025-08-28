from pytest import raises as pytest_raises
from src.a01_term_logic.rope import default_knot_if_None
from src.a02_finance_logic.finance_config import default_fund_iota_if_None
from src.a03_group_logic.group import GroupUnit, groupunit_shop, membership_shop
from src.a03_group_logic.test._util.a03_str import (
    _memberships_str,
    credor_pool_str,
    debtor_pool_str,
    fund_agenda_give_str,
    fund_agenda_take_str,
    fund_give_str,
    fund_iota_str,
    fund_take_str,
    group_title_str,
    knot_str,
)


def test_GroupUnit_Exists():
    # ESTABLISH / WHEN
    x_groupunit = GroupUnit()
    # THEN
    assert x_groupunit is not None
    assert not x_groupunit.group_title
    assert not x_groupunit._memberships
    assert not x_groupunit.fund_give
    assert not x_groupunit.fund_take
    assert not x_groupunit.fund_agenda_give
    assert not x_groupunit.fund_agenda_take
    assert not x_groupunit.credor_pool
    assert not x_groupunit.debtor_pool
    assert not x_groupunit.knot
    assert not x_groupunit.fund_iota
    print(f"{x_groupunit.__dict__=}")
    assert set(x_groupunit.__dict__.keys()) == {
        group_title_str(),
        _memberships_str(),
        fund_give_str(),
        fund_take_str(),
        fund_agenda_give_str(),
        fund_agenda_take_str(),
        credor_pool_str(),
        debtor_pool_str(),
        knot_str(),
        fund_iota_str(),
    }


def test_groupunit_shop_ReturnsObj():
    # ESTABLISH
    swim_str = ";swimmers"

    # WHEN
    swim_groupunit = groupunit_shop(group_title=swim_str)

    # THEN
    print(f"{swim_str}")
    assert swim_groupunit is not None
    assert swim_groupunit.group_title is not None
    assert swim_groupunit.group_title == swim_str
    assert swim_groupunit._memberships == {}
    assert swim_groupunit.fund_give == 0
    assert swim_groupunit.fund_take == 0
    assert swim_groupunit.fund_agenda_give == 0
    assert swim_groupunit.fund_agenda_take == 0
    assert swim_groupunit.credor_pool == 0
    assert swim_groupunit.debtor_pool == 0
    assert swim_groupunit.knot == default_knot_if_None()
    assert swim_groupunit.fund_iota == default_fund_iota_if_None()


def test_groupunit_shop_ReturnsObj_knot():
    # ESTABLISH
    swim_str = "/swimmers"
    slash_str = "/"
    x_fund_iota = 7

    # WHEN
    swim_groupunit = groupunit_shop(
        group_title=swim_str, knot=slash_str, fund_iota=x_fund_iota
    )

    # THEN
    assert swim_groupunit.knot == slash_str
    assert swim_groupunit.fund_iota == x_fund_iota


# def test_GroupUnit_set_group_title_RaisesErrorIfParameterContains_knot_And_voice_mirror_True():
#     # ESTABLISH
#     slash_str = "/"
#     bob_str = f"Bob{slash_str}Texas"

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         groupunit_shop(bob_str, _voice_mirror=True, knot=slash_str)
#     assert (
#         str(excinfo.value)
#         == f"'{bob_str}' needs to be a LabelTerm. Cannot contain knot: '{slash_str}'"
#     )


def test_GroupUnit_set_membership_SetsAttr():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    swim_str = ";swimmers"
    yao_swim_membership = membership_shop(swim_str)
    sue_swim_membership = membership_shop(swim_str)
    yao_swim_membership.voice_name = yao_str
    sue_swim_membership.voice_name = sue_str
    swimmers_groupunit = groupunit_shop(swim_str)

    # WHEN
    swimmers_groupunit.set_membership(yao_swim_membership)
    swimmers_groupunit.set_membership(sue_swim_membership)

    # THEN
    swimmers_memberships = {
        yao_swim_membership.voice_name: yao_swim_membership,
        sue_swim_membership.voice_name: sue_swim_membership,
    }
    assert swimmers_groupunit._memberships == swimmers_memberships


def test_GroupUnit_set_membership_SetsAttr_credor_pool_debtor_pool():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    ohio_str = ";Ohio"
    yao_ohio_membership = membership_shop(ohio_str)
    sue_ohio_membership = membership_shop(ohio_str)
    yao_ohio_membership.voice_name = yao_str
    yao_ohio_membership.voice_name = yao_str
    sue_ohio_membership.voice_name = sue_str
    yao_ohio_membership.credor_pool = 66
    sue_ohio_membership.credor_pool = 22
    yao_ohio_membership.debtor_pool = 6600
    sue_ohio_membership.debtor_pool = 2200
    ohio_groupunit = groupunit_shop(ohio_str)
    assert ohio_groupunit.credor_pool == 0
    assert ohio_groupunit.debtor_pool == 0

    # WHEN
    ohio_groupunit.set_membership(yao_ohio_membership)
    # THEN
    assert ohio_groupunit.credor_pool == 66
    assert ohio_groupunit.debtor_pool == 6600

    # WHEN
    ohio_groupunit.set_membership(sue_ohio_membership)
    # THEN
    assert ohio_groupunit.credor_pool == 88
    assert ohio_groupunit.debtor_pool == 8800


def test_GroupUnit_set_membership_RaisesErrorIf_membership_group_title_IsWrong():
    # ESTABLISH
    yao_str = "Yao"
    ohio_str = ";Ohio"
    iowa_str = ";Iowa"
    yao_ohio_membership = membership_shop(ohio_str)
    yao_ohio_membership.voice_name = yao_str
    yao_ohio_membership.voice_name = yao_str
    yao_ohio_membership.credor_pool = 66
    yao_ohio_membership.debtor_pool = 6600
    iowa_groupunit = groupunit_shop(iowa_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        iowa_groupunit.set_membership(yao_ohio_membership)
    exception_str = (
        f"GroupUnit.group_title={iowa_str} cannot set membership.group_title={ohio_str}"
    )
    assert str(excinfo.value) == exception_str


def test_GroupUnit_set_membership_RaisesErrorIf_voice_name_IsNone():
    # ESTABLISH
    ohio_str = ";Ohio"
    ohio_groupunit = groupunit_shop(ohio_str)
    yao_ohio_membership = membership_shop(ohio_str)
    assert yao_ohio_membership.voice_name is None

    # WHEN
    with pytest_raises(Exception) as excinfo:
        ohio_groupunit.set_membership(yao_ohio_membership)

    # THEN
    exception_str = (
        f"membership group_title={ohio_str} cannot be set when _voice_name is None."
    )
    assert str(excinfo.value) == exception_str
