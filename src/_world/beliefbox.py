from src._instrument.python import get_1_if_None, get_dict_from_json
from src._road.road import BeliefID, CharID, default_road_delimiter_if_none
from src._world.belieflink import BeliefCore, BeliefLink
from dataclasses import dataclass


class InvalidBeliefException(Exception):
    pass


class belieflink_belief_id_Exception(Exception):
    pass


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


@dataclass
class BeliefBox(BeliefCore):
    _belieflinks: dict[CharID, BeliefLink] = None  # set by WorldUnit.set_charunit()
    _road_delimiter: str = None  # calculated by WorldUnit
    # calculated by WorldUnit.calc_world_metrics()
    _world_cred: float = None
    _world_debt: float = None
    _world_agenda_cred: float = None
    _world_agenda_debt: float = None
    _credor_pool: float = None
    _debtor_pool: float = None

    def set_belieflink(self, x_belieflink: BeliefLink):
        if x_belieflink.belief_id != self.belief_id:
            raise belieflink_belief_id_Exception(
                f"BeliefBox.belief_id={self.belief_id} cannot set belieflink.belief_id={x_belieflink.belief_id}"
            )
        if x_belieflink._char_id is None:
            raise belieflink_belief_id_Exception(
                f"belieflink belief_id={x_belieflink.belief_id} cannot be set when _char_id is None."
            )

        self._belieflinks[x_belieflink._char_id] = x_belieflink
        self._add_credor_pool(x_belieflink._credor_pool)
        self._add_debtor_pool(x_belieflink._debtor_pool)

    def _add_credor_pool(self, x_credor_pool: float):
        self._credor_pool += x_credor_pool

    def _add_debtor_pool(self, x_debtor_pool: float):
        self._debtor_pool += x_debtor_pool

    def get_belieflink(self, x_char_id: CharID) -> BeliefLink:
        return self._belieflinks.get(x_char_id)

    def belieflink_exists(self, x_char_id: CharID) -> bool:
        return self.get_belieflink(x_char_id) != None

    def del_belieflink(self, char_id):
        self._belieflinks.pop(char_id)

    def reset_world_cred_debt(self):
        self._world_cred = 0
        self._world_debt = 0
        self._world_agenda_cred = 0
        self._world_agenda_debt = 0
        for belieflink in self._belieflinks.values():
            belieflink.reset_world_cred_debt()

    def _set_belieflink_world_cred_debt(self):
        belieflinks_credor_weight_sum = sum(
            belieflink.credor_weight for belieflink in self._belieflinks.values()
        )
        belieflinks_debtor_weight_sum = sum(
            belieflink.debtor_weight for belieflink in self._belieflinks.values()
        )

        for belieflink in self._belieflinks.values():
            belieflink.set_world_cred_debt(
                belieflinks_credor_weight_sum=belieflinks_credor_weight_sum,
                belieflinks_debtor_weight_sum=belieflinks_debtor_weight_sum,
                belief_world_cred=self._world_cred,
                belief_world_debt=self._world_debt,
                belief_world_agenda_cred=self._world_agenda_cred,
                belief_world_agenda_debt=self._world_agenda_debt,
            )


def beliefbox_shop(belief_id: BeliefID, _road_delimiter: str = None) -> BeliefBox:
    return BeliefBox(
        belief_id=belief_id,
        _belieflinks={},
        _world_cred=0,
        _world_debt=0,
        _world_agenda_cred=0,
        _world_agenda_debt=0,
        _credor_pool=0,
        _debtor_pool=0,
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )
    # x_beliefbox.set_belief_id(belief_id=belief_id)
    # return x_beliefbox
