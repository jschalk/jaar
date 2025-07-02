from src.a06_believer_logic.believer import BelieverUnit, believerunit_shop
from src.a11_bud_logic.cell import cellunit_shop
from src.a12_hub_toolbox.hub_path import (
    create_believerevent_path,
    create_cell_dir_path as cell_dir,
)
from src.a12_hub_toolbox.hub_tool import (
    cellunit_get_from_dir,
    cellunit_save_to_dir,
    save_believer_file,
)
from src.a15_belief_logic.belief_cell import DecreeUnit, set_cell_trees_decrees
from src.a15_belief_logic.test._util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a15_belief_logic.test._util.example_beliefs import (
    example_casa_clean_factunit,
    example_casa_dirty_factunit,
    get_bob_mop_with_reason_believerunit_example,
    get_bob_mop_without_reason_believerunit_example,
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
    assert not x_decreeunit.cell_believer_name
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


# create a world with, cell.json, found facts and believer events
# for every found_fact change believerevent to that fact
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


def test_set_cell_trees_decrees_SetsRootAttr_Scenario1_Depth0AndOne_believerevent_fact(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy"
    tp5 = 5
    bob_str = "Bob"
    das = []
    event7 = 7
    bob_believeradjust = get_bob_mop_with_reason_believerunit_example()
    # create cell file
    clean_fact = example_casa_clean_factunit()
    clean_facts = {clean_fact.fcontext: clean_fact}
    bob_cell = cellunit_shop(
        bob_str,
        [],
        event7,
        0,
        believeradjust=bob_believeradjust,
        believerevent_facts=clean_facts,
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
    bob_believeradjust = get_bob_mop_with_reason_believerunit_example()
    # create cell file
    clean_fact = example_casa_clean_factunit()
    clean_facts = {clean_fact.fcontext: clean_fact}
    bob_cell = cellunit_shop(
        bob_str,
        [],
        event7,
        celldepth=0,
        believeradjust=bob_believeradjust,
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
    bob_believeradjust = get_bob_mop_without_reason_believerunit_example()
    bob_believeradjust.add_personunit(sue_str, 1)
    bob_sue_believeradjust = believerunit_shop(sue_str, a23_str)
    # create cell file
    bob_cell = cellunit_shop(
        bob_str, bob_ancs, event_int=e7, celldepth=2, believeradjust=bob_believeradjust
    )
    bob_sue_cell = cellunit_shop(
        bob_str,
        bob_sue_ancs,
        event_int=e7,
        celldepth=0,
        believeradjust=bob_sue_believeradjust,
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
    bob_believeradjust = get_bob_mop_with_reason_believerunit_example()
    bob_believeradjust.add_personunit(sue_str, 1)
    bob_sue_believeradjust = get_bob_mop_with_reason_believerunit_example()
    bob_sue_believeradjust.set_believer_name(sue_str)
    # create cell file
    dirty_fact = example_casa_dirty_factunit()
    dirty_facts = {dirty_fact.fcontext: dirty_fact}
    bob_cell = cellunit_shop(
        bob_str,
        bob_ancs,
        event_int=e7,
        celldepth=2,
        believeradjust=bob_believeradjust,
        believerevent_facts=dirty_facts,
    )
    bob_sue_cell = cellunit_shop(
        bob_str,
        bob_sue_ancs,
        event_int=e7,
        celldepth=0,
        believeradjust=bob_sue_believeradjust,
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
    bob_believeradjust = get_bob_mop_with_reason_believerunit_example()
    bob_believeradjust.add_personunit(sue_str, 1)
    b_sue_ba = get_bob_mop_with_reason_believerunit_example()
    b_sue_ba.set_believer_name(sue_str)
    b_sue_ba.add_personunit(yao_str, 1)
    bs_yao_ba = get_bob_mop_with_reason_believerunit_example()
    bs_yao_ba.set_believer_name(yao_str)
    bs_yao_ba.add_personunit(zia_str, 1)
    bsy_zia_ba = get_bob_mop_with_reason_believerunit_example()
    bsy_zia_ba.set_believer_name(zia_str)
    # create cell file
    dirty_fact = example_casa_dirty_factunit()
    dirty_facts = {dirty_fact.fcontext: dirty_fact}
    bob_cell = cellunit_shop(
        bob_str,
        bob_ancs,
        event_int=e7,
        celldepth=4,
        believeradjust=bob_believeradjust,
        believerevent_facts=dirty_facts,
    )
    b_sue_cell = cellunit_shop(bob_str, b_sue_ancs, e7, 0, believeradjust=b_sue_ba)
    bs_yao_cell = cellunit_shop(bob_str, bs_yao_ancs, e7, 0, believeradjust=bs_yao_ba)
    bsy_zia_cell = cellunit_shop(
        bob_str, bsy_zia_ancs, e7, 0, believeradjust=bsy_zia_ba
    )
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
    bob_believeradjust = get_bob_mop_with_reason_believerunit_example()
    bob_believeradjust.add_personunit(sue_str, 1)
    b_sue_ba = get_bob_mop_with_reason_believerunit_example()
    b_sue_ba.set_believer_name(sue_str)
    b_sue_ba.add_personunit(yao_str, 1)
    bs_yao_ba = get_bob_mop_with_reason_believerunit_example()
    bs_yao_ba.set_believer_name(yao_str)
    bs_yao_ba.add_personunit(zia_str, 1)
    bsy_zia_ba = get_bob_mop_with_reason_believerunit_example()
    bsy_zia_ba.set_believer_name(zia_str)
    # create cell file
    dirty_fact = example_casa_dirty_factunit()
    dirty_facts = {dirty_fact.fcontext: dirty_fact}
    bob_cell = cellunit_shop(
        bob_str,
        bob_ancs,
        event_int=e7,
        celldepth=2,
        believeradjust=bob_believeradjust,
        believerevent_facts=dirty_facts,
    )
    b_sue_cell = cellunit_shop(bob_str, b_sue_ancs, e7, 0, believeradjust=b_sue_ba)
    bs_yao_cell = cellunit_shop(bob_str, bs_yao_ancs, e7, 0, believeradjust=bs_yao_ba)
    bsy_zia_cell = cellunit_shop(
        bob_str, bsy_zia_ancs, e7, 0, believeradjust=bsy_zia_ba
    )
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
    bob_believeradjust = get_bob_mop_with_reason_believerunit_example()
    bob_believeradjust.add_personunit(sue_str, 1)
    b_sue_ba = believerunit_shop(sue_str, a23_str)
    b_sue_ba.set_believer_name(sue_str)
    b_sue_ba.add_personunit(yao_str, 1)
    bs_yao_ba = get_bob_mop_with_reason_believerunit_example()
    bs_yao_ba.set_believer_name(yao_str)
    bs_yao_ba.add_personunit(zia_str, 1)
    clean_fact = example_casa_clean_factunit()
    bs_yao_ba.add_fact(clean_fact.fcontext, clean_fact.fstate)
    bsy_zia_ba = get_bob_mop_with_reason_believerunit_example()
    bsy_zia_ba.set_believer_name(zia_str)
    # create cell file
    dirty_fact = example_casa_dirty_factunit()
    dirty_facts = {dirty_fact.fcontext: dirty_fact}
    bob_cell = cellunit_shop(
        bob_str,
        bob_ancs,
        event_int=e7,
        celldepth=3,
        believeradjust=bob_believeradjust,
        believerevent_facts=dirty_facts,
    )
    b_sue_cell = cellunit_shop(bob_str, b_sue_ancs, e7, 0, believeradjust=b_sue_ba)
    bs_yao_cell = cellunit_shop(bob_str, bs_yao_ancs, e7, 0)
    bs_yao_cell.eval_believerevent(bs_yao_ba)
    bsy_zia_cell = cellunit_shop(
        bob_str, bsy_zia_ancs, e7, 0, believeradjust=bsy_zia_ba
    )
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
    clean_facts = {clean_fact.fcontext: clean_fact}
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == clean_facts
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == clean_facts


def test_set_cell_trees_decrees_SetsChildCells_Scenario7_NoCell_GetBelieverEvent(
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
    bob_believeradjust = get_bob_mop_with_reason_believerunit_example()
    bob_believeradjust.add_personunit(sue_str, 1)
    b_sue_ba = get_bob_mop_with_reason_believerunit_example()
    b_sue_ba.set_believer_name(sue_str)
    b_sue_ba.add_personunit(yao_str, 1)
    bs_yao_ba = get_bob_mop_with_reason_believerunit_example()
    bs_yao_ba.set_believer_name(yao_str)
    bs_yao_ba.add_personunit(zia_str, 1)
    bsy_zia_ba = get_bob_mop_with_reason_believerunit_example()
    bsy_zia_ba.set_believer_name(zia_str)
    # create cell file
    dirty_fact = example_casa_dirty_factunit()
    dirty_facts = {dirty_fact.fcontext: dirty_fact}
    bob_cell = cellunit_shop(
        bob_str,
        bob_ancs,
        event_int=e7,
        celldepth=4,
        believeradjust=bob_believeradjust,
        believerevent_facts=dirty_facts,
    )
    b_sue_cell = cellunit_shop(bob_str, b_sue_ancs, e7, 0, believeradjust=b_sue_ba)
    # bs_yao_cell = cellunit_shop(bob_str, bs_yao_ancs, e7, 0, believeradjust=bs_yao_ba)
    bsy_zia_cell = cellunit_shop(
        bob_str, bsy_zia_ancs, e7, 0, believeradjust=bsy_zia_ba
    )
    bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_ancs)
    bob_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, b_sue_ancs)
    bob_sue_yao_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bs_yao_ancs)
    bob_sue_yao_zia_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bsy_zia_ancs)
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_sue_dir, b_sue_cell)
    believerevent_path = create_believerevent_path(mstr_dir, a23_str, yao_str, e7)
    save_believer_file(believerevent_path, None, bs_yao_ba)
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
