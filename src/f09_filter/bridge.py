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
    RoadUnit,
    RoadNode,
)
from src.f04_gift.atom_config import (
    get_atom_args_python_types,
    type_AcctID_str,
    type_GroupID_str,
    type_RoadUnit_str,
)
from dataclasses import dataclass
from copy import copy as copy_copy


class set_all_src_to_dstException(Exception):
    pass


class atom_args_python_typeException(Exception):
    pass


def filterable_python_types() -> set:
    return {"AcctID", "GroupID", "RoadNode", "RoadUnit"}


def filterable_atom_args() -> set:
    return {
        "acct_id",
        "road",
        "parent_road",
        "label",
        "healer_id",
        "need",
        "base",
        "pick",
        "group_id",
    }


@dataclass
class BridgeKind:
    src_to_dst: dict[any:any] = None
    unknown_word: str = None
    src_road_delimiter: str = None
    dst_road_delimiter: str = None
    explicit_label_map: dict = None
    python_type: str = None
    face_id: str = None

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
            if self.python_type in {"GroupID"}:
                src_r_delimiter = self.src_road_delimiter
                dst_r_delimiter = self.dst_road_delimiter
                dst_word = dst_word.replace(src_r_delimiter, dst_r_delimiter)
            if self.python_type in {"RoadUnit", "RoadNode"}:
                dst_word = self._get_create_roadunit_dst(src_word)
            if self.dst_road_delimiter in src_word:
                return None
            self.set_src_to_dst(src_word, dst_word)
        return self._get_dst_value(src_word)

    def _get_create_roadunit_dst(self, src_road) -> RoadUnit:
        src_parent_road = get_parent_road(src_road, self.src_road_delimiter)
        if is_roadnode(src_road, self.src_road_delimiter):
            return self._get_explicit_roadnode(src_road)
        elif self.src_exists(src_parent_road) is False:
            return None
        src_terminus = get_terminus_node(src_road, self.src_road_delimiter)
        src_terminus = self._get_explicit_roadnode(src_terminus)
        dst_parent_road = self._get_dst_value(src_parent_road)
        return create_road(dst_parent_road, src_terminus, self.dst_road_delimiter)

    def _get_explicit_roadnode(self, x_roadNode: RoadNode) -> RoadNode:
        if self.explicit_src_label_exists(x_roadNode):
            return self._get_explicit_dst_label(x_roadNode)
        return x_roadNode

    def src_to_dst_exists(self, src_word: str, dst_word: str) -> bool:
        return self._get_dst_value(src_word) == dst_word

    def src_exists(self, src_word: str) -> bool:
        return self._get_dst_value(src_word) != None

    def del_src_to_dst(self, src_word: str):
        self.src_to_dst.pop(src_word)

    def set_explicit_label_map(self, src_label: RoadNode, dst_label: RoadNode):
        self.explicit_label_map[src_label] = dst_label

    def _get_explicit_dst_label(self, src_label: RoadNode) -> RoadNode:
        return self.explicit_label_map.get(src_label)

    def explicit_label_map_exists(
        self, src_label: RoadNode, dst_label: RoadNode
    ) -> bool:
        return self._get_explicit_dst_label(src_label) == dst_label

    def explicit_src_label_exists(self, src_label: RoadNode) -> bool:
        return self._get_explicit_dst_label(src_label) != None

    def del_explicit_label_map(self, src_label: RoadNode) -> bool:
        self.explicit_label_map.pop(src_label)

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
        if self.python_type in {"AcctID", "RoadNode"}:
            return not self._src_road_delimiter_in_src_words()
        elif self.python_type in {"GroupID"}:
            return str_in_all_dict_keys(self.src_road_delimiter, self.src_to_dst)
        elif self.python_type in {"RoadUnit"}:
            return True

    def _is_dst_delimiter_inclusion_correct(self) -> bool:
        if self.python_type in {"AcctID", "RoadNode"}:
            return not self._dst_road_delimiter_in_dst_words()
        elif self.python_type in {"GroupID"}:
            return str_in_all_dict_values(self.dst_road_delimiter, self.src_to_dst)
        elif self.python_type in {"RoadUnit"}:
            return True

    def all_src_parent_roads_exist(self) -> bool:
        if self.python_type not in {"RoadUnit"}:
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
            and self.all_src_parent_roads_exist()
        )

    def get_dict(self) -> dict:
        return {
            "src_road_delimiter": self.src_road_delimiter,
            "dst_road_delimiter": self.dst_road_delimiter,
            "unknown_word": self.unknown_word,
            "explicit_label_map": self.explicit_label_map,
            "src_to_dst": self.src_to_dst,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def bridgekind_shop(
    x_python_type: str,
    x_src_road_delimiter: str = None,
    x_dst_road_delimiter: str = None,
    x_explicit_label_map: dict = None,
    x_src_to_dst: dict = None,
    x_unknown_word: str = None,
    x_face_id: str = None,
) -> BridgeKind:
    if x_unknown_word is None:
        x_unknown_word = default_unknown_word()
    if x_src_road_delimiter is None:
        x_src_road_delimiter = default_road_delimiter_if_none()
    if x_dst_road_delimiter is None:
        x_dst_road_delimiter = default_road_delimiter_if_none()

    return BridgeKind(
        python_type=x_python_type,
        src_to_dst=get_empty_dict_if_none(x_src_to_dst),
        unknown_word=x_unknown_word,
        src_road_delimiter=x_src_road_delimiter,
        dst_road_delimiter=x_dst_road_delimiter,
        explicit_label_map=get_empty_dict_if_none(x_explicit_label_map),
        face_id=x_face_id,
    )


def default_unknown_word() -> str:
    return "UNKNOWN"


def get_bridgekind_from_dict(x_dict: dict) -> BridgeKind:
    return bridgekind_shop(
        x_python_type=x_dict.get("python_type"),
        x_dst_road_delimiter=x_dict.get("dst_road_delimiter"),
        x_explicit_label_map=x_dict.get("explicit_label_map"),
        x_src_road_delimiter=x_dict.get("src_road_delimiter"),
        x_src_to_dst=x_dict.get("src_to_dst"),
        x_unknown_word=x_dict.get("unknown_word"),
    )


def get_bridgekind_from_json(x_json: str) -> BridgeKind:
    return get_bridgekind_from_dict(get_dict_from_json(x_json))


@dataclass
class BridgeUnit:
    face_id: str = None
    bridgekinds: dict[str, BridgeKind] = None
    unknown_word: str = None
    src_road_delimiter: str = None
    dst_road_delimiter: str = None

    def set_bridgekind(self, x_bridgekind: BridgeKind):
        if self.src_road_delimiter != x_bridgekind.src_road_delimiter:
            exception_str = f"set_bridgekind Error: BrideUnit src_road_delimiter is '{self.src_road_delimiter}', BridgeKind is '{x_bridgekind.src_road_delimiter}'."
            raise atom_args_python_typeException(exception_str)
        if self.dst_road_delimiter != x_bridgekind.dst_road_delimiter:
            exception_str = f"set_bridgekind Error: BrideUnit dst_road_delimiter is '{self.dst_road_delimiter}', BridgeKind is '{x_bridgekind.dst_road_delimiter}'."
            raise atom_args_python_typeException(exception_str)
        if self.unknown_word != x_bridgekind.unknown_word:
            exception_str = f"set_bridgekind Error: BrideUnit unknown_word is '{self.unknown_word}', BridgeKind is '{x_bridgekind.unknown_word}'."
            raise atom_args_python_typeException(exception_str)

        self.bridgekinds[x_bridgekind.python_type] = x_bridgekind

    def get_bridgekind(self, x_python_type: str) -> BridgeKind:
        return self.bridgekinds.get(x_python_type)

    # def set_atom_arg(self, x_atom_arg: str):
    #     x_atom_python_type = get_atom_args_python_types().get(x_atom_arg)
    #     if x_atom_python_type is None:
    #         exception_str = (
    #             f"set_atom_arg Error: '{x_atom_arg}' not arg in atom_config."
    #         )
    #         raise atom_args_python_typeException(exception_str)

    #     self.atom_arg = x_atom_arg
    #     self.python_type = x_atom_python_type


def bridgeunit_shop(
    x_face_id: str,
    x_src_road_delimiter: str = None,
    x_dst_road_delimiter: str = None,
    x_unknown_word: str = None,
) -> BridgeUnit:
    if x_unknown_word is None:
        x_unknown_word = default_unknown_word()
    if x_src_road_delimiter is None:
        x_src_road_delimiter = default_road_delimiter_if_none()
    if x_dst_road_delimiter is None:
        x_dst_road_delimiter = default_road_delimiter_if_none()

    x_bridgekinds = {
        type_AcctID_str(): bridgekind_shop(
            x_python_type=type_AcctID_str(),
            x_unknown_word=x_unknown_word,
            x_src_road_delimiter=x_src_road_delimiter,
            x_dst_road_delimiter=x_dst_road_delimiter,
        ),
        type_GroupID_str(): bridgekind_shop(
            x_python_type=type_GroupID_str(),
            x_unknown_word=x_unknown_word,
            x_src_road_delimiter=x_src_road_delimiter,
            x_dst_road_delimiter=x_dst_road_delimiter,
        ),
        type_RoadUnit_str(): bridgekind_shop(
            x_python_type=type_RoadUnit_str(),
            x_unknown_word=x_unknown_word,
            x_src_road_delimiter=x_src_road_delimiter,
            x_dst_road_delimiter=x_dst_road_delimiter,
        ),
    }

    return BridgeUnit(
        face_id=x_face_id,
        unknown_word=x_unknown_word,
        src_road_delimiter=x_src_road_delimiter,
        dst_road_delimiter=x_dst_road_delimiter,
        bridgekinds=x_bridgekinds,
    )
