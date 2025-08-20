from os.path import exists as os_path_exists
from pytest import raises as pytest_raises
from src.a00_data_toolbox.file_toolbox import create_path, open_json, set_dir
from src.a01_term_logic.rope import create_rope
from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a06_belief_logic.test._util.a06_str import penny_str
from src.a06_belief_logic.test._util.example_beliefs import (
    get_beliefunit_irrational_example,
    get_beliefunit_with_4_levels,
)
from src.a09_pack_logic.test._util.a09_str import event_int_str
from src.a11_bud_logic.cell import CELLNODE_QUOTA_DEFAULT, cellunit_shop
from src.a11_bud_logic.test._util.a11_str import (
    ancestors_str,
    bud_belief_name_str,
    celldepth_str,
    quota_str,
)
from src.a11_bud_logic.test._util.example_factunits import (
    example_casa_clean_factunit as clean_factunit,
    example_casa_dirty_factunit as dirty_factunit,
    example_casa_grimy_factunit as grimy_factunit,
    example_sky_blue_factunit as sky_blue_factunit,
)
from src.a12_hub_toolbox.a12_path import (
    create_belief_event_dir_path,
    create_beliefevent_path,
    create_beliefpoint_path,
    create_budunit_json_path,
    create_cell_dir_path,
    create_cell_json_path as node_path,
    create_cell_partner_mandate_ledger_path,
    create_gut_path,
    create_job_path,
)
from src.a12_hub_toolbox.hub_tool import (
    beliefpoint_file_exists,
    bud_file_exists,
    cellunit_add_json_file,
    cellunit_get_from_dir,
    cellunit_save_to_dir,
    collect_belief_event_dir_sets,
    create_cell_partner_mandate_ledger_json,
    get_beliefevent_obj,
    get_beliefs_downhill_event_ints,
    get_timepoint_dirs,
    gut_file_exists,
    job_file_exists,
    open_belief_file,
    open_beliefpoint_file,
    open_bud_file,
    open_gut_file,
    open_job_file,
    save_arbitrary_beliefevent,
    save_belief_file,
    save_beliefpoint_file,
    save_bud_file,
    save_gut_file,
    save_job_file,
)
from src.a12_hub_toolbox.test._util.a12_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a12_hub_toolbox.test._util.example_hub_atoms import (
    get_budunit_55_example,
    get_budunit_invalid_example,
)


def test_save_belief_file_SetsFile(env_dir_setup_cleanup):
    # ESTABLISH
    temp_dir = get_module_temp_dir()
    belief_filename = "belief.json"
    belief_path = create_path(temp_dir, belief_filename)
    sue_str = "Sue"
    sue_belief = beliefunit_shop(sue_str)
    assert os_path_exists(belief_path) is False

    # WHEN
    save_belief_file(belief_path, None, sue_belief)

    # THEN
    assert os_path_exists(belief_path)


def test_open_belief_file_ReturnsObj_Scenario0_NoFile():
    # ESTABLISH
    temp_dir = get_module_temp_dir()
    belief_filename = "belief.json"
    belief_path = create_path(temp_dir, belief_filename)
    assert os_path_exists(belief_path) is False

    # WHEN
    gen_sue_belief = open_belief_file(belief_path)

    # THEN
    assert not gen_sue_belief


def test_open_belief_file_ReturnsObj_Scenario1_FileExists():
    # ESTABLISH
    temp_dir = get_module_temp_dir()
    belief_filename = "belief.json"
    belief_path = create_path(temp_dir, belief_filename)
    sue_str = "Sue"
    expected_sue_belief = beliefunit_shop(sue_str)
    save_belief_file(belief_path, None, expected_sue_belief)
    assert os_path_exists(belief_path)

    # WHEN
    gen_sue_belief = open_belief_file(belief_path)

    # THEN
    assert gen_sue_belief == expected_sue_belief


