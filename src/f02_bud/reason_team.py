from src.f00_instrument.dict_tool import get_empty_set_if_none
from src.f02_bud.group import GroupBox, GroupID
from src.f02_bud.acct import AcctID
from dataclasses import dataclass


class InvalidTeamHeirPopulateException(Exception):
    pass


@dataclass
class TeamUnit:
    _teamlinks: set[GroupID]

    def get_dict(self) -> dict[str, str]:
        return {"_teamlinks": list(self._teamlinks)}

    def set_teamlink(self, group_id: GroupID):
        self._teamlinks.add(group_id)

    def teamlink_exists(self, group_id: GroupID):
        return group_id in self._teamlinks

    def del_teamlink(self, group_id: GroupID):
        self._teamlinks.remove(group_id)

    def get_teamlink(self, group_id: GroupID) -> GroupID:
        if self.teamlink_exists(group_id):
            return group_id


def teamunit_shop(_teamlinks: set[GroupID] = None) -> TeamUnit:
    return TeamUnit(get_empty_set_if_none(_teamlinks))


def create_teamunit(teamlink: GroupID):
    x_teamunit = teamunit_shop()
    x_teamunit.set_teamlink(teamlink)
    return x_teamunit


@dataclass
class TeamHeir:
    _teamlinks: set[GroupID]
    _owner_id_team: bool

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
        return self._teamlinks == set()

    def set_owner_id_team(
        self, bud_groupboxs: dict[GroupID, GroupBox], bud_owner_id: AcctID
    ):
        self._owner_id_team = self.get_owner_id_team_bool(bud_groupboxs, bud_owner_id)

    def get_owner_id_team_bool(
        self, bud_groupboxs: dict[GroupID, GroupBox], bud_owner_id: AcctID
    ) -> bool:
        if self._teamlinks == set():
            return True

        for x_group_id, x_groupbox in bud_groupboxs.items():
            if x_group_id in self._teamlinks:
                for x_acct_id in x_groupbox._memberships.keys():
                    if x_acct_id == bud_owner_id:
                        return True
        return False

    def set_teamlinks(
        self,
        parent_teamheir,
        teamunit: TeamUnit,
        bud_groupboxs: dict[GroupID, GroupBox],
    ):
        x_teamlinks = set()
        if parent_teamheir is None or parent_teamheir._teamlinks == set():
            for teamlink in teamunit._teamlinks:
                x_teamlinks.add(teamlink)
        elif teamunit._teamlinks == set() or (
            parent_teamheir._teamlinks == teamunit._teamlinks
        ):
            for teamlink in parent_teamheir._teamlinks:
                x_teamlinks.add(teamlink)
        else:
            # get all_accts of parent teamheir groupboxs
            all_parent_teamheir_accts = self._get_all_accts(
                bud_groupboxs=bud_groupboxs,
                group_id_set=parent_teamheir._teamlinks,
            )
            # get all_accts of teamunit groupboxs
            all_teamunit_accts = self._get_all_accts(
                bud_groupboxs=bud_groupboxs,
                group_id_set=teamunit._teamlinks,
            )
            if not set(all_teamunit_accts).issubset(set(all_parent_teamheir_accts)):
                # else raise error
                raise InvalidTeamHeirPopulateException(
                    f"parent_teamheir does not contain all accts of the item's teamunit\n{set(all_parent_teamheir_accts)=}\n\n{set(all_teamunit_accts)=}"
                )

            # set dict_x = to teamunit groupboxs
            for teamlink in teamunit._teamlinks:
                x_teamlinks.add(teamlink)
        self._teamlinks = x_teamlinks

    def has_group(self, group_ids: set[GroupID]):
        return self.is_empty() or any(gn_x in self._teamlinks for gn_x in group_ids)


def teamheir_shop(
    _teamlinks: set[GroupID] = None, _owner_id_team: bool = None
) -> TeamHeir:
    _teamlinks = get_empty_set_if_none(_teamlinks)
    if _owner_id_team is None:
        _owner_id_team = False

    return TeamHeir(_teamlinks=_teamlinks, _owner_id_team=_owner_id_team)


def teamunit_get_from_dict(teamunit_dict: dict) -> TeamUnit:
    x_teamunit = teamunit_shop()
    for x_group_id in teamunit_dict.get("_teamlinks"):
        x_teamunit.set_teamlink(x_group_id)

    return x_teamunit