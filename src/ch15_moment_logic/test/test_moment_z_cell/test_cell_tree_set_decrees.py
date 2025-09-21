from src.a06_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.ch11_bud_logic.cell import cellunit_shop
from src.ch12_hub_toolbox.ch12_path import (
    create_beliefevent_path,
    create_cell_dir_path as cell_dir,
)
from src.ch12_hub_toolbox.hub_tool import (
    cellunit_get_from_dir,
    cellunit_save_to_dir,
    save_belief_file,
)
from src.ch15_moment_logic.moment_cell import DecreeUnit, set_cell_trees_decrees
from src.ch15_moment_logic.test._util.ch15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.ch15_moment_logic.test._util.example_moments import (
    example_casa_clean_factunit,
    example_casa_dirty_factunit,
    get_bob_mop_with_reason_beliefunit_example,
    get_bob_mop_without_reason_beliefunit_example,
)


def test_DecreeUnit_Exists():
    # ESTABLISH / WHEN
    x_decreeunit = DecreeUnit()
    # THEN
    assert not x_decreeunit.parent_cell_dir
    assert not x_decreeunit.cell_dir
    assert not x_decreeunit.cell_ancestors
    assert not x_decreeunit.cell_mandate
    assert not x_decreeunit.cell_celldepth
    assert not x_decreeunit.root_cell_bool
    assert not x_decreeunit.cell_belief_name
    assert not x_decreeunit.event_int


def test_DecreeUnit_get_child_cell_ancestors_ReturnsObj_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    x_decreeunit = DecreeUnit(cell_ancestors=[yao_str])

    # WHEN
    child_cell_ancestors = x_decreeunit.get_child_cell_ancestors(bob_str)

    # THEN
    assert child_cell_ancestors == [yao_str, bob_str]
    assert x_decreeunit.cell_ancestors != [yao_str, bob_str]
    assert x_decreeunit.cell_ancestors != child_cell_ancestors


# create a world with, cell.json, found facts and belief events
# for every found_fact change beliefevent to that fact
# create agenda (different than if found_fact was not applied)
def test_set_cell_trees_decrees_SetsRootAttr_Scenario0_Depth0NoFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy"
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
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}

    # WHEN
    set_cell_trees_decrees(mstr_dir, a23_str)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}


def test_set_cell_trees_decrees_SetsRootAttr_Scenario1_Depth0AndOne_beliefevent_fact(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy"
    tp5 = 5
    bob_str = "Bob"
    das = []
    event7 = 7
    bob_beliefadjust = get_bob_mop_with_reason_beliefunit_example()
    # create cell file
    clean_fact = example_casa_clean_factunit()
    clean_facts = {clean_fact.fact_context: clean_fact}
    bob_cell = cellunit_shop(
        bob_str,
        [],
        event7,
        0,
        beliefadjust=bob_beliefadjust,
        beliefevent_facts=clean_facts,
    )
    bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, [])
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}

    # WHEN
    set_cell_trees_decrees(mstr_dir, a23_str)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == clean_facts


def test_set_cell_trees_decrees_SetsRootAttr_Scenario2_Depth0AndOne_found_fact(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy"
    tp5 = 5
    bob_str = "Bob"
    das = []
    event7 = 7
    bob_beliefadjust = get_bob_mop_with_reason_beliefunit_example()
    # create cell file
    clean_fact = example_casa_clean_factunit()
    clean_facts = {clean_fact.fact_context: clean_fact}
    bob_cell = cellunit_shop(
        bob_str,
        [],
        event7,
        celldepth=0,
        beliefadjust=bob_beliefadjust,
        found_facts=clean_facts,
    )
    bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, [])
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}

    # WHEN
    set_cell_trees_decrees(mstr_dir, a23_str)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == clean_facts


