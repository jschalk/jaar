from os.path import exists as os_path_exists
from src.a01_term_logic.rope import create_rope
from src.a05_plan_logic.plan import get_default_belief_label as root_label
from src.a12_hub_toolbox.a12_path import create_keep_rope_path
from src.a12_hub_toolbox.keep_tool import create_keep_path_dir_if_missing
from src.a12_hub_toolbox.test._util.a12_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_create_keep_path_dir_if_missing_CreatesDirectory(
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
    belief_mstr_dir = get_module_temp_dir()
    keep_path = create_keep_rope_path(
        belief_mstr_dir, sue_str, a23_str, texas_rope, None
    )
    assert os_path_exists(keep_path) is False

    # WHEN
    create_keep_path_dir_if_missing(belief_mstr_dir, sue_str, a23_str, texas_rope, None)

    # THEN
    assert os_path_exists(keep_path)
