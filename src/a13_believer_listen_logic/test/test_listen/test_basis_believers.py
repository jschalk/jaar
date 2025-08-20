from src.a02_finance_logic.finance_config import (
    default_respect_num,
    validate_respect_num,
)
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a13_believer_listen_logic.basis_believers import (
    create_empty_believer_from_believer,
    create_listen_basis,
    get_default_job,
)


def test_create_empty_believer_from_believer_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    slash_str = "/"
    penny_float = 0.7
    yao_gut = believerunit_shop(yao_str, knot=slash_str, penny=penny_float)
    yao_gut.set_l1_plan(planunit_shop("Iowa"))
    zia_str = "Zia"
    zia_partner_cred_points = 47
    zia_partner_debt_points = 41
    zia_credor_pool = 87
    zia_debtor_pool = 81
    yao_gut.add_partnerunit(zia_str, zia_partner_cred_points, zia_partner_debt_points)
    zia_irrational_partner_debt_points = 11
    zia_inallocable_partner_debt_points = 22
    duty_zia_partnerunit = yao_gut.get_partner(zia_str)
    duty_zia_partnerunit.add_irrational_partner_debt_points(
        zia_irrational_partner_debt_points
    )
    duty_zia_partnerunit.add_inallocable_partner_debt_points(
        zia_inallocable_partner_debt_points
    )
    zia_partnerunit = yao_gut.get_partner(zia_str)
    zia_partnerunit.add_membership(f"{slash_str}swimmers")
    yao_gut.set_credor_respect(zia_credor_pool)
    yao_gut.set_debtor_respect(zia_debtor_pool)

    # WHEN
    yao_empty_vision = create_empty_believer_from_believer(
        yao_gut, x_believer_name=zia_str
    )

    # THEN
    assert yao_empty_vision.believer_name != yao_gut.believer_name
    assert yao_empty_vision.believer_name == zia_str
    assert yao_empty_vision.coin_label == yao_gut.coin_label
    assert yao_empty_vision.last_pack_id is None
    assert yao_empty_vision.get_partnerunits_dict() == {}
    assert yao_empty_vision.knot == yao_gut.knot
    assert yao_empty_vision.fund_pool == yao_gut.fund_pool
    assert yao_empty_vision.fund_iota == yao_gut.fund_iota
    assert yao_empty_vision.respect_bit == yao_gut.respect_bit
    assert yao_empty_vision.penny == yao_gut.penny
    assert yao_empty_vision.credor_respect != yao_gut.credor_respect
    assert yao_empty_vision.credor_respect == validate_respect_num()
    assert yao_empty_vision.debtor_respect != yao_gut.debtor_respect
    assert yao_empty_vision.debtor_respect == validate_respect_num()
    yao_empty_vision.settle_believer()
    assert yao_empty_vision.partners == {}


def test_create_listen_basis_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    slash_str = "/"
    yao_duty = believerunit_shop(yao_str, knot=slash_str)
    yao_duty.set_l1_plan(planunit_shop("Iowa"))
    zia_str = "Zia"
    zia_partner_cred_points = 47
    zia_partner_debt_points = 41
    zia_credor_pool = 8700
    zia_debtor_pool = 8100
    yao_duty.add_partnerunit(zia_str, zia_partner_cred_points, zia_partner_debt_points)
    zia_irrational_partner_debt_points = 11
    zia_inallocable_partner_debt_points = 22
    duty_zia_partnerunit = yao_duty.get_partner(zia_str)
    duty_zia_partnerunit.add_irrational_partner_debt_points(
        zia_irrational_partner_debt_points
    )
    duty_zia_partnerunit.add_inallocable_partner_debt_points(
        zia_inallocable_partner_debt_points
    )
    zia_partnerunit = yao_duty.get_partner(zia_str)
    zia_partnerunit.add_membership(f"{slash_str}swimmers")
    yao_duty.set_credor_respect(zia_credor_pool)
    yao_duty.set_debtor_respect(zia_debtor_pool)

    # WHEN
    yao_basis_vision = create_listen_basis(yao_duty)

    # THEN
    assert yao_basis_vision.believer_name == yao_duty.believer_name
    assert yao_basis_vision.coin_label == yao_duty.coin_label
    assert yao_basis_vision.last_pack_id == yao_duty.last_pack_id
    assert yao_basis_vision.get_partnerunits_dict() == yao_duty.get_partnerunits_dict()
    assert yao_basis_vision.knot == yao_duty.knot
    assert yao_basis_vision.fund_pool == yao_duty.fund_pool
    assert yao_basis_vision.fund_iota == yao_duty.fund_iota
    assert yao_basis_vision.respect_bit == yao_duty.respect_bit
    assert yao_basis_vision.credor_respect == yao_duty.credor_respect
    assert yao_basis_vision.debtor_respect == yao_duty.debtor_respect
    yao_basis_vision.settle_believer()
    assert len(yao_basis_vision._plan_dict) != len(yao_duty._plan_dict)
    assert len(yao_basis_vision._plan_dict) == 1
    vision_zia_partnerunit = yao_basis_vision.get_partner(zia_str)
    assert (
        yao_basis_vision.get_partnerunits_dict().keys()
        == yao_duty.get_partnerunits_dict().keys()
    )
    assert vision_zia_partnerunit._irrational_partner_debt_points == 0
    assert vision_zia_partnerunit._inallocable_partner_debt_points == 0


def test_get_default_job_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    blue_str = "blue"
    slash_str = "/"
    x_fund_pool = 99000
    x_fund_iota = 80
    x_respect_bit = 5
    sue_partner_pool = 800
    casa_str = "casa"
    bob_str = "Bob"
    last_pack_id = 7
    sue_max_tree_traverse = 9
    sue_believerunit = believerunit_shop(
        sue_str, blue_str, slash_str, x_fund_pool, x_fund_iota, x_respect_bit
    )
    sue_believerunit.set_last_pack_id(last_pack_id)
    sue_believerunit.add_partnerunit(bob_str, 3, 4)
    bob_partnerunit = sue_believerunit.get_partner(bob_str)
    bob_partnerunit.add_membership(f"{slash_str}swimmers")
    sue_believerunit.set_partner_respect(sue_partner_pool)
    sue_believerunit.set_l1_plan(planunit_shop(casa_str))
    sue_believerunit.set_max_tree_traverse(sue_max_tree_traverse)

    # WHEN
    default_job = get_default_job(sue_believerunit)

    # THEN
    default_job.settle_believer()
    assert default_job.believer_name == sue_believerunit.believer_name
    assert default_job.believer_name == sue_str
    assert default_job.coin_label == sue_believerunit.coin_label
    assert default_job.coin_label == blue_str
    assert default_job.knot == slash_str
    assert default_job.fund_pool == sue_partner_pool
    assert default_job.fund_iota == x_fund_iota
    assert default_job.respect_bit == x_respect_bit
    assert default_job.credor_respect == default_respect_num()
    assert default_job.debtor_respect == default_respect_num()
    assert default_job.max_tree_traverse == sue_max_tree_traverse
    assert len(default_job.get_partnerunits_dict()) == 1
    assert len(default_job._plan_dict) == 1
