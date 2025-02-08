from src.f00_instrument.file import create_path
from src.f01_road.road import OwnerName, TitleUnit


def create_timeline_dir_path(
    fiscals_dir: str, fiscal_title: TitleUnit, owner_name: OwnerName
) -> str:
    fiscal_dir = create_path(fiscals_dir, fiscal_title)
    owners_dir = create_path(fiscal_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    return create_path(owner_dir, "timeline")


def create_timepoint_dir_path(
    fiscals_dir: str, fiscal_title: TitleUnit, owner_name: OwnerName, timepoint_int: int
):
    timeline_dir = create_timeline_dir_path(fiscals_dir, fiscal_title, owner_name)
    return create_path(timeline_dir, timepoint_int)


def create_deal_path(
    fiscals_dir: str, fiscal_title: TitleUnit, owner_name: OwnerName, timepoint_int: int
) -> str:
    timepoint_dir = create_timepoint_dir_path(
        fiscals_dir, fiscal_title, owner_name, timepoint_int
    )
    return create_path(timepoint_dir, "deal.json")


def create_budpoint_dir_path(
    fiscals_dir: str, fiscal_title: TitleUnit, owner_name: OwnerName, timepoint_int: int
) -> str:
    timepoint_dir = create_timepoint_dir_path(
        fiscals_dir, fiscal_title, owner_name, timepoint_int
    )
    return create_path(timepoint_dir, "budpoint.json")


def create_events_owner_dir_path(
    fiscals_dir: str, fiscal_title: TitleUnit, owner_name: OwnerName, event_int: int
):
    fiscal_dir = create_path(fiscals_dir, fiscal_title)
    fiscal_events_dir = create_path(fiscal_dir, "events")
    fiscal_events_owner_dir = create_path(fiscal_events_dir, owner_name)
    return create_path(fiscal_events_owner_dir, event_int)


def create_voice_path(fiscals_dir: str, fiscal_title: TitleUnit, owner_name: OwnerName):
    fiscal_dir = create_path(fiscals_dir, fiscal_title)
    owners_dir = create_path(fiscal_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    voice_dir = create_path(owner_dir, "voice")
    return create_path(voice_dir, f"{owner_name}.json")
