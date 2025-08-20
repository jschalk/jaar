from os.path import exists as os_path_exist, exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import delete_dir, open_file, save_file
from src.a01_term_logic.rope import create_rope
from src.a05_plan_logic.plan import get_default_coin_label as root_label
from src.a06_believer_logic.test._util.example_believers import (
    get_believerunit_with_4_levels,
)
from src.a12_hub_toolbox.a12_path import create_keep_rope_path
from src.a12_hub_toolbox.keep_tool import (
    create_keep_duty_path,
    create_keep_path_dir_if_missing,
    create_treasury_db_file,
    create_treasury_db_path,
    get_duty_believer,
    save_duty_believer,
    treasury_db_file_exists,
)
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
    coin_mstr_dir = get_module_temp_dir()
    keep_path = create_keep_rope_path(coin_mstr_dir, sue_str, a23_str, texas_rope, None)
    assert os_path_exists(keep_path) is False

    # WHEN
    create_keep_path_dir_if_missing(coin_mstr_dir, sue_str, a23_str, texas_rope, None)

    # THEN
    assert os_path_exists(keep_path)


def test_treasury_db_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "amy23"
    coin_mstr_dir = get_module_temp_dir()
    texas_rope = create_rope(root_label(), "Texas")
    treasury_db_path = create_treasury_db_path(
        coin_mstr_dir,
        believer_name=sue_str,
        coin_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
    )
    assert (
        treasury_db_file_exists(
            coin_mstr_dir,
            believer_name=sue_str,
            coin_label=a23_str,
            keep_rope=texas_rope,
            knot=None,
        )
        is False
    )

    # WHEN
    save_file(treasury_db_path, None, "fizzbuzz")

    # THEN
    assert treasury_db_file_exists(
        coin_mstr_dir,
        believer_name=sue_str,
        coin_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
    )


def test_create_treasury_db_file_CreatesDatabase(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    a23_str = "amy23"
    coin_mstr_dir = get_module_temp_dir()
    texas_rope = create_rope(a23_str, "Texas")
    treasury_db_path = create_treasury_db_path(
        coin_mstr_dir=coin_mstr_dir,
        believer_name=sue_str,
        coin_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
    )
    assert os_path_exists(treasury_db_path) is False

    # WHEN
    create_treasury_db_file(
        coin_mstr_dir=coin_mstr_dir,
        believer_name=sue_str,
        coin_label=a23_str,
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
    coin_mstr_dir = get_module_temp_dir()
    texas_rope = create_rope(a23_str, "Texas")
    treasury_db_path = create_treasury_db_path(
        coin_mstr_dir=coin_mstr_dir,
        believer_name=sue_str,
        coin_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
    )
    delete_dir(treasury_db_path)  # clear out any treasury.db file
    create_treasury_db_file(
        coin_mstr_dir=coin_mstr_dir,
        believer_name=sue_str,
        coin_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
    )
    assert os_path_exists(treasury_db_path)

    # ESTABLISH
    treasury_db_path = create_treasury_db_path(
        coin_mstr_dir, sue_str, a23_str, texas_rope, None
    )
    x_file_str = "Texas Dallas ElPaso"
    save_file(treasury_db_path, None, file_str=x_file_str, replace=True)
    assert os_path_exists(treasury_db_path)
    assert open_file(treasury_db_path) == x_file_str

    # WHEN
    create_treasury_db_file(
        coin_mstr_dir=coin_mstr_dir,
        believer_name=sue_str,
        coin_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
    )

    # THEN
    assert open_file(treasury_db_path) == x_file_str


def test_save_duty_believer_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"
    coin_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"
    bob_believer = get_believerunit_with_4_levels()
    bob_believer.set_believer_name(bob_str)
    keep_duty_path = create_keep_duty_path(
        coin_mstr_dir=coin_mstr_dir,
        believer_name=sue_str,
        coin_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
        duty_believer=bob_str,
    )
    assert os_path_exists(keep_duty_path) is False

    # WHEN
    save_duty_believer(
        coin_mstr_dir=coin_mstr_dir,
        believer_name=sue_str,
        coin_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
        duty_believer=bob_believer,
    )

    # THEN
    assert os_path_exists(keep_duty_path)


def test_get_duty_believer_reason_lowersFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    a23_str = "amy23"
    coin_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"
    bob_believer = get_believerunit_with_4_levels()
    bob_believer.set_believer_name(bob_str)
    save_duty_believer(
        coin_mstr_dir=coin_mstr_dir,
        believer_name=sue_str,
        coin_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
        duty_believer=bob_believer,
    )

    # WHEN
    gen_bob_duty = get_duty_believer(
        coin_mstr_dir=coin_mstr_dir,
        believer_name=sue_str,
        coin_label=a23_str,
        keep_rope=texas_rope,
        knot=None,
        duty_believer_name=bob_str,
    )

    # THEN
    assert gen_bob_duty.to_dict() == bob_believer.to_dict()
