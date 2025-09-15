from pathlib import Path
from src.a00_data_toolbox.file_toolbox import open_json
from src.a17_idea_logic.idea_config import get_default_sorted_list, get_idea_formats_dir


def get_idea_brick_md(idea_brick_config) -> str:
    # Create per-idea Markdown file
    idea = idea_brick_config["idea_number"]
    attr_names = list(idea_brick_config["attributes"].keys())
    dimens = list(idea_brick_config["dimens"])
    sorted_attrs = get_default_sorted_list(attr_names)

    idea_md_lines = [
        f"# Idea `{idea}`\n",
        f"## Dimens `{dimens}`\n",
        "## Attributes",
        *(f"- `{attr}`" for attr in sorted_attrs),
    ]
    return "\n".join(idea_md_lines) + "\n"


def get_idea_brick_mds(idea_brick_format_dir: str = None) -> dict[str,]:
    if not idea_brick_format_dir:
        idea_brick_format_dir = get_idea_formats_dir()

    idea_formats_dir = Path(idea_brick_format_dir)
    idea_brick_mds = {}
    for json_path in sorted(idea_formats_dir.glob("*.json")):
        idea_brick_format = open_json(json_path)
        idea_number = idea_brick_format["idea_number"]
        idea_brick_mds[idea_number] = get_idea_brick_md(idea_brick_format)

    return idea_brick_mds


def get_brick_formats_md():
    idea_formats_dir = Path(get_idea_formats_dir())

    manifest_lines = []
    for json_path in sorted(idea_formats_dir.glob("*.json")):
        data = open_json(json_path)

        idea = data["idea_number"]
        attr_names = list(data["attributes"].keys())
        sorted_attrs = get_default_sorted_list(attr_names)
        manifest_line = f"- [`{idea}`](ideas/{idea}.md): " + ", ".join(sorted_attrs)
        manifest_lines.append(manifest_line)

    # Where the Markdown manifest will be written
    return "# Idea Manifest\n\n" + "\n".join(manifest_lines)
