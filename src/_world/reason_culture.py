from src._instrument.python import get_empty_set_if_none
from src._world.beliefunit import BeliefUnit, BeliefID
from src._world.char import CharID
from dataclasses import dataclass


class InvalidCultureHeirPopulateException(Exception):
    pass


@dataclass
class CultureUnit:
    _allyholds: set[BeliefID]

    def get_dict(self) -> dict[str, str]:
        return {"_allyholds": list(self._allyholds)}

    def set_allyhold(self, belief_id: BeliefID):
        self._allyholds.add(belief_id)

    def allyhold_exists(self, belief_id: BeliefID):
        return belief_id in self._allyholds

    def del_allyhold(self, belief_id: BeliefID):
        self._allyholds.remove(belief_id)

    def get_allyhold(self, belief_id: BeliefID) -> BeliefID:
        if self.allyhold_exists(belief_id):
            return belief_id


def cultureunit_shop(_allyholds: set[BeliefID] = None) -> CultureUnit:
    return CultureUnit(get_empty_set_if_none(_allyholds))


def create_cultureunit(allyhold: BeliefID):
    x_cultureunit = cultureunit_shop()
    x_cultureunit.set_allyhold(allyhold)
    return x_cultureunit


@dataclass
class CultureHeir:
    _allyholds: set[BeliefID]
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
        return self._get_all_chars(world_beliefs, self._allyholds)

    def is_empty(self) -> bool:
        return self._allyholds == set()

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

    def set_allyholds(
        self,
        parent_cultureheir,
        cultureunit: CultureUnit,
        world_beliefs: dict[BeliefID, BeliefUnit],
    ):
        x_allyholds = set()
        if parent_cultureheir is None or parent_cultureheir._allyholds == set():
            for allyhold in cultureunit._allyholds:
                x_allyholds.add(allyhold)
        elif cultureunit._allyholds == set() or (
            parent_cultureheir._allyholds == cultureunit._allyholds
        ):
            for allyhold in parent_cultureheir._allyholds:
                x_allyholds.add(allyhold)
        else:
            # get all_chars of parent cultureheir beliefs
            all_parent_cultureheir_chars = self._get_all_chars(
                world_beliefs=world_beliefs,
                belief_id_set=parent_cultureheir._allyholds,
            )
            # get all_chars of cultureunit beliefs
            all_cultureunit_chars = self._get_all_chars(
                world_beliefs=world_beliefs,
                belief_id_set=cultureunit._allyholds,
            )
            if not set(all_cultureunit_chars).issubset(
                set(all_parent_cultureheir_chars)
            ):
                # else raise error
                raise InvalidCultureHeirPopulateException(
                    f"parent_cultureheir does not contain all chars of the idea's cultureunit\n{set(all_parent_cultureheir_chars)=}\n\n{set(all_cultureunit_chars)=}"
                )

            # set dict_x = to cultureunit beliefs
            for allyhold in cultureunit._allyholds:
                x_allyholds.add(allyhold)
        self._allyholds = x_allyholds

    def has_belief(self, belief_ids: set[BeliefID]):
        return self.is_empty() or any(gn_x in self._allyholds for gn_x in belief_ids)


def cultureheir_shop(
    _allyholds: set[BeliefID] = None, _owner_id_culture: bool = None
) -> CultureHeir:
    _allyholds = get_empty_set_if_none(_allyholds)
    if _owner_id_culture is None:
        _owner_id_culture = False

    return CultureHeir(_allyholds=_allyholds, _owner_id_culture=_owner_id_culture)


def cultureunit_get_from_dict(cultureunit_dict: dict) -> CultureUnit:
    x_cultureunit = cultureunit_shop()
    for x_belief_id in cultureunit_dict.get("_allyholds"):
        x_cultureunit.set_allyhold(x_belief_id)

    return x_cultureunit
