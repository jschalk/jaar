from src._instrument.python import get_empty_set_if_none
from src._road.road import LobbyID
from dataclasses import dataclass


@dataclass
class HealerHold:
    _lobby_ids: set[LobbyID]

    def set_lobby_id(self, x_lobby_id: LobbyID):
        self._lobby_ids.add(x_lobby_id)

    def lobby_id_exists(self, x_lobby_id: LobbyID) -> bool:
        return x_lobby_id in self._lobby_ids

    def any_lobby_id_exists(self) -> bool:
        return len(self._lobby_ids) > 0

    def del_lobby_id(self, x_lobby_id: LobbyID):
        self._lobby_ids.remove(x_lobby_id)

    def get_dict(self):
        return {"healerhold_lobby_ids": list(self._lobby_ids)}


def healerhold_shop(_lobby_ids: set[LobbyID] = None) -> HealerHold:
    return HealerHold(_lobby_ids=get_empty_set_if_none(_lobby_ids))


def healerhold_get_from_dict(x_dict: dict[str, set]) -> HealerHold:
    x_healerhold = healerhold_shop()
    if x_dict.get("healerhold_lobby_ids") != None:
        for x_lobby_id in x_dict.get("healerhold_lobby_ids"):
            x_healerhold.set_lobby_id(x_lobby_id=x_lobby_id)
    return x_healerhold
