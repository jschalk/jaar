from src.a00_data_toolbox.file_toolbox import create_path
from src.a18_etl_toolbox.tran_path import (
    BRICK_PIDGIN_FILENAME,
    STANCE0001_FILENAME,
    create_brick_pidgin_path,
    create_syntax_otx_pidgin_path,
    create_otx_event_pidgin_path,
    create_stances_dir_path,
    create_stances_owner_dir_path,
    create_stance0001_path,
)
from src.a18_etl_toolbox._utils.env_a18 import (
    get_module_temp_dir,
    env_dir_setup_cleanup,
)


def test_hub_path_constants_are_values():
    # ESTABLISH / WHEN / THEN
    assert BRICK_PIDGIN_FILENAME == "pidgin.xlsx"
    assert STANCE0001_FILENAME == "stance0001.xlsx"


def test_create_brick_pidgin_path_ReturnObj():
    # ESTABLISH
    x_brick_dir = get_module_temp_dir()

    # WHEN
    gen_brick_event_path = create_brick_pidgin_path(x_brick_dir)

    # THEN
    expected_brick_event_path = create_path(x_brick_dir, BRICK_PIDGIN_FILENAME)
    assert gen_brick_event_path == expected_brick_event_path


def test_create_syntax_otx_pidgin_path_ReturnObj():
    # ESTABLISH
    syntax_otz_dir = get_module_temp_dir()
    bob_str = "Bob"

    # WHEN
    gen_pidgin_path = create_syntax_otx_pidgin_path(syntax_otz_dir, bob_str)

    # THEN
    bob_otz_path = create_path(syntax_otz_dir, bob_str)
    expected_pidgin_path = create_path(bob_otz_path, BRICK_PIDGIN_FILENAME)
    assert gen_pidgin_path == expected_pidgin_path


def test_create_otx_event_pidgin_path_ReturnObj():
    # ESTABLISH
    syntax_otz_dir = get_module_temp_dir()
    bob_str = "Bob"
    event7 = 7

    # WHEN
    gen_pidgin_path = create_otx_event_pidgin_path(syntax_otz_dir, bob_str, event7)

    # THEN
    bob_otz_path = create_path(syntax_otz_dir, bob_str)
    event_path = create_path(bob_otz_path, event7)
    expected_pidgin_path = create_path(event_path, BRICK_PIDGIN_FILENAME)
    assert gen_pidgin_path == expected_pidgin_path


def test_create_stances_dir_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_module_temp_dir()

    # WHEN
    gen_bob_stance_dir = create_stances_dir_path(x_fisc_mstr_dir)

    # THEN
    expected_stances_dir = create_path(x_fisc_mstr_dir, "stances")
    assert gen_bob_stance_dir == expected_stances_dir


def test_create_stances_owner_dir_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"

    # WHEN
    gen_bob_stance_dir = create_stances_owner_dir_path(x_fisc_mstr_dir, bob_str)

    # THEN
    stances_dir = create_path(x_fisc_mstr_dir, "stances")
    expected_bob_stance_dir = create_path(stances_dir, bob_str)
    assert gen_bob_stance_dir == expected_bob_stance_dir


def test_create_stance0001_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_module_temp_dir()

    # WHEN
    gen_stance0001_xlsx_path = create_stance0001_path(x_fisc_mstr_dir)

    # THEN
    stances_dir = create_path(x_fisc_mstr_dir, "stances")
    expected_stance000001_path = create_path(stances_dir, STANCE0001_FILENAME)
    assert gen_stance0001_xlsx_path == expected_stance000001_path
