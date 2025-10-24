from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import create_path
from src.ch12_bud._ref.ch12_path import (
    create_cell_dir_path as cell_dir,
    create_cell_json_path as node_path,
)
from src.ch12_bud.bud_filehandler import (
    cellunit_get_from_dir,
    cellunit_save_to_dir,
    save_arbitrary_beliefspark as save_beliefspark,
)
from src.ch12_bud.cell import cellunit_shop
from src.ch15_moment.moment_cell import create_cell_tree
from src.ch15_moment.test._util.ch15_env import get_temp_dir, temp_dir_setup


def test_create_cell_tree_Scenaro0_epochtime_Empty(temp_dir_setup):
    # ESTABLISH
    moment_mstr_dir = create_path(get_temp_dir(), "Fay_mstr")
    a23_str = "amy23"
    bob_str = "Bob"
    tp37 = 37

    a23_bob_tp37_path = cell_dir(moment_mstr_dir, a23_str, bob_str, tp37, [])
    print(f"{a23_bob_tp37_path=}")
    assert os_path_exists(a23_bob_tp37_path) is False

    # WHEN
    create_cell_tree(moment_mstr_dir, a23_str, bob_str, tp37)

    # THEN
    assert os_path_exists(a23_bob_tp37_path) is False


def test_create_cell_tree_Scenaro1_LedgerDepth0(temp_dir_setup):
    # ESTABLISH
    moment_mstr_dir = create_path(get_temp_dir(), "Fay_mstr")
    a23_str = "amy23"
    bob_str = "Bob"
    yao_str = "Yao"
    tp37 = 37  # epochtime
    bud1_quota = 450
    bud1_celldepth = 0
    spark56 = 56
    x_cell = cellunit_shop(bob_str, [], spark56, bud1_celldepth, quota=bud1_quota)
    bob37_root_cell_dir = cell_dir(moment_mstr_dir, a23_str, bob_str, tp37, [])
    cellunit_save_to_dir(bob37_root_cell_dir, x_cell)
    save_beliefspark(moment_mstr_dir, a23_str, bob_str, spark56, [[yao_str], [bob_str]])
    assert (
        cellunit_get_from_dir(bob37_root_cell_dir).get_beliefsparks_quota_ledger() == {}
    )

    # WHEN
    create_cell_tree(moment_mstr_dir, a23_str, bob_str, tp37)

    # THEN
    bob37_root_cell = cellunit_get_from_dir(bob37_root_cell_dir)
    generated_bob37_quota_ledger = bob37_root_cell.get_beliefsparks_quota_ledger()
    assert generated_bob37_quota_ledger == {"Bob": 225, yao_str: 225}


