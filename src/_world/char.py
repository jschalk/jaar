from src._instrument.python import get_1_if_None, get_dict_from_json, get_0_if_None
from src._road.road import (
    CharID,
    default_road_delimiter_if_none,
    validate_roadnode,
    is_roadnode,
)
from src._road.finance import default_bit_if_none, RespectNum, allot_scale
from src._world.lobby import (
    LobbyID,
    LobbyShip,
    lobbyships_get_from_dict,
    lobbyship_shop,
)
from dataclasses import dataclass


class InvalidCharException(Exception):
    pass


class _lobbyship_Exception(Exception):
    pass


@dataclass
class CharCore:
    char_id: CharID = None
    _road_delimiter: str = None
    _bit: float = None

    def set_char_id(self, x_char_id: CharID):
        self.char_id = validate_roadnode(x_char_id, self._road_delimiter)


@dataclass
class CharUnit(CharCore):
    """This represents the WorldUnit._owner_id's opinion of the CharUnit.char_id
    CharUnit.credor_weight represents how much credor_weight the _owner_id projects to the char_id
    CharUnit.debtor_weight represents how much debtor_weight the _owner_id projects to the char_id
    """

    credor_weight: int = None
    debtor_weight: int = None
    # special attribute: static in world json, in memory it is deleted after loading and recalculated during saving.
    _lobbyships: dict[CharID, LobbyShip] = None
    # calculated fields
    _credor_pool: RespectNum = None
    _debtor_pool: RespectNum = None
    _irrational_debtor_weight: int = None  # set by listening process
    _inallocable_debtor_weight: int = None  # set by listening process
    # set by World.settle_world()
    _bud_give: float = None
    _bud_take: float = None
    _bud_agenda_give: float = None
    _bud_agenda_take: float = None
    _bud_agenda_ratio_give: float = None
    _bud_agenda_ratio_take: float = None

    def set_bit(self, x_bit: float):
        self._bit = x_bit

    def set_credor_debtor_weight(
        self,
        credor_weight: float = None,
        debtor_weight: float = None,
    ):
        if credor_weight != None:
            self.set_credor_weight(credor_weight)
        if debtor_weight != None:
            self.set_debtor_weight(debtor_weight)

    def set_credor_weight(self, credor_weight: int):
        self.credor_weight = credor_weight

    def set_debtor_weight(self, debtor_weight: int):
        self.debtor_weight = debtor_weight

    def get_credor_weight(self):
        return get_1_if_None(self.credor_weight)

    def get_debtor_weight(self):
        return get_1_if_None(self.debtor_weight)

    def reset_bud_give_take(self):
        self._bud_give = 0
        self._bud_take = 0
        self._bud_agenda_give = 0
        self._bud_agenda_take = 0
        self._bud_agenda_ratio_give = 0
        self._bud_agenda_ratio_take = 0

    def add_irrational_debtor_weight(self, x_irrational_debtor_weight: float):
        self._irrational_debtor_weight += x_irrational_debtor_weight

    def add_inallocable_debtor_weight(self, x_inallocable_debtor_weight: float):
        self._inallocable_debtor_weight += x_inallocable_debtor_weight

    def reset_listen_calculated_attrs(self):
        self._irrational_debtor_weight = 0
        self._inallocable_debtor_weight = 0

    def add_bud_give_take(
        self,
        bud_give: float,
        bud_take,
        world_agenda_cred: float,
        world_agenda_debt,
    ):
        self._bud_give += bud_give
        self._bud_take += bud_take
        self._bud_agenda_give += world_agenda_cred
        self._bud_agenda_take += world_agenda_debt

    def set_bud_agenda_ratio_give_take(
        self,
        bud_agenda_ratio_give_sum: float,
        bud_agenda_ratio_take_sum: float,
        world_charunit_total_credor_weight: float,
        world_charunit_total_debtor_weight: float,
    ):
        if bud_agenda_ratio_give_sum == 0:
            self._bud_agenda_ratio_give = (
                self.get_credor_weight() / world_charunit_total_credor_weight
            )
        else:
            self._bud_agenda_ratio_give = (
                self._bud_agenda_give / bud_agenda_ratio_give_sum
            )

        if bud_agenda_ratio_take_sum == 0:
            self._bud_agenda_ratio_take = (
                self.get_debtor_weight() / world_charunit_total_debtor_weight
            )
        else:
            self._bud_agenda_ratio_take = (
                self._bud_agenda_take / bud_agenda_ratio_take_sum
            )

    def add_lobbyship(
        self,
        lobby_id: LobbyID,
        credor_weight: float = None,
        debtor_weight: float = None,
    ):
        x_lobbyship = lobbyship_shop(lobby_id, credor_weight, debtor_weight)
        self.set_lobbyship(x_lobbyship)

    def set_lobbyship(self, x_lobbyship: LobbyShip):
        x_lobby_id = x_lobbyship.lobby_id
        lobby_id_is_char_id = is_roadnode(x_lobby_id, self._road_delimiter)
        if lobby_id_is_char_id and self.char_id != x_lobby_id:
            raise _lobbyship_Exception(
                f"CharUnit with char_id='{self.char_id}' cannot have link to '{x_lobby_id}'."
            )

        x_lobbyship._char_id = self.char_id
        self._lobbyships[x_lobbyship.lobby_id] = x_lobbyship

    def get_lobbyship(self, lobby_id: LobbyID) -> LobbyShip:
        return self._lobbyships.get(lobby_id)

    def lobbyship_exists(self, lobby_id: LobbyID) -> bool:
        return self._lobbyships.get(lobby_id) != None

    def delete_lobbyship(self, lobby_id: LobbyID):
        return self._lobbyships.pop(lobby_id)

    def lobbyships_exist(self):
        return len(self._lobbyships) != 0

    def clear_lobbyships(self):
        self._lobbyships = {}

    def set_credor_pool(self, credor_pool: RespectNum):
        self._credor_pool = credor_pool
        ledger_dict = {
            x_lobbyship.lobby_id: x_lobbyship.credor_weight
            for x_lobbyship in self._lobbyships.values()
        }
        allot_dict = allot_scale(ledger_dict, self._credor_pool, self._bit)
        for x_lobby_id, lobby_credor_pool in allot_dict.items():
            self.get_lobbyship(x_lobby_id)._credor_pool = lobby_credor_pool

    def set_debtor_pool(self, debtor_pool: RespectNum):
        self._debtor_pool = debtor_pool
        ledger_dict = {
            x_lobbyship.lobby_id: x_lobbyship.debtor_weight
            for x_lobbyship in self._lobbyships.values()
        }
        allot_dict = allot_scale(ledger_dict, self._debtor_pool, self._bit)
        for x_lobby_id, lobby_debtor_pool in allot_dict.items():
            self.get_lobbyship(x_lobby_id)._debtor_pool = lobby_debtor_pool

    def get_lobbyships_dict(self) -> dict:
        return {
            x_lobbyship.lobby_id: {
                "lobby_id": x_lobbyship.lobby_id,
                "credor_weight": x_lobbyship.credor_weight,
                "debtor_weight": x_lobbyship.debtor_weight,
            }
            for x_lobbyship in self._lobbyships.values()
        }

    def get_dict(self, all_attrs: bool = False) -> dict[str, str]:
        x_dict = {
            "char_id": self.char_id,
            "credor_weight": self.credor_weight,
            "debtor_weight": self.debtor_weight,
            "_lobbyships": self.get_lobbyships_dict(),
        }
        if self._irrational_debtor_weight not in [None, 0]:
            x_dict["_irrational_debtor_weight"] = self._irrational_debtor_weight
        if self._inallocable_debtor_weight not in [None, 0]:
            x_dict["_inallocable_debtor_weight"] = self._inallocable_debtor_weight

        if all_attrs:
            self._all_attrs_necessary_in_dict(x_dict)
        return x_dict

    def _all_attrs_necessary_in_dict(self, x_dict):
        x_dict["_bud_give"] = self._bud_give
        x_dict["_bud_take"] = self._bud_take
        x_dict["_bud_agenda_give"] = self._bud_agenda_give
        x_dict["_bud_agenda_take"] = self._bud_agenda_take
        x_dict["_bud_agenda_ratio_give"] = self._bud_agenda_ratio_give
        x_dict["_bud_agenda_ratio_take"] = self._bud_agenda_ratio_take


