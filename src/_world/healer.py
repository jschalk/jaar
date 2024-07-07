from src._instrument.python import get_empty_set_if_none
from src._world.beliefunit import BeliefID
from dataclasses import dataclass


@dataclass
class HealerHold:
    _belief_ids: set[BeliefID]

    def set_belief_id(self, x_belief_id: BeliefID):
        self._belief_ids.add(x_belief_id)

    def belief_id_exists(self, x_belief_id: BeliefID) -> bool:
        return x_belief_id in self._belief_ids

    def any_belief_id_exists(self) -> bool:
        return len(self._belief_ids) > 0

    def del_belief_id(self, x_belief_id: BeliefID):
        self._belief_ids.remove(x_belief_id)

    def get_dict(self):
        return {"healerhold_belief_ids": list(self._belief_ids)}


def healerhold_shop(_belief_ids: set[BeliefID] = None) -> HealerHold:
    return HealerHold(_belief_ids=get_empty_set_if_none(_belief_ids))


def healerhold_get_from_dict(x_dict: dict[str, set]) -> HealerHold:
    x_healerhold = healerhold_shop()
    if x_dict.get("healerhold_belief_ids") != None:
        for x_belief_id in x_dict.get("healerhold_belief_ids"):
            x_healerhold.set_belief_id(x_belief_id=x_belief_id)
    return x_healerhold
