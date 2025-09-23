from dataclasses import dataclass
from src.ch01_data_toolbox.dict_toolbox import (
    get_0_if_None,
    get_dict_from_json,
    get_json_from_dict,
)
from src.ch02_rope_logic.term import BeliefName, EventInt, default_knot_if_None
from src.ch16_lire_logic.lire_config import default_unknown_str_if_None
from src.ch16_lire_logic.map import (
    LabelMap,
    MapCore,
    NameMap,
    RopeMap,
    TitleMap,
    get_labelmap_from_dict,
    get_namemap_from_dict,
    get_ropemap_from_dict,
    get_titlemap_from_dict,
    inherit_labelmap,
    inherit_namemap,
    inherit_ropemap,
    inherit_titlemap,
    labelmap_shop,
    namemap_shop,
    ropemap_shop,
    titlemap_shop,
)


class check_attrException(Exception):
    pass


@dataclass
class LireUnit:
    """Per face object that translates any translatable str.
    otx is the reference for the outside, what the face says
    inx is the reference for the inside, what the same inteprets from the face
    Contains a mapunit for each translatable type: RopeTerm, NameTerm, TitleTerm...
    """

    event_int: EventInt = None
    face_name: BeliefName = None
    titlemap: TitleMap = None
    namemap: NameMap = None
    labelmap: LabelMap = None
    ropemap: RopeMap = None
    unknown_str: str = None  # lireunit
    otx_knot: str = None  # lireunit
    inx_knot: str = None  # lireunit

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
        elif x_class_type == "RopeTerm":
            return self.ropemap

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

    def set_ropemap(self, x_ropemap: RopeMap):
        self._check_all_core_attrs_match(x_ropemap)
        self.ropemap = x_ropemap

    def get_ropemap(self) -> RopeMap:
        return self.ropemap

    def set_rope(self, otx_rope: str, inx_rope: str):
        self.ropemap.set_otx2inx(otx_rope, inx_rope)

    def rope_exists(self, otx_rope: str, inx_rope: str):
        return self.ropemap.otx2inx_exists(otx_rope, inx_rope)

    def _get_inx_rope(self, otx_rope: str):
        return self.ropemap._get_inx_value(otx_rope)

    def del_rope(self, otx_rope: str):
        return self.ropemap.del_otx2inx(otx_rope)

    def _check_all_core_attrs_match(self, x_mapcore: MapCore):
        self._check_attr_match("face_name", x_mapcore)
        self._check_attr_match("otx_knot", x_mapcore)
        self._check_attr_match("inx_knot", x_mapcore)
        self._check_attr_match("unknown_str", x_mapcore)

    def _check_attr_match(self, attr: str, mapcore):
        self_attr = getattr(self, attr)
        unit_attr = getattr(mapcore, attr)
        if self_attr != unit_attr:
            exception_str = f"set_mapcore Error: LireUnit {attr} is '{self_attr}', MapCore is '{unit_attr}'."
            raise check_attrException(exception_str)

    def is_valid(self) -> bool:
        return (
            self.namemap.is_valid()
            and self.titlemap.is_valid()
            and self.labelmap.is_valid()
            and self.ropemap.is_valid()
        )

    def set_otx2inx(self, x_class_type: str, x_otx: str, x_inx: str):
        """class_type: NameTerm, TitleTerm, LabelTerm, RopeTerm"""
        if x_class_type == "NameTerm":
            self.namemap.set_otx2inx(x_otx, x_inx)
        elif x_class_type == "TitleTerm":
            self.titlemap.set_otx2inx(x_otx, x_inx)
        elif x_class_type == "LabelTerm":
            self.labelmap.set_otx2inx(x_otx, x_inx)
        elif x_class_type == "RopeTerm":
            self.ropemap.set_otx2inx(x_otx, x_inx)

    def _get_inx_value(self, x_class_type: str, x_otx: str) -> str:
        """class_type: NameTerm, TitleTerm, LabelTerm, RopeTerm"""
        if x_class_type == "NameTerm":
            return self.namemap._get_inx_value(x_otx)
        elif x_class_type == "TitleTerm":
            return self.titlemap._get_inx_value(x_otx)
        elif x_class_type == "LabelTerm":
            return self.labelmap._get_inx_value(x_otx)
        elif x_class_type == "RopeTerm":
            return self.ropemap._get_inx_value(x_otx)

    def otx2inx_exists(self, x_class_type: str, x_otx: str, x_inx: str) -> bool:
        """class_type: NameTerm, TitleTerm, LabelTerm, RopeTerm"""
        if x_class_type == "NameTerm":
            return self.namemap.otx2inx_exists(x_otx, x_inx)
        elif x_class_type == "TitleTerm":
            return self.titlemap.otx2inx_exists(x_otx, x_inx)
        elif x_class_type == "LabelTerm":
            return self.labelmap.otx2inx_exists(x_otx, x_inx)
        elif x_class_type == "RopeTerm":
            return self.ropemap.otx2inx_exists(x_otx, x_inx)

    def del_otx2inx(self, x_class_type: str, x_otx: str):
        """class_type: NameTerm, TitleTerm, LabelTerm, RopeTerm"""
        if x_class_type == "NameTerm":
            self.namemap.del_otx2inx(x_otx)
        elif x_class_type == "TitleTerm":
            self.titlemap.del_otx2inx(x_otx)
        elif x_class_type == "LabelTerm":
            self.labelmap.del_otx2inx(x_otx)
        elif x_class_type == "RopeTerm":
            self.ropemap.del_otx2inx(x_otx)

    def set_label(self, x_otx: str, x_inx: str):
        self.ropemap.set_label(x_otx, x_inx)

    def _get_inx_label(self, x_otx: str) -> str:
        return self.ropemap._get_inx_label(x_otx)

    def label_exists(self, x_otx: str, x_inx: str) -> bool:
        return self.ropemap.label_exists(x_otx, x_inx)

    def del_label(self, x_otx: str):
        self.ropemap.del_label(x_otx)

    def to_dict(self) -> dict:
        x_namemap = _get_rid_of_lire_core_keys(self.namemap.to_dict())
        x_titlemap = _get_rid_of_lire_core_keys(self.titlemap.to_dict())
        x_labelmap = _get_rid_of_lire_core_keys(self.labelmap.to_dict())
        x_ropemap = _get_rid_of_lire_core_keys(self.ropemap.to_dict())

        return {
            "face_name": self.face_name,
            "event_int": self.event_int,
            "otx_knot": self.otx_knot,
            "inx_knot": self.inx_knot,
            "unknown_str": self.unknown_str,
            "namemap": x_namemap,
            "labelmap": x_labelmap,
            "titlemap": x_titlemap,
            "ropemap": x_ropemap,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.to_dict())


