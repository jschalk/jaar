from src.a00_data_toolboxs.dict_toolbox import (
    get_0_if_None,
    get_json_from_dict,
    get_dict_from_json,
)
from src.a01_word_logic.road import default_bridge_if_None, OwnerName, EventInt
from src.a16_pidgin_logic.pidgin_config import default_unknown_word_if_None
from src.a16_pidgin_logic.map import (
    MapCore,
    LabelMap,
    NameMap,
    TitleMap,
    RoadMap,
    labelmap_shop,
    namemap_shop,
    titlemap_shop,
    roadmap_shop,
    get_namemap_from_dict,
    get_labelmap_from_dict,
    get_titlemap_from_dict,
    get_roadmap_from_dict,
    inherit_namemap,
    inherit_labelmap,
    inherit_titlemap,
    inherit_roadmap,
)
from dataclasses import dataclass


class check_attrException(Exception):
    pass


def pidginable_class_types() -> set:
    return {"NameUnit", "LabelUnit", "TitleUnit", "RoadUnit"}


def pidginable_atom_args() -> set:
    return {
        "acct_name",
        "awardee_tag",
        "base",
        "face_name",
        "fisc_title",
        "group_label",
        "healer_name",
        "hour_title",
        "item_title",
        "month_title",
        "parent_road",
        "pick",
        "need",
        "owner_name",
        "road",
        "team_tag",
        "timeline_title",
        "weekday_title",
    }


