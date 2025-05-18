from src.a00_data_toolbox.dict_toolbox import (
    get_empty_dict_if_None,
    str_in_dict,
    str_in_dict_keys,
    str_in_dict_values,
    get_str_in_sub_dict,
    str_in_all_dict_keys,
    str_in_all_dict_values,
    get_json_from_dict,
    get_dict_from_json,
    get_0_if_None,
)
from src.a01_way_logic.way import (
    default_bridge_if_None,
    create_way,
    get_all_way_words,
    create_way_from_words,
    get_terminus_word,
    get_parent_way,
    is_wordstr,
    WayStr,
    WordStr,
    FaceName,
    EventInt,
)
from src.a16_pidgin_logic.pidgin_config import default_unknown_term_if_None
from dataclasses import dataclass
from copy import copy as copy_copy


class set_all_otx2inxException(Exception):
    pass


class set_word_Exception(Exception):
    pass


@dataclass
class MapCore:
    face_name: FaceName = None
    event_int: EventInt = None
    otx2inx: dict = None
    unknown_term: str = None
    otx_bridge: str = None
    inx_bridge: str = None

    def _unknown_term_in_otx2inx(self) -> bool:
        return str_in_dict(self.unknown_term, self.otx2inx)

    def set_all_otx2inx(
        self, x_otx2inx: dict, raise_exception_if_invalid: bool = False
    ):
        if raise_exception_if_invalid and str_in_dict(self.unknown_term, x_otx2inx):
            error_dict = get_str_in_sub_dict(self.unknown_term, x_otx2inx)
            exception_str = f"otx2inx cannot have unknown_term '{self.unknown_term}' in any str. Affected keys include {list(error_dict.keys())}."
            raise set_all_otx2inxException(exception_str)
        self.otx2inx = x_otx2inx

    def get_dict(self) -> dict:
        return {
            "face_name": self.face_name,
            "event_int": self.event_int,
            "otx_bridge": self.otx_bridge,
            "inx_bridge": self.inx_bridge,
            "unknown_term": self.unknown_term,
            "otx2inx": self.otx2inx,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


class NameMap(MapCore):
    def set_otx2inx(self, otx_name: str, inx_name: str):
        self.otx2inx[otx_name] = inx_name

    def _get_inx_value(self, otx_name: str) -> str:
        return self.otx2inx.get(otx_name)

    def otx2inx_exists(self, otx_name: str, inx_name: str) -> bool:
        return self._get_inx_value(otx_name) == inx_name

    def otx_exists(self, otx_name: str) -> bool:
        return self._get_inx_value(otx_name) != None

    def del_otx2inx(self, otx_name: str):
        self.otx2inx.pop(otx_name)

    def reveal_inx(self, otx_name: str, missing_add: bool = True) -> str:
        if missing_add and self.otx_exists(otx_name) is False:
            inx_name = copy_copy(otx_name)
            if self.inx_bridge in otx_name:
                return None
            otx_r_bridge = self.otx_bridge
            inx_r_bridge = self.inx_bridge
            inx_name = inx_name.replace(otx_r_bridge, inx_r_bridge)
            self.set_otx2inx(otx_name, inx_name)

        return self._get_inx_value(otx_name)

    def _is_inx_bridge_inclusion_correct(self) -> bool:
        return not str_in_dict_values(self.inx_bridge, self.otx2inx)

    def _is_otx_bridge_inclusion_correct(self) -> bool:
        return not str_in_dict_keys(self.otx_bridge, self.otx2inx)

    def is_valid(self) -> bool:
        return (
            self._is_inx_bridge_inclusion_correct()
            and self._is_otx_bridge_inclusion_correct()
        )


def namemap_shop(
    face_name: FaceName = None,
    event_int: EventInt = None,
    otx_bridge: str = None,
    inx_bridge: str = None,
    otx2inx: dict = None,
    unknown_term: str = None,
) -> NameMap:
    unknown_term = default_unknown_term_if_None(unknown_term)
    otx_bridge = default_bridge_if_None(otx_bridge)
    inx_bridge = default_bridge_if_None(inx_bridge)

    return NameMap(
        face_name=face_name,
        event_int=get_0_if_None(event_int),
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_term=unknown_term,
        otx2inx=get_empty_dict_if_None(otx2inx),
    )


def get_namemap_from_dict(x_dict: dict) -> NameMap:
    return namemap_shop(
        face_name=x_dict.get("face_name"),
        event_int=x_dict.get("event_int"),
        otx_bridge=x_dict.get("otx_bridge"),
        inx_bridge=x_dict.get("inx_bridge"),
        otx2inx=x_dict.get("otx2inx"),
        unknown_term=x_dict.get("unknown_term"),
    )


def get_namemap_from_json(x_json: str) -> NameMap:
    return get_namemap_from_dict(get_dict_from_json(x_json))


class TitleMap(MapCore):
    def set_otx2inx(self, otx_title: str, inx_title: str):
        self.otx2inx[otx_title] = inx_title

    def _get_inx_value(self, otx_title: str) -> str:
        return self.otx2inx.get(otx_title)

    def otx2inx_exists(self, otx_title: str, inx_title: str) -> bool:
        return self._get_inx_value(otx_title) == inx_title

    def otx_exists(self, otx_title: str) -> bool:
        return self._get_inx_value(otx_title) != None

    def del_otx2inx(self, otx_title: str):
        self.otx2inx.pop(otx_title)

    def reveal_inx(self, otx_title: str, missing_add: bool = True) -> str:
        if missing_add and self.otx_exists(otx_title) is False:
            inx_title = copy_copy(otx_title)
            if self.inx_bridge in otx_title:
                return None
            otx_r_bridge = self.otx_bridge
            inx_r_bridge = self.inx_bridge
            inx_title = inx_title.replace(otx_r_bridge, inx_r_bridge)
            self.set_otx2inx(otx_title, inx_title)

        return self._get_inx_value(otx_title)

    def _is_inx_bridge_inclusion_correct(self):
        return str_in_all_dict_values(self.inx_bridge, self.otx2inx)

    def _is_otx_bridge_inclusion_correct(self):
        return str_in_all_dict_keys(self.otx_bridge, self.otx2inx)

    def is_valid(self):
        return (
            self._is_otx_bridge_inclusion_correct()
            and self._is_inx_bridge_inclusion_correct()
        )


def titlemap_shop(
    face_name: FaceName = None,
    event_int: EventInt = None,
    otx_bridge: str = None,
    inx_bridge: str = None,
    otx2inx: dict = None,
    unknown_term: str = None,
) -> TitleMap:
    unknown_term = default_unknown_term_if_None(unknown_term)
    otx_bridge = default_bridge_if_None(otx_bridge)
    inx_bridge = default_bridge_if_None(inx_bridge)

    return TitleMap(
        face_name=face_name,
        event_int=get_0_if_None(event_int),
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_term=unknown_term,
        otx2inx=get_empty_dict_if_None(otx2inx),
    )


def get_titlemap_from_dict(x_dict: dict) -> TitleMap:
    return titlemap_shop(
        face_name=x_dict.get("face_name"),
        event_int=x_dict.get("event_int"),
        otx_bridge=x_dict.get("otx_bridge"),
        inx_bridge=x_dict.get("inx_bridge"),
        otx2inx=x_dict.get("otx2inx"),
        unknown_term=x_dict.get("unknown_term"),
    )


def get_titlemap_from_json(x_json: str) -> TitleMap:
    return get_titlemap_from_dict(get_dict_from_json(x_json))


class WordMap(MapCore):
    def set_otx2inx(self, otx_word: str, inx_word: str):
        self.otx2inx[otx_word] = inx_word

    def _get_inx_value(self, otx_word: str) -> str:
        return self.otx2inx.get(otx_word)

    def otx2inx_exists(self, otx_word: str, inx_word: str) -> bool:
        return self._get_inx_value(otx_word) == inx_word

    def otx_exists(self, otx_word: str) -> bool:
        return self._get_inx_value(otx_word) != None

    def del_otx2inx(self, otx_word: str):
        self.otx2inx.pop(otx_word)

    def reveal_inx(self, otx_word: str, missing_add: bool = True) -> str:
        if missing_add and self.otx_exists(otx_word) is False:
            inx_word = copy_copy(otx_word)
            if self.inx_bridge in otx_word:
                return None
            otx_r_bridge = self.otx_bridge
            inx_r_bridge = self.inx_bridge
            inx_word = inx_word.replace(otx_r_bridge, inx_r_bridge)
            self.set_otx2inx(otx_word, inx_word)

        return self._get_inx_value(otx_word)

    def _is_inx_bridge_inclusion_correct(self) -> bool:
        return not str_in_dict_values(self.inx_bridge, self.otx2inx)

    def _is_otx_bridge_inclusion_correct(self) -> bool:
        return not str_in_dict_keys(self.otx_bridge, self.otx2inx)

    def is_valid(self) -> bool:
        return (
            self._is_inx_bridge_inclusion_correct()
            and self._is_otx_bridge_inclusion_correct()
        )


def wordmap_shop(
    face_name: FaceName = None,
    event_int: EventInt = None,
    otx_bridge: str = None,
    inx_bridge: str = None,
    otx2inx: dict = None,
    unknown_term: str = None,
) -> WordMap:
    unknown_term = default_unknown_term_if_None(unknown_term)
    otx_bridge = default_bridge_if_None(otx_bridge)
    inx_bridge = default_bridge_if_None(inx_bridge)

    return WordMap(
        face_name=face_name,
        event_int=get_0_if_None(event_int),
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_term=unknown_term,
        otx2inx=get_empty_dict_if_None(otx2inx),
    )


def get_wordmap_from_dict(x_dict: dict) -> WordMap:
    return wordmap_shop(
        face_name=x_dict.get("face_name"),
        event_int=x_dict.get("event_int"),
        otx_bridge=x_dict.get("otx_bridge"),
        inx_bridge=x_dict.get("inx_bridge"),
        otx2inx=x_dict.get("otx2inx"),
        unknown_term=x_dict.get("unknown_term"),
    )


def get_wordmap_from_json(x_json: str) -> WordMap:
    return get_wordmap_from_dict(get_dict_from_json(x_json))


@dataclass
class WayMap:
    face_name: FaceName = None
    event_int: EventInt = None
    otx2inx: dict = None
    unknown_term: str = None
    otx_bridge: str = None
    inx_bridge: str = None
    wordmap: WordMap = None

    def set_all_otx2inx(
        self, x_otx2inx: dict, raise_exception_if_invalid: bool = False
    ):
        if raise_exception_if_invalid and str_in_dict(self.unknown_term, x_otx2inx):
            error_dict = get_str_in_sub_dict(self.unknown_term, x_otx2inx)
            exception_str = f"otx2inx cannot have unknown_term '{self.unknown_term}' in any str. Affected keys include {list(error_dict.keys())}."
            raise set_all_otx2inxException(exception_str)
        self.otx2inx = x_otx2inx

    def set_otx2inx(self, otx_way: str, inx_way: str):
        self.otx2inx[otx_way] = inx_way

    def _get_inx_value(self, otx_way: str) -> str:
        return self.otx2inx.get(otx_way)

    def reveal_inx(self, otx_way: str, missing_add: bool = True) -> str:
        if missing_add and self.otx_exists(otx_way) is False:
            inx_way = copy_copy(otx_way)
            inx_way = self._reveal_waystr_inx(otx_way)
            self.set_otx2inx(otx_way, inx_way)

        return self._get_inx_value(otx_way)

    def _reveal_waystr_inx(self, otx_way) -> WayStr:
        otx_parent_way = get_parent_way(otx_way, self.otx_bridge)
        if self.otx_exists(otx_parent_way) is False and otx_parent_way != "":
            return None
        otx_terminus = get_terminus_word(otx_way, self.otx_bridge)
        otx_terminus = self._get_wordmap_wordstr(otx_terminus)
        if otx_parent_way == "":
            inx_parent_way = ""
        else:
            inx_parent_way = self._get_inx_value(otx_parent_way)
        return create_way(inx_parent_way, otx_terminus, self.inx_bridge)

    def _get_wordmap_wordstr(self, x_wordStr: WordStr) -> WordStr:
        if self.otx_word_exists(x_wordStr):
            return self.wordmap.reveal_inx(x_wordStr)
        return x_wordStr

    def otx2inx_exists(self, otx_way: str, inx_way: str) -> bool:
        return self._get_inx_value(otx_way) == inx_way

    def otx_exists(self, otx_way: str) -> bool:
        return self._get_inx_value(otx_way) != None

    def del_otx2inx(self, otx_way: str):
        self.otx2inx.pop(otx_way)

    def set_word(self, otx_word: WordStr, inx_word: WordStr):
        if self.otx_bridge in otx_word:
            exception_str = f"word cannot have otx_word '{otx_word}'. It must be not have bridge {self.otx_bridge}."
            raise set_word_Exception(exception_str)
        if self.inx_bridge in inx_word:
            exception_str = f"word cannot have inx_word '{inx_word}'. It must be not have bridge {self.inx_bridge}."
            raise set_word_Exception(exception_str)

        self.wordmap.set_otx2inx(otx_word, inx_word)
        self._set_new_word_to_otx_inx(otx_word, inx_word)

    def _set_new_word_to_otx_inx(self, otx_word, inx_word):
        for otx_way, inx_way in self.otx2inx.items():
            otx_wordstrs = get_all_way_words(otx_way, self.otx_bridge)
            inx_wordstrs = get_all_way_words(inx_way, self.inx_bridge)
            for x_count, otx_wordstr in enumerate(otx_wordstrs):
                if otx_wordstr == otx_word:
                    inx_wordstrs[x_count] = inx_word
            self.set_otx2inx(otx_way, create_way_from_words(inx_wordstrs))

    def _get_inx_word(self, otx_word: WordStr) -> WordStr:
        return self.wordmap.otx2inx.get(otx_word)

    def word_exists(self, otx_word: WordStr, inx_word: WordStr) -> bool:
        return self.wordmap.otx2inx_exists(otx_word, inx_word)

    def otx_word_exists(self, otx_word: WordStr) -> bool:
        return self.wordmap.otx_exists(otx_word)

    def del_word(self, otx_word: WordStr) -> bool:
        self.wordmap.del_otx2inx(otx_word)

    def _unknown_term_in_otx2inx(self) -> bool:
        return str_in_dict(self.unknown_term, self.otx2inx)

    def all_otx_parent_ways_exist(self) -> bool:
        for x_way in self.otx2inx.keys():
            print(f"{x_way=}")
            parent_way = get_parent_way(x_way, self.otx_bridge)
            if parent_way and self.otx_exists(parent_way) is False:
                print("false")
                return False
        return True

    def is_valid(self) -> bool:
        return self.all_otx_parent_ways_exist()

    def get_dict(self) -> dict:
        return {
            "face_name": self.face_name,
            "event_int": self.event_int,
            "otx_bridge": self.otx_bridge,
            "inx_bridge": self.inx_bridge,
            "unknown_term": self.unknown_term,
            "otx2inx": self.otx2inx,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def waymap_shop(
    face_name: FaceName = None,
    event_int: EventInt = None,
    otx_bridge: str = None,
    inx_bridge: str = None,
    x_wordmap: WordMap = None,
    otx2inx: dict = None,
    unknown_term: str = None,
) -> WayMap:
    unknown_term = default_unknown_term_if_None(unknown_term)
    otx_bridge = default_bridge_if_None(otx_bridge)
    inx_bridge = default_bridge_if_None(inx_bridge)

    if x_wordmap is None:
        x_wordmap = wordmap_shop(
            otx_bridge=otx_bridge,
            inx_bridge=inx_bridge,
            unknown_term=unknown_term,
            face_name=face_name,
            event_int=event_int,
        )

    return WayMap(
        otx2inx=get_empty_dict_if_None(otx2inx),
        unknown_term=unknown_term,
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        wordmap=x_wordmap,
        face_name=face_name,
        event_int=get_0_if_None(event_int),
    )


def get_waymap_from_dict(x_dict: dict) -> WayMap:
    return waymap_shop(
        face_name=x_dict.get("face_name"),
        event_int=x_dict.get("event_int"),
        otx_bridge=x_dict.get("otx_bridge"),
        inx_bridge=x_dict.get("inx_bridge"),
        otx2inx=x_dict.get("otx2inx"),
        unknown_term=x_dict.get("unknown_term"),
    )


def get_waymap_from_json(x_json: str) -> WayMap:
    return get_waymap_from_dict(get_dict_from_json(x_json))


class MapCoreAttrConflictException(Exception):
    pass


def _check_core_attributes(new_obj, old_obj):
    if (
        old_obj.face_name != new_obj.face_name
        or old_obj.otx_bridge != new_obj.otx_bridge
        or old_obj.inx_bridge != new_obj.inx_bridge
        or old_obj.unknown_term != new_obj.unknown_term
    ):
        raise MapCoreAttrConflictException("Core attributes in conflict")
    if old_obj.event_int >= new_obj.event_int:
        raise MapCoreAttrConflictException("older mapunit is not older")


def _inherit_mapunit(new, old):
    _check_core_attributes(new, old)
    for otx_key, old_inx in old.otx2inx.items():
        if new.otx_exists(otx_key) is False:
            new.set_otx2inx(otx_key, old_inx)
    return new


def inherit_namemap(new: NameMap, old: NameMap) -> NameMap:
    return _inherit_mapunit(new, old)


def inherit_titlemap(new: TitleMap, old: TitleMap) -> TitleMap:
    return _inherit_mapunit(new, old)


def inherit_wordmap(new: WordMap, old: WordMap) -> WordMap:
    return _inherit_mapunit(new, old)


def inherit_waymap(new: WayMap, old: WayMap) -> WayMap:
    return _inherit_mapunit(new, old)
