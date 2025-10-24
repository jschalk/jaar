from src.ch04_rope.rope import create_rope, default_knot_if_None
from src.ch07_belief_logic.test._util.ch07_examples import get_beliefunit_with_4_levels
from src.ch10_bud.test._util.ch10_env import get_temp_dir as env_dir, temp_dir_setup
from src.ch10_bud.test._util.ch10_examples import get_ch10_example_moment_label
from src.ch11_belief_listen.keep_tool import (
    get_vision_belief,
    save_vision_belief,
    vision_file_exists,
)


def test_save_vision_belief_SavesFile(temp_dir_setup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(get_ch10_example_moment_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"

    bob_str = "Bob"
    bob_belief = get_beliefunit_with_4_levels()
    bob_belief.set_belief_name(bob_str)
    x_knot = default_knot_if_None()
    assert not vision_file_exists(
        env_dir(), sue_str, a23_str, texas_rope, x_knot, bob_str
    )

    # WHEN
    save_vision_belief(env_dir(), sue_str, a23_str, texas_rope, x_knot, bob_belief)

    # THEN
    assert vision_file_exists(env_dir(), sue_str, a23_str, texas_rope, x_knot, bob_str)


def test_vision_file_exists_ReturnsBool(temp_dir_setup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(get_ch10_example_moment_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"

    bob_str = "Bob"
    bob_belief = get_beliefunit_with_4_levels()
    bob_belief.set_belief_name(bob_str)
    x_knot = default_knot_if_None()
    assert not (
        vision_file_exists(env_dir(), sue_str, a23_str, texas_rope, x_knot, bob_str)
    )

    # WHEN
    save_vision_belief(env_dir(), sue_str, a23_str, texas_rope, x_knot, bob_belief)

    # THEN
    assert vision_file_exists(env_dir(), sue_str, a23_str, texas_rope, x_knot, bob_str)


def test_get_vision_belief_reason_lowersFile(temp_dir_setup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(get_ch10_example_moment_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"

    bob_str = "Bob"
    bob_belief = get_beliefunit_with_4_levels()
    bob_belief.set_belief_name(bob_str)
    x_knot = default_knot_if_None()
    save_vision_belief(env_dir(), sue_str, a23_str, texas_rope, x_knot, bob_belief)

    # WHEN
    bob_vision = get_vision_belief(
        env_dir(), sue_str, a23_str, texas_rope, x_knot, bob_str
    )

    # THEN
    assert bob_vision.to_dict() == bob_belief.to_dict()


def test_get_vision_belief_ReturnsNoneIfFileDoesNotExist(
    temp_dir_setup,
):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(get_ch10_example_moment_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"
    bob_str = "Bob"
    x_knot = default_knot_if_None()

    # WHEN
    bob_vision = get_vision_belief(
        env_dir(), sue_str, a23_str, texas_rope, x_knot, bob_str
    )

    # THEN
    assert not bob_vision
