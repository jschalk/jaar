from os.path import exists as os_path_exists
from src.ch01_data_toolbox.file_toolbox import create_path, delete_dir
from src.ch10_pack_logic.pack import init_pack_id
from src.ch12_pack_file.packfilehandler import (
    create_gut_path,
    gut_file_exists,
    open_gut_file,
    packfilehandler_shop,
    save_gut_file,
)
from src.ch12_pack_file.test._util.ch12_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir as env_dir,
)
from src.ch12_pack_file.test._util.ch12_examples import sue_2beliefatoms_packunit


def test_PackFileHandler_default_gut_belief_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    slash_str = "/"
    x_fund_pool = 9000000
    pnine_float = 0.9
    pfour_float = 0.4
    sue_packfilehandler = packfilehandler_shop(
        env_dir(),
        "amy23",
        sue_str,
        knot=slash_str,
        fund_pool=x_fund_pool,
        fund_grain=pnine_float,
        respect_grain=pnine_float,
        money_grain=pfour_float,
    )

    # WHEN
    sue_default_gut = sue_packfilehandler.default_gut_belief()

    # THEN
    assert sue_default_gut.moment_label == sue_packfilehandler.moment_label
    assert sue_default_gut.belief_name == sue_packfilehandler.belief_name
    assert sue_default_gut.knot == sue_packfilehandler.knot
    assert sue_default_gut.fund_pool == sue_packfilehandler.fund_pool
    assert sue_default_gut.fund_grain == sue_packfilehandler.fund_grain
    assert sue_default_gut.respect_grain == sue_packfilehandler.respect_grain
    assert sue_default_gut.money_grain == sue_packfilehandler.money_grain
    assert sue_default_gut.last_pack_id == init_pack_id()


def test_PackFileHandler_create_initial_pack_files_from_default_SavesPackUnitFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    init_pack_filename = sue_packfilehandler.pack_filename(init_pack_id())
    init_pack_file_path = create_path(
        sue_packfilehandler._packs_dir, init_pack_filename
    )
    assert os_path_exists(init_pack_file_path) is False
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False

    # WHEN
    sue_packfilehandler._create_initial_pack_files_from_default()

    # THEN
    assert os_path_exists(init_pack_file_path)
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False


def test_PackFileHandler_create_gut_from_packs_CreatesgutFileFromPackFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    init_pack_filename = sue_packfilehandler.pack_filename(init_pack_id())
    init_pack_file_path = create_path(
        sue_packfilehandler._packs_dir, init_pack_filename
    )
    sue_packfilehandler._create_initial_pack_files_from_default()
    assert os_path_exists(init_pack_file_path)
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False

    # WHEN
    sue_packfilehandler._create_gut_from_packs()

    # THEN
    assert gut_file_exists(env_dir(), "amy23", sue_str)
    static_sue_gut = sue_packfilehandler._merge_any_packs(
        sue_packfilehandler.default_gut_belief()
    )
    gut_belief = open_gut_file(env_dir(), "amy23", sue_str)
    assert gut_belief.to_dict() == static_sue_gut.to_dict()


def test_PackFileHandler_create_initial_pack_and_gut_files_CreatesPackFilesAndgutFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    init_pack_filename = sue_packfilehandler.pack_filename(init_pack_id())
    init_pack_file_path = create_path(
        sue_packfilehandler._packs_dir, init_pack_filename
    )
    assert os_path_exists(init_pack_file_path) is False
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False

    # WHEN
    sue_packfilehandler._create_initial_pack_and_gut_files()

    # THEN
    assert os_path_exists(init_pack_file_path)
    assert gut_file_exists(env_dir(), "amy23", sue_str)
    static_sue_gut = sue_packfilehandler._merge_any_packs(
        sue_packfilehandler.default_gut_belief()
    )
    gut_belief = open_gut_file(env_dir(), "amy23", sue_str)
    assert gut_belief.to_dict() == static_sue_gut.to_dict()


def test_PackFileHandler_create_initial_pack_files_from_gut_SavesOnlyPackFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    sue_gut_belief = sue_packfilehandler.default_gut_belief()
    bob_str = "Bob"
    sue_gut_belief.add_voiceunit(bob_str)
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False
    save_gut_file(env_dir(), sue_gut_belief)
    assert gut_file_exists(env_dir(), "amy23", sue_str)
    init_pack_file_path = create_path(
        sue_packfilehandler._packs_dir, f"{init_pack_id()}.json"
    )
    assert os_path_exists(init_pack_file_path) is False

    # WHEN
    sue_packfilehandler._create_initial_pack_files_from_gut()

    # THEN
    assert os_path_exists(init_pack_file_path)


