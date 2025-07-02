from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises
from src.a03_group_logic.person import personunit_shop
from src.a06_believer_logic.believer import believerunit_shop


def test_BelieverUnit_set_personunit_SetObjCorrectly():
    # ESTABLISH
    yao_str = "Yao"
    yao_personunit = personunit_shop(yao_str)
    yao_personunit.add_membership(yao_str)
    deepcopy_yao_personunit = copy_deepcopy(yao_personunit)
    slash_str = "/"
    bob_believer = believerunit_shop("Bob", knot=slash_str)

    # WHEN
    bob_believer.set_personunit(yao_personunit)

    # THEN
    assert bob_believer.persons.get(yao_str).knot == slash_str
    x_persons = {yao_personunit.person_name: deepcopy_yao_personunit}
    assert bob_believer.persons != x_persons
    deepcopy_yao_personunit.knot = bob_believer.knot
    assert bob_believer.persons == x_persons


def test_BelieverUnit_set_person_DoesNotSet_person_name_membership():
    # ESTABLISH
    x_respect_bit = 5
    yao_believer = believerunit_shop("Yao", respect_bit=x_respect_bit)
    zia_str = "Zia"

    # WHEN
    yao_believer.set_personunit(personunit_shop(zia_str), auto_set_membership=False)

    # THEN
    assert yao_believer.get_person(zia_str).get_membership(zia_str) is None


def test_BelieverUnit_set_person_DoesSet_person_name_membership():
    # ESTABLISH
    x_respect_bit = 5
    yao_believer = believerunit_shop("Yao", respect_bit=x_respect_bit)
    zia_str = "Zia"

    # WHEN
    yao_believer.set_personunit(personunit_shop(zia_str))

    # THEN
    zia_zia_membership = yao_believer.get_person(zia_str).get_membership(zia_str)
    assert zia_zia_membership is not None
    assert zia_zia_membership.group_cred_points == 1
    assert zia_zia_membership.group_debt_points == 1


def test_BelieverUnit_set_person_DoesNotOverRide_person_name_membership():
    # ESTABLISH
    x_respect_bit = 5
    yao_believer = believerunit_shop("Yao", respect_bit=x_respect_bit)
    zia_str = "Zia"
    ohio_str = ";Ohio"
    zia_ohio_credit_w = 33
    zia_ohio_debt_w = 44
    zia_personunit = personunit_shop(zia_str)
    zia_personunit.add_membership(ohio_str, zia_ohio_credit_w, zia_ohio_debt_w)

    # WHEN
    yao_believer.set_personunit(zia_personunit)

    # THEN
    zia_ohio_membership = yao_believer.get_person(zia_str).get_membership(ohio_str)
    assert zia_ohio_membership is not None
    assert zia_ohio_membership.group_cred_points == zia_ohio_credit_w
    assert zia_ohio_membership.group_debt_points == zia_ohio_debt_w
    zia_zia_membership = yao_believer.get_person(zia_str).get_membership(zia_str)
    assert zia_zia_membership is None


def test_BelieverUnit_add_personunit_CorrectlySets_persons():
    # ESTABLISH
    x_respect_bit = 6
    yao_believer = believerunit_shop("Yao", respect_bit=x_respect_bit)
    zia_str = "Zia"
    sue_str = "Sue"
    xio_str = "Xio"

    # WHEN
    yao_believer.add_personunit(zia_str, person_cred_points=13, person_debt_points=8)
    yao_believer.add_personunit(sue_str, person_debt_points=5)
    yao_believer.add_personunit(xio_str, person_cred_points=17)

    # THEN
    assert len(yao_believer.persons) == 3
    assert len(yao_believer.get_personunit_group_titles_dict()) == 3
    assert yao_believer.persons.get(xio_str).person_cred_points == 17
    assert yao_believer.persons.get(sue_str).person_debt_points == 5
    assert yao_believer.persons.get(xio_str).respect_bit == x_respect_bit


def test_BelieverUnit_person_exists_ReturnsObj():
    # ESTABLISH
    bob_believer = believerunit_shop("Bob")
    yao_str = "Yao"

    # WHEN / THEN
    assert bob_believer.person_exists(yao_str) is False

    # ESTABLISH
    bob_believer.add_personunit(yao_str)

    # WHEN / THEN
    assert bob_believer.person_exists(yao_str)


def test_BelieverUnit_set_person_Creates_membership():
    # ESTABLISH
    yao_believer = believerunit_shop("Yao")
    zia_str = "Zia"
    before_zia_credit = 7
    before_zia_debt = 17
    yao_believer.add_personunit(zia_str, before_zia_credit, before_zia_debt)
    zia_personunit = yao_believer.get_person(zia_str)
    zia_membership = zia_personunit.get_membership(zia_str)
    assert zia_membership.group_cred_points != before_zia_credit
    assert zia_membership.group_debt_points != before_zia_debt
    assert zia_membership.group_cred_points == 1
    assert zia_membership.group_debt_points == 1

    # WHEN
    after_zia_credit = 11
    after_zia_debt = 13
    yao_believer.set_personunit(
        personunit_shop(zia_str, after_zia_credit, after_zia_debt)
    )

    # THEN
    assert zia_membership.group_cred_points != after_zia_credit
    assert zia_membership.group_debt_points != after_zia_debt
    assert zia_membership.group_cred_points == 1
    assert zia_membership.group_debt_points == 1


def test_BelieverUnit_edit_person_RaiseExceptionWhenPersonDoesNotExist():
    # ESTABLISH
    yao_believer = believerunit_shop("Yao")
    zia_str = "Zia"
    zia_person_cred_points = 55

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_believer.edit_personunit(zia_str, person_cred_points=zia_person_cred_points)
    assert str(excinfo.value) == f"PersonUnit '{zia_str}' does not exist."


def test_BelieverUnit_edit_person_CorrectlyUpdatesObj():
    # ESTABLISH
    yao_believer = believerunit_shop("Yao")
    zia_str = "Zia"
    old_zia_person_cred_points = 55
    old_zia_person_debt_points = 66
    yao_believer.set_personunit(
        personunit_shop(
            zia_str,
            old_zia_person_cred_points,
            old_zia_person_debt_points,
        )
    )
    zia_personunit = yao_believer.get_person(zia_str)
    assert zia_personunit.person_cred_points == old_zia_person_cred_points
    assert zia_personunit.person_debt_points == old_zia_person_debt_points

    # WHEN
    new_zia_person_cred_points = 22
    new_zia_person_debt_points = 33
    yao_believer.edit_personunit(
        person_name=zia_str,
        person_cred_points=new_zia_person_cred_points,
        person_debt_points=new_zia_person_debt_points,
    )

    # THEN
    assert zia_personunit.person_cred_points == new_zia_person_cred_points
    assert zia_personunit.person_debt_points == new_zia_person_debt_points


def test_BelieverUnit_get_person_ReturnsObj():
    # ESTABLISH
    yao_believer = believerunit_shop("Yao")
    zia_str = "Zia"
    sue_str = "Sue"
    yao_believer.add_personunit(zia_str)
    yao_believer.add_personunit(sue_str)

    # WHEN
    zia_person = yao_believer.get_person(zia_str)
    sue_person = yao_believer.get_person(sue_str)

    # THEN
    assert zia_person == yao_believer.persons.get(zia_str)
    assert sue_person == yao_believer.persons.get(sue_str)
