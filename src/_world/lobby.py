from src._instrument.python import get_1_if_None, get_dict_from_json
from src._road.road import LobbyID, CharID, default_road_delimiter_if_none
from dataclasses import dataclass


class InvalidLobbyException(Exception):
    pass


class lobbylink_lobby_id_Exception(Exception):
    pass


@dataclass
class LobbyCore:
    lobby_id: LobbyID = None


@dataclass
class LobbyLink(LobbyCore):
    credor_weight: float = 1.0
    debtor_weight: float = 1.0
    # calculated fields
    _credor_pool: float = None
    _debtor_pool: float = None
    _bud_give: float = None
    _bud_take: float = None
    _bud_agenda_give: float = None
    _bud_agenda_take: float = None
    _bud_agenda_ratio_give: float = None
    _bud_agenda_ratio_take: float = None
    _char_id: CharID = None

    def set_credor_weight(self, x_credor_weight: float):
        if x_credor_weight != None:
            self.credor_weight = x_credor_weight

    def set_debtor_weight(self, x_debtor_weight: float):
        if x_debtor_weight != None:
            self.debtor_weight = x_debtor_weight

    def get_dict(self) -> dict[str, str]:
        return {
            "lobby_id": self.lobby_id,
            "credor_weight": self.credor_weight,
            "debtor_weight": self.debtor_weight,
        }

    def reset_bud_give_take(self):
        self._bud_give = 0
        self._bud_take = 0
        self._bud_agenda_give = 0
        self._bud_agenda_take = 0
        self._bud_agenda_ratio_give = 0
        self._bud_agenda_ratio_take = 0

    def set_bud_give_take(
        self,
        lobbylinks_credor_weight_sum: float,
        lobbylinks_debtor_weight_sum: float,
        lobby_bud_give: float,
        lobby_bud_take: float,
        lobby_bud_agenda_give: float,
        lobby_bud_agenda_take: float,
    ):
        lobby_bud_give = get_1_if_None(lobby_bud_give)
        lobby_bud_take = get_1_if_None(lobby_bud_take)
        credor_ratio = self.credor_weight / lobbylinks_credor_weight_sum
        debtor_ratio = self.debtor_weight / lobbylinks_debtor_weight_sum

        self._bud_give = lobby_bud_give * credor_ratio
        self._bud_take = lobby_bud_take * debtor_ratio
        self._bud_agenda_give = lobby_bud_agenda_give * credor_ratio
        self._bud_agenda_take = lobby_bud_agenda_take * debtor_ratio


def lobbylink_shop(
    lobby_id: LobbyID,
    credor_weight: float = None,
    debtor_weight: float = None,
    _char_id: CharID = None,
) -> LobbyLink:
    return LobbyLink(
        lobby_id=lobby_id,
        credor_weight=get_1_if_None(credor_weight),
        debtor_weight=get_1_if_None(debtor_weight),
        _credor_pool=0,
        _debtor_pool=0,
        _char_id=_char_id,
    )


def lobbylink_get_from_dict(x_dict: dict, x_char_id: CharID) -> LobbyLink:
    return lobbylink_shop(
        lobby_id=x_dict.get("lobby_id"),
        credor_weight=x_dict.get("credor_weight"),
        debtor_weight=x_dict.get("debtor_weight"),
        _char_id=x_char_id,
    )


def lobbylinks_get_from_dict(
    x_dict: dict, x_char_id: CharID
) -> dict[LobbyID, LobbyLink]:
    return {
        x_lobby_id: lobbylink_get_from_dict(x_lobbylink_dict, x_char_id)
        for x_lobby_id, x_lobbylink_dict in x_dict.items()
    }


@dataclass
class AwardLink(LobbyCore):
    give_weight: float = 1.0
    take_weight: float = 1.0

    def get_dict(self) -> dict[str, str]:
        return {
            "lobby_id": self.lobby_id,
            "give_weight": self.give_weight,
            "take_weight": self.take_weight,
        }


# class AwardLinksshop:
def awardlinks_get_from_json(awardlinks_json: str) -> dict[LobbyID, AwardLink]:
    awardlinks_dict = get_dict_from_json(json_x=awardlinks_json)
    return awardlinks_get_from_dict(x_dict=awardlinks_dict)


def awardlinks_get_from_dict(x_dict: dict) -> dict[LobbyID, AwardLink]:
    awardlinks = {}
    for awardlinks_dict in x_dict.values():
        x_lobby = awardlink_shop(
            lobby_id=awardlinks_dict["lobby_id"],
            give_weight=awardlinks_dict["give_weight"],
            take_weight=awardlinks_dict["take_weight"],
        )
        awardlinks[x_lobby.lobby_id] = x_lobby
    return awardlinks


def awardlink_shop(
    lobby_id: LobbyID, give_weight: float = None, take_weight: float = None
) -> AwardLink:
    give_weight = get_1_if_None(give_weight)
    take_weight = get_1_if_None(take_weight)
    return AwardLink(lobby_id, give_weight, take_weight=take_weight)


