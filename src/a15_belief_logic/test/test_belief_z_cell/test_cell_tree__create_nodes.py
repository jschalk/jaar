from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path
from src.a11_bud_logic.cell import cellunit_shop
from src.a12_hub_toolbox.hub_path import (
    create_cell_dir_path as cell_dir,
    create_cell_json_path as node_path,
)
from src.a12_hub_toolbox.hub_tool import (
    cellunit_get_from_dir,
    cellunit_save_to_dir,
    save_arbitrary_planevent as save_planevent,
)
from src.a15_belief_logic.belief_cell import create_cell_tree
from src.a15_belief_logic.test._util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_create_cell_tree_Scenaro0_timepoint_Empty(env_dir_setup_cleanup):
    # ESTABLISH
    belief_mstr_dir = create_path(get_module_temp_dir(), "Fay_mstr")
    a23_str = "amy23"
    bob_str = "Bob"
    tp37 = 37

    a23_bob_tp37_path = cell_dir(belief_mstr_dir, a23_str, bob_str, tp37, [])
    print(f"{a23_bob_tp37_path=}")
    assert os_path_exists(a23_bob_tp37_path) is False

    # WHEN
    create_cell_tree(belief_mstr_dir, a23_str, bob_str, tp37)

    # THEN
    assert os_path_exists(a23_bob_tp37_path) is False


def test_create_cell_tree_Scenaro1_LedgerDepth0(env_dir_setup_cleanup):
    # ESTABLISH
    belief_mstr_dir = create_path(get_module_temp_dir(), "Fay_mstr")
    a23_str = "amy23"
    bob_str = "Bob"
    yao_str = "Yao"
    tp37 = 37  # timepoint
    bud1_quota = 450
    bud1_celldepth = 0
    event56 = 56
    x_cell = cellunit_shop(bob_str, [], event56, bud1_celldepth, quota=bud1_quota)
    bob37_root_cell_dir = cell_dir(belief_mstr_dir, a23_str, bob_str, tp37, [])
    cellunit_save_to_dir(bob37_root_cell_dir, x_cell)
    save_planevent(belief_mstr_dir, a23_str, bob_str, event56, [[yao_str], [bob_str]])
    assert (
        cellunit_get_from_dir(bob37_root_cell_dir).get_planevents_quota_ledger() == {}
    )

    # WHEN
    create_cell_tree(belief_mstr_dir, a23_str, bob_str, tp37)

    # THEN
    bob37_root_cell = cellunit_get_from_dir(bob37_root_cell_dir)
    generated_bob37_quota_ledger = bob37_root_cell.get_planevents_quota_ledger()
    assert generated_bob37_quota_ledger == {"Bob": 225, yao_str: 225}


