from src.a17_idea_logic.test._util.a17_str import error_message_str
from typing import Literal


def believer_net_amount_str() -> Literal["believer_net_amount"]:
    """Column name for the believer net amounts."""
    return "believer_net_amount"


def brick_agg_str() -> str:
    return "brick_agg"


def brick_raw_str() -> str:
    return "brick_raw"


def brick_valid_str() -> str:
    return "brick_valid"


def coin_event_time_agg_str() -> Literal["coin_event_time_agg"]:
    return "coin_event_time_agg"


def coin_ote1_agg_str() -> Literal["coin_ote1_agg"]:
    return "coin_ote1_agg"


def coin_partner_nets_str() -> Literal["coin_partner_nets"]:
    """Table name for the account net amounts."""
    return "coin_partner_nets"


def events_brick_agg_str() -> Literal["events_brick_agg"]:
    return "events_brick_agg"


def events_brick_valid_str() -> Literal["events_brick_valid"]:
    return "events_brick_valid"


def sound_agg_str() -> str:
    return "sound_agg"


def sound_raw_str() -> str:
    return "sound_raw"


def voice_agg_str() -> str:
    return "voice_agg"


def voice_raw_str() -> str:
    return "voice_raw"
