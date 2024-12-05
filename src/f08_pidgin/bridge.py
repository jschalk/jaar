from src.f01_road.jaar_config import default_unknown_word
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
    get_all_road_ideas,
    create_road_from_ideas,
    get_terminus_idea,
    get_parent_road,
    combine_roads,
    is_ideaunit,
    RoadUnit,
    IdeaUnit,
    OwnerID,
)
from dataclasses import dataclass
from copy import copy as copy_copy


class set_all_otx2inxException(Exception):
    pass


class set_nub_label_Exception(Exception):
    pass


@dataclass
class BridgeCore:
    face_id: OwnerID = None
    otx2inx: dict = None
    unknown_word: str = None
    otx_wall: str = None
    inx_wall: str = None

    def _unknown_word_in_otx2inx(self) -> bool:
        return str_in_dict(self.unknown_word, self.otx2inx)

    def set_all_otx2inx(
        self, x_otx2inx: dict, raise_exception_if_invalid: bool = False
    ):
        if raise_exception_if_invalid and str_in_dict(self.unknown_word, x_otx2inx):
            error_dict = get_str_in_sub_dict(self.unknown_word, x_otx2inx)
            exception_str = f"otx2inx cannot have unknown_word '{self.unknown_word}' in any str. Affected keys include {list(error_dict.keys())}."
            raise set_all_otx2inxException(exception_str)
        self.otx2inx = x_otx2inx

    def get_dict(self) -> dict:
        return {
            "face_id": self.face_id,
            "otx_wall": self.otx_wall,
            "inx_wall": self.inx_wall,
            "unknown_word": self.unknown_word,
            "otx2inx": self.otx2inx,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


class GroupBridge(BridgeCore):
    def set_otx2inx(self, otx_groupid: str, inx_groupid: str):
        self.otx2inx[otx_groupid] = inx_groupid

    def _get_inx_value(self, otx_groupid: str) -> str:
        return self.otx2inx.get(otx_groupid)

    def otx2inx_exists(self, otx_groupid: str, inx_groupid: str) -> bool:
        return self._get_inx_value(otx_groupid) == inx_groupid

    def otx_exists(self, otx_groupid: str) -> bool:
        return self._get_inx_value(otx_groupid) != None

    def del_otx2inx(self, otx_groupid: str):
        self.otx2inx.pop(otx_groupid)

    def reveal_inx(self, otx_groupid: str, missing_add: bool = True) -> str:
        if missing_add and self.otx_exists(otx_groupid) is False:
            inx_groupid = copy_copy(otx_groupid)
            if self.inx_wall in otx_groupid:
                return None
            otx_r_wall = self.otx_wall
            inx_r_wall = self.inx_wall
            inx_groupid = inx_groupid.replace(otx_r_wall, inx_r_wall)
            self.set_otx2inx(otx_groupid, inx_groupid)

        return self._get_inx_value(otx_groupid)

    def _is_inx_wall_inclusion_correct(self):
        return str_in_all_dict_values(self.inx_wall, self.otx2inx)

    def _is_otx_wall_inclusion_correct(self):
        return str_in_all_dict_keys(self.otx_wall, self.otx2inx)

    def is_valid(self):
        return (
            self._is_otx_wall_inclusion_correct()
            and self._is_inx_wall_inclusion_correct()
        )


def groupbridge_shop(
    x_otx_wall: str = None,
    x_inx_wall: str = None,
    x_otx2inx: dict = None,
    x_unknown_word: str = None,
    x_face_id: OwnerID = None,
) -> GroupBridge:
    if x_unknown_word is None:
        x_unknown_word = default_unknown_word()
    if x_otx_wall is None:
        x_otx_wall = default_wall_if_none()
    if x_inx_wall is None:
        x_inx_wall = default_wall_if_none()

    return GroupBridge(
        face_id=x_face_id,
        otx_wall=x_otx_wall,
        inx_wall=x_inx_wall,
        unknown_word=x_unknown_word,
        otx2inx=get_empty_dict_if_none(x_otx2inx),
    )


def get_groupbridge_from_dict(x_dict: dict) -> GroupBridge:
    return groupbridge_shop(
        x_face_id=x_dict.get("face_id"),
        x_otx_wall=x_dict.get("otx_wall"),
        x_inx_wall=x_dict.get("inx_wall"),
        x_otx2inx=x_dict.get("otx2inx"),
        x_unknown_word=x_dict.get("unknown_word"),
    )


def get_groupbridge_from_json(x_json: str) -> GroupBridge:
    return get_groupbridge_from_dict(get_dict_from_json(x_json))


class AcctBridge(BridgeCore):
    def set_otx2inx(self, otx_acctid: str, inx_acctid: str):
        self.otx2inx[otx_acctid] = inx_acctid

    def _get_inx_value(self, otx_acctid: str) -> str:
        return self.otx2inx.get(otx_acctid)

    def otx2inx_exists(self, otx_acctid: str, inx_acctid: str) -> bool:
        return self._get_inx_value(otx_acctid) == inx_acctid

    def otx_exists(self, otx_acctid: str) -> bool:
        return self._get_inx_value(otx_acctid) != None

    def del_otx2inx(self, otx_acctid: str):
        self.otx2inx.pop(otx_acctid)

    def reveal_inx(self, otx_acctid: str, missing_add: bool = True) -> str:
        if missing_add and self.otx_exists(otx_acctid) is False:
            inx_acctid = copy_copy(otx_acctid)
            if self.inx_wall in otx_acctid:
                return None
            otx_r_wall = self.otx_wall
            inx_r_wall = self.inx_wall
            inx_acctid = inx_acctid.replace(otx_r_wall, inx_r_wall)
            self.set_otx2inx(otx_acctid, inx_acctid)

        return self._get_inx_value(otx_acctid)

    def _is_inx_wall_inclusion_correct(self) -> bool:
        return not str_in_dict_values(self.inx_wall, self.otx2inx)

    def _is_otx_wall_inclusion_correct(self) -> bool:
        return not str_in_dict_keys(self.otx_wall, self.otx2inx)

    def is_valid(self) -> bool:
        return (
            self._is_inx_wall_inclusion_correct()
            and self._is_otx_wall_inclusion_correct()
        )


def acctbridge_shop(
    x_otx_wall: str = None,
    x_inx_wall: str = None,
    x_otx2inx: dict = None,
    x_unknown_word: str = None,
    x_face_id: OwnerID = None,
) -> AcctBridge:
    if x_unknown_word is None:
        x_unknown_word = default_unknown_word()
    if x_otx_wall is None:
        x_otx_wall = default_wall_if_none()
    if x_inx_wall is None:
        x_inx_wall = default_wall_if_none()

    return AcctBridge(
        face_id=x_face_id,
        otx_wall=x_otx_wall,
        inx_wall=x_inx_wall,
        unknown_word=x_unknown_word,
        otx2inx=get_empty_dict_if_none(x_otx2inx),
    )


def get_acctbridge_from_dict(x_dict: dict) -> AcctBridge:
    return acctbridge_shop(
        x_face_id=x_dict.get("face_id"),
        x_otx_wall=x_dict.get("otx_wall"),
        x_inx_wall=x_dict.get("inx_wall"),
        x_otx2inx=x_dict.get("otx2inx"),
        x_unknown_word=x_dict.get("unknown_word"),
    )


def get_acctbridge_from_json(x_json: str) -> AcctBridge:
    return get_acctbridge_from_dict(get_dict_from_json(x_json))


@dataclass
class RoadBridge:
    otx2inx: dict = None
    unknown_word: str = None
    otx_wall: str = None
    inx_wall: str = None
    nub_label: dict = None
    face_id: OwnerID = None

    def set_all_otx2inx(
        self, x_otx2inx: dict, raise_exception_if_invalid: bool = False
    ):
        if raise_exception_if_invalid and str_in_dict(self.unknown_word, x_otx2inx):
            error_dict = get_str_in_sub_dict(self.unknown_word, x_otx2inx)
            exception_str = f"otx2inx cannot have unknown_word '{self.unknown_word}' in any str. Affected keys include {list(error_dict.keys())}."
            raise set_all_otx2inxException(exception_str)
        self.otx2inx = x_otx2inx

    def set_otx2inx(self, otx_road: str, inx_road: str):
        self.otx2inx[otx_road] = inx_road

    def _get_inx_value(self, otx_road: str) -> str:
        return self.otx2inx.get(otx_road)

    def reveal_inx(self, otx_road: str, missing_add: bool = True) -> str:
        if missing_add and self.otx_exists(otx_road) is False:
            inx_road = copy_copy(otx_road)
            inx_road = self._reveal_roadunit_inx(otx_road)
            self.set_otx2inx(otx_road, inx_road)

        return self._get_inx_value(otx_road)

    def _reveal_roadunit_inx(self, otx_road) -> RoadUnit:
        otx_parent_road = get_parent_road(otx_road, self.otx_wall)
        if self.otx_exists(otx_parent_road) is False and otx_parent_road != "":
            return None
        otx_terminus = get_terminus_idea(otx_road, self.otx_wall)
        otx_terminus = self._get_nub_ideaunit(otx_terminus)
        if otx_parent_road == "":
            inx_parent_road = ""
        else:
            inx_parent_road = self._get_inx_value(otx_parent_road)
        x_road = combine_roads(inx_parent_road, otx_terminus, self.inx_wall)
        print(f"{x_road=}")
        return x_road

    def _get_nub_ideaunit(self, x_ideaUnit: IdeaUnit) -> IdeaUnit:
        if self.nub_otx_label_exists(x_ideaUnit):
            return self._get_nub_inx_label(x_ideaUnit)
        return x_ideaUnit

    def otx2inx_exists(self, otx_road: str, inx_road: str) -> bool:
        return self._get_inx_value(otx_road) == inx_road

    def otx_exists(self, otx_road: str) -> bool:
        return self._get_inx_value(otx_road) != None

    def del_otx2inx(self, otx_road: str):
        self.otx2inx.pop(otx_road)

    def set_nub_label(self, otx_label: IdeaUnit, inx_label: IdeaUnit):
        if self.otx_wall in otx_label:
            exception_str = f"nub_label cannot have otx_label '{otx_label}'. It must be not have wall {self.otx_wall}."
            raise set_nub_label_Exception(exception_str)
        if self.inx_wall in inx_label:
            exception_str = f"nub_label cannot have inx_label '{inx_label}'. It must be not have wall {self.inx_wall}."
            raise set_nub_label_Exception(exception_str)

        self.nub_label[otx_label] = inx_label
        self._set_new_nub_label_to_otx_inx(otx_label, inx_label)

    def _set_new_nub_label_to_otx_inx(self, otx_label, inx_label):
        for otx_road, inx_road in self.otx2inx.items():
            otx_ideaunits = get_all_road_ideas(otx_road, self.otx_wall)
            inx_ideaunits = get_all_road_ideas(inx_road, self.inx_wall)
            for x_count, otx_ideaunit in enumerate(otx_ideaunits):
                if otx_ideaunit == otx_label:
                    inx_ideaunits[x_count] = inx_label
            self.set_otx2inx(otx_road, create_road_from_ideas(inx_ideaunits))

    def _get_nub_inx_label(self, otx_label: IdeaUnit) -> IdeaUnit:
        return self.nub_label.get(otx_label)

    def nub_label_exists(self, otx_label: IdeaUnit, inx_label: IdeaUnit) -> bool:
        return self._get_nub_inx_label(otx_label) == inx_label

    def nub_otx_label_exists(self, otx_label: IdeaUnit) -> bool:
        return self._get_nub_inx_label(otx_label) != None

    def del_nub_label(self, otx_label: IdeaUnit) -> bool:
        self.nub_label.pop(otx_label)

    def _unknown_word_in_otx2inx(self) -> bool:
        return str_in_dict(self.unknown_word, self.otx2inx)

    def all_otx_parent_roads_exist(self) -> bool:
        for x_road in self.otx2inx.keys():
            if is_ideaunit(x_road, self.otx_wall) is False:
                parent_road = get_parent_road(x_road, self.otx_wall)
                if self.otx_exists(parent_road) is False:
                    return False
        return True

    def is_valid(self) -> bool:
        return self.all_otx_parent_roads_exist()

    def get_dict(self) -> dict:
        return {
            "face_id": self.face_id,
            "otx_wall": self.otx_wall,
            "inx_wall": self.inx_wall,
            "unknown_word": self.unknown_word,
            "nub_label": self.nub_label,
            "otx2inx": self.otx2inx,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def roadbridge_shop(
    x_otx_wall: str = None,
    x_inx_wall: str = None,
    x_nub_label: dict = None,
    x_otx2inx: dict = None,
    x_unknown_word: str = None,
    x_face_id: OwnerID = None,
) -> RoadBridge:
    if x_unknown_word is None:
        x_unknown_word = default_unknown_word()
    if x_otx_wall is None:
        x_otx_wall = default_wall_if_none()
    if x_inx_wall is None:
        x_inx_wall = default_wall_if_none()

    return RoadBridge(
        otx2inx=get_empty_dict_if_none(x_otx2inx),
        unknown_word=x_unknown_word,
        otx_wall=x_otx_wall,
        inx_wall=x_inx_wall,
        nub_label=get_empty_dict_if_none(x_nub_label),
        face_id=x_face_id,
    )


def get_roadbridge_from_dict(x_dict: dict) -> RoadBridge:
    return roadbridge_shop(
        x_face_id=x_dict.get("face_id"),
        x_otx_wall=x_dict.get("otx_wall"),
        x_inx_wall=x_dict.get("inx_wall"),
        x_otx2inx=x_dict.get("otx2inx"),
        x_nub_label=x_dict.get("nub_label"),
        x_unknown_word=x_dict.get("unknown_word"),
    )


def get_roadbridge_from_json(x_json: str) -> RoadBridge:
    return get_roadbridge_from_dict(get_dict_from_json(x_json))


class IdeaBridge(BridgeCore):
    def set_otx2inx(self, otx_ideaid: str, inx_ideaid: str):
        self.otx2inx[otx_ideaid] = inx_ideaid

    def _get_inx_value(self, otx_ideaid: str) -> str:
        return self.otx2inx.get(otx_ideaid)

    def otx2inx_exists(self, otx_ideaid: str, inx_ideaid: str) -> bool:
        return self._get_inx_value(otx_ideaid) == inx_ideaid

    def otx_exists(self, otx_ideaid: str) -> bool:
        return self._get_inx_value(otx_ideaid) != None

    def del_otx2inx(self, otx_ideaid: str):
        self.otx2inx.pop(otx_ideaid)

    def reveal_inx(self, otx_ideaid: str, missing_add: bool = True) -> str:
        if missing_add and self.otx_exists(otx_ideaid) is False:
            inx_ideaid = copy_copy(otx_ideaid)
            if self.inx_wall in otx_ideaid:
                return None
            otx_r_wall = self.otx_wall
            inx_r_wall = self.inx_wall
            inx_ideaid = inx_ideaid.replace(otx_r_wall, inx_r_wall)
            self.set_otx2inx(otx_ideaid, inx_ideaid)

        return self._get_inx_value(otx_ideaid)

    def _is_inx_wall_inclusion_correct(self) -> bool:
        return not str_in_dict_values(self.inx_wall, self.otx2inx)

    def _is_otx_wall_inclusion_correct(self) -> bool:
        return not str_in_dict_keys(self.otx_wall, self.otx2inx)

    def is_valid(self) -> bool:
        return (
            self._is_inx_wall_inclusion_correct()
            and self._is_otx_wall_inclusion_correct()
        )


def ideabridge_shop(
    x_otx_wall: str = None,
    x_inx_wall: str = None,
    x_otx2inx: dict = None,
    x_unknown_word: str = None,
    x_face_id: OwnerID = None,
) -> IdeaBridge:
    if x_unknown_word is None:
        x_unknown_word = default_unknown_word()
    if x_otx_wall is None:
        x_otx_wall = default_wall_if_none()
    if x_inx_wall is None:
        x_inx_wall = default_wall_if_none()

    return IdeaBridge(
        face_id=x_face_id,
        otx_wall=x_otx_wall,
        inx_wall=x_inx_wall,
        unknown_word=x_unknown_word,
        otx2inx=get_empty_dict_if_none(x_otx2inx),
    )


def get_ideabridge_from_dict(x_dict: dict) -> IdeaBridge:
    return ideabridge_shop(
        x_face_id=x_dict.get("face_id"),
        x_otx_wall=x_dict.get("otx_wall"),
        x_inx_wall=x_dict.get("inx_wall"),
        x_otx2inx=x_dict.get("otx2inx"),
        x_unknown_word=x_dict.get("unknown_word"),
    )


def get_ideabridge_from_json(x_json: str) -> IdeaBridge:
    return get_ideabridge_from_dict(get_dict_from_json(x_json))
