from src.f00_instrument.dict_tool import (
    get_empty_dict_if_none,
    str_in_dict,
    str_in_dict_keys,
    str_in_dict_values,
    get_str_in_sub_dict,
)
from src.f01_road.road import default_road_delimiter_if_none
from dataclasses import dataclass


class set_all_src_to_dstException(Exception):
    pass


@dataclass
class BridgeUnit:
    src_to_dst: dict[any:any] = None
    unknown_word: str = None
    src_road_delimiter: str = None
    dst_road_delimiter: str = None

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


def bridgeunit_shop(
    x_src_to_dst: dict = None,
    x_unknown_word: str = None,
    x_src_road_delimiter: str = None,
    x_dst_road_delimiter: str = None,
) -> BridgeUnit:
    if x_unknown_word is None:
        x_unknown_word = default_unknown_word()
    if x_src_road_delimiter is None:
        x_src_road_delimiter = default_road_delimiter_if_none()
    if x_dst_road_delimiter is None:
        x_dst_road_delimiter = default_road_delimiter_if_none()

    # if x_src_to_dst.get(x_unknown_word) != None:
    #     exception_str = f"src_to_dst cannot have unknown_word '{x_unknown_word}' as key"
    #     raise Exception(exception_str)
    # for dst_word in x_src_to_dst.values():
    #     if dst_word == x_u

    return BridgeUnit(
        src_to_dst=get_empty_dict_if_none(x_src_to_dst),
        unknown_word=x_unknown_word,
        src_road_delimiter=x_src_road_delimiter,
        dst_road_delimiter=x_dst_road_delimiter,
    )


def default_unknown_word() -> str:
    return "UNKNOWN"


def get_bridgeunit_mapping(x_bridgeunit: BridgeUnit, x_str: str) -> str:
    return x_str
