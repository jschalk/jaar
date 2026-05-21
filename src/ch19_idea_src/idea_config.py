from ch00_py.file_toolbox import open_json
from importlib.resources import as_file, files
from pathlib import Path


def idea_config_path() -> str:
    "Returns path: ch19_idea_src/idea_config.json"
    module_dir = Path(__file__).resolve().parent
    candidate_path = module_dir / "idea_config.json"
    if candidate_path.exists():
        return str(candidate_path)

    try:
        resource = files(__package__) / "idea_config.json"
        with as_file(resource) as resource_path:
            if resource_path.exists():
                return str(resource_path)
    except Exception:
        pass

    raise FileNotFoundError(
        f"Missing idea_config.json from package resources or module path: {candidate_path}"
    )


def get_idea_config_dict() -> dict:
    return open_json(idea_config_path())


def get_idea_types() -> set:
    return {
        "ii00001",
        "ii00002",
        "ii00005",
        "ii00007",
        "ii00100",
        "ii00101",
        "ii00102",
        "ii00103",
        "ii00104",
        "ii00105",
        "ii00106",
        "ii00112",
        "ii00119",
        "ii00120",
        "ii00121",
        "ii00122",
        "ii00123",
        "ii00124",
        "ii00125",
        "ii00126",
        "ii00127",
        "ii00128",
        "ii00129",
        "ii00136",
        "ii00142",
        "ii00143",
        "ii00144",
        "ii00145",
        "ii00150",
        "ii00151",
        "ii00152",
        "ii00153",
        "ii00154",
        "ii00155",
        "ii00156",
        "ii00157",
        "ii00158",
        "ii00159",
        "ii00170",
        "ii00171",
        "ii00172",
        "ii00173",
        "ii00174",
        "ii00502",
    }


def get_non_mirror_idea_types() -> set[str]:
    return {"ii00502"}


def is_non_mirror(idea_type: str) -> bool:
    return idea_type in get_non_mirror_idea_types()