# class CharUnitsshop:
def charunits_get_from_json(charunits_json: str) -> dict[str, CharUnit]:
    charunits_dict = get_dict_from_json(json_x=charunits_json)
    return charunits_get_from_dict(x_dict=charunits_dict)


def charunits_get_from_dict(
    x_dict: dict, _road_delimiter: str = None
) -> dict[str, CharUnit]:
    charunits = {}
    for charunit_dict in x_dict.values():
        x_charunit = charunit_get_from_dict(charunit_dict, _road_delimiter)
        charunits[x_charunit.char_id] = x_charunit
    return charunits


def charunit_get_from_dict(charunit_dict: dict, _road_delimiter: str) -> CharUnit:
    x_char_id = charunit_dict["char_id"]
    x_credor_weight = charunit_dict["credor_weight"]
    x_debtor_weight = charunit_dict["debtor_weight"]
    x_lobbyships_dict = charunit_dict["_lobbyships"]
    x_charunit = charunit_shop(
        x_char_id, x_credor_weight, x_debtor_weight, _road_delimiter
    )
    x_charunit._lobbyships = lobbyships_get_from_dict(x_lobbyships_dict, x_char_id)
    _irrational_debtor_weight = charunit_dict.get("_irrational_debtor_weight", 0)
    _inallocable_debtor_weight = charunit_dict.get("_inallocable_debtor_weight", 0)
    x_charunit.add_irrational_debtor_weight(get_0_if_None(_irrational_debtor_weight))
    x_charunit.add_inallocable_debtor_weight(get_0_if_None(_inallocable_debtor_weight))

    return x_charunit


def charunit_shop(
    char_id: CharID,
    credor_weight: int = None,
    debtor_weight: int = None,
    _road_delimiter: str = None,
    _bit: float = None,
) -> CharUnit:
    x_charunit = CharUnit(
        credor_weight=get_1_if_None(credor_weight),
        debtor_weight=get_1_if_None(debtor_weight),
        _lobbyships={},
        _credor_pool=0,
        _debtor_pool=0,
        _irrational_debtor_weight=0,
        _inallocable_debtor_weight=0,
        _bud_give=0,
        _bud_take=0,
        _bud_agenda_give=0,
        _bud_agenda_take=0,
        _bud_agenda_ratio_give=0,
        _bud_agenda_ratio_take=0,
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _bit=default_bit_if_none(_bit),
    )
    x_charunit.set_char_id(x_char_id=char_id)
    return x_charunit
