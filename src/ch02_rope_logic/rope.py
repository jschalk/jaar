from pathlib import Path as pathlib_Path
from src.ch01_data_toolbox.file_toolbox import is_path_valid
from src.ch02_rope_logic._ref.ch02_semantic_types import (
    LabelTerm,
    RopeTerm,
    default_knot_if_None,
)


class knot_not_in_parent_rope_Exception(Exception):
    pass


def to_rope(label: LabelTerm, knot: str = None) -> LabelTerm:
    x_knot = default_knot_if_None(knot)
    if label is None:
        return x_knot
    label = label if label.find(x_knot) == 0 else f"{x_knot}{label}"
    return label if label.endswith(x_knot) else LabelTerm(f"{label}{x_knot}")


class init_knot_not_presentException(Exception):
    pass


class knot_in_label_Exception(Exception):
    pass


def create_rope(
    parent_rope: RopeTerm,
    tail_label: LabelTerm = None,
    knot: str = None,
    auto_add_first_knot: bool = True,
) -> RopeTerm:
    knot = default_knot_if_None(knot)
    if tail_label in {"", None}:
        return to_rope(parent_rope, knot)

    if parent_rope and parent_rope.find(knot) != 0:
        if auto_add_first_knot:
            parent_rope = to_rope(parent_rope, knot)
        else:
            exception_str = (
                f"Parent rope must have knot '{knot}' at position 0 in string"
            )
            raise init_knot_not_presentException(exception_str)

    tail_label = LabelTerm(tail_label)
    if tail_label.is_label(knot) is False:
        raise knot_in_label_Exception(f"knot '{knot}' is in {tail_label}")
    if tail_label is None:
        return RopeTerm(parent_rope)
    if tail_label.is_label(knot) is False:
        raise knot_in_label_Exception(f"knot '{knot}' is in {tail_label}")
    if parent_rope in {"", None}:
        x_rope = to_rope(tail_label, knot)
    elif parent_rope.endswith(knot):
        x_rope = f"{parent_rope}{tail_label}{knot}"
    else:
        x_rope = f"{parent_rope}{knot}{tail_label}{knot}"
    return to_rope(x_rope, knot)


def rebuild_rope(
    subj_rope: RopeTerm, old_rope: RopeTerm, new_rope: RopeTerm
) -> RopeTerm:
    if subj_rope is None:
        return subj_rope
    elif is_sub_rope(subj_rope, old_rope):
        return subj_rope.replace(old_rope, new_rope, 1)
    else:
        return subj_rope


def is_sub_rope(ref_rope: RopeTerm, sub_rope: RopeTerm) -> bool:
    ref_rope = "" if ref_rope is None else ref_rope
    return ref_rope.find(sub_rope) == 0


def is_heir_rope(src: RopeTerm, heir: RopeTerm, knot: str = None) -> bool:
    return src == heir or heir.find(src) == 0


def find_replace_rope_key_dict(
    dict_x: dict, old_rope: RopeTerm, new_rope: RopeTerm
) -> dict:
    keys_to_delete = []
    objs_to_add = []
    for x_key, x_obj in dict_x.items():
        if old_rope != new_rope and is_sub_rope(ref_rope=x_key, sub_rope=old_rope):
            x_obj.find_replace_rope(old_rope=old_rope, new_rope=new_rope)
            objs_to_add.append(x_obj)
            keys_to_delete.append(x_key)

    for x_obj in objs_to_add:
        dict_x[x_obj.get_obj_key()] = x_obj

    for x_key in keys_to_delete:
        dict_x.pop(x_key)

    return dict_x


def get_all_rope_labels(rope: RopeTerm, knot: str = None) -> list[LabelTerm]:
    return rope.split(default_knot_if_None(knot))[1:-1]


def get_tail_label(rope: RopeTerm, knot: str = None) -> LabelTerm:
    knot = default_knot_if_None(knot)
    if rope in ["", knot]:
        return ""
    all_rope_labels = get_all_rope_labels(rope=rope, knot=knot)
    return all_rope_labels[0] if len(all_rope_labels) == 1 else all_rope_labels[-1]