@dataclass
class AwardHeir(LobbyCore):
    give_weight: float = 1.0
    take_weight: float = 1.0
    _bud_give: float = None
    _bud_take: float = None

    def set_bud_give_take(
        self,
        idea_bud_share,
        awardheirs_give_weight_sum: float,
        awardheirs_take_weight_sum: float,
    ):
        credor_share_ratio = self.give_weight / awardheirs_give_weight_sum
        self._bud_give = idea_bud_share * credor_share_ratio
        debtor_share_ratio = self.take_weight / awardheirs_take_weight_sum
        self._bud_take = idea_bud_share * debtor_share_ratio


def awardheir_shop(
    lobby_id: LobbyID,
    give_weight: float = None,
    take_weight: float = None,
    _bud_give: float = None,
    _bud_take: float = None,
) -> AwardHeir:
    give_weight = get_1_if_None(give_weight)
    take_weight = get_1_if_None(take_weight)
    return AwardHeir(lobby_id, give_weight, take_weight, _bud_give, _bud_take)


@dataclass
class AwardLine(LobbyCore):
    _bud_give: float = None
    _bud_take: float = None

    def add_bud_give_take(self, bud_give: float, bud_take: float):
        self.set_bud_give_take_zero_if_none()
        self._bud_give += bud_give
        self._bud_take += bud_take

    def set_bud_give_take_zero_if_none(self):
        if self._bud_give is None:
            self._bud_give = 0
        if self._bud_take is None:
            self._bud_take = 0


def awardline_shop(lobby_id: LobbyID, _bud_give: float, _bud_take: float):
    return AwardLine(lobby_id, _bud_give=_bud_give, _bud_take=_bud_take)


@dataclass
class LobbyBox(LobbyCore):
    _lobbylinks: dict[CharID, LobbyLink] = None  # set by WorldUnit.set_charunit()
    _road_delimiter: str = None  # calculated by WorldUnit
    # calculated by WorldUnit.calc_world_metrics()
    _bud_give: float = None
    _bud_take: float = None
    _bud_agenda_give: float = None
    _bud_agenda_take: float = None
    _credor_pool: float = None
    _debtor_pool: float = None

    def set_lobbylink(self, x_lobbylink: LobbyLink):
        if x_lobbylink.lobby_id != self.lobby_id:
            raise lobbylink_lobby_id_Exception(
                f"LobbyBox.lobby_id={self.lobby_id} cannot set lobbylink.lobby_id={x_lobbylink.lobby_id}"
            )
        if x_lobbylink._char_id is None:
            raise lobbylink_lobby_id_Exception(
                f"lobbylink lobby_id={x_lobbylink.lobby_id} cannot be set when _char_id is None."
            )

        self._lobbylinks[x_lobbylink._char_id] = x_lobbylink
        self._add_credor_pool(x_lobbylink._credor_pool)
        self._add_debtor_pool(x_lobbylink._debtor_pool)

    def _add_credor_pool(self, x_credor_pool: float):
        self._credor_pool += x_credor_pool

    def _add_debtor_pool(self, x_debtor_pool: float):
        self._debtor_pool += x_debtor_pool

    def get_lobbylink(self, x_char_id: CharID) -> LobbyLink:
        return self._lobbylinks.get(x_char_id)

    def lobbylink_exists(self, x_char_id: CharID) -> bool:
        return self.get_lobbylink(x_char_id) != None

    def del_lobbylink(self, char_id):
        self._lobbylinks.pop(char_id)

    def reset_bud_give_take(self):
        self._bud_give = 0
        self._bud_take = 0
        self._bud_agenda_give = 0
        self._bud_agenda_take = 0
        for lobbylink in self._lobbylinks.values():
            lobbylink.reset_bud_give_take()

    def _set_lobbylink_bud_give_take(self):
        lobbylinks_credor_weight_sum = sum(
            lobbylink.credor_weight for lobbylink in self._lobbylinks.values()
        )
        lobbylinks_debtor_weight_sum = sum(
            lobbylink.debtor_weight for lobbylink in self._lobbylinks.values()
        )

        for lobbylink in self._lobbylinks.values():
            lobbylink.set_bud_give_take(
                lobbylinks_credor_weight_sum=lobbylinks_credor_weight_sum,
                lobbylinks_debtor_weight_sum=lobbylinks_debtor_weight_sum,
                lobby_bud_give=self._bud_give,
                lobby_bud_take=self._bud_take,
                lobby_bud_agenda_give=self._bud_agenda_give,
                lobby_bud_agenda_take=self._bud_agenda_take,
            )


def lobbybox_shop(lobby_id: LobbyID, _road_delimiter: str = None) -> LobbyBox:
    return LobbyBox(
        lobby_id=lobby_id,
        _lobbylinks={},
        _bud_give=0,
        _bud_take=0,
        _bud_agenda_give=0,
        _bud_agenda_take=0,
        _credor_pool=0,
        _debtor_pool=0,
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )
    # x_lobbybox.set_lobby_id(lobby_id=lobby_id)
    # return x_lobbybox