def test_set_cell_trees_decrees_SetsChildCells_Scenario3_Depth1AndZero_boss_facts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    tp5 = 5
    bob_str = "Bob"
    sue_str = "Sue"
    bob_ancs = []
    bob_sue_ancs = [sue_str]
    e7 = 7
    bob_beliefadjust = get_bob_mop_without_reason_beliefunit_example()
    bob_beliefadjust.add_voiceunit(sue_str, 1)
    bob_sue_beliefadjust = beliefunit_shop(sue_str, a23_str)
    # create cell file
    bob_cell = cellunit_shop(
        bob_str, bob_ancs, event_int=e7, celldepth=2, beliefadjust=bob_beliefadjust
    )
    bob_sue_cell = cellunit_shop(
        bob_str,
        bob_sue_ancs,
        event_int=e7,
        celldepth=0,
        beliefadjust=bob_sue_beliefadjust,
    )
    bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_ancs)
    bob_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_sue_ancs)
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_sue_dir, bob_sue_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}

    # WHEN
    set_cell_trees_decrees(mstr_dir, a23_str)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}


def test_set_cell_trees_decrees_SetsChildCells_Scenario3_Depth1And_boss_facts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    tp5 = 5
    bob_str = "Bob"
    sue_str = "Sue"
    bob_ancs = []
    bob_sue_ancs = [sue_str]
    e7 = 7
    bob_beliefadjust = get_bob_mop_with_reason_beliefunit_example()
    bob_beliefadjust.add_voiceunit(sue_str, 1)
    bob_sue_beliefadjust = get_bob_mop_with_reason_beliefunit_example()
    bob_sue_beliefadjust.set_belief_name(sue_str)
    # create cell file
    dirty_fact = example_casa_dirty_factunit()
    dirty_facts = {dirty_fact.fact_context: dirty_fact}
    bob_cell = cellunit_shop(
        bob_str,
        bob_ancs,
        event_int=e7,
        celldepth=2,
        beliefadjust=bob_beliefadjust,
        beliefevent_facts=dirty_facts,
    )
    bob_sue_cell = cellunit_shop(
        bob_str,
        bob_sue_ancs,
        event_int=e7,
        celldepth=0,
        beliefadjust=bob_sue_beliefadjust,
    )
    bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_ancs)
    bob_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_sue_ancs)
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_sue_dir, bob_sue_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}

    # WHEN
    set_cell_trees_decrees(mstr_dir, a23_str)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == dirty_facts


