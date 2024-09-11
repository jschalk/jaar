from src._road.finance import default_fund_coin_if_none
from src._road.road import (
    get_default_real_id_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from src.bud.group import membership_shop
from src.bud.group import groupbox_shop, GroupBox
from pytest import raises as pytest_raises


def test_GroupBox_exists():
    # ESTABLISH
    swim_str = ";swimmers"
    # WHEN
    swim_groupbox = GroupBox(group_id=swim_str)
    # THEN
    assert swim_groupbox is not None
    assert swim_groupbox.group_id == swim_str
    assert swim_groupbox._memberships is None
    assert swim_groupbox._fund_give is None
    assert swim_groupbox._fund_take is None
    assert swim_groupbox._fund_agenda_give is None
    assert swim_groupbox._fund_agenda_take is None
    assert swim_groupbox._credor_pool is None
    assert swim_groupbox._debtor_pool is None
    assert swim_groupbox._road_delimiter is None
    assert swim_groupbox._fund_coin is None


def test_groupbox_shop_ReturnsCorrectObj():
    # ESTABLISH
    swim_str = ";swimmers"
    nation_road = create_road(root_label(), "nation-states")
    usa_road = create_road(nation_road, "USA")

    # WHEN
    swim_groupbox = groupbox_shop(group_id=swim_str)

    # THEN
    print(f"{swim_str}")
    assert swim_groupbox is not None
    assert swim_groupbox.group_id is not None
    assert swim_groupbox.group_id == swim_str
    assert swim_groupbox._memberships == {}
    assert swim_groupbox._fund_give == 0
    assert swim_groupbox._fund_take == 0
    assert swim_groupbox._fund_agenda_give == 0
    assert swim_groupbox._fund_agenda_take == 0
    assert swim_groupbox._credor_pool == 0
    assert swim_groupbox._debtor_pool == 0
    assert swim_groupbox._road_delimiter == default_road_delimiter_if_none()
    assert swim_groupbox._fund_coin == default_fund_coin_if_none()


def test_groupbox_shop_ReturnsCorrectObj_road_delimiter():
    # ESTABLISH
    swim_str = "/swimmers"
    slash_str = "/"
    x_fund_coin = 7

    # WHEN
    swim_groupbox = groupbox_shop(
        group_id=swim_str, _road_delimiter=slash_str, _fund_coin=x_fund_coin
    )

    # THEN
    assert swim_groupbox._road_delimiter == slash_str
    assert swim_groupbox._fund_coin == x_fund_coin


# def test_GroupBox_set_group_id_RaisesErrorIfParameterContains_road_delimiter_And_acct_mirror_True():
#     # ESTABLISH
#     slash_str = "/"
#     bob_str = f"Bob{slash_str}Texas"

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         groupbox_shop(bob_str, _acct_mirror=True, _road_delimiter=slash_str)
#     assert (
#         str(excinfo.value)
#         == f"'{bob_str}' needs to be a RoadNode. Cannot contain delimiter: '{slash_str}'"
#     )


def test_GroupBox_set_membership_CorrectlySetsAttr():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    swim_str = ";swimmers"
    yao_swim_membership = membership_shop(swim_str)
    sue_swim_membership = membership_shop(swim_str)
    yao_swim_membership._acct_id = yao_str
    sue_swim_membership._acct_id = sue_str
    swimmers_groupbox = groupbox_shop(swim_str)

    # WHEN
    swimmers_groupbox.set_membership(yao_swim_membership)
    swimmers_groupbox.set_membership(sue_swim_membership)

    # THEN
    swimmers_memberships = {
        yao_swim_membership._acct_id: yao_swim_membership,
        sue_swim_membership._acct_id: sue_swim_membership,
    }
    assert swimmers_groupbox._memberships == swimmers_memberships


def test_GroupBox_set_membership_SetsAttr_credor_pool_debtor_pool():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    ohio_str = ";Ohio"
    yao_ohio_membership = membership_shop(ohio_str)
    sue_ohio_membership = membership_shop(ohio_str)
    yao_ohio_membership._acct_id = yao_str
    yao_ohio_membership._acct_id = yao_str
    sue_ohio_membership._acct_id = sue_str
    yao_ohio_membership._credor_pool = 66
    sue_ohio_membership._credor_pool = 22
    yao_ohio_membership._debtor_pool = 6600
    sue_ohio_membership._debtor_pool = 2200
    ohio_groupbox = groupbox_shop(ohio_str)
    assert ohio_groupbox._credor_pool == 0
    assert ohio_groupbox._debtor_pool == 0

    # WHEN
    ohio_groupbox.set_membership(yao_ohio_membership)
    # THEN
    assert ohio_groupbox._credor_pool == 66
    assert ohio_groupbox._debtor_pool == 6600

    # WHEN
    ohio_groupbox.set_membership(sue_ohio_membership)
    # THEN
    assert ohio_groupbox._credor_pool == 88
    assert ohio_groupbox._debtor_pool == 8800


def test_GroupBox_set_membership_RaisesErrorIf_membership_group_id_IsWrong():
    # ESTABLISH
    yao_str = "Yao"
    ohio_str = ";Ohio"
    iowa_str = ";Iowa"
    yao_ohio_membership = membership_shop(ohio_str)
    yao_ohio_membership._acct_id = yao_str
    yao_ohio_membership._acct_id = yao_str
    yao_ohio_membership._credor_pool = 66
    yao_ohio_membership._debtor_pool = 6600
    iowa_groupbox = groupbox_shop(iowa_str)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        iowa_groupbox.set_membership(yao_ohio_membership)
    assert (
        str(excinfo.value)
        == f"GroupBox.group_id={iowa_str} cannot set membership.group_id={ohio_str}"
    )


def test_GroupBox_set_membership_RaisesErrorIf_acct_id_IsNone():
    # ESTABLISH
    ohio_str = ";Ohio"
    ohio_groupbox = groupbox_shop(ohio_str)
    yao_ohio_membership = membership_shop(ohio_str)
    assert yao_ohio_membership._acct_id is None

    with pytest_raises(Exception) as excinfo:
        ohio_groupbox.set_membership(yao_ohio_membership)
    assert (
        str(excinfo.value)
        == f"membership group_id={ohio_str} cannot be set when _acct_id is None."
    )