def lireunit_shop(
    face_name: BeliefName,
    event_int: EventInt = None,
    otx_knot: str = None,
    inx_knot: str = None,
    unknown_str: str = None,
) -> LireUnit:
    unknown_str = default_unknown_str_if_None(unknown_str)
    otx_knot = default_knot_if_None(otx_knot)
    inx_knot = default_knot_if_None(inx_knot)

    x_namemap = namemap_shop(
        face_name=face_name,
        event_int=event_int,
        otx_knot=otx_knot,
        inx_knot=inx_knot,
        unknown_str=unknown_str,
    )
    x_titlemap = titlemap_shop(
        face_name=face_name,
        event_int=event_int,
        otx_knot=otx_knot,
        inx_knot=inx_knot,
        unknown_str=unknown_str,
    )
    x_labelmap = labelmap_shop(
        face_name=face_name,
        event_int=event_int,
        otx_knot=otx_knot,
        inx_knot=inx_knot,
        unknown_str=unknown_str,
    )
    x_ropemap = ropemap_shop(
        face_name=face_name,
        event_int=event_int,
        otx_knot=otx_knot,
        inx_knot=inx_knot,
        unknown_str=unknown_str,
        x_labelmap=x_labelmap,
    )

    return LireUnit(
        face_name=face_name,
        event_int=get_0_if_None(event_int),
        unknown_str=unknown_str,
        otx_knot=otx_knot,
        inx_knot=inx_knot,
        namemap=x_namemap,
        titlemap=x_titlemap,
        labelmap=x_labelmap,
        ropemap=x_ropemap,
    )


