from src.f00_instrument.file import save_file, create_path, open_file
from src.f00_instrument.dict_toolbox import get_json_from_dict, get_dict_from_json
from src.f01_road.allot import (
    allot_scale,
    _create_allot_dict,
    _allot_missing_scale,
    _get_missing_scale_list,
    allot_nested_scale,
)
from src.f01_road.examples.road_env import get_road_temp_env_dir, env_dir_setup_cleanup
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_allot_nested_scale_ReturnsObj_Scenari0_depth0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    x_dir = get_road_temp_env_dir()
    bob_str = "Bob"
    sue_str = "Sue"
    root_ledger = {bob_str: 10, sue_str: 40}
    x_filename = "ledger.json"
    save_file(x_dir, x_filename, get_json_from_dict(root_ledger))
    x_scale = 200
    x_grain = 1

    # WHEN
    nested_allot_scale = allot_nested_scale(
        x_dir=x_dir,
        src_filename=x_filename,
        scale_number=x_scale,
        grain_unit=x_grain,
        depth=0,
    )

    # THEN
    assert nested_allot_scale == {bob_str: 40, sue_str: 160}


def test_allot_nested_scale_ReturnsObj_Scenari1_depth0_NestedFilesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    x_dir = get_road_temp_env_dir()
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    root_ledger = {bob_str: 10, sue_str: 40}
    bob_ledger = {sue_str: 1, yao_str: 1}
    sue_ledger = {sue_str: 1, yao_str: 3}
    x_filename = "ledger.json"
    bob_dir = create_path(x_dir, bob_str)
    sue_dir = create_path(x_dir, sue_str)
    save_file(x_dir, x_filename, get_json_from_dict(root_ledger))
    save_file(bob_dir, x_filename, get_json_from_dict(bob_ledger))
    save_file(sue_dir, x_filename, get_json_from_dict(sue_ledger))
    x_scale = 200
    x_grain = 1

    # WHEN
    nested_allot_scale = allot_nested_scale(
        x_dir=x_dir,
        src_filename=x_filename,
        scale_number=x_scale,
        grain_unit=x_grain,
        depth=0,
    )

    # THEN
    assert nested_allot_scale == {bob_str: 40, sue_str: 160}


def test_allot_nested_scale_ReturnsObj_Scenari2_depth1_NestedFilesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    x_dir = get_road_temp_env_dir()
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    root_ledger = {bob_str: 10, sue_str: 40}
    bob_ledger = {sue_str: 1, yao_str: 1}
    sue_ledger = {sue_str: 1, yao_str: 3}
    x_filename = "ledger.json"
    bob_dir = create_path(x_dir, bob_str)
    sue_dir = create_path(x_dir, sue_str)
    save_file(x_dir, x_filename, get_json_from_dict(root_ledger))
    save_file(bob_dir, x_filename, get_json_from_dict(bob_ledger))
    save_file(sue_dir, x_filename, get_json_from_dict(sue_ledger))
    x_scale = 200
    x_grain = 1

    # WHEN
    nested_allot_scale = allot_nested_scale(
        x_dir=x_dir,
        src_filename=x_filename,
        scale_number=x_scale,
        grain_unit=x_grain,
        depth=1,
    )

    # THEN
    assert set(nested_allot_scale.keys()) == {sue_str, yao_str}
    print(set(nested_allot_scale.keys()))
    assert nested_allot_scale == {sue_str: 60, yao_str: 140}


def test_allot_nested_scale_ReturnsObj_Scenari3_depth1_NoNestedFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    x_dir = get_road_temp_env_dir()
    bob_str = "Bob"
    sue_str = "Sue"
    root_ledger = {bob_str: 10, sue_str: 40}
    x_filename = "ledger.json"
    save_file(x_dir, x_filename, get_json_from_dict(root_ledger))
    x_scale = 200
    x_grain = 1

    # WHEN
    nested_allot_scale = allot_nested_scale(
        x_dir=x_dir,
        src_filename=x_filename,
        scale_number=x_scale,
        grain_unit=x_grain,
        depth=0,
    )

    # THEN
    assert nested_allot_scale == {bob_str: 40, sue_str: 160}


