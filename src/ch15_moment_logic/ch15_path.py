from src.ch01_data_toolbox.file_toolbox import create_path
from src.ch02_rope_logic._ref.ch02_semantic_types import BeliefName, LabelTerm
from src.ch12_hub_toolbox.ch12_path import create_bud_dir_path

BUD_MANDATE_FILENAME = "bud_voice_mandate_ledger.json"


def create_bud_voice_mandate_ledger_path(
    moment_mstr_dir: str,
    moment_label: LabelTerm,
    belief_name: BeliefName,
    bud_time: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\buds\n\\bud_time\\bud_voice_mandate_ledger.json"""
    timepoint_dir = create_bud_dir_path(
        moment_mstr_dir, moment_label, belief_name, bud_time
    )
    return create_path(timepoint_dir, "bud_voice_mandate_ledger.json")
