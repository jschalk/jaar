from json import loads as json_loads
from pathlib import Path
from src.a00_data_toolbox.file_toolbox import count_files, save_json
from src.a06_plan_logic.test._util.a06_str import (
    belief_label_str,
    concept_rope_str,
    gogo_want_str,
    owner_name_str,
    plan_conceptunit_str,
)
from src.a08_plan_atom_logic.atom_config import get_atom_config_args
from src.a17_idea_logic.idea_config import (
    get_default_sorted_list,
    get_idea_config_dict,
    get_idea_formats_dir,
    get_idea_numbers,
)
from src.a17_idea_logic.test._util.a17_str import attributes_str, dimens_str


def create_dimens_idea_format_dict() -> dict:
    idea_format_files_dict = {}
    x_count = 20
    for idea_dimen, dimen_dict in get_idea_config_dict().items():
        if dimen_dict.get("idea_category") == "plan":
            idea_filename = f"idea_format_{x_count:05}_{idea_dimen}_v0_0_0.json"
            attributes_set = {belief_label_str(), owner_name_str()}
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
    plan_conceptunit_filename = (
        f"idea_format_00028_{plan_conceptunit_str()}_v0_0_0.json"
    )
    assert dimens_idea_format_dict.get(plan_conceptunit_filename)
    plan_conceptunit_dict = dimens_idea_format_dict.get(plan_conceptunit_filename)
    assert plan_conceptunit_dict.get(dimens_str()) == [plan_conceptunit_str()]
    assert plan_conceptunit_dict.get(attributes_str())
    plan_conceptunit_attributes = plan_conceptunit_dict.get(attributes_str())
    assert belief_label_str() in plan_conceptunit_attributes
    assert owner_name_str() in plan_conceptunit_attributes
    assert concept_rope_str() in plan_conceptunit_attributes
    assert gogo_want_str() in plan_conceptunit_attributes

    rebuild_format_jsons(rebuild_bool)


def rebuild_format_jsons(x_rebuild_format_jsons: bool):
    if x_rebuild_format_jsons:
        for x_filename, idea_format in create_dimens_idea_format_dict().items():
            save_json(get_idea_formats_dir(), x_filename, idea_format)


def test_idea_brick_formats_MarkdownFileExists():
    # Gather lines here
    doc_main_dir = "docs"
    doc_ideas_dir = Path(f"{doc_main_dir}/a17_idea_brick_formats")
    doc_ideas_dir.mkdir(parents=True, exist_ok=True)

    manifest_lines = []
    idea_formats_dir = Path(get_idea_formats_dir())
    for json_path in sorted(idea_formats_dir.glob("*.json")):
        data = json_loads(json_path.read_text())
        # print(f"{data=}")

        # Basic validation
        assert "idea_number" in data, f"{json_path.name} missing 'idea_number'"
        assert "attributes" in data, f"{json_path.name} missing 'attributes'"
        assertion_fail_str = f"{json_path.name} has malformed 'attributes'"
        assert isinstance(data["attributes"], dict), assertion_fail_str

        idea = data["idea_number"]
        attr_names = list(data["attributes"].keys())
        dimens = list(data["dimens"])
        sorted_attrs = get_default_sorted_list(attr_names)
        manifest_line = f"- [`{idea}`](ideas/{idea}.md): " + ", ".join(sorted_attrs)
        manifest_lines.append(manifest_line)

        # Create per-idea Markdown file
        idea_md_path = doc_ideas_dir / f"{idea}.md"
        idea_md_lines = [
            f"# Idea `{idea}`\n",
            f"## Dimens `{dimens}`\n",
            "## Attributes",
            *(f"- `{attr}`" for attr in sorted_attrs),
        ]
        idea_md_path.write_text("\n".join(idea_md_lines) + "\n")

    # Where the Markdown manifest will be written
    dst_path = Path(f"{doc_main_dir}/idea_brick_formats.md")
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    dst_path.write_text("# Idea Manifest\n\n" + "\n".join(manifest_lines))
    assert dst_path.exists(), f"Failed to write manifest to {dst_path}"

    assertion_fail_str = f"Expected {len(get_idea_numbers())} idea files, found {count_files(doc_ideas_dir)}"
    assert count_files(doc_ideas_dir) == len(get_idea_numbers()), assertion_fail_str
