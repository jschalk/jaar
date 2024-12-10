from src.f00_instrument.dict_toolbox import get_empty_set_if_None
from src.f01_road.road import GroupID
from dataclasses import dataclass


@dataclass
class HealerLink:
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
        return {"healerlink_healer_ids": list(self._healer_ids)}


def healerlink_shop(_healer_ids: set[GroupID] = None) -> HealerLink:
    return HealerLink(_healer_ids=get_empty_set_if_None(_healer_ids))


def healerlink_get_from_dict(x_dict: dict[str, set]) -> HealerLink:
    x_healerlink = healerlink_shop()
    if x_dict.get("healerlink_healer_ids") is not None:
        for x_healer_id in x_dict.get("healerlink_healer_ids"):
            x_healerlink.set_healer_id(x_healer_id=x_healer_id)
    return x_healerlink
