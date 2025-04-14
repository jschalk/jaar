from src.f00_data_toolboxs.file_toolbox import create_path
from src.f11_etl.tran_path import (
    CART_EVENTS_FILENAME,
    CART_PIDGIN_FILENAME,
    STANCE0001_FILENAME,
    create_cart_events_path,
    create_cart_pidgin_path,
    create_otx_face_pidgin_path,
    create_otx_event_pidgin_path,
    create_stances_dir_path,
    create_stances_owner_dir_path,
    create_stance0001_path,
)
from src.f06_listen.examples.listen_env import get_listen_temp_env_dir


def test_hub_path_constants_are_values():
    # ESTABLISH / WHEN / THEN
    assert CART_EVENTS_FILENAME == "events.xlsx"
    assert CART_PIDGIN_FILENAME == "pidgin.xlsx"
    assert STANCE0001_FILENAME == "stance0001.xlsx"


def test_create_cart_events_path_ReturnObj():
    # ESTABLISH
    x_cart_dir = get_listen_temp_env_dir()

    # WHEN
    gen_cart_event_path = create_cart_events_path(x_cart_dir)

    # THEN
    expected_cart_event_path = create_path(x_cart_dir, CART_EVENTS_FILENAME)
    assert gen_cart_event_path == expected_cart_event_path


def test_create_cart_pidgin_path_ReturnObj():
    # ESTABLISH
    x_cart_dir = get_listen_temp_env_dir()

    # WHEN
    gen_cart_event_path = create_cart_pidgin_path(x_cart_dir)

    # THEN
    expected_cart_event_path = create_path(x_cart_dir, CART_PIDGIN_FILENAME)
    assert gen_cart_event_path == expected_cart_event_path


def test_create_otx_face_pidgin_path_ReturnObj():
    # ESTABLISH
    faces_otz_dir = get_listen_temp_env_dir()
    bob_str = "Bob"

    # WHEN
    gen_pidgin_path = create_otx_face_pidgin_path(faces_otz_dir, bob_str)

    # THEN
    bob_otz_path = create_path(faces_otz_dir, bob_str)
    expected_pidgin_path = create_path(bob_otz_path, CART_PIDGIN_FILENAME)
    assert gen_pidgin_path == expected_pidgin_path


def test_create_otx_event_pidgin_path_ReturnObj():
    # ESTABLISH
    faces_otz_dir = get_listen_temp_env_dir()
    bob_str = "Bob"
    event7 = 7

    # WHEN
    gen_pidgin_path = create_otx_event_pidgin_path(faces_otz_dir, bob_str, event7)

    # THEN
    bob_otz_path = create_path(faces_otz_dir, bob_str)
    event_path = create_path(bob_otz_path, event7)
    expected_pidgin_path = create_path(event_path, CART_PIDGIN_FILENAME)
    assert gen_pidgin_path == expected_pidgin_path


def test_create_stances_dir_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()

    # WHEN
    gen_bob_stance_dir = create_stances_dir_path(x_fisc_mstr_dir)

    # THEN
    expected_stances_dir = create_path(x_fisc_mstr_dir, "stances")
    assert gen_bob_stance_dir == expected_stances_dir


def test_create_stances_owner_dir_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    bob_str = "Bob"

    # WHEN
    gen_bob_stance_dir = create_stances_owner_dir_path(x_fisc_mstr_dir, bob_str)

    # THEN
    stances_dir = create_path(x_fisc_mstr_dir, "stances")
    expected_bob_stance_dir = create_path(stances_dir, bob_str)
    assert gen_bob_stance_dir == expected_bob_stance_dir


def test_create_stance0001_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()

    # WHEN
    gen_stance0001_xlsx_path = create_stance0001_path(x_fisc_mstr_dir)

    # THEN
    stances_dir = create_path(x_fisc_mstr_dir, "stances")
    expected_stance000001_path = create_path(stances_dir, STANCE0001_FILENAME)
    assert gen_stance0001_xlsx_path == expected_stance000001_path