def test_save_gut_file_SetsFile(env_dir_setup_cleanup):
    # ESTABLISH
    coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    sue_gut_path = create_gut_path(coin_mstr_dir, a23_str, sue_str)
    sue_belief = beliefunit_shop(sue_str, a23_str)
    assert os_path_exists(sue_gut_path) is False

    # WHEN
    save_gut_file(coin_mstr_dir, sue_belief)

    # THEN
    assert os_path_exists(sue_gut_path)


def test_gut_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    sue_belief = beliefunit_shop(sue_str, a23_str)
    assert gut_file_exists(coin_mstr_dir, a23_str, sue_str) is False

    # WHEN
    save_gut_file(coin_mstr_dir, sue_belief)

    # THEN
    assert gut_file_exists(coin_mstr_dir, a23_str, sue_str)


def test_open_gut_file_ReturnsObj_Scenario0_noFile():
    # ESTABLISH
    coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    sue_gut_path = create_gut_path(coin_mstr_dir, a23_str, sue_str)
    assert os_path_exists(sue_gut_path) is False

    # WHEN / THEN
    assert not open_gut_file(coin_mstr_dir, a23_str, sue_str)


def test_open_gut_file_ReturnsObj_Scenario1_FileExists():
    # ESTABLISH
    coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    sue_gut_path = create_gut_path(coin_mstr_dir, a23_str, sue_str)
    sue_belief = beliefunit_shop(sue_str, a23_str)
    save_gut_file(coin_mstr_dir, sue_belief)
    assert os_path_exists(sue_gut_path)

    # WHEN / THEN
    assert sue_belief == open_gut_file(coin_mstr_dir, a23_str, sue_str)


def test_save_job_file_SetsFile(env_dir_setup_cleanup):
    # ESTABLISH
    coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    sue_job_path = create_job_path(coin_mstr_dir, a23_str, sue_str)
    sue_belief = beliefunit_shop(sue_str, a23_str)
    assert os_path_exists(sue_job_path) is False

    # WHEN
    save_job_file(coin_mstr_dir, sue_belief)

    # THEN
    assert os_path_exists(sue_job_path)


def test_job_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    sue_belief = beliefunit_shop(sue_str, a23_str)
    assert job_file_exists(coin_mstr_dir, a23_str, sue_str) is False

    # WHEN
    save_job_file(coin_mstr_dir, sue_belief)

    # THEN
    assert job_file_exists(coin_mstr_dir, a23_str, sue_str)


def test_open_job_file_ReturnsObj_Scenario0_noFile():
    # ESTABLISH
    coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    sue_job_path = create_job_path(coin_mstr_dir, a23_str, sue_str)
    assert os_path_exists(sue_job_path) is False

    # WHEN / THEN
    assert not open_job_file(coin_mstr_dir, a23_str, sue_str)


def test_open_job_file_ReturnsObj_Scenario1_FileExists():
    # ESTABLISH
    coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    sue_job_path = create_job_path(coin_mstr_dir, a23_str, sue_str)
    sue_belief = beliefunit_shop(sue_str, a23_str)
    save_job_file(coin_mstr_dir, sue_belief)
    assert os_path_exists(sue_job_path)

    # WHEN / THEN
    assert sue_belief == open_job_file(coin_mstr_dir, a23_str, sue_str)


def test_save_arbitrary_beliefevent_SetsFile_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    event5 = 5
    sue_str = "Sue"
    beliefevent_path = create_beliefevent_path(coin_mstr_dir, a23_str, sue_str, event5)
    assert os_path_exists(beliefevent_path) is False

    # WHEN
    save_arbitrary_beliefevent(coin_mstr_dir, a23_str, sue_str, event5)

    # THEN
    assert os_path_exists(beliefevent_path)
    expected_sue_belief = beliefunit_shop(sue_str, a23_str)
    assert open_belief_file(beliefevent_path).to_dict() == expected_sue_belief.to_dict()


