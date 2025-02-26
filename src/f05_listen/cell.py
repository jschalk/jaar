from src.f00_instrument.dict_toolbox import (
    get_empty_list_if_None,
    get_empty_dict_if_None,
    get_0_if_None,
    get_1_if_None,
)
from src.f01_road.finance import PennyNum
from src.f01_road.road import OwnerName, EventInt, RoadUnit
from src.f02_bud.reason_item import (
    FactUnit,
    factunits_get_from_dict,
    get_dict_from_factunits,
)
from src.f02_bud.bud import (
    BudUnit,
    budunit_shop,
    get_from_dict as budunit_get_from_dict,
)
from src.f02_bud.bud_tool import get_bud_root_facts_dict
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
    budevent_facts: dict[RoadUnit, FactUnit] = None
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
            "budevent_facts": get_dict_from_factunits(self.budevent_facts),
            "found_facts": get_dict_from_factunits(self.found_facts),
            "boss_facts": get_dict_from_factunits(self.boss_facts),
        }


def cellunit_shop(
    ancestors: list[OwnerName] = None,
    event_int: EventInt = None,
    celldepth: int = None,
    deal_owner_name: OwnerName = None,
    penny: PennyNum = None,
    quota: float = None,
    budadjust: BudUnit = None,
    budevent_facts: dict[RoadUnit, FactUnit] = None,
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
        budadjust=budadjust,
        budevent_facts=get_empty_dict_if_None(budevent_facts),
        found_facts=get_empty_dict_if_None(found_facts),
        boss_facts=get_empty_dict_if_None(boss_facts),
    )
