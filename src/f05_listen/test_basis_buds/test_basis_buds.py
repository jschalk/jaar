from src.f01_road.finance import default_respect_num, validate_respect_num
from src.f02_bud.item import itemunit_shop
from src.f02_bud.bud import budunit_shop
from src.f05_listen.basis_buds import (
    create_empty_bud,
    create_listen_basis,
    get_default_forecast_bud,
)


def test_create_empty_bud_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    slash_str = "/"
    penny_float = 0.7
    yao_voice = budunit_shop(yao_str, bridge=slash_str, penny=penny_float)
    yao_voice.set_l1_item(itemunit_shop("Iowa"))
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
    yao_empty_job = create_empty_bud(yao_voice, x_owner_name=zia_str)

    # THEN
    assert yao_empty_job.owner_name != yao_voice.owner_name
    assert yao_empty_job.owner_name == zia_str
    assert yao_empty_job.fisc_title == yao_voice.fisc_title
    assert yao_empty_job.last_vow_id is None
    assert yao_empty_job.get_acctunits_dict() == {}
    assert yao_empty_job.bridge == yao_voice.bridge
    assert yao_empty_job.fund_pool == yao_voice.fund_pool
    assert yao_empty_job.fund_coin == yao_voice.fund_coin
    assert yao_empty_job.respect_bit == yao_voice.respect_bit
    assert yao_empty_job.penny == yao_voice.penny
    assert yao_empty_job.credor_respect != yao_voice.credor_respect
    assert yao_empty_job.credor_respect == validate_respect_num()
    assert yao_empty_job.debtor_respect != yao_voice.debtor_respect
    assert yao_empty_job.debtor_respect == validate_respect_num()
    yao_empty_job.settle_bud()
    assert yao_empty_job.accts == {}


def test_create_listen_basis_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    slash_str = "/"
    yao_duty = budunit_shop(yao_str, bridge=slash_str)
    yao_duty.set_l1_item(itemunit_shop("Iowa"))
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
    assert yao_basis_job.owner_name == yao_duty.owner_name
    assert yao_basis_job.fisc_title == yao_duty.fisc_title
    assert yao_basis_job.last_vow_id == yao_duty.last_vow_id
    assert yao_basis_job.get_acctunits_dict() == yao_duty.get_acctunits_dict()
    assert yao_basis_job.bridge == yao_duty.bridge
    assert yao_basis_job.fund_pool == yao_duty.fund_pool
    assert yao_basis_job.fund_coin == yao_duty.fund_coin
    assert yao_basis_job.respect_bit == yao_duty.respect_bit
    assert yao_basis_job.credor_respect == yao_duty.credor_respect
    assert yao_basis_job.debtor_respect == yao_duty.debtor_respect
    yao_basis_job.settle_bud()
    assert len(yao_basis_job._item_dict) != len(yao_duty._item_dict)
    assert len(yao_basis_job._item_dict) == 1
    job_zia_acctunit = yao_basis_job.get_acct(zia_str)
    assert (
        yao_basis_job.get_acctunits_dict().keys()
        == yao_duty.get_acctunits_dict().keys()
    )
    assert job_zia_acctunit._irrational_debtit_belief == 0
    assert job_zia_acctunit._inallocable_debtit_belief == 0


def test_get_default_forecast_bud_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    blue_str = "blue"
    slash_str = "/"
    x_fund_pool = 99000
    x_fund_coin = 80
    x_respect_bit = 5
    sue_acct_pool = 800
    casa_str = "casa"
    bob_str = "Bob"
    last_vow_id = 7
    sue_max_tree_traverse = 9
    sue_budunit = budunit_shop(
        sue_str, blue_str, slash_str, x_fund_pool, x_fund_coin, x_respect_bit
    )
    sue_budunit.set_last_vow_id(last_vow_id)
    sue_budunit.add_acctunit(bob_str, 3, 4)
    bob_acctunit = sue_budunit.get_acct(bob_str)
    bob_acctunit.add_membership(f"{slash_str}swimmers")
    sue_budunit.set_acct_respect(sue_acct_pool)
    sue_budunit.set_l1_item(itemunit_shop(casa_str))
    sue_budunit.set_max_tree_traverse(sue_max_tree_traverse)

    # WHEN
    default_forecast_bud = get_default_forecast_bud(sue_budunit)

    # THEN
    default_forecast_bud.settle_bud()
    assert default_forecast_bud.owner_name == sue_budunit.owner_name
    assert default_forecast_bud.owner_name == sue_str
    assert default_forecast_bud.fisc_title == sue_budunit.fisc_title
    assert default_forecast_bud.fisc_title == blue_str
    assert default_forecast_bud.bridge == slash_str
    assert default_forecast_bud.fund_pool == sue_acct_pool
    assert default_forecast_bud.fund_coin == x_fund_coin
    assert default_forecast_bud.respect_bit == x_respect_bit
    assert default_forecast_bud.credor_respect == default_respect_num()
    assert default_forecast_bud.debtor_respect == default_respect_num()
    assert default_forecast_bud.max_tree_traverse == sue_max_tree_traverse
    assert len(default_forecast_bud.get_acctunits_dict()) == 1
    assert len(default_forecast_bud._item_dict) == 1
