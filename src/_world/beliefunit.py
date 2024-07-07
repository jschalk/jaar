from src._instrument.python import (
    get_empty_dict_if_none,
    get_1_if_None,
    get_dict_from_json,
    get_0_if_None,
)
from src._road.road import CharID, default_road_delimiter_if_none, validate_roadnode
from src._world.beliefhold import BeliefID, BeliefCore
from src._world.char import (
    CharLink,
    charlinks_get_from_dict,
    charlink_shop,
    CharUnit,
)
from src._world.meld import get_meld_weight
from dataclasses import dataclass


class InvalidBeliefException(Exception):
    pass


@dataclass
class BeliefUnit(BeliefCore):
    _char_mirror: bool = None  # set by WorldUnit.set_charunit()
    _chars: dict[CharID, CharLink] = None  # set by WorldUnit.set_charunit()
    _road_delimiter: str = None  # calculated by WorldUnit.set_beliefunit
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
            x_dict["_chars"] = self.get_chars_dict()

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

    def get_chars_dict(self) -> dict[str, str]:
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

    def meld(self, exterior_belief):
        self._meld_attributes_that_must_be_equal(exterior_belief=exterior_belief)
        self.meld_charlinks(exterior_belief=exterior_belief)

    def meld_charlinks(self, exterior_belief):
        for oba in exterior_belief._chars.values():
            if self._chars.get(oba.char_id) is None:
                self._chars[oba.char_id] = oba
            else:
                self._chars[oba.char_id].meld(oba)

    def _meld_attributes_that_must_be_equal(self, exterior_belief):
        xl = [("belief_id", self.belief_id, exterior_belief.belief_id)]
        while xl != []:
            attrs = xl.pop()
            if attrs[1] != attrs[2]:
                raise InvalidBeliefException(
                    f"Meld fail BeliefUnit {self.belief_id} .{attrs[0]}='{attrs[1]}' not the equal as .{attrs[0]}='{attrs[2]}"
                )

        # if self.belief_id != exterior_belief.belief_id:
        #     raise InvalidBeliefException(
        #             f"Meld fail idea={self.get_road()} {attrs[0]}:{attrs[1]} with {exterior_idea.get_road()} {attrs[0]}:{attrs[2]}"
        #     )


# class BeliefUnitsshop:
def get_from_json(beliefunits_json: str) -> dict[BeliefID, BeliefUnit]:
    beliefunits_dict = get_dict_from_json(json_x=beliefunits_json)
    return get_beliefunits_from_dict(x_dict=beliefunits_dict)


def get_beliefunits_from_dict(
    x_dict: dict, _road_delimiter: str = None
) -> dict[BeliefID, BeliefUnit]:
    beliefunits = {}
    for beliefunit_dict in x_dict.values():
        x_belief = get_beliefunit_from_dict(beliefunit_dict, _road_delimiter)
        beliefunits[x_belief.belief_id] = x_belief
    return beliefunits


def get_beliefunit_from_dict(
    beliefunit_dict: dict, _road_delimiter: str = None
) -> BeliefUnit:
    return beliefunit_shop(
        belief_id=beliefunit_dict["belief_id"],
        _char_mirror=get_obj_from_beliefunit_dict(beliefunit_dict, "_char_mirror"),
        _chars=get_obj_from_beliefunit_dict(beliefunit_dict, "_chars"),
        _road_delimiter=_road_delimiter,
    )


def get_obj_from_beliefunit_dict(x_dict: dict[str,], dict_key: str) -> any:
    if dict_key == "_chars":
        return charlinks_get_from_dict(x_dict.get(dict_key))
    elif dict_key in {"_char_mirror"}:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else False
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else None


def beliefunit_shop(
    belief_id: BeliefID,
    _char_mirror: bool = None,
    _chars: dict[CharID, CharLink] = None,
    _road_delimiter: str = None,
) -> BeliefUnit:
    if _char_mirror is None:
        _char_mirror = False
    x_beliefunit = BeliefUnit(
        _char_mirror=_char_mirror,
        _chars=get_empty_dict_if_none(_chars),
        _world_cred=get_0_if_None(),
        _world_debt=get_0_if_None(),
        _world_agenda_cred=get_0_if_None(),
        _world_agenda_debt=get_0_if_None(),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )
    x_beliefunit.set_belief_id(belief_id=belief_id)
    return x_beliefunit


