from src.f00_instrument.file import delete_dir, copy_dir
from src.f01_road.road import create_road_from_ideas, RoadUnit
from src.f05_listen.hubunit import hubunit_shop, HubUnit
from os.path import exists as os_path_exists
from pytest import fixture as pytest_fixture


def temp_deal_id():
    return "ex_keep04"


def temp_deal_dir():
    return f"{temp_deals_dir()}/{temp_deal_id()}"


def temp_deals_dir():
    return "src/f06_keep/examples/deals"


def temp_owner_id():
    return "ex_owner04"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = temp_deals_dir()
    delete_dir(env_dir)
    yield env_dir
    delete_dir(env_dir)


def get_texas_road() -> RoadUnit:
    naton_str = "nation-state"
    usa_str = "usa"
    texas_str = "texas"
    return create_road_from_ideas([naton_str, usa_str, texas_str])


def get_texas_hubunit() -> HubUnit:
    return hubunit_shop(
        temp_deals_dir(), temp_deal_id(), temp_owner_id(), get_texas_road()
    )


class InvalidkeepCopyException(Exception):
    pass


def copy_evaluation_keep(src_deal_id: str, dest_deal_id: str):
    base_dir = "src/keep/examples/keeps"
    new_dir = f"{base_dir}/{dest_deal_id}"
    if os_path_exists(new_dir):
        raise InvalidkeepCopyException(
            f"Cannot copy keep to '{new_dir}' directory because '{new_dir}' exists."
        )
    # base_dir = keep_obj.hubunit.keep_dir()
    src_dir = f"{base_dir}/{src_deal_id}"
    dest_dir = f"{base_dir}/{dest_deal_id}"
    copy_dir(src_dir=src_dir, dest_dir=dest_dir)
