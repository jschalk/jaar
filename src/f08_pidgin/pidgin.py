from src.f01_road.jaar_config import default_unknown_word
from src.f00_instrument.dict_toolbox import (
    get_0_if_None,
    get_json_from_dict,
    get_dict_from_json,
)
from src.f01_road.finance import TimeLinePoint
from src.f01_road.road import default_wall_if_none, OwnerID
from src.f08_pidgin.birdgeunit_old import (
    BridgeUnit,
    bridgeunit_shop,
    get_bridgeunit_from_dict,
    get_bridgeunit_from_json,
)
from dataclasses import dataclass


class atom_args_jaar_typeException(Exception):
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
