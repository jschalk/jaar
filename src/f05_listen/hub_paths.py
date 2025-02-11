from src.f00_instrument.file import create_path
from src.f01_road.road import OwnerName, TitleUnit


def create_fisc_json_path(fisc_mstr_dir: str, fisc_title: str) -> str:
    fiscs_path = create_path(fisc_mstr_dir, "fiscs")
    fisc_path = create_path(fiscs_path, fisc_title)
    return create_path(fisc_path, "fisc.json")


def create_fisc_owner_time_csv_path(fisc_mstr_dir: str, fisc_title: str):
    fiscs_path = create_path(fisc_mstr_dir, "fiscs")
    fisc_path = create_path(fiscs_path, fisc_title)
    return create_path(fisc_path, "fisc_owner_time_agg.csv")


def create_fisc_owner_time_json_path(fisc_mstr_dir: str, fisc_title: str):
    fiscs_path = create_path(fisc_mstr_dir, "fiscs")
    fisc_path = create_path(fiscs_path, fisc_title)
    return create_path(fisc_path, "fisc_owner_time_agg.json")


def fisc_agenda_list_report_path(fisc_mstr_dir: str, fisc_title: str) -> str:
    fiscs_path = create_path(fisc_mstr_dir, "fiscs")
    fisc_path = create_path(fiscs_path, fisc_title)
    return create_path(fisc_path, "agenda_full_listing.csv")


def create_timeline_dir_path(
    fiscs_dir: str, fisc_title: TitleUnit, owner_name: OwnerName
) -> str:
    fisc_dir = create_path(fiscs_dir, fisc_title)
    owners_dir = create_path(fisc_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    return create_path(owner_dir, "timeline")


def create_timepoint_dir_path(
    fiscs_dir: str, fisc_title: TitleUnit, owner_name: OwnerName, timepoint_int: int
):
    timeline_dir = create_timeline_dir_path(fiscs_dir, fisc_title, owner_name)
    return create_path(timeline_dir, timepoint_int)


def create_deal_path(
    fiscs_dir: str, fisc_title: TitleUnit, owner_name: OwnerName, timepoint_int: int
) -> str:
    timepoint_dir = create_timepoint_dir_path(
        fiscs_dir, fisc_title, owner_name, timepoint_int
    )
    return create_path(timepoint_dir, "deal.json")


def create_budpoint_dir_path(
    fiscs_dir: str, fisc_title: TitleUnit, owner_name: OwnerName, timepoint_int: int
) -> str:
    timepoint_dir = create_timepoint_dir_path(
        fiscs_dir, fisc_title, owner_name, timepoint_int
    )
    return create_path(timepoint_dir, "budpoint.json")


def create_events_owner_dir_path(
    fiscs_dir: str, fisc_title: TitleUnit, owner_name: OwnerName, event_int: int
):
    fisc_dir = create_path(fiscs_dir, fisc_title)
    fisc_events_dir = create_path(fisc_dir, "events")
    fisc_events_owner_dir = create_path(fisc_events_dir, owner_name)
    return create_path(fisc_events_owner_dir, event_int)


def create_voice_path(fiscs_dir: str, fisc_title: TitleUnit, owner_name: OwnerName):
    fisc_dir = create_path(fiscs_dir, fisc_title)
    owners_dir = create_path(fisc_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    voice_dir = create_path(owner_dir, "voice")
    return create_path(voice_dir, f"{owner_name}.json")


def create_forecast_path(fiscs_dir: str, fisc_title: TitleUnit, owner_name: OwnerName):
    fisc_dir = create_path(fiscs_dir, fisc_title)
    owners_dir = create_path(fisc_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    forecast_dir = create_path(owner_dir, "forecast")
    return create_path(forecast_dir, f"{owner_name}.json")
