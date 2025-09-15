from json import loads as json_loads
from pathlib import Path
from src.a00_data_toolbox.file_toolbox import count_files, open_file, save_json
from src.a08_belief_atom_logic.atom_config import get_atom_config_args
from src.a17_idea_logic._ref.a17_doc_builder import (
    get_brick_formats_md,
    get_idea_brick_md,
    get_idea_brick_mds,
)
from src.a17_idea_logic._ref.a17_terms import (
    attributes_str,
    belief_name_str,
    belief_planunit_str,
    c400_number_str,
    dimens_str,
    event_int_str,
    face_name_str,
    fund_iota_str,
    gogo_want_str,
    idea_number_str,
    job_listen_rotations_str,
    knot_str,
    moment_label_str,
    monthday_distortion_str,
    otx_key_str,
    penny_str,
    plan_rope_str,
    respect_bit_str,
    timeline_label_str,
    yr1_jan1_offset_str,
)
from src.a17_idea_logic.idea_config import (
    get_default_sorted_list,
    get_idea_config_dict,
    get_idea_formats_dir,
    get_idea_numbers,
)
from src.a17_idea_logic.test._util.a17_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def create_dimens_idea_format_dict() -> dict:
    idea_format_files_dict = {}
    x_count = 20
    for idea_dimen, dimen_dict in get_idea_config_dict().items():
        if dimen_dict.get("idea_category") == "belief":
            idea_filename = f"idea_format_{x_count:05}_{idea_dimen}_v0_0_0.json"
            attributes_set = {moment_label_str(), belief_name_str()}
            args_dict = get_atom_config_args(idea_dimen)
            attributes_set.update(set(args_dict.keys()))

            idea_format = {"dimens": [idea_dimen], "attributes": attributes_set}
            idea_format_files_dict[idea_filename] = idea_format
            x_count += 1
    return idea_format_files_dict


def test_create_dimens_idea_format_dict_ReturnsObj(rebuild_bool):
    # ESTABLISH / WHEN
    dimens_idea_format_dict = create_dimens_idea_format_dict()
    print(f"{dimens_idea_format_dict.keys()=}")

    # THEN
    assert len(dimens_idea_format_dict) == 10
    belief_planunit_filename = f"idea_format_00028_{belief_planunit_str()}_v0_0_0.json"
    assert dimens_idea_format_dict.get(belief_planunit_filename)
    belief_planunit_dict = dimens_idea_format_dict.get(belief_planunit_filename)
    assert belief_planunit_dict.get(dimens_str()) == [belief_planunit_str()]
    assert belief_planunit_dict.get(attributes_str())
    belief_planunit_attributes = belief_planunit_dict.get(attributes_str())
    assert moment_label_str() in belief_planunit_attributes
    assert belief_name_str() in belief_planunit_attributes
    assert plan_rope_str() in belief_planunit_attributes
    assert gogo_want_str() in belief_planunit_attributes

    rebuild_format_jsons(rebuild_bool)


def rebuild_format_jsons(x_rebuild_format_jsons: bool):
    if x_rebuild_format_jsons:
        for x_filename, idea_format in create_dimens_idea_format_dict().items():
            save_json(get_idea_formats_dir(), x_filename, idea_format)


def test_get_idea_brick_md_ReturnsObj():
    # ESTABLISH
    idea_brick_config = {
        "attributes": {
            knot_str(): {otx_key_str(): False},
            c400_number_str(): {otx_key_str(): False},
            event_int_str(): {otx_key_str(): True},
            face_name_str(): {otx_key_str(): True},
            moment_label_str(): {otx_key_str(): True},
            fund_iota_str(): {otx_key_str(): False},
            job_listen_rotations_str(): {otx_key_str(): False},
            monthday_distortion_str(): {otx_key_str(): False},
            penny_str(): {otx_key_str(): False},
            respect_bit_str(): {otx_key_str(): False},
            timeline_label_str(): {otx_key_str(): False},
            yr1_jan1_offset_str(): {otx_key_str(): False},
        },
        idea_number_str(): "br00000",
        dimens_str(): ["momentunit"],
    }

    # WHEN
    idea_brick_md = get_idea_brick_md(idea_brick_config)

    # THEN
    print(idea_brick_md)
    expected_idea_brick_md = f"""# Idea `br00000`

## Dimens `['momentunit']`

## Attributes
- `{event_int_str()}`
- `{face_name_str()}`
- `{moment_label_str()}`
- `{timeline_label_str()}`
- `{c400_number_str()}`
- `{yr1_jan1_offset_str()}`
- `{monthday_distortion_str()}`
- `{fund_iota_str()}`
- `{penny_str()}`
- `{respect_bit_str()}`
- `{knot_str()}`
- `{job_listen_rotations_str()}`
"""
    assert (idea_brick_md) == expected_idea_brick_md


def test_get_idea_brick_mds_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    temp_dir = get_module_temp_dir()
    br00000_str = "br00000"
    idea_brick_config = {
        "attributes": {
            knot_str(): {otx_key_str(): False},
            c400_number_str(): {otx_key_str(): False},
            event_int_str(): {otx_key_str(): True},
            face_name_str(): {otx_key_str(): True},
            moment_label_str(): {otx_key_str(): True},
            fund_iota_str(): {otx_key_str(): False},
            job_listen_rotations_str(): {otx_key_str(): False},
            monthday_distortion_str(): {otx_key_str(): False},
            penny_str(): {otx_key_str(): False},
            respect_bit_str(): {otx_key_str(): False},
            timeline_label_str(): {otx_key_str(): False},
            yr1_jan1_offset_str(): {otx_key_str(): False},
        },
        idea_number_str(): br00000_str,
        dimens_str(): ["momentunit"],
    }
    save_json(temp_dir, f"{br00000_str}.json", idea_brick_config)

    # WHEN
    idea_brick_mds = get_idea_brick_mds(temp_dir)

    # THEN
    expected_idea_brick_md = f"""# Idea `br00000`

## Dimens `['momentunit']`

## Attributes
- `{event_int_str()}`
- `{face_name_str()}`
- `{moment_label_str()}`
- `{timeline_label_str()}`
- `{c400_number_str()}`
- `{yr1_jan1_offset_str()}`
- `{monthday_distortion_str()}`
- `{fund_iota_str()}`
- `{penny_str()}`
- `{respect_bit_str()}`
- `{knot_str()}`
- `{job_listen_rotations_str()}`
"""
    assert set(idea_brick_mds.keys()) == {br00000_str}
    assert idea_brick_mds == {br00000_str: expected_idea_brick_md}


def test_get_brick_formats_md_ReturnsObj():
    # ESTABLISH / WHEN
    idea_brick_formats_md = get_brick_formats_md()

    # THEN
    assert idea_brick_formats_md
    assert idea_brick_formats_md.find("br00004") > 0
