from os.path import exists as os_path_exists
from pytest import raises as pytest_raises
from src.a00_data_toolbox.file_toolbox import create_path, open_json, set_dir
from src.a01_term_logic.rope import create_rope
from src.a02_finance_logic._test_util.a02_str import quota_str
from src.a06_plan_logic._test_util.a06_str import penny_str
from src.a06_plan_logic._test_util.example_plans import (
    get_planunit_irrational_example,
    get_planunit_with_4_levels,
)
from src.a06_plan_logic.plan import planunit_shop
from src.a09_pack_logic._test_util.a09_str import event_int_str
from src.a11_bud_cell_logic._test_util.a11_str import (
    ancestors_str,
    bud_owner_name_str,
    celldepth_str,
)
from src.a11_bud_cell_logic._test_util.example_factunits import (
    example_casa_clean_factunit as clean_factunit,
    example_casa_dirty_factunit as dirty_factunit,
    example_casa_grimy_factunit as grimy_factunit,
    example_sky_blue_factunit as sky_blue_factunit,
)
from src.a11_bud_cell_logic.cell import CELLNODE_QUOTA_DEFAULT, cellunit_shop
from src.a12_hub_toolbox._test_util.a12_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a12_hub_toolbox._test_util.example_hub_atoms import (
    get_budunit_55_example,
    get_budunit_invalid_example,
)
from src.a12_hub_toolbox.hub_path import (
    create_budunit_json_path,
    create_cell_acct_mandate_ledger_path,
    create_cell_dir_path,
    create_cell_json_path as node_path,
    create_gut_path,
    create_job_path,
    create_owner_event_dir_path,
    create_planevent_path,
    create_planpoint_path,
)
from src.a12_hub_toolbox.hub_tool import (
    bud_file_exists,
    cellunit_add_json_file,
    cellunit_get_from_dir,
    cellunit_save_to_dir,
    collect_owner_event_dir_sets,
    create_cell_acct_mandate_ledger_json,
    get_owners_downhill_event_ints,
    get_planevent_obj,
    get_timepoint_dirs,
    gut_file_exists,
    job_file_exists,
    open_bud_file,
    open_gut_file,
    open_job_file,
    open_plan_file,
    open_planpoint_file,
    planpoint_file_exists,
    save_arbitrary_planevent,
    save_bud_file,
    save_gut_file,
    save_job_file,
    save_plan_file,
    save_planpoint_file,
)


def test_save_plan_file_SetsFile(env_dir_setup_cleanup):
    # ESTABLISH
    temp_dir = get_module_temp_dir()
    plan_filename = "plan.json"
    plan_path = create_path(temp_dir, plan_filename)
    sue_str = "Sue"
    sue_plan = planunit_shop(sue_str)
    assert os_path_exists(plan_path) is False

    # WHEN
    save_plan_file(plan_path, None, sue_plan)

    # THEN
    assert os_path_exists(plan_path)


def test_open_plan_file_ReturnsObj_Scenario0_NoFile():
    # ESTABLISH
    temp_dir = get_module_temp_dir()
    plan_filename = "plan.json"
    plan_path = create_path(temp_dir, plan_filename)
    assert os_path_exists(plan_path) is False

    # WHEN
    gen_sue_plan = open_plan_file(plan_path)

    # THEN
    assert not gen_sue_plan


def test_open_plan_file_ReturnsObj_Scenario1_FileExists():
    # ESTABLISH
    temp_dir = get_module_temp_dir()
    plan_filename = "plan.json"
    plan_path = create_path(temp_dir, plan_filename)
    sue_str = "Sue"
    expected_sue_plan = planunit_shop(sue_str)
    save_plan_file(plan_path, None, expected_sue_plan)
    assert os_path_exists(plan_path)

    # WHEN
    gen_sue_plan = open_plan_file(plan_path)

    # THEN
    assert gen_sue_plan == expected_sue_plan


def test_save_gut_file_SetsFile(env_dir_setup_cleanup):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    sue_gut_path = create_gut_path(vow_mstr_dir, a23_str, sue_str)
    sue_plan = planunit_shop(sue_str, a23_str)
    assert os_path_exists(sue_gut_path) is False

    # WHEN
    save_gut_file(vow_mstr_dir, sue_plan)

    # THEN
    assert os_path_exists(sue_gut_path)


