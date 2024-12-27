from src.f01_road.jaar_config import default_unknown_word_if_None
from src.f00_instrument.dict_toolbox import (
    get_0_if_None,
    get_json_from_dict,
    get_dict_from_json,
)
from src.f01_road.road import default_wall_if_None, OwnerID, EventID
from src.f08_pidgin.map import (
    MapCore,
    GroupMap,
    AcctMap,
    IdeaMap,
    RoadMap,
    groupmap_shop,
    acctmap_shop,
    ideamap_shop,
    roadmap_shop,
    get_acctmap_from_dict,
    get_groupmap_from_dict,
    get_ideamap_from_dict,
    get_roadmap_from_dict,
    inherit_acctmap,
    inherit_groupmap,
    inherit_ideamap,
    inherit_roadmap,
)
from dataclasses import dataclass


class check_attrException(Exception):
    pass


def pidginable_jaar_types() -> set:
    return {"AcctID", "GroupID", "IdeaUnit", "RoadUnit"}


def pidginable_atom_args() -> set:
    return {
        "acct_id",
        "awardee_id",
        "base",
        "face_id",
        "deal_id",
        "group_id",
        "healer_id",
        "hour_lx",
        "lx",
        "month_lx",
        "parent_road",
        "pick",
        "need",
        "owner_id",
        "road",
        "team_id",
        "timeline_lx",
        "weekday_lx",
    }