def test_save_arbitrary_beliefevent_SetsFile_Scenario1_includes_facts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    event5 = 5
    sue_str = "Sue"
    beliefevent_path = create_beliefevent_path(coin_mstr_dir, a23_str, sue_str, event5)
    casa_rope = create_rope(a23_str, "casa")
    clean_rope = create_rope(casa_rope, "clean")
    clean_fact_lower = 11
    clean_fact_upper = 16
    x_facts = [(casa_rope, clean_rope, clean_fact_lower, clean_fact_upper)]
    assert os_path_exists(beliefevent_path) is False

    # WHEN
    save_arbitrary_beliefevent(coin_mstr_dir, a23_str, sue_str, event5, facts=x_facts)

    # THEN
    assert os_path_exists(beliefevent_path)
    expected_sue_belief = beliefunit_shop(sue_str, a23_str)
    expected_sue_belief.add_fact(
        casa_rope, clean_rope, clean_fact_lower, clean_fact_upper, True
    )
    gen_sue_belief = open_belief_file(beliefevent_path)
    assert (
        gen_sue_belief.get_factunits_dict() == expected_sue_belief.get_factunits_dict()
    )
    assert gen_sue_belief.to_dict() == expected_sue_belief.to_dict()


def test_get_beliefevent_obj_ReturnsObj_Scenario0_NoFile(env_dir_setup_cleanup):
    # ESTABLISH
    coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy"
    sue_str = "Sue"
    t3 = 3

    # WHEN / THEN
    assert get_beliefevent_obj(coin_mstr_dir, a23_str, sue_str, t3) is None


def test_get_beliefevent_obj_ReturnsObj_Scenario1_FileExists(env_dir_setup_cleanup):
    # ESTABLISH
    coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy"
    sue_str = "Sue"
    t3 = 3
    t3_json_path = create_beliefevent_path(coin_mstr_dir, a23_str, sue_str, t3)
    sue_belief = beliefunit_shop(sue_str, a23_str)
    casa_rope = sue_belief.make_l1_rope("casa")
    clean_rope = sue_belief.make_l1_rope("clean")
    dirty_rope = sue_belief.make_l1_rope("dirty")
    sue_belief.add_fact(casa_rope, dirty_rope, create_missing_plans=True)
    save_belief_file(t3_json_path, None, sue_belief)

    # WHEN
    gen_a3_beliefevent = get_beliefevent_obj(coin_mstr_dir, a23_str, sue_str, t3)

    # THEN
    assert gen_a3_beliefevent == sue_belief


