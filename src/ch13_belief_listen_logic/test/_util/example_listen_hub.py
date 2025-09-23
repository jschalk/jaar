from src.ch02_rope_logic.rope import RopeTerm, create_rope_from_labels
from src.ch06_plan_logic.plan import get_default_moment_label
from src.ch12_hub_toolbox.hubunit import HubUnit, hubunit_shop
from src.ch13_belief_listen_logic.test._util.ch13_env import get_chapter_temp_dir


def get_texas_rope() -> RopeTerm:
    moment_label = get_default_moment_label()
    nation_str = "nation"
    usa_str = "USA"
    texas_str = "Texas"
    return create_rope_from_labels([moment_label, nation_str, usa_str, texas_str])


def get_texas_hubunit() -> HubUnit:
    moment_label = get_default_moment_label()
    return hubunit_shop(
        get_chapter_temp_dir(),
        moment_label,
        belief_name="Sue",
        keep_rope=get_texas_rope(),
        # pipeline_duty_vision_str(),
    )


def get_dakota_rope() -> RopeTerm:
    moment_label = get_default_moment_label()
    nation_str = "nation"
    usa_str = "USA"
    dakota_str = "Dakota"
    return create_rope_from_labels([moment_label, nation_str, usa_str, dakota_str])


def get_dakota_hubunit() -> HubUnit:
    moment_label = get_default_moment_label()
    return hubunit_shop(
        get_chapter_temp_dir(),
        moment_label,
        belief_name="Sue",
        keep_rope=get_dakota_rope(),
        # pipeline_duty_vision_str(),
    )
