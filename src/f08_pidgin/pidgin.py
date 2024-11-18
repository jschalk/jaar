from src.f00_instrument.dict_toolbox import (
    get_0_if_None,
    get_empty_dict_if_none,
    str_in_dict,
    str_in_dict_keys,
    str_in_dict_values,
    get_str_in_sub_dict,
    str_in_all_dict_keys,
    str_in_all_dict_values,
    get_json_from_dict,
    get_dict_from_json,
)
from src.f01_road.finance import TimeLinePoint
from src.f01_road.road import (
    default_wall_if_none,
    get_all_road_nodes,
    create_road_from_nodes,
    get_terminus_node,
    get_parent_road,
    create_road,
    is_roadnode,
    RoadUnit,
    RoadNode,
    OwnerID,
)
from dataclasses import dataclass
from copy import copy as copy_copy


class set_all_otx2inxException(Exception):
    pass


class atom_args_jaar_typeException(Exception):
    pass


class set_nub_label_Exception(Exception):
    pass


def pidginable_jaar_types() -> set:
    return {"AcctID", "GroupID", "RoadNode", "RoadUnit"}


def pidginable_atom_args() -> set:
    return {
        "acct_id",
        "awardee_id",
        "road",
        "parent_road",
        "label",
        "healer_id",
        "need",
        "base",
        "pick",
        "group_id",
        "team_id",
    }


