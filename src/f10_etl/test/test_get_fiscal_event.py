from src.f00_instrument.file import create_path, set_dir, delete_dir
from src.f10_etl.transformers import get_fiscal_events_by_dirs
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_get_fiscal_events_by_dirs_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    zia_str = "Zia"
    event3 = 3
    event7 = 7
    event9 = 9
    music23_str = "music23"
    music55_str = "music55"
    x_etl_dir = get_test_etl_dir()
    x_faces_bow_dir = create_path(x_etl_dir, "faces_bow")
    sue_dir = create_path(x_faces_bow_dir, sue_str)
    zia_dir = create_path(x_faces_bow_dir, zia_str)
    event3_dir = create_path(sue_dir, event3)
    event7_dir = create_path(zia_dir, event7)
    event9_dir = create_path(zia_dir, event9)
    e3_music23_dir = create_path(event3_dir, music23_str)
    e7_music23_dir = create_path(event7_dir, music23_str)
    e9_music23_dir = create_path(event9_dir, music23_str)
    e9_music55_dir = create_path(event9_dir, music55_str)
    set_dir(e3_music23_dir)
    set_dir(e7_music23_dir)
    set_dir(e9_music23_dir)
    set_dir(e9_music55_dir)
    print(f"{e3_music23_dir=}")
    print(f"{e7_music23_dir=}")
    print(f"{e9_music23_dir=}")
    print(f"{e9_music55_dir=}")
    assert os_path_exists(e3_music23_dir)
    assert os_path_exists(e7_music23_dir)
    assert os_path_exists(e9_music23_dir)
    assert os_path_exists(e9_music55_dir)

    # WHEN
    x_fiscal_events = get_fiscal_events_by_dirs(x_faces_bow_dir)

    # THEN
    assert x_fiscal_events == {
        music23_str: {event3, event7, event9},
        music55_str: {event9},
    }

    # WHEN
    delete_dir(e9_music55_dir)
    assert os_path_exists(e3_music23_dir)
    assert os_path_exists(e7_music23_dir)
    assert os_path_exists(e9_music23_dir)
    assert os_path_exists(e9_music55_dir) is False

    # WHEN
    x_fiscal_events = get_fiscal_events_by_dirs(x_faces_bow_dir)

    # THEN
    assert x_fiscal_events == {music23_str: {event3, event7, event9}}
