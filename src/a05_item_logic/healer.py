from src.a00_data_toolbox.dict_toolbox import get_empty_set_if_None
from src.a01_word_logic.road import GroupLabel
from dataclasses import dataclass


@dataclass
class HealerLink:
    _healer_names: set[GroupLabel]

    def set_healer_name(self, x_healer_name: GroupLabel):
        self._healer_names.add(x_healer_name)

    def healer_name_exists(self, x_healer_name: GroupLabel) -> bool:
        return x_healer_name in self._healer_names

    def any_healer_name_exists(self) -> bool:
        return len(self._healer_names) > 0

    def del_healer_name(self, x_healer_name: GroupLabel):
        self._healer_names.remove(x_healer_name)

    def get_dict(self):
        return {"healerlink_healer_names": list(self._healer_names)}


def healerlink_shop(_healer_names: set[GroupLabel] = None) -> HealerLink:
    return HealerLink(_healer_names=get_empty_set_if_None(_healer_names))


def healerlink_get_from_dict(x_dict: dict[str, set]) -> HealerLink:
    x_healerlink = healerlink_shop()
    if x_dict.get("healerlink_healer_names") is not None:
        for x_healer_name in x_dict.get("healerlink_healer_names"):
            x_healerlink.set_healer_name(x_healer_name=x_healer_name)
    return x_healerlink
