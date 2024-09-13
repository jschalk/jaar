from src._instrument.file import delete_dir, copy_dir
from src._road.road import create_road_from_nodes, RoadUnit
from src.d_listen.hubunit import hubunit_shop, HubUnit
from os.path import exists as os_path_exists
from pytest import fixture as pytest_fixture


def temp_fiscal_id():
    return "ex_econ04"


def temp_fiscal_dir():
    return f"{temp_fiscals_dir()}/{temp_fiscal_id()}"


def temp_fiscals_dir():
    return "src/money/examples/fiscals"


def temp_owner_id():
    return "ex_owner04"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = temp_fiscals_dir()
    delete_dir(env_dir)
    yield env_dir
    delete_dir(env_dir)


def get_texas_road() -> RoadUnit:
    naton_str = "nation-state"
    usa_str = "usa"
    texas_str = "texas"
    return create_road_from_nodes([naton_str, usa_str, texas_str])


def get_texas_hubunit() -> HubUnit:
    return hubunit_shop(
        temp_fiscals_dir(), temp_fiscal_id(), temp_owner_id(), get_texas_road()
    )


# def modify_fiscal_id_example_econ(
#     econ_obj: MoneyUnit, src_hubunit: HubUnit, dst_hubunit: HubUnit, new_fiscal_id
# ):
#     src_dir = src_hubunit.econ_dir()
#     dst_dir = dst_hubunit.econ_dir()
#     os_rename(src=src_dir, dst=dst_dir)
#     econ_obj.set_fiscal_id(fiscal_id=new_fiscal_id)
#     econ_obj.econ_dir = dst_dir


class InvalideconCopyException(Exception):
    pass


def copy_evaluation_econ(src_fiscal_id: str, dest_fiscal_id: str):
    base_dir = "src/money/examples/econs"
    new_dir = f"{base_dir}/{dest_fiscal_id}"
    if os_path_exists(new_dir):
        raise InvalideconCopyException(
            f"Cannot copy econ to '{new_dir}' directory because '{new_dir}' exists."
        )
    # base_dir = econ_obj.hubunit.econ_dir()
    src_dir = f"{base_dir}/{src_fiscal_id}"
    dest_dir = f"{base_dir}/{dest_fiscal_id}"
    copy_dir(src_dir=src_dir, dest_dir=dest_dir)
