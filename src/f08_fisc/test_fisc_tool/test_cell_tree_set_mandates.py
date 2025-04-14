from src.f00_data_toolboxs.file_toolbox import open_json
from src.f02_bud.bud import budunit_shop, BudUnit
from src.f06_listen.cell import cellunit_shop
from src.f06_listen.hub_path import (
    create_budevent_path,
    create_cell_dir_path as cell_dir,
    create_cell_acct_mandate_ledger_path as mandate_path,
)
from src.f06_listen.hub_tool import (
    cellunit_save_to_dir,
    cellunit_get_from_dir,
    save_bud_file,
)
from src.f08_fisc.fisc_tool import set_cell_tree_cell_mandates
from src.f08_fisc.examples.example_fiscs import (
    example_casa_clean_factunit,
    example_casa_dirty_factunit,
    get_bob_mop_with_reason_budunit_example,
)
from src.f08_fisc.examples.fisc_env import env_dir_setup_cleanup, get_test_fisc_mstr_dir
from os.path import exists as os_path_exists


def test_set_cell_tree_cell_mandates_SetsRootAttr_Scenario0_Depth0NoFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_test_fisc_mstr_dir()
    a23_str = "accord"
    tp5 = 5
    bob_str = "Bob"
    das = []
    event7 = 7
    # create cell file
    bob_cell = cellunit_shop(bob_str, [], event7, celldepth=0)
    bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, [])
    bob_bob_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, [bob_str])
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_bob_dir, bob_cell)
    bob_root_mandate_path = mandate_path(mstr_dir, a23_str, bob_str, tp5, [])
    bob_bob_mandate_path = mandate_path(mstr_dir, a23_str, bob_str, tp5, [bob_str])
    assert os_path_exists(bob_root_mandate_path) is False
    assert os_path_exists(bob_bob_mandate_path) is False

    # WHEN
    set_cell_tree_cell_mandates(mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob_root_mandate_path)
    assert os_path_exists(bob_bob_mandate_path)
    assert open_json(bob_root_mandate_path) == {bob_str: 1000}
    assert open_json(bob_bob_mandate_path) == {bob_str: 1000}


# def test_set_cell_tree_cell_mandates_SetsRootAttr_Scenario1_Depth0AndOne_budevent_fact(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     mstr_dir = get_test_fisc_mstr_dir()
#     a23_str = "accord"
#     tp5 = 5
#     bob_str = "Bob"
#     das = []
#     event7 = 7
#     bob_budadjust = get_bob_mop_with_reason_budunit_example()
#     # create cell file
#     clean_fact = example_casa_clean_factunit()
#     clean_facts = {clean_fact.base: clean_fact}
#     bob_cell = cellunit_shop(
#         bob_str, [], event7, 0, budadjust=bob_budadjust, budevent_facts=clean_facts
#     )
#     bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, [])
#     cellunit_save_to_dir(bob_root_dir, bob_cell)
#     assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}

#     # WHEN
#     set_cell_tree_cell_mandates(mstr_dir, a23_str)

#     # THEN
#     assert cellunit_get_from_dir(bob_root_dir).boss_facts == clean_facts


# def test_set_cell_tree_cell_mandates_SetsRootAttr_Scenario2_Depth0AndOne_found_fact(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     mstr_dir = get_test_fisc_mstr_dir()
#     a23_str = "accord"
#     tp5 = 5
#     bob_str = "Bob"
#     das = []
#     event7 = 7
#     bob_budadjust = get_bob_mop_with_reason_budunit_example()
#     # create cell file
#     clean_fact = example_casa_clean_factunit()
#     clean_facts = {clean_fact.base: clean_fact}
#     bob_cell = cellunit_shop(
#         bob_str,
#         [],
#         event7,
#         celldepth=0,
#         budadjust=bob_budadjust,
#         found_facts=clean_facts,
#     )
#     bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, [])
#     cellunit_save_to_dir(bob_root_dir, bob_cell)
#     assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}

