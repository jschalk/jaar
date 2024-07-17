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
    _world_cred: float = None
    _world_debt: float = None
    _world_agenda_cred: float = None
    _world_agenda_debt: float = None
    _world_agenda_ratio_cred: float = None
    _world_agenda_ratio_debt: float = None
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

    def reset_world_cred_debt(self):
        self._world_cred = 0
        self._world_debt = 0
        self._world_agenda_cred = 0
        self._world_agenda_debt = 0
        self._world_agenda_ratio_cred = 0
        self._world_agenda_ratio_debt = 0

    def set_world_cred_debt(
        self,
        lobbylinks_credor_weight_sum: float,
        lobbylinks_debtor_weight_sum: float,
        lobby_world_cred: float,
        lobby_world_debt: float,
        lobby_world_agenda_cred: float,
        lobby_world_agenda_debt: float,
    ):
        lobby_world_cred = get_1_if_None(lobby_world_cred)
        lobby_world_debt = get_1_if_None(lobby_world_debt)
        credor_ratio = self.credor_weight / lobbylinks_credor_weight_sum
        debtor_ratio = self.debtor_weight / lobbylinks_debtor_weight_sum

        self._world_cred = lobby_world_cred * credor_ratio
        self._world_debt = lobby_world_debt * debtor_ratio
        self._world_agenda_cred = lobby_world_agenda_cred * credor_ratio
        self._world_agenda_debt = lobby_world_agenda_debt * debtor_ratio


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
    credor_weight: float = 1.0
    debtor_weight: float = 1.0

    def get_dict(self) -> dict[str, str]:
        return {
            "lobby_id": self.lobby_id,
            "credor_weight": self.credor_weight,
            "debtor_weight": self.debtor_weight,
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
            credor_weight=awardlinks_dict["credor_weight"],
            debtor_weight=awardlinks_dict["debtor_weight"],
        )
        awardlinks[x_lobby.lobby_id] = x_lobby
    return awardlinks


def awardlink_shop(
    lobby_id: LobbyID, credor_weight: float = None, debtor_weight: float = None
) -> AwardLink:
    credor_weight = get_1_if_None(credor_weight)
    debtor_weight = get_1_if_None(debtor_weight)
    return AwardLink(lobby_id, credor_weight, debtor_weight=debtor_weight)


@dataclass
class AwardHeir(LobbyCore):
    credor_weight: float = 1.0
    debtor_weight: float = 1.0
    _world_cred: float = None
    _world_debt: float = None

    def set_world_cred_debt(
        self,
        idea_bud_share,
        awardheirs_credor_weight_sum: float,
        awardheirs_debtor_weight_sum: float,
    ):
        credor_share_ratio = self.credor_weight / awardheirs_credor_weight_sum
        self._world_cred = idea_bud_share * credor_share_ratio
        debtor_share_ratio = self.debtor_weight / awardheirs_debtor_weight_sum
        self._world_debt = idea_bud_share * debtor_share_ratio


def awardheir_shop(
    lobby_id: LobbyID,
    credor_weight: float = None,
    debtor_weight: float = None,
    _world_cred: float = None,
    _world_debt: float = None,
) -> AwardHeir:
    credor_weight = get_1_if_None(credor_weight)
    debtor_weight = get_1_if_None(debtor_weight)
    return AwardHeir(lobby_id, credor_weight, debtor_weight, _world_cred, _world_debt)


@dataclass
class AwardLine(LobbyCore):
    _world_cred: float = None
    _world_debt: float = None

    def add_world_cred_debt(self, world_cred: float, world_debt: float):
        self.set_world_cred_debt_zero_if_none()
        self._world_cred += world_cred
        self._world_debt += world_debt

    def set_world_cred_debt_zero_if_none(self):
        if self._world_cred is None:
            self._world_cred = 0
        if self._world_debt is None:
            self._world_debt = 0


def awardline_shop(lobby_id: LobbyID, _world_cred: float, _world_debt: float):
    return AwardLine(lobby_id, _world_cred=_world_cred, _world_debt=_world_debt)


@dataclass
class LobbyBox(LobbyCore):
    _lobbylinks: dict[CharID, LobbyLink] = None  # set by WorldUnit.set_charunit()
    _road_delimiter: str = None  # calculated by WorldUnit
    # calculated by WorldUnit.calc_world_metrics()
    _world_cred: float = None
    _world_debt: float = None
    _world_agenda_cred: float = None
    _world_agenda_debt: float = None
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

    def reset_world_cred_debt(self):
        self._world_cred = 0
        self._world_debt = 0
        self._world_agenda_cred = 0
        self._world_agenda_debt = 0
        for lobbylink in self._lobbylinks.values():
            lobbylink.reset_world_cred_debt()

    def _set_lobbylink_world_cred_debt(self):
        lobbylinks_credor_weight_sum = sum(
            lobbylink.credor_weight for lobbylink in self._lobbylinks.values()
        )
        lobbylinks_debtor_weight_sum = sum(
            lobbylink.debtor_weight for lobbylink in self._lobbylinks.values()
        )

        for lobbylink in self._lobbylinks.values():
            lobbylink.set_world_cred_debt(
                lobbylinks_credor_weight_sum=lobbylinks_credor_weight_sum,
                lobbylinks_debtor_weight_sum=lobbylinks_debtor_weight_sum,
                lobby_world_cred=self._world_cred,
                lobby_world_debt=self._world_debt,
                lobby_world_agenda_cred=self._world_agenda_cred,
                lobby_world_agenda_debt=self._world_agenda_debt,
            )


def lobbybox_shop(lobby_id: LobbyID, _road_delimiter: str = None) -> LobbyBox:
    return LobbyBox(
        lobby_id=lobby_id,
        _lobbylinks={},
        _world_cred=0,
        _world_debt=0,
        _world_agenda_cred=0,
        _world_agenda_debt=0,
        _credor_pool=0,
        _debtor_pool=0,
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )
    # x_lobbybox.set_lobby_id(lobby_id=lobby_id)
    # return x_lobbybox
