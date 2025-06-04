from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import (
    get_0_if_None,
    get_dict_from_json,
    get_json_from_dict,
)
from src.a01_term_logic.term import EventInt, OwnerName, default_bridge_if_None
from src.a16_pidgin_logic.map import (
    LabelMap,
    MapCore,
    NameMap,
    TitleMap,
    WayMap,
    get_labelmap_from_dict,
    get_namemap_from_dict,
    get_titlemap_from_dict,
    get_waymap_from_dict,
    inherit_labelmap,
    inherit_namemap,
    inherit_titlemap,
    inherit_waymap,
    labelmap_shop,
    namemap_shop,
    titlemap_shop,
    waymap_shop,
)
from src.a16_pidgin_logic.pidgin_config import default_unknown_str_if_None


class check_attrException(Exception):
    pass


@dataclass
class PidginUnit:
    """Per face object that translates any translatable str.
    otx is the reference for the outside, what the face says
    inx is the reference for the inside, what the same inteprets from the face
    Contains a mapunit for each translatable type: WayTerm, NameTerm, TitleTerm...
    """

    event_int: EventInt = None
    face_name: OwnerName = None
    titlemap: TitleMap = None
    namemap: NameMap = None
    labelmap: LabelMap = None
    waymap: WayMap = None
    unknown_str: str = None  # pidginunit heart
    otx_bridge: str = None  # pidginunit heart
    inx_bridge: str = None  # pidginunit heart

    def set_titlemap(self, x_titlemap: TitleMap):
        self._check_all_core_attrs_match(x_titlemap)
        self.titlemap = x_titlemap

    def get_titlemap(self) -> TitleMap:
        return self.titlemap

    def set_titleterm(self, otx_title: str, inx_title: str):
        self.titlemap.set_otx2inx(otx_title, inx_title)

    def titleterm_exists(self, otx_title: str, inx_title: str):
        return self.titlemap.otx2inx_exists(otx_title, inx_title)

    def _get_inx_title(self, otx_title: str):
        return self.titlemap._get_inx_value(otx_title)

    def del_titleterm(self, otx_title: str):
        return self.titlemap.del_otx2inx(otx_title)

    def get_mapunit(self, x_class_type: str):
        if x_class_type == "NameTerm":
            return self.namemap
        elif x_class_type == "TitleTerm":
            return self.titlemap
        elif x_class_type == "LabelTerm":
            return self.labelmap
        elif x_class_type == "WayTerm":
            return self.waymap

    def set_namemap(self, x_namemap: NameMap):
        self._check_all_core_attrs_match(x_namemap)
        self.namemap = x_namemap

    def get_namemap(self) -> NameMap:
        return self.namemap

    def set_nameterm(self, otx_name: str, inx_name: str):
        self.namemap.set_otx2inx(otx_name, inx_name)

    def nameterm_exists(self, otx_name: str, inx_name: str):
        return self.namemap.otx2inx_exists(otx_name, inx_name)

    def _get_inx_name(self, otx_name: str):
        return self.namemap._get_inx_value(otx_name)

    def del_nameterm(self, otx_name: str):
        return self.namemap.del_otx2inx(otx_name)

    def set_labelmap(self, x_labelmap: LabelMap):
        self._check_all_core_attrs_match(x_labelmap)
        self.labelmap = x_labelmap

    def get_labelmap(self) -> LabelMap:
        return self.labelmap

    def set_label(self, otx_label: str, inx_label: str):
        self.labelmap.set_otx2inx(otx_label, inx_label)

    def label_exists(self, otx_label: str, inx_label: str):
        return self.labelmap.otx2inx_exists(otx_label, inx_label)

    def _get_inx_label(self, otx_label: str):
        return self.labelmap._get_inx_value(otx_label)

    def del_label(self, otx_label: str):
        return self.labelmap.del_otx2inx(otx_label)

    def set_waymap(self, x_waymap: WayMap):
        self._check_all_core_attrs_match(x_waymap)
        self.waymap = x_waymap

    def get_waymap(self) -> WayMap:
        return self.waymap

    def set_way(self, otx_way: str, inx_way: str):
        self.waymap.set_otx2inx(otx_way, inx_way)

    def way_exists(self, otx_way: str, inx_way: str):
        return self.waymap.otx2inx_exists(otx_way, inx_way)

    def _get_inx_way(self, otx_way: str):
        return self.waymap._get_inx_value(otx_way)

    def del_way(self, otx_way: str):
        return self.waymap.del_otx2inx(otx_way)

    def _check_all_core_attrs_match(self, x_mapcore: MapCore):
        self._check_attr_match("face_name", x_mapcore)
        self._check_attr_match("otx_bridge", x_mapcore)
        self._check_attr_match("inx_bridge", x_mapcore)
        self._check_attr_match("unknown_str", x_mapcore)

    def _check_attr_match(self, attr: str, mapcore):
        self_attr = getattr(self, attr)
        unit_attr = getattr(mapcore, attr)
        if self_attr != unit_attr:
            exception_str = f"set_mapcore Error: PidginUnit {attr} is '{self_attr}', MapCore is '{unit_attr}'."
            raise check_attrException(exception_str)

    def is_valid(self) -> bool:
        return (
            self.namemap.is_valid()
            and self.titlemap.is_valid()
            and self.labelmap.is_valid()
            and self.waymap.is_valid()
        )

    def set_otx2inx(self, x_class_type: str, x_otx: str, x_inx: str):
        """class_type: NameTerm, TitleTerm, LabelTerm, WayTerm"""
        if x_class_type == "NameTerm":
            self.namemap.set_otx2inx(x_otx, x_inx)
        elif x_class_type == "TitleTerm":
            self.titlemap.set_otx2inx(x_otx, x_inx)
        elif x_class_type == "LabelTerm":
            self.labelmap.set_otx2inx(x_otx, x_inx)
        elif x_class_type == "WayTerm":
            self.waymap.set_otx2inx(x_otx, x_inx)

    def _get_inx_value(self, x_class_type: str, x_otx: str) -> str:
        """class_type: NameTerm, TitleTerm, LabelTerm, WayTerm"""
        if x_class_type == "NameTerm":
            return self.namemap._get_inx_value(x_otx)
        elif x_class_type == "TitleTerm":
            return self.titlemap._get_inx_value(x_otx)
        elif x_class_type == "LabelTerm":
            return self.labelmap._get_inx_value(x_otx)
        elif x_class_type == "WayTerm":
            return self.waymap._get_inx_value(x_otx)

    def otx2inx_exists(self, x_class_type: str, x_otx: str, x_inx: str) -> bool:
        """class_type: NameTerm, TitleTerm, LabelTerm, WayTerm"""
        if x_class_type == "NameTerm":
            return self.namemap.otx2inx_exists(x_otx, x_inx)
        elif x_class_type == "TitleTerm":
            return self.titlemap.otx2inx_exists(x_otx, x_inx)
        elif x_class_type == "LabelTerm":
            return self.labelmap.otx2inx_exists(x_otx, x_inx)
        elif x_class_type == "WayTerm":
            return self.waymap.otx2inx_exists(x_otx, x_inx)

    def del_otx2inx(self, x_class_type: str, x_otx: str):
        """class_type: NameTerm, TitleTerm, LabelTerm, WayTerm"""
        if x_class_type == "NameTerm":
            self.namemap.del_otx2inx(x_otx)
        elif x_class_type == "TitleTerm":
            self.titlemap.del_otx2inx(x_otx)
        elif x_class_type == "LabelTerm":
            self.labelmap.del_otx2inx(x_otx)
        elif x_class_type == "WayTerm":
            self.waymap.del_otx2inx(x_otx)

    def set_label(self, x_otx: str, x_inx: str):
        self.waymap.set_label(x_otx, x_inx)

    def _get_inx_label(self, x_otx: str) -> str:
        return self.waymap._get_inx_label(x_otx)

    def label_exists(self, x_otx: str, x_inx: str) -> bool:
        return self.waymap.label_exists(x_otx, x_inx)

    def del_label(self, x_otx: str):
        self.waymap.del_label(x_otx)

    def get_dict(self) -> dict:
        x_namemap = _get_rid_of_pidgin_core_keys(self.namemap.get_dict())
        x_titlemap = _get_rid_of_pidgin_core_keys(self.titlemap.get_dict())
        x_labelmap = _get_rid_of_pidgin_core_keys(self.labelmap.get_dict())
        x_waymap = _get_rid_of_pidgin_core_keys(self.waymap.get_dict())

        return {
            "face_name": self.face_name,
            "event_int": self.event_int,
            "otx_bridge": self.otx_bridge,
            "inx_bridge": self.inx_bridge,
            "unknown_str": self.unknown_str,
            "namemap": x_namemap,
            "labelmap": x_labelmap,
            "titlemap": x_titlemap,
            "waymap": x_waymap,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def pidginunit_shop(
    face_name: OwnerName,
    event_int: EventInt = None,
    otx_bridge: str = None,
    inx_bridge: str = None,
    unknown_str: str = None,
) -> PidginUnit:
    unknown_str = default_unknown_str_if_None(unknown_str)
    otx_bridge = default_bridge_if_None(otx_bridge)
    inx_bridge = default_bridge_if_None(inx_bridge)

    x_namemap = namemap_shop(
        face_name=face_name,
        event_int=event_int,
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_str=unknown_str,
    )
    x_titlemap = titlemap_shop(
        face_name=face_name,
        event_int=event_int,
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_str=unknown_str,
    )
    x_labelmap = labelmap_shop(
        face_name=face_name,
        event_int=event_int,
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_str=unknown_str,
    )
    x_waymap = waymap_shop(
        face_name=face_name,
        event_int=event_int,
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_str=unknown_str,
        x_labelmap=x_labelmap,
    )

    return PidginUnit(
        face_name=face_name,
        event_int=get_0_if_None(event_int),
        unknown_str=unknown_str,
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        namemap=x_namemap,
        titlemap=x_titlemap,
        labelmap=x_labelmap,
        waymap=x_waymap,
    )


def get_pidginunit_from_dict(x_dict: dict) -> PidginUnit:
    x_event_int = x_dict.get("event_int")
    x_face_name = x_dict.get("face_name")
    x_otx_bridge = x_dict.get("otx_bridge")
    x_inx_bridge = x_dict.get("inx_bridge")
    x_unknown_str = x_dict.get("unknown_str")
    namemap_dict = x_dict.get("namemap")
    titlemap_dict = x_dict.get("titlemap")
    labelmap_dict = x_dict.get("labelmap")
    waymap_dict = x_dict.get("waymap")
    namemap_dict = _add_pidgin_core_keys(
        namemap_dict,
        x_event_int,
        x_face_name,
        x_otx_bridge,
        x_inx_bridge,
        x_unknown_str,
    )
    titlemap_dict = _add_pidgin_core_keys(
        titlemap_dict,
        x_event_int,
        x_face_name,
        x_otx_bridge,
        x_inx_bridge,
        x_unknown_str,
    )
    labelmap_dict = _add_pidgin_core_keys(
        labelmap_dict,
        x_event_int,
        x_face_name,
        x_otx_bridge,
        x_inx_bridge,
        x_unknown_str,
    )
    waymap_dict = _add_pidgin_core_keys(
        waymap_dict,
        x_event_int,
        x_face_name,
        x_otx_bridge,
        x_inx_bridge,
        x_unknown_str,
    )
    x_namemap = get_namemap_from_dict(namemap_dict)
    x_titlemap = get_titlemap_from_dict(titlemap_dict)
    x_labelmap = get_labelmap_from_dict(labelmap_dict)
    x_waymap = get_waymap_from_dict(waymap_dict)
    x_waymap.labelmap = x_labelmap
    return PidginUnit(
        face_name=x_face_name,
        event_int=x_event_int,
        otx_bridge=x_otx_bridge,
        inx_bridge=x_inx_bridge,
        unknown_str=x_unknown_str,
        namemap=x_namemap,
        titlemap=x_titlemap,
        labelmap=x_labelmap,
        waymap=x_waymap,
    )


def get_pidginunit_from_json(x_json: str) -> PidginUnit:
    return get_pidginunit_from_dict(get_dict_from_json(x_json))


def _get_rid_of_pidgin_core_keys(map_dict: dict) -> dict:
    map_dict.pop("event_int")
    map_dict.pop("face_name")
    map_dict.pop("otx_bridge")
    map_dict.pop("inx_bridge")
    map_dict.pop("unknown_str")
    return map_dict


def _add_pidgin_core_keys(
    map_dict: dict,
    event_int: int,
    face_name: str,
    otx_bridge: str,
    inx_bridge: str,
    unknown_str: str,
) -> dict:
    map_dict["event_int"] = event_int
    map_dict["face_name"] = face_name
    map_dict["otx_bridge"] = otx_bridge
    map_dict["inx_bridge"] = inx_bridge
    map_dict["unknown_str"] = unknown_str
    return map_dict


class PidginCoreAttrConflictException(Exception):
    pass


def inherit_pidginunit(older: PidginUnit, newer: PidginUnit) -> PidginUnit:
    if (
        older.face_name != newer.face_name
        or older.otx_bridge != newer.otx_bridge
        or older.inx_bridge != newer.inx_bridge
        or older.unknown_str != newer.unknown_str
    ):
        raise PidginCoreAttrConflictException("Core attributes in conflict")
    if older.event_int >= newer.event_int:
        raise PidginCoreAttrConflictException("older pidginunit is not older")
    newer.set_namemap(inherit_namemap(newer.namemap, older.namemap))
    newer.set_titlemap(inherit_titlemap(newer.titlemap, older.titlemap))
    newer.set_labelmap(inherit_labelmap(newer.labelmap, older.labelmap))
    newer.set_waymap(inherit_waymap(newer.waymap, older.waymap))

    return newer
