from src.f00_instrument.file import save_file, delete_dir, create_file_path
from src.f01_road.finance_tran import timeconversion_shop
from src.f09_filter.filter import filterunit_shop
from src.f10_world.world import (
    init_fiscalunits_from_dirs,
    WorldUnit,
    worldunit_shop,
)
from src.f10_world.examples.world_env import (
    get_test_world_id,
    get_test_worlds_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists

# The goal of the world function is to allow a single command, pointing at a bunch of directories
# initialize fiscalunits and output acct metrics such as calendars, financial status, healer status


def test_WorldUnit_Exists():
    # ESTABLISH / WHEN
    x_world = WorldUnit()

    # THEN
    assert x_world.world_id is None
    assert x_world.worlds_dir is None
    assert x_world.current_time is None
    assert x_world.timeconversions is None
    assert x_world.faces is None
    assert x_world._faces_dir is None
    assert x_world._fiscalunits is None


def test_worldunit_shop_ReturnsObj_WithParameters():
    # ESTABLISH
    worlds2_dir = f"{get_test_worlds_dir()}/worlds2"
    five_world_id = "five"
    world2_current_time = 55
    music_text = "music45"
    sue_str = "Sue"
    bob_str = "Bob"
    world2_faces = {
        sue_str: filterunit_shop(sue_str),
        bob_str: filterunit_shop(bob_str),
    }
    world2timeconversions = {music_text: timeconversion_shop(music_text)}
    world2_fiscalunits = {"music45"}

    # WHEN
    x_world = worldunit_shop(
        five_world_id,
        worlds2_dir,
        world2_current_time,
        world2timeconversions,
        world2_faces,
        world2_fiscalunits,
    )

    # THEN
    assert x_world.world_id == five_world_id
    assert x_world.worlds_dir == worlds2_dir
    assert x_world.current_time == world2_current_time
    assert x_world.timeconversions == world2timeconversions
    assert x_world.faces == world2_faces
    assert x_world._faces_dir == f"{worlds2_dir}/faces"
    assert x_world._fiscalunits == world2_fiscalunits


def test_worldunit_shop_ReturnsObj_WithoutParameters():
    # ESTABLISH / WHEN
    x_world = worldunit_shop()

    # THEN
    assert x_world.world_id == get_test_world_id()
    assert x_world.worlds_dir == get_test_worlds_dir()
    assert x_world.current_time == 0
    assert x_world.timeconversions == {}
    assert x_world.faces == {}
    assert x_world._faces_dir == f"{get_test_worlds_dir()}/faces"
    assert x_world._fiscalunits == set()


def test_WorldUnit_set_face_id_SetsAttr_Scenario0():
    # ESTABLISH
    x_world = worldunit_shop()
    assert x_world.faces == {}

    # WHEN
    sue_str = "Sue"
    sue_filterunit = filterunit_shop(sue_str)
    x_world.set_face_id(sue_str, sue_filterunit)

    # THEN
    assert x_world.faces != {}
    assert x_world.faces == {sue_str: sue_filterunit}


def test_WorldUnit_set_face_id_SetsAttr_Scenario1_NoValue():
    # ESTABLISH
    x_world = worldunit_shop()
    assert x_world.faces == {}

    # WHEN
    sue_str = "Sue"
    x_world.set_face_id(sue_str)

    # THEN
    assert x_world.faces != {}
    assert x_world.faces == {sue_str: filterunit_shop(sue_str)}


def test_FilterUnit_face_id_exists_ReturnsObj():
    # ESTABLISH
    x_world = worldunit_shop()
    sue_str = "Sue"
    assert x_world.face_id_exists(sue_str) is False

    # WHEN
    x_world.set_face_id(sue_str)

    # THEN
    assert x_world.face_id_exists(sue_str)


def test_FilterUnit_get_face_id_filterunit_ReturnsObj():
    # ESTABLISH
    x_world = worldunit_shop()
    slash_str = "/"
    sue_str = "Sue"
    sue_filterunit = filterunit_shop(sue_str, slash_str)
    assert x_world.get_face_id_filterunit(sue_str) is None

    # WHEN
    x_world.set_face_id(sue_str, sue_filterunit)

    # THEN
    assert x_world.get_face_id_filterunit(sue_str) == sue_filterunit


def test_FilterUnit_del_face_id_ReturnsObj():
    # ESTABLISH
    x_world = worldunit_shop()
    sue_str = "Sue"
    bob_str = "Bob"
    sue_filterunit = filterunit_shop(sue_str)
    bob_filterunit = filterunit_shop(bob_str)
    x_world.set_face_id(sue_str, sue_filterunit)
    x_world.set_face_id(bob_str, bob_filterunit)
    assert x_world.get_face_id_filterunit(sue_str) == sue_filterunit
    assert x_world.get_face_id_filterunit(bob_str) == bob_filterunit

    # WHEN
    x_world.del_face_id(sue_str)

    # THEN
    assert x_world.get_face_id_filterunit(sue_str) is None
    assert x_world.get_face_id_filterunit(bob_str) == bob_filterunit


def test_WorldUnit_del_all_face_id_SetsAttr():
    # ESTABLISH
    x_world = worldunit_shop()
    sue_str = "Sue"
    bob_str = "Bob"
    sue_filterunit = filterunit_shop(sue_str)
    bob_filterunit = filterunit_shop(bob_str)
    x_world.set_face_id(sue_str, sue_filterunit)
    x_world.set_face_id(bob_str, bob_filterunit)
    assert x_world.get_face_id_filterunit(sue_str) == sue_filterunit
    assert x_world.get_face_id_filterunit(bob_str) == bob_filterunit

    # WHEN
    x_world.del_all_face_id()

    # THEN
    assert x_world.get_face_id_filterunit(sue_str) is None
    assert x_world.get_face_id_filterunit(bob_str) is None
    assert x_world.faces == {}


def test_WorldUnit_face_ids_empty_ReturnsObj():
    # ESTABLISH
    x_world = worldunit_shop()
    sue_str = "Sue"
    bob_str = "Bob"
    assert x_world.face_ids_empty()

    # WHEN / THEN
    x_world.set_face_id(sue_str)
    assert x_world.face_ids_empty() is False

    # WHEN / THEN
    x_world.set_face_id(bob_str)
    assert x_world.face_ids_empty() is False

    # WHEN / THEN
    x_world.del_all_face_id()
    assert x_world.face_ids_empty()


def test_WorldUnit_save_face_files_SavesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    sue_str = "Sue"
    bob_str = "Bob"
    x_world.set_face_id(sue_str)
    x_world.set_face_id(bob_str)
    sue_dir = create_file_path(x_world._faces_dir, sue_str)
    bob_dir = create_file_path(x_world._faces_dir, bob_str)
    assert os_path_exists(bob_dir) is False
    assert os_path_exists(sue_dir) is False

    # WHEN
    x_world.save_face_files(sue_str)

    # THEN
    assert os_path_exists(bob_dir) is False
    assert os_path_exists(sue_dir)


def test_WorldUnit_face_files_exist_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    sue_str = "Sue"
    bob_str = "Bob"
    x_world.set_face_id(sue_str)
    x_world.set_face_id(bob_str)
    sue_dir = create_file_path(x_world._faces_dir, sue_str)
    bob_dir = create_file_path(x_world._faces_dir, bob_str)
    assert os_path_exists(bob_dir) is False
    assert os_path_exists(sue_dir) is False
    assert x_world.face_files_exists(bob_str) is False
    assert x_world.face_files_exists(sue_str) is False

    # WHEN
    x_world.save_face_files(sue_str)

    # THEN
    assert os_path_exists(bob_dir) is False
    assert os_path_exists(sue_dir)
    assert x_world.face_files_exists(bob_str) is False
    assert x_world.face_files_exists(sue_str)


# def test_WorldUnit_open_face_from_files_ReturnsObj(env_dir_setup_cleanup):
#     # ESTABLISH
#     x_world = worldunit_shop()
#     sue_str = "Sue"
#     bob_str = "Bob"
#     x_world.set_face_id(sue_str)
#     x_world.set_face_id(bob_str)
#     sue_dir = create_file_path(x_world._faces_dir, sue_str)
#     bob_dir = create_file_path(x_world._faces_dir, bob_str)
#     assert os_path_exists(sue_dir) is False
#     assert os_path_exists(bob_dir) is False

#     # WHEN
#     x_world.save_face_files(sue_str)

#     # THEN
#     assert os_path_exists(sue_dir)
#     assert os_path_exists(bob_dir) is False


def test_WorldUnit_set_all_face_ids_from_dirs_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    x_world = worldunit_shop()
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    save_file(f"{x_world._faces_dir}/{sue_str}", "temp.txt", "")
    save_file(f"{x_world._faces_dir}/{bob_str}", "temp.txt", "")
    save_file(f"{x_world._faces_dir}/{zia_str}", "temp.txt", "")
    assert x_world.face_id_exists(sue_str) is False
    assert x_world.face_id_exists(bob_str) is False
    assert x_world.face_id_exists(zia_str) is False
    assert x_world.face_ids_empty()

    # WHEN
    x_world._set_all_face_ids_from_dirs()

    # THEN
    assert x_world.face_id_exists(sue_str)
    assert x_world.face_id_exists(bob_str)
    assert x_world.face_id_exists(zia_str)
    assert x_world.face_ids_empty() is False

    # WHEN
    delete_dir(f"{x_world._faces_dir}/{zia_str}")
    x_world._set_all_face_ids_from_dirs()

    # THEN
    assert x_world.face_id_exists(sue_str)
    assert x_world.face_id_exists(bob_str)
    assert x_world.face_id_exists(zia_str) is False
    assert x_world.face_ids_empty() is False


# def test_WorldUnit_save_face_id_elements_ChangesFiles(env_dir_setup_cleanup):
#     # ESTABLISH
#     x_world = worldunit_shop()
#     sue_str = "Sue"
#     bob_str = "Bob"
#     zia_str = "Zia"
#     save_file(f"{x_world._faces_dir}/{sue_str}", "temp.txt", "")
#     save_file(f"{x_world._faces_dir}/{bob_str}", "temp.txt", "")
#     save_file(f"{x_world._faces_dir}/{zia_str}", "temp.txt", "")
#     assert x_world.face_id_exists(sue_str) is False
#     assert x_world.face_id_exists(bob_str) is False
#     assert x_world.face_id_exists(zia_str) is False
#     assert x_world.face_ids_empty()

#     # WHEN
#     x_world._set_all_face_ids_from_dirs()

#     # THEN
#     assert x_world.face_id_exists(sue_str)
#     assert x_world.face_id_exists(bob_str)
#     assert x_world.face_id_exists(zia_str)
#     assert x_world.face_ids_empty() is False

#     # WHEN
#     delete_dir(f"{x_world._faces_dir}/{zia_str}")
#     x_world._set_all_face_ids_from_dirs()

#     # THEN
#     assert x_world.face_id_exists(sue_str)
#     assert x_world.face_id_exists(bob_str)
#     assert x_world.face_id_exists(zia_str) is False
#     assert x_world.face_ids_empty() is False


def test_init_fiscalunits_from_dirs_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    x_dir = get_test_worlds_dir()

    # WHEN
    x_fiscalunits = init_fiscalunits_from_dirs([])

    # THEN
    assert x_fiscalunits == []
