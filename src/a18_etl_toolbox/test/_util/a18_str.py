from typing import Literal


def brick_agg_str() -> str:
    return "brick_agg"


def brick_valid_str() -> str:
    return "brick_valid"


def events_brick_agg_str() -> Literal["events_brick_agg"]:
    return "events_brick_agg"


def events_brick_valid_str() -> Literal["events_brick_valid"]:
    return "events_brick_valid"


def owner_net_amount_str() -> Literal["owner_net_amount"]:
    """Column name for the owner net amounts."""
    return "owner_net_amount"


def sound_agg_str() -> str:
    return "sound_agg"


def sound_raw_str() -> str:
    return "sound_raw"


def voice_agg_str() -> str:
    return "voice_agg"


def voice_raw_str() -> str:
    return "voice_raw"


def vow_acct_nets_str() -> Literal["vow_acct_nets"]:
    """Table name for the account net amounts."""
    return "vow_acct_nets"


def vow_event_time_agg_str() -> Literal["vow_event_time_agg"]:
    return "vow_event_time_agg"
