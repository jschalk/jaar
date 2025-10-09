from src.ch02_rope_logic.rope import create_rope
from src.ch07_belief_logic.test._util.ch07_examples import get_beliefunit_with_4_levels
from src.ch12_belief_file_toolbox.hubunit import hubunit_shop
from src.ch12_belief_file_toolbox.keep_tool import (
    get_vision_belief,
    save_vision_belief,
    vision_file_exists,
)
from src.ch12_belief_file_toolbox.test._util.ch12_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir as env_dir,
)
from src.ch12_belief_file_toolbox.test._util.ch12_examples import (
    get_ch12_example_moment_label,
)


def test_save_vision_belief_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(get_ch12_example_moment_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    bob_str = "Bob"
    bob_belief = get_beliefunit_with_4_levels()
    bob_belief.set_belief_name(bob_str)
    assert (
        vision_file_exists(
            sue_hubunit.moment_mstr_dir,
            sue_hubunit.belief_name,
            sue_hubunit.moment_label,
            sue_hubunit.keep_rope,
            sue_hubunit.knot,
            bob_str,
        )
        is False
    )

    # WHEN
    save_vision_belief(
        sue_hubunit.moment_mstr_dir,
        sue_hubunit.belief_name,
        sue_hubunit.moment_label,
        sue_hubunit.keep_rope,
        sue_hubunit.knot,
        bob_belief,
    )

    # THEN
    assert vision_file_exists(
        sue_hubunit.moment_mstr_dir,
        sue_hubunit.belief_name,
        sue_hubunit.moment_label,
        sue_hubunit.keep_rope,
        sue_hubunit.knot,
        bob_str,
    )


def test_vision_file_exists_ReturnsBool(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(get_ch12_example_moment_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    bob_str = "Bob"
    bob_belief = get_beliefunit_with_4_levels()
    bob_belief.set_belief_name(bob_str)
    assert (
        vision_file_exists(
            sue_hubunit.moment_mstr_dir,
            sue_hubunit.belief_name,
            sue_hubunit.moment_label,
            sue_hubunit.keep_rope,
            sue_hubunit.knot,
            bob_str,
        )
        is False
    )

    # WHEN
    save_vision_belief(
        sue_hubunit.moment_mstr_dir,
        sue_hubunit.belief_name,
        sue_hubunit.moment_label,
        sue_hubunit.keep_rope,
        sue_hubunit.knot,
        bob_belief,
    )

    # THEN
    assert vision_file_exists(
        sue_hubunit.moment_mstr_dir,
        sue_hubunit.belief_name,
        sue_hubunit.moment_label,
        sue_hubunit.keep_rope,
        sue_hubunit.knot,
        bob_str,
    )


def test_get_vision_belief_reason_lowersFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(get_ch12_example_moment_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    bob_str = "Bob"
    bob_belief = get_beliefunit_with_4_levels()
    bob_belief.set_belief_name(bob_str)
    save_vision_belief(
        sue_hubunit.moment_mstr_dir,
        sue_hubunit.belief_name,
        sue_hubunit.moment_label,
        sue_hubunit.keep_rope,
        sue_hubunit.knot,
        bob_belief,
    )

    # WHEN / THEN
    assert (
        get_vision_belief(
            sue_hubunit.moment_mstr_dir,
            sue_hubunit.belief_name,
            sue_hubunit.moment_label,
            sue_hubunit.keep_rope,
            sue_hubunit.knot,
            bob_str,
        ).to_dict()
        == bob_belief.to_dict()
    )


def test_get_vision_belief_ReturnsNoneIfFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(get_ch12_example_moment_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    bob_str = "Bob"

    # WHEN / THEN
    assert (
        get_vision_belief(
            sue_hubunit.moment_mstr_dir,
            sue_hubunit.belief_name,
            sue_hubunit.moment_label,
            sue_hubunit.keep_rope,
            sue_hubunit.knot,
            bob_str,
        )
        is None
    )
