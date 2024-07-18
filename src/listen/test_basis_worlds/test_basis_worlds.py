from src._road.finance import default_respect_num, validate_respect_num
from src._world.idea import ideaunit_shop
from src._world.world import worldunit_shop
from src.listen.basis_worlds import (
    create_empty_world,
    create_listen_basis,
    get_default_action_world,
)


def test_create_empty_world_ReturnsCorrectObj():
    # ESTABLISH
    yao_text = "Yao"
    slash_text = "/"
    penny_float = 0.7
    yao_voice = worldunit_shop(yao_text, _road_delimiter=slash_text, _penny=penny_float)
    yao_voice.add_l1_idea(ideaunit_shop("Iowa"))
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    zia_credor_pool = 87
    zia_debtor_pool = 81
    yao_voice.add_charunit(zia_text, zia_credor_weight, zia_debtor_weight)
    zia_irrational_debtor_weight = 11
    zia_inallocable_debtor_weight = 22
    duty_zia_charunit = yao_voice.get_char(zia_text)
    duty_zia_charunit.add_irrational_debtor_weight(zia_irrational_debtor_weight)
    duty_zia_charunit.add_inallocable_debtor_weight(zia_inallocable_debtor_weight)
    zia_charunit = yao_voice.get_char(zia_text)
    zia_charunit.add_lobbyship(f"{slash_text}swimmers")
    yao_voice.set_credor_respect(zia_credor_pool)
    yao_voice.set_debtor_resepect(zia_debtor_pool)

    # WHEN
    yao_empty_job = create_empty_world(yao_voice, x_owner_id=zia_text)

    # THEN
    assert yao_empty_job._owner_id != yao_voice._owner_id
    assert yao_empty_job._owner_id == zia_text
    assert yao_empty_job._real_id == yao_voice._real_id
    assert yao_empty_job._last_gift_id is None
    assert yao_empty_job.get_charunits_dict() == {}
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
    yao_empty_job.settle_world()
    assert yao_empty_job._chars == {}


def test_create_listen_basis_ReturnsCorrectObj():
    # ESTABLISH
    yao_text = "Yao"
    slash_text = "/"
    yao_duty = worldunit_shop(yao_text, _road_delimiter=slash_text)
    yao_duty.add_l1_idea(ideaunit_shop("Iowa"))
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    zia_credor_pool = 8700
    zia_debtor_pool = 8100
    yao_duty.add_charunit(zia_text, zia_credor_weight, zia_debtor_weight)
    zia_irrational_debtor_weight = 11
    zia_inallocable_debtor_weight = 22
    duty_zia_charunit = yao_duty.get_char(zia_text)
    duty_zia_charunit.add_irrational_debtor_weight(zia_irrational_debtor_weight)
    duty_zia_charunit.add_inallocable_debtor_weight(zia_inallocable_debtor_weight)
    zia_charunit = yao_duty.get_char(zia_text)
    zia_charunit.add_lobbyship(f"{slash_text}swimmers")
    yao_duty.set_credor_respect(zia_credor_pool)
    yao_duty.set_debtor_resepect(zia_debtor_pool)

    # WHEN
    yao_basis_job = create_listen_basis(yao_duty)

    # THEN
    assert yao_basis_job._owner_id == yao_duty._owner_id
    assert yao_basis_job._real_id == yao_duty._real_id
    assert yao_basis_job._last_gift_id == yao_duty._last_gift_id
    assert yao_basis_job.get_charunits_dict() == yao_duty.get_charunits_dict()
    assert yao_basis_job._road_delimiter == yao_duty._road_delimiter
    assert yao_basis_job._fund_pool == yao_duty._fund_pool
    assert yao_basis_job._fund_coin == yao_duty._fund_coin
    assert yao_basis_job._bit == yao_duty._bit
    assert yao_basis_job._monetary_desc == yao_duty._monetary_desc
    assert yao_basis_job._credor_respect == yao_duty._credor_respect
    assert yao_basis_job._debtor_respect == yao_duty._debtor_respect
    yao_basis_job.settle_world()
    assert len(yao_basis_job._idea_dict) != len(yao_duty._idea_dict)
    assert len(yao_basis_job._idea_dict) == 1
    job_zia_charunit = yao_basis_job.get_char(zia_text)
    assert (
        yao_basis_job.get_charunits_dict().keys()
        == yao_duty.get_charunits_dict().keys()
    )
    assert job_zia_charunit._irrational_debtor_weight == 0
    assert job_zia_charunit._inallocable_debtor_weight == 0


def test_get_default_action_world_ReturnsCorrectObj():
    # ESTABLISH
    sue_text = "Sue"
    blue_text = "blue"
    slash_text = "/"
    x_fund_pool = 99000
    x_fund_coin = 80
    x_bit = 5
    sue_char_pool = 800
    casa_text = "casa"
    bob_text = "Bob"
    last_gift_id = 7
    sue_max_tree_traverse = 9
    sue_worldunit = worldunit_shop(
        sue_text, blue_text, slash_text, x_fund_pool, x_fund_coin, x_bit
    )
    sue_worldunit.set_last_gift_id(last_gift_id)
    sue_worldunit.add_charunit(bob_text, 3, 4)
    bob_charunit = sue_worldunit.get_char(bob_text)
    bob_charunit.add_lobbyship(f"{slash_text}swimmers")
    sue_worldunit.set_char_respect(sue_char_pool)
    sue_worldunit.add_l1_idea(ideaunit_shop(casa_text))
    sue_worldunit.set_max_tree_traverse(sue_max_tree_traverse)

    # WHEN
    default_action_world = get_default_action_world(sue_worldunit)

    # THEN
    default_action_world.settle_world()
    assert default_action_world._owner_id == sue_worldunit._owner_id
    assert default_action_world._owner_id == sue_text
    assert default_action_world._real_id == sue_worldunit._real_id
    assert default_action_world._real_id == blue_text
    assert default_action_world._road_delimiter == slash_text
    assert default_action_world._fund_pool == sue_char_pool
    assert default_action_world._fund_coin == x_fund_coin
    assert default_action_world._bit == x_bit
    assert default_action_world._credor_respect == default_respect_num()
    assert default_action_world._debtor_respect == default_respect_num()
    assert default_action_world._max_tree_traverse == sue_max_tree_traverse
    assert len(default_action_world.get_charunits_dict()) == 1
    assert len(default_action_world._idea_dict) == 1
