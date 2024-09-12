from src._instrument.file import delete_dir
from src._road.road import (
    create_road_from_nodes,
    get_default_pecun_id_roadnode,
    RoadUnit,
)
from src.hear.hubunit import HubUnit, hubunit_shop
from pytest import fixture as pytest_fixture


def get_codespace_hear_dir() -> str:
    return "src/hear"


def get_hear_examples_dir():
    return f"{get_codespace_hear_dir()}/examples"


def get_hear_temp_env_dir():
    return f"{get_hear_examples_dir()}/temp"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_hear_temp_env_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)


def get_texas_road() -> RoadUnit:
    pecun_id = get_default_pecun_id_roadnode()
    nation_str = "nation-state"
    usa_str = "USA"
    texas_str = "Texas"
    return create_road_from_nodes([pecun_id, nation_str, usa_str, texas_str])


def get_texas_hubunit() -> HubUnit:
    pecun_id = get_default_pecun_id_roadnode()
    return hubunit_shop(
        get_hear_temp_env_dir(),
        pecun_id,
        owner_id="Sue",
        econ_road=get_texas_road(),
        # pipeline_duty_job_str(),
    )


def get_dakota_road() -> RoadUnit:
    pecun_id = get_default_pecun_id_roadnode()
    nation_str = "nation-state"
    usa_str = "USA"
    dakota_str = "Dakota"
    return create_road_from_nodes([pecun_id, nation_str, usa_str, dakota_str])


def get_dakota_hubunit() -> HubUnit:
    pecun_id = get_default_pecun_id_roadnode()
    return hubunit_shop(
        get_hear_temp_env_dir(),
        pecun_id,
        owner_id="Sue",
        econ_road=get_dakota_road(),
        # pipeline_duty_job_str(),
    )