def test_PackFileHandler_initialize_pack_gut_files_SavesgutFileAndPackFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    seven_int = 25
    sue_packfilehandler = packfilehandler_shop(
        env_dir(), "amy23", sue_str, respect_grain=seven_int
    )
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False
    init_pack_file_path = create_path(
        sue_packfilehandler._packs_dir, f"{init_pack_id()}.json"
    )
    delete_dir(sue_packfilehandler._packs_dir)
    assert os_path_exists(init_pack_file_path) is False

    # WHEN
    sue_packfilehandler.initialize_pack_gut_files()

    # THEN
    gut_belief = open_gut_file(env_dir(), "amy23", sue_str)
    assert gut_belief.moment_label == "amy23"
    assert gut_belief.belief_name == sue_str
    assert gut_belief.respect_grain == seven_int
    assert os_path_exists(init_pack_file_path)


def test_PackFileHandler_initialize_pack_gut_files_SavesOnlygutFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    seven_int = 25
    sue_packfilehandler = packfilehandler_shop(
        env_dir(), "amy23", sue_str, respect_grain=seven_int
    )
    sue_packfilehandler.initialize_pack_gut_files()
    assert gut_file_exists(env_dir(), "amy23", sue_str)
    gut_path = create_gut_path(env_dir(), "amy23", sue_str)
    delete_dir(gut_path)
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False
    init_pack_file_path = create_path(
        sue_packfilehandler._packs_dir, f"{init_pack_id()}.json"
    )
    assert os_path_exists(init_pack_file_path)

    # WHEN
    sue_packfilehandler.initialize_pack_gut_files()

    # THEN
    gut_belief = open_gut_file(env_dir(), "amy23", sue_str)
    assert gut_belief.moment_label == "amy23"
    assert gut_belief.belief_name == sue_str
    assert gut_belief.respect_grain == seven_int
    assert os_path_exists(init_pack_file_path)


def test_PackFileHandler_initialize_pack_gut_files_SavesOnlyPackFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    seven_int = 25
    sue_packfilehandler = packfilehandler_shop(
        env_dir(), "amy23", sue_str, respect_grain=seven_int
    )
    sue_packfilehandler.initialize_pack_gut_files()
    sue_gut_belief = open_gut_file(env_dir(), "amy23", sue_str)
    bob_str = "Bob"
    sue_gut_belief.add_voiceunit(bob_str)
    save_gut_file(env_dir(), sue_gut_belief)
    assert gut_file_exists(env_dir(), "amy23", sue_str)
    init_pack_file_path = create_path(
        sue_packfilehandler._packs_dir, f"{init_pack_id()}.json"
    )
    delete_dir(sue_packfilehandler._packs_dir)
    assert os_path_exists(init_pack_file_path) is False

    # WHEN
    sue_packfilehandler.initialize_pack_gut_files()

    # THEN
    assert sue_gut_belief.moment_label == "amy23"
    assert sue_gut_belief.belief_name == sue_str
    assert sue_gut_belief.respect_grain == seven_int
    assert sue_gut_belief.voice_exists(bob_str)
    assert os_path_exists(init_pack_file_path)


def test_PackFileHandler_append_packs_to_gut_file_AddsPacksTogutFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    sue_packfilehandler.initialize_pack_gut_files()
    sue_packfilehandler.save_pack_file(sue_2beliefatoms_packunit())
    gut_belief = open_gut_file(env_dir(), "amy23", sue_str)
    # gut_belief.add_plan(gut_belief.make_l1_rope("sports"))
    sports_str = "sports"
    sports_rope = gut_belief.make_l1_rope(sports_str)
    knee_str = "knee"
    knee_rope = gut_belief.make_rope(sports_rope, knee_str)
    assert gut_belief.plan_exists(sports_rope) is False
    assert gut_belief.plan_exists(knee_rope) is False

    # WHEN
    new_belief = sue_packfilehandler.append_packs_to_gut_file()

    # THEN
    assert new_belief != gut_belief
    assert new_belief.plan_exists(sports_rope)
    assert new_belief.plan_exists(knee_rope)