def test_gut_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    sue_plan = planunit_shop(sue_str, a23_str)
    assert gut_file_exists(vow_mstr_dir, a23_str, sue_str) is False

    # WHEN
    save_gut_file(vow_mstr_dir, sue_plan)

    # THEN
    assert gut_file_exists(vow_mstr_dir, a23_str, sue_str)


def test_open_gut_file_ReturnsObj_Scenario0_noFile():
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    sue_gut_path = create_gut_path(vow_mstr_dir, a23_str, sue_str)
    assert os_path_exists(sue_gut_path) is False

    # WHEN / THEN
    assert not open_gut_file(vow_mstr_dir, a23_str, sue_str)


def test_open_gut_file_ReturnsObj_Scenario1_FileExists():
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    sue_gut_path = create_gut_path(vow_mstr_dir, a23_str, sue_str)
    sue_plan = planunit_shop(sue_str, a23_str)
    save_gut_file(vow_mstr_dir, sue_plan)
    assert os_path_exists(sue_gut_path)

    # WHEN / THEN
    assert sue_plan == open_gut_file(vow_mstr_dir, a23_str, sue_str)


def test_save_job_file_SetsFile(env_dir_setup_cleanup):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    sue_job_path = create_job_path(vow_mstr_dir, a23_str, sue_str)
    sue_plan = planunit_shop(sue_str, a23_str)
    assert os_path_exists(sue_job_path) is False

    # WHEN
    save_job_file(vow_mstr_dir, sue_plan)

    # THEN
    assert os_path_exists(sue_job_path)


def test_job_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    sue_plan = planunit_shop(sue_str, a23_str)
    assert job_file_exists(vow_mstr_dir, a23_str, sue_str) is False

    # WHEN
    save_job_file(vow_mstr_dir, sue_plan)

    # THEN
    assert job_file_exists(vow_mstr_dir, a23_str, sue_str)


def test_open_job_file_ReturnsObj_Scenario0_noFile():
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    sue_job_path = create_job_path(vow_mstr_dir, a23_str, sue_str)
    assert os_path_exists(sue_job_path) is False

    # WHEN / THEN
    assert not open_job_file(vow_mstr_dir, a23_str, sue_str)


def test_open_job_file_ReturnsObj_Scenario1_FileExists():
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    sue_job_path = create_job_path(vow_mstr_dir, a23_str, sue_str)
    sue_plan = planunit_shop(sue_str, a23_str)
    save_job_file(vow_mstr_dir, sue_plan)
    assert os_path_exists(sue_job_path)

    # WHEN / THEN
    assert sue_plan == open_job_file(vow_mstr_dir, a23_str, sue_str)


def test_save_arbitrary_planevent_SetsFile_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    event5 = 5
    sue_str = "Sue"
    planevent_path = create_planevent_path(vow_mstr_dir, a23_str, sue_str, event5)
    assert os_path_exists(planevent_path) is False

    # WHEN
    save_arbitrary_planevent(vow_mstr_dir, a23_str, sue_str, event5)

    # THEN
    assert os_path_exists(planevent_path)
    expected_sue_plan = planunit_shop(sue_str, a23_str)
    assert open_plan_file(planevent_path).get_dict() == expected_sue_plan.get_dict()


def test_save_arbitrary_planevent_SetsFile_Scenario1_includes_facts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    event5 = 5
    sue_str = "Sue"
    planevent_path = create_planevent_path(vow_mstr_dir, a23_str, sue_str, event5)
    casa_rope = create_rope(a23_str, "casa")
    clean_rope = create_rope(casa_rope, "clean")
    clean_fopen = 11
    clean_fnigh = 16
    x_facts = [(casa_rope, clean_rope, clean_fopen, clean_fnigh)]
    assert os_path_exists(planevent_path) is False

    # WHEN
    save_arbitrary_planevent(vow_mstr_dir, a23_str, sue_str, event5, facts=x_facts)

    # THEN
    assert os_path_exists(planevent_path)
    expected_sue_plan = planunit_shop(sue_str, a23_str)
    expected_sue_plan.add_fact(casa_rope, clean_rope, clean_fopen, clean_fnigh, True)
    gen_sue_plan = open_plan_file(planevent_path)
    assert gen_sue_plan.get_factunits_dict() == expected_sue_plan.get_factunits_dict()
    assert gen_sue_plan.get_dict() == expected_sue_plan.get_dict()


