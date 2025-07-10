from src.a00_data_toolbox.file_toolbox import create_path, set_dir
from src.a01_term_logic.term import BeliefLabel, BelieverName, LabelTerm
from src.a12_hub_toolbox.a12_path import create_keep_rope_path


def create_keep_path_dir_if_missing(
    belief_mstr_dir: str,
    believer_name: BelieverName,
    belief_label: BeliefLabel,
    keep_rope: LabelTerm,
    knot: str,
):
    keep_path = create_keep_rope_path(
        belief_mstr_dir,
        believer_name,
        belief_label,
        keep_rope,
        knot,
    )
    set_dir(keep_path)
