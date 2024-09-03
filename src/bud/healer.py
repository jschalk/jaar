from src._instrument.python_tool import get_empty_set_if_none
from src._road.road import GroupID
from dataclasses import dataclass


@dataclass
class HealerHold:
    _healer_ids: set[GroupID]

    def set_healer_id(self, x_healer_id: GroupID):
        self._healer_ids.add(x_healer_id)

    def healer_id_exists(self, x_healer_id: GroupID) -> bool:
        return x_healer_id in self._healer_ids

    def any_healer_id_exists(self) -> bool:
        return len(self._healer_ids) > 0

    def del_healer_id(self, x_healer_id: GroupID):
        self._healer_ids.remove(x_healer_id)

    def get_dict(self):
        return {"healerhold_healer_ids": list(self._healer_ids)}


def healerhold_shop(_healer_ids: set[GroupID] = None) -> HealerHold:
    return HealerHold(_healer_ids=get_empty_set_if_none(_healer_ids))


def healerhold_get_from_dict(x_dict: dict[str, set]) -> HealerHold:
    x_healerhold = healerhold_shop()
    if x_dict.get("healerhold_healer_ids") is not None:
        for x_healer_id in x_dict.get("healerhold_healer_ids"):
            x_healerhold.set_healer_id(x_healer_id=x_healer_id)
    return x_healerhold