@dataclass
class PidginUnit:
    """Per face object that translates any translatable str.
    otx is the reference for the outside, what the face says
    inx is the reference for the inside, what the same inteprets from the face
    Contains a mapunit for each translatable type: RoadUnit, AcctID, GroupID...
    """

    event_id: EventID = None
    face_id: OwnerID = None
    groupmap: GroupMap = None
    acctmap: AcctMap = None
    ideamap: IdeaMap = None
    roadmap: RoadMap = None
    unknown_word: str = None  # pidginunit heart
    otx_wall: str = None  # pidginunit heart
    inx_wall: str = None  # pidginunit heart

    def set_groupmap(self, x_groupmap: GroupMap):
        self._check_all_core_attrs_match(x_groupmap)
        self.groupmap = x_groupmap

    def get_groupmap(self) -> GroupMap:
        return self.groupmap

    def set_group_id(self, otx_group_id: str, inx_group_id: str):
        self.groupmap.set_otx2inx(otx_group_id, inx_group_id)

    def group_id_exists(self, otx_group_id: str, inx_group_id: str):
        return self.groupmap.otx2inx_exists(otx_group_id, inx_group_id)

    def _get_inx_group_id(self, otx_group_id: str):
        return self.groupmap._get_inx_value(otx_group_id)

    def del_group_id(self, otx_group_id: str):
        return self.groupmap.del_otx2inx(otx_group_id)

    def get_mapunit(self, x_jaar_type: str):
        if x_jaar_type == "AcctID":
            return self.acctmap
        elif x_jaar_type == "GroupID":
            return self.groupmap
        elif x_jaar_type == "IdeaUnit":
            return self.ideamap
        elif x_jaar_type == "RoadUnit":
            return self.roadmap

    def set_acctmap(self, x_acctmap: AcctMap):
        self._check_all_core_attrs_match(x_acctmap)
        self.acctmap = x_acctmap

    def get_acctmap(self) -> AcctMap:
        return self.acctmap

    def set_acct_id(self, otx_acct_id: str, inx_acct_id: str):
        self.acctmap.set_otx2inx(otx_acct_id, inx_acct_id)

    def acct_id_exists(self, otx_acct_id: str, inx_acct_id: str):
        return self.acctmap.otx2inx_exists(otx_acct_id, inx_acct_id)

    def _get_inx_acct_id(self, otx_acct_id: str):
        return self.acctmap._get_inx_value(otx_acct_id)

    def del_acct_id(self, otx_acct_id: str):
        return self.acctmap.del_otx2inx(otx_acct_id)

    def set_ideamap(self, x_ideamap: IdeaMap):
        self._check_all_core_attrs_match(x_ideamap)
        self.ideamap = x_ideamap

    def get_ideamap(self) -> IdeaMap:
        return self.ideamap

    def set_idea(self, otx_idea: str, inx_idea: str):
        self.ideamap.set_otx2inx(otx_idea, inx_idea)

    def idea_exists(self, otx_idea: str, inx_idea: str):
        return self.ideamap.otx2inx_exists(otx_idea, inx_idea)

    def _get_inx_idea(self, otx_idea: str):
        return self.ideamap._get_inx_value(otx_idea)

    def del_idea(self, otx_idea: str):
        return self.ideamap.del_otx2inx(otx_idea)

    def set_roadmap(self, x_roadmap: RoadMap):
        self._check_all_core_attrs_match(x_roadmap)
        self.roadmap = x_roadmap

    def get_roadmap(self) -> RoadMap:
        return self.roadmap

    def set_road(self, otx_road: str, inx_road: str):
        self.roadmap.set_otx2inx(otx_road, inx_road)

    def road_exists(self, otx_road: str, inx_road: str):
        return self.roadmap.otx2inx_exists(otx_road, inx_road)

    def _get_inx_road(self, otx_road: str):
        return self.roadmap._get_inx_value(otx_road)

    def del_road(self, otx_road: str):
        return self.roadmap.del_otx2inx(otx_road)

    def _check_all_core_attrs_match(self, x_mapcore: MapCore):
        self._check_attr_match("face_id", x_mapcore)
        self._check_attr_match("otx_wall", x_mapcore)
        self._check_attr_match("inx_wall", x_mapcore)
        self._check_attr_match("unknown_word", x_mapcore)

    def _check_attr_match(self, attr: str, mapcore):
        self_attr = getattr(self, attr)
        unit_attr = getattr(mapcore, attr)
        if self_attr != unit_attr:
            exception_str = f"set_mapcore Error: PidginUnit {attr} is '{self_attr}', MapCore is '{unit_attr}'."
            raise check_attrException(exception_str)

    def is_valid(self) -> bool:
        return (
            self.acctmap.is_valid()
            and self.groupmap.is_valid()
            and self.ideamap.is_valid()
            and self.roadmap.is_valid()
        )

    def set_otx2inx(self, x_jaar_type: str, x_otx: str, x_inx: str):
        if x_jaar_type == "AcctID":
            self.acctmap.set_otx2inx(x_otx, x_inx)
        elif x_jaar_type == "GroupID":
            self.groupmap.set_otx2inx(x_otx, x_inx)
        elif x_jaar_type == "IdeaUnit":
            self.ideamap.set_otx2inx(x_otx, x_inx)
        elif x_jaar_type == "RoadUnit":
            self.roadmap.set_otx2inx(x_otx, x_inx)

    def _get_inx_value(self, x_jaar_type: str, x_otx: str) -> str:
        if x_jaar_type == "AcctID":
            return self.acctmap._get_inx_value(x_otx)
        elif x_jaar_type == "GroupID":
            return self.groupmap._get_inx_value(x_otx)
        elif x_jaar_type == "IdeaUnit":
            return self.ideamap._get_inx_value(x_otx)
        elif x_jaar_type == "RoadUnit":
            return self.roadmap._get_inx_value(x_otx)

    def otx2inx_exists(self, x_jaar_type: str, x_otx: str, x_inx: str) -> bool:
        if x_jaar_type == "AcctID":
            return self.acctmap.otx2inx_exists(x_otx, x_inx)
        elif x_jaar_type == "GroupID":
            return self.groupmap.otx2inx_exists(x_otx, x_inx)
        elif x_jaar_type == "IdeaUnit":
            return self.ideamap.otx2inx_exists(x_otx, x_inx)
        elif x_jaar_type == "RoadUnit":
            return self.roadmap.otx2inx_exists(x_otx, x_inx)

    def del_otx2inx(self, x_jaar_type: str, x_otx: str):
        if x_jaar_type == "AcctID":
            self.acctmap.del_otx2inx(x_otx)
        elif x_jaar_type == "GroupID":
            self.groupmap.del_otx2inx(x_otx)
        elif x_jaar_type == "IdeaUnit":
            self.ideamap.del_otx2inx(x_otx)
        elif x_jaar_type == "RoadUnit":
            self.roadmap.del_otx2inx(x_otx)

    def set_idea(self, x_otx: str, x_inx: str):
        self.roadmap.set_idea(x_otx, x_inx)

    def _get_inx_idea(self, x_otx: str) -> str:
        return self.roadmap._get_inx_idea(x_otx)

    def idea_exists(self, x_otx: str, x_inx: str) -> bool:
        return self.roadmap.idea_exists(x_otx, x_inx)

    def del_idea(self, x_otx: str):
        self.roadmap.del_idea(x_otx)

    def get_dict(self) -> dict:
        return {
            "face_id": self.face_id,
            "event_id": self.event_id,
            "otx_wall": self.otx_wall,
            "inx_wall": self.inx_wall,
            "unknown_word": self.unknown_word,
            "acctmap": self.acctmap.get_dict(),
            "ideamap": self.ideamap.get_dict(),
            "groupmap": self.groupmap.get_dict(),
            "roadmap": self.roadmap.get_dict(),
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def pidginunit_shop(
    face_id: OwnerID,
    event_id: EventID = None,
    otx_wall: str = None,
    inx_wall: str = None,
    unknown_word: str = None,
) -> PidginUnit:
    unknown_word = default_unknown_word_if_None(unknown_word)
    otx_wall = default_wall_if_None(otx_wall)
    inx_wall = default_wall_if_None(inx_wall)

    x_acctmap = acctmap_shop(
        face_id=face_id,
        event_id=event_id,
        otx_wall=otx_wall,
        inx_wall=inx_wall,
        unknown_word=unknown_word,
    )
    x_groupmap = groupmap_shop(
        face_id=face_id,
        event_id=event_id,
        otx_wall=otx_wall,
        inx_wall=inx_wall,
        unknown_word=unknown_word,
    )
    x_ideamap = ideamap_shop(
        face_id=face_id,
        event_id=event_id,
        otx_wall=otx_wall,
        inx_wall=inx_wall,
        unknown_word=unknown_word,
    )
    x_roadmap = roadmap_shop(
        face_id=face_id,
        event_id=event_id,
        otx_wall=otx_wall,
        inx_wall=inx_wall,
        unknown_word=unknown_word,
        x_ideamap=x_ideamap,
    )

    return PidginUnit(
        face_id=face_id,
        event_id=get_0_if_None(event_id),
        unknown_word=unknown_word,
        otx_wall=otx_wall,
        inx_wall=inx_wall,
        acctmap=x_acctmap,
        groupmap=x_groupmap,
        ideamap=x_ideamap,
        roadmap=x_roadmap,
    )


def get_pidginunit_from_dict(x_dict: dict) -> PidginUnit:
    x_acctmap = get_acctmap_from_dict(x_dict.get("acctmap"))
    x_groupmap = get_groupmap_from_dict(x_dict.get("groupmap"))
    x_ideamap = get_ideamap_from_dict(x_dict.get("ideamap"))
    x_roadmap = get_roadmap_from_dict(x_dict.get("roadmap"))
    x_roadmap.ideamap = x_ideamap
    return PidginUnit(
        face_id=x_dict.get("face_id"),
        event_id=x_dict.get("event_id"),
        otx_wall=x_dict.get("otx_wall"),
        inx_wall=x_dict.get("inx_wall"),
        unknown_word=x_dict.get("unknown_word"),
        acctmap=x_acctmap,
        groupmap=x_groupmap,
        ideamap=x_ideamap,
        roadmap=x_roadmap,
    )


def get_pidginunit_from_json(x_json: str) -> PidginUnit:
    return get_pidginunit_from_dict(get_dict_from_json(x_json))


class PidginCoreAttrConflictException(Exception):
    pass


def inherit_pidginunit(older: PidginUnit, newer: PidginUnit) -> PidginUnit:
    if (
        older.face_id != newer.face_id
        or older.otx_wall != newer.otx_wall
        or older.inx_wall != newer.inx_wall
        or older.unknown_word != newer.unknown_word
    ):
        raise PidginCoreAttrConflictException("Core attributes in conflict")
    if older.event_id >= newer.event_id:
        raise PidginCoreAttrConflictException("older pidginunit is not older")
    newer.set_acctmap(inherit_acctmap(newer.acctmap, older.acctmap))
    newer.set_groupmap(inherit_groupmap(newer.groupmap, older.groupmap))
    newer.set_ideamap(inherit_ideamap(newer.ideamap, older.ideamap))
    newer.set_roadmap(inherit_roadmap(newer.roadmap, older.roadmap))

    return newer
