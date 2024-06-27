from src._world.beliefunit import beliefunit_shop
from src._world.char import charlink_shop
from src._world.idea import ideaunit_shop
from src._world.world import worldunit_shop
from src.listen.basis_worlds import (
    create_empty_world,
    create_listen_basis,
    get_default_home_world,
)


def test_create_empty_world_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    slash_text = "/"
    penny_float = 0.7
    yao_soul = worldunit_shop(yao_text, _road_delimiter=slash_text, _penny=penny_float)
    yao_soul.add_l1_idea(ideaunit_shop("Iowa"))
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    zia_credor_pool = 87
    zia_debtor_pool = 81
    yao_soul.add_charunit(zia_text, zia_credor_weight, zia_debtor_weight)
    zia_irrational_debtor_weight = 11
    zia_inallocable_debtor_weight = 22
    role_zia_charunit = yao_soul.get_char(zia_text)
    role_zia_charunit.add_irrational_debtor_weight(zia_irrational_debtor_weight)
    role_zia_charunit.add_inallocable_debtor_weight(zia_inallocable_debtor_weight)
    swim_belief = beliefunit_shop(f"{slash_text}swimmers", _road_delimiter=slash_text)
    swim_belief.set_charlink(charlink_shop(zia_text))
    yao_soul.set_beliefunit(swim_belief)
    yao_soul.set_char_credor_pool(zia_credor_pool, True)
    yao_soul.set_char_debtor_pool(zia_debtor_pool, True)

    # WHEN
    yao_empty_job = create_empty_world(yao_soul, x_owner_id=zia_text)

    # THEN
    assert yao_empty_job._owner_id != yao_soul._owner_id
    assert yao_empty_job._owner_id == zia_text
    assert yao_empty_job._real_id == yao_soul._real_id
    assert yao_empty_job._last_gift_id is None
    assert yao_empty_job.get_beliefunits_dict() == {}
    assert yao_empty_job._road_delimiter == yao_soul._road_delimiter
    assert yao_empty_job._pixel == yao_soul._pixel
    assert yao_empty_job._penny == yao_soul._penny
    assert yao_empty_job._monetary_desc is None
    assert yao_empty_job._char_credor_pool != yao_soul._char_credor_pool
    assert yao_empty_job._char_credor_pool is None
    assert yao_empty_job._char_debtor_pool != yao_soul._char_debtor_pool
    assert yao_empty_job._char_debtor_pool is None
    yao_empty_job.calc_world_metrics()
    assert yao_empty_job._chars == {}


def test_create_listen_basis_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    slash_text = "/"
    yao_role = worldunit_shop(yao_text, _road_delimiter=slash_text)
    yao_role.add_l1_idea(ideaunit_shop("Iowa"))
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    zia_credor_pool = 87
    zia_debtor_pool = 81
    yao_role.add_charunit(zia_text, zia_credor_weight, zia_debtor_weight)
    zia_irrational_debtor_weight = 11
    zia_inallocable_debtor_weight = 22
    role_zia_charunit = yao_role.get_char(zia_text)
    role_zia_charunit.add_irrational_debtor_weight(zia_irrational_debtor_weight)
    role_zia_charunit.add_inallocable_debtor_weight(zia_inallocable_debtor_weight)
    swim_belief = beliefunit_shop(f"{slash_text}swimmers", _road_delimiter=slash_text)
    swim_belief.set_charlink(charlink_shop(zia_text))
    yao_role.set_beliefunit(swim_belief)
    yao_role.set_char_credor_pool(zia_credor_pool, True)
    yao_role.set_char_debtor_pool(zia_debtor_pool, True)

    # WHEN
    yao_basis_job = create_listen_basis(yao_role)

    # THEN
    assert yao_basis_job._owner_id == yao_role._owner_id
    assert yao_basis_job._real_id == yao_role._real_id
    assert yao_basis_job._last_gift_id == yao_role._last_gift_id
    assert yao_basis_job.get_beliefunits_dict() == yao_role.get_beliefunits_dict()
    assert yao_basis_job._road_delimiter == yao_role._road_delimiter
    assert yao_basis_job._pixel == yao_role._pixel
    assert yao_basis_job._monetary_desc == yao_role._monetary_desc
    assert yao_basis_job._char_credor_pool == yao_role._char_credor_pool
    assert yao_basis_job._char_debtor_pool == yao_role._char_debtor_pool
    yao_basis_job.calc_world_metrics()
    assert len(yao_basis_job._idea_dict) != len(yao_role._idea_dict)
    assert len(yao_basis_job._idea_dict) == 1
    job_zia_charunit = yao_basis_job.get_char(zia_text)
    assert yao_basis_job.get_chars_dict().keys() == yao_role.get_chars_dict().keys()
    assert job_zia_charunit._irrational_debtor_weight == 0
    assert job_zia_charunit._inallocable_debtor_weight == 0


def test_get_default_home_world_ReturnsCorrectObj():
    # GIVEN
    sue_text = "Sue"
    blue_text = "blue"
    slash_text = "/"
    five_pixel = 5
    sue_char_pool = 800
    casa_text = "casa"
    bob_text = "Bob"
    last_gift_id = 7
    sue_max_tree_traverse = 9
    sue_worldunit = worldunit_shop(sue_text, blue_text, slash_text, five_pixel)
    sue_worldunit.set_last_gift_id(last_gift_id)
    sue_worldunit.add_charunit(bob_text, 3, 4)
    swim_text = "/swimmers"
    swim_beliefunit = beliefunit_shop(swim_text, _road_delimiter=slash_text)
    swim_beliefunit.edit_charlink(bob_text)
    sue_worldunit.set_beliefunit(swim_beliefunit)
    sue_worldunit.set_char_pool(sue_char_pool)
    sue_worldunit.add_l1_idea(ideaunit_shop(casa_text))
    sue_worldunit.set_max_tree_traverse(sue_max_tree_traverse)

    # WHEN
    default_home_world = get_default_home_world(sue_worldunit)

    # THEN
    default_home_world.calc_world_metrics()
    assert default_home_world._owner_id == sue_worldunit._owner_id
    assert default_home_world._owner_id == sue_text
    assert default_home_world._real_id == sue_worldunit._real_id
    assert default_home_world._real_id == blue_text
    assert default_home_world._road_delimiter == slash_text
    assert default_home_world._pixel == five_pixel
    assert default_home_world._char_credor_pool is None
    assert default_home_world._char_debtor_pool is None
    assert default_home_world._max_tree_traverse == sue_max_tree_traverse
    assert len(default_home_world.get_chars_dict()) == 1
    assert len(default_home_world.get_beliefunits_dict()) == 1
    assert len(default_home_world._idea_dict) == 1
