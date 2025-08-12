from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises
from src.a03_group_logic.partner import partnerunit_shop
from src.a06_believer_logic.believer_main import believerunit_shop


def test_BelieverUnit_set_partnerunit_SetsAttr():
    # ESTABLISH
    yao_str = "Yao"
    yao_partnerunit = partnerunit_shop(yao_str)
    yao_partnerunit.add_membership(yao_str)
    deepcopy_yao_partnerunit = copy_deepcopy(yao_partnerunit)
    slash_str = "/"
    bob_believer = believerunit_shop("Bob", knot=slash_str)

    # WHEN
    bob_believer.set_partnerunit(yao_partnerunit)

    # THEN
    assert bob_believer.partners.get(yao_str).knot == slash_str
    x_partners = {yao_partnerunit.partner_name: deepcopy_yao_partnerunit}
    assert bob_believer.partners != x_partners
    deepcopy_yao_partnerunit.knot = bob_believer.knot
    assert bob_believer.partners == x_partners


def test_BelieverUnit_set_partner_DoesNotSet_partner_name_membership():
    # ESTABLISH
    x_respect_bit = 5
    yao_believer = believerunit_shop("Yao", respect_bit=x_respect_bit)
    zia_str = "Zia"

    # WHEN
    yao_believer.set_partnerunit(partnerunit_shop(zia_str), auto_set_membership=False)

    # THEN
    assert yao_believer.get_partner(zia_str).get_membership(zia_str) is None


def test_BelieverUnit_set_partner_DoesSet_partner_name_membership():
    # ESTABLISH
    x_respect_bit = 5
    yao_believer = believerunit_shop("Yao", respect_bit=x_respect_bit)
    zia_str = "Zia"

    # WHEN
    yao_believer.set_partnerunit(partnerunit_shop(zia_str))

    # THEN
    zia_zia_membership = yao_believer.get_partner(zia_str).get_membership(zia_str)
    assert zia_zia_membership is not None
    assert zia_zia_membership.group_cred_points == 1
    assert zia_zia_membership.group_debt_points == 1


def test_BelieverUnit_set_partner_DoesNotOverRide_partner_name_membership():
    # ESTABLISH
    x_respect_bit = 5
    yao_believer = believerunit_shop("Yao", respect_bit=x_respect_bit)
    zia_str = "Zia"
    ohio_str = ";Ohio"
    zia_ohio_credit_w = 33
    zia_ohio_debt_w = 44
    zia_partnerunit = partnerunit_shop(zia_str)
    zia_partnerunit.add_membership(ohio_str, zia_ohio_credit_w, zia_ohio_debt_w)

    # WHEN
    yao_believer.set_partnerunit(zia_partnerunit)

    # THEN
    zia_ohio_membership = yao_believer.get_partner(zia_str).get_membership(ohio_str)
    assert zia_ohio_membership is not None
    assert zia_ohio_membership.group_cred_points == zia_ohio_credit_w
    assert zia_ohio_membership.group_debt_points == zia_ohio_debt_w
    zia_zia_membership = yao_believer.get_partner(zia_str).get_membership(zia_str)
    assert zia_zia_membership is None


def test_BelieverUnit_add_partnerunit_Sets_partners():
    # ESTABLISH
    x_respect_bit = 6
    yao_believer = believerunit_shop("Yao", respect_bit=x_respect_bit)
    zia_str = "Zia"
    sue_str = "Sue"
    xio_str = "Xio"

    # WHEN
    yao_believer.add_partnerunit(zia_str, partner_cred_points=13, partner_debt_points=8)
    yao_believer.add_partnerunit(sue_str, partner_debt_points=5)
    yao_believer.add_partnerunit(xio_str, partner_cred_points=17)

    # THEN
    assert len(yao_believer.partners) == 3
    assert len(yao_believer.get_partnerunit_group_titles_dict()) == 3
    assert yao_believer.partners.get(xio_str).partner_cred_points == 17
    assert yao_believer.partners.get(sue_str).partner_debt_points == 5
    assert yao_believer.partners.get(xio_str).respect_bit == x_respect_bit


