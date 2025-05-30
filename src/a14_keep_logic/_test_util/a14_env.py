from src.a00_data_toolbox.file_toolbox import delete_dir, copy_dir, create_path
from src.a01_way_logic.way import create_way_from_labels, WayStr
from src.a12_hub_tools.hubunit import hubunit_shop, HubUnit
from os.path import exists as os_path_exists
from pytest import fixture as pytest_fixture


def temp_fisc_label():
    return "ex_keep04"


def temp_fisc_mstr_dir():
    return "src\\a14_keep_logic\\_test_util\\fisc_mstr"


def get_module_temp_dir():
    return "src\\a14_keep_logic\\_test_util\\fisc_mstr\\fiscs"


def temp_owner_name():
    return "ex_owner04"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_module_temp_dir()
    delete_dir(env_dir)
    yield env_dir
    delete_dir(env_dir)


def get_texas_way() -> WayStr:
    naton_str = "nation"
    usa_str = "usa"
    texas_str = "texas"
    return create_way_from_labels([naton_str, usa_str, texas_str])


def get_texas_hubunit() -> HubUnit:
    return hubunit_shop(
        get_module_temp_dir(), temp_fisc_label(), temp_owner_name(), get_texas_way()
    )


class InvalidkeepCopyException(Exception):
    pass


def copy_evaluation_keep(src_fisc_label: str, dest_fisc_label: str):
    keeps_dir = "src\\keep\\_utils/keeps"
    new_dir = create_path(keeps_dir, dest_fisc_label)
    if os_path_exists(new_dir):
        raise InvalidkeepCopyException(
            f"Cannot copy keep to '{new_dir}' directory because '{new_dir}' exists."
        )
    src_dir = create_path(keeps_dir, src_fisc_label)
    dest_dir = create_path(keeps_dir, dest_fisc_label)
    copy_dir(src_dir=src_dir, dest_dir=dest_dir)
