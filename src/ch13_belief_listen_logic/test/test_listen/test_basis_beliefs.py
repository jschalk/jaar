from src.ch03_allot_toolbox.allot import default_pool_num, validate_pool_num
from src.ch04_voice_logic.voice import RespectNum
from src.ch06_plan_logic.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch13_belief_listen_logic.basis_beliefs import (
    create_empty_belief_from_belief,
    create_listen_basis,
    get_default_job,
)


def test_create_empty_belief_from_belief_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    slash_str = "/"
    money_grain_float = 0.7
    yao_gut = beliefunit_shop(yao_str, knot=slash_str, money_grain=money_grain_float)
    yao_gut.set_l1_plan(planunit_shop("Iowa"))
    zia_str = "Zia"
    zia_voice_cred_points = 47
    zia_voice_debt_points = 41
    zia_credor_pool = 87
    zia_debtor_pool = 81
    yao_gut.add_voiceunit(zia_str, zia_voice_cred_points, zia_voice_debt_points)
    zia_irrational_voice_debt_points = 11
    zia_inallocable_voice_debt_points = 22
    duty_zia_voiceunit = yao_gut.get_voice(zia_str)
    duty_zia_voiceunit.add_irrational_voice_debt_points(
        zia_irrational_voice_debt_points
    )
    duty_zia_voiceunit.add_inallocable_voice_debt_points(
        zia_inallocable_voice_debt_points
    )
    zia_voiceunit = yao_gut.get_voice(zia_str)
    zia_voiceunit.add_membership(f"{slash_str}swimmers")
    yao_gut.set_credor_respect(zia_credor_pool)
    yao_gut.set_debtor_respect(zia_debtor_pool)

    # WHEN
    yao_empty_vision = create_empty_belief_from_belief(yao_gut, x_belief_name=zia_str)

    # THEN
    assert yao_empty_vision.belief_name != yao_gut.belief_name
    assert yao_empty_vision.belief_name == zia_str
    assert yao_empty_vision.moment_label == yao_gut.moment_label
    assert yao_empty_vision.last_pack_id is None
    assert yao_empty_vision.get_voiceunits_dict() == {}
    assert yao_empty_vision.knot == yao_gut.knot
    assert yao_empty_vision.fund_pool == yao_gut.fund_pool
    assert yao_empty_vision.fund_grain == yao_gut.fund_grain
    assert yao_empty_vision.respect_grain == yao_gut.respect_grain
    assert yao_empty_vision.money_grain == yao_gut.money_grain
    assert yao_empty_vision.credor_respect != yao_gut.credor_respect
    assert yao_empty_vision.credor_respect == RespectNum(validate_pool_num())
    assert yao_empty_vision.debtor_respect != yao_gut.debtor_respect
    assert yao_empty_vision.debtor_respect == RespectNum(validate_pool_num())
    yao_empty_vision.cashout()
    assert yao_empty_vision.voices == {}


def test_create_listen_basis_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    slash_str = "/"
    yao_duty = beliefunit_shop(yao_str, knot=slash_str)
    yao_duty.set_l1_plan(planunit_shop("Iowa"))
    zia_str = "Zia"
    zia_voice_cred_points = 47
    zia_voice_debt_points = 41
    zia_credor_pool = 8700
    zia_debtor_pool = 8100
    yao_duty.add_voiceunit(zia_str, zia_voice_cred_points, zia_voice_debt_points)
    zia_irrational_voice_debt_points = 11
    zia_inallocable_voice_debt_points = 22
    duty_zia_voiceunit = yao_duty.get_voice(zia_str)
    duty_zia_voiceunit.add_irrational_voice_debt_points(
        zia_irrational_voice_debt_points
    )
    duty_zia_voiceunit.add_inallocable_voice_debt_points(
        zia_inallocable_voice_debt_points
    )
    zia_voiceunit = yao_duty.get_voice(zia_str)
    zia_voiceunit.add_membership(f"{slash_str}swimmers")
    yao_duty.set_credor_respect(zia_credor_pool)
    yao_duty.set_debtor_respect(zia_debtor_pool)

    # WHEN
    yao_basis_vision = create_listen_basis(yao_duty)

    # THEN
    assert yao_basis_vision.belief_name == yao_duty.belief_name
    assert yao_basis_vision.moment_label == yao_duty.moment_label
    assert yao_basis_vision.last_pack_id == yao_duty.last_pack_id
    assert yao_basis_vision.get_voiceunits_dict() == yao_duty.get_voiceunits_dict()
    assert yao_basis_vision.knot == yao_duty.knot
    assert yao_basis_vision.fund_pool == yao_duty.fund_pool
    assert yao_basis_vision.fund_grain == yao_duty.fund_grain
    assert yao_basis_vision.respect_grain == yao_duty.respect_grain
    assert yao_basis_vision.credor_respect == yao_duty.credor_respect
    assert yao_basis_vision.debtor_respect == yao_duty.debtor_respect
    yao_basis_vision.cashout()
    assert len(yao_basis_vision._plan_dict) != len(yao_duty._plan_dict)
    assert len(yao_basis_vision._plan_dict) == 1
    vision_zia_voiceunit = yao_basis_vision.get_voice(zia_str)
    assert (
        yao_basis_vision.get_voiceunits_dict().keys()
        == yao_duty.get_voiceunits_dict().keys()
    )
    assert vision_zia_voiceunit.irrational_voice_debt_points == 0
    assert vision_zia_voiceunit.inallocable_voice_debt_points == 0


def test_get_default_job_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    blue_str = "blue"
    slash_str = "/"
    x_fund_pool = 99000
    x_fund_grain = 80
    x_respect_grain = 5
    sue_voice_pool = 800
    casa_str = "casa"
    bob_str = "Bob"
    last_pack_id = 7
    sue_max_tree_traverse = 9
    sue_beliefunit = beliefunit_shop(
        sue_str, blue_str, slash_str, x_fund_pool, x_fund_grain, x_respect_grain
    )
    sue_beliefunit.set_last_pack_id(last_pack_id)
    sue_beliefunit.add_voiceunit(bob_str, 3, 4)
    bob_voiceunit = sue_beliefunit.get_voice(bob_str)
    bob_voiceunit.add_membership(f"{slash_str}swimmers")
    sue_beliefunit.set_voice_respect(sue_voice_pool)
    sue_beliefunit.set_l1_plan(planunit_shop(casa_str))
    sue_beliefunit.set_max_tree_traverse(sue_max_tree_traverse)

    # WHEN
    default_job = get_default_job(sue_beliefunit)

    # THEN
    default_job.cashout()
    assert default_job.belief_name == sue_beliefunit.belief_name
    assert default_job.belief_name == sue_str
    assert default_job.moment_label == sue_beliefunit.moment_label
    assert default_job.moment_label == blue_str
    assert default_job.knot == slash_str
    assert default_job.fund_pool == sue_voice_pool
    assert default_job.fund_grain == x_fund_grain
    assert default_job.respect_grain == x_respect_grain
    assert default_job.credor_respect == RespectNum(default_pool_num())
    assert default_job.debtor_respect == RespectNum(default_pool_num())
    assert default_job.max_tree_traverse == sue_max_tree_traverse
    assert len(default_job.get_voiceunits_dict()) == 1
    assert len(default_job._plan_dict) == 1