def get_lireunit_from_dict(x_dict: dict) -> LireUnit:
    x_event_int = x_dict.get("event_int")
    x_face_name = x_dict.get("face_name")
    x_otx_knot = x_dict.get("otx_knot")
    x_inx_knot = x_dict.get("inx_knot")
    x_unknown_str = x_dict.get("unknown_str")
    namemap_dict = x_dict.get("namemap")
    titlemap_dict = x_dict.get("titlemap")
    labelmap_dict = x_dict.get("labelmap")
    ropemap_dict = x_dict.get("ropemap")
    namemap_dict = _add_lire_core_keys(
        namemap_dict,
        x_event_int,
        x_face_name,
        x_otx_knot,
        x_inx_knot,
        x_unknown_str,
    )
    titlemap_dict = _add_lire_core_keys(
        titlemap_dict,
        x_event_int,
        x_face_name,
        x_otx_knot,
        x_inx_knot,
        x_unknown_str,
    )
    labelmap_dict = _add_lire_core_keys(
        labelmap_dict,
        x_event_int,
        x_face_name,
        x_otx_knot,
        x_inx_knot,
        x_unknown_str,
    )
    ropemap_dict = _add_lire_core_keys(
        ropemap_dict,
        x_event_int,
        x_face_name,
        x_otx_knot,
        x_inx_knot,
        x_unknown_str,
    )
    x_namemap = get_namemap_from_dict(namemap_dict)
    x_titlemap = get_titlemap_from_dict(titlemap_dict)
    x_labelmap = get_labelmap_from_dict(labelmap_dict)
    x_ropemap = get_ropemap_from_dict(ropemap_dict)
    x_ropemap.labelmap = x_labelmap
    return LireUnit(
        face_name=x_face_name,
        event_int=x_event_int,
        otx_knot=x_otx_knot,
        inx_knot=x_inx_knot,
        unknown_str=x_unknown_str,
        namemap=x_namemap,
        titlemap=x_titlemap,
        labelmap=x_labelmap,
        ropemap=x_ropemap,
    )


def get_lireunit_from_json(x_json: str) -> LireUnit:
    return get_lireunit_from_dict(get_dict_from_json(x_json))


def _get_rid_of_lire_core_keys(map_dict: dict) -> dict:
    map_dict.pop("event_int")
    map_dict.pop("face_name")
    map_dict.pop("otx_knot")
    map_dict.pop("inx_knot")
    map_dict.pop("unknown_str")
    return map_dict


def _add_lire_core_keys(
    map_dict: dict,
    event_int: int,
    face_name: str,
    otx_knot: str,
    inx_knot: str,
    unknown_str: str,
) -> dict:
    map_dict["event_int"] = event_int
    map_dict["face_name"] = face_name
    map_dict["otx_knot"] = otx_knot
    map_dict["inx_knot"] = inx_knot
    map_dict["unknown_str"] = unknown_str
    return map_dict


class LireCoreAttrConflictException(Exception):
    pass


def inherit_lireunit(older: LireUnit, newer: LireUnit) -> LireUnit:
    if (
        older.face_name != newer.face_name
        or older.otx_knot != newer.otx_knot
        or older.inx_knot != newer.inx_knot
        or older.unknown_str != newer.unknown_str
    ):
        raise LireCoreAttrConflictException("Core attributes in conflict")
    if older.event_int >= newer.event_int:
        raise LireCoreAttrConflictException("older lireunit is not older")
    newer.set_namemap(inherit_namemap(newer.namemap, older.namemap))
    newer.set_titlemap(inherit_titlemap(newer.titlemap, older.titlemap))
    newer.set_labelmap(inherit_labelmap(newer.labelmap, older.labelmap))
    newer.set_ropemap(inherit_ropemap(newer.ropemap, older.ropemap))

    return newer