def test_collect_belief_event_dir_sets_ReturnsObj_Scenario0_none(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    # WHEN
    belief_events_sets = collect_belief_event_dir_sets(coin_mstr_dir, a23_str)
    # THEN
    assert belief_events_sets == {}


def test_collect_belief_event_dir_sets_ReturnsObj_Scenario1_DirsExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    bob_str = "Bob"
    event1 = 1
    event2 = 2
    bob1_dir = create_belief_event_dir_path(coin_mstr_dir, a23_str, bob_str, event1)
    bob2_dir = create_belief_event_dir_path(coin_mstr_dir, a23_str, bob_str, event2)
    print(f"  {bob1_dir=}")
    print(f"  {bob2_dir=}")
    set_dir(bob1_dir)
    set_dir(bob2_dir)

    # WHEN
    belief_events_sets = collect_belief_event_dir_sets(coin_mstr_dir, a23_str)

    # THEN
    assert belief_events_sets == {bob_str: {event1, event2}}


def test_collect_belief_event_dir_sets_ReturnsObj_Scenario2_DirsExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    bob_str = "Bob"
    sue_str = "Sue"
    event1 = 1
    event2 = 2
    event7 = 7
    bob1_dir = create_belief_event_dir_path(coin_mstr_dir, a23_str, bob_str, event1)
    bob2_dir = create_belief_event_dir_path(coin_mstr_dir, a23_str, bob_str, event2)
    sue2_dir = create_belief_event_dir_path(coin_mstr_dir, a23_str, sue_str, event2)
    sue7_dir = create_belief_event_dir_path(coin_mstr_dir, a23_str, sue_str, event7)
    set_dir(bob1_dir)
    set_dir(bob2_dir)
    set_dir(sue2_dir)
    set_dir(sue7_dir)

    # WHEN
    belief_events_sets = collect_belief_event_dir_sets(coin_mstr_dir, a23_str)

    # THEN
    assert belief_events_sets == {
        bob_str: {event1, event2},
        sue_str: {event2, event7},
    }


def test_get_beliefs_downhill_event_ints_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    event2 = 2
    belief_events_sets = {}
    downhill_event_int = event2
    downhill_beliefs = {bob_str, sue_str}

    # WHEN
    beliefs_downhill_event_ints = get_beliefs_downhill_event_ints(
        belief_events_sets, downhill_beliefs, downhill_event_int
    )

    # THEN
    assert beliefs_downhill_event_ints == {}


def test_get_beliefs_downhill_event_ints_ReturnsObj_Scenario1_simple():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    event1 = 1
    event2 = 2
    event7 = 7
    belief_events_sets = {bob_str: {event1, event2}, sue_str: {event2, event7}}
    downhill_event_int = event2
    downhill_beliefs = {bob_str, sue_str}

    # WHEN
    beliefs_downhill_event_ints = get_beliefs_downhill_event_ints(
        belief_events_sets, downhill_beliefs, downhill_event_int
    )

    # THEN
    assert beliefs_downhill_event_ints == {bob_str: event2, sue_str: event2}


def test_get_beliefs_downhill_event_ints_ReturnsObj_Scenario2Empty_downhill_event_int():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event2 = 2
    event7 = 7
    belief_events_sets = {
        bob_str: {event1, event2},
        sue_str: {event2, event7},
        yao_str: {event1, event2, event7},
    }
    downhill_beliefs = {bob_str, sue_str}

    # WHEN
    beliefs_downhill_event_ints = get_beliefs_downhill_event_ints(
        belief_events_sets, downhill_beliefs
    )

    # THEN
    assert beliefs_downhill_event_ints == {bob_str: event2, sue_str: event7}


def test_get_beliefs_downhill_event_ints_ReturnsObj_Scenario3Empty_downhill_beliefs():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event2 = 2
    event7 = 7
    belief_events_sets = {
        bob_str: {event1, event2},
        sue_str: {event2, event7},
        yao_str: {event1, event2, event7},
    }

    # WHEN
    beliefs_downhill_event_ints = get_beliefs_downhill_event_ints(belief_events_sets)

    # THEN
    assert beliefs_downhill_event_ints == {
        bob_str: event2,
        sue_str: event7,
        yao_str: event7,
    }


def test_get_beliefs_downhill_event_ints_ReturnsObj_Scenario4Empty_downhill_beliefs_Withdownhill_event_int():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event2 = 2
    event7 = 7
    belief_events_sets = {
        bob_str: {event1, event2},
        sue_str: {event2, event7},
        yao_str: {event7},
    }
    downhill_event_int = 2

    # WHEN
    beliefs_downhill_event_ints = get_beliefs_downhill_event_ints(
        belief_events_sets, ref_event_int=downhill_event_int
    )

    # THEN
    assert beliefs_downhill_event_ints == {bob_str: event2, sue_str: event2}


def test_cellunit_add_json_file_SetsFile_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    time7 = 777000
    sue_str = "Sue"
    sue7_cell_path = node_path(coin_mstr_dir, a23_str, sue_str, time7)
    event3 = 3
    das = []
    quota500 = 500
    celldepth4 = 4
    penny6 = 6
    assert os_path_exists(sue7_cell_path) is False

    # WHEN
    cellunit_add_json_file(
        coin_mstr_dir=coin_mstr_dir,
        coin_label=a23_str,
        time_belief_name=sue_str,
        bud_time=time7,
        quota=quota500,
        event_int=event3,
        celldepth=celldepth4,
        penny=penny6,
        bud_ancestors=das,
    )

    # THEN
    print(f"{sue7_cell_path=}")
    assert os_path_exists(sue7_cell_path)
    generated_cell_dict = open_json(sue7_cell_path)
    assert generated_cell_dict.get(ancestors_str()) == das
    assert generated_cell_dict.get(event_int_str()) == event3
    assert generated_cell_dict.get(celldepth_str()) == celldepth4
    assert generated_cell_dict.get(bud_belief_name_str()) == sue_str
    assert generated_cell_dict.get(penny_str()) == penny6
    assert generated_cell_dict.get(quota_str()) == quota500


def test_cellunit_add_json_file_SetsFile_Scenario1_ManyParametersEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    time7 = 777000
    sue_str = "Sue"
    bob_str = "Bob"
    das = [bob_str, sue_str]
    sue7_cell_path = node_path(coin_mstr_dir, a23_str, sue_str, time7, das)
    event3 = 3
    assert os_path_exists(sue7_cell_path) is False

    # WHEN
    cellunit_add_json_file(
        coin_mstr_dir, a23_str, sue_str, time7, event3, bud_ancestors=das
    )

    # THEN
    print(f"{sue7_cell_path=}")
    assert os_path_exists(sue7_cell_path)
    generated_cell_dict = open_json(sue7_cell_path)
    assert generated_cell_dict.get(ancestors_str()) == das
    assert generated_cell_dict.get(event_int_str()) == event3
    assert generated_cell_dict.get(celldepth_str()) == 0
    assert generated_cell_dict.get(bud_belief_name_str()) == sue_str
    assert generated_cell_dict.get(penny_str()) == 1
    assert generated_cell_dict.get(quota_str()) == CELLNODE_QUOTA_DEFAULT


def test_cellunit_get_from_dir_ReturnsObj_Scenario0_NoFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    time7 = 777000
    sue_str = "Sue"
    bob_str = "Bob"
    das = [bob_str, sue_str]
    sue7_cell_path = node_path(coin_mstr_dir, a23_str, sue_str, time7, das)
    event3 = 3
    assert os_path_exists(sue7_cell_path) is False
    cell_dir = create_cell_dir_path(
        coin_mstr_dir, a23_str, sue_str, time7, bud_ancestors=das
    )

    # WHEN / THEN
    assert cellunit_get_from_dir(cell_dir) is None


def test_cellunit_get_from_dir_ReturnsObj_Scenario1_FileExists(env_dir_setup_cleanup):
    # ESTABLISH
    coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    time7 = 777000
    sue_str = "Sue"
    bob_str = "Bob"
    das = [bob_str, sue_str]
    sue7_cell_path = node_path(coin_mstr_dir, a23_str, sue_str, time7, das)
    event3 = 3
    assert os_path_exists(sue7_cell_path) is False
    cellunit_add_json_file(
        coin_mstr_dir, a23_str, sue_str, time7, event3, bud_ancestors=das
    )
    cell_dir = create_cell_dir_path(
        coin_mstr_dir, a23_str, sue_str, time7, bud_ancestors=das
    )

    # WHEN
    gen_cellunit = cellunit_get_from_dir(cell_dir)

    # THEN
    expected_cellunit = cellunit_shop(sue_str, ancestors=das, event_int=event3)
    assert gen_cellunit == expected_cellunit


def test_cellunit_save_to_dir_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    coin_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    time7 = 777000
    sue_str = "Sue"
    bob_str = "Bob"
    das = [bob_str, sue_str]
    sue7_cell_path = node_path(coin_mstr_dir, a23_str, sue_str, time7, das)
    event3 = 3
    sue_cell = cellunit_shop(sue_str, ancestors=das, event_int=event3)
    cell_dir = create_cell_dir_path(coin_mstr_dir, a23_str, sue_str, time7, das)
    assert os_path_exists(sue7_cell_path) is False

    # WHEN
    cellunit_save_to_dir(cell_dir, sue_cell)

    # THEN
    assert os_path_exists(sue7_cell_path)
    assert cellunit_get_from_dir(cell_dir) == sue_cell


def test_create_cell_partner_mandate_ledger_json_CreatesFile_Scenario0_NoCellFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    a23_str = "amy23"
    bob_str = "Bob"
    tp6 = 6
    sue_partner_mandate_ledger_path = create_cell_partner_mandate_ledger_path(
        mstr_dir, a23_str, bob_str, tp6, sue_ancestors
    )
    sue_cell_dir = create_cell_dir_path(mstr_dir, a23_str, bob_str, tp6, sue_ancestors)
    assert os_path_exists(sue_partner_mandate_ledger_path) is False

    # WHEN
    create_cell_partner_mandate_ledger_json(sue_cell_dir)

    # THEN
    assert os_path_exists(sue_partner_mandate_ledger_path) is False


def test_create_cell_partner_mandate_ledger_json_CreatesFile_Scenario1(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    yao_str = "Yao"
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    sue_event7 = 7
    sue_celldepth3 = 3
    sue_penny2 = 2
    sue_quota300 = 300
    sue_mandate = 444
    a23_str = "amy23"
    sue_belief = beliefunit_shop(sue_str, a23_str)
    sue_belief.add_partnerunit(sue_str, 3, 5)
    sue_belief.add_partnerunit(yao_str, 7, 2)
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sue_belief.add_plan(clean_fact.fact_state)
    sue_belief.add_plan(dirty_fact.fact_state)
    casa_rope = sue_belief.make_l1_rope("casa")
    mop_rope = sue_belief.make_rope(casa_rope, "mop")
    sue_belief.add_plan(mop_rope, 1, task=True)
    sue_belief.edit_reason(mop_rope, dirty_fact.fact_context, dirty_fact.fact_state)
    sue_belief.add_fact(
        dirty_fact.fact_context, dirty_fact.fact_state, create_missing_plans=True
    )
    sky_blue_fact = sky_blue_factunit()
    sue_beliefevent_factunits = {clean_fact.fact_context: clean_fact}
    sue_found_factunits = {dirty_fact.fact_context: dirty_fact}
    sue_boss_factunits = {sky_blue_fact.fact_context: sky_blue_fact}
    sue_cell = cellunit_shop(
        bud_belief_name=yao_str,
        ancestors=sue_ancestors,
        event_int=sue_event7,
        celldepth=sue_celldepth3,
        penny=sue_penny2,
        quota=sue_quota300,
        beliefadjust=sue_belief,
        beliefevent_facts=sue_beliefevent_factunits,
        found_facts=sue_found_factunits,
        boss_facts=sue_boss_factunits,
        mandate=sue_mandate,
    )
    sue_cell._reason_contexts = set()
    bob_str = "Bob"
    tp6 = 6
    sue_partner_mandate_ledger_path = create_cell_partner_mandate_ledger_path(
        mstr_dir, a23_str, bob_str, tp6, sue_ancestors
    )
    sue_cell_dir = create_cell_dir_path(mstr_dir, a23_str, bob_str, tp6, sue_ancestors)
    cellunit_save_to_dir(sue_cell_dir, sue_cell)
    assert os_path_exists(sue_partner_mandate_ledger_path) is False

    # WHEN
    create_cell_partner_mandate_ledger_json(sue_cell_dir)

    # THEN
    assert os_path_exists(sue_partner_mandate_ledger_path)
    assert open_json(sue_partner_mandate_ledger_path) == {yao_str: 311, sue_str: 133}


def test_save_valid_bud_file_Scenario0_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    yao_str = "Yao"
    t55_bud = get_budunit_55_example()
    t55_bud_time = t55_bud.bud_time
    t55_bud_path = create_budunit_json_path(mstr_dir, a23_str, yao_str, t55_bud_time)
    assert os_path_exists(t55_bud_path) is False

    # WHEN
    save_bud_file(mstr_dir, a23_str, yao_str, t55_bud)

    # THEN
    assert os_path_exists(t55_bud_path)


def test_save_valid_bud_file_Scenario1_RaisesError(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    yao_str = "Yao"
    invalid_bud = get_budunit_invalid_example()

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        save_bud_file(mstr_dir, a23_str, yao_str, invalid_bud)
    exception_str = "magnitude cannot be calculated: debt_bud_partner_net=-5, cred_bud_partner_net=3"
    assert str(excinfo.value) == exception_str


def test_bud_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    yao_str = "Yao"
    t55_bud = get_budunit_55_example()
    assert not bud_file_exists(mstr_dir, a23_str, yao_str, t55_bud.bud_time)

    # WHEN
    save_bud_file(mstr_dir, a23_str, yao_str, t55_bud)

    # THEN
    assert bud_file_exists(mstr_dir, a23_str, yao_str, t55_bud.bud_time)


def test_open_bud_file_ReturnsObj_Scenario0_NoFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    yao_str = "Yao"
    t55_bud = get_budunit_55_example()
    t55_bud_time = t55_bud.bud_time
    assert not bud_file_exists(mstr_dir, a23_str, yao_str, t55_bud_time)

    # WHEN / THEN
    assert not open_bud_file(mstr_dir, a23_str, yao_str, t55_bud_time)


def test_open_bud_file_ReturnsObj_Scenario1_FileExists(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    yao_str = "Yao"
    t55_bud = get_budunit_55_example()
    t55_bud_time = t55_bud.bud_time
    save_bud_file(mstr_dir, a23_str, yao_str, t55_bud)
    assert bud_file_exists(mstr_dir, a23_str, yao_str, t55_bud_time)

    # WHEN / THEN
    assert open_bud_file(mstr_dir, a23_str, yao_str, t55_bud_time) == t55_bud


def test_save_beliefpoint_file_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    t55_beliefpoint = get_beliefunit_with_4_levels()
    t55_bud_time = 55
    t55_beliefpoint_path = create_beliefpoint_path(
        mstr_dir, a23_str, sue_str, t55_bud_time
    )
    print(f"{t55_beliefpoint.coin_label=}")
    print(f"               {mstr_dir=}")
    print(f"      {t55_beliefpoint_path=}")
    assert os_path_exists(t55_beliefpoint_path) is False

    # WHEN
    save_beliefpoint_file(mstr_dir, t55_beliefpoint, t55_bud_time)

    # THEN
    assert os_path_exists(t55_beliefpoint_path)


def test_save_beliefpoint_file_RaisesError(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    irrational_beliefpoint = get_beliefunit_irrational_example()
    t55_bud_time = 55

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        save_beliefpoint_file(mstr_dir, irrational_beliefpoint, t55_bud_time)
    exception_str = "BeliefPoint could not be saved BeliefUnit._rational is False"
    assert str(excinfo.value) == exception_str


def test_beliefpoint_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    t55_bud_time = 55
    assert beliefpoint_file_exists(mstr_dir, a23_str, sue_str, t55_bud_time) is False

    # WHEN
    t55_beliefpoint = get_beliefunit_with_4_levels()
    save_beliefpoint_file(mstr_dir, t55_beliefpoint, t55_bud_time)

    # THEN
    assert beliefpoint_file_exists(mstr_dir, a23_str, sue_str, t55_bud_time)


def test_open_beliefpoint_file_ReturnsObj_Scenario0_NoFileExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    t55_bud_time = 55
    assert not beliefpoint_file_exists(mstr_dir, a23_str, sue_str, t55_bud_time)

    # WHEN / THEN
    assert not open_beliefpoint_file(mstr_dir, a23_str, sue_str, t55_bud_time)


def test_open_beliefpoint_file_ReturnsObj_Scenario1_FileExists(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    t55_bud_time = 55
    t55_beliefpoint = get_beliefunit_with_4_levels()
    save_beliefpoint_file(mstr_dir, t55_beliefpoint, t55_bud_time)
    assert beliefpoint_file_exists(mstr_dir, a23_str, sue_str, t55_bud_time)

    # WHEN
    file_beliefpoint = open_beliefpoint_file(mstr_dir, a23_str, sue_str, t55_bud_time)

    # THEN
    assert file_beliefpoint.to_dict() == t55_beliefpoint.to_dict()


def test_get_timepoint_dirs_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    t55_bud_time = 55
    t77_bud_time = 77
    beliefpoint = get_beliefunit_with_4_levels()
    save_beliefpoint_file(mstr_dir, beliefpoint, t55_bud_time)
    save_beliefpoint_file(mstr_dir, beliefpoint, t77_bud_time)

    # WHEN
    timepoint_dirs = get_timepoint_dirs(mstr_dir, a23_str, sue_str)

    # THEN
    assert timepoint_dirs == [t55_bud_time, t77_bud_time]
