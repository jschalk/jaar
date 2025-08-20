from os.path import exists as os_path_exists
from src.a01_term_logic.rope import create_rope
from src.a05_plan_logic.plan import get_default_moment_label as root_label
from src.a06_belief_logic.test._util.example_beliefs import get_beliefunit_with_4_levels
from src.a12_hub_toolbox.a12_path import create_keep_duty_path, create_treasury_db_path
from src.a12_hub_toolbox.hubunit import hubunit_shop
from src.a12_hub_toolbox.keep_tool import (
    create_treasury_db_file,
    save_duty_belief,
    treasury_db_file_exists,
)
from src.a12_hub_toolbox.test._util.a12_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as env_dir,
)
from src.a12_hub_toolbox.test._util.example_hub_atoms import (
    get_texas_hubunit,
    get_texas_rope,
)


def test_HubUnit_save_vision_belief_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    bob_str = "Bob"
    bob_belief = get_beliefunit_with_4_levels()
    bob_belief.set_belief_name(bob_str)
    assert sue_hubunit.vision_file_exists(bob_str) is False

    # WHEN
    sue_hubunit.save_vision_belief(bob_belief)

    # THEN
    assert sue_hubunit.vision_file_exists(bob_str)


def test_HubUnit_vision_file_exists_ReturnsBool(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    bob_str = "Bob"
    bob_belief = get_beliefunit_with_4_levels()
    bob_belief.set_belief_name(bob_str)
    assert sue_hubunit.vision_file_exists(bob_str) is False

    # WHEN
    sue_hubunit.save_vision_belief(bob_belief)

    # THEN
    assert sue_hubunit.vision_file_exists(bob_str)


def test_HubUnit_get_vision_belief_reason_lowersFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    bob_str = "Bob"
    bob_belief = get_beliefunit_with_4_levels()
    bob_belief.set_belief_name(bob_str)
    sue_hubunit.save_vision_belief(bob_belief)

    # WHEN / THEN
    assert sue_hubunit.get_vision_belief(bob_str).to_dict() == bob_belief.to_dict()


def test_HubUnit_get_vision_belief_ReturnsNoneIfFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"
    sue_hubunit = hubunit_shop(env_dir(), a23_str, sue_str, texas_rope)
    bob_str = "Bob"

    # WHEN / THEN
    assert sue_hubunit.get_vision_belief(bob_str) is None
