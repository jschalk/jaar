from src.a00_data_toolboxs.file_toolbox import delete_dir, copy_dir, create_path
from src.a01_word_logic.road import create_road_from_titles, RoadUnit
from src.a12_hub_tools.hubunit import hubunit_shop, HubUnit
from os.path import exists as os_path_exists
from pytest import fixture as pytest_fixture


def temp_fisc_title():
    return "ex_keep04"


def temp_fisc_dir():
    return create_path(temp_fiscs_dir(), temp_fisc_title())


def temp_fisc_mstr_dir():
    return "src/a14_keep_logic/examples/fisc_mstr"


def temp_fiscs_dir():
    return "src/a14_keep_logic/examples/fisc_mstr/fiscs"


def temp_owner_name():
    return "ex_owner04"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = temp_fiscs_dir()
    delete_dir(env_dir)
    yield env_dir
    delete_dir(env_dir)


def get_texas_road() -> RoadUnit:
    naton_str = "nation-state"
    usa_str = "usa"
    texas_str = "texas"
    return create_road_from_titles([naton_str, usa_str, texas_str])


def get_texas_hubunit() -> HubUnit:
    return hubunit_shop(
        temp_fiscs_dir(), temp_fisc_title(), temp_owner_name(), get_texas_road()
    )


class InvalidkeepCopyException(Exception):
    pass


def copy_evaluation_keep(src_fisc_title: str, dest_fisc_title: str):
    base_dir = "src/keep/examples/keeps"
    new_dir = create_path(base_dir, dest_fisc_title)
    if os_path_exists(new_dir):
        raise InvalidkeepCopyException(
            f"Cannot copy keep to '{new_dir}' directory because '{new_dir}' exists."
        )
    # base_dir = keep_obj.hubunit.keep_dir()
    src_dir = create_path(base_dir, src_fisc_title)
    dest_dir = create_path(base_dir, dest_fisc_title)
    copy_dir(src_dir=src_dir, dest_dir=dest_dir)
