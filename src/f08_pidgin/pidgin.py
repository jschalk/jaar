from src.f01_road.jaar_config import default_unknown_word_if_None
from src.f00_instrument.dict_toolbox import (
    get_0_if_None,
    get_json_from_dict,
    get_dict_from_json,
)
from src.f01_road.road import default_bridge_if_None, OwnerName, EventInt
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
    return {"AcctName", "GroupID", "IdeaUnit", "RoadUnit"}


def pidginable_atom_args() -> set:
    return {
        "acct_name",
        "awardee_id",
        "base",
        "face_name",
        "deal_idea",
        "group_id",
        "healer_name",
        "hour_idea",
        "lx",
        "month_idea",
        "parent_road",
        "pick",
        "need",
        "owner_name",
        "road",
        "team_id",
        "timeline_idea",
        "weekday_idea",
    }


@dataclass
class PidginUnit:
    """Per face object that translates any translatable str.
    otx is the reference for the outside, what the face says
    inx is the reference for the inside, what the same inteprets from the face
    Contains a mapunit for each translatable type: RoadUnit, AcctName, GroupID...
    """

    event_int: EventInt = None
    face_name: OwnerName = None
    groupmap: GroupMap = None
    acctmap: AcctMap = None
    ideamap: IdeaMap = None
    roadmap: RoadMap = None
    unknown_word: str = None  # pidginunit heart
    otx_bridge: str = None  # pidginunit heart
    inx_bridge: str = None  # pidginunit heart

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
        if x_jaar_type == "AcctName":
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

    def set_acct_name(self, otx_name: str, inx_name: str):
        self.acctmap.set_otx2inx(otx_name, inx_name)

    def acct_name_exists(self, otx_name: str, inx_name: str):
        return self.acctmap.otx2inx_exists(otx_name, inx_name)

    def _get_inx_name(self, otx_name: str):
        return self.acctmap._get_inx_value(otx_name)

    def del_acct_name(self, otx_name: str):
        return self.acctmap.del_otx2inx(otx_name)

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
        self._check_attr_match("face_name", x_mapcore)
        self._check_attr_match("otx_bridge", x_mapcore)
        self._check_attr_match("inx_bridge", x_mapcore)
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
        if x_jaar_type == "AcctName":
            self.acctmap.set_otx2inx(x_otx, x_inx)
        elif x_jaar_type == "GroupID":
            self.groupmap.set_otx2inx(x_otx, x_inx)
        elif x_jaar_type == "IdeaUnit":
            self.ideamap.set_otx2inx(x_otx, x_inx)
        elif x_jaar_type == "RoadUnit":
            self.roadmap.set_otx2inx(x_otx, x_inx)

    def _get_inx_value(self, x_jaar_type: str, x_otx: str) -> str:
        if x_jaar_type == "AcctName":
            return self.acctmap._get_inx_value(x_otx)
        elif x_jaar_type == "GroupID":
            return self.groupmap._get_inx_value(x_otx)
        elif x_jaar_type == "IdeaUnit":
            return self.ideamap._get_inx_value(x_otx)
        elif x_jaar_type == "RoadUnit":
            return self.roadmap._get_inx_value(x_otx)

    def otx2inx_exists(self, x_jaar_type: str, x_otx: str, x_inx: str) -> bool:
        if x_jaar_type == "AcctName":
            return self.acctmap.otx2inx_exists(x_otx, x_inx)
        elif x_jaar_type == "GroupID":
            return self.groupmap.otx2inx_exists(x_otx, x_inx)
        elif x_jaar_type == "IdeaUnit":
            return self.ideamap.otx2inx_exists(x_otx, x_inx)
        elif x_jaar_type == "RoadUnit":
            return self.roadmap.otx2inx_exists(x_otx, x_inx)

    def del_otx2inx(self, x_jaar_type: str, x_otx: str):
        if x_jaar_type == "AcctName":
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
            "face_name": self.face_name,
            "event_int": self.event_int,
            "otx_bridge": self.otx_bridge,
            "inx_bridge": self.inx_bridge,
            "unknown_word": self.unknown_word,
            "acctmap": self.acctmap.get_dict(),
            "ideamap": self.ideamap.get_dict(),
            "groupmap": self.groupmap.get_dict(),
            "roadmap": self.roadmap.get_dict(),
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def pidginunit_shop(
    face_name: OwnerName,
    event_int: EventInt = None,
    otx_bridge: str = None,
    inx_bridge: str = None,
    unknown_word: str = None,
) -> PidginUnit:
    unknown_word = default_unknown_word_if_None(unknown_word)
    otx_bridge = default_bridge_if_None(otx_bridge)
    inx_bridge = default_bridge_if_None(inx_bridge)

    x_acctmap = acctmap_shop(
        face_name=face_name,
        event_int=event_int,
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_word=unknown_word,
    )
    x_groupmap = groupmap_shop(
        face_name=face_name,
        event_int=event_int,
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_word=unknown_word,
    )
    x_ideamap = ideamap_shop(
        face_name=face_name,
        event_int=event_int,
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_word=unknown_word,
    )
    x_roadmap = roadmap_shop(
        face_name=face_name,
        event_int=event_int,
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_word=unknown_word,
        x_ideamap=x_ideamap,
    )

    return PidginUnit(
        face_name=face_name,
        event_int=get_0_if_None(event_int),
        unknown_word=unknown_word,
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
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
        face_name=x_dict.get("face_name"),
        event_int=x_dict.get("event_int"),
        otx_bridge=x_dict.get("otx_bridge"),
        inx_bridge=x_dict.get("inx_bridge"),
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
        older.face_name != newer.face_name
        or older.otx_bridge != newer.otx_bridge
        or older.inx_bridge != newer.inx_bridge
        or older.unknown_word != newer.unknown_word
    ):
        raise PidginCoreAttrConflictException("Core attributes in conflict")
    if older.event_int >= newer.event_int:
        raise PidginCoreAttrConflictException("older pidginunit is not older")
    newer.set_acctmap(inherit_acctmap(newer.acctmap, older.acctmap))
    newer.set_groupmap(inherit_groupmap(newer.groupmap, older.groupmap))
    newer.set_ideamap(inherit_ideamap(newer.ideamap, older.ideamap))
    newer.set_roadmap(inherit_roadmap(newer.roadmap, older.roadmap))

    return newer
