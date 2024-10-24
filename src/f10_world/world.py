from src.f00_instrument.dict_tool import get_empty_dict_if_none, get_0_if_None
from src.f01_road.finance_tran import TimeLinePoint, TimeConversion
from src.f01_road.road import WorldID, RoadNode, TimeLineLabel, get_default_world_id
from src.f07_fiscal.fiscal import FiscalUnit
from dataclasses import dataclass


def get_default_worlds_dir():
    return "src/f10_world/examples/worlds"


@dataclass
class WorldUnit:
    world_id: WorldID = None
    worlds_dir: str = None
    current_time: TimeLinePoint = None
    timeconversions: dict[RoadNode, TimeConversion] = None


def worldunit_shop(
    world_id: WorldID = None,
    worlds_dir: str = None,
    current_time: TimeLinePoint = None,
    timeconversions: dict[TimeLineLabel, TimeConversion] = None,
):
    if world_id is None:
        world_id = get_default_world_id()
    if worlds_dir is None:
        worlds_dir = get_default_worlds_dir()
    return WorldUnit(
        world_id=world_id,
        worlds_dir=worlds_dir,
        current_time=get_0_if_None(current_time),
        timeconversions=get_empty_dict_if_none(timeconversions),
    )


def init_fiscalunits_from_dirs(x_dirs: list[str]) -> list[FiscalUnit]:
    return []
