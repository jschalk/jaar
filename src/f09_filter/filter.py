from src.f00_instrument.dict_tool import (
    get_empty_dict_if_none,
    str_in_dict,
    str_in_dict_keys,
    str_in_dict_values,
    get_str_in_sub_dict,
    str_in_all_dict_keys,
    str_in_all_dict_values,
)
from src.f01_road.road import default_road_delimiter_if_none
from src.f04_gift.atom_config import get_atom_args_python_types
from dataclasses import dataclass


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

    def get_src_to_dst(self, src_word: str) -> str:
        return self.src_to_dst.get(src_word)

    def src_to_dst_exists(self, src_word: str, dst_word: str) -> bool:
        return self.get_src_to_dst(src_word) == dst_word

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

    def _is_dst_delimiter_inclusion_correct(self) -> bool:
        if self._calc_atom_python_type in {"AcctID", "RoadNode"}:
            return not self._dst_road_delimiter_in_dst_words()
        elif self._calc_atom_python_type in {"GroupID"}:
            return str_in_all_dict_values(self.dst_road_delimiter, self.src_to_dst)

    def is_valid(self) -> bool:
        return (
            self._is_src_delimiter_inclusion_correct()
            and self._is_dst_delimiter_inclusion_correct()
        )


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


def get_bridgeunit_mapping(x_bridgeunit: BridgeUnit, x_str: str) -> str:
    return x_str