def get_parent_rope(
    rope: RopeTerm, knot: str = None
) -> RopeTerm:  # rope without tail label
    parent_labels = get_all_rope_labels(rope=rope, knot=knot)[:-1]
    return create_rope_from_labels(parent_labels, knot=knot)


def get_root_label_from_rope(rope: RopeTerm, knot: str = None) -> LabelTerm:
    return get_all_rope_labels(rope=rope, knot=knot)[0]


def get_ancestor_ropes(rope: RopeTerm, knot: str = None) -> list[RopeTerm]:
    knot = default_knot_if_None(knot)
    if not rope:
        return []
    labels = get_all_rope_labels(rope, knot)
    temp_rope = to_rope(labels.pop(0), knot)

    temp_ropes = [temp_rope]
    if labels != []:
        while labels != []:
            temp_rope = create_rope(temp_rope, labels.pop(0), knot)
            temp_ropes.append(temp_rope)

    x_ropes = []
    while temp_ropes != []:
        x_ropes.append(temp_ropes.pop(len(temp_ropes) - 1))
    return x_ropes


def all_ropes_between(src_rope: str, dst_rope: str, knot: str = None) -> list[RopeTerm]:
    x_list = []
    anc_ropes = get_ancestor_ropes(dst_rope, knot)
    while anc_ropes != []:
        anc_rope = anc_ropes.pop()
        if is_sub_rope(anc_rope, src_rope):
            x_list.append(anc_rope)
    return x_list


class ForeFatherException(Exception):
    pass


def get_forefather_ropes(rope: RopeTerm) -> dict[RopeTerm]:
    ancestor_ropes = get_ancestor_ropes(rope=rope)
    popped_rope = ancestor_ropes.pop(0)
    if popped_rope != rope:
        raise ForeFatherException(
            f"Incorrect rope {popped_rope} from out of ancestor_ropes."
        )
    return {a_rope: None for a_rope in ancestor_ropes}


def create_rope_from_labels(labels: list[LabelTerm], knot: str = None) -> RopeTerm:
    return to_rope(default_knot_if_None(knot).join(labels), knot) if labels else ""


class InvalidknotReplaceException(Exception):
    pass


def is_string_in_rope(string: str, rope: RopeTerm) -> bool:
    return rope.find(string) >= 0


def replace_knot(rope: RopeTerm, old_knot: str, new_knot: str) -> str:
    if is_string_in_rope(string=new_knot, rope=rope):
        raise InvalidknotReplaceException(
            f"Cannot replace_knot '{old_knot}' with '{new_knot}' because the new one exists in rope '{rope}'."
        )
    return rope.replace(old_knot, new_knot)


class ValidateLabelTermException(Exception):
    pass


def is_labelterm(x_labelterm: LabelTerm, x_knot: str) -> bool:
    x_labelterm = LabelTerm(x_labelterm)
    return x_labelterm.is_label(knot=x_knot)


def validate_labelterm(
    x_labelterm: LabelTerm, x_knot: str, not_labelterm_required: bool = False
) -> LabelTerm:
    if is_labelterm(x_labelterm, x_knot) and not_labelterm_required:
        raise ValidateLabelTermException(
            f"'{x_labelterm}' needs to not be a LabelTerm. Must contain knot: '{x_knot}'"
        )
    elif is_labelterm(x_labelterm, x_knot) is False and not not_labelterm_required:
        raise ValidateLabelTermException(
            f"'{x_labelterm}' needs to be a LabelTerm. Cannot contain knot: '{x_knot}'"
        )
    return x_labelterm


def rope_is_valid_dir_path(x_rope: RopeTerm, knot: str) -> bool:
    """Returns path built from RopeTerm if it is a valid directory path."""
    x_rope_labels = get_all_rope_labels(x_rope, knot)
    slash_str = "/"
    x_rope_os_path = create_rope_from_labels(x_rope_labels, knot=slash_str)
    parts = pathlib_Path(x_rope_os_path).parts
    parts = parts[1:]
    return False if len(parts) != len(x_rope_labels) else is_path_valid(x_rope_os_path)
