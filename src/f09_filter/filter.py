from src.f00_instrument.file import save_file, get_dir_file_strs
from src.f00_instrument.dict_tool import (
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
    default_road_delimiter_if_none,
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
from src.f04_gift.atom_config import (
    type_AcctID_str,
    type_GroupID_str,
    road_str,
    type_RoadNode_str,
    type_RoadUnit_str,
)
from src.f08_brick.pandas_tool import get_ordered_csv, open_csv
from pandas import DataFrame
from dataclasses import dataclass
from copy import copy as copy_copy


class set_all_otx_to_inxException(Exception):
    pass


class atom_args_jaar_typeException(Exception):
    pass


class set_explicit_label_Exception(Exception):
    pass


def filterable_jaar_types() -> set:
    return {"AcctID", "GroupID", "RoadNode", "RoadUnit"}


def filterable_atom_args() -> set:
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
    otx_to_inx: dict = None
    unknown_word: str = None
    otx_road_delimiter: str = None
    inx_road_delimiter: str = None
    explicit_label: dict = None
    jaar_type: str = None
    face_id: OwnerID = None

    def set_all_otx_to_inx(
        self, x_otx_to_inx: dict, raise_exception_if_invalid: bool = False
    ):
        if raise_exception_if_invalid and str_in_dict(self.unknown_word, x_otx_to_inx):
            error_dict = get_str_in_sub_dict(self.unknown_word, x_otx_to_inx)
            exception_str = f"otx_to_inx cannot have unknown_word '{self.unknown_word}' in any str. Affected keys include {list(error_dict.keys())}."
            raise set_all_otx_to_inxException(exception_str)
        self.otx_to_inx = x_otx_to_inx

    def set_otx_to_inx(self, otx_word: str, inx_word: str):
        self.otx_to_inx[otx_word] = inx_word

    def _get_inx_value(self, otx_word: str) -> str:
        return self.otx_to_inx.get(otx_word)

    def get_create_inx(self, otx_word: str, missing_add: bool = True) -> str:
        if missing_add and self.otx_exists(otx_word) is False:
            inx_word = copy_copy(otx_word)
            if self.jaar_type in {"GroupID"}:
                if self.inx_road_delimiter in otx_word:
                    return None
                otx_r_delimiter = self.otx_road_delimiter
                inx_r_delimiter = self.inx_road_delimiter
                inx_word = inx_word.replace(otx_r_delimiter, inx_r_delimiter)
            if self.jaar_type in {"RoadUnit"}:
                inx_word = self._get_create_roadunit_inx(otx_word)
            if self.jaar_type in {"RoadNode"}:
                if self.inx_road_delimiter in otx_word:
                    return None
                inx_word = self._get_explicit_roadnode(otx_word)
            self.set_otx_to_inx(otx_word, inx_word)

        return self._get_inx_value(otx_word)

    def _get_create_roadunit_inx(self, otx_road) -> RoadUnit:
        otx_parent_road = get_parent_road(otx_road, self.otx_road_delimiter)
        if self.otx_exists(otx_parent_road) is False and otx_parent_road != "":
            return None
        otx_terminus = get_terminus_node(otx_road, self.otx_road_delimiter)
        otx_terminus = self._get_explicit_roadnode(otx_terminus)
        if otx_parent_road == "":
            inx_parent_road = ""
        else:
            inx_parent_road = self._get_inx_value(otx_parent_road)
        return create_road(inx_parent_road, otx_terminus, self.inx_road_delimiter)

    def _get_explicit_roadnode(self, x_roadNode: RoadNode) -> RoadNode:
        if self.explicit_otx_label_exists(x_roadNode):
            return self._get_explicit_inx_label(x_roadNode)
        return x_roadNode

    def otx_to_inx_exists(self, otx_word: str, inx_word: str) -> bool:
        return self._get_inx_value(otx_word) == inx_word

    def otx_exists(self, otx_word: str) -> bool:
        return self._get_inx_value(otx_word) != None

    def del_otx_to_inx(self, otx_word: str):
        self.otx_to_inx.pop(otx_word)

    def set_explicit_label(self, otx_label: RoadNode, inx_label: RoadNode):
        if self.otx_road_delimiter in otx_label:
            exception_str = f"explicit_label cannot have otx_label '{otx_label}'. It must be not have road_delimiter {self.otx_road_delimiter}."
            raise set_explicit_label_Exception(exception_str)
        if self.inx_road_delimiter in inx_label:
            exception_str = f"explicit_label cannot have inx_label '{inx_label}'. It must be not have road_delimiter {self.inx_road_delimiter}."
            raise set_explicit_label_Exception(exception_str)

        self.explicit_label[otx_label] = inx_label

        if self.jaar_type == "RoadUnit":
            self._set_new_explicit_label_to_otx_inx(otx_label, inx_label)

    def _set_new_explicit_label_to_otx_inx(self, otx_label, inx_label):
        for otx_road, inx_road in self.otx_to_inx.items():
            otx_roadnodes = get_all_road_nodes(otx_road, self.otx_road_delimiter)
            inx_roadnodes = get_all_road_nodes(inx_road, self.inx_road_delimiter)
            for x_count, otx_roadnode in enumerate(otx_roadnodes):
                if otx_roadnode == otx_label:
                    inx_roadnodes[x_count] = inx_label
            self.set_otx_to_inx(otx_road, create_road_from_nodes(inx_roadnodes))

    def _get_explicit_inx_label(self, otx_label: RoadNode) -> RoadNode:
        return self.explicit_label.get(otx_label)

    def explicit_label_exists(self, otx_label: RoadNode, inx_label: RoadNode) -> bool:
        return self._get_explicit_inx_label(otx_label) == inx_label

    def explicit_otx_label_exists(self, otx_label: RoadNode) -> bool:
        return self._get_explicit_inx_label(otx_label) != None

    def del_explicit_label(self, otx_label: RoadNode) -> bool:
        self.explicit_label.pop(otx_label)

    def _unknown_word_in_otx_to_inx(self) -> bool:
        return str_in_dict(self.unknown_word, self.otx_to_inx)

    def _otx_road_delimiter_in_otx_words(self) -> bool:
        return str_in_dict_keys(self.otx_road_delimiter, self.otx_to_inx)

    def _inx_road_delimiter_in_otx_words(self) -> bool:
        return str_in_dict_keys(self.inx_road_delimiter, self.otx_to_inx)

    def _otx_road_delimiter_in_inx_words(self) -> bool:
        return str_in_dict_values(self.otx_road_delimiter, self.otx_to_inx)

    def _inx_road_delimiter_in_inx_words(self) -> bool:
        return str_in_dict_values(self.inx_road_delimiter, self.otx_to_inx)

    def _is_otx_delimiter_inclusion_correct(self) -> bool:
        if self.jaar_type in {"AcctID", "RoadNode"}:
            return not self._otx_road_delimiter_in_otx_words()
        elif self.jaar_type in {"GroupID"}:
            return str_in_all_dict_keys(self.otx_road_delimiter, self.otx_to_inx)
        elif self.jaar_type in {"RoadUnit"}:
            return True

    def _is_inx_delimiter_inclusion_correct(self) -> bool:
        if self.jaar_type in {"AcctID", "RoadNode"}:
            return not self._inx_road_delimiter_in_inx_words()
        elif self.jaar_type in {"GroupID"}:
            return str_in_all_dict_values(self.inx_road_delimiter, self.otx_to_inx)
        elif self.jaar_type in {"RoadUnit"}:
            return True

    def all_otx_parent_roads_exist(self) -> bool:
        if self.jaar_type not in {"RoadUnit"}:
            return True
        for x_road in self.otx_to_inx.keys():
            if is_roadnode(x_road, self.otx_road_delimiter) is False:
                parent_road = get_parent_road(x_road, self.otx_road_delimiter)
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
            "otx_road_delimiter": self.otx_road_delimiter,
            "inx_road_delimiter": self.inx_road_delimiter,
            "unknown_word": self.unknown_word,
            "explicit_label": self.explicit_label,
            "otx_to_inx": self.otx_to_inx,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def bridgeunit_shop(
    x_jaar_type: str,
    x_otx_road_delimiter: str = None,
    x_inx_road_delimiter: str = None,
    x_explicit_label: dict = None,
    x_otx_to_inx: dict = None,
    x_unknown_word: str = None,
    x_face_id: OwnerID = None,
) -> BridgeUnit:
    if x_unknown_word is None:
        x_unknown_word = default_unknown_word()
    if x_otx_road_delimiter is None:
        x_otx_road_delimiter = default_road_delimiter_if_none()
    if x_inx_road_delimiter is None:
        x_inx_road_delimiter = default_road_delimiter_if_none()

    return BridgeUnit(
        jaar_type=x_jaar_type,
        otx_to_inx=get_empty_dict_if_none(x_otx_to_inx),
        unknown_word=x_unknown_word,
        otx_road_delimiter=x_otx_road_delimiter,
        inx_road_delimiter=x_inx_road_delimiter,
        explicit_label=get_empty_dict_if_none(x_explicit_label),
        face_id=x_face_id,
    )


def default_unknown_word() -> str:
    return "UNKNOWN"


def get_bridgeunit_from_dict(x_dict: dict) -> BridgeUnit:
    return bridgeunit_shop(
        x_jaar_type=x_dict.get("jaar_type"),
        x_face_id=x_dict.get("face_id"),
        x_inx_road_delimiter=x_dict.get("inx_road_delimiter"),
        x_explicit_label=x_dict.get("explicit_label"),
        x_otx_road_delimiter=x_dict.get("otx_road_delimiter"),
        x_otx_to_inx=x_dict.get("otx_to_inx"),
        x_unknown_word=x_dict.get("unknown_word"),
    )


def get_bridgeunit_from_json(x_json: str) -> BridgeUnit:
    return get_bridgeunit_from_dict(get_dict_from_json(x_json))


@dataclass
class FilterUnit:
    time_id: TimeLinePoint = None
    face_id: OwnerID = None
    bridgeunits: dict[str, BridgeUnit] = None
    unknown_word: str = None
    otx_road_delimiter: str = None
    inx_road_delimiter: str = None

    def set_bridgeunit(self, x_bridgeunit: BridgeUnit):
        self._check_attr_match("face_id", x_bridgeunit)
        self._check_attr_match("otx_road_delimiter", x_bridgeunit)
        self._check_attr_match("inx_road_delimiter", x_bridgeunit)
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

    def set_otx_to_inx(self, x_jaar_type: str, x_otx: str, x_inx: str):
        self.get_bridgeunit(x_jaar_type).set_otx_to_inx(x_otx, x_inx)

    def _get_inx_value(self, x_jaar_type: str, x_otx: str) -> str:
        return self.get_bridgeunit(x_jaar_type)._get_inx_value(x_otx)

    def otx_to_inx_exists(self, x_jaar_type: str, x_otx: str, x_inx: str) -> bool:
        return self.get_bridgeunit(x_jaar_type).otx_to_inx_exists(x_otx, x_inx)

    def del_otx_to_inx(self, x_jaar_type: str, x_otx: str):
        self.get_bridgeunit(x_jaar_type).del_otx_to_inx(x_otx)

    def set_explicit_label(self, x_jaar_type: str, x_otx: str, x_inx: str):
        self.get_bridgeunit(x_jaar_type).set_explicit_label(x_otx, x_inx)

    def _get_explicit_inx_label(self, x_jaar_type: str, x_otx: str) -> str:
        return self.get_bridgeunit(x_jaar_type)._get_explicit_inx_label(x_otx)

    def explicit_label_exists(self, x_jaar_type: str, x_otx: str, x_inx: str) -> bool:
        x_bridgeunit = self.get_bridgeunit(x_jaar_type)
        return x_bridgeunit.explicit_label_exists(x_otx, x_inx)

    def del_explicit_label(self, x_jaar_type: str, x_otx: str):
        self.get_bridgeunit(x_jaar_type).del_explicit_label(x_otx)

    def get_dict(self) -> dict:
        return {
            "face_id": self.face_id,
            "time_id": self.time_id,
            "otx_road_delimiter": self.otx_road_delimiter,
            "inx_road_delimiter": self.inx_road_delimiter,
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


def filterunit_shop(
    x_face_id: OwnerID,
    x_time_id: TimeLinePoint = None,
    x_otx_road_delimiter: str = None,
    x_inx_road_delimiter: str = None,
    x_unknown_word: str = None,
) -> FilterUnit:
    if x_unknown_word is None:
        x_unknown_word = default_unknown_word()
    if x_otx_road_delimiter is None:
        x_otx_road_delimiter = default_road_delimiter_if_none()
    if x_inx_road_delimiter is None:
        x_inx_road_delimiter = default_road_delimiter_if_none()

    x_bridgeunits = {
        "AcctID": bridgeunit_shop(
            x_jaar_type="AcctID",
            x_unknown_word=x_unknown_word,
            x_otx_road_delimiter=x_otx_road_delimiter,
            x_inx_road_delimiter=x_inx_road_delimiter,
            x_face_id=x_face_id,
        ),
        "GroupID": bridgeunit_shop(
            x_jaar_type="GroupID",
            x_unknown_word=x_unknown_word,
            x_otx_road_delimiter=x_otx_road_delimiter,
            x_inx_road_delimiter=x_inx_road_delimiter,
            x_face_id=x_face_id,
        ),
        "road": bridgeunit_shop(
            x_jaar_type="RoadUnit",
            x_unknown_word=x_unknown_word,
            x_otx_road_delimiter=x_otx_road_delimiter,
            x_inx_road_delimiter=x_inx_road_delimiter,
            x_face_id=x_face_id,
        ),
    }

    return FilterUnit(
        face_id=x_face_id,
        time_id=get_0_if_None(x_time_id),
        unknown_word=x_unknown_word,
        otx_road_delimiter=x_otx_road_delimiter,
        inx_road_delimiter=x_inx_road_delimiter,
        bridgeunits=x_bridgeunits,
    )


def get_filterunit_from_dict(x_dict: dict) -> FilterUnit:
    return FilterUnit(
        face_id=x_dict.get("face_id"),
        time_id=x_dict.get("time_id"),
        otx_road_delimiter=x_dict.get("otx_road_delimiter"),
        inx_road_delimiter=x_dict.get("inx_road_delimiter"),
        unknown_word=x_dict.get("unknown_word"),
        bridgeunits=get_bridgeunits_from_dict(x_dict.get("bridgeunits")),
    )


def get_bridgeunits_from_dict(bridgeunits_dict: dict) -> dict[str, BridgeUnit]:
    return {
        x_jaar_type: get_bridgeunit_from_dict(x_bridgeunit_dict)
        for x_jaar_type, x_bridgeunit_dict in bridgeunits_dict.items()
    }


def get_filterunit_from_json(x_json: str) -> FilterUnit:
    return get_filterunit_from_dict(get_dict_from_json(x_json))


def get_otx_to_inx_dt_columns() -> list[str]:
    return [
        "face_id",
        "jaar_type",
        "otx_road_delimiter",
        "inx_road_delimiter",
        "unknown_word",
        "otx_word",
        "inx_word",
    ]


def get_explicit_label_columns() -> list[str]:
    return [
        "face_id",
        "jaar_type",
        "otx_road_delimiter",
        "inx_road_delimiter",
        "unknown_word",
        "otx_label",
        "inx_label",
    ]


def create_otx_to_inx_dt(x_bridgeunit: BridgeUnit) -> DataFrame:
    x_rows_list = [
        {
            "face_id": x_bridgeunit.face_id,
            "jaar_type": x_bridgeunit.jaar_type,
            "otx_road_delimiter": x_bridgeunit.otx_road_delimiter,
            "inx_road_delimiter": x_bridgeunit.inx_road_delimiter,
            "unknown_word": x_bridgeunit.unknown_word,
            "otx_word": otx_value,
            "inx_word": inx_value,
        }
        for otx_value, inx_value in x_bridgeunit.otx_to_inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_otx_to_inx_dt_columns())


def create_explicit_label_dt(x_bridgeunit: BridgeUnit) -> DataFrame:
    x_rows_list = [
        {
            "face_id": x_bridgeunit.face_id,
            "jaar_type": x_bridgeunit.jaar_type,
            "otx_road_delimiter": x_bridgeunit.otx_road_delimiter,
            "inx_road_delimiter": x_bridgeunit.inx_road_delimiter,
            "unknown_word": x_bridgeunit.unknown_word,
            "otx_label": otx_value,
            "inx_label": inx_value,
        }
        for otx_value, inx_value in x_bridgeunit.explicit_label.items()
    ]
    return DataFrame(x_rows_list, columns=get_explicit_label_columns())


def save_all_csvs_from_filterunit(x_dir: str, x_filterunit: FilterUnit):
    for x_key, x_bridgeunit in x_filterunit.bridgeunits.items():
        _save_otx_to_inx_csv(x_dir, x_bridgeunit, x_key)
        _save_explicit_label_csv(x_dir, x_bridgeunit, x_key)


def _save_otx_to_inx_csv(x_dir: str, x_bridgeunit: BridgeUnit, x_filename: str):
    x_otx_to_inx_dt = create_otx_to_inx_dt(x_bridgeunit)
    x_otx_to_inx_csv = get_ordered_csv(x_otx_to_inx_dt)
    x_otx_to_inx_filename = f"{x_filename}_otx_to_inx.csv"
    save_file(x_dir, x_otx_to_inx_filename, x_otx_to_inx_csv)


def _save_explicit_label_csv(x_dir, x_bridgeunit, x_key):
    x_explicit_label_dt = create_explicit_label_dt(x_bridgeunit)
    x_explicit_label_csv = get_ordered_csv(x_explicit_label_dt)
    x_explicit_label_filename = f"{x_key}_explicit_label.csv"
    save_file(x_dir, x_explicit_label_filename, x_explicit_label_csv)


def _load_otx_to_inx_from_csv(x_dir, x_bridgeunit: BridgeUnit) -> BridgeUnit:
    file_key = x_bridgeunit.jaar_type
    if x_bridgeunit.jaar_type in {type_RoadUnit_str(), type_RoadUnit_str()}:
        file_key = road_str()
    otx_to_inx_filename = f"{file_key}_otx_to_inx.csv"
    otx_to_inx_dt = open_csv(x_dir, otx_to_inx_filename)
    for table_row in otx_to_inx_dt.to_dict("records"):
        otx_word_value = table_row.get("otx_word")
        inx_word_value = table_row.get("inx_word")
        if x_bridgeunit.otx_to_inx_exists(otx_word_value, inx_word_value) is False:
            x_bridgeunit.set_otx_to_inx(otx_word_value, inx_word_value)
    return x_bridgeunit


def _load_explicit_label_from_csv(x_dir, x_bridgeunit: BridgeUnit) -> BridgeUnit:
    file_key = x_bridgeunit.jaar_type
    if x_bridgeunit.jaar_type in {type_RoadUnit_str(), type_RoadUnit_str()}:
        file_key = road_str()
    explicit_label_filename = f"{file_key}_explicit_label.csv"
    explicit_label_dt = open_csv(x_dir, explicit_label_filename)
    for table_row in explicit_label_dt.to_dict("records"):
        otx_word_value = table_row.get("otx_label")
        inx_word_value = table_row.get("inx_label")
        if x_bridgeunit.explicit_label_exists(otx_word_value, inx_word_value) is False:
            x_bridgeunit.set_explicit_label(otx_word_value, inx_word_value)
    return x_bridgeunit


def create_dir_valid_filterunit(x_dir: str) -> FilterUnit:
    face_id_set = set()
    unknown_word_set = set()
    otx_road_delimiter_set = set()
    inx_road_delimiter_set = set()
    for x_filename in get_dir_file_strs(x_dir).keys():
        x_dt = open_csv(x_dir, x_filename)
        face_id_set.update(x_dt.face_id.unique())
        unknown_word_set.update(x_dt.unknown_word.unique())
        otx_road_delimiter_set.update(x_dt.otx_road_delimiter.unique())
        inx_road_delimiter_set.update(x_dt.inx_road_delimiter.unique())

    if len(face_id_set) == 1:
        x_face_id = face_id_set.pop()
    if len(unknown_word_set) == 1:
        x_unknown_word = unknown_word_set.pop()
    if len(otx_road_delimiter_set) == 1:
        x_otx_road_delimiter = otx_road_delimiter_set.pop()
    if len(inx_road_delimiter_set) == 1:
        x_inx_road_delimiter = inx_road_delimiter_set.pop()

    # if (
    #     face_id_set != set()
    #     or unknown_word_set != set()
    #     or otx_road_delimiter_set != set()
    #     or inx_road_delimiter_set != set()
    # ):
    #     raise Exception(
    #         f"{face_id_set=} {unknown_word_set=}  {otx_road_delimiter_set=} {inx_road_delimiter_set=}"
    #     )

    return filterunit_shop(
        x_face_id=x_face_id,
        x_otx_road_delimiter=x_otx_road_delimiter,
        x_inx_road_delimiter=x_inx_road_delimiter,
        x_unknown_word=x_unknown_word,
    )


def init_filterunit_from_dir(x_dir: str) -> FilterUnit:
    x_filterunit = create_dir_valid_filterunit(x_dir)
    for x_bridgeunit in x_filterunit.bridgeunits.values():
        _load_otx_to_inx_from_csv(x_dir, x_bridgeunit)
        _load_explicit_label_from_csv(x_dir, x_bridgeunit)
    return x_filterunit
