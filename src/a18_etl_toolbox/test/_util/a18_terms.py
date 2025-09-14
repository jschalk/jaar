from src.a17_idea_logic.test._util.a17_terms import *
from typing import Literal


def belief_net_amount_str() -> Literal["belief_net_amount"]:
    """Column name for the belief net amounts."""
    return "belief_net_amount"


def brick_agg_str() -> str:
    return "brick_agg"


def brick_raw_str() -> str:
    return "brick_raw"


def brick_valid_str() -> str:
    return "brick_valid"


def events_brick_agg_str() -> Literal["events_brick_agg"]:
    return "events_brick_agg"


def events_brick_valid_str() -> Literal["events_brick_valid"]:
    return "events_brick_valid"


def heard_agg_str() -> str:
    return "heard_agg"


def heard_raw_str() -> str:
    return "heard_raw"


def moment_event_time_agg_str() -> Literal["moment_event_time_agg"]:
    return "moment_event_time_agg"


def moment_ote1_agg_str() -> Literal["moment_ote1_agg"]:
    return "moment_ote1_agg"


def moment_voice_nets_str() -> Literal["moment_voice_nets"]:
    """Table name for the account net amounts."""
    return "moment_voice_nets"


def sound_agg_str() -> str:
    return "sound_agg"


def sound_raw_str() -> str:
    return "sound_raw"
