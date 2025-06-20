from os.path import exists as os_path_exists
from pytest import fixture as pytest_fixture
from src.a00_data_toolbox.file_toolbox import copy_dir, create_path, delete_dir
from src.a01_term_logic.rope import RopeTerm, create_rope_from_labels
from src.a12_hub_toolbox.hubunit import HubUnit, hubunit_shop


def temp_vow_label():
    return "ex_keep04"


def temp_vow_mstr_dir():
    return "src\\a14_keep_logic\\test\\_util\\vow_mstr"


def get_module_temp_dir():
    return "src\\a14_keep_logic\\test\\_util\\vow_mstr\\vows"


def temp_owner_name():
    return "ex_owner04"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = temp_vow_mstr_dir()
    delete_dir(env_dir)
    yield env_dir
    delete_dir(env_dir)


def get_texas_rope() -> RopeTerm:
    naton_str = "nation"
    usa_str = "usa"
    texas_str = "texas"
    return create_rope_from_labels([naton_str, usa_str, texas_str])


def get_texas_hubunit() -> HubUnit:
    return hubunit_shop(
        get_module_temp_dir(), temp_vow_label(), temp_owner_name(), get_texas_rope()
    )


class InvalidkeepCopyException(Exception):
    pass


def copy_evaluation_keep(src_vow_label: str, dest_vow_label: str):
    keeps_dir = "src\\keep\\_utils/keeps"
    new_dir = create_path(keeps_dir, dest_vow_label)
    if os_path_exists(new_dir):
        raise InvalidkeepCopyException(
            f"Cannot copy keep to '{new_dir}' directory because '{new_dir}' exists."
        )
    src_dir = create_path(keeps_dir, src_vow_label)
    dest_dir = create_path(keeps_dir, dest_vow_label)
    copy_dir(src_dir=src_dir, dest_dir=dest_dir)