def test_set_cell_trees_decrees_SetsChildCells_Scenario4_Depth3And_boss_facts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    tp5 = 5
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    bob_ancs = []
    b_sue_ancs = [sue_str]
    bs_yao_ancs = [sue_str, yao_str]
    bsy_zia_ancs = [sue_str, yao_str, zia_str]
    e7 = 7
    bob_beliefadjust = get_bob_mop_with_reason_beliefunit_example()
    bob_beliefadjust.add_voiceunit(sue_str, 1)
    b_sue_ba = get_bob_mop_with_reason_beliefunit_example()
    b_sue_ba.set_belief_name(sue_str)
    b_sue_ba.add_voiceunit(yao_str, 1)
    bs_yao_ba = get_bob_mop_with_reason_beliefunit_example()
    bs_yao_ba.set_belief_name(yao_str)
    bs_yao_ba.add_voiceunit(zia_str, 1)
    bsy_zia_ba = get_bob_mop_with_reason_beliefunit_example()
    bsy_zia_ba.set_belief_name(zia_str)
    # create cell file
    dirty_fact = example_casa_dirty_factunit()
    dirty_facts = {dirty_fact.fact_context: dirty_fact}
    bob_cell = cellunit_shop(
        bob_str,
        bob_ancs,
        event_int=e7,
        celldepth=4,
        beliefadjust=bob_beliefadjust,
        beliefevent_facts=dirty_facts,
    )
    b_sue_cell = cellunit_shop(bob_str, b_sue_ancs, e7, 0, beliefadjust=b_sue_ba)
    bs_yao_cell = cellunit_shop(bob_str, bs_yao_ancs, e7, 0, beliefadjust=bs_yao_ba)
    bsy_zia_cell = cellunit_shop(bob_str, bsy_zia_ancs, e7, 0, beliefadjust=bsy_zia_ba)
    bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_ancs)
    bob_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, b_sue_ancs)
    bob_sue_yao_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bs_yao_ancs)
    bob_sue_yao_zia_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bsy_zia_ancs)
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_sue_dir, b_sue_cell)
    cellunit_save_to_dir(bob_sue_yao_dir, bs_yao_cell)
    cellunit_save_to_dir(bob_sue_yao_zia_dir, bsy_zia_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == {}

    # WHEN
    set_cell_trees_decrees(mstr_dir, a23_str)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == dirty_facts


def test_set_cell_trees_decrees_SetsChildCells_Scenario5_Depth2And_boss_facts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    tp5 = 5
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    bob_ancs = []
    b_sue_ancs = [sue_str]
    bs_yao_ancs = [sue_str, yao_str]
    bsy_zia_ancs = [sue_str, yao_str, zia_str]
    e7 = 7
    bob_beliefadjust = get_bob_mop_with_reason_beliefunit_example()
    bob_beliefadjust.add_voiceunit(sue_str, 1)
    b_sue_ba = get_bob_mop_with_reason_beliefunit_example()
    b_sue_ba.set_belief_name(sue_str)
    b_sue_ba.add_voiceunit(yao_str, 1)
    bs_yao_ba = get_bob_mop_with_reason_beliefunit_example()
    bs_yao_ba.set_belief_name(yao_str)
    bs_yao_ba.add_voiceunit(zia_str, 1)
    bsy_zia_ba = get_bob_mop_with_reason_beliefunit_example()
    bsy_zia_ba.set_belief_name(zia_str)
    # create cell file
    dirty_fact = example_casa_dirty_factunit()
    dirty_facts = {dirty_fact.fact_context: dirty_fact}
    bob_cell = cellunit_shop(
        bob_str,
        bob_ancs,
        event_int=e7,
        celldepth=2,
        beliefadjust=bob_beliefadjust,
        beliefevent_facts=dirty_facts,
    )
    b_sue_cell = cellunit_shop(bob_str, b_sue_ancs, e7, 0, beliefadjust=b_sue_ba)
    bs_yao_cell = cellunit_shop(bob_str, bs_yao_ancs, e7, 0, beliefadjust=bs_yao_ba)
    bsy_zia_cell = cellunit_shop(bob_str, bsy_zia_ancs, e7, 0, beliefadjust=bsy_zia_ba)
    bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_ancs)
    bob_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, b_sue_ancs)
    bob_sue_yao_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bs_yao_ancs)
    bob_sue_yao_zia_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bsy_zia_ancs)
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_sue_dir, b_sue_cell)
    cellunit_save_to_dir(bob_sue_yao_dir, bs_yao_cell)
    cellunit_save_to_dir(bob_sue_yao_zia_dir, bsy_zia_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == {}

    # WHEN
    set_cell_trees_decrees(mstr_dir, a23_str)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == {}


def test_set_cell_trees_decrees_SetsChildCells_Scenario6_boss_facts_ResetAtEachCell(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    tp5 = 5
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    bob_ancs = []
    b_sue_ancs = [sue_str]
    bs_yao_ancs = [sue_str, yao_str]
    bsy_zia_ancs = [sue_str, yao_str, zia_str]
    e7 = 7
    bob_beliefadjust = get_bob_mop_with_reason_beliefunit_example()
    bob_beliefadjust.add_voiceunit(sue_str, 1)
    b_sue_ba = beliefunit_shop(sue_str, a23_str)
    b_sue_ba.set_belief_name(sue_str)
    b_sue_ba.add_voiceunit(yao_str, 1)
    bs_yao_ba = get_bob_mop_with_reason_beliefunit_example()
    bs_yao_ba.set_belief_name(yao_str)
    bs_yao_ba.add_voiceunit(zia_str, 1)
    clean_fact = example_casa_clean_factunit()
    bs_yao_ba.add_fact(clean_fact.fact_context, clean_fact.fact_state)
    bsy_zia_ba = get_bob_mop_with_reason_beliefunit_example()
    bsy_zia_ba.set_belief_name(zia_str)
    # create cell file
    dirty_fact = example_casa_dirty_factunit()
    dirty_facts = {dirty_fact.fact_context: dirty_fact}
    bob_cell = cellunit_shop(
        bob_str,
        bob_ancs,
        event_int=e7,
        celldepth=3,
        beliefadjust=bob_beliefadjust,
        beliefevent_facts=dirty_facts,
    )
    b_sue_cell = cellunit_shop(bob_str, b_sue_ancs, e7, 0, beliefadjust=b_sue_ba)
    bs_yao_cell = cellunit_shop(bob_str, bs_yao_ancs, e7, 0)
    bs_yao_cell.eval_beliefevent(bs_yao_ba)
    bsy_zia_cell = cellunit_shop(bob_str, bsy_zia_ancs, e7, 0, beliefadjust=bsy_zia_ba)
    bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_ancs)
    bob_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, b_sue_ancs)
    bob_sue_yao_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bs_yao_ancs)
    bob_sue_yao_zia_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bsy_zia_ancs)
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_sue_dir, b_sue_cell)
    cellunit_save_to_dir(bob_sue_yao_dir, bs_yao_cell)
    cellunit_save_to_dir(bob_sue_yao_zia_dir, bsy_zia_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == {}

    # WHEN
    set_cell_trees_decrees(mstr_dir, a23_str)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}
    clean_facts = {clean_fact.fact_context: clean_fact}
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == clean_facts
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == clean_facts


