from src._instrument.python import get_empty_set_if_none
from src._world.beliefunit import BeliefUnit, BeliefID
from src._world.char import CharID
from dataclasses import dataclass


class InvalidCultureHeirPopulateException(Exception):
    pass


@dataclass
class CultureUnit:
    _heldbeliefs: set[BeliefID]

    def get_dict(self) -> dict[str, str]:
        return {"_heldbeliefs": list(self._heldbeliefs)}

    def set_heldbelief(self, belief_id: BeliefID):
        self._heldbeliefs.add(belief_id)

    def heldbelief_exists(self, belief_id: BeliefID):
        return belief_id in self._heldbeliefs

    def del_heldbelief(self, belief_id: BeliefID):
        self._heldbeliefs.remove(belief_id)

    def get_heldbelief(self, belief_id: BeliefID) -> BeliefID:
        if self.heldbelief_exists(belief_id):
            return belief_id


def cultureunit_shop(_heldbeliefs: set[BeliefID] = None) -> CultureUnit:
    return CultureUnit(get_empty_set_if_none(_heldbeliefs))


def create_cultureunit(heldbelief: BeliefID):
    x_cultureunit = cultureunit_shop()
    x_cultureunit.set_heldbelief(heldbelief)
    return x_cultureunit


@dataclass
class CultureHeir:
    _heldbeliefs: set[BeliefID]
    _owner_id_culture: bool

    def _get_all_chars(
        self,
        world_beliefs: dict[BeliefID, BeliefUnit],
        belief_id_set: set[BeliefID],
    ) -> dict[BeliefID, BeliefUnit]:
        dict_x = {}
        for belief_id_x in belief_id_set:
            dict_x |= world_beliefs.get(belief_id_x)._chars
        return dict_x

    def _get_all_suff_chars(
        self, world_beliefs: dict[BeliefID, BeliefUnit]
    ) -> dict[BeliefID, BeliefUnit]:
        return self._get_all_chars(world_beliefs, self._heldbeliefs)

    def is_empty(self) -> bool:
        return self._heldbeliefs == set()

    def set_owner_id_culture(
        self, world_beliefs: dict[BeliefID, BeliefUnit], world_owner_id: CharID
    ):
        self._owner_id_culture = False
        if self.is_empty():
            self._owner_id_culture = True
        else:
            all_suff_chars_x = self._get_all_suff_chars(world_beliefs)
            if all_suff_chars_x.get(world_owner_id) != None:
                self._owner_id_culture = True

    def set_heldbeliefs(
        self,
        parent_cultureheir,
        cultureunit: CultureUnit,
        world_beliefs: dict[BeliefID, BeliefUnit],
    ):
        x_set = set()
        if parent_cultureheir is None or parent_cultureheir._heldbeliefs == set():
            for heldbelief in cultureunit._heldbeliefs:
                x_set.add(heldbelief)
        elif cultureunit._heldbeliefs == set() or (
            parent_cultureheir._heldbeliefs == cultureunit._heldbeliefs
        ):
            for heldbelief in parent_cultureheir._heldbeliefs:
                x_set.add(heldbelief)
        else:
            # get all_chars of parent cultureheir beliefs
            all_parent_cultureheir_chars = self._get_all_chars(
                world_beliefs=world_beliefs,
                belief_id_set=parent_cultureheir._heldbeliefs,
            )
            # get all_chars of cultureunit beliefs
            all_cultureunit_chars = self._get_all_chars(
                world_beliefs=world_beliefs,
                belief_id_set=cultureunit._heldbeliefs,
            )
            if not set(all_cultureunit_chars).issubset(
                set(all_parent_cultureheir_chars)
            ):
                # else raise error
                raise InvalidCultureHeirPopulateException(
                    f"parent_cultureheir does not contain all chars of the idea's cultureunit\n{set(all_parent_cultureheir_chars)=}\n\n{set(all_cultureunit_chars)=}"
                )

            # set dict_x = to cultureunit beliefs
            for heldbelief in cultureunit._heldbeliefs:
                x_set.add(heldbelief)
        self._heldbeliefs = x_set

    def belief_in(self, belief_ids: set[BeliefID]):
        return self.is_empty() or any(gn_x in self._heldbeliefs for gn_x in belief_ids)


def cultureheir_shop(
    _heldbeliefs: set[BeliefID] = None, _owner_id_culture: bool = None
) -> CultureHeir:
    _heldbeliefs = get_empty_set_if_none(_heldbeliefs)
    if _owner_id_culture is None:
        _owner_id_culture = False

    return CultureHeir(_heldbeliefs=_heldbeliefs, _owner_id_culture=_owner_id_culture)


def cultureunit_get_from_dict(cultureunit_dict: dict) -> CultureUnit:
    x_cultureunit = cultureunit_shop()
    for x_belief_id in cultureunit_dict.get("_heldbeliefs"):
        x_cultureunit.set_heldbelief(x_belief_id)

    return x_cultureunit