#     # WHEN
#     set_cell_tree_cell_mandates(mstr_dir, a23_str)

#     # THEN
#     assert cellunit_get_from_dir(bob_root_dir).boss_facts == clean_facts


# def test_set_cell_tree_cell_mandates_SetsChildCells_Scenario3_Depth1AndZero_boss_facts(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     mstr_dir = get_test_fisc_mstr_dir()
#     a23_str = "accord23"
#     tp5 = 5
#     bob_str = "Bob"
#     sue_str = "Sue"
#     bob_ancs = []
#     bob_sue_ancs = [sue_str]
#     e7 = 7
#     bob_budadjust = get_bob_mop_without_reason_budunit_example()
#     bob_budadjust.add_acctunit(sue_str, 1)
#     bob_sue_budadjust = budunit_shop(sue_str, a23_str)
#     # create cell file
#     bob_cell = cellunit_shop(
#         bob_str, bob_ancs, event_int=e7, celldepth=2, budadjust=bob_budadjust
#     )
#     bob_sue_cell = cellunit_shop(
#         bob_str, bob_sue_ancs, event_int=e7, celldepth=0, budadjust=bob_sue_budadjust
#     )
#     bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_ancs)
#     bob_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_sue_ancs)
#     cellunit_save_to_dir(bob_root_dir, bob_cell)
#     cellunit_save_to_dir(bob_sue_dir, bob_sue_cell)
#     assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
#     assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}

#     # WHEN
#     set_cell_tree_cell_mandates(mstr_dir, a23_str)

#     # THEN
#     assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
#     assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}


# def test_set_cell_tree_cell_mandates_SetsChildCells_Scenario3_Depth1And_boss_facts(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     mstr_dir = get_test_fisc_mstr_dir()
#     a23_str = "accord23"
#     tp5 = 5
#     bob_str = "Bob"
#     sue_str = "Sue"
#     bob_ancs = []
#     bob_sue_ancs = [sue_str]
#     e7 = 7
#     bob_budadjust = get_bob_mop_with_reason_budunit_example()
#     bob_budadjust.add_acctunit(sue_str, 1)
#     bob_sue_budadjust = get_bob_mop_with_reason_budunit_example()
#     bob_sue_budadjust.set_owner_name(sue_str)
#     # create cell file
#     dirty_fact = example_casa_dirty_factunit()
#     dirty_facts = {dirty_fact.base: dirty_fact}
#     bob_cell = cellunit_shop(
#         bob_str,
#         bob_ancs,
#         event_int=e7,
#         celldepth=2,
#         budadjust=bob_budadjust,
#         budevent_facts=dirty_facts,
#     )
#     bob_sue_cell = cellunit_shop(
#         bob_str, bob_sue_ancs, event_int=e7, celldepth=0, budadjust=bob_sue_budadjust
#     )
#     bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_ancs)
#     bob_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_sue_ancs)
#     cellunit_save_to_dir(bob_root_dir, bob_cell)
#     cellunit_save_to_dir(bob_sue_dir, bob_sue_cell)
#     assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
#     assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}

#     # WHEN
#     set_cell_tree_cell_mandates(mstr_dir, a23_str)

#     # THEN
#     assert cellunit_get_from_dir(bob_root_dir).boss_facts == dirty_facts
#     assert cellunit_get_from_dir(bob_sue_dir).boss_facts == dirty_facts


