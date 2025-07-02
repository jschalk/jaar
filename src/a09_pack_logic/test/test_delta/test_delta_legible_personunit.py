from src.a06_believer_logic.believer import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    believer_personunit_str,
    person_name_str,
)
from src.a08_believer_atom_logic.atom import believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import believerdelta_shop
from src.a09_pack_logic.legible import create_legible_list


def test_create_legible_list_ReturnsObj_personunit_INSERT():
    # ESTABLISH
    dimen = believer_personunit_str()
    person_cred_points_str = "person_cred_points"
    person_debt_points_str = "person_debt_points"
    person_cred_points_value = 81
    person_debt_points_value = 43
    yao_str = "Yao"
    yao_believeratom = believeratom_shop(dimen, INSERT_str())
    yao_believeratom.set_arg(person_name_str(), yao_str)
    yao_believeratom.set_arg(person_cred_points_str, person_cred_points_value)
    yao_believeratom.set_arg(person_debt_points_str, person_debt_points_value)
    # print(f"{yao_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(yao_believeratom)
    sue_believer = believerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"{yao_str} was added with {person_cred_points_value} score credit and {person_debt_points_value} score debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_personunit_INSERT_score():
    # ESTABLISH
    dimen = believer_personunit_str()
    person_cred_points_str = "person_cred_points"
    person_debt_points_str = "person_debt_points"
    person_cred_points_value = 81
    person_debt_points_value = 43
    yao_str = "Yao"
    yao_believeratom = believeratom_shop(dimen, INSERT_str())
    yao_believeratom.set_arg(person_name_str(), yao_str)
    yao_believeratom.set_arg(person_cred_points_str, person_cred_points_value)
    yao_believeratom.set_arg(person_debt_points_str, person_debt_points_value)
    # print(f"{yao_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(yao_believeratom)
    sue_believer = believerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"{yao_str} was added with {person_cred_points_value} score credit and {person_debt_points_value} score debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_personunit_UPDATE_person_cred_points_person_debt_points():
    # ESTABLISH
    dimen = believer_personunit_str()
    person_cred_points_str = "person_cred_points"
    person_debt_points_str = "person_debt_points"
    person_cred_points_value = 81
    person_debt_points_value = 43
    yao_str = "Yao"
    yao_believeratom = believeratom_shop(dimen, UPDATE_str())
    yao_believeratom.set_arg(person_name_str(), yao_str)
    yao_believeratom.set_arg(person_cred_points_str, person_cred_points_value)
    yao_believeratom.set_arg(person_debt_points_str, person_debt_points_value)
    # print(f"{yao_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(yao_believeratom)
    sue_believer = believerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"{yao_str} now has {person_cred_points_value} score credit and {person_debt_points_value} score debt."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_personunit_UPDATE_person_cred_points():
    # ESTABLISH
    dimen = believer_personunit_str()
    person_cred_points_str = "person_cred_points"
    person_cred_points_value = 81
    yao_str = "Yao"
    yao_believeratom = believeratom_shop(dimen, UPDATE_str())
    yao_believeratom.set_arg(person_name_str(), yao_str)
    yao_believeratom.set_arg(person_cred_points_str, person_cred_points_value)
    # print(f"{yao_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(yao_believeratom)
    sue_believer = believerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"{yao_str} now has {person_cred_points_value} score credit."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_personunit_UPDATE_person_debt_points():
    # ESTABLISH
    dimen = believer_personunit_str()
    person_debt_points_str = "person_debt_points"
    person_debt_points_value = 43
    yao_str = "Yao"
    yao_believeratom = believeratom_shop(dimen, UPDATE_str())
    yao_believeratom.set_arg(person_name_str(), yao_str)
    yao_believeratom.set_arg(person_debt_points_str, person_debt_points_value)
    # print(f"{yao_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(yao_believeratom)
    sue_believer = believerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"{yao_str} now has {person_debt_points_value} score debt."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_personunit_DELETE():
    # ESTABLISH
    dimen = believer_personunit_str()
    yao_str = "Yao"
    yao_believeratom = believeratom_shop(dimen, DELETE_str())
    yao_believeratom.set_arg(person_name_str(), yao_str)
    # print(f"{yao_believeratom=}")
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(yao_believeratom)
    sue_believer = believerunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_believerdelta, sue_believer)

    # THEN
    x_str = f"{yao_str} was removed from score persons."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
