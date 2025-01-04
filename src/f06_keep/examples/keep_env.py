from src.f00_instrument.file import delete_dir, copy_dir
from src.f01_road.road import create_road_from_titles, RoadUnit
from src.f05_listen.hubunit import hubunit_shop, HubUnit
from os.path import exists as os_path_exists
from pytest import fixture as pytest_fixture


def temp_cmty_title():
    return "ex_keep04"


def temp_cmty_dir():
    return f"{temp_cmtys_dir()}/{temp_cmty_title()}"


def temp_cmtys_dir():
    return "src/f06_keep/examples/cmtys"


def temp_owner_name():
    return "ex_owner04"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = temp_cmtys_dir()
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
        temp_cmtys_dir(), temp_cmty_title(), temp_owner_name(), get_texas_road()
    )


class InvalidkeepCopyException(Exception):
    pass


def copy_evaluation_keep(src_cmty_title: str, dest_cmty_title: str):
    base_dir = "src/keep/examples/keeps"
    new_dir = f"{base_dir}/{dest_cmty_title}"
    if os_path_exists(new_dir):
        raise InvalidkeepCopyException(
            f"Cannot copy keep to '{new_dir}' directory because '{new_dir}' exists."
        )
    # base_dir = keep_obj.hubunit.keep_dir()
    src_dir = f"{base_dir}/{src_cmty_title}"
    dest_dir = f"{base_dir}/{dest_cmty_title}"
    copy_dir(src_dir=src_dir, dest_dir=dest_dir)