def test_BelieverUnit_partner_exists_ReturnsObj():
    # ESTABLISH
    bob_believer = believerunit_shop("Bob")
    yao_str = "Yao"

    # WHEN / THEN
    assert bob_believer.partner_exists(yao_str) is False

    # ESTABLISH
    bob_believer.add_partnerunit(yao_str)

    # WHEN / THEN
    assert bob_believer.partner_exists(yao_str)


def test_BelieverUnit_set_partner_Creates_membership():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    yao_believer = believerunit_shop("Yao")
    zia_str = "Zia"
    before_zia_credit = 7
    before_zia_debt = 17
    yao_believer.add_partnerunit(zia_str, before_zia_credit, before_zia_debt)
    zia_partnerunit = yao_believer.get_partner(zia_str)
    zia_membership = zia_partnerunit.get_membership(zia_str)
    assert zia_membership.group_cred_points != before_zia_credit
    assert zia_membership.group_debt_points != before_zia_debt
    assert zia_membership.group_cred_points == 1
    assert zia_membership.group_debt_points == 1

    # WHEN
    after_zia_credit = 11
    after_zia_debt = 13
    yao_believer.set_partnerunit(
        partnerunit_shop(zia_str, after_zia_credit, after_zia_debt)
    )

    # THEN
    assert zia_membership.group_cred_points != after_zia_credit
    assert zia_membership.group_debt_points != after_zia_debt
    assert zia_membership.group_cred_points == 1
    assert zia_membership.group_debt_points == 1


def test_BelieverUnit_edit_partner_RaiseExceptionWhenPartnerDoesNotExist():
    # ESTABLISH
    yao_believer = believerunit_shop("Yao")
    zia_str = "Zia"
    zia_partner_cred_points = 55

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_believer.edit_partnerunit(
            zia_str, partner_cred_points=zia_partner_cred_points
        )
    assert str(excinfo.value) == f"PartnerUnit '{zia_str}' does not exist."


def test_BelieverUnit_edit_partner_UpdatesObj():
    # ESTABLISH
    yao_believer = believerunit_shop("Yao")
    zia_str = "Zia"
    old_zia_partner_cred_points = 55
    old_zia_partner_debt_points = 66
    yao_believer.set_partnerunit(
        partnerunit_shop(
            zia_str,
            old_zia_partner_cred_points,
            old_zia_partner_debt_points,
        )
    )
    zia_partnerunit = yao_believer.get_partner(zia_str)
    assert zia_partnerunit.partner_cred_points == old_zia_partner_cred_points
    assert zia_partnerunit.partner_debt_points == old_zia_partner_debt_points

    # WHEN
    new_zia_partner_cred_points = 22
    new_zia_partner_debt_points = 33
    yao_believer.edit_partnerunit(
        partner_name=zia_str,
        partner_cred_points=new_zia_partner_cred_points,
        partner_debt_points=new_zia_partner_debt_points,
    )

    # THEN
    assert zia_partnerunit.partner_cred_points == new_zia_partner_cred_points
    assert zia_partnerunit.partner_debt_points == new_zia_partner_debt_points


def test_BelieverUnit_get_partner_ReturnsObj():
    # ESTABLISH
    yao_believer = believerunit_shop("Yao")
    zia_str = "Zia"
    sue_str = "Sue"
    yao_believer.add_partnerunit(zia_str)
    yao_believer.add_partnerunit(sue_str)

    # WHEN
    zia_partner = yao_believer.get_partner(zia_str)
    sue_partner = yao_believer.get_partner(sue_str)

    # THEN
    assert zia_partner == yao_believer.partners.get(zia_str)
    assert sue_partner == yao_believer.partners.get(sue_str)
