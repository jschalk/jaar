from src.a02_finance_logic.finance_config import (
    default_respect_num,
    validate_respect_num,
)
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic.plan import planunit_shop
from src.a12_hub_toolbox.basis_plans import (
    create_empty_plan_from_plan,
    create_listen_basis,
    get_default_job,
)


def test_create_empty_plan_from_plan_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    slash_str = "/"
    penny_float = 0.7
    yao_gut = planunit_shop(yao_str, knot=slash_str, penny=penny_float)
    yao_gut.set_l1_concept(conceptunit_shop("Iowa"))
    zia_str = "Zia"
    zia_credit_score = 47
    zia_debt_score = 41
    zia_credor_pool = 87
    zia_debtor_pool = 81
    yao_gut.add_acctunit(zia_str, zia_credit_score, zia_debt_score)
    zia_irrational_debt_score = 11
    zia_inallocable_debt_score = 22
    duty_zia_acctunit = yao_gut.get_acct(zia_str)
    duty_zia_acctunit.add_irrational_debt_score(zia_irrational_debt_score)
    duty_zia_acctunit.add_inallocable_debt_score(zia_inallocable_debt_score)
    zia_acctunit = yao_gut.get_acct(zia_str)
    zia_acctunit.add_membership(f"{slash_str}swimmers")
    yao_gut.set_credor_respect(zia_credor_pool)
    yao_gut.set_debtor_respect(zia_debtor_pool)

    # WHEN
    yao_empty_vision = create_empty_plan_from_plan(yao_gut, x_owner_name=zia_str)

    # THEN
    assert yao_empty_vision.owner_name != yao_gut.owner_name
    assert yao_empty_vision.owner_name == zia_str
    assert yao_empty_vision.vow_label == yao_gut.vow_label
    assert yao_empty_vision.last_pack_id is None
    assert yao_empty_vision.get_acctunits_dict() == {}
    assert yao_empty_vision.knot == yao_gut.knot
    assert yao_empty_vision.fund_pool == yao_gut.fund_pool
    assert yao_empty_vision.fund_iota == yao_gut.fund_iota
    assert yao_empty_vision.respect_bit == yao_gut.respect_bit
    assert yao_empty_vision.penny == yao_gut.penny
    assert yao_empty_vision.credor_respect != yao_gut.credor_respect
    assert yao_empty_vision.credor_respect == validate_respect_num()
    assert yao_empty_vision.debtor_respect != yao_gut.debtor_respect
    assert yao_empty_vision.debtor_respect == validate_respect_num()
    yao_empty_vision.settle_plan()
    assert yao_empty_vision.accts == {}


def test_create_listen_basis_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    slash_str = "/"
    yao_duty = planunit_shop(yao_str, knot=slash_str)
    yao_duty.set_l1_concept(conceptunit_shop("Iowa"))
    zia_str = "Zia"
    zia_credit_score = 47
    zia_debt_score = 41
    zia_credor_pool = 8700
    zia_debtor_pool = 8100
    yao_duty.add_acctunit(zia_str, zia_credit_score, zia_debt_score)
    zia_irrational_debt_score = 11
    zia_inallocable_debt_score = 22
    duty_zia_acctunit = yao_duty.get_acct(zia_str)
    duty_zia_acctunit.add_irrational_debt_score(zia_irrational_debt_score)
    duty_zia_acctunit.add_inallocable_debt_score(zia_inallocable_debt_score)
    zia_acctunit = yao_duty.get_acct(zia_str)
    zia_acctunit.add_membership(f"{slash_str}swimmers")
    yao_duty.set_credor_respect(zia_credor_pool)
    yao_duty.set_debtor_respect(zia_debtor_pool)

    # WHEN
    yao_basis_vision = create_listen_basis(yao_duty)

    # THEN
    assert yao_basis_vision.owner_name == yao_duty.owner_name
    assert yao_basis_vision.vow_label == yao_duty.vow_label
    assert yao_basis_vision.last_pack_id == yao_duty.last_pack_id
    assert yao_basis_vision.get_acctunits_dict() == yao_duty.get_acctunits_dict()
    assert yao_basis_vision.knot == yao_duty.knot
    assert yao_basis_vision.fund_pool == yao_duty.fund_pool
    assert yao_basis_vision.fund_iota == yao_duty.fund_iota
    assert yao_basis_vision.respect_bit == yao_duty.respect_bit
    assert yao_basis_vision.credor_respect == yao_duty.credor_respect
    assert yao_basis_vision.debtor_respect == yao_duty.debtor_respect
    yao_basis_vision.settle_plan()
    assert len(yao_basis_vision._concept_dict) != len(yao_duty._concept_dict)
    assert len(yao_basis_vision._concept_dict) == 1
    vision_zia_acctunit = yao_basis_vision.get_acct(zia_str)
    assert (
        yao_basis_vision.get_acctunits_dict().keys()
        == yao_duty.get_acctunits_dict().keys()
    )
    assert vision_zia_acctunit._irrational_debt_score == 0
    assert vision_zia_acctunit._inallocable_debt_score == 0


def test_get_default_job_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    blue_str = "blue"
    slash_str = "/"
    x_fund_pool = 99000
    x_fund_iota = 80
    x_respect_bit = 5
    sue_acct_pool = 800
    casa_str = "casa"
    bob_str = "Bob"
    last_pack_id = 7
    sue_max_tree_traverse = 9
    sue_planunit = planunit_shop(
        sue_str, blue_str, slash_str, x_fund_pool, x_fund_iota, x_respect_bit
    )
    sue_planunit.set_last_pack_id(last_pack_id)
    sue_planunit.add_acctunit(bob_str, 3, 4)
    bob_acctunit = sue_planunit.get_acct(bob_str)
    bob_acctunit.add_membership(f"{slash_str}swimmers")
    sue_planunit.set_acct_respect(sue_acct_pool)
    sue_planunit.set_l1_concept(conceptunit_shop(casa_str))
    sue_planunit.set_max_tree_traverse(sue_max_tree_traverse)

    # WHEN
    default_job = get_default_job(sue_planunit)

    # THEN
    default_job.settle_plan()
    assert default_job.owner_name == sue_planunit.owner_name
    assert default_job.owner_name == sue_str
    assert default_job.vow_label == sue_planunit.vow_label
    assert default_job.vow_label == blue_str
    assert default_job.knot == slash_str
    assert default_job.fund_pool == sue_acct_pool
    assert default_job.fund_iota == x_fund_iota
    assert default_job.respect_bit == x_respect_bit
    assert default_job.credor_respect == default_respect_num()
    assert default_job.debtor_respect == default_respect_num()
    assert default_job.max_tree_traverse == sue_max_tree_traverse
    assert len(default_job.get_acctunits_dict()) == 1
    assert len(default_job._concept_dict) == 1
