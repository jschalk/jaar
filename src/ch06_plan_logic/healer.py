from dataclasses import dataclass
from src.ch01_data_toolbox.dict_toolbox import get_empty_set_if_None
from src.ch04_voice_logic._ref.ch04_semantic_types import GroupTitle


@dataclass
class HealerUnit:
    _healer_names: set[GroupTitle]

    def set_healer_name(self, x_healer_name: GroupTitle):
        self._healer_names.add(x_healer_name)

    def healer_name_exists(self, x_healer_name: GroupTitle) -> bool:
        return x_healer_name in self._healer_names

    def any_healer_name_exists(self) -> bool:
        return len(self._healer_names) > 0

    def del_healer_name(self, x_healer_name: GroupTitle):
        self._healer_names.remove(x_healer_name)

    def to_dict(self) -> dict[str, list[GroupTitle]]:
        return {"healerunit_healer_names": list(self._healer_names)}


def healerunit_shop(_healer_names: set[GroupTitle] = None) -> HealerUnit:
    return HealerUnit(_healer_names=get_empty_set_if_None(_healer_names))


def healerunit_get_from_dict(x_dict: dict[str, set]) -> HealerUnit:
    x_healerunit = healerunit_shop()
    if x_dict.get("healerunit_healer_names") is not None:
        for x_healer_name in x_dict.get("healerunit_healer_names"):
            x_healerunit.set_healer_name(x_healer_name=x_healer_name)
    return x_healerunit
