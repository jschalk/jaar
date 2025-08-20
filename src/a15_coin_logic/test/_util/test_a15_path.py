from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from src.a00_data_toolbox.file_toolbox import create_path
from src.a09_pack_logic.test._util.a09_str import (
    believer_name_str,
    bud_time_str,
    coin_label_str,
)
from src.a12_hub_toolbox.test._util.a12_env import get_module_temp_dir
from src.a15_coin_logic.a15_path import (
    BUD_MANDATE_FILENAME,
    create_bud_partner_mandate_ledger_path,
)


def test_create_bud_partner_mandate_ledger_path_ReturnsObj():
    # ESTABLISH
    x_coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    timepoint7 = 7

    # WHEN
    gen_bud_path = create_bud_partner_mandate_ledger_path(
        x_coin_mstr_dir, a23_str, sue_str, timepoint7
    )

    # THEN
    x_coins_dir = create_path(x_coin_mstr_dir, "coins")
    amy23_dir = create_path(x_coins_dir, a23_str)
    believers_dir = create_path(amy23_dir, "believers")
    sue_dir = create_path(believers_dir, sue_str)
    buds_dir = create_path(sue_dir, "buds")
    timepoint_dir = create_path(buds_dir, timepoint7)
    expected_bud_path_dir = create_path(timepoint_dir, BUD_MANDATE_FILENAME)
    assert gen_bud_path == expected_bud_path_dir


LINUX_OS = platform_system() == "Linux"


def test_create_bud_partner_mandate_ledger_path_HasDocString():
    # ESTABLISH
    doc_str = create_bud_partner_mandate_ledger_path(
        coin_mstr_dir="coin_mstr_dir",
        coin_label=coin_label_str(),
        believer_name=believer_name_str(),
        bud_time=bud_time_str(),
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_bud_partner_mandate_ledger_path) == doc_str
