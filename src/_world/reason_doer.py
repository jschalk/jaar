from src._instrument.python import get_empty_set_if_none
from src._world.beliefbox import BeliefBox, BeliefID
from src._world.char import CharID, CharUnit
from dataclasses import dataclass


class InvalidDoerHeirPopulateException(Exception):
    pass


@dataclass
class DoerUnit:
    _beliefholds: set[BeliefID]

    def get_dict(self) -> dict[str, str]:
        return {"_beliefholds": list(self._beliefholds)}

    def set_beliefhold(self, belief_id: BeliefID):
        self._beliefholds.add(belief_id)

    def beliefhold_exists(self, belief_id: BeliefID):
        return belief_id in self._beliefholds

    def del_beliefhold(self, belief_id: BeliefID):
        self._beliefholds.remove(belief_id)

    def get_beliefhold(self, belief_id: BeliefID) -> BeliefID:
        if self.beliefhold_exists(belief_id):
            return belief_id


def doerunit_shop(_beliefholds: set[BeliefID] = None) -> DoerUnit:
    return DoerUnit(get_empty_set_if_none(_beliefholds))


def create_doerunit(beliefhold: BeliefID):
    x_doerunit = doerunit_shop()
    x_doerunit.set_beliefhold(beliefhold)
    return x_doerunit


@dataclass
class DoerHeir:
    _beliefholds: set[BeliefID]
    _owner_id_doer: bool

    def _get_all_chars(
        self,
        world_beliefs: dict[BeliefID, BeliefBox],
        belief_id_set: set[BeliefID],
    ) -> dict[BeliefID, BeliefBox]:
        dict_x = {}
        for belief_id_x in belief_id_set:
            dict_x |= world_beliefs.get(belief_id_x)._chars
        return dict_x

    def _get_all_suff_chars(
        self, world_beliefs: dict[BeliefID, BeliefBox]
    ) -> dict[BeliefID, BeliefBox]:
        return self._get_all_chars(world_beliefs, self._beliefholds)

    def is_empty(self) -> bool:
        return self._beliefholds == set()

    def set_owner_id_doer(
        self, world_beliefs: dict[BeliefID, BeliefBox], world_owner_id: CharID
    ):
        self._owner_id_doer = False
        if self.is_empty():
            self._owner_id_doer = True
        else:
            all_suff_chars_x = self._get_all_suff_chars(world_beliefs)
            if all_suff_chars_x.get(world_owner_id) != None:
                self._owner_id_doer = True

    def set_beliefholds(
        self,
        parent_doerheir,
        doerunit: DoerUnit,
        world_beliefs: dict[BeliefID, BeliefBox],
    ):
        x_beliefholds = set()
        if parent_doerheir is None or parent_doerheir._beliefholds == set():
            for beliefhold in doerunit._beliefholds:
                x_beliefholds.add(beliefhold)
        elif doerunit._beliefholds == set() or (
            parent_doerheir._beliefholds == doerunit._beliefholds
        ):
            for beliefhold in parent_doerheir._beliefholds:
                x_beliefholds.add(beliefhold)
        else:
            # get all_chars of parent doerheir beliefs
            all_parent_doerheir_chars = self._get_all_chars(
                world_beliefs=world_beliefs,
                belief_id_set=parent_doerheir._beliefholds,
            )
            # get all_chars of doerunit beliefs
            all_doerunit_chars = self._get_all_chars(
                world_beliefs=world_beliefs,
                belief_id_set=doerunit._beliefholds,
            )
            if not set(all_doerunit_chars).issubset(set(all_parent_doerheir_chars)):
                # else raise error
                raise InvalidDoerHeirPopulateException(
                    f"parent_doerheir does not contain all chars of the idea's doerunit\n{set(all_parent_doerheir_chars)=}\n\n{set(all_doerunit_chars)=}"
                )

            # set dict_x = to doerunit beliefs
            for beliefhold in doerunit._beliefholds:
                x_beliefholds.add(beliefhold)
        self._beliefholds = x_beliefholds

    def has_belief(self, belief_ids: set[BeliefID]):
        return self.is_empty() or any(gn_x in self._beliefholds for gn_x in belief_ids)


def doerheir_shop(
    _beliefholds: set[BeliefID] = None, _owner_id_doer: bool = None
) -> DoerHeir:
    _beliefholds = get_empty_set_if_none(_beliefholds)
    if _owner_id_doer is None:
        _owner_id_doer = False

    return DoerHeir(_beliefholds=_beliefholds, _owner_id_doer=_owner_id_doer)


def doerunit_get_from_dict(doerunit_dict: dict) -> DoerUnit:
    x_doerunit = doerunit_shop()
    for x_belief_id in doerunit_dict.get("_beliefholds"):
        x_doerunit.set_beliefhold(x_belief_id)

    return x_doerunit