# def test_set_cell_tree_cell_mandates_SetsChildCells_Scenario4_Depth3And_boss_facts(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     mstr_dir = get_test_fisc_mstr_dir()
#     a23_str = "accord23"
#     tp5 = 5
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     zia_str = "Zia"
#     bob_ancs = []
#     b_sue_ancs = [sue_str]
#     bs_yao_ancs = [sue_str, yao_str]
#     bsy_zia_ancs = [sue_str, yao_str, zia_str]
#     e7 = 7
#     bob_budadjust = get_bob_mop_with_reason_budunit_example()
#     bob_budadjust.add_acctunit(sue_str, 1)
#     b_sue_ba = get_bob_mop_with_reason_budunit_example()
#     b_sue_ba.set_owner_name(sue_str)
#     b_sue_ba.add_acctunit(yao_str, 1)
#     bs_yao_ba = get_bob_mop_with_reason_budunit_example()
#     bs_yao_ba.set_owner_name(yao_str)
#     bs_yao_ba.add_acctunit(zia_str, 1)
#     bsy_zia_ba = get_bob_mop_with_reason_budunit_example()
#     bsy_zia_ba.set_owner_name(zia_str)
#     # create cell file
#     dirty_fact = example_casa_dirty_factunit()
#     dirty_facts = {dirty_fact.base: dirty_fact}
#     bob_cell = cellunit_shop(
#         bob_str,
#         bob_ancs,
#         event_int=e7,
#         celldepth=4,
#         budadjust=bob_budadjust,
#         budevent_facts=dirty_facts,
#     )
#     b_sue_cell = cellunit_shop(bob_str, b_sue_ancs, e7, 0, budadjust=b_sue_ba)
#     bs_yao_cell = cellunit_shop(bob_str, bs_yao_ancs, e7, 0, budadjust=bs_yao_ba)
#     bsy_zia_cell = cellunit_shop(bob_str, bsy_zia_ancs, e7, 0, budadjust=bsy_zia_ba)
#     bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_ancs)
#     bob_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, b_sue_ancs)
#     bob_sue_yao_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bs_yao_ancs)
#     bob_sue_yao_zia_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bsy_zia_ancs)
#     cellunit_save_to_dir(bob_root_dir, bob_cell)
#     cellunit_save_to_dir(bob_sue_dir, b_sue_cell)
#     cellunit_save_to_dir(bob_sue_yao_dir, bs_yao_cell)
#     cellunit_save_to_dir(bob_sue_yao_zia_dir, bsy_zia_cell)
#     assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
#     assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}
#     assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == {}
#     assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == {}

#     # WHEN
#     set_cell_tree_cell_mandates(mstr_dir, a23_str)

#     # THEN
#     assert cellunit_get_from_dir(bob_root_dir).boss_facts == dirty_facts
#     assert cellunit_get_from_dir(bob_sue_dir).boss_facts == dirty_facts
#     assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == dirty_facts
#     assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == dirty_facts


# def test_set_cell_tree_cell_mandates_SetsChildCells_Scenario5_Depth2And_boss_facts(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     mstr_dir = get_test_fisc_mstr_dir()
#     a23_str = "accord23"
#     tp5 = 5
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     zia_str = "Zia"
#     bob_ancs = []
#     b_sue_ancs = [sue_str]
#     bs_yao_ancs = [sue_str, yao_str]
#     bsy_zia_ancs = [sue_str, yao_str, zia_str]
#     e7 = 7
#     bob_budadjust = get_bob_mop_with_reason_budunit_example()
#     bob_budadjust.add_acctunit(sue_str, 1)
#     b_sue_ba = get_bob_mop_with_reason_budunit_example()
#     b_sue_ba.set_owner_name(sue_str)
#     b_sue_ba.add_acctunit(yao_str, 1)
#     bs_yao_ba = get_bob_mop_with_reason_budunit_example()
#     bs_yao_ba.set_owner_name(yao_str)
#     bs_yao_ba.add_acctunit(zia_str, 1)
#     bsy_zia_ba = get_bob_mop_with_reason_budunit_example()
#     bsy_zia_ba.set_owner_name(zia_str)
#     # create cell file
#     dirty_fact = example_casa_dirty_factunit()
#     dirty_facts = {dirty_fact.base: dirty_fact}
#     bob_cell = cellunit_shop(
#         bob_str,
#         bob_ancs,
#         event_int=e7,
#         celldepth=2,
#         budadjust=bob_budadjust,
#         budevent_facts=dirty_facts,
#     )
#     b_sue_cell = cellunit_shop(bob_str, b_sue_ancs, e7, 0, budadjust=b_sue_ba)
#     bs_yao_cell = cellunit_shop(bob_str, bs_yao_ancs, e7, 0, budadjust=bs_yao_ba)
#     bsy_zia_cell = cellunit_shop(bob_str, bsy_zia_ancs, e7, 0, budadjust=bsy_zia_ba)
#     bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_ancs)
#     bob_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, b_sue_ancs)
#     bob_sue_yao_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bs_yao_ancs)
#     bob_sue_yao_zia_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bsy_zia_ancs)
#     cellunit_save_to_dir(bob_root_dir, bob_cell)
#     cellunit_save_to_dir(bob_sue_dir, b_sue_cell)
#     cellunit_save_to_dir(bob_sue_yao_dir, bs_yao_cell)
#     cellunit_save_to_dir(bob_sue_yao_zia_dir, bsy_zia_cell)
#     assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
#     assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}
#     assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == {}
#     assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == {}

