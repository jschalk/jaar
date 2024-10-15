from src.f00_instrument.dict_tool import (
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
from src.f01_road.road import (
    default_road_delimiter_if_none,
    get_terminus_node,
    get_parent_road,
    create_road,
    is_roadnode,
)
from src.f04_gift.atom_config import get_atom_args_python_types
from dataclasses import dataclass
from copy import copy as copy_copy


class set_all_src_to_dstException(Exception):
    pass


class atom_args_python_typeException(Exception):
    pass


def rules_by_python_type() -> dict:
    return {
        "AcctID": {"python_type": "AcctID", "rule": "No road_delimiter"},
        "bool": None,
        "float": None,
        "GroupID": {"python_type": "GroupID", "rule": "Must have road_delimiter"},
        "int": None,
        "RoadNode": {"python_type": "RoadNode", "rule": "No road_delimiter"},
        "RoadUnit": None,
        "TimeLinePoint": None,
    }


@dataclass
class BridgeUnit:
    atom_arg: str = None  # always key from from get_atom_args_python_types
    src_to_dst: dict[any:any] = None
    unknown_word: str = None
    src_road_delimiter: str = None
    dst_road_delimiter: str = None
    _calc_atom_python_type: str = None

    def set_atom_arg(self, x_atom_arg: str):
        x_atom_python_type = get_atom_args_python_types().get(x_atom_arg)
        if x_atom_python_type is None:
            exception_str = (
                f"set_atom_arg Error: '{x_atom_arg}' not arg in atom_config."
            )
            raise atom_args_python_typeException(exception_str)

        self.atom_arg = x_atom_arg
        self._calc_atom_python_type = x_atom_python_type

    def set_all_src_to_dst(
        self, x_src_to_dst: dict, raise_exception_if_invalid: bool = False
    ):
        if raise_exception_if_invalid and str_in_dict(self.unknown_word, x_src_to_dst):
            error_dict = get_str_in_sub_dict(self.unknown_word, x_src_to_dst)
            exception_str = f"src_to_dst cannot have unknown_word '{self.unknown_word}' in any str. Affected keys include {list(error_dict.keys())}."
            raise set_all_src_to_dstException(exception_str)
        self.src_to_dst = x_src_to_dst

    def set_src_to_dst(self, src_word: str, dst_word: str):
        self.src_to_dst[src_word] = dst_word

    def _get_dst_value(self, src_word: str) -> str:
        return self.src_to_dst.get(src_word)

    def get_create_dst(self, src_word: str, missing_add: bool = True) -> str:
        if missing_add and self.src_exists(src_word) is False:
            dst_word = copy_copy(src_word)
            if self._calc_atom_python_type in {"GroupID", "RoadUnit"}:
                src_r_delimiter = self.src_road_delimiter
                dst_r_delimiter = self.dst_road_delimiter
                dst_word = dst_word.replace(src_r_delimiter, dst_r_delimiter)
                if self._calc_atom_python_type in {"RoadUnit"}:
                    src_parent_road = get_parent_road(src_word, self.src_road_delimiter)
                    if is_roadnode(src_word, self.src_road_delimiter):
                        dst_word = src_word
                    elif self.src_exists(src_parent_road) is False:
                        return None
                    else:
                        src_terminus = get_terminus_node(
                            src_word, self.src_road_delimiter
                        )
                        dst_parent_road = self._get_dst_value(src_parent_road)
                        dst_word = create_road(
                            dst_parent_road, src_terminus, self.dst_road_delimiter
                        )
                        print(f"{dst_word=}")
            if self.dst_road_delimiter in src_word:
                return None
            self.set_src_to_dst(src_word, dst_word)

        return self._get_dst_value(src_word)

    def src_to_dst_exists(self, src_word: str, dst_word: str) -> bool:
        return self._get_dst_value(src_word) == dst_word

    def src_exists(self, src_word: str) -> bool:
        return self._get_dst_value(src_word) != None

    def del_src_to_dst(self, src_word: str):
        self.src_to_dst.pop(src_word)

    def _unknown_word_in_src_to_dst(self) -> bool:
        return str_in_dict(self.unknown_word, self.src_to_dst)

    def _src_road_delimiter_in_src_words(self) -> bool:
        return str_in_dict_keys(self.src_road_delimiter, self.src_to_dst)

    def _dst_road_delimiter_in_src_words(self) -> bool:
        return str_in_dict_keys(self.dst_road_delimiter, self.src_to_dst)

    def _src_road_delimiter_in_dst_words(self) -> bool:
        return str_in_dict_values(self.src_road_delimiter, self.src_to_dst)

    def _dst_road_delimiter_in_dst_words(self) -> bool:
        return str_in_dict_values(self.dst_road_delimiter, self.src_to_dst)

    def _is_src_delimiter_inclusion_correct(self) -> bool:
        if self._calc_atom_python_type in {"AcctID", "RoadNode"}:
            return not self._src_road_delimiter_in_src_words()
        elif self._calc_atom_python_type in {"GroupID"}:
            return str_in_all_dict_keys(self.src_road_delimiter, self.src_to_dst)
        elif self._calc_atom_python_type in {"RoadUnit"}:
            return True

    def _is_dst_delimiter_inclusion_correct(self) -> bool:
        if self._calc_atom_python_type in {"AcctID", "RoadNode"}:
            return not self._dst_road_delimiter_in_dst_words()
        elif self._calc_atom_python_type in {"GroupID"}:
            return str_in_all_dict_values(self.dst_road_delimiter, self.src_to_dst)
        elif self._calc_atom_python_type in {"RoadUnit"}:
            return True

    def all_src_parent_roads_exist(self) -> bool:
        if self._calc_atom_python_type not in {"RoadUnit"}:
            return True
        for x_road in self.src_to_dst.keys():
            if is_roadnode(x_road, self.src_road_delimiter) is False:
                parent_road = get_parent_road(x_road, self.src_road_delimiter)
                if self.src_exists(parent_road) is False:
                    return False
        return True

    def is_valid(self) -> bool:
        return (
            self._is_src_delimiter_inclusion_correct()
            and self._is_dst_delimiter_inclusion_correct()
        )

    def get_dict(self) -> dict:
        return {
            "atom_arg": self.atom_arg,
            "src_road_delimiter": self.src_road_delimiter,
            "dst_road_delimiter": self.dst_road_delimiter,
            "unknown_word": self.unknown_word,
            "src_to_dst": self.src_to_dst,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def bridgeunit_shop(
    x_atom_arg: str,
    x_src_road_delimiter: str = None,
    x_dst_road_delimiter: str = None,
    x_src_to_dst: dict = None,
    x_unknown_word: str = None,
) -> BridgeUnit:
    if x_unknown_word is None:
        x_unknown_word = default_unknown_word()
    if x_src_road_delimiter is None:
        x_src_road_delimiter = default_road_delimiter_if_none()
    if x_dst_road_delimiter is None:
        x_dst_road_delimiter = default_road_delimiter_if_none()

    return BridgeUnit(
        atom_arg=x_atom_arg,
        src_to_dst=get_empty_dict_if_none(x_src_to_dst),
        unknown_word=x_unknown_word,
        src_road_delimiter=x_src_road_delimiter,
        dst_road_delimiter=x_dst_road_delimiter,
        _calc_atom_python_type=get_atom_args_python_types().get(x_atom_arg),
    )


def default_unknown_word() -> str:
    return "UNKNOWN"


def get_bridgeunit_from_dict(x_dict: dict) -> BridgeUnit:
    return bridgeunit_shop(
        x_atom_arg=x_dict.get("atom_arg"),
        x_dst_road_delimiter=x_dict.get("dst_road_delimiter"),
        x_src_road_delimiter=x_dict.get("src_road_delimiter"),
        x_src_to_dst=x_dict.get("src_to_dst"),
        x_unknown_word=x_dict.get("unknown_word"),
    )


def get_bridgeunit_from_json(x_json: str) -> BridgeUnit:
    return get_bridgeunit_from_dict(get_dict_from_json(x_json))