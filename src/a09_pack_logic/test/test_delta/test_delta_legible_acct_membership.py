from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.a06_str import (
    acct_name_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    owner_acct_membership_str,
)
from src.a08_owner_atom_logic.atom import owneratom_shop
from src.a08_owner_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import ownerdelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_acct_membership_INSERT():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_acct_membership_str()
    swim_str = f"{sue_owner.knot}Swimmers"
    yao_str = "Yao"
    group_cred_points_value = 81
    group_debt_points_value = 43
    yao_owneratom = owneratom_shop(dimen, INSERT_str())
    yao_owneratom.set_arg(group_title_str(), swim_str)
    yao_owneratom.set_arg(acct_name_str(), yao_str)
    yao_owneratom.set_arg(group_cred_points_str(), group_cred_points_value)
    yao_owneratom.set_arg(group_debt_points_str(), group_debt_points_value)
    # print(f"{yao_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(yao_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"Group '{swim_str}' has new membership {yao_str} with group_cred_points_value{group_cred_points_value} and group_debt_points_value={group_debt_points_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_UPDATE_group_cred_points_group_debt_points():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_acct_membership_str()
    group_cred_points_str = "group_cred_points"
    group_debt_points_str = "group_debt_points"
    swim_str = f"{sue_owner.knot}Swimmers"
    yao_str = "Yao"
    group_cred_points_value = 81
    group_debt_points_value = 43
    yao_owneratom = owneratom_shop(dimen, UPDATE_str())
    yao_owneratom.set_arg(group_title_str(), swim_str)
    yao_owneratom.set_arg(acct_name_str(), yao_str)
    yao_owneratom.set_arg(group_cred_points_str, group_cred_points_value)
    yao_owneratom.set_arg(group_debt_points_str, group_debt_points_value)
    # print(f"{yao_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(yao_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"Group '{swim_str}' membership {yao_str} has new group_cred_points_value{group_cred_points_value} and group_debt_points_value={group_debt_points_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_UPDATE_group_cred_points():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_acct_membership_str()
    group_cred_points_str = "group_cred_points"
    swim_str = f"{sue_owner.knot}Swimmers"
    yao_str = "Yao"
    group_cred_points_value = 81
    yao_owneratom = owneratom_shop(dimen, UPDATE_str())
    yao_owneratom.set_arg(group_title_str(), swim_str)
    yao_owneratom.set_arg(acct_name_str(), yao_str)
    yao_owneratom.set_arg(group_cred_points_str, group_cred_points_value)
    # print(f"{yao_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(yao_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"Group '{swim_str}' membership {yao_str} has new group_cred_points_value{group_cred_points_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_UPDATE_group_debt_points():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_acct_membership_str()
    group_debt_points_str = "group_debt_points"
    swim_str = f"{sue_owner.knot}Swimmers"
    yao_str = "Yao"
    group_debt_points_value = 43
    yao_owneratom = owneratom_shop(dimen, UPDATE_str())
    yao_owneratom.set_arg(group_title_str(), swim_str)
    yao_owneratom.set_arg(acct_name_str(), yao_str)
    yao_owneratom.set_arg(group_debt_points_str, group_debt_points_value)
    # print(f"{yao_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(yao_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"Group '{swim_str}' membership {yao_str} has new group_debt_points_value={group_debt_points_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acct_membership_DELETE():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    dimen = owner_acct_membership_str()
    swim_str = f"{sue_owner.knot}Swimmers"
    yao_str = "Yao"
    yao_owneratom = owneratom_shop(dimen, DELETE_str())
    yao_owneratom.set_arg(group_title_str(), swim_str)
    yao_owneratom.set_arg(acct_name_str(), yao_str)
    # print(f"{yao_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(yao_owneratom)

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"Group '{swim_str}' no longer has membership {yao_str}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