@dataclass
class BridgeUnit:
    otx2inx: dict = None
    unknown_word: str = None
    otx_wall: str = None
    inx_wall: str = None
    nub_label: dict = None
    jaar_type: str = None
    face_id: OwnerID = None

    def set_all_otx2inx(
        self, x_otx2inx: dict, raise_exception_if_invalid: bool = False
    ):
        if raise_exception_if_invalid and str_in_dict(self.unknown_word, x_otx2inx):
            error_dict = get_str_in_sub_dict(self.unknown_word, x_otx2inx)
            exception_str = f"otx2inx cannot have unknown_word '{self.unknown_word}' in any str. Affected keys include {list(error_dict.keys())}."
            raise set_all_otx2inxException(exception_str)
        self.otx2inx = x_otx2inx

    def set_otx2inx(self, otx_word: str, inx_word: str):
        self.otx2inx[otx_word] = inx_word

    def _get_inx_value(self, otx_word: str) -> str:
        return self.otx2inx.get(otx_word)

    def get_create_inx(self, otx_word: str, missing_add: bool = True) -> str:
        if missing_add and self.otx_exists(otx_word) is False:
            inx_word = copy_copy(otx_word)
            if self.jaar_type in {"GroupID"}:
                if self.inx_wall in otx_word:
                    return None
                otx_r_delimiter = self.otx_wall
                inx_r_delimiter = self.inx_wall
                inx_word = inx_word.replace(otx_r_delimiter, inx_r_delimiter)
            if self.jaar_type in {"RoadUnit"}:
                inx_word = self._get_create_roadunit_inx(otx_word)
            if self.jaar_type in {"RoadNode"}:
                if self.inx_wall in otx_word:
                    return None
                inx_word = self._get_nub_roadnode(otx_word)
            self.set_otx2inx(otx_word, inx_word)

        return self._get_inx_value(otx_word)

    def _get_create_roadunit_inx(self, otx_road) -> RoadUnit:
        otx_parent_road = get_parent_road(otx_road, self.otx_wall)
        if self.otx_exists(otx_parent_road) is False and otx_parent_road != "":
            return None
        otx_terminus = get_terminus_node(otx_road, self.otx_wall)
        otx_terminus = self._get_nub_roadnode(otx_terminus)
        if otx_parent_road == "":
            inx_parent_road = ""
        else:
            inx_parent_road = self._get_inx_value(otx_parent_road)
        return create_road(inx_parent_road, otx_terminus, self.inx_wall)

    def _get_nub_roadnode(self, x_roadNode: RoadNode) -> RoadNode:
        if self.nub_otx_label_exists(x_roadNode):
            return self._get_nub_inx_label(x_roadNode)
        return x_roadNode

    def otx2inx_exists(self, otx_word: str, inx_word: str) -> bool:
        return self._get_inx_value(otx_word) == inx_word

    def otx_exists(self, otx_word: str) -> bool:
        return self._get_inx_value(otx_word) != None

    def del_otx2inx(self, otx_word: str):
        self.otx2inx.pop(otx_word)

    def set_nub_label(self, otx_label: RoadNode, inx_label: RoadNode):
        if self.otx_wall in otx_label:
            exception_str = f"nub_label cannot have otx_label '{otx_label}'. It must be not have wall {self.otx_wall}."
            raise set_nub_label_Exception(exception_str)
        if self.inx_wall in inx_label:
            exception_str = f"nub_label cannot have inx_label '{inx_label}'. It must be not have wall {self.inx_wall}."
            raise set_nub_label_Exception(exception_str)

        self.nub_label[otx_label] = inx_label

        if self.jaar_type == "RoadUnit":
            self._set_new_nub_label_to_otx_inx(otx_label, inx_label)

    def _set_new_nub_label_to_otx_inx(self, otx_label, inx_label):
        for otx_road, inx_road in self.otx2inx.items():
            otx_roadnodes = get_all_road_nodes(otx_road, self.otx_wall)
            inx_roadnodes = get_all_road_nodes(inx_road, self.inx_wall)
            for x_count, otx_roadnode in enumerate(otx_roadnodes):
                if otx_roadnode == otx_label:
                    inx_roadnodes[x_count] = inx_label
            self.set_otx2inx(otx_road, create_road_from_nodes(inx_roadnodes))

    def _get_nub_inx_label(self, otx_label: RoadNode) -> RoadNode:
        return self.nub_label.get(otx_label)

    def nub_label_exists(self, otx_label: RoadNode, inx_label: RoadNode) -> bool:
        return self._get_nub_inx_label(otx_label) == inx_label

    def nub_otx_label_exists(self, otx_label: RoadNode) -> bool:
        return self._get_nub_inx_label(otx_label) != None

    def del_nub_label(self, otx_label: RoadNode) -> bool:
        self.nub_label.pop(otx_label)

    def _unknown_word_in_otx2inx(self) -> bool:
        return str_in_dict(self.unknown_word, self.otx2inx)

    def _otx_wall_in_otx_words(self) -> bool:
        return str_in_dict_keys(self.otx_wall, self.otx2inx)

    def _inx_wall_in_otx_words(self) -> bool:
        return str_in_dict_keys(self.inx_wall, self.otx2inx)

    def _otx_wall_in_inx_words(self) -> bool:
        return str_in_dict_values(self.otx_wall, self.otx2inx)

    def _inx_wall_in_inx_words(self) -> bool:
        return str_in_dict_values(self.inx_wall, self.otx2inx)

    def _is_otx_delimiter_inclusion_correct(self) -> bool:
        if self.jaar_type in {"AcctID", "RoadNode"}:
            return not self._otx_wall_in_otx_words()
        elif self.jaar_type in {"GroupID"}:
            return str_in_all_dict_keys(self.otx_wall, self.otx2inx)
        elif self.jaar_type in {"RoadUnit"}:
            return True

    def _is_inx_delimiter_inclusion_correct(self) -> bool:
        if self.jaar_type in {"AcctID", "RoadNode"}:
            return not self._inx_wall_in_inx_words()
        elif self.jaar_type in {"GroupID"}:
            return str_in_all_dict_values(self.inx_wall, self.otx2inx)
        elif self.jaar_type in {"RoadUnit"}:
            return True

    def all_otx_parent_roads_exist(self) -> bool:
        if self.jaar_type not in {"RoadUnit"}:
            return True
        for x_road in self.otx2inx.keys():
            if is_roadnode(x_road, self.otx_wall) is False:
                parent_road = get_parent_road(x_road, self.otx_wall)
                if self.otx_exists(parent_road) is False:
                    return False
        return True

    def is_valid(self) -> bool:
        return (
            self._is_otx_delimiter_inclusion_correct()
            and self._is_inx_delimiter_inclusion_correct()
            and self.all_otx_parent_roads_exist()
        )

    def get_dict(self) -> dict:
        return {
            "jaar_type": self.jaar_type,
            "face_id": self.face_id,
            "otx_wall": self.otx_wall,
            "inx_wall": self.inx_wall,
            "unknown_word": self.unknown_word,
            "nub_label": self.nub_label,
            "otx2inx": self.otx2inx,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def bridgeunit_shop(
    x_jaar_type: str,
    x_otx_wall: str = None,
    x_inx_wall: str = None,
    x_nub_label: dict = None,
    x_otx2inx: dict = None,
    x_unknown_word: str = None,
    x_face_id: OwnerID = None,
) -> BridgeUnit:
    if x_unknown_word is None:
        x_unknown_word = default_unknown_word()
    if x_otx_wall is None:
        x_otx_wall = default_wall_if_none()
    if x_inx_wall is None:
        x_inx_wall = default_wall_if_none()

    return BridgeUnit(
        jaar_type=x_jaar_type,
        otx2inx=get_empty_dict_if_none(x_otx2inx),
        unknown_word=x_unknown_word,
        otx_wall=x_otx_wall,
        inx_wall=x_inx_wall,
        nub_label=get_empty_dict_if_none(x_nub_label),
        face_id=x_face_id,
    )


def default_unknown_word() -> str:
    return "UNKNOWN"


def get_bridgeunit_from_dict(x_dict: dict) -> BridgeUnit:
    return bridgeunit_shop(
        x_jaar_type=x_dict.get("jaar_type"),
        x_face_id=x_dict.get("face_id"),
        x_inx_wall=x_dict.get("inx_wall"),
        x_nub_label=x_dict.get("nub_label"),
        x_otx_wall=x_dict.get("otx_wall"),
        x_otx2inx=x_dict.get("otx2inx"),
        x_unknown_word=x_dict.get("unknown_word"),
    )


def get_bridgeunit_from_json(x_json: str) -> BridgeUnit:
    return get_bridgeunit_from_dict(get_dict_from_json(x_json))


@dataclass
class PidginUnit:
    """Per face object that translates any translatable str.
    otx is the reference for the outside, what the face says
    inx is the reference for the inside, what the same inteprets from the face
    Contains a bridgeunit for each translatable type: RoadUnit, AcctID, GroupID...
    """

    event_id: TimeLinePoint = None
    face_id: OwnerID = None
    bridgeunits: dict[str, BridgeUnit] = None
    unknown_word: str = None
    otx_wall: str = None
    inx_wall: str = None

    def set_bridgeunit(self, x_bridgeunit: BridgeUnit):
        self._check_attr_match("face_id", x_bridgeunit)
        self._check_attr_match("otx_wall", x_bridgeunit)
        self._check_attr_match("inx_wall", x_bridgeunit)
        self._check_attr_match("unknown_word", x_bridgeunit)

        x_jaar_type = None
        if x_bridgeunit.jaar_type in {"RoadUnit", "RoadNode"}:
            x_jaar_type = "road"
            if x_bridgeunit.jaar_type in {"RoadNode"}:
                x_bridgeunit.jaar_type = "RoadUnit"
        else:
            x_jaar_type = x_bridgeunit.jaar_type

        self.bridgeunits[x_jaar_type] = x_bridgeunit

    def _check_attr_match(self, attr: str, bridgeunit: BridgeUnit):
        self_attr = getattr(self, attr)
        unit_attr = getattr(bridgeunit, attr)
        if self_attr != unit_attr:
            exception_str = f"set_bridgeunit Error: BridgeUnit {attr} is '{self_attr}', BridgeUnit is '{unit_attr}'."
            raise atom_args_jaar_typeException(exception_str)

    def get_bridgeunit(self, x_jaar_type: str) -> BridgeUnit:
        if x_jaar_type in {"RoadUnit", "RoadNode"}:
            x_jaar_type = "road"
        return self.bridgeunits.get(x_jaar_type)

    def is_valid(self) -> bool:
        x_bridgeunits = self.bridgeunits.values()
        return all(x_bridgeunit.is_valid() is True for x_bridgeunit in x_bridgeunits)

    def set_otx2inx(self, x_jaar_type: str, x_otx: str, x_inx: str):
        self.get_bridgeunit(x_jaar_type).set_otx2inx(x_otx, x_inx)

    def _get_inx_value(self, x_jaar_type: str, x_otx: str) -> str:
        return self.get_bridgeunit(x_jaar_type)._get_inx_value(x_otx)

    def otx2inx_exists(self, x_jaar_type: str, x_otx: str, x_inx: str) -> bool:
        return self.get_bridgeunit(x_jaar_type).otx2inx_exists(x_otx, x_inx)

    def del_otx2inx(self, x_jaar_type: str, x_otx: str):
        self.get_bridgeunit(x_jaar_type).del_otx2inx(x_otx)

    def set_nub_label(self, x_jaar_type: str, x_otx: str, x_inx: str):
        self.get_bridgeunit(x_jaar_type).set_nub_label(x_otx, x_inx)

    def _get_nub_inx_label(self, x_jaar_type: str, x_otx: str) -> str:
        return self.get_bridgeunit(x_jaar_type)._get_nub_inx_label(x_otx)

    def nub_label_exists(self, x_jaar_type: str, x_otx: str, x_inx: str) -> bool:
        x_bridgeunit = self.get_bridgeunit(x_jaar_type)
        return x_bridgeunit.nub_label_exists(x_otx, x_inx)

    def del_nub_label(self, x_jaar_type: str, x_otx: str):
        self.get_bridgeunit(x_jaar_type).del_nub_label(x_otx)

    def get_dict(self) -> dict:
        return {
            "face_id": self.face_id,
            "event_id": self.event_id,
            "otx_wall": self.otx_wall,
            "inx_wall": self.inx_wall,
            "unknown_word": self.unknown_word,
            "bridgeunits": self.get_bridgeunits_dict(),
        }

    def get_bridgeunits_dict(self) -> dict:
        return {
            x_key: x_bridgeunit.get_dict()
            for x_key, x_bridgeunit in self.bridgeunits.items()
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def pidginunit_shop(
    x_face_id: OwnerID,
    x_event_id: TimeLinePoint = None,
    x_otx_wall: str = None,
    x_inx_wall: str = None,
    x_unknown_word: str = None,
) -> PidginUnit:
    if x_unknown_word is None:
        x_unknown_word = default_unknown_word()
    if x_otx_wall is None:
        x_otx_wall = default_wall_if_none()
    if x_inx_wall is None:
        x_inx_wall = default_wall_if_none()

    x_bridgeunits = {
        "AcctID": bridgeunit_shop(
            x_jaar_type="AcctID",
            x_unknown_word=x_unknown_word,
            x_otx_wall=x_otx_wall,
            x_inx_wall=x_inx_wall,
            x_face_id=x_face_id,
        ),
        "GroupID": bridgeunit_shop(
            x_jaar_type="GroupID",
            x_unknown_word=x_unknown_word,
            x_otx_wall=x_otx_wall,
            x_inx_wall=x_inx_wall,
            x_face_id=x_face_id,
        ),
        "road": bridgeunit_shop(
            x_jaar_type="RoadUnit",
            x_unknown_word=x_unknown_word,
            x_otx_wall=x_otx_wall,
            x_inx_wall=x_inx_wall,
            x_face_id=x_face_id,
        ),
    }

    return PidginUnit(
        face_id=x_face_id,
        event_id=get_0_if_None(x_event_id),
        unknown_word=x_unknown_word,
        otx_wall=x_otx_wall,
        inx_wall=x_inx_wall,
        bridgeunits=x_bridgeunits,
    )


def get_pidginunit_from_dict(x_dict: dict) -> PidginUnit:
    return PidginUnit(
        face_id=x_dict.get("face_id"),
        event_id=x_dict.get("event_id"),
        otx_wall=x_dict.get("otx_wall"),
        inx_wall=x_dict.get("inx_wall"),
        unknown_word=x_dict.get("unknown_word"),
        bridgeunits=get_bridgeunits_from_dict(x_dict.get("bridgeunits")),
    )


def get_bridgeunits_from_dict(bridgeunits_dict: dict) -> dict[str, BridgeUnit]:
    return {
        x_jaar_type: get_bridgeunit_from_dict(x_bridgeunit_dict)
        for x_jaar_type, x_bridgeunit_dict in bridgeunits_dict.items()
    }


def get_pidginunit_from_json(x_json: str) -> PidginUnit:
    return get_pidginunit_from_dict(get_dict_from_json(x_json))