def test_set_cell_trees_decrees_SetsChildCells_Scenario7_NoCell_GetBeliefEvent(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    tp5 = 5
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    bob_ancs = []
    b_sue_ancs = [sue_str]
    bs_yao_ancs = [sue_str, yao_str]
    bsy_zia_ancs = [sue_str, yao_str, zia_str]
    e7 = 7
    bob_beliefadjust = get_bob_mop_with_reason_beliefunit_example()
    bob_beliefadjust.add_voiceunit(sue_str, 1)
    b_sue_ba = get_bob_mop_with_reason_beliefunit_example()
    b_sue_ba.set_belief_name(sue_str)
    b_sue_ba.add_voiceunit(yao_str, 1)
    bs_yao_ba = get_bob_mop_with_reason_beliefunit_example()
    bs_yao_ba.set_belief_name(yao_str)
    bs_yao_ba.add_voiceunit(zia_str, 1)
    bsy_zia_ba = get_bob_mop_with_reason_beliefunit_example()
    bsy_zia_ba.set_belief_name(zia_str)
    # create cell file
    dirty_fact = example_casa_dirty_factunit()
    dirty_facts = {dirty_fact.fact_context: dirty_fact}
    bob_cell = cellunit_shop(
        bob_str,
        bob_ancs,
        event_int=e7,
        celldepth=4,
        beliefadjust=bob_beliefadjust,
        beliefevent_facts=dirty_facts,
    )
    b_sue_cell = cellunit_shop(bob_str, b_sue_ancs, e7, 0, beliefadjust=b_sue_ba)
    # bs_yao_cell = cellunit_shop(bob_str, bs_yao_ancs, e7, 0, beliefadjust=bs_yao_ba)
    bsy_zia_cell = cellunit_shop(bob_str, bsy_zia_ancs, e7, 0, beliefadjust=bsy_zia_ba)
    bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_ancs)
    bob_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, b_sue_ancs)
    bob_sue_yao_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bs_yao_ancs)
    bob_sue_yao_zia_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bsy_zia_ancs)
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_sue_dir, b_sue_cell)
    beliefevent_path = create_beliefevent_path(mstr_dir, a23_str, yao_str, e7)
    save_belief_file(beliefevent_path, None, bs_yao_ba)
    # cellunit_save_to_dir(bob_sue_yao_dir, bs_yao_cell)
    cellunit_save_to_dir(bob_sue_yao_zia_dir, bsy_zia_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}
    assert not cellunit_get_from_dir(bob_sue_yao_dir)
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == {}

    # WHEN
    set_cell_trees_decrees(mstr_dir, a23_str)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == dirty_facts