def test_create_cell_tree_Scenaro2_LedgerDepth1(env_dir_setup_cleanup):
    # ESTABLISH
    belief_mstr_dir = create_path(get_module_temp_dir(), "Fay_mstr")
    a23_str = "amy23"
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    tp37 = 37  # timepoint
    x_quota = 450
    x_celldepth = 1
    event56 = 56
    x_cell = cellunit_shop(bob_str, [], event56, x_celldepth, quota=x_quota)
    bob37_dir = cell_dir(belief_mstr_dir, a23_str, bob_str, tp37, [])
    cellunit_save_to_dir(bob37_dir, x_cell)
    bob_accts = [[yao_str], [bob_str], [zia_str]]
    yao_accts = [[zia_str]]
    zia_accts = [[bob_str], [yao_str]]
    bob_e56_path = save_planevent(belief_mstr_dir, a23_str, bob_str, event56, bob_accts)
    yao_e56_path = save_planevent(belief_mstr_dir, a23_str, yao_str, event56, yao_accts)
    zia_e56_path = save_planevent(belief_mstr_dir, a23_str, zia_str, event56, zia_accts)
    assert os_path_exists(bob_e56_path)
    assert os_path_exists(yao_e56_path)
    assert os_path_exists(zia_e56_path)
    bob37_node_path = node_path(belief_mstr_dir, a23_str, bob_str, tp37, [])
    bob37_bob_node_path = node_path(belief_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    bob37_yao_node_path = node_path(belief_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    bob37_zia_node_path = node_path(belief_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path) is False
    assert os_path_exists(bob37_yao_node_path) is False
    assert os_path_exists(bob37_zia_node_path) is False
    assert cellunit_get_from_dir(bob37_dir).get_planevents_quota_ledger() == {}

    # WHEN
    create_cell_tree(belief_mstr_dir, a23_str, bob_str, tp37)

    # THEN
    print(f"{bob37_bob_node_path=}")
    print(f"{bob37_yao_node_path=}")
    print(f"{bob37_zia_node_path=}")
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path)
    assert os_path_exists(bob37_yao_node_path)
    assert os_path_exists(bob37_zia_node_path)
    bob37_bob_dir = cell_dir(belief_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    bob37_yao_dir = cell_dir(belief_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    bob37_zia_dir = cell_dir(belief_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    bob37_cell = cellunit_get_from_dir(bob37_dir)
    bob37_bob_cell = cellunit_get_from_dir(bob37_bob_dir)
    bob37_yao_cell = cellunit_get_from_dir(bob37_yao_dir)
    bob37_zia_cell = cellunit_get_from_dir(bob37_zia_dir)
    assert bob37_cell.ancestors == []
    assert bob37_cell.event_int == 56
    assert bob37_cell.celldepth == 1
    assert bob37_cell.bud_owner_name == bob_str
    assert bob37_cell.penny == 1
    assert bob37_cell.quota == 450
    assert bob37_bob_cell.ancestors == [bob_str]
    assert bob37_bob_cell.event_int == 56
    assert bob37_bob_cell.celldepth == 0
    assert bob37_bob_cell.bud_owner_name == bob_str
    assert bob37_bob_cell.penny == 1
    assert bob37_bob_cell.quota == 150
    assert bob37_yao_cell.ancestors == [yao_str]
    assert bob37_yao_cell.event_int == 56
    assert bob37_yao_cell.celldepth == 0
    assert bob37_yao_cell.bud_owner_name == bob_str
    assert bob37_yao_cell.penny == 1
    assert bob37_yao_cell.quota == 150
    assert bob37_zia_cell.ancestors == [zia_str]
    assert bob37_zia_cell.event_int == 56
    assert bob37_zia_cell.celldepth == 0
    assert bob37_zia_cell.bud_owner_name == bob_str
    assert bob37_zia_cell.penny == 1
    assert bob37_zia_cell.quota == 150
    gen_bob37_quota_ledger = bob37_cell.get_planevents_quota_ledger()
    gen_bob37_bob_quota_ledger = bob37_bob_cell.get_planevents_quota_ledger()
    gen_bob37_yao_quota_ledger = bob37_yao_cell.get_planevents_quota_ledger()
    gen_bob37_zia_quota_ledger = bob37_zia_cell.get_planevents_quota_ledger()
    assert gen_bob37_quota_ledger == {bob_str: 150, yao_str: 150, zia_str: 150}
    assert gen_bob37_bob_quota_ledger == {bob_str: 50, yao_str: 50, zia_str: 50}
    assert gen_bob37_yao_quota_ledger == {zia_str: 150}
    assert gen_bob37_zia_quota_ledger == {bob_str: 75, yao_str: 75}


def test_create_cell_tree_Scenaro3_LedgerDepth1_MostRecentEvent(env_dir_setup_cleanup):
    # ESTABLISH
    belief_mstr_dir = create_path(get_module_temp_dir(), "Fay_mstr")
    a23_str = "amy23"
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    tp37 = 37  # timepoint
    x_quota = 450
    x_celldepth = 1
    event33 = 33
    event44 = 44
    event55 = 55
    x_cell = cellunit_shop(bob_str, [], event55, x_celldepth, quota=x_quota)
    bob37_dir = cell_dir(belief_mstr_dir, a23_str, bob_str, tp37, [])
    cellunit_save_to_dir(bob37_dir, x_cell)
    bob_accts = [[yao_str], [bob_str], [zia_str]]
    yao_accts = [[zia_str]]
    zia_accts = [[bob_str], [yao_str]]
    bob_e55_path = save_planevent(belief_mstr_dir, a23_str, bob_str, event55, bob_accts)
    yao_e44_path = save_planevent(belief_mstr_dir, a23_str, yao_str, event44, yao_accts)
    yao_e33_path = save_planevent(belief_mstr_dir, a23_str, yao_str, event33, yao_accts)
    zia_e33_path = save_planevent(belief_mstr_dir, a23_str, zia_str, event33, zia_accts)
    assert os_path_exists(bob_e55_path)
    assert os_path_exists(yao_e44_path)
    assert os_path_exists(zia_e33_path)
    bob37_node_path = node_path(belief_mstr_dir, a23_str, bob_str, tp37, [])
    bob37_bob_node_path = node_path(belief_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    bob37_yao_node_path = node_path(belief_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    bob37_zia_node_path = node_path(belief_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path) is False
    assert os_path_exists(bob37_yao_node_path) is False
    assert os_path_exists(bob37_zia_node_path) is False

    # WHEN
    create_cell_tree(belief_mstr_dir, a23_str, bob_str, tp37)

    # THEN
    print(f"{bob37_bob_node_path=}")
    print(f"{bob37_yao_node_path=}")
    print(f"{bob37_zia_node_path=}")
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path)
    assert os_path_exists(bob37_yao_node_path)
    assert os_path_exists(bob37_zia_node_path)
    bob37_bob_dir = cell_dir(belief_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    bob37_yao_dir = cell_dir(belief_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    bob37_zia_dir = cell_dir(belief_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    bob37_cell = cellunit_get_from_dir(bob37_dir)
    bob37_bob_cell = cellunit_get_from_dir(bob37_bob_dir)
    bob37_yao_cell = cellunit_get_from_dir(bob37_yao_dir)
    bob37_zia_cell = cellunit_get_from_dir(bob37_zia_dir)
    assert bob37_cell.ancestors == []
    assert bob37_cell.event_int == 55
    assert bob37_cell.celldepth == 1
    assert bob37_cell.bud_owner_name == bob_str
    assert bob37_cell.penny == 1
    assert bob37_cell.quota == 450
    assert bob37_bob_cell.ancestors == [bob_str]
    assert bob37_bob_cell.event_int == 55
    assert bob37_bob_cell.celldepth == 0
    assert bob37_bob_cell.bud_owner_name == bob_str
    assert bob37_bob_cell.penny == 1
    assert bob37_bob_cell.quota == 150
    assert bob37_yao_cell.ancestors == [yao_str]
    assert bob37_yao_cell.event_int == 44
    assert bob37_yao_cell.celldepth == 0
    assert bob37_yao_cell.bud_owner_name == bob_str
    assert bob37_yao_cell.penny == 1
    assert bob37_yao_cell.quota == 150
    assert bob37_zia_cell.ancestors == [zia_str]
    assert bob37_zia_cell.event_int == 33
    assert bob37_zia_cell.celldepth == 0
    assert bob37_zia_cell.bud_owner_name == bob_str
    assert bob37_zia_cell.penny == 1
    assert bob37_zia_cell.quota == 150
    gen_bob37_quota_ledger = bob37_cell.get_planevents_quota_ledger()
    gen_bob37_bob_quota_ledger = bob37_bob_cell.get_planevents_quota_ledger()
    gen_bob37_yao_quota_ledger = bob37_yao_cell.get_planevents_quota_ledger()
    gen_bob37_zia_quota_ledger = bob37_zia_cell.get_planevents_quota_ledger()
    assert gen_bob37_quota_ledger == {bob_str: 150, yao_str: 150, zia_str: 150}
    assert gen_bob37_bob_quota_ledger == {bob_str: 50, yao_str: 50, zia_str: 50}
    assert gen_bob37_yao_quota_ledger == {zia_str: 150}
    assert gen_bob37_zia_quota_ledger == {bob_str: 75, yao_str: 75}


def test_create_cell_tree_Scenaro4_LedgerDepth1_OneOwnerHasNoPast_planevent(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = create_path(get_module_temp_dir(), "Fay_mstr")
    a23_str = "amy23"
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    tp37 = 37  # timepoint
    x_quota = 450
    x_celldepth = 1
    event33 = 33
    event44 = 44
    event55 = 55
    event66 = 66
    x_cell = cellunit_shop(bob_str, [], event55, x_celldepth, quota=x_quota)
    bob37_dir = cell_dir(belief_mstr_dir, a23_str, bob_str, tp37, [])
    cellunit_save_to_dir(bob37_dir, x_cell)
    bob_accts = [[yao_str], [bob_str], [zia_str]]
    yao_accts = [[zia_str]]
    zia_accts = [[bob_str], [yao_str]]
    bob_e55_path = save_planevent(belief_mstr_dir, a23_str, bob_str, event55, bob_accts)
    yao_e44_path = save_planevent(belief_mstr_dir, a23_str, yao_str, event44, yao_accts)
    yao_e33_path = save_planevent(belief_mstr_dir, a23_str, yao_str, event33, yao_accts)
    zia_e66_path = save_planevent(belief_mstr_dir, a23_str, zia_str, event66, zia_accts)
    assert os_path_exists(bob_e55_path)
    assert os_path_exists(yao_e44_path)
    assert os_path_exists(zia_e66_path)
    bob37_dir = cell_dir(belief_mstr_dir, a23_str, bob_str, tp37, [])
    bob37_node_path = node_path(belief_mstr_dir, a23_str, bob_str, tp37, [])
    bob37_bob_node_path = node_path(belief_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    bob37_yao_node_path = node_path(belief_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    bob37_zia_node_path = node_path(belief_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path) is False
    assert os_path_exists(bob37_yao_node_path) is False
    assert os_path_exists(bob37_zia_node_path) is False

    # WHEN
    create_cell_tree(belief_mstr_dir, a23_str, bob_str, tp37)

    # THEN
    print(f"{bob37_bob_node_path=}")
    print(f"{bob37_yao_node_path=}")
    print(f"{bob37_zia_node_path=}")
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path)
    assert os_path_exists(bob37_yao_node_path)
    assert os_path_exists(bob37_zia_node_path) is False
    bob37_bob_dir = cell_dir(belief_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    bob37_yao_dir = cell_dir(belief_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    bob37_cell = cellunit_get_from_dir(bob37_dir)
    bob37_bob_cell = cellunit_get_from_dir(bob37_bob_dir)
    bob37_yao_cell = cellunit_get_from_dir(bob37_yao_dir)
    assert bob37_bob_cell.ancestors == [bob_str]
    assert bob37_bob_cell.event_int == 55
    assert bob37_bob_cell.celldepth == 0
    assert bob37_bob_cell.bud_owner_name == bob_str
    assert bob37_bob_cell.penny == 1
    assert bob37_bob_cell.quota == 150
    assert bob37_yao_cell.ancestors == [yao_str]
    assert bob37_yao_cell.event_int == 44
    assert bob37_yao_cell.celldepth == 0
    assert bob37_yao_cell.bud_owner_name == bob_str
    assert bob37_yao_cell.penny == 1
    assert bob37_yao_cell.quota == 150
    gen_bob37_quota_ledger = bob37_cell.get_planevents_quota_ledger()
    gen_bob37_bob_quota_ledger = bob37_bob_cell.get_planevents_quota_ledger()
    gen_bob37_yao_quota_ledger = bob37_yao_cell.get_planevents_quota_ledger()
    assert gen_bob37_quota_ledger == {bob_str: 150, yao_str: 150, zia_str: 150}
    assert gen_bob37_bob_quota_ledger == {bob_str: 50, yao_str: 50, zia_str: 50}
    assert gen_bob37_yao_quota_ledger == {zia_str: 150}


def test_create_cell_tree_Scenaro5_LedgerDepth1_ZeroQuotaDoesNotGetCreated(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = create_path(get_module_temp_dir(), "Fay_mstr")
    a23_str = "amy23"
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    tp37 = 37  # timepoint
    x_quota = 2
    x_celldepth = 1
    event33 = 33
    event44 = 44
    event55 = 55
    x_cell = cellunit_shop(bob_str, [], event55, x_celldepth, quota=x_quota)
    bob37_dir = cell_dir(belief_mstr_dir, a23_str, bob_str, tp37, [])
    cellunit_save_to_dir(bob37_dir, x_cell)
    bob_accts = [[yao_str], [bob_str], [zia_str]]
    yao_accts = [[zia_str]]
    zia_accts = [[bob_str], [yao_str]]
    bob_e55_path = save_planevent(belief_mstr_dir, a23_str, bob_str, event55, bob_accts)
    yao_e44_path = save_planevent(belief_mstr_dir, a23_str, yao_str, event44, yao_accts)
    yao_e33_path = save_planevent(belief_mstr_dir, a23_str, yao_str, event33, yao_accts)
    zia_e33_path = save_planevent(belief_mstr_dir, a23_str, zia_str, event33, zia_accts)
    assert os_path_exists(bob_e55_path)
    assert os_path_exists(yao_e44_path)
    assert os_path_exists(zia_e33_path)
    bob37_dir = cell_dir(belief_mstr_dir, a23_str, bob_str, tp37, [])
    bob37_node_path = node_path(belief_mstr_dir, a23_str, bob_str, tp37, [])
    bob37_bob_node_path = node_path(belief_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    bob37_yao_node_path = node_path(belief_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    bob37_zia_node_path = node_path(belief_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path) is False
    assert os_path_exists(bob37_yao_node_path) is False
    assert os_path_exists(bob37_zia_node_path) is False

    # WHEN
    create_cell_tree(belief_mstr_dir, a23_str, bob_str, tp37)

    # THEN
    print(f"{bob37_bob_node_path=}")
    print(f"{bob37_yao_node_path=}")
    print(f"{bob37_zia_node_path=}")
    assert os_path_exists(bob37_node_path)
    assert os_path_exists(bob37_bob_node_path) is False
    assert os_path_exists(bob37_yao_node_path)
    assert os_path_exists(bob37_zia_node_path)
    bob37_bob_dir = cell_dir(belief_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    bob37_yao_dir = cell_dir(belief_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    bob37_zia_dir = cell_dir(belief_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    bob37_cell = cellunit_get_from_dir(bob37_dir)
    bob37_yao_cell = cellunit_get_from_dir(bob37_yao_dir)
    bob37_zia_cell = cellunit_get_from_dir(bob37_zia_dir)
    gen_bob37_quota_ledger = bob37_cell.get_planevents_quota_ledger()
    gen_bob37_yao_quota_ledger = bob37_yao_cell.get_planevents_quota_ledger()
    gen_bob37_zia_quota_ledger = bob37_zia_cell.get_planevents_quota_ledger()
    assert gen_bob37_quota_ledger == {bob_str: 0, yao_str: 1, zia_str: 1}
    assert gen_bob37_yao_quota_ledger == {zia_str: 1}
    assert gen_bob37_zia_quota_ledger == {bob_str: 1, yao_str: 0}
