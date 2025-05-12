from src.a01_way_logic.way import (
    create_way_from_tags,
    get_default_fisc_tag,
    WayStr,
)
from src.a12_hub_tools.hubunit import HubUnit, hubunit_shop
from src.a13_bud_listen_logic._utils.env_a13 import get_module_temp_dir


def get_texas_way() -> WayStr:
    fisc_tag = get_default_fisc_tag()
    nation_str = "nation-state"
    usa_str = "USA"
    texas_str = "Texas"
    return create_way_from_tags([fisc_tag, nation_str, usa_str, texas_str])


def get_texas_hubunit() -> HubUnit:
    fisc_tag = get_default_fisc_tag()
    return hubunit_shop(
        get_module_temp_dir(),
        fisc_tag,
        owner_name="Sue",
        keep_way=get_texas_way(),
        # pipeline_duty_plan_str(),
    )


def get_dakota_way() -> WayStr:
    fisc_tag = get_default_fisc_tag()
    nation_str = "nation-state"
    usa_str = "USA"
    dakota_str = "Dakota"
    return create_way_from_tags([fisc_tag, nation_str, usa_str, dakota_str])


def get_dakota_hubunit() -> HubUnit:
    fisc_tag = get_default_fisc_tag()
    return hubunit_shop(
        get_module_temp_dir(),
        fisc_tag,
        owner_name="Sue",
        keep_way=get_dakota_way(),
        # pipeline_duty_plan_str(),
    )