@dataclass
class PidginUnit:
    """Per face object that translates any translatable str.
    otx is the reference for the outside, what the face says
    inx is the reference for the inside, what the same inteprets from the face
    Contains a mapunit for each translatable type: RoadUnit, NameUnit, LabelUnit...
    """

    event_int: EventInt = None
    face_name: OwnerName = None
    labelmap: LabelMap = None
    namemap: NameMap = None
    titlemap: TitleMap = None
    roadmap: RoadMap = None
    unknown_word: str = None  # pidginunit heart
    otx_bridge: str = None  # pidginunit heart
    inx_bridge: str = None  # pidginunit heart

    def set_labelmap(self, x_labelmap: LabelMap):
        self._check_all_core_attrs_match(x_labelmap)
        self.labelmap = x_labelmap

    def get_labelmap(self) -> LabelMap:
        return self.labelmap

    def set_labelunit(self, otx_label: str, inx_label: str):
        self.labelmap.set_otx2inx(otx_label, inx_label)

    def labelunit_exists(self, otx_label: str, inx_label: str):
        return self.labelmap.otx2inx_exists(otx_label, inx_label)

    def _get_inx_label(self, otx_label: str):
        return self.labelmap._get_inx_value(otx_label)

    def del_labelunit(self, otx_label: str):
        return self.labelmap.del_otx2inx(otx_label)

    def get_mapunit(self, x_class_type: str):
        if x_class_type == "NameUnit":
            return self.namemap
        elif x_class_type == "LabelUnit":
            return self.labelmap
        elif x_class_type == "TitleUnit":
            return self.titlemap
        elif x_class_type == "RoadUnit":
            return self.roadmap

    def set_namemap(self, x_namemap: NameMap):
        self._check_all_core_attrs_match(x_namemap)
        self.namemap = x_namemap

    def get_namemap(self) -> NameMap:
        return self.namemap

    def set_nameunit(self, otx_name: str, inx_name: str):
        self.namemap.set_otx2inx(otx_name, inx_name)

    def nameunit_exists(self, otx_name: str, inx_name: str):
        return self.namemap.otx2inx_exists(otx_name, inx_name)

    def _get_inx_name(self, otx_name: str):
        return self.namemap._get_inx_value(otx_name)

    def del_nameunit(self, otx_name: str):
        return self.namemap.del_otx2inx(otx_name)

    def set_titlemap(self, x_titlemap: TitleMap):
        self._check_all_core_attrs_match(x_titlemap)
        self.titlemap = x_titlemap

    def get_titlemap(self) -> TitleMap:
        return self.titlemap

    def set_title(self, otx_title: str, inx_title: str):
        self.titlemap.set_otx2inx(otx_title, inx_title)

    def title_exists(self, otx_title: str, inx_title: str):
        return self.titlemap.otx2inx_exists(otx_title, inx_title)

    def _get_inx_title(self, otx_title: str):
        return self.titlemap._get_inx_value(otx_title)

    def del_title(self, otx_title: str):
        return self.titlemap.del_otx2inx(otx_title)

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
            self.namemap.is_valid()
            and self.labelmap.is_valid()
            and self.titlemap.is_valid()
            and self.roadmap.is_valid()
        )

    def set_otx2inx(self, x_class_type: str, x_otx: str, x_inx: str):
        """class_type: NameUnit, LabelUnit, TitleUnit, RoadUnit"""
        if x_class_type == "NameUnit":
            self.namemap.set_otx2inx(x_otx, x_inx)
        elif x_class_type == "LabelUnit":
            self.labelmap.set_otx2inx(x_otx, x_inx)
        elif x_class_type == "TitleUnit":
            self.titlemap.set_otx2inx(x_otx, x_inx)
        elif x_class_type == "RoadUnit":
            self.roadmap.set_otx2inx(x_otx, x_inx)

    def _get_inx_value(self, x_class_type: str, x_otx: str) -> str:
        """class_type: NameUnit, LabelUnit, TitleUnit, RoadUnit"""
        if x_class_type == "NameUnit":
            return self.namemap._get_inx_value(x_otx)
        elif x_class_type == "LabelUnit":
            return self.labelmap._get_inx_value(x_otx)
        elif x_class_type == "TitleUnit":
            return self.titlemap._get_inx_value(x_otx)
        elif x_class_type == "RoadUnit":
            return self.roadmap._get_inx_value(x_otx)

    def otx2inx_exists(self, x_class_type: str, x_otx: str, x_inx: str) -> bool:
        """class_type: NameUnit, LabelUnit, TitleUnit, RoadUnit"""
        if x_class_type == "NameUnit":
            return self.namemap.otx2inx_exists(x_otx, x_inx)
        elif x_class_type == "LabelUnit":
            return self.labelmap.otx2inx_exists(x_otx, x_inx)
        elif x_class_type == "TitleUnit":
            return self.titlemap.otx2inx_exists(x_otx, x_inx)
        elif x_class_type == "RoadUnit":
            return self.roadmap.otx2inx_exists(x_otx, x_inx)

    def del_otx2inx(self, x_class_type: str, x_otx: str):
        """class_type: NameUnit, LabelUnit, TitleUnit, RoadUnit"""
        if x_class_type == "NameUnit":
            self.namemap.del_otx2inx(x_otx)
        elif x_class_type == "LabelUnit":
            self.labelmap.del_otx2inx(x_otx)
        elif x_class_type == "TitleUnit":
            self.titlemap.del_otx2inx(x_otx)
        elif x_class_type == "RoadUnit":
            self.roadmap.del_otx2inx(x_otx)

    def set_title(self, x_otx: str, x_inx: str):
        self.roadmap.set_title(x_otx, x_inx)

    def _get_inx_title(self, x_otx: str) -> str:
        return self.roadmap._get_inx_title(x_otx)

    def title_exists(self, x_otx: str, x_inx: str) -> bool:
        return self.roadmap.title_exists(x_otx, x_inx)

    def del_title(self, x_otx: str):
        self.roadmap.del_title(x_otx)

    def get_dict(self) -> dict:
        return {
            "face_name": self.face_name,
            "event_int": self.event_int,
            "otx_bridge": self.otx_bridge,
            "inx_bridge": self.inx_bridge,
            "unknown_word": self.unknown_word,
            "namemap": self.namemap.get_dict(),
            "titlemap": self.titlemap.get_dict(),
            "labelmap": self.labelmap.get_dict(),
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

    x_namemap = namemap_shop(
        face_name=face_name,
        event_int=event_int,
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_word=unknown_word,
    )
    x_labelmap = labelmap_shop(
        face_name=face_name,
        event_int=event_int,
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_word=unknown_word,
    )
    x_titlemap = titlemap_shop(
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
        x_titlemap=x_titlemap,
    )

    return PidginUnit(
        face_name=face_name,
        event_int=get_0_if_None(event_int),
        unknown_word=unknown_word,
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        namemap=x_namemap,
        labelmap=x_labelmap,
        titlemap=x_titlemap,
        roadmap=x_roadmap,
    )


def get_pidginunit_from_dict(x_dict: dict) -> PidginUnit:
    x_namemap = get_namemap_from_dict(x_dict.get("namemap"))
    x_labelmap = get_labelmap_from_dict(x_dict.get("labelmap"))
    x_titlemap = get_titlemap_from_dict(x_dict.get("titlemap"))
    x_roadmap = get_roadmap_from_dict(x_dict.get("roadmap"))
    x_roadmap.titlemap = x_titlemap
    return PidginUnit(
        face_name=x_dict.get("face_name"),
        event_int=x_dict.get("event_int"),
        otx_bridge=x_dict.get("otx_bridge"),
        inx_bridge=x_dict.get("inx_bridge"),
        unknown_word=x_dict.get("unknown_word"),
        namemap=x_namemap,
        labelmap=x_labelmap,
        titlemap=x_titlemap,
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
    newer.set_namemap(inherit_namemap(newer.namemap, older.namemap))
    newer.set_labelmap(inherit_labelmap(newer.labelmap, older.labelmap))
    newer.set_titlemap(inherit_titlemap(newer.titlemap, older.titlemap))
    newer.set_roadmap(inherit_roadmap(newer.roadmap, older.roadmap))

    return newer
