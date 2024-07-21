from src.bud.healer import healerhold_shop
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.listen.hubunit import hubunit_shop
from src.real.real import realunit_shop
from src.real.examples.real_env import get_test_reals_dir, env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_RealUnit_generate_action_bud_Sets_action_BudFile(env_dir_setup_cleanup):
    # ESTABLISH
    music_text = "Music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), True)
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(None, music_text, sue_text, None)
    x_sue_action_path = f"{music_real._owners_dir}/{sue_text}/action/{sue_text}.json"
    assert os_path_exists(x_sue_action_path) is False
    music_real.init_owner_econs(sue_text)
    assert sue_hubunit.action_path() == x_sue_action_path
    assert os_path_exists(x_sue_action_path)

    # WHEN
    sue_action = music_real.generate_action_bud(sue_text)

    # THEN
    example_bud = budunit_shop(sue_text, music_text)
    assert sue_action._real_id == example_bud._real_id
    assert sue_action._owner_id == example_bud._owner_id


def test_RealUnit_generate_action_bud_ReturnsRegeneratedObj(env_dir_setup_cleanup):
    # ESTABLISH
    music_real = realunit_shop("music", get_test_reals_dir(), True)
    sue_text = "Sue"
    music_real.init_owner_econs(sue_text)
    sue_hubunit = hubunit_shop(music_real.reals_dir, music_real.real_id, sue_text, None)
    before_sue_bud = sue_hubunit.get_action_bud()
    bob_text = "Bob"
    before_sue_bud.add_acctunit(bob_text)
    sue_hubunit.save_action_bud(before_sue_bud)
    assert sue_hubunit.get_action_bud().acct_exists(bob_text)

    # WHEN
    after_sue_bud = music_real.generate_action_bud(sue_text)

    # THEN method should wipe over action bud
    assert after_sue_bud.acct_exists(bob_text) is False


def test_RealUnit_generate_action_bud_SetsCorrectFileWithout_healerhold(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    music_real = realunit_shop("music", get_test_reals_dir(), True)
    bob_text = "Bob"
    music_real.init_owner_econs(bob_text)
    bob_hubunit = hubunit_shop(music_real.reals_dir, music_real.real_id, bob_text, None)
    before_bob_action_bud = music_real.generate_action_bud(bob_text)
    sue_text = "Sue"
    assert before_bob_action_bud.acct_exists(sue_text) is False

    # WHEN
    bob_voice_bud = bob_hubunit.get_voice_bud()
    bob_voice_bud.add_acctunit(sue_text)
    bob_hubunit.save_voice_bud(bob_voice_bud)

    # WHEN
    after_bob_action_bud = music_real.generate_action_bud(bob_text)

    # THEN
    assert after_bob_action_bud.acct_exists(sue_text)


def test_RealUnit_generate_action_bud_SetsFileWith_healerhold(env_dir_setup_cleanup):
    # ESTABLISH
    music_real = realunit_shop("music", get_test_reals_dir(), True)

    bob_text = "Bob"
    music_real.init_owner_econs(bob_text)
    bob_hubunit = hubunit_shop(music_real.reals_dir, music_real.real_id, bob_text, None)
    after_bob_action_bud = music_real.generate_action_bud(bob_text)
    assert after_bob_action_bud.acct_exists(bob_text) is False

    # WHEN
    bob_voice_bud = bob_hubunit.get_voice_bud()
    bob_voice_bud.add_acctunit(bob_text)
    bob_voice_bud.set_acct_respect(100)
    texas_text = "Texas"
    texas_road = bob_voice_bud.make_l1_road(texas_text)
    elpaso_text = "el paso"
    elpaso_road = bob_voice_bud.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({bob_text}))
    bob_voice_bud.set_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    bob_voice_bud.set_idea(elpaso_idea, texas_road)
    bob_hubunit.save_voice_bud(bob_voice_bud)
    after_bob_action_bud = music_real.generate_action_bud(bob_text)

    # THEN
    assert after_bob_action_bud.acct_exists(bob_text)


def test_RealUnit_generate_all_action_buds_SetsCorrectFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    music_real = realunit_shop("music", get_test_reals_dir(), True)

    bob_text = "Bob"
    sue_text = "Sue"
    music_real.init_owner_econs(bob_text)
    reals_dir = music_real.reals_dir
    bob_hubunit = hubunit_shop(reals_dir, music_real.real_id, bob_text, None)
    music_real.init_owner_econs(sue_text)
    sue_hubunit = hubunit_shop(reals_dir, music_real.real_id, sue_text, None)
    bob_voice_bud = music_real.generate_action_bud(bob_text)
    sue_voice_bud = music_real.generate_action_bud(sue_text)

    texas_text = "Texas"
    texas_road = bob_voice_bud.make_l1_road(texas_text)
    elpaso_text = "el paso"
    elpaso_road = bob_voice_bud.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({bob_text}))

    bob_voice_bud = bob_hubunit.get_voice_bud()
    bob_voice_bud.add_acctunit(bob_text)
    bob_voice_bud.set_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    bob_voice_bud.set_idea(elpaso_idea, texas_road)
    bob_hubunit.save_voice_bud(bob_voice_bud)

    sue_voice_bud = sue_hubunit.get_voice_bud()
    sue_voice_bud.add_acctunit(sue_text)
    sue_voice_bud.add_acctunit(bob_text)
    sue_voice_bud.set_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    sue_voice_bud.set_idea(elpaso_idea, texas_road)
    sue_hubunit.save_voice_bud(sue_voice_bud)

    before_bob_action_bud = music_real.get_action_file_bud(bob_text)
    before_sue_action_bud = music_real.get_action_file_bud(sue_text)
    assert before_bob_action_bud.acct_exists(bob_text) is False
    assert before_sue_action_bud.acct_exists(sue_text) is False

    # WHEN
    music_real.generate_all_action_buds()

    # THEN
    after_bob_action_bud = music_real.get_action_file_bud(bob_text)
    after_sue_action_bud = music_real.get_action_file_bud(sue_text)
    assert after_bob_action_bud.acct_exists(bob_text)
    assert after_sue_action_bud.acct_exists(sue_text)
