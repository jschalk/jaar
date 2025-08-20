from src.a00_data_toolbox.file_toolbox import create_path
from src.a01_term_logic.term import BelieverName, LabelTerm
from src.a12_hub_toolbox.a12_path import create_bud_dir_path

BUD_MANDATE_FILENAME = "bud_partner_mandate_ledger.json"


def create_bud_partner_mandate_ledger_path(
    coin_mstr_dir: str,
    coin_label: LabelTerm,
    believer_name: BelieverName,
    bud_time: int,
) -> str:
    """Returns path: coin_mstr_dir\\coins\\coin_label\\believers\\believer_name\\buds\n\\bud_time\\bud_partner_mandate_ledger.json"""
    timepoint_dir = create_bud_dir_path(
        coin_mstr_dir, coin_label, believer_name, bud_time
    )
    return create_path(timepoint_dir, "bud_partner_mandate_ledger.json")