def test_get_planevent_obj_ReturnsObj_Scenario0_NoFile(env_dir_setup_cleanup):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord"
    sue_str = "Sue"
    t3 = 3

    # WHEN / THEN
    assert get_planevent_obj(vow_mstr_dir, a23_str, sue_str, t3) is None


def test_get_planevent_obj_ReturnsObj_Scenario1_FileExists(env_dir_setup_cleanup):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord"
    sue_str = "Sue"
    t3 = 3
    t3_json_path = create_planevent_path(vow_mstr_dir, a23_str, sue_str, t3)
    sue_plan = planunit_shop(sue_str, a23_str)
    casa_rope = sue_plan.make_l1_rope("case")
    clean_rope = sue_plan.make_l1_rope("clean")
    dirty_rope = sue_plan.make_l1_rope("dirty")
    sue_plan.add_fact(casa_rope, dirty_rope, create_missing_concepts=True)
    save_plan_file(t3_json_path, None, sue_plan)

    # WHEN
    gen_a3_planevent = get_planevent_obj(vow_mstr_dir, a23_str, sue_str, t3)

    # THEN
    assert gen_a3_planevent == sue_plan


def test_collect_owner_event_dir_sets_ReturnsObj_Scenario0_none(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    # WHEN
    owner_events_sets = collect_owner_event_dir_sets(vow_mstr_dir, a23_str)
    # THEN
    assert owner_events_sets == {}


def test_collect_owner_event_dir_sets_ReturnsObj_Scenario1_DirsExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    bob_str = "Bob"
    event1 = 1
    event2 = 2
    bob1_dir = create_owner_event_dir_path(vow_mstr_dir, a23_str, bob_str, event1)
    bob2_dir = create_owner_event_dir_path(vow_mstr_dir, a23_str, bob_str, event2)
    print(f"  {bob1_dir=}")
    print(f"  {bob2_dir=}")
    set_dir(bob1_dir)
    set_dir(bob2_dir)

    # WHEN
    owner_events_sets = collect_owner_event_dir_sets(vow_mstr_dir, a23_str)

    # THEN
    assert owner_events_sets == {bob_str: {event1, event2}}


def test_collect_owner_event_dir_sets_ReturnsObj_Scenario2_DirsExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    bob_str = "Bob"
    sue_str = "Sue"
    event1 = 1
    event2 = 2
    event7 = 7
    bob1_dir = create_owner_event_dir_path(vow_mstr_dir, a23_str, bob_str, event1)
    bob2_dir = create_owner_event_dir_path(vow_mstr_dir, a23_str, bob_str, event2)
    sue2_dir = create_owner_event_dir_path(vow_mstr_dir, a23_str, sue_str, event2)
    sue7_dir = create_owner_event_dir_path(vow_mstr_dir, a23_str, sue_str, event7)
    set_dir(bob1_dir)
    set_dir(bob2_dir)
    set_dir(sue2_dir)
    set_dir(sue7_dir)

    # WHEN
    owner_events_sets = collect_owner_event_dir_sets(vow_mstr_dir, a23_str)

    # THEN
    assert owner_events_sets == {bob_str: {event1, event2}, sue_str: {event2, event7}}


def test_get_owners_downhill_event_ints_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    event2 = 2
    owner_events_sets = {}
    downhill_event_int = event2
    downhill_owners = {bob_str, sue_str}

    # WHEN
    owners_downhill_event_ints = get_owners_downhill_event_ints(
        owner_events_sets, downhill_owners, downhill_event_int
    )

    # THEN
    assert owners_downhill_event_ints == {}


def test_get_owners_downhill_event_ints_ReturnsObj_Scenario1_simple():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    event1 = 1
    event2 = 2
    event7 = 7
    owner_events_sets = {bob_str: {event1, event2}, sue_str: {event2, event7}}
    downhill_event_int = event2
    downhill_owners = {bob_str, sue_str}

    # WHEN
    owners_downhill_event_ints = get_owners_downhill_event_ints(
        owner_events_sets, downhill_owners, downhill_event_int
    )

    # THEN
    assert owners_downhill_event_ints == {bob_str: event2, sue_str: event2}


def test_get_owners_downhill_event_ints_ReturnsObj_Scenario2Empty_downhill_event_int():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event2 = 2
    event7 = 7
    owner_events_sets = {
        bob_str: {event1, event2},
        sue_str: {event2, event7},
        yao_str: {event1, event2, event7},
    }
    downhill_owners = {bob_str, sue_str}

    # WHEN
    owners_downhill_event_ints = get_owners_downhill_event_ints(
        owner_events_sets, downhill_owners
    )

    # THEN
    assert owners_downhill_event_ints == {bob_str: event2, sue_str: event7}


def test_get_owners_downhill_event_ints_ReturnsObj_Scenario3Empty_downhill_owners():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event2 = 2
    event7 = 7
    owner_events_sets = {
        bob_str: {event1, event2},
        sue_str: {event2, event7},
        yao_str: {event1, event2, event7},
    }

    # WHEN
    owners_downhill_event_ints = get_owners_downhill_event_ints(owner_events_sets)

    # THEN
    assert owners_downhill_event_ints == {
        bob_str: event2,
        sue_str: event7,
        yao_str: event7,
    }


def test_get_owners_downhill_event_ints_ReturnsObj_Scenario4Empty_downhill_owners_Withdownhill_event_int():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event2 = 2
    event7 = 7
    owner_events_sets = {
        bob_str: {event1, event2},
        sue_str: {event2, event7},
        yao_str: {event7},
    }
    downhill_event_int = 2

    # WHEN
    owners_downhill_event_ints = get_owners_downhill_event_ints(
        owner_events_sets, ref_event_int=downhill_event_int
    )

    # THEN
    assert owners_downhill_event_ints == {bob_str: event2, sue_str: event2}


def test_cellunit_add_json_file_SetsFile_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    time7 = 777000
    sue_str = "Sue"
    sue7_cell_path = node_path(vow_mstr_dir, a23_str, sue_str, time7)
    event3 = 3
    das = []
    quota500 = 500
    celldepth4 = 4
    penny6 = 6
    assert os_path_exists(sue7_cell_path) is False

    # WHEN
    cellunit_add_json_file(
        vow_mstr_dir=vow_mstr_dir,
        vow_label=a23_str,
        time_owner_name=sue_str,
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
    assert generated_cell_dict.get(bud_owner_name_str()) == sue_str
    assert generated_cell_dict.get(penny_str()) == penny6
    assert generated_cell_dict.get(quota_str()) == quota500


def test_cellunit_add_json_file_SetsFile_Scenario1_ManyParametersEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    time7 = 777000
    sue_str = "Sue"
    bob_str = "Bob"
    das = [bob_str, sue_str]
    sue7_cell_path = node_path(vow_mstr_dir, a23_str, sue_str, time7, das)
    event3 = 3
    assert os_path_exists(sue7_cell_path) is False

    # WHEN
    cellunit_add_json_file(
        vow_mstr_dir, a23_str, sue_str, time7, event3, bud_ancestors=das
    )

    # THEN
    print(f"{sue7_cell_path=}")
    assert os_path_exists(sue7_cell_path)
    generated_cell_dict = open_json(sue7_cell_path)
    assert generated_cell_dict.get(ancestors_str()) == das
    assert generated_cell_dict.get(event_int_str()) == event3
    assert generated_cell_dict.get(celldepth_str()) == 0
    assert generated_cell_dict.get(bud_owner_name_str()) == sue_str
    assert generated_cell_dict.get(penny_str()) == 1
    assert generated_cell_dict.get(quota_str()) == CELLNODE_QUOTA_DEFAULT


def test_cellunit_get_from_dir_ReturnsObj_Scenario0_NoFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    time7 = 777000
    sue_str = "Sue"
    bob_str = "Bob"
    das = [bob_str, sue_str]
    sue7_cell_path = node_path(vow_mstr_dir, a23_str, sue_str, time7, das)
    event3 = 3
    assert os_path_exists(sue7_cell_path) is False
    cell_dir = create_cell_dir_path(
        vow_mstr_dir, a23_str, sue_str, time7, bud_ancestors=das
    )

    # WHEN / THEN
    assert cellunit_get_from_dir(cell_dir) is None


def test_cellunit_get_from_dir_ReturnsObj_Scenario1_FileExists(env_dir_setup_cleanup):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    time7 = 777000
    sue_str = "Sue"
    bob_str = "Bob"
    das = [bob_str, sue_str]
    sue7_cell_path = node_path(vow_mstr_dir, a23_str, sue_str, time7, das)
    event3 = 3
    assert os_path_exists(sue7_cell_path) is False
    cellunit_add_json_file(
        vow_mstr_dir, a23_str, sue_str, time7, event3, bud_ancestors=das
    )
    cell_dir = create_cell_dir_path(
        vow_mstr_dir, a23_str, sue_str, time7, bud_ancestors=das
    )

    # WHEN
    gen_cellunit = cellunit_get_from_dir(cell_dir)

    # THEN
    expected_cellunit = cellunit_shop(sue_str, ancestors=das, event_int=event3)
    assert gen_cellunit == expected_cellunit


def test_cellunit_save_to_dir_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    time7 = 777000
    sue_str = "Sue"
    bob_str = "Bob"
    das = [bob_str, sue_str]
    sue7_cell_path = node_path(vow_mstr_dir, a23_str, sue_str, time7, das)
    event3 = 3
    sue_cell = cellunit_shop(sue_str, ancestors=das, event_int=event3)
    cell_dir = create_cell_dir_path(vow_mstr_dir, a23_str, sue_str, time7, das)
    assert os_path_exists(sue7_cell_path) is False

    # WHEN
    cellunit_save_to_dir(cell_dir, sue_cell)

    # THEN
    assert os_path_exists(sue7_cell_path)
    assert cellunit_get_from_dir(cell_dir) == sue_cell


def test_create_cell_acct_mandate_ledger_json_CreatesFile_Scenario0_NoCellFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    sue_str = "Sue"
    sue_ancestors = [sue_str]
    a23_str = "accord23"
    bob_str = "Bob"
    tp6 = 6
    sue_acct_mandate_ledger_path = create_cell_acct_mandate_ledger_path(
        mstr_dir, a23_str, bob_str, tp6, sue_ancestors
    )
    sue_cell_dir = create_cell_dir_path(mstr_dir, a23_str, bob_str, tp6, sue_ancestors)
    assert os_path_exists(sue_acct_mandate_ledger_path) is False

    # WHEN
    create_cell_acct_mandate_ledger_json(sue_cell_dir)

    # THEN
    assert os_path_exists(sue_acct_mandate_ledger_path) is False


def test_create_cell_acct_mandate_ledger_json_CreatesFile_Scenario1(
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
    a23_str = "accord23"
    sue_plan = planunit_shop(sue_str, a23_str)
    sue_plan.add_acctunit(sue_str, 3, 5)
    sue_plan.add_acctunit(yao_str, 7, 2)
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sue_plan.add_concept(clean_fact.fstate)
    sue_plan.add_concept(dirty_fact.fstate)
    casa_rope = sue_plan.make_l1_rope("casa")
    mop_rope = sue_plan.make_rope(casa_rope, "mop")
    sue_plan.add_concept(mop_rope, 1, task=True)
    sue_plan.edit_reason(mop_rope, dirty_fact.fcontext, dirty_fact.fstate)
    sue_plan.add_fact(
        dirty_fact.fcontext, dirty_fact.fstate, create_missing_concepts=True
    )
    sky_blue_fact = sky_blue_factunit()
    sue_planevent_factunits = {clean_fact.fcontext: clean_fact}
    sue_found_factunits = {dirty_fact.fcontext: dirty_fact}
    sue_boss_factunits = {sky_blue_fact.fcontext: sky_blue_fact}
    sue_cell = cellunit_shop(
        bud_owner_name=yao_str,
        ancestors=sue_ancestors,
        event_int=sue_event7,
        celldepth=sue_celldepth3,
        penny=sue_penny2,
        quota=sue_quota300,
        planadjust=sue_plan,
        planevent_facts=sue_planevent_factunits,
        found_facts=sue_found_factunits,
        boss_facts=sue_boss_factunits,
        mandate=sue_mandate,
    )
    sue_cell._reason_rcontexts = set()
    bob_str = "Bob"
    tp6 = 6
    sue_acct_mandate_ledger_path = create_cell_acct_mandate_ledger_path(
        mstr_dir, a23_str, bob_str, tp6, sue_ancestors
    )
    sue_cell_dir = create_cell_dir_path(mstr_dir, a23_str, bob_str, tp6, sue_ancestors)
    cellunit_save_to_dir(sue_cell_dir, sue_cell)
    assert os_path_exists(sue_acct_mandate_ledger_path) is False

    # WHEN
    create_cell_acct_mandate_ledger_json(sue_cell_dir)

    # THEN
    assert os_path_exists(sue_acct_mandate_ledger_path)
    assert open_json(sue_acct_mandate_ledger_path) == {yao_str: 311, sue_str: 133}


def test_save_valid_bud_file_Scenario0_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
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
    a23_str = "accord23"
    yao_str = "Yao"
    invalid_bud = get_budunit_invalid_example()

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        save_bud_file(mstr_dir, a23_str, yao_str, invalid_bud)
    exception_str = (
        "magnitude cannot be calculated: debt_bud_acct_net=-5, cred_bud_acct_net=3"
    )
    assert str(excinfo.value) == exception_str


def test_bud_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
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
    a23_str = "accord23"
    yao_str = "Yao"
    t55_bud = get_budunit_55_example()
    t55_bud_time = t55_bud.bud_time
    assert not bud_file_exists(mstr_dir, a23_str, yao_str, t55_bud_time)

    # WHEN / THEN
    assert not open_bud_file(mstr_dir, a23_str, yao_str, t55_bud_time)


def test_open_bud_file_ReturnsObj_Scenario1_FileExists(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    yao_str = "Yao"
    t55_bud = get_budunit_55_example()
    t55_bud_time = t55_bud.bud_time
    save_bud_file(mstr_dir, a23_str, yao_str, t55_bud)
    assert bud_file_exists(mstr_dir, a23_str, yao_str, t55_bud_time)

    # WHEN / THEN
    assert open_bud_file(mstr_dir, a23_str, yao_str, t55_bud_time) == t55_bud


def test_save_planpoint_file_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    t55_planpoint = get_planunit_with_4_levels()
    t55_bud_time = 55
    t55_planpoint_path = create_planpoint_path(mstr_dir, a23_str, sue_str, t55_bud_time)
    print(f"{t55_planpoint.vow_label=}")
    print(f"               {mstr_dir=}")
    print(f"      {t55_planpoint_path=}")
    assert os_path_exists(t55_planpoint_path) is False

    # WHEN
    save_planpoint_file(mstr_dir, t55_planpoint, t55_bud_time)

    # THEN
    assert os_path_exists(t55_planpoint_path)


def test_save_planpoint_file_RaisesError(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    irrational_planpoint = get_planunit_irrational_example()
    t55_bud_time = 55

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        save_planpoint_file(mstr_dir, irrational_planpoint, t55_bud_time)
    exception_str = "PlanPoint could not be saved PlanUnit._rational is False"
    assert str(excinfo.value) == exception_str


def test_planpoint_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    t55_bud_time = 55
    assert planpoint_file_exists(mstr_dir, a23_str, sue_str, t55_bud_time) is False

    # WHEN
    t55_planpoint = get_planunit_with_4_levels()
    save_planpoint_file(mstr_dir, t55_planpoint, t55_bud_time)

    # THEN
    assert planpoint_file_exists(mstr_dir, a23_str, sue_str, t55_bud_time)


def test_open_planpoint_file_ReturnsObj_Scenario0_NoFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    t55_bud_time = 55
    assert not planpoint_file_exists(mstr_dir, a23_str, sue_str, t55_bud_time)

    # WHEN / THEN
    assert not open_planpoint_file(mstr_dir, a23_str, sue_str, t55_bud_time)


def test_open_planpoint_file_ReturnsObj_Scenario1_FileExists(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    t55_bud_time = 55
    t55_planpoint = get_planunit_with_4_levels()
    save_planpoint_file(mstr_dir, t55_planpoint, t55_bud_time)
    assert planpoint_file_exists(mstr_dir, a23_str, sue_str, t55_bud_time)

    # WHEN
    file_planpoint = open_planpoint_file(mstr_dir, a23_str, sue_str, t55_bud_time)

    # THEN
    assert file_planpoint.get_dict() == t55_planpoint.get_dict()


def test_get_timepoint_dirs_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    t55_bud_time = 55
    t77_bud_time = 77
    planpoint = get_planunit_with_4_levels()
    save_planpoint_file(mstr_dir, planpoint, t55_bud_time)
    save_planpoint_file(mstr_dir, planpoint, t77_bud_time)

    # WHEN
    timepoint_dirs = get_timepoint_dirs(mstr_dir, a23_str, sue_str)

    # THEN
    assert timepoint_dirs == [t55_bud_time, t77_bud_time]
