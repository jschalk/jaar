from src._instrument.python import get_1_if_None
from dataclasses import dataclass


class BeliefID(str):  # Created to help track the concept
    pass


@dataclass
class BeliefCore:
    belief_id: BeliefID = None


@dataclass
class BeliefHold(BeliefCore):
    credor_weight: float = 1.0
    debtor_weight: float = 1.0

    def get_dict(self) -> dict[str, str]:
        return {
            "belief_id": self.belief_id,
            "credor_weight": self.credor_weight,
            "debtor_weight": self.debtor_weight,
        }


def beliefhold_shop(
    belief_id: BeliefID, credor_weight: float = None, debtor_weight: float = None
) -> BeliefHold:
    credor_weight = get_1_if_None(credor_weight)
    debtor_weight = get_1_if_None(debtor_weight)
    return BeliefHold(
        belief_id=belief_id, credor_weight=credor_weight, debtor_weight=debtor_weight
    )


def beliefhold_get_from_dict(x_dict: dict) -> BeliefHold:
    return beliefhold_shop(
        belief_id=x_dict.get("belief_id"),
        credor_weight=x_dict.get("credor_weight"),
        debtor_weight=x_dict.get("debtor_weight"),
    )


def beliefholds_get_from_dict(x_dict: dict) -> dict[BeliefID, BeliefHold]:
    return {
        x_belief_id: beliefhold_get_from_dict(x_beliefhold_dict)
        for x_belief_id, x_beliefhold_dict in x_dict.items()
    }
