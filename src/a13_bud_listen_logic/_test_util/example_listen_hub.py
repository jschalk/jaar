from src.a01_term_logic.way import WayTerm, create_way_from_labels
from src.a05_concept_logic.concept import get_default_vow_label
from src.a12_hub_tools.hubunit import HubUnit, hubunit_shop
from src.a13_bud_listen_logic._test_util.a13_env import get_module_temp_dir


def get_texas_way() -> WayTerm:
    vow_label = get_default_vow_label()
    nation_str = "nation"
    usa_str = "USA"
    texas_str = "Texas"
    return create_way_from_labels([vow_label, nation_str, usa_str, texas_str])


def get_texas_hubunit() -> HubUnit:
    vow_label = get_default_vow_label()
    return hubunit_shop(
        get_module_temp_dir(),
        vow_label,
        owner_name="Sue",
        keep_way=get_texas_way(),
        # pipeline_duty_vision_str(),
    )


def get_dakota_way() -> WayTerm:
    vow_label = get_default_vow_label()
    nation_str = "nation"
    usa_str = "USA"
    dakota_str = "Dakota"
    return create_way_from_labels([vow_label, nation_str, usa_str, dakota_str])


def get_dakota_hubunit() -> HubUnit:
    vow_label = get_default_vow_label()
    return hubunit_shop(
        get_module_temp_dir(),
        vow_label,
        owner_name="Sue",
        keep_way=get_dakota_way(),
        # pipeline_duty_vision_str(),
    )
