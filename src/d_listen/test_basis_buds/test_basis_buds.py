from src._road.finance import default_respect_num, validate_respect_num
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.d_listen.basis_buds import (
    create_empty_bud,
    create_listen_basis,
    get_default_action_bud,
)


def test_create_empty_bud_ReturnsCorrectObj():
    # ESTABLISH
    yao_str = "Yao"
    slash_str = "/"
    penny_float = 0.7
    yao_voice = budunit_shop(yao_str, _road_delimiter=slash_str, penny=penny_float)
    yao_voice.set_l1_idea(ideaunit_shop("Iowa"))
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    zia_credor_pool = 87
    zia_debtor_pool = 81
    yao_voice.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    zia_irrational_debtit_belief = 11
    zia_inallocable_debtit_belief = 22
    duty_zia_acctunit = yao_voice.get_acct(zia_str)
    duty_zia_acctunit.add_irrational_debtit_belief(zia_irrational_debtit_belief)
    duty_zia_acctunit.add_inallocable_debtit_belief(zia_inallocable_debtit_belief)
    zia_acctunit = yao_voice.get_acct(zia_str)
    zia_acctunit.add_membership(f"{slash_str}swimmers")
    yao_voice.set_credor_respect(zia_credor_pool)
    yao_voice.set_debtor_respect(zia_debtor_pool)

    # WHEN
    yao_empty_job = create_empty_bud(yao_voice, x_owner_id=zia_str)

    # THEN
    assert yao_empty_job._owner_id != yao_voice._owner_id
    assert yao_empty_job._owner_id == zia_str
    assert yao_empty_job._fiscal_id == yao_voice._fiscal_id
    assert yao_empty_job._last_gift_id is None
    assert yao_empty_job.get_acctunits_dict() == {}
    assert yao_empty_job._road_delimiter == yao_voice._road_delimiter
    assert yao_empty_job.fund_pool == yao_voice.fund_pool
    assert yao_empty_job.fund_coin == yao_voice.fund_coin
    assert yao_empty_job.bit == yao_voice.bit
    assert yao_empty_job.penny == yao_voice.penny
    assert yao_empty_job.monetary_desc is None
    assert yao_empty_job.credor_respect != yao_voice.credor_respect
    assert yao_empty_job.credor_respect == validate_respect_num()
    assert yao_empty_job.debtor_respect != yao_voice.debtor_respect
    assert yao_empty_job.debtor_respect == validate_respect_num()
    yao_empty_job.settle_bud()
    assert yao_empty_job._accts == {}


def test_create_listen_basis_ReturnsCorrectObj():
    # ESTABLISH
    yao_str = "Yao"
    slash_str = "/"
    yao_duty = budunit_shop(yao_str, _road_delimiter=slash_str)
    yao_duty.set_l1_idea(ideaunit_shop("Iowa"))
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    zia_credor_pool = 8700
    zia_debtor_pool = 8100
    yao_duty.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    zia_irrational_debtit_belief = 11
    zia_inallocable_debtit_belief = 22
    duty_zia_acctunit = yao_duty.get_acct(zia_str)
    duty_zia_acctunit.add_irrational_debtit_belief(zia_irrational_debtit_belief)
    duty_zia_acctunit.add_inallocable_debtit_belief(zia_inallocable_debtit_belief)
    zia_acctunit = yao_duty.get_acct(zia_str)
    zia_acctunit.add_membership(f"{slash_str}swimmers")
    yao_duty.set_credor_respect(zia_credor_pool)
    yao_duty.set_debtor_respect(zia_debtor_pool)

    # WHEN
    yao_basis_job = create_listen_basis(yao_duty)

    # THEN
    assert yao_basis_job._owner_id == yao_duty._owner_id
    assert yao_basis_job._fiscal_id == yao_duty._fiscal_id
    assert yao_basis_job._last_gift_id == yao_duty._last_gift_id
    assert yao_basis_job.get_acctunits_dict() == yao_duty.get_acctunits_dict()
    assert yao_basis_job._road_delimiter == yao_duty._road_delimiter
    assert yao_basis_job.fund_pool == yao_duty.fund_pool
    assert yao_basis_job.fund_coin == yao_duty.fund_coin
    assert yao_basis_job.bit == yao_duty.bit
    assert yao_basis_job.monetary_desc == yao_duty.monetary_desc
    assert yao_basis_job.credor_respect == yao_duty.credor_respect
    assert yao_basis_job.debtor_respect == yao_duty.debtor_respect
    yao_basis_job.settle_bud()
    assert len(yao_basis_job._idea_dict) != len(yao_duty._idea_dict)
    assert len(yao_basis_job._idea_dict) == 1
    job_zia_acctunit = yao_basis_job.get_acct(zia_str)
    assert (
        yao_basis_job.get_acctunits_dict().keys()
        == yao_duty.get_acctunits_dict().keys()
    )
    assert job_zia_acctunit._irrational_debtit_belief == 0
    assert job_zia_acctunit._inallocable_debtit_belief == 0


def test_get_default_action_bud_ReturnsCorrectObj():
    # ESTABLISH
    sue_str = "Sue"
    blue_str = "blue"
    slash_str = "/"
    x_fund_pool = 99000
    x_fund_coin = 80
    x_bit = 5
    sue_acct_pool = 800
    casa_str = "casa"
    bob_str = "Bob"
    last_gift_id = 7
    sue_max_tree_traverse = 9
    sue_budunit = budunit_shop(
        sue_str, blue_str, slash_str, x_fund_pool, x_fund_coin, x_bit
    )
    sue_budunit.set_last_gift_id(last_gift_id)
    sue_budunit.add_acctunit(bob_str, 3, 4)
    bob_acctunit = sue_budunit.get_acct(bob_str)
    bob_acctunit.add_membership(f"{slash_str}swimmers")
    sue_budunit.set_acct_respect(sue_acct_pool)
    sue_budunit.set_l1_idea(ideaunit_shop(casa_str))
    sue_budunit.set_max_tree_traverse(sue_max_tree_traverse)

    # WHEN
    default_action_bud = get_default_action_bud(sue_budunit)

    # THEN
    default_action_bud.settle_bud()
    assert default_action_bud._owner_id == sue_budunit._owner_id
    assert default_action_bud._owner_id == sue_str
    assert default_action_bud._fiscal_id == sue_budunit._fiscal_id
    assert default_action_bud._fiscal_id == blue_str
    assert default_action_bud._road_delimiter == slash_str
    assert default_action_bud.fund_pool == sue_acct_pool
    assert default_action_bud.fund_coin == x_fund_coin
    assert default_action_bud.bit == x_bit
    assert default_action_bud.credor_respect == default_respect_num()
    assert default_action_bud.debtor_respect == default_respect_num()
    assert default_action_bud.max_tree_traverse == sue_max_tree_traverse
    assert len(default_action_bud.get_acctunits_dict()) == 1
    assert len(default_action_bud._idea_dict) == 1
