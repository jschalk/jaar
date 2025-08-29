from src.a00_data_toolbox.file_toolbox import create_path
from src.a01_term_logic.term import BeliefName, LabelTerm
from src.a12_hub_toolbox.a12_path import create_bud_dir_path

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
