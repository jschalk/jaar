from src.a01_term_logic.way import (
    create_way_from_labels,
    get_default_fisc_label,
    WayTerm,
)
from src.a12_hub_tools.hubunit import HubUnit, hubunit_shop
from src.a13_bud_listen_logic._test_util.a13_env import get_module_temp_dir


def get_texas_way() -> WayTerm:
    fisc_label = get_default_fisc_label()
    nation_str = "nation"
    usa_str = "USA"
    texas_str = "Texas"
    return create_way_from_labels([fisc_label, nation_str, usa_str, texas_str])


def get_texas_hubunit() -> HubUnit:
    fisc_label = get_default_fisc_label()
    return hubunit_shop(
        get_module_temp_dir(),
        fisc_label,
        owner_name="Sue",
        keep_way=get_texas_way(),
        # pipeline_duty_plan_str(),
    )


def get_dakota_way() -> WayTerm:
    fisc_label = get_default_fisc_label()
    nation_str = "nation"
    usa_str = "USA"
    dakota_str = "Dakota"
    return create_way_from_labels([fisc_label, nation_str, usa_str, dakota_str])


def get_dakota_hubunit() -> HubUnit:
    fisc_label = get_default_fisc_label()
    return hubunit_shop(
        get_module_temp_dir(),
        fisc_label,
        owner_name="Sue",
        keep_way=get_dakota_way(),
        # pipeline_duty_plan_str(),
    )
