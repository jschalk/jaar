from src.ch01_data_toolbox.file_toolbox import save_json
from src.ch09_belief_atom_logic.atom_config import get_atom_config_args
from src.ch17_idea_logic._ref.ch17_doc_builder import (
    get_brick_formats_md,
    get_idea_brick_md,
    get_idea_brick_mds,
)
from src.ch17_idea_logic._ref.ch17_keywords import (
    Ch02Keywords as wx,
    Ch03Keywords as wx,
    Ch04Keywords as wx,
    Ch07Keywords as wx,
    Ch08Keywords as wx,
    Ch10Keywords as wx,
    Ch15Keywords as wx,
    Ch16Keywords as wx,
    Ch17Keywords as wx,
    gogo_want_str,
    moment_label_str,
    plan_rope_str,
)
from src.ch17_idea_logic.idea_config import get_idea_config_dict, get_idea_formats_dir
from src.ch17_idea_logic.test._util.ch17_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)


def create_dimens_idea_format_dict() -> dict:
    idea_format_files_dict = {}
    x_count = 20
    for idea_dimen, dimen_dict in get_idea_config_dict().items():
        if dimen_dict.get(wx.idea_category) == "belief":
            idea_filename = f"idea_format_{x_count:05}_{idea_dimen}_v0_0_0.json"
            attributes_set = {moment_label_str(), wx.belief_name}
            args_dict = get_atom_config_args(idea_dimen)
            attributes_set.update(set(args_dict.keys()))

            idea_format = {"dimens": [idea_dimen], "attributes": attributes_set}
            idea_format_files_dict[idea_filename] = idea_format
            x_count += 1
    return idea_format_files_dict


def test_create_dimens_idea_format_dict_ReturnsObj(rebuild_bool):
    # ESTABLISH / WHEN
    dimens_idea_format_dict = create_dimens_idea_format_dict()
    for idea_format in sorted(dimens_idea_format_dict.keys()):
        print(f"{idea_format=}")

    # THEN
    assert len(dimens_idea_format_dict) == 10
    belief_planunit_filename = f"idea_format_00026_{wx.belief_planunit}_v0_0_0.json"
    assert dimens_idea_format_dict.get(belief_planunit_filename)
    belief_planunit_dict = dimens_idea_format_dict.get(belief_planunit_filename)
    assert belief_planunit_dict.get(wx.dimens) == [wx.belief_planunit]
    assert belief_planunit_dict.get(wx.attributes)
    belief_planunit_attributes = belief_planunit_dict.get(wx.attributes)
    assert moment_label_str() in belief_planunit_attributes
    assert wx.belief_name in belief_planunit_attributes
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
            wx.knot: {wx.otx_key: False},
            wx.c400_number: {wx.otx_key: False},
            wx.event_int: {wx.otx_key: True},
            wx.face_name: {wx.otx_key: True},
            moment_label_str(): {wx.otx_key: True},
            wx.fund_iota: {wx.otx_key: False},
            wx.job_listen_rotations: {wx.otx_key: False},
            wx.monthday_distortion: {wx.otx_key: False},
            wx.penny: {wx.otx_key: False},
            wx.respect_bit: {wx.otx_key: False},
            wx.timeline_label: {wx.otx_key: False},
            wx.yr1_jan1_offset: {wx.otx_key: False},
        },
        wx.idea_number: "br00000",
        wx.dimens: ["momentunit"],
    }

    # WHEN
    idea_brick_md = get_idea_brick_md(idea_brick_config)

    # THEN
    print(idea_brick_md)
    expected_idea_brick_md = f"""# Idea `br00000`

## Dimens `['momentunit']`

## Attributes
- `{wx.event_int}`
- `{wx.face_name}`
- `{moment_label_str()}`
- `{wx.timeline_label}`
- `{wx.c400_number}`
- `{wx.yr1_jan1_offset}`
- `{wx.monthday_distortion}`
- `{wx.fund_iota}`
- `{wx.penny}`
- `{wx.respect_bit}`
- `{wx.knot}`
- `{wx.job_listen_rotations}`
"""
    assert (idea_brick_md) == expected_idea_brick_md


def test_get_idea_brick_mds_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    temp_dir = get_chapter_temp_dir()
    br00000_str = "br00000"
    idea_brick_config = {
        "attributes": {
            wx.knot: {wx.otx_key: False},
            wx.c400_number: {wx.otx_key: False},
            wx.event_int: {wx.otx_key: True},
            wx.face_name: {wx.otx_key: True},
            moment_label_str(): {wx.otx_key: True},
            wx.fund_iota: {wx.otx_key: False},
            wx.job_listen_rotations: {wx.otx_key: False},
            wx.monthday_distortion: {wx.otx_key: False},
            wx.penny: {wx.otx_key: False},
            wx.respect_bit: {wx.otx_key: False},
            wx.timeline_label: {wx.otx_key: False},
            wx.yr1_jan1_offset: {wx.otx_key: False},
        },
        wx.idea_number: br00000_str,
        wx.dimens: ["momentunit"],
    }
    save_json(temp_dir, f"{br00000_str}.json", idea_brick_config)

    # WHEN
    idea_brick_mds = get_idea_brick_mds(temp_dir)

    # THEN
    expected_idea_brick_md = f"""# Idea `br00000`

## Dimens `['momentunit']`

## Attributes
- `{wx.event_int}`
- `{wx.face_name}`
- `{moment_label_str()}`
- `{wx.timeline_label}`
- `{wx.c400_number}`
- `{wx.yr1_jan1_offset}`
- `{wx.monthday_distortion}`
- `{wx.fund_iota}`
- `{wx.penny}`
- `{wx.respect_bit}`
- `{wx.knot}`
- `{wx.job_listen_rotations}`
"""
    assert set(idea_brick_mds.keys()) == {br00000_str}
    assert idea_brick_mds == {br00000_str: expected_idea_brick_md}


def test_get_brick_formats_md_ReturnsObj():
    # ESTABLISH / WHEN
    idea_brick_formats_md = get_brick_formats_md()

    # THEN
    assert idea_brick_formats_md
    assert idea_brick_formats_md.find("br00004") > 0
