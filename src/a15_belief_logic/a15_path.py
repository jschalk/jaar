from src.a00_data_toolbox.file_toolbox import create_path
from src.a01_term_logic.term import BelieverName, LabelTerm
from src.a12_hub_toolbox.a12_path import create_bud_dir_path

BUD_MANDATE_FILENAME = "bud_person_mandate_ledger.json"


def create_bud_person_mandate_ledger_path(
    belief_mstr_dir: str,
    belief_label: LabelTerm,
    believer_name: BelieverName,
    bud_time: int,
) -> str:
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\buds\n\\bud_time\\bud_person_mandate_ledger.json"""
    timepoint_dir = create_bud_dir_path(
        belief_mstr_dir, belief_label, believer_name, bud_time
    )
    return create_path(timepoint_dir, "bud_person_mandate_ledger.json")
