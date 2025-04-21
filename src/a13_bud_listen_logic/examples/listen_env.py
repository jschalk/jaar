from src.a00_data_toolboxs.file_toolbox import delete_dir, create_path
from src.a01_word_logic.road import (
    create_road_from_tags,
    get_default_fisc_tag,
    RoadUnit,
)
from src.a12_hub_tools.hubunit import HubUnit, hubunit_shop
from pytest import fixture as pytest_fixture


def get_codespace_listen_dir() -> str:
    return "src/a13_bud_listen_logic"


def get_listen_examples_dir():
    return create_path(get_codespace_listen_dir(), "examples")


def get_listen_temp_env_dir():
    return create_path(get_listen_examples_dir(), "temp")


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_listen_temp_env_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)


def get_texas_road() -> RoadUnit:
    fisc_tag = get_default_fisc_tag()
    nation_str = "nation-state"
    usa_str = "USA"
    texas_str = "Texas"
    return create_road_from_tags([fisc_tag, nation_str, usa_str, texas_str])


def get_texas_hubunit() -> HubUnit:
    fisc_tag = get_default_fisc_tag()
    return hubunit_shop(
        get_listen_temp_env_dir(),
        fisc_tag,
        owner_name="Sue",
        keep_road=get_texas_road(),
        # pipeline_duty_plan_str(),
    )


def get_dakota_road() -> RoadUnit:
    fisc_tag = get_default_fisc_tag()
    nation_str = "nation-state"
    usa_str = "USA"
    dakota_str = "Dakota"
    return create_road_from_tags([fisc_tag, nation_str, usa_str, dakota_str])


def get_dakota_hubunit() -> HubUnit:
    fisc_tag = get_default_fisc_tag()
    return hubunit_shop(
        get_listen_temp_env_dir(),
        fisc_tag,
        owner_name="Sue",
        keep_road=get_dakota_road(),
        # pipeline_duty_plan_str(),
    )