#     # WHEN
#     set_cell_tree_cell_mandates(mstr_dir, a23_str)

#     # THEN
#     assert cellunit_get_from_dir(bob_root_dir).boss_facts == dirty_facts
#     assert cellunit_get_from_dir(bob_sue_dir).boss_facts == dirty_facts
#     assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == dirty_facts
#     assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == {}


# def test_set_cell_tree_cell_mandates_SetsChildCells_Scenario6_boss_facts_ResetAtEachCell(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     mstr_dir = get_test_fisc_mstr_dir()
#     a23_str = "accord23"
#     tp5 = 5
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     zia_str = "Zia"
#     bob_ancs = []
#     b_sue_ancs = [sue_str]
#     bs_yao_ancs = [sue_str, yao_str]
#     bsy_zia_ancs = [sue_str, yao_str, zia_str]
#     e7 = 7
#     bob_budadjust = get_bob_mop_with_reason_budunit_example()
#     bob_budadjust.add_acctunit(sue_str, 1)
#     b_sue_ba = budunit_shop(sue_str, a23_str)
#     b_sue_ba.set_owner_name(sue_str)
#     b_sue_ba.add_acctunit(yao_str, 1)
#     bs_yao_ba = get_bob_mop_with_reason_budunit_example()
#     bs_yao_ba.set_owner_name(yao_str)
#     bs_yao_ba.add_acctunit(zia_str, 1)
#     clean_fact = example_casa_clean_factunit()
#     bs_yao_ba.add_fact(clean_fact.base, clean_fact.pick)
#     bsy_zia_ba = get_bob_mop_with_reason_budunit_example()
#     bsy_zia_ba.set_owner_name(zia_str)
#     # create cell file
#     dirty_fact = example_casa_dirty_factunit()
#     dirty_facts = {dirty_fact.base: dirty_fact}
#     bob_cell = cellunit_shop(
#         bob_str,
#         bob_ancs,
#         event_int=e7,
#         celldepth=3,
#         budadjust=bob_budadjust,
#         budevent_facts=dirty_facts,
#     )
#     b_sue_cell = cellunit_shop(bob_str, b_sue_ancs, e7, 0, budadjust=b_sue_ba)
#     bs_yao_cell = cellunit_shop(bob_str, bs_yao_ancs, e7, 0)
#     bs_yao_cell.eval_budevent(bs_yao_ba)
#     bsy_zia_cell = cellunit_shop(bob_str, bsy_zia_ancs, e7, 0, budadjust=bsy_zia_ba)
#     bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_ancs)
#     bob_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, b_sue_ancs)
#     bob_sue_yao_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bs_yao_ancs)
#     bob_sue_yao_zia_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bsy_zia_ancs)
#     cellunit_save_to_dir(bob_root_dir, bob_cell)
#     cellunit_save_to_dir(bob_sue_dir, b_sue_cell)
#     cellunit_save_to_dir(bob_sue_yao_dir, bs_yao_cell)
#     cellunit_save_to_dir(bob_sue_yao_zia_dir, bsy_zia_cell)
#     assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
#     assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}
#     assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == {}
#     assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == {}

