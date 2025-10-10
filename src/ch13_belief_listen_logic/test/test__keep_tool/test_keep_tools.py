from os.path import exists as os_path_exists
from src.ch01_data_toolbox.file_toolbox import delete_dir, open_file, save_file
from src.ch02_rope_logic.rope import create_rope
from src.ch07_belief_logic.test._util.ch07_examples import get_beliefunit_with_4_levels
from src.ch12_belief_file_toolbox._ref.ch12_path import create_keep_rope_path
from src.ch12_belief_file_toolbox.test._util.ch12_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)
from src.ch12_belief_file_toolbox.test._util.ch12_examples import (
    get_ch12_example_moment_label,
)
from src.ch13_belief_listen_logic.keep_tool import (
    create_keep_duty_path,
    create_keep_path_dir_if_missing,
    create_treasury_db_file,
    create_treasury_db_path,
    get_duty_belief,
    save_duty_belief,
    treasury_db_file_exists,
)


def test_create_keep_path_dir_if_missing_CreatesDirectory(
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
    moment_mstr_dir = get_chapter_temp_dir()
    keep_path = create_keep_rope_path(
        moment_mstr_dir, sue_str, a23_str, texas_rope, None
    )
    assert os_path_exists(keep_path) is False

    # WHEN
    create_keep_path_dir_if_missing(moment_mstr_dir, sue_str, a23_str, texas_rope, None)

    # THEN
    assert os_path_exists(keep_path)


def test_treasury_db_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "amy23"
    moment_mstr_dir = get_chapter_temp_dir()
    texas_rope = create_rope(get_ch12_example_moment_label(), "Texas")
    treasury_db_path = create_treasury_db_path(
        moment_mstr_dir,
        belief_name=sue_str,
        moment_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
    )
    assert (
        treasury_db_file_exists(
            moment_mstr_dir,
            belief_name=sue_str,
            moment_label=a23_str,
            keep_rope=texas_rope,
            knot=None,
        )
        is False
    )

    # WHEN
    save_file(treasury_db_path, None, "fizzbuzz")

    # THEN
    assert treasury_db_file_exists(
        moment_mstr_dir,
        belief_name=sue_str,
        moment_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
    )


def test_create_treasury_db_file_CreatesDatabase(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "amy23"
    moment_mstr_dir = get_chapter_temp_dir()
    texas_rope = create_rope(a23_str, "Texas")
    treasury_db_path = create_treasury_db_path(
        moment_mstr_dir=moment_mstr_dir,
        belief_name=sue_str,
        moment_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
    )
    assert os_path_exists(treasury_db_path) is False

    # WHEN
    create_treasury_db_file(
        moment_mstr_dir=moment_mstr_dir,
        belief_name=sue_str,
        moment_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
    )

    # THEN
    assert os_path_exists(treasury_db_path)


def test_create_treasury_db_DoesNotOverWriteDBIfExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH create keep
    sue_str = "Sue"
    a23_str = "amy23"
    moment_mstr_dir = get_chapter_temp_dir()
    texas_rope = create_rope(a23_str, "Texas")
    treasury_db_path = create_treasury_db_path(
        moment_mstr_dir=moment_mstr_dir,
        belief_name=sue_str,
        moment_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
    )
    delete_dir(treasury_db_path)  # clear out any treasury.db file
    create_treasury_db_file(
        moment_mstr_dir=moment_mstr_dir,
        belief_name=sue_str,
        moment_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
    )
    assert os_path_exists(treasury_db_path)

    # ESTABLISH
    treasury_db_path = create_treasury_db_path(
        moment_mstr_dir, sue_str, a23_str, texas_rope, None
    )
    x_file_str = "Texas Dallas ElPaso"
    save_file(treasury_db_path, None, file_str=x_file_str, replace=True)
    assert os_path_exists(treasury_db_path)
    assert open_file(treasury_db_path) == x_file_str

    # WHEN
    create_treasury_db_file(
        moment_mstr_dir=moment_mstr_dir,
        belief_name=sue_str,
        moment_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
    )

    # THEN
    assert open_file(treasury_db_path) == x_file_str


def test_save_duty_belief_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(get_ch12_example_moment_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"
    moment_mstr_dir = get_chapter_temp_dir()
    bob_str = "Bob"
    bob_belief = get_beliefunit_with_4_levels()
    bob_belief.set_belief_name(bob_str)
    keep_duty_path = create_keep_duty_path(
        moment_mstr_dir=moment_mstr_dir,
        belief_name=sue_str,
        moment_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
        duty_belief=bob_str,
    )
    assert os_path_exists(keep_duty_path) is False

    # WHEN
    save_duty_belief(
        moment_mstr_dir=moment_mstr_dir,
        belief_name=sue_str,
        moment_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
        duty_belief=bob_belief,
    )

    # THEN
    assert os_path_exists(keep_duty_path)


def test_get_duty_belief_reason_lowersFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(get_ch12_example_moment_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"
    moment_mstr_dir = get_chapter_temp_dir()
    bob_str = "Bob"
    bob_belief = get_beliefunit_with_4_levels()
    bob_belief.set_belief_name(bob_str)
    save_duty_belief(
        moment_mstr_dir=moment_mstr_dir,
        belief_name=sue_str,
        moment_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
        duty_belief=bob_belief,
    )

    # WHEN
    gen_bob_duty = get_duty_belief(
        moment_mstr_dir=moment_mstr_dir,
        belief_name=sue_str,
        moment_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
        duty_belief_name=bob_str,
    )

    # THEN
    assert gen_bob_duty.to_dict() == bob_belief.to_dict()