@dataclass
class FiscalLink(BeliefCore):
    credor_weight: float = 1.0
    debtor_weight: float = 1.0

    def get_dict(self) -> dict[str, str]:
        return {
            "belief_id": self.belief_id,
            "credor_weight": self.credor_weight,
            "debtor_weight": self.debtor_weight,
        }

    def meld(
        self,
        exterior_fiscallink,
        exterior_meld_strategy: str,
        src_meld_strategy: str,
    ):
        self.credor_weight = get_meld_weight(
            src_weight=self.credor_weight,
            src_meld_strategy=src_meld_strategy,
            exterior_weight=exterior_fiscallink.credor_weight,
            exterior_meld_strategy=exterior_meld_strategy,
        )
        self.debtor_weight = get_meld_weight(
            src_weight=self.debtor_weight,
            src_meld_strategy=src_meld_strategy,
            exterior_weight=exterior_fiscallink.debtor_weight,
            exterior_meld_strategy=exterior_meld_strategy,
        )


# class FiscalLinksshop:
def fiscallinks_get_from_json(fiscallinks_json: str) -> dict[BeliefID, FiscalLink]:
    fiscallinks_dict = get_dict_from_json(json_x=fiscallinks_json)
    return fiscallinks_get_from_dict(x_dict=fiscallinks_dict)


def fiscallinks_get_from_dict(x_dict: dict) -> dict[BeliefID, FiscalLink]:
    fiscallinks = {}
    for fiscallinks_dict in x_dict.values():
        x_belief = fiscallink_shop(
            belief_id=fiscallinks_dict["belief_id"],
            credor_weight=fiscallinks_dict["credor_weight"],
            debtor_weight=fiscallinks_dict["debtor_weight"],
        )
        fiscallinks[x_belief.belief_id] = x_belief
    return fiscallinks


def fiscallink_shop(
    belief_id: BeliefID, credor_weight: float = None, debtor_weight: float = None
) -> FiscalLink:
    credor_weight = get_1_if_None(credor_weight)
    debtor_weight = get_1_if_None(debtor_weight)
    return FiscalLink(belief_id, credor_weight, debtor_weight=debtor_weight)


@dataclass
class FiscalHeir(BeliefCore):
    credor_weight: float = 1.0
    debtor_weight: float = 1.0
    _world_cred: float = None
    _world_debt: float = None

    def set_world_cred_debt(
        self,
        idea_world_importance,
        fiscalheirs_credor_weight_sum: float,
        fiscalheirs_debtor_weight_sum: float,
    ):
        credor_importance_ratio = self.credor_weight / fiscalheirs_credor_weight_sum
        self._world_cred = idea_world_importance * credor_importance_ratio
        debtor_importance_ratio = self.debtor_weight / fiscalheirs_debtor_weight_sum
        self._world_debt = idea_world_importance * debtor_importance_ratio


def fiscalheir_shop(
    belief_id: BeliefID,
    credor_weight: float = None,
    debtor_weight: float = None,
    _world_cred: float = None,
    _world_debt: float = None,
) -> FiscalHeir:
    credor_weight = get_1_if_None(credor_weight)
    debtor_weight = get_1_if_None(debtor_weight)
    return FiscalHeir(belief_id, credor_weight, debtor_weight, _world_cred, _world_debt)


@dataclass
class FiscalLine(BeliefCore):
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


def fiscalline_shop(belief_id: BeliefID, _world_cred: float, _world_debt: float):
    return FiscalLine(belief_id, _world_cred=_world_cred, _world_debt=_world_debt)


def get_intersection_of_chars(
    chars_x: dict[CharID, CharUnit], chars_y: dict[CharID, CharUnit]
) -> dict[CharID, int]:
    x_set = set(chars_x)
    y_set = set(chars_y)
    intersection_x = x_set.intersection(y_set)
    return {char_id_x: -1 for char_id_x in intersection_x}


def get_chars_relevant_beliefs(
    beliefs_x: dict[BeliefID, BeliefUnit], chars_x: dict[CharID, CharUnit]
) -> dict[BeliefID, dict[CharID, int]]:
    relevant_beliefs = {}
    for char_id_x in chars_x:
        for belief_x in beliefs_x.values():
            if belief_x._chars.get(char_id_x) != None:
                if relevant_beliefs.get(belief_x.belief_id) is None:
                    relevant_beliefs[belief_x.belief_id] = {}
                relevant_beliefs.get(belief_x.belief_id)[char_id_x] = -1

    return relevant_beliefs
