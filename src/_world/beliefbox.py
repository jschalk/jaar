from src._instrument.python import (
    get_empty_dict_if_none,
    get_1_if_None,
    get_dict_from_json,
    get_0_if_None,
)
from src._road.road import CharID, default_road_delimiter_if_none, validate_roadnode
from src._world.belieflink import BeliefID, BeliefCore
from src._world.char import (
    CharLink,
    charlinks_get_from_dict,
    charlink_shop,
    CharUnit,
)
from dataclasses import dataclass


class InvalidBeliefException(Exception):
    pass


@dataclass
class BeliefBox(BeliefCore):
    _char_mirror: bool = None  # set by WorldUnit.set_charunit()
    _chars: dict[CharID, CharLink] = None  # set by WorldUnit.set_charunit()
    _road_delimiter: str = None  # calculated by WorldUnit.set_beliefbox
    # calculated by WorldUnit.calc_world_metrics()
    _world_cred: float = None
    _world_debt: float = None
    _world_agenda_cred: float = None
    _world_agenda_debt: float = None

    def set_belief_id(self, belief_id: BeliefID = None):
        if belief_id != None:
            if self._char_mirror:
                self.belief_id = validate_roadnode(belief_id, self._road_delimiter)
            else:
                self.belief_id = validate_roadnode(
                    belief_id, self._road_delimiter, not_roadnode_required=True
                )

    def get_dict(self) -> dict[str, str]:
        x_dict = {"belief_id": self.belief_id}
        if self._char_mirror:
            x_dict["_char_mirror"] = self._char_mirror
        if self._chars not in [{}, None]:
            x_dict["_chars"] = self.get_charunits_dict()

        return x_dict

    def reset_world_cred_debt(self):
        self._world_cred = 0
        self._world_debt = 0
        self._world_agenda_cred = 0
        self._world_agenda_debt = 0
        for charlink in self._chars.values():
            charlink.reset_world_cred_debt()

    def _set_charlink_world_cred_debt(self):
        charlinks_credor_weight_sum = sum(
            charlink.credor_weight for charlink in self._chars.values()
        )
        charlinks_debtor_weight_sum = sum(
            charlink.debtor_weight for charlink in self._chars.values()
        )

        for charlink in self._chars.values():
            charlink.set_world_cred_debt(
                charlinks_credor_weight_sum=charlinks_credor_weight_sum,
                charlinks_debtor_weight_sum=charlinks_debtor_weight_sum,
                belief_world_cred=self._world_cred,
                belief_world_debt=self._world_debt,
                belief_world_agenda_cred=self._world_agenda_cred,
                belief_world_agenda_debt=self._world_agenda_debt,
            )

    def clear_charlinks(self):
        self._chars = {}

    def get_charunits_dict(self) -> dict[str, str]:
        chars_x_dict = {}
        for char in self._chars.values():
            char_dict = char.get_dict()
            chars_x_dict[char_dict["char_id"]] = char_dict
        return chars_x_dict

    def set_charlink(self, charlink: CharLink):
        self._chars[charlink.char_id] = charlink

    def edit_charlink(
        self, char_id: CharID, credor_weight: int = None, debtor_weight: int = None
    ):
        x_charlink = self.get_charlink(char_id)
        if credor_weight != None:
            x_charlink.credor_weight = credor_weight
        if debtor_weight != None:
            x_charlink.debtor_weight = debtor_weight

    def get_charlink(self, char_id: CharID) -> CharLink:
        return self._chars.get(char_id)

    def charlink_exists(self, charlink_char_id: CharID) -> bool:
        return self.get_charlink(charlink_char_id) != None

    def del_charlink(self, char_id):
        self._chars.pop(char_id)

    def _shift_charlink(self, to_delete_char_id: CharID, to_absorb_char_id: CharID):
        old_belief_charlink = self.get_charlink(to_delete_char_id)
        new_charlink_credor_weight = old_belief_charlink.credor_weight
        new_charlink_debtor_weight = old_belief_charlink.debtor_weight

        new_charlink = self.get_charlink(to_absorb_char_id)
        if new_charlink != None:
            new_charlink_credor_weight += new_charlink.credor_weight
            new_charlink_debtor_weight += new_charlink.debtor_weight

        self.set_charlink(
            charlink=charlink_shop(
                char_id=to_absorb_char_id,
                credor_weight=new_charlink_credor_weight,
                debtor_weight=new_charlink_debtor_weight,
            )
        )
        self.del_charlink(char_id=to_delete_char_id)


# class BeliefBoxsshop:
def get_from_json(beliefboxs_json: str) -> dict[BeliefID, BeliefBox]:
    beliefboxs_dict = get_dict_from_json(json_x=beliefboxs_json)
    return get_beliefboxs_from_dict(x_dict=beliefboxs_dict)


