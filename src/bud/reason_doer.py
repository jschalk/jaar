from src._instrument.python import get_empty_set_if_none
from src.bud.lobby import LobbyBox, LobbyID
from src.bud.char import CharID
from dataclasses import dataclass


class InvalidDoerHeirPopulateException(Exception):
    pass


@dataclass
class DoerUnit:
    _lobbyholds: set[LobbyID]

    def get_dict(self) -> dict[str, str]:
        return {"_lobbyholds": list(self._lobbyholds)}

    def set_lobbyhold(self, lobby_id: LobbyID):
        self._lobbyholds.add(lobby_id)

    def lobbyhold_exists(self, lobby_id: LobbyID):
        return lobby_id in self._lobbyholds

    def del_lobbyhold(self, lobby_id: LobbyID):
        self._lobbyholds.remove(lobby_id)

    def get_lobbyhold(self, lobby_id: LobbyID) -> LobbyID:
        if self.lobbyhold_exists(lobby_id):
            return lobby_id


def doerunit_shop(_lobbyholds: set[LobbyID] = None) -> DoerUnit:
    return DoerUnit(get_empty_set_if_none(_lobbyholds))


def create_doerunit(lobbyhold: LobbyID):
    x_doerunit = doerunit_shop()
    x_doerunit.set_lobbyhold(lobbyhold)
    return x_doerunit


@dataclass
class DoerHeir:
    _lobbyholds: set[LobbyID]
    _owner_id_doer: bool

    def _get_all_chars(
        self,
        bud_lobbyboxs: dict[LobbyID, LobbyBox],
        lobby_id_set: set[LobbyID],
    ) -> dict[LobbyID, LobbyBox]:
        dict_x = {}
        for lobby_id_x in lobby_id_set:
            dict_x |= bud_lobbyboxs.get(lobby_id_x)._lobbyships
        return dict_x

    def is_empty(self) -> bool:
        return self._lobbyholds == set()

    def set_owner_id_doer(
        self, bud_lobbyboxs: dict[LobbyID, LobbyBox], bud_owner_id: CharID
    ):
        self._owner_id_doer = self.get_owner_id_doer_bool(bud_lobbyboxs, bud_owner_id)

    def get_owner_id_doer_bool(
        self, bud_lobbyboxs: dict[LobbyID, LobbyBox], bud_owner_id: CharID
    ) -> bool:
        if self._lobbyholds == set():
            return True

        for x_lobby_id, x_lobbybox in bud_lobbyboxs.items():
            if x_lobby_id in self._lobbyholds:
                for x_char_id in x_lobbybox._lobbyships.keys():
                    if x_char_id == bud_owner_id:
                        return True
        return False

    def set_lobbyholds(
        self,
        parent_doerheir,
        doerunit: DoerUnit,
        bud_lobbyboxs: dict[LobbyID, LobbyBox],
    ):
        x_lobbyholds = set()
        if parent_doerheir is None or parent_doerheir._lobbyholds == set():
            for lobbyhold in doerunit._lobbyholds:
                x_lobbyholds.add(lobbyhold)
        elif doerunit._lobbyholds == set() or (
            parent_doerheir._lobbyholds == doerunit._lobbyholds
        ):
            for lobbyhold in parent_doerheir._lobbyholds:
                x_lobbyholds.add(lobbyhold)
        else:
            # get all_chars of parent doerheir lobbyboxs
            all_parent_doerheir_chars = self._get_all_chars(
                bud_lobbyboxs=bud_lobbyboxs,
                lobby_id_set=parent_doerheir._lobbyholds,
            )
            # get all_chars of doerunit lobbyboxs
            all_doerunit_chars = self._get_all_chars(
                bud_lobbyboxs=bud_lobbyboxs,
                lobby_id_set=doerunit._lobbyholds,
            )
            if not set(all_doerunit_chars).issubset(set(all_parent_doerheir_chars)):
                # else raise error
                raise InvalidDoerHeirPopulateException(
                    f"parent_doerheir does not contain all chars of the idea's doerunit\n{set(all_parent_doerheir_chars)=}\n\n{set(all_doerunit_chars)=}"
                )

            # set dict_x = to doerunit lobbyboxs
            for lobbyhold in doerunit._lobbyholds:
                x_lobbyholds.add(lobbyhold)
        self._lobbyholds = x_lobbyholds

    def has_lobby(self, lobby_ids: set[LobbyID]):
        return self.is_empty() or any(gn_x in self._lobbyholds for gn_x in lobby_ids)


def doerheir_shop(
    _lobbyholds: set[LobbyID] = None, _owner_id_doer: bool = None
) -> DoerHeir:
    _lobbyholds = get_empty_set_if_none(_lobbyholds)
    if _owner_id_doer is None:
        _owner_id_doer = False

    return DoerHeir(_lobbyholds=_lobbyholds, _owner_id_doer=_owner_id_doer)


def doerunit_get_from_dict(doerunit_dict: dict) -> DoerUnit:
    x_doerunit = doerunit_shop()
    for x_lobby_id in doerunit_dict.get("_lobbyholds"):
        x_doerunit.set_lobbyhold(x_lobby_id)

    return x_doerunit
