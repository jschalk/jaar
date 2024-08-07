from src._road.finance import default_respect_num, validate_respect_num
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.listen.basis_buds import (
    create_empty_bud,
    create_listen_basis,
    get_default_action_bud,
)


def test_create_empty_bud_ReturnsCorrectObj():
    # ESTABLISH
    yao_text = "Yao"
    slash_text = "/"
    penny_float = 0.7
    yao_voice = budunit_shop(yao_text, _road_delimiter=slash_text, _penny=penny_float)
    yao_voice.set_l1_idea(ideaunit_shop("Iowa"))
    zia_text = "Zia"
    zia_credit_score = 47
    zia_debtit_score = 41
    zia_credor_pool = 87
    zia_debtor_pool = 81
    yao_voice.add_acctunit(zia_text, zia_credit_score, zia_debtit_score)
    zia_irrational_debtit_score = 11
    zia_inallocable_debtit_score = 22
    duty_zia_acctunit = yao_voice.get_acct(zia_text)
    duty_zia_acctunit.add_irrational_debtit_score(zia_irrational_debtit_score)
    duty_zia_acctunit.add_inallocable_debtit_score(zia_inallocable_debtit_score)
    zia_acctunit = yao_voice.get_acct(zia_text)
    zia_acctunit.add_membership(f"{slash_text}swimmers")
    yao_voice.set_credor_respect(zia_credor_pool)
    yao_voice.set_debtor_respect(zia_debtor_pool)

    # WHEN
    yao_empty_job = create_empty_bud(yao_voice, x_owner_id=zia_text)

    # THEN
    assert yao_empty_job._owner_id != yao_voice._owner_id
    assert yao_empty_job._owner_id == zia_text
    assert yao_empty_job._real_id == yao_voice._real_id
    assert yao_empty_job._last_gift_id is None
    assert yao_empty_job.get_acctunits_dict() == {}
    assert yao_empty_job._road_delimiter == yao_voice._road_delimiter
    assert yao_empty_job._fund_pool == yao_voice._fund_pool
    assert yao_empty_job._fund_coin == yao_voice._fund_coin
    assert yao_empty_job._bit == yao_voice._bit
    assert yao_empty_job._penny == yao_voice._penny
    assert yao_empty_job._monetary_desc is None
    assert yao_empty_job._credor_respect != yao_voice._credor_respect
    assert yao_empty_job._credor_respect == validate_respect_num()
    assert yao_empty_job._debtor_respect != yao_voice._debtor_respect
    assert yao_empty_job._debtor_respect == validate_respect_num()
    yao_empty_job.settle_bud()
    assert yao_empty_job._accts == {}


def test_create_listen_basis_ReturnsCorrectObj():
    # ESTABLISH
    yao_text = "Yao"
    slash_text = "/"
    yao_duty = budunit_shop(yao_text, _road_delimiter=slash_text)
    yao_duty.set_l1_idea(ideaunit_shop("Iowa"))
    zia_text = "Zia"
    zia_credit_score = 47
    zia_debtit_score = 41
    zia_credor_pool = 8700
    zia_debtor_pool = 8100
    yao_duty.add_acctunit(zia_text, zia_credit_score, zia_debtit_score)
    zia_irrational_debtit_score = 11
    zia_inallocable_debtit_score = 22
    duty_zia_acctunit = yao_duty.get_acct(zia_text)
    duty_zia_acctunit.add_irrational_debtit_score(zia_irrational_debtit_score)
    duty_zia_acctunit.add_inallocable_debtit_score(zia_inallocable_debtit_score)
    zia_acctunit = yao_duty.get_acct(zia_text)
    zia_acctunit.add_membership(f"{slash_text}swimmers")
    yao_duty.set_credor_respect(zia_credor_pool)
    yao_duty.set_debtor_respect(zia_debtor_pool)

    # WHEN
    yao_basis_job = create_listen_basis(yao_duty)

    # THEN
    assert yao_basis_job._owner_id == yao_duty._owner_id
    assert yao_basis_job._real_id == yao_duty._real_id
    assert yao_basis_job._last_gift_id == yao_duty._last_gift_id
    assert yao_basis_job.get_acctunits_dict() == yao_duty.get_acctunits_dict()
    assert yao_basis_job._road_delimiter == yao_duty._road_delimiter
    assert yao_basis_job._fund_pool == yao_duty._fund_pool
    assert yao_basis_job._fund_coin == yao_duty._fund_coin
    assert yao_basis_job._bit == yao_duty._bit
    assert yao_basis_job._monetary_desc == yao_duty._monetary_desc
    assert yao_basis_job._credor_respect == yao_duty._credor_respect
    assert yao_basis_job._debtor_respect == yao_duty._debtor_respect
    yao_basis_job.settle_bud()
    assert len(yao_basis_job._idea_dict) != len(yao_duty._idea_dict)
    assert len(yao_basis_job._idea_dict) == 1
    job_zia_acctunit = yao_basis_job.get_acct(zia_text)
    assert (
        yao_basis_job.get_acctunits_dict().keys()
        == yao_duty.get_acctunits_dict().keys()
    )
    assert job_zia_acctunit._irrational_debtit_score == 0
    assert job_zia_acctunit._inallocable_debtit_score == 0


def test_get_default_action_bud_ReturnsCorrectObj():
    # ESTABLISH
    sue_text = "Sue"
    blue_text = "blue"
    slash_text = "/"
    x_fund_pool = 99000
    x_fund_coin = 80
    x_bit = 5
    sue_acct_pool = 800
    casa_text = "casa"
    bob_text = "Bob"
    last_gift_id = 7
    sue_max_tree_traverse = 9
    sue_budunit = budunit_shop(
        sue_text, blue_text, slash_text, x_fund_pool, x_fund_coin, x_bit
    )
    sue_budunit.set_last_gift_id(last_gift_id)
    sue_budunit.add_acctunit(bob_text, 3, 4)
    bob_acctunit = sue_budunit.get_acct(bob_text)
    bob_acctunit.add_membership(f"{slash_text}swimmers")
    sue_budunit.set_acct_respect(sue_acct_pool)
    sue_budunit.set_l1_idea(ideaunit_shop(casa_text))
    sue_budunit.set_max_tree_traverse(sue_max_tree_traverse)

    # WHEN
    default_action_bud = get_default_action_bud(sue_budunit)

    # THEN
    default_action_bud.settle_bud()
    assert default_action_bud._owner_id == sue_budunit._owner_id
    assert default_action_bud._owner_id == sue_text
    assert default_action_bud._real_id == sue_budunit._real_id
    assert default_action_bud._real_id == blue_text
    assert default_action_bud._road_delimiter == slash_text
    assert default_action_bud._fund_pool == sue_acct_pool
    assert default_action_bud._fund_coin == x_fund_coin
    assert default_action_bud._bit == x_bit
    assert default_action_bud._credor_respect == default_respect_num()
    assert default_action_bud._debtor_respect == default_respect_num()
    assert default_action_bud._max_tree_traverse == sue_max_tree_traverse
    assert len(default_action_bud.get_acctunits_dict()) == 1
    assert len(default_action_bud._idea_dict) == 1
