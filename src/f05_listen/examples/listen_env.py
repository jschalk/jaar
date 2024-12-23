from src.f00_instrument.file import delete_dir
from src.f01_road.road import (
    create_road_from_ideas,
    get_default_fiscal_id_ideaunit,
    RoadUnit,
)
from src.f05_listen.hubunit import HubUnit, hubunit_shop
from pytest import fixture as pytest_fixture


def get_codespace_listen_dir() -> str:
    return "src/f05_listen"


def get_listen_examples_dir():
    return f"{get_codespace_listen_dir()}/examples"


def get_listen_temp_env_dir():
    return f"{get_listen_examples_dir()}/temp"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_listen_temp_env_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)


def get_texas_road() -> RoadUnit:
    fiscal_id = get_default_fiscal_id_ideaunit()
    nation_str = "nation-state"
    usa_str = "USA"
    texas_str = "Texas"
    return create_road_from_ideas([fiscal_id, nation_str, usa_str, texas_str])


def get_texas_hubunit() -> HubUnit:
    fiscal_id = get_default_fiscal_id_ideaunit()
    return hubunit_shop(
        get_listen_temp_env_dir(),
        fiscal_id,
        owner_id="Sue",
        keep_road=get_texas_road(),
        # pipeline_duty_job_str(),
    )


def get_dakota_road() -> RoadUnit:
    fiscal_id = get_default_fiscal_id_ideaunit()
    nation_str = "nation-state"
    usa_str = "USA"
    dakota_str = "Dakota"
    return create_road_from_ideas([fiscal_id, nation_str, usa_str, dakota_str])


def get_dakota_hubunit() -> HubUnit:
    fiscal_id = get_default_fiscal_id_ideaunit()
    return hubunit_shop(
        get_listen_temp_env_dir(),
        fiscal_id,
        owner_id="Sue",
        keep_road=get_dakota_road(),
        # pipeline_duty_job_str(),
    )
