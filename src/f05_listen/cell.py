from src.f00_instrument.dict_toolbox import (
    get_empty_list_if_None,
    get_0_if_None,
    get_1_if_None,
)
from src.f01_road.finance import PennyNum
from src.f01_road.road import OwnerName, EventInt, RoadUnit
from src.f02_bud.reason_item import FactUnit
from src.f02_bud.bud import (
    BudUnit,
    budunit_shop,
    get_from_dict as budunit_get_from_dict,
)
from dataclasses import dataclass

CELL_NODE_QUOTA_DEFAULT = 1000


@dataclass
class CellUnit:
    ancestors: list[OwnerName] = None
    event_int: EventInt = None
    celldepth: int = None
    deal_owner_name: OwnerName = None
    penny: PennyNum = None
    quota: float = None
    budadjust: BudUnit = None
    found_facts: dict[RoadUnit, FactUnit] = None
    boss_facts: dict[RoadUnit, FactUnit] = None

    def get_dict(self) -> dict[str]:
        return {
            "ancestors": self.ancestors,
            "event_int": self.event_int,
            "celldepth": self.celldepth,
            "deal_owner_name": self.deal_owner_name,
            "penny": self.penny,
            "quota": self.quota,
            "budadjust": self.budadjust,
            "found_facts": self.found_facts,
            "boss_facts": self.boss_facts,
        }


def cellunit_shop(
    ancestors: list[OwnerName] = None,
    event_int: EventInt = None,
    celldepth: int = None,
    deal_owner_name: OwnerName = None,
    penny: PennyNum = None,
    quota: float = None,
    budadjust: BudUnit = None,
    found_facts: dict[RoadUnit, FactUnit] = None,
    boss_facts: dict[RoadUnit, FactUnit] = None,
) -> CellUnit:
    if quota is None:
        quota = CELL_NODE_QUOTA_DEFAULT
    return CellUnit(
        ancestors=get_empty_list_if_None(ancestors),
        event_int=event_int,
        celldepth=get_0_if_None(celldepth),
        deal_owner_name=deal_owner_name,
        penny=get_1_if_None(penny),
        quota=quota,
    )