def get_beliefboxs_from_dict(
    x_dict: dict, _road_delimiter: str = None
) -> dict[BeliefID, BeliefBox]:
    beliefboxs = {}
    for beliefbox_dict in x_dict.values():
        x_belief = get_beliefbox_from_dict(beliefbox_dict, _road_delimiter)
        beliefboxs[x_belief.belief_id] = x_belief
    return beliefboxs


def get_beliefbox_from_dict(
    beliefbox_dict: dict, _road_delimiter: str = None
) -> BeliefBox:
    return beliefbox_shop(
        belief_id=beliefbox_dict["belief_id"],
        _char_mirror=get_obj_from_beliefbox_dict(beliefbox_dict, "_char_mirror"),
        _chars=get_obj_from_beliefbox_dict(beliefbox_dict, "_chars"),
        _road_delimiter=_road_delimiter,
    )


def get_obj_from_beliefbox_dict(x_dict: dict[str,], dict_key: str) -> any:
    if dict_key == "_chars":
        return charlinks_get_from_dict(x_dict.get(dict_key))
    elif dict_key in {"_char_mirror"}:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else False
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else None


def beliefbox_shop(
    belief_id: BeliefID,
    _char_mirror: bool = None,
    _chars: dict[CharID, CharLink] = None,
    _road_delimiter: str = None,
) -> BeliefBox:
    _char_mirror = False if _char_mirror is None else _char_mirror
    x_beliefbox = BeliefBox(
        _char_mirror=_char_mirror,
        _chars=get_empty_dict_if_none(_chars),
        _world_cred=get_0_if_None(),
        _world_debt=get_0_if_None(),
        _world_agenda_cred=get_0_if_None(),
        _world_agenda_debt=get_0_if_None(),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )
    x_beliefbox.set_belief_id(belief_id=belief_id)
    return x_beliefbox


@dataclass
class AwardLink(BeliefCore):
    credor_weight: float = 1.0
    debtor_weight: float = 1.0

    def get_dict(self) -> dict[str, str]:
        return {
            "belief_id": self.belief_id,
            "credor_weight": self.credor_weight,
            "debtor_weight": self.debtor_weight,
        }


# class AwardLinksshop:
def awardlinks_get_from_json(awardlinks_json: str) -> dict[BeliefID, AwardLink]:
    awardlinks_dict = get_dict_from_json(json_x=awardlinks_json)
    return awardlinks_get_from_dict(x_dict=awardlinks_dict)


def awardlinks_get_from_dict(x_dict: dict) -> dict[BeliefID, AwardLink]:
    awardlinks = {}
    for awardlinks_dict in x_dict.values():
        x_belief = awardlink_shop(
            belief_id=awardlinks_dict["belief_id"],
            credor_weight=awardlinks_dict["credor_weight"],
            debtor_weight=awardlinks_dict["debtor_weight"],
        )
        awardlinks[x_belief.belief_id] = x_belief
    return awardlinks


def awardlink_shop(
    belief_id: BeliefID, credor_weight: float = None, debtor_weight: float = None
) -> AwardLink:
    credor_weight = get_1_if_None(credor_weight)
    debtor_weight = get_1_if_None(debtor_weight)
    return AwardLink(belief_id, credor_weight, debtor_weight=debtor_weight)


@dataclass
class AwardHeir(BeliefCore):
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
    belief_id: BeliefID,
    credor_weight: float = None,
    debtor_weight: float = None,
    _world_cred: float = None,
    _world_debt: float = None,
) -> AwardHeir:
    credor_weight = get_1_if_None(credor_weight)
    debtor_weight = get_1_if_None(debtor_weight)
    return AwardHeir(belief_id, credor_weight, debtor_weight, _world_cred, _world_debt)


@dataclass
class AwardLine(BeliefCore):
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


def awardline_shop(belief_id: BeliefID, _world_cred: float, _world_debt: float):
    return AwardLine(belief_id, _world_cred=_world_cred, _world_debt=_world_debt)


def get_intersection_of_chars(
    chars_x: dict[CharID, CharUnit], chars_y: dict[CharID, CharUnit]
) -> dict[CharID, int]:
    x_set = set(chars_x)
    y_set = set(chars_y)
    intersection_x = x_set.intersection(y_set)
    return {char_id_x: -1 for char_id_x in intersection_x}


def get_chars_relevant_beliefs(
    beliefs_x: dict[BeliefID, BeliefBox], chars_x: dict[CharID, CharUnit]
) -> dict[BeliefID, dict[CharID, int]]:
    relevant_beliefs = {}
    for char_id_x in chars_x:
        for belief_x in beliefs_x.values():
            if belief_x._chars.get(char_id_x) != None:
                if relevant_beliefs.get(belief_x.belief_id) is None:
                    relevant_beliefs[belief_x.belief_id] = {}
                relevant_beliefs.get(belief_x.belief_id)[char_id_x] = -1

    return relevant_beliefs