def test_allot_nested_scale_ReturnsObj_Scenari4_depth1_NestedFilesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    x_dir = get_road_temp_env_dir()
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    xio_str = "Xio"
    zia_str = "Zia"
    root_ledger = {bob_str: 10, sue_str: 40}
    bob_ledger = {sue_str: 1, yao_str: 1}
    sue_ledger = {sue_str: 1, yao_str: 3}
    sue_yao_ledger = {sue_str: 1, yao_str: 1, xio_str: 3}
    bob_yao_ledger = {sue_str: 1, yao_str: 1, zia_str: 3}
    x_filename = "ledger.json"
    bob_dir = create_path(x_dir, bob_str)
    sue_dir = create_path(x_dir, sue_str)
    bob_yao_dir = create_path(bob_dir, yao_str)
    sue_yao_dir = create_path(sue_dir, yao_str)
    save_file(x_dir, x_filename, get_json_from_dict(root_ledger))
    save_file(bob_dir, x_filename, get_json_from_dict(bob_ledger))
    save_file(sue_dir, x_filename, get_json_from_dict(sue_ledger))
    save_file(bob_yao_dir, x_filename, get_json_from_dict(bob_yao_ledger))
    save_file(sue_yao_dir, x_filename, get_json_from_dict(sue_yao_ledger))
    x_scale = 200
    x_grain = 1

    # WHEN
    nested_allot_scale = allot_nested_scale(
        x_dir=x_dir,
        src_filename=x_filename,
        scale_number=x_scale,
        grain_unit=x_grain,
        depth=3,
    )

    # THEN
    assert set(nested_allot_scale.keys()) == {sue_str, yao_str, xio_str, zia_str}
    print(set(nested_allot_scale.keys()))
    assert nested_allot_scale == {sue_str: 88, yao_str: 28, xio_str: 72, zia_str: 12}


def test_allot_nested_scale_SavesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_road_temp_env_dir()
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    xio_str = "Xio"
    zia_str = "Zia"
    root_ledger = {bob_str: 10, sue_str: 40}
    bob_ledger = {sue_str: 1, yao_str: 1}
    sue_ledger = {sue_str: 1, yao_str: 3}
    sue_yao_ledger = {sue_str: 1, yao_str: 1, xio_str: 3}
    bob_yao_ledger = {sue_str: 1, yao_str: 1, zia_str: 3}
    x_filename = "ledger.json"
    bob_dir = create_path(x_dir, bob_str)
    sue_dir = create_path(x_dir, sue_str)
    bob_yao_dir = create_path(bob_dir, yao_str)
    sue_yao_dir = create_path(sue_dir, yao_str)
    save_file(x_dir, x_filename, get_json_from_dict(root_ledger))
    save_file(bob_dir, x_filename, get_json_from_dict(bob_ledger))
    save_file(sue_dir, x_filename, get_json_from_dict(sue_ledger))
    save_file(bob_yao_dir, x_filename, get_json_from_dict(bob_yao_ledger))
    save_file(sue_yao_dir, x_filename, get_json_from_dict(sue_yao_ledger))
    x_scale = 200
    x_grain = 1
    alloted_filename = "alloted.json"
    x_alloted_path = create_path(x_dir, alloted_filename)
    bob_alloted_path = create_path(bob_dir, alloted_filename)
    sue_alloted_path = create_path(sue_dir, alloted_filename)
    bob_yao_alloted_path = create_path(bob_yao_dir, alloted_filename)
    sue_yao_alloted_path = create_path(sue_yao_dir, alloted_filename)
    assert os_path_exists(x_alloted_path) is False
    assert os_path_exists(bob_alloted_path) is False
    assert os_path_exists(sue_alloted_path) is False
    assert os_path_exists(bob_yao_alloted_path) is False
    assert os_path_exists(sue_yao_alloted_path) is False

    # WHEN
    allot_nested_scale(
        x_dir=x_dir,
        src_filename=x_filename,
        scale_number=x_scale,
        grain_unit=x_grain,
        depth=3,
    )

    # THEN
    assert os_path_exists(x_alloted_path)
    assert os_path_exists(bob_alloted_path)
    assert os_path_exists(sue_alloted_path)
    assert os_path_exists(bob_yao_alloted_path)
    assert os_path_exists(sue_yao_alloted_path)
    x_alloted_dict = get_dict_from_json(open_file(x_alloted_path))
    bob_alloted_dict = get_dict_from_json(open_file(bob_alloted_path))
    sue_alloted_dict = get_dict_from_json(open_file(sue_alloted_path))
    bob_yao_alloted_dict = get_dict_from_json(open_file(bob_yao_alloted_path))
    sue_yao_alloted_dict = get_dict_from_json(open_file(sue_yao_alloted_path))

    assert x_alloted_dict == {sue_str: 160, bob_str: 40}
    assert bob_alloted_dict == {sue_str: 20, yao_str: 20}
    assert sue_alloted_dict == {sue_str: 40, yao_str: 120}
    assert bob_yao_alloted_dict == {sue_str: 4, yao_str: 4, zia_str: 12}
    assert sue_yao_alloted_dict == {sue_str: 24, yao_str: 24, xio_str: 72}
