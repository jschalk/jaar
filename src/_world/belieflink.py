from src._instrument.python import get_1_if_None as get1ifNone
from src._road.road import CharID
from dataclasses import dataclass


class BeliefID(str):  # Created to help track the concept
    pass


@dataclass
class BeliefCore:
    belief_id: BeliefID = None


@dataclass
class BeliefLink(BeliefCore):
    credor_weight: float = 1.0
    debtor_weight: float = 1.0
    # calculated fields
    _credor_pool: float = None
    _debtor_pool: float = None
    _char_id: CharID = None

    def set_credor_weight(self, x_credor_weight: float):
        if x_credor_weight != None:
            self.credor_weight = x_credor_weight

    def set_debtor_weight(self, x_debtor_weight: float):
        if x_debtor_weight != None:
            self.debtor_weight = x_debtor_weight

    def get_dict(self) -> dict[str, str]:
        return {
            "belief_id": self.belief_id,
            "credor_weight": self.credor_weight,
            "debtor_weight": self.debtor_weight,
        }


def belieflink_shop(
    belief_id: BeliefID,
    credor_weight: float = None,
    debtor_weight: float = None,
    _char_id: CharID = None,
) -> BeliefLink:
    return BeliefLink(
        belief_id=belief_id,
        credor_weight=get1ifNone(credor_weight),
        debtor_weight=get1ifNone(debtor_weight),
        _credor_pool=0,
        _debtor_pool=0,
        _char_id=_char_id,
    )


def belieflink_get_from_dict(x_dict: dict, x_char_id: CharID) -> BeliefLink:
    return belieflink_shop(
        belief_id=x_dict.get("belief_id"),
        credor_weight=x_dict.get("credor_weight"),
        debtor_weight=x_dict.get("debtor_weight"),
        _char_id=x_char_id,
    )


def belieflinks_get_from_dict(
    x_dict: dict, x_char_id: CharID
) -> dict[BeliefID, BeliefLink]:
    return {
        x_belief_id: belieflink_get_from_dict(x_belieflink_dict, x_char_id)
        for x_belief_id, x_belieflink_dict in x_dict.items()
    }
