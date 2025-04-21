from src.a02_finance_toolboxs.finance_config import default_fund_coin_if_None
from src.a01_word_logic.road import (
    get_default_fisc_tag as root_tag,
    create_road,
    default_bridge_if_None,
)
from src.a03_group_logic.group import membership_shop
from src.a03_group_logic.group import groupunit_shop, GroupUnit
from pytest import raises as pytest_raises


def test_GroupUnit_exists():
    # ESTABLISH
    swim_str = ";swimmers"
    # WHEN
    swim_groupunit = GroupUnit(group_label=swim_str)
    # THEN
    assert swim_groupunit is not None
    assert swim_groupunit.group_label == swim_str
    assert swim_groupunit._memberships is None
    assert swim_groupunit._fund_give is None
    assert swim_groupunit._fund_take is None
    assert swim_groupunit._fund_agenda_give is None
    assert swim_groupunit._fund_agenda_take is None
    assert swim_groupunit._credor_pool is None
    assert swim_groupunit._debtor_pool is None
    assert swim_groupunit.bridge is None
    assert swim_groupunit.fund_coin is None


def test_groupunit_shop_ReturnsObj():
    # ESTABLISH
    swim_str = ";swimmers"
    nation_road = create_road(root_tag(), "nation-states")
    usa_road = create_road(nation_road, "USA")

    # WHEN
    swim_groupunit = groupunit_shop(group_label=swim_str)

    # THEN
    print(f"{swim_str}")
    assert swim_groupunit is not None
    assert swim_groupunit.group_label is not None
    assert swim_groupunit.group_label == swim_str
    assert swim_groupunit._memberships == {}
    assert swim_groupunit._fund_give == 0
    assert swim_groupunit._fund_take == 0
    assert swim_groupunit._fund_agenda_give == 0
    assert swim_groupunit._fund_agenda_take == 0
    assert swim_groupunit._credor_pool == 0
    assert swim_groupunit._debtor_pool == 0
    assert swim_groupunit.bridge == default_bridge_if_None()
    assert swim_groupunit.fund_coin == default_fund_coin_if_None()


def test_groupunit_shop_ReturnsObj_bridge():
    # ESTABLISH
    swim_str = "/swimmers"
    slash_str = "/"
    x_fund_coin = 7

    # WHEN
    swim_groupunit = groupunit_shop(
        group_label=swim_str, bridge=slash_str, fund_coin=x_fund_coin
    )

    # THEN
    assert swim_groupunit.bridge == slash_str
    assert swim_groupunit.fund_coin == x_fund_coin


# def test_GroupUnit_set_group_label_RaisesErrorIfParameterContains_bridge_And_acct_mirror_True():
#     # ESTABLISH
#     slash_str = "/"
#     bob_str = f"Bob{slash_str}Texas"

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         groupunit_shop(bob_str, _acct_mirror=True, bridge=slash_str)
#     assert (
#         str(excinfo.value)
#         == f"'{bob_str}' needs to be a TagUnit. Cannot contain bridge: '{slash_str}'"
#     )


def test_GroupUnit_set_membership_CorrectlySetsAttr():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    swim_str = ";swimmers"
    yao_swim_membership = membership_shop(swim_str)
    sue_swim_membership = membership_shop(swim_str)
    yao_swim_membership.acct_name = yao_str
    sue_swim_membership.acct_name = sue_str
    swimmers_groupunit = groupunit_shop(swim_str)

    # WHEN
    swimmers_groupunit.set_membership(yao_swim_membership)
    swimmers_groupunit.set_membership(sue_swim_membership)

    # THEN
    swimmers_memberships = {
        yao_swim_membership.acct_name: yao_swim_membership,
        sue_swim_membership.acct_name: sue_swim_membership,
    }
    assert swimmers_groupunit._memberships == swimmers_memberships


def test_GroupUnit_set_membership_SetsAttr_credor_pool_debtor_pool():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    ohio_str = ";Ohio"
    yao_ohio_membership = membership_shop(ohio_str)
    sue_ohio_membership = membership_shop(ohio_str)
    yao_ohio_membership.acct_name = yao_str
    yao_ohio_membership.acct_name = yao_str
    sue_ohio_membership.acct_name = sue_str
    yao_ohio_membership._credor_pool = 66
    sue_ohio_membership._credor_pool = 22
    yao_ohio_membership._debtor_pool = 6600
    sue_ohio_membership._debtor_pool = 2200
    ohio_groupunit = groupunit_shop(ohio_str)
    assert ohio_groupunit._credor_pool == 0
    assert ohio_groupunit._debtor_pool == 0

    # WHEN
    ohio_groupunit.set_membership(yao_ohio_membership)
    # THEN
    assert ohio_groupunit._credor_pool == 66
    assert ohio_groupunit._debtor_pool == 6600

    # WHEN
    ohio_groupunit.set_membership(sue_ohio_membership)
    # THEN
    assert ohio_groupunit._credor_pool == 88
    assert ohio_groupunit._debtor_pool == 8800


def test_GroupUnit_set_membership_RaisesErrorIf_membership_group_label_IsWrong():
    # ESTABLISH
    yao_str = "Yao"
    ohio_str = ";Ohio"
    iowa_str = ";Iowa"
    yao_ohio_membership = membership_shop(ohio_str)
    yao_ohio_membership.acct_name = yao_str
    yao_ohio_membership.acct_name = yao_str
    yao_ohio_membership._credor_pool = 66
    yao_ohio_membership._debtor_pool = 6600
    iowa_groupunit = groupunit_shop(iowa_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        iowa_groupunit.set_membership(yao_ohio_membership)
    assert (
        str(excinfo.value)
        == f"GroupUnit.group_label={iowa_str} cannot set membership.group_label={ohio_str}"
    )


def test_GroupUnit_set_membership_RaisesErrorIf_acct_name_IsNone():
    # ESTABLISH
    ohio_str = ";Ohio"
    ohio_groupunit = groupunit_shop(ohio_str)
    yao_ohio_membership = membership_shop(ohio_str)
    assert yao_ohio_membership.acct_name is None

    with pytest_raises(Exception) as excinfo:
        ohio_groupunit.set_membership(yao_ohio_membership)
    assert (
        str(excinfo.value)
        == f"membership group_label={ohio_str} cannot be set when _acct_name is None."
    )
