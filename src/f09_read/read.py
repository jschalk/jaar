from src.f00_instrument.dict_tool import (
    get_empty_dict_if_none,
    str_in_dict,
    str_in_dict_keys,
    str_in_dict_values,
    get_str_in_sub_dict,
)
from src.f01_road.road import default_road_delimiter_if_none
from dataclasses import dataclass


class set_all_word_mapException(Exception):
    pass


@dataclass
class BridgeUnit:
    word_map: dict[any:any] = None
    unknown_word: str = None
    src_road_delimiter: str = None
    dst_road_delimiter: str = None

    def set_all_word_map(
        self, x_word_map: dict, raise_exception_if_invalid: bool = False
    ):
        if raise_exception_if_invalid and str_in_dict(self.unknown_word, x_word_map):
            error_dict = get_str_in_sub_dict(self.unknown_word, x_word_map)
            exception_str = f"word_map cannot have unknown_word '{self.unknown_word}' in any str. Affected keys include {list(error_dict.keys())}."
            raise set_all_word_mapException(exception_str)
        self.word_map = x_word_map

    def set_word_map(self, src_word: str, dst_word: str):
        self.word_map[src_word] = dst_word

    def get_word_map(self, src_word: str) -> str:
        return self.word_map.get(src_word)

    def word_map_exists(self, src_word: str, dst_word: str) -> bool:
        return self.get_word_map(src_word) == dst_word

    def del_word_map(self, src_word: str):
        self.word_map.pop(src_word)

    def _unknown_word_in_word_map(self) -> bool:
        return str_in_dict(self.unknown_word, self.word_map)

    def _src_road_delimiter_in_src_words(self) -> bool:
        return str_in_dict_keys(self.src_road_delimiter, self.word_map)

    def _dst_road_delimiter_in_src_words(self) -> bool:
        return str_in_dict_keys(self.dst_road_delimiter, self.word_map)

    def _src_road_delimiter_in_dst_words(self) -> bool:
        return str_in_dict_values(self.src_road_delimiter, self.word_map)

    def _dst_road_delimiter_in_dst_words(self) -> bool:
        return str_in_dict_values(self.dst_road_delimiter, self.word_map)


def bridgeunit_shop(
    x_word_map: dict = None,
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

    # if x_word_map.get(x_unknown_word) != None:
    #     exception_str = f"word_map cannot have unknown_word '{x_unknown_word}' as key"
    #     raise Exception(exception_str)
    # for dst_word in x_word_map.values():
    #     if dst_word == x_u

    return BridgeUnit(
        word_map=get_empty_dict_if_none(x_word_map),
        unknown_word=x_unknown_word,
        src_road_delimiter=x_src_road_delimiter,
        dst_road_delimiter=x_dst_road_delimiter,
    )


def default_unknown_word() -> str:
    return "UNKNOWN"


def get_bridgeunit_mapping(x_bridgeunit: BridgeUnit, x_str: str) -> str:
    return x_str
