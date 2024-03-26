from src._road.road import default_road_delimiter_if_none, create_road
from src.instrument.file import delete_dir
from os import path as os_path
from src.econ.econ import (
    EconUnit,
    econunit_shop,
    get_temp_env_person_id,
    get_temp_env_problem_id,
    get_temp_env_healer_id,
    get_temp_env_econ_id,
)
from src.econ.examples.econ_env_kit import (
    get_test_econ_dir,
    change_econ_id_example_econ,
    copy_evaluation_econ,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_EconUnit_exists():
    # GIVEN
    x_econ_id = "test1"

    # WHEN
    x_econ = EconUnit(x_econ_id, econ_dir=get_test_econ_dir())

    # THEN
    assert x_econ.econ_id == x_econ_id
    assert x_econ.econ_dir == get_test_econ_dir()
    assert x_econ._manager_person_id is None
    assert x_econ._road_delimiter is None


def test_EconUnit_set_econ_id_CorrectlySetsAttr():
    # GIVEN
    x_econunit = EconUnit()
    assert x_econunit.econ_id is None

    # WHEN
    texas_text = "texas"
    x_econunit.set_econ_id(texas_text)

    # THEN
    assert x_econunit.econ_id == texas_text


def test_econunit_shop_ReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    x_econ_id = get_temp_env_econ_id()
    econ_dir = f"src/econ/examples/econs/{x_econ_id}"
    sue_text = "Sue"
    assert os_path.exists(econ_dir) is False
    knee_text = "knee"
    zia_text = "knee"

    # WHEN
    x_econ = econunit_shop(
        econ_id=x_econ_id,
        econ_dir=get_test_econ_dir(),
        _manager_person_id=sue_text,
    )

    # THEN
    assert x_econ != None
    assert x_econ.econ_id == x_econ_id
    assert os_path.exists(econ_dir)
    assert x_econ._treasury_db != None
    assert x_econ._manager_person_id == sue_text
    assert x_econ._clerkunits == {}
    assert x_econ._road_delimiter == default_road_delimiter_if_none()


def test_econunit_shop_ReturnsObj_WithTempNames(env_dir_setup_cleanup):
    # GIVEN
    x_econ_id = get_temp_env_econ_id()
    # assert os_path.exists(econ_dir) is False

    # WHEN
    x_econ = econunit_shop(econ_id=x_econ_id, econ_dir=get_test_econ_dir())

    # THEN
    assert x_econ != None
    assert x_econ.econ_id == x_econ_id
    # assert os_path.exists(econ_dir)
    assert x_econ._treasury_db != None
    assert x_econ._manager_person_id == get_temp_env_person_id()
    assert x_econ._clerkunits == {}
    assert x_econ._road_delimiter == default_road_delimiter_if_none()


def test_econunit_shop_RaisesErrorIfParameterContains_road_delimiter():
    # GIVEN
    slash_text = "/"
    texas_text = f"Texas{slash_text}Arkansas"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        econunit_shop(econ_id=texas_text, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{texas_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_EconUnit_set_road_delimiter_CorrectSetsAttribute(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_econ_id = get_temp_env_econ_id()
    econ_dir = f"src/econ/examples/econs/{x_econ_id}"
    sue_text = "Sue"
    x_econ = econunit_shop(x_econ_id, get_test_econ_dir(), _manager_person_id=sue_text)
    assert x_econ._road_delimiter == default_road_delimiter_if_none()

    # WHEN
    slash_text = "/"
    x_econ.set_road_delimiter(slash_text)

    # THEN
    assert x_econ._road_delimiter == slash_text


def test_EconUnit_set_econ_dirs_CreatesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create econ
    x_econ_id = get_temp_env_econ_id()
    x_econ = EconUnit(x_econ_id, econ_dir=get_test_econ_dir())
    print(f"{get_test_econ_dir()=} {x_econ.econ_dir=}")
    # delete_dir(x_econ.get_object_root_dir())
    print(f"delete {x_econ.get_object_root_dir()=}")
    econ_dir = f"src/econ/examples/econs/{x_econ_id}"
    econ_file_name = "econ.json"
    econ_file_path = f"{econ_dir}/{econ_file_name}"
    forum_text = "forum"
    forum_dir = f"{econ_dir}/{forum_text}"
    clerkunits_dir = f"{econ_dir}/clerkunits"
    treasury_file_name = "treasury.db"
    treasury_file_path = f"{econ_dir}/{treasury_file_name}"

    assert os_path.exists(econ_dir) is False
    assert os_path.isdir(econ_dir) is False
    assert os_path.exists(econ_file_path) is False
    assert os_path.exists(forum_dir) is False
    assert os_path.exists(clerkunits_dir) is False
    assert os_path.exists(treasury_file_path) is False

    # WHEN
    x_econ.set_econ_dirs(in_memory_treasury=False)

    # THEN check agendas src directory created
    assert os_path.exists(econ_dir)
    assert os_path.isdir(econ_dir)
    assert os_path.exists(econ_file_path)
    assert os_path.exists(forum_dir)
    assert os_path.exists(clerkunits_dir)
    assert os_path.exists(treasury_file_path)
    assert x_econ.get_object_root_dir() == econ_dir
    assert x_econ.get_forum_dir() == forum_dir
    assert x_econ.get_clerkunits_dir() == clerkunits_dir
    assert x_econ.get_treasury_db_path() == treasury_file_path


def test_change_econ_id_example_econ_CorrectlyChangesDirAndFiles(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    old_x_econ_id = get_temp_env_econ_id()
    old_econ_dir = f"src/econ/examples/econs/{old_x_econ_id}"
    old_econ_file_name = "econ.json"
    old_econ_file_path = f"{old_econ_dir}/{old_econ_file_name}"
    forum_text = "forum"
    old_forum_dir = f"{old_econ_dir}/{forum_text}"
    old_clerkunits_dir = f"{old_econ_dir}/clerkunits"

    new_x_econ_id = "ex_env1"
    new_econ_dir = f"src/econ/examples/econs/{new_x_econ_id}"
    new_econ_file_name = "econ.json"
    new_econ_file_path = f"{new_econ_dir}/{new_econ_file_name}"
    forum_text = "forum"
    new_forum_dir = f"{new_econ_dir}/{forum_text}"
    new_clerkunits_dir = f"{new_econ_dir}/clerkunits"
    delete_dir(dir=new_econ_dir)
    print(f"{new_econ_dir=}")

    x_econ = econunit_shop(econ_id=old_x_econ_id, econ_dir=get_test_econ_dir())
    # delete_dir(x_econ.get_object_root_dir())
    # print(f"{x_econ.get_object_root_dir()=}")

    x_econ.set_econ_dirs(in_memory_treasury=True)

    assert os_path.exists(old_econ_dir)
    assert os_path.isdir(old_econ_dir)
    assert os_path.exists(old_econ_file_path)
    assert os_path.exists(old_forum_dir)
    assert os_path.exists(old_clerkunits_dir)
    assert x_econ.get_forum_dir() == old_forum_dir
    assert x_econ.get_clerkunits_dir() == old_clerkunits_dir

    assert os_path.exists(new_econ_dir) is False
    assert os_path.isdir(new_econ_dir) is False
    assert os_path.exists(new_econ_file_path) is False
    assert os_path.exists(new_forum_dir) is False
    assert os_path.exists(new_clerkunits_dir) is False
    assert x_econ.get_forum_dir() != new_forum_dir
    assert x_econ.get_clerkunits_dir() != new_clerkunits_dir
    assert x_econ.econ_id != new_x_econ_id

    # WHEN
    print(f"{new_x_econ_id=} {old_x_econ_id=}")
    change_econ_id_example_econ(econ_obj=x_econ, new_econ_id=new_x_econ_id)

    # THEN check agendas src directory created
    assert os_path.exists(old_econ_dir) is False
    assert os_path.isdir(old_econ_dir) is False
    assert os_path.exists(old_econ_file_path) is False
    assert os_path.exists(old_forum_dir) is False
    assert os_path.exists(old_clerkunits_dir) is False
    assert x_econ.econ_id == new_x_econ_id
    print(f"{x_econ.get_forum_dir()=}")
    print(f"           {old_forum_dir=}")
    assert x_econ.get_forum_dir() != old_forum_dir
    assert x_econ.get_clerkunits_dir() != old_clerkunits_dir

    assert os_path.exists(new_econ_dir)
    assert os_path.isdir(new_econ_dir)
    assert os_path.exists(new_econ_file_path)
    assert os_path.exists(new_forum_dir)
    assert os_path.exists(new_clerkunits_dir)
    assert x_econ.get_forum_dir() == new_forum_dir
    assert x_econ.get_clerkunits_dir() == new_clerkunits_dir

    # Undo change to directory
    # delete_dir(dir=old_econ_dir)
    # print(f"{old_econ_dir=}")
    delete_dir(dir=new_econ_dir)
    print(f"{new_econ_dir=}")


def test_copy_evaluation_econ_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create econ
    old_x_econ_id = get_temp_env_econ_id()
    old_econ_dir = f"src/econ/examples/econs/{old_x_econ_id}"
    old_econ_file_name = "econ.json"
    old_econ_file_path = f"{old_econ_dir}/{old_econ_file_name}"
    forum_text = "forum"
    old_forum_dir = f"{old_econ_dir}/{forum_text}"
    old_clerkunits_dir = f"{old_econ_dir}/clerkunits"

    x_econ = econunit_shop(old_x_econ_id, get_test_econ_dir())
    x_econ.set_econ_dirs()

    assert os_path.exists(old_econ_dir)
    assert os_path.isdir(old_econ_dir)
    assert os_path.exists(old_econ_file_path)
    assert os_path.exists(old_forum_dir)
    assert os_path.exists(old_clerkunits_dir)
    assert x_econ.get_forum_dir() == old_forum_dir
    assert x_econ.get_clerkunits_dir() == old_clerkunits_dir

    new_x_econ_id = "ex_env1"
    new_econ_dir = f"src/econ/examples/econs/{new_x_econ_id}"
    new_econ_file_name = "econ.json"
    new_econ_file_path = f"{new_econ_dir}/{new_econ_file_name}"
    new_forum_dir = f"{new_econ_dir}/{forum_text}"
    new_clerkunits_dir = f"{new_econ_dir}/clerkunits"

    assert os_path.exists(new_econ_dir) is False
    assert os_path.isdir(new_econ_dir) is False
    assert os_path.exists(new_econ_file_path) is False
    assert os_path.exists(new_forum_dir) is False
    assert os_path.exists(new_clerkunits_dir) is False
    assert x_econ.get_forum_dir() != new_forum_dir
    assert x_econ.get_clerkunits_dir() != new_clerkunits_dir
    assert x_econ.econ_id != new_x_econ_id

    # WHEN
    copy_evaluation_econ(src_econ_id=x_econ.econ_id, dest_econ_id=new_x_econ_id)

    # THEN check agendas src directory created
    assert os_path.exists(old_econ_dir)
    assert os_path.isdir(old_econ_dir)
    assert os_path.exists(old_econ_file_path)
    assert os_path.exists(old_forum_dir)
    assert os_path.exists(old_clerkunits_dir)
    assert x_econ.get_forum_dir() == old_forum_dir
    assert x_econ.get_clerkunits_dir() == old_clerkunits_dir

    assert os_path.exists(new_econ_dir)
    assert os_path.isdir(new_econ_dir)
    assert os_path.exists(new_econ_file_path)
    assert os_path.exists(new_forum_dir)
    assert os_path.exists(new_clerkunits_dir)
    assert x_econ.get_forum_dir() != new_forum_dir
    assert x_econ.get_clerkunits_dir() != new_clerkunits_dir
    assert x_econ.econ_id != new_x_econ_id

    # Undo change to directory
    # delete_dir(x_econ.get_object_root_dir())
    # delete_dir(dir=old_econ_dir)
    delete_dir(dir=new_econ_dir)


def test_copy_evaluation_econ_CorrectlyRaisesError(env_dir_setup_cleanup):
    # GIVEN create econ
    old_x_econ_id = get_temp_env_econ_id()
    x_econ = econunit_shop(old_x_econ_id, get_test_econ_dir())
    x_econ.set_econ_dirs()

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        copy_evaluation_econ(src_econ_id=x_econ.econ_id, dest_econ_id=old_x_econ_id)
    assert (
        str(excinfo.value)
        == f"Cannot copy econ to '{x_econ.get_object_root_dir()}' directory because '{x_econ.get_object_root_dir()}' exists."
    )


def test_EconUnit_get_road_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    x_econ_id = get_temp_env_econ_id()
    x_econ = econunit_shop(x_econ_id, econ_dir=get_test_econ_dir())
    bob_text = "Bob"
    econ_road_with_woot = create_road(x_econ.econ_id, bob_text)
    econ_road_wo_root = bob_text
    # healer_list_wo_root = get_all_road_nodes(econ_road_wo_root)
    bloomers_text = "bloomers"
    bloomers_road_with_root = create_road(econ_road_with_woot, bloomers_text)
    bloomers_road_wo_root = create_road(econ_road_wo_root, bloomers_text)
    # bloomers_list_wo_root = get_all_road_nodes(bloomers_road_wo_root)
    roses_text = "roses"
    roses_road_with_root = create_road(bloomers_road_with_root, roses_text)
    roses_road_wo_root = create_road(bloomers_road_wo_root, roses_text)
    # roses_list_wo_root = get_all_road_nodes(roses_road_wo_root)

    # WHEN / THEN
    assert x_econ.econ_id == x_econ.build_econ_road()
    assert econ_road_with_woot == x_econ.build_econ_road(econ_road_wo_root)
    assert bloomers_road_with_root == x_econ.build_econ_road(bloomers_road_wo_root)
    assert roses_road_with_root == x_econ.build_econ_road(roses_road_wo_root)
