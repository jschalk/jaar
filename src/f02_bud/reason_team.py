from src.a00_data_toolboxs.dict_toolbox import get_empty_set_if_None
from src.f02_bud.group import GroupUnit, GroupLabel
from src.f02_bud.acct import AcctName
from dataclasses import dataclass


class InvalidTeamHeirPopulateException(Exception):
    pass


@dataclass
class TeamUnit:
    _teamlinks: set[GroupLabel]

    def get_dict(self) -> dict[str, str]:
        return {"_teamlinks": list(self._teamlinks)}

    def set_teamlink(self, team_tag: GroupLabel):
        self._teamlinks.add(team_tag)

    def teamlink_exists(self, team_tag: GroupLabel):
        return team_tag in self._teamlinks

    def del_teamlink(self, team_tag: GroupLabel):
        self._teamlinks.remove(team_tag)

    def get_teamlink(self, team_tag: GroupLabel) -> GroupLabel:
        if self.teamlink_exists(team_tag):
            return team_tag


def teamunit_shop(_teamlinks: set[GroupLabel] = None) -> TeamUnit:
    return TeamUnit(get_empty_set_if_None(_teamlinks))


def create_teamunit(teamlink: GroupLabel):
    x_teamunit = teamunit_shop()
    x_teamunit.set_teamlink(teamlink)
    return x_teamunit


@dataclass
class TeamHeir:
    _teamlinks: set[GroupLabel]
    _owner_name_team: bool

    def _get_all_accts(
        self,
        bud_groupunits: dict[GroupLabel, GroupUnit],
        team_tag_set: set[GroupLabel],
    ) -> dict[GroupLabel, GroupUnit]:
        dict_x = {}
        for x_team_tag in team_tag_set:
            dict_x |= bud_groupunits.get(x_team_tag)._memberships
        return dict_x

    def is_empty(self) -> bool:
        return self._teamlinks == set()

    def set_owner_name_team(
        self, bud_groupunits: dict[GroupLabel, GroupUnit], bud_owner_name: AcctName
    ):
        self._owner_name_team = self.get_owner_name_team_bool(
            bud_groupunits, bud_owner_name
        )

    def get_owner_name_team_bool(
        self, bud_groupunits: dict[GroupLabel, GroupUnit], bud_owner_name: AcctName
    ) -> bool:
        if self._teamlinks == set():
            return True

        for x_team_tag, x_groupunit in bud_groupunits.items():
            if x_team_tag in self._teamlinks:
                for x_acct_name in x_groupunit._memberships.keys():
                    if x_acct_name == bud_owner_name:
                        return True
        return False

    def set_teamlinks(
        self,
        parent_teamheir,
        teamunit: TeamUnit,
        bud_groupunits: dict[GroupLabel, GroupUnit],
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
            # get all_accts of parent teamheir groupunits
            all_parent_teamheir_accts = self._get_all_accts(
                bud_groupunits=bud_groupunits,
                team_tag_set=parent_teamheir._teamlinks,
            )
            # get all_accts of teamunit groupunits
            all_teamunit_accts = self._get_all_accts(
                bud_groupunits=bud_groupunits,
                team_tag_set=teamunit._teamlinks,
            )
            if not set(all_teamunit_accts).issubset(set(all_parent_teamheir_accts)):
                # else raise error
                raise InvalidTeamHeirPopulateException(
                    f"parent_teamheir does not contain all accts of the item's teamunit\n{set(all_parent_teamheir_accts)=}\n\n{set(all_teamunit_accts)=}"
                )

            # set dict_x = to teamunit groupunits
            for teamlink in teamunit._teamlinks:
                x_teamlinks.add(teamlink)
        self._teamlinks = x_teamlinks

    def has_team(self, team_tags: set[GroupLabel]):
        return self.is_empty() or any(gn_x in self._teamlinks for gn_x in team_tags)


def teamheir_shop(
    _teamlinks: set[GroupLabel] = None, _owner_name_team: bool = None
) -> TeamHeir:
    _teamlinks = get_empty_set_if_None(_teamlinks)
    if _owner_name_team is None:
        _owner_name_team = False

    return TeamHeir(_teamlinks=_teamlinks, _owner_name_team=_owner_name_team)


def teamunit_get_from_dict(teamunit_dict: dict) -> TeamUnit:
    x_teamunit = teamunit_shop()
    for x_team_tag in teamunit_dict.get("_teamlinks"):
        x_teamunit.set_teamlink(x_team_tag)

    return x_teamunit
