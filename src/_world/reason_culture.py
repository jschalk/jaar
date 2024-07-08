from src._instrument.python import get_empty_set_if_none
from src._world.beliefunit import BeliefUnit, BeliefID
from src._world.char import CharID
from dataclasses import dataclass


class InvalidCultureHeirPopulateException(Exception):
    pass


@dataclass
class CultureUnit:
    _belieflinks: set[BeliefID]

    def get_dict(self) -> dict[str, str]:
        return {"_belieflinks": list(self._belieflinks)}

    def set_belieflink(self, belief_id: BeliefID):
        self._belieflinks.add(belief_id)

    def belieflink_exists(self, belief_id: BeliefID):
        return belief_id in self._belieflinks

    def del_belieflink(self, belief_id: BeliefID):
        self._belieflinks.remove(belief_id)

    def get_belieflink(self, belief_id: BeliefID) -> BeliefID:
        if self.belieflink_exists(belief_id):
            return belief_id


def cultureunit_shop(_belieflinks: set[BeliefID] = None) -> CultureUnit:
    return CultureUnit(get_empty_set_if_none(_belieflinks))


def create_cultureunit(belieflink: BeliefID):
    x_cultureunit = cultureunit_shop()
    x_cultureunit.set_belieflink(belieflink)
    return x_cultureunit


@dataclass
class CultureHeir:
    _belieflinks: set[BeliefID]
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
        return self._get_all_chars(world_beliefs, self._belieflinks)

    def is_empty(self) -> bool:
        return self._belieflinks == set()

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

    def set_belieflinks(
        self,
        parent_cultureheir,
        cultureunit: CultureUnit,
        world_beliefs: dict[BeliefID, BeliefUnit],
    ):
        x_belieflinks = set()
        if parent_cultureheir is None or parent_cultureheir._belieflinks == set():
            for belieflink in cultureunit._belieflinks:
                x_belieflinks.add(belieflink)
        elif cultureunit._belieflinks == set() or (
            parent_cultureheir._belieflinks == cultureunit._belieflinks
        ):
            for belieflink in parent_cultureheir._belieflinks:
                x_belieflinks.add(belieflink)
        else:
            # get all_chars of parent cultureheir beliefs
            all_parent_cultureheir_chars = self._get_all_chars(
                world_beliefs=world_beliefs,
                belief_id_set=parent_cultureheir._belieflinks,
            )
            # get all_chars of cultureunit beliefs
            all_cultureunit_chars = self._get_all_chars(
                world_beliefs=world_beliefs,
                belief_id_set=cultureunit._belieflinks,
            )
            if not set(all_cultureunit_chars).issubset(
                set(all_parent_cultureheir_chars)
            ):
                # else raise error
                raise InvalidCultureHeirPopulateException(
                    f"parent_cultureheir does not contain all chars of the idea's cultureunit\n{set(all_parent_cultureheir_chars)=}\n\n{set(all_cultureunit_chars)=}"
                )

            # set dict_x = to cultureunit beliefs
            for belieflink in cultureunit._belieflinks:
                x_belieflinks.add(belieflink)
        self._belieflinks = x_belieflinks

    def has_belief(self, belief_ids: set[BeliefID]):
        return self.is_empty() or any(gn_x in self._belieflinks for gn_x in belief_ids)


def cultureheir_shop(
    _belieflinks: set[BeliefID] = None, _owner_id_culture: bool = None
) -> CultureHeir:
    _belieflinks = get_empty_set_if_none(_belieflinks)
    if _owner_id_culture is None:
        _owner_id_culture = False

    return CultureHeir(_belieflinks=_belieflinks, _owner_id_culture=_owner_id_culture)


def cultureunit_get_from_dict(cultureunit_dict: dict) -> CultureUnit:
    x_cultureunit = cultureunit_shop()
    for x_belief_id in cultureunit_dict.get("_belieflinks"):
        x_cultureunit.set_belieflink(x_belief_id)

    return x_cultureunit
