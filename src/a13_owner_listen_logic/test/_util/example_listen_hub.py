from src.a01_term_logic.rope import RopeTerm, create_rope_from_labels
from src.a05_plan_logic.plan import get_default_belief_label
from src.a12_hub_toolbox.hubunit import HubUnit, hubunit_shop
from src.a13_owner_listen_logic.test._util.a13_env import get_module_temp_dir


def get_texas_rope() -> RopeTerm:
    belief_label = get_default_belief_label()
    nation_str = "nation"
    usa_str = "USA"
    texas_str = "Texas"
    return create_rope_from_labels([belief_label, nation_str, usa_str, texas_str])


def get_texas_hubunit() -> HubUnit:
    belief_label = get_default_belief_label()
    return hubunit_shop(
        get_module_temp_dir(),
        belief_label,
        owner_name="Sue",
        keep_rope=get_texas_rope(),
        # pipeline_duty_vision_str(),
    )


def get_dakota_rope() -> RopeTerm:
    belief_label = get_default_belief_label()
    nation_str = "nation"
    usa_str = "USA"
    dakota_str = "Dakota"
    return create_rope_from_labels([belief_label, nation_str, usa_str, dakota_str])


def get_dakota_hubunit() -> HubUnit:
    belief_label = get_default_belief_label()
    return hubunit_shop(
        get_module_temp_dir(),
        belief_label,
        owner_name="Sue",
        keep_rope=get_dakota_rope(),
        # pipeline_duty_vision_str(),
    )