def test_create_cell_tree_Scenaro2_LedgerDepth1(temp_dir_setup):
    # ESTABLISH
    moment_mstr_dir = create_path(get_temp_dir(), "Fay_mstr")
    a23_str = "amy23"
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    tp37 = 37  # epochtime
    x_quota = 450
    x_celldepth = 1
    spark56 = 56
    x_cell = cellunit_shop(bob_str, [], spark56, x_celldepth, quota=x_quota)
    bob37_dir = cell_dir(moment_mstr_dir, a23_str, bob_str, tp37, [])
    cellunit_save_to_dir(bob37_dir, x_cell)
    bob_voices = [[yao_str], [bob_str], [zia_str]]
    yao_voices = [[zia_str]]
    zia_voices = [[bob_str], [yao_str]]
    bob_e56_path = save_beliefspark(
        moment_mstr_dir, a23_str, bob_str, spark56, bob_voices
    )
    yao_e56_path = save_beliefspark(
        moment_mstr_dir, a23_str, yao_str, spark56, yao_voices
    )
    zia_e56_path = save_beliefspark(
        moment_mstr_dir, a23_str, zia_str, spark56, zia_voices
    )
    assert os_path_exists(bob_e56_path)
    assert os_path_exists(yao_e56_path)
    assert os_path_exists(zia_e56_path)
    bob37_node_path = node_path(moment_mstr_dir, a23_str, bob_str, tp37, [])
    bob37_bob_node_path = node_path(moment_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    bob37_yao_node_path = node_path(moment_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    bob37_zia_node_path = node_path(moment_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path) is False
    assert os_path_exists(bob37_yao_node_path) is False
    assert os_path_exists(bob37_zia_node_path) is False
    assert cellunit_get_from_dir(bob37_dir).get_beliefsparks_quota_ledger() == {}

    # WHEN
    create_cell_tree(moment_mstr_dir, a23_str, bob_str, tp37)

    # THEN
    print(f"{bob37_bob_node_path=}")
    print(f"{bob37_yao_node_path=}")
    print(f"{bob37_zia_node_path=}")
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path)
    assert os_path_exists(bob37_yao_node_path)
    assert os_path_exists(bob37_zia_node_path)
    bob37_bob_dir = cell_dir(moment_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    bob37_yao_dir = cell_dir(moment_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    bob37_zia_dir = cell_dir(moment_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    bob37_cell = cellunit_get_from_dir(bob37_dir)
    bob37_bob_cell = cellunit_get_from_dir(bob37_bob_dir)
    bob37_yao_cell = cellunit_get_from_dir(bob37_yao_dir)
    bob37_zia_cell = cellunit_get_from_dir(bob37_zia_dir)
    assert bob37_cell.ancestors == []
    assert bob37_cell.spark_num == 56
    assert bob37_cell.celldepth == 1
    assert bob37_cell.bud_belief_name == bob_str
    assert bob37_cell.mana_grain == 1
    assert bob37_cell.quota == 450
    assert bob37_bob_cell.ancestors == [bob_str]
    assert bob37_bob_cell.spark_num == 56
    assert bob37_bob_cell.celldepth == 0
    assert bob37_bob_cell.bud_belief_name == bob_str
    assert bob37_bob_cell.mana_grain == 1
    assert bob37_bob_cell.quota == 150
    assert bob37_yao_cell.ancestors == [yao_str]
    assert bob37_yao_cell.spark_num == 56
    assert bob37_yao_cell.celldepth == 0
    assert bob37_yao_cell.bud_belief_name == bob_str
    assert bob37_yao_cell.mana_grain == 1
    assert bob37_yao_cell.quota == 150
    assert bob37_zia_cell.ancestors == [zia_str]
    assert bob37_zia_cell.spark_num == 56
    assert bob37_zia_cell.celldepth == 0
    assert bob37_zia_cell.bud_belief_name == bob_str
    assert bob37_zia_cell.mana_grain == 1
    assert bob37_zia_cell.quota == 150
    gen_bob37_quota_ledger = bob37_cell.get_beliefsparks_quota_ledger()
    gen_bob37_bob_quota_ledger = bob37_bob_cell.get_beliefsparks_quota_ledger()
    gen_bob37_yao_quota_ledger = bob37_yao_cell.get_beliefsparks_quota_ledger()
    gen_bob37_zia_quota_ledger = bob37_zia_cell.get_beliefsparks_quota_ledger()
    assert gen_bob37_quota_ledger == {bob_str: 150, yao_str: 150, zia_str: 150}
    assert gen_bob37_bob_quota_ledger == {bob_str: 50, yao_str: 50, zia_str: 50}
    assert gen_bob37_yao_quota_ledger == {zia_str: 150}
    assert gen_bob37_zia_quota_ledger == {bob_str: 75, yao_str: 75}


def test_create_cell_tree_Scenaro3_LedgerDepth1_MostRecentSpark(temp_dir_setup):
    # ESTABLISH
    moment_mstr_dir = create_path(get_temp_dir(), "Fay_mstr")
    a23_str = "amy23"
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    tp37 = 37  # epochtime
    x_quota = 450
    x_celldepth = 1
    spark33 = 33
    spark44 = 44
    spark55 = 55
    x_cell = cellunit_shop(bob_str, [], spark55, x_celldepth, quota=x_quota)
    bob37_dir = cell_dir(moment_mstr_dir, a23_str, bob_str, tp37, [])
    cellunit_save_to_dir(bob37_dir, x_cell)
    bob_voices = [[yao_str], [bob_str], [zia_str]]
    yao_voices = [[zia_str]]
    zia_voices = [[bob_str], [yao_str]]
    bob_e55_path = save_beliefspark(
        moment_mstr_dir, a23_str, bob_str, spark55, bob_voices
    )
    yao_e44_path = save_beliefspark(
        moment_mstr_dir, a23_str, yao_str, spark44, yao_voices
    )
    yao_e33_path = save_beliefspark(
        moment_mstr_dir, a23_str, yao_str, spark33, yao_voices
    )
    zia_e33_path = save_beliefspark(
        moment_mstr_dir, a23_str, zia_str, spark33, zia_voices
    )
    assert os_path_exists(bob_e55_path)
    assert os_path_exists(yao_e44_path)
    assert os_path_exists(zia_e33_path)
    bob37_node_path = node_path(moment_mstr_dir, a23_str, bob_str, tp37, [])
    bob37_bob_node_path = node_path(moment_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    bob37_yao_node_path = node_path(moment_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    bob37_zia_node_path = node_path(moment_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path) is False
    assert os_path_exists(bob37_yao_node_path) is False
    assert os_path_exists(bob37_zia_node_path) is False

    # WHEN
    create_cell_tree(moment_mstr_dir, a23_str, bob_str, tp37)

    # THEN
    print(f"{bob37_bob_node_path=}")
    print(f"{bob37_yao_node_path=}")
    print(f"{bob37_zia_node_path=}")
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path)
    assert os_path_exists(bob37_yao_node_path)
    assert os_path_exists(bob37_zia_node_path)
    bob37_bob_dir = cell_dir(moment_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    bob37_yao_dir = cell_dir(moment_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    bob37_zia_dir = cell_dir(moment_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    bob37_cell = cellunit_get_from_dir(bob37_dir)
    bob37_bob_cell = cellunit_get_from_dir(bob37_bob_dir)
    bob37_yao_cell = cellunit_get_from_dir(bob37_yao_dir)
    bob37_zia_cell = cellunit_get_from_dir(bob37_zia_dir)
    assert bob37_cell.ancestors == []
    assert bob37_cell.spark_num == 55
    assert bob37_cell.celldepth == 1
    assert bob37_cell.bud_belief_name == bob_str
    assert bob37_cell.mana_grain == 1
    assert bob37_cell.quota == 450
    assert bob37_bob_cell.ancestors == [bob_str]
    assert bob37_bob_cell.spark_num == 55
    assert bob37_bob_cell.celldepth == 0
    assert bob37_bob_cell.bud_belief_name == bob_str
    assert bob37_bob_cell.mana_grain == 1
    assert bob37_bob_cell.quota == 150
    assert bob37_yao_cell.ancestors == [yao_str]
    assert bob37_yao_cell.spark_num == 44
    assert bob37_yao_cell.celldepth == 0
    assert bob37_yao_cell.bud_belief_name == bob_str
    assert bob37_yao_cell.mana_grain == 1
    assert bob37_yao_cell.quota == 150
    assert bob37_zia_cell.ancestors == [zia_str]
    assert bob37_zia_cell.spark_num == 33
    assert bob37_zia_cell.celldepth == 0
    assert bob37_zia_cell.bud_belief_name == bob_str
    assert bob37_zia_cell.mana_grain == 1
    assert bob37_zia_cell.quota == 150
    gen_bob37_quota_ledger = bob37_cell.get_beliefsparks_quota_ledger()
    gen_bob37_bob_quota_ledger = bob37_bob_cell.get_beliefsparks_quota_ledger()
    gen_bob37_yao_quota_ledger = bob37_yao_cell.get_beliefsparks_quota_ledger()
    gen_bob37_zia_quota_ledger = bob37_zia_cell.get_beliefsparks_quota_ledger()
    assert gen_bob37_quota_ledger == {bob_str: 150, yao_str: 150, zia_str: 150}
    assert gen_bob37_bob_quota_ledger == {bob_str: 50, yao_str: 50, zia_str: 50}
    assert gen_bob37_yao_quota_ledger == {zia_str: 150}
    assert gen_bob37_zia_quota_ledger == {bob_str: 75, yao_str: 75}


def test_create_cell_tree_Scenaro4_LedgerDepth1_OneBeliefHasNoPast_beliefspark(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = create_path(get_temp_dir(), "Fay_mstr")
    a23_str = "amy23"
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    tp37 = 37  # epochtime
    x_quota = 450
    x_celldepth = 1
    spark33 = 33
    spark44 = 44
    spark55 = 55
    spark66 = 66
    x_cell = cellunit_shop(bob_str, [], spark55, x_celldepth, quota=x_quota)
    bob37_dir = cell_dir(moment_mstr_dir, a23_str, bob_str, tp37, [])
    cellunit_save_to_dir(bob37_dir, x_cell)
    bob_voices = [[yao_str], [bob_str], [zia_str]]
    yao_voices = [[zia_str]]
    zia_voices = [[bob_str], [yao_str]]
    bob_e55_path = save_beliefspark(
        moment_mstr_dir, a23_str, bob_str, spark55, bob_voices
    )
    yao_e44_path = save_beliefspark(
        moment_mstr_dir, a23_str, yao_str, spark44, yao_voices
    )
    yao_e33_path = save_beliefspark(
        moment_mstr_dir, a23_str, yao_str, spark33, yao_voices
    )
    zia_e66_path = save_beliefspark(
        moment_mstr_dir, a23_str, zia_str, spark66, zia_voices
    )
    assert os_path_exists(bob_e55_path)
    assert os_path_exists(yao_e44_path)
    assert os_path_exists(zia_e66_path)
    bob37_dir = cell_dir(moment_mstr_dir, a23_str, bob_str, tp37, [])
    bob37_node_path = node_path(moment_mstr_dir, a23_str, bob_str, tp37, [])
    bob37_bob_node_path = node_path(moment_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    bob37_yao_node_path = node_path(moment_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    bob37_zia_node_path = node_path(moment_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path) is False
    assert os_path_exists(bob37_yao_node_path) is False
    assert os_path_exists(bob37_zia_node_path) is False

    # WHEN
    create_cell_tree(moment_mstr_dir, a23_str, bob_str, tp37)

    # THEN
    print(f"{bob37_bob_node_path=}")
    print(f"{bob37_yao_node_path=}")
    print(f"{bob37_zia_node_path=}")
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path)
    assert os_path_exists(bob37_yao_node_path)
    assert os_path_exists(bob37_zia_node_path) is False
    bob37_bob_dir = cell_dir(moment_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    bob37_yao_dir = cell_dir(moment_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    bob37_cell = cellunit_get_from_dir(bob37_dir)
    bob37_bob_cell = cellunit_get_from_dir(bob37_bob_dir)
    bob37_yao_cell = cellunit_get_from_dir(bob37_yao_dir)
    assert bob37_bob_cell.ancestors == [bob_str]
    assert bob37_bob_cell.spark_num == 55
    assert bob37_bob_cell.celldepth == 0
    assert bob37_bob_cell.bud_belief_name == bob_str
    assert bob37_bob_cell.mana_grain == 1
    assert bob37_bob_cell.quota == 150
    assert bob37_yao_cell.ancestors == [yao_str]
    assert bob37_yao_cell.spark_num == 44
    assert bob37_yao_cell.celldepth == 0
    assert bob37_yao_cell.bud_belief_name == bob_str
    assert bob37_yao_cell.mana_grain == 1
    assert bob37_yao_cell.quota == 150
    gen_bob37_quota_ledger = bob37_cell.get_beliefsparks_quota_ledger()
    gen_bob37_bob_quota_ledger = bob37_bob_cell.get_beliefsparks_quota_ledger()
    gen_bob37_yao_quota_ledger = bob37_yao_cell.get_beliefsparks_quota_ledger()
    assert gen_bob37_quota_ledger == {bob_str: 150, yao_str: 150, zia_str: 150}
    assert gen_bob37_bob_quota_ledger == {bob_str: 50, yao_str: 50, zia_str: 50}
    assert gen_bob37_yao_quota_ledger == {zia_str: 150}


def test_create_cell_tree_Scenaro5_LedgerDepth1_ZeroQuotaDoesNotGetCreated(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = create_path(get_temp_dir(), "Fay_mstr")
    a23_str = "amy23"
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    tp37 = 37  # epochtime
    x_quota = 2
    x_celldepth = 1
    spark33 = 33
    spark44 = 44
    spark55 = 55
    x_cell = cellunit_shop(bob_str, [], spark55, x_celldepth, quota=x_quota)
    bob37_dir = cell_dir(moment_mstr_dir, a23_str, bob_str, tp37, [])
    cellunit_save_to_dir(bob37_dir, x_cell)
    bob_voices = [[yao_str], [bob_str], [zia_str]]
    yao_voices = [[zia_str]]
    zia_voices = [[bob_str], [yao_str]]
    bob_e55_path = save_beliefspark(
        moment_mstr_dir, a23_str, bob_str, spark55, bob_voices
    )
    yao_e44_path = save_beliefspark(
        moment_mstr_dir, a23_str, yao_str, spark44, yao_voices
    )
    yao_e33_path = save_beliefspark(
        moment_mstr_dir, a23_str, yao_str, spark33, yao_voices
    )
    zia_e33_path = save_beliefspark(
        moment_mstr_dir, a23_str, zia_str, spark33, zia_voices
    )
    assert os_path_exists(bob_e55_path)
    assert os_path_exists(yao_e44_path)
    assert os_path_exists(zia_e33_path)
    bob37_dir = cell_dir(moment_mstr_dir, a23_str, bob_str, tp37, [])
    bob37_node_path = node_path(moment_mstr_dir, a23_str, bob_str, tp37, [])
    bob37_bob_node_path = node_path(moment_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    bob37_yao_node_path = node_path(moment_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    bob37_zia_node_path = node_path(moment_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path) is False
    assert os_path_exists(bob37_yao_node_path) is False
    assert os_path_exists(bob37_zia_node_path) is False

    # WHEN
    create_cell_tree(moment_mstr_dir, a23_str, bob_str, tp37)

    # THEN
    print(f"{bob37_bob_node_path=}")
    print(f"{bob37_yao_node_path=}")
    print(f"{bob37_zia_node_path=}")
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path) is False
    assert os_path_exists(bob37_yao_node_path)
    assert os_path_exists(bob37_zia_node_path)
    bob37_bob_dir = cell_dir(moment_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    bob37_yao_dir = cell_dir(moment_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    bob37_zia_dir = cell_dir(moment_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    bob37_cell = cellunit_get_from_dir(bob37_dir)
    bob37_yao_cell = cellunit_get_from_dir(bob37_yao_dir)
    bob37_zia_cell = cellunit_get_from_dir(bob37_zia_dir)
    gen_bob37_quota_ledger = bob37_cell.get_beliefsparks_quota_ledger()
    gen_bob37_yao_quota_ledger = bob37_yao_cell.get_beliefsparks_quota_ledger()
    gen_bob37_zia_quota_ledger = bob37_zia_cell.get_beliefsparks_quota_ledger()
    assert gen_bob37_quota_ledger == {bob_str: 0, yao_str: 1, zia_str: 1}
    assert gen_bob37_yao_quota_ledger == {zia_str: 1}
    assert gen_bob37_zia_quota_ledger == {bob_str: 1, yao_str: 0}
