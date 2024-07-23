from src._instrument.python import get_empty_set_if_none
from src.bud.group import GroupBox, GroupID
from src.bud.acct import AcctID
from dataclasses import dataclass


class InvalidDoerHeirPopulateException(Exception):
    pass


@dataclass
class DoerUnit:
    _groupholds: set[GroupID]

    def get_dict(self) -> dict[str, str]:
        return {"_groupholds": list(self._groupholds)}

    def set_grouphold(self, group_id: GroupID):
        self._groupholds.add(group_id)

    def grouphold_exists(self, group_id: GroupID):
        return group_id in self._groupholds

    def del_grouphold(self, group_id: GroupID):
        self._groupholds.remove(group_id)

    def get_grouphold(self, group_id: GroupID) -> GroupID:
        if self.grouphold_exists(group_id):
            return group_id


def doerunit_shop(_groupholds: set[GroupID] = None) -> DoerUnit:
    return DoerUnit(get_empty_set_if_none(_groupholds))


def create_doerunit(grouphold: GroupID):
    x_doerunit = doerunit_shop()
    x_doerunit.set_grouphold(grouphold)
    return x_doerunit


@dataclass
class DoerHeir:
    _groupholds: set[GroupID]
    _owner_id_doer: bool

    def _get_all_accts(
        self,
        bud_groupboxs: dict[GroupID, GroupBox],
        group_id_set: set[GroupID],
    ) -> dict[GroupID, GroupBox]:
        dict_x = {}
        for group_id_x in group_id_set:
            dict_x |= bud_groupboxs.get(group_id_x)._memberships
        return dict_x

    def is_empty(self) -> bool:
        return self._groupholds == set()

    def set_owner_id_doer(
        self, bud_groupboxs: dict[GroupID, GroupBox], bud_owner_id: AcctID
    ):
        self._owner_id_doer = self.get_owner_id_doer_bool(bud_groupboxs, bud_owner_id)

    def get_owner_id_doer_bool(
        self, bud_groupboxs: dict[GroupID, GroupBox], bud_owner_id: AcctID
    ) -> bool:
        if self._groupholds == set():
            return True

        for x_group_id, x_groupbox in bud_groupboxs.items():
            if x_group_id in self._groupholds:
                for x_acct_id in x_groupbox._memberships.keys():
                    if x_acct_id == bud_owner_id:
                        return True
        return False

    def set_groupholds(
        self,
        parent_doerheir,
        doerunit: DoerUnit,
        bud_groupboxs: dict[GroupID, GroupBox],
    ):
        x_groupholds = set()
        if parent_doerheir is None or parent_doerheir._groupholds == set():
            for grouphold in doerunit._groupholds:
                x_groupholds.add(grouphold)
        elif doerunit._groupholds == set() or (
            parent_doerheir._groupholds == doerunit._groupholds
        ):
            for grouphold in parent_doerheir._groupholds:
                x_groupholds.add(grouphold)
        else:
            # get all_accts of parent doerheir groupboxs
            all_parent_doerheir_accts = self._get_all_accts(
                bud_groupboxs=bud_groupboxs,
                group_id_set=parent_doerheir._groupholds,
            )
            # get all_accts of doerunit groupboxs
            all_doerunit_accts = self._get_all_accts(
                bud_groupboxs=bud_groupboxs,
                group_id_set=doerunit._groupholds,
            )
            if not set(all_doerunit_accts).issubset(set(all_parent_doerheir_accts)):
                # else raise error
                raise InvalidDoerHeirPopulateException(
                    f"parent_doerheir does not contain all accts of the idea's doerunit\n{set(all_parent_doerheir_accts)=}\n\n{set(all_doerunit_accts)=}"
                )

            # set dict_x = to doerunit groupboxs
            for grouphold in doerunit._groupholds:
                x_groupholds.add(grouphold)
        self._groupholds = x_groupholds

    def has_group(self, group_ids: set[GroupID]):
        return self.is_empty() or any(gn_x in self._groupholds for gn_x in group_ids)


def doerheir_shop(
    _groupholds: set[GroupID] = None, _owner_id_doer: bool = None
) -> DoerHeir:
    _groupholds = get_empty_set_if_none(_groupholds)
    if _owner_id_doer is None:
        _owner_id_doer = False

    return DoerHeir(_groupholds=_groupholds, _owner_id_doer=_owner_id_doer)


def doerunit_get_from_dict(doerunit_dict: dict) -> DoerUnit:
    x_doerunit = doerunit_shop()
    for x_group_id in doerunit_dict.get("_groupholds"):
        x_doerunit.set_grouphold(x_group_id)

    return x_doerunit
