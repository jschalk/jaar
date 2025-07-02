from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.a06_str import acct_name_str, owner_acctunit_str
from src.a08_owner_atom_logic.atom import owneratom_shop
from src.a08_owner_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import ownerdelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_acctunit_INSERT():
    # ESTABLISH
    dimen = owner_acctunit_str()
    acct_cred_points_str = "acct_cred_points"
    acct_debt_points_str = "acct_debt_points"
    acct_cred_points_value = 81
    acct_debt_points_value = 43
    yao_str = "Yao"
    yao_owneratom = owneratom_shop(dimen, INSERT_str())
    yao_owneratom.set_arg(acct_name_str(), yao_str)
    yao_owneratom.set_arg(acct_cred_points_str, acct_cred_points_value)
    yao_owneratom.set_arg(acct_debt_points_str, acct_debt_points_value)
    # print(f"{yao_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(yao_owneratom)
    sue_owner = ownerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"{yao_str} was added with {acct_cred_points_value} score credit and {acct_debt_points_value} score debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_INSERT_score():
    # ESTABLISH
    dimen = owner_acctunit_str()
    acct_cred_points_str = "acct_cred_points"
    acct_debt_points_str = "acct_debt_points"
    acct_cred_points_value = 81
    acct_debt_points_value = 43
    yao_str = "Yao"
    yao_owneratom = owneratom_shop(dimen, INSERT_str())
    yao_owneratom.set_arg(acct_name_str(), yao_str)
    yao_owneratom.set_arg(acct_cred_points_str, acct_cred_points_value)
    yao_owneratom.set_arg(acct_debt_points_str, acct_debt_points_value)
    # print(f"{yao_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(yao_owneratom)
    sue_owner = ownerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"{yao_str} was added with {acct_cred_points_value} score credit and {acct_debt_points_value} score debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_UPDATE_acct_cred_points_acct_debt_points():
    # ESTABLISH
    dimen = owner_acctunit_str()
    acct_cred_points_str = "acct_cred_points"
    acct_debt_points_str = "acct_debt_points"
    acct_cred_points_value = 81
    acct_debt_points_value = 43
    yao_str = "Yao"
    yao_owneratom = owneratom_shop(dimen, UPDATE_str())
    yao_owneratom.set_arg(acct_name_str(), yao_str)
    yao_owneratom.set_arg(acct_cred_points_str, acct_cred_points_value)
    yao_owneratom.set_arg(acct_debt_points_str, acct_debt_points_value)
    # print(f"{yao_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(yao_owneratom)
    sue_owner = ownerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"{yao_str} now has {acct_cred_points_value} score credit and {acct_debt_points_value} score debt."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_UPDATE_acct_cred_points():
    # ESTABLISH
    dimen = owner_acctunit_str()
    acct_cred_points_str = "acct_cred_points"
    acct_cred_points_value = 81
    yao_str = "Yao"
    yao_owneratom = owneratom_shop(dimen, UPDATE_str())
    yao_owneratom.set_arg(acct_name_str(), yao_str)
    yao_owneratom.set_arg(acct_cred_points_str, acct_cred_points_value)
    # print(f"{yao_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(yao_owneratom)
    sue_owner = ownerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"{yao_str} now has {acct_cred_points_value} score credit."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_UPDATE_acct_debt_points():
    # ESTABLISH
    dimen = owner_acctunit_str()
    acct_debt_points_str = "acct_debt_points"
    acct_debt_points_value = 43
    yao_str = "Yao"
    yao_owneratom = owneratom_shop(dimen, UPDATE_str())
    yao_owneratom.set_arg(acct_name_str(), yao_str)
    yao_owneratom.set_arg(acct_debt_points_str, acct_debt_points_value)
    # print(f"{yao_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(yao_owneratom)
    sue_owner = ownerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"{yao_str} now has {acct_debt_points_value} score debt."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_acctunit_DELETE():
    # ESTABLISH
    dimen = owner_acctunit_str()
    yao_str = "Yao"
    yao_owneratom = owneratom_shop(dimen, DELETE_str())
    yao_owneratom.set_arg(acct_name_str(), yao_str)
    # print(f"{yao_owneratom=}")
    x_ownerdelta = ownerdelta_shop()
    x_ownerdelta.set_owneratom(yao_owneratom)
    sue_owner = ownerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_ownerdelta, sue_owner)

    # THEN
    x_str = f"{yao_str} was removed from score accts."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