#     # WHEN
#     set_cell_tree_cell_mandates(mstr_dir, a23_str)

#     # THEN
#     assert cellunit_get_from_dir(bob_root_dir).boss_facts == dirty_facts
#     assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}
#     clean_facts = {clean_fact.base: clean_fact}
#     assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == clean_facts
#     assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == clean_facts


# def test_set_cell_tree_cell_mandates_SetsChildCells_Scenario7_NoCell_GetBudEvent(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     mstr_dir = get_test_fisc_mstr_dir()
#     a23_str = "accord23"
#     tp5 = 5
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     zia_str = "Zia"
#     bob_ancs = []
#     b_sue_ancs = [sue_str]
#     bs_yao_ancs = [sue_str, yao_str]
#     bsy_zia_ancs = [sue_str, yao_str, zia_str]
#     e7 = 7
#     bob_budadjust = get_bob_mop_with_reason_budunit_example()
#     bob_budadjust.add_acctunit(sue_str, 1)
#     b_sue_ba = get_bob_mop_with_reason_budunit_example()
#     b_sue_ba.set_owner_name(sue_str)
#     b_sue_ba.add_acctunit(yao_str, 1)
#     bs_yao_ba = get_bob_mop_with_reason_budunit_example()
#     bs_yao_ba.set_owner_name(yao_str)
#     bs_yao_ba.add_acctunit(zia_str, 1)
#     bsy_zia_ba = get_bob_mop_with_reason_budunit_example()
#     bsy_zia_ba.set_owner_name(zia_str)
#     # create cell file
#     dirty_fact = example_casa_dirty_factunit()
#     dirty_facts = {dirty_fact.base: dirty_fact}
#     bob_cell = cellunit_shop(
#         bob_str,
#         bob_ancs,
#         event_int=e7,
#         celldepth=4,
#         budadjust=bob_budadjust,
#         budevent_facts=dirty_facts,
#     )
#     b_sue_cell = cellunit_shop(bob_str, b_sue_ancs, e7, 0, budadjust=b_sue_ba)
#     # bs_yao_cell = cellunit_shop(bob_str, bs_yao_ancs, e7, 0, budadjust=bs_yao_ba)
#     bsy_zia_cell = cellunit_shop(bob_str, bsy_zia_ancs, e7, 0, budadjust=bsy_zia_ba)
#     bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_ancs)
#     bob_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, b_sue_ancs)
#     bob_sue_yao_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bs_yao_ancs)
#     bob_sue_yao_zia_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bsy_zia_ancs)
#     cellunit_save_to_dir(bob_root_dir, bob_cell)
#     cellunit_save_to_dir(bob_sue_dir, b_sue_cell)
#     budevent_path = create_budevent_path(mstr_dir, a23_str, yao_str, e7)
#     save_bud_file(budevent_path, None, bs_yao_ba)
#     # cellunit_save_to_dir(bob_sue_yao_dir, bs_yao_cell)
#     cellunit_save_to_dir(bob_sue_yao_zia_dir, bsy_zia_cell)
#     assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
#     assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}
#     assert not cellunit_get_from_dir(bob_sue_yao_dir)
#     assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == {}

#     # WHEN
#     set_cell_tree_cell_mandates(mstr_dir, a23_str)

#     # THEN
#     assert cellunit_get_from_dir(bob_root_dir).boss_facts == dirty_facts
#     assert cellunit_get_from_dir(bob_sue_dir).boss_facts == dirty_facts
#     assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == dirty_facts
#     assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == dirty_facts
