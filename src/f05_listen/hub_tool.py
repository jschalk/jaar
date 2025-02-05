from src.f00_instrument.file import create_path
from src.f01_road.road import (
    default_bridge_if_None,
    create_road_from_titles,
    create_road,
    get_default_fiscal_title as root_title,
    OwnerName,
    TitleUnit,
)


def create_timeline_dir(
    fiscals_dir: str, fiscal_title: TitleUnit, owner_name: OwnerName
) -> str:
    fiscal_dir = create_path(fiscals_dir, fiscal_title)
    owners_dir = create_path(fiscal_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    return create_path(owner_dir, "timeline")
