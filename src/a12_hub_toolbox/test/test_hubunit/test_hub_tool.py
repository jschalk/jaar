from os.path import exists as os_path_exists
from pytest import raises as pytest_raises
from src.a00_data_toolbox.file_toolbox import create_path, open_json, set_dir
from src.a01_term_logic.rope import create_rope
from src.a06_believer_logic.believer import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import penny_str
from src.a06_believer_logic.test._util.example_believers import (
    get_believerunit_irrational_example,
    get_believerunit_with_4_levels,
)
from src.a09_pack_logic.test._util.a09_str import event_int_str
from src.a11_bud_logic.cell import CELLNODE_QUOTA_DEFAULT, cellunit_shop
from src.a11_bud_logic.test._util.a11_str import (
    ancestors_str,
    bud_believer_name_str,
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
    create_believer_event_dir_path,
    create_believerevent_path,
    create_believerpoint_path,
    create_budunit_json_path,
    create_cell_dir_path,
    create_cell_json_path as node_path,
    create_cell_partner_mandate_ledger_path,
    create_gut_path,
    create_job_path,
)
from src.a12_hub_toolbox.hub_tool import (
    believerpoint_file_exists,
    bud_file_exists,
    cellunit_add_json_file,
    cellunit_get_from_dir,
    cellunit_save_to_dir,
    collect_believer_event_dir_sets,
    create_cell_partner_mandate_ledger_json,
    get_believerevent_obj,
    get_believers_downhill_event_ints,
    get_timepoint_dirs,
    gut_file_exists,
    job_file_exists,
    open_believer_file,
    open_believerpoint_file,
    open_bud_file,
    open_gut_file,
    open_job_file,
    save_arbitrary_believerevent,
    save_believer_file,
    save_believerpoint_file,
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


def test_save_believer_file_SetsFile(env_dir_setup_cleanup):
    # ESTABLISH
    temp_dir = get_module_temp_dir()
    believer_filename = "believer.json"
    believer_path = create_path(temp_dir, believer_filename)
    sue_str = "Sue"
    sue_believer = believerunit_shop(sue_str)
    assert os_path_exists(believer_path) is False

    # WHEN
    save_believer_file(believer_path, None, sue_believer)

    # THEN
    assert os_path_exists(believer_path)


def test_open_believer_file_ReturnsObj_Scenario0_NoFile():
    # ESTABLISH
    temp_dir = get_module_temp_dir()
    believer_filename = "believer.json"
    believer_path = create_path(temp_dir, believer_filename)
    assert os_path_exists(believer_path) is False

    # WHEN
    gen_sue_believer = open_believer_file(believer_path)

    # THEN
    assert not gen_sue_believer


def test_open_believer_file_ReturnsObj_Scenario1_FileExists():
    # ESTABLISH
    temp_dir = get_module_temp_dir()
    believer_filename = "believer.json"
    believer_path = create_path(temp_dir, believer_filename)
    sue_str = "Sue"
    expected_sue_believer = believerunit_shop(sue_str)
    save_believer_file(believer_path, None, expected_sue_believer)
    assert os_path_exists(believer_path)

    # WHEN
    gen_sue_believer = open_believer_file(believer_path)

    # THEN
    assert gen_sue_believer == expected_sue_believer


def test_save_gut_file_SetsFile(env_dir_setup_cleanup):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    sue_gut_path = create_gut_path(belief_mstr_dir, a23_str, sue_str)
    sue_believer = believerunit_shop(sue_str, a23_str)
    assert os_path_exists(sue_gut_path) is False

    # WHEN
    save_gut_file(belief_mstr_dir, sue_believer)

    # THEN
    assert os_path_exists(sue_gut_path)


def test_gut_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    sue_believer = believerunit_shop(sue_str, a23_str)
    assert gut_file_exists(belief_mstr_dir, a23_str, sue_str) is False

    # WHEN
    save_gut_file(belief_mstr_dir, sue_believer)

    # THEN
    assert gut_file_exists(belief_mstr_dir, a23_str, sue_str)


def test_open_gut_file_ReturnsObj_Scenario0_noFile():
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    sue_gut_path = create_gut_path(belief_mstr_dir, a23_str, sue_str)
    assert os_path_exists(sue_gut_path) is False

    # WHEN / THEN
    assert not open_gut_file(belief_mstr_dir, a23_str, sue_str)


def test_open_gut_file_ReturnsObj_Scenario1_FileExists():
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    sue_gut_path = create_gut_path(belief_mstr_dir, a23_str, sue_str)
    sue_believer = believerunit_shop(sue_str, a23_str)
    save_gut_file(belief_mstr_dir, sue_believer)
    assert os_path_exists(sue_gut_path)

    # WHEN / THEN
    assert sue_believer == open_gut_file(belief_mstr_dir, a23_str, sue_str)


def test_save_job_file_SetsFile(env_dir_setup_cleanup):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    sue_job_path = create_job_path(belief_mstr_dir, a23_str, sue_str)
    sue_believer = believerunit_shop(sue_str, a23_str)
    assert os_path_exists(sue_job_path) is False

    # WHEN
    save_job_file(belief_mstr_dir, sue_believer)

    # THEN
    assert os_path_exists(sue_job_path)


def test_job_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    sue_believer = believerunit_shop(sue_str, a23_str)
    assert job_file_exists(belief_mstr_dir, a23_str, sue_str) is False

    # WHEN
    save_job_file(belief_mstr_dir, sue_believer)

    # THEN
    assert job_file_exists(belief_mstr_dir, a23_str, sue_str)


def test_open_job_file_ReturnsObj_Scenario0_noFile():
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    sue_job_path = create_job_path(belief_mstr_dir, a23_str, sue_str)
    assert os_path_exists(sue_job_path) is False

    # WHEN / THEN
    assert not open_job_file(belief_mstr_dir, a23_str, sue_str)


def test_open_job_file_ReturnsObj_Scenario1_FileExists():
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    sue_job_path = create_job_path(belief_mstr_dir, a23_str, sue_str)
    sue_believer = believerunit_shop(sue_str, a23_str)
    save_job_file(belief_mstr_dir, sue_believer)
    assert os_path_exists(sue_job_path)

    # WHEN / THEN
    assert sue_believer == open_job_file(belief_mstr_dir, a23_str, sue_str)


def test_save_arbitrary_believerevent_SetsFile_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    event5 = 5
    sue_str = "Sue"
    believerevent_path = create_believerevent_path(
        belief_mstr_dir, a23_str, sue_str, event5
    )
    assert os_path_exists(believerevent_path) is False

    # WHEN
    save_arbitrary_believerevent(belief_mstr_dir, a23_str, sue_str, event5)

    # THEN
    assert os_path_exists(believerevent_path)
    expected_sue_believer = believerunit_shop(sue_str, a23_str)
    assert (
        open_believer_file(believerevent_path).get_dict()
        == expected_sue_believer.get_dict()
    )


def test_save_arbitrary_believerevent_SetsFile_Scenario1_includes_facts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    event5 = 5
    sue_str = "Sue"
    believerevent_path = create_believerevent_path(
        belief_mstr_dir, a23_str, sue_str, event5
    )
    casa_rope = create_rope(a23_str, "casa")
    clean_rope = create_rope(casa_rope, "clean")
    clean_f_lower = 11
    clean_f_upper = 16
    x_facts = [(casa_rope, clean_rope, clean_f_lower, clean_f_upper)]
    assert os_path_exists(believerevent_path) is False

    # WHEN
    save_arbitrary_believerevent(
        belief_mstr_dir, a23_str, sue_str, event5, facts=x_facts
    )

    # THEN
    assert os_path_exists(believerevent_path)
    expected_sue_believer = believerunit_shop(sue_str, a23_str)
    expected_sue_believer.add_fact(
        casa_rope, clean_rope, clean_f_lower, clean_f_upper, True
    )
    gen_sue_believer = open_believer_file(believerevent_path)
    assert (
        gen_sue_believer.get_factunits_dict()
        == expected_sue_believer.get_factunits_dict()
    )
    assert gen_sue_believer.get_dict() == expected_sue_believer.get_dict()


def test_get_believerevent_obj_ReturnsObj_Scenario0_NoFile(env_dir_setup_cleanup):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy"
    sue_str = "Sue"
    t3 = 3

    # WHEN / THEN
    assert get_believerevent_obj(belief_mstr_dir, a23_str, sue_str, t3) is None


def test_get_believerevent_obj_ReturnsObj_Scenario1_FileExists(env_dir_setup_cleanup):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy"
    sue_str = "Sue"
    t3 = 3
    t3_json_path = create_believerevent_path(belief_mstr_dir, a23_str, sue_str, t3)
    sue_believer = believerunit_shop(sue_str, a23_str)
    casa_rope = sue_believer.make_l1_rope("casa")
    clean_rope = sue_believer.make_l1_rope("clean")
    dirty_rope = sue_believer.make_l1_rope("dirty")
    sue_believer.add_fact(casa_rope, dirty_rope, create_missing_plans=True)
    save_believer_file(t3_json_path, None, sue_believer)

    # WHEN
    gen_a3_believerevent = get_believerevent_obj(belief_mstr_dir, a23_str, sue_str, t3)

    # THEN
    assert gen_a3_believerevent == sue_believer


def test_collect_believer_event_dir_sets_ReturnsObj_Scenario0_none(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    # WHEN
    believer_events_sets = collect_believer_event_dir_sets(belief_mstr_dir, a23_str)
    # THEN
    assert believer_events_sets == {}


def test_collect_believer_event_dir_sets_ReturnsObj_Scenario1_DirsExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    bob_str = "Bob"
    event1 = 1
    event2 = 2
    bob1_dir = create_believer_event_dir_path(belief_mstr_dir, a23_str, bob_str, event1)
    bob2_dir = create_believer_event_dir_path(belief_mstr_dir, a23_str, bob_str, event2)
    print(f"  {bob1_dir=}")
    print(f"  {bob2_dir=}")
    set_dir(bob1_dir)
    set_dir(bob2_dir)

    # WHEN
    believer_events_sets = collect_believer_event_dir_sets(belief_mstr_dir, a23_str)

    # THEN
    assert believer_events_sets == {bob_str: {event1, event2}}


def test_collect_believer_event_dir_sets_ReturnsObj_Scenario2_DirsExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    bob_str = "Bob"
    sue_str = "Sue"
    event1 = 1
    event2 = 2
    event7 = 7
    bob1_dir = create_believer_event_dir_path(belief_mstr_dir, a23_str, bob_str, event1)
    bob2_dir = create_believer_event_dir_path(belief_mstr_dir, a23_str, bob_str, event2)
    sue2_dir = create_believer_event_dir_path(belief_mstr_dir, a23_str, sue_str, event2)
    sue7_dir = create_believer_event_dir_path(belief_mstr_dir, a23_str, sue_str, event7)
    set_dir(bob1_dir)
    set_dir(bob2_dir)
    set_dir(sue2_dir)
    set_dir(sue7_dir)

    # WHEN
    believer_events_sets = collect_believer_event_dir_sets(belief_mstr_dir, a23_str)

    # THEN
    assert believer_events_sets == {
        bob_str: {event1, event2},
        sue_str: {event2, event7},
    }


def test_get_believers_downhill_event_ints_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    event2 = 2
    believer_events_sets = {}
    downhill_event_int = event2
    downhill_believers = {bob_str, sue_str}

    # WHEN
    believers_downhill_event_ints = get_believers_downhill_event_ints(
        believer_events_sets, downhill_believers, downhill_event_int
    )

    # THEN
    assert believers_downhill_event_ints == {}


def test_get_believers_downhill_event_ints_ReturnsObj_Scenario1_simple():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    event1 = 1
    event2 = 2
    event7 = 7
    believer_events_sets = {bob_str: {event1, event2}, sue_str: {event2, event7}}
    downhill_event_int = event2
    downhill_believers = {bob_str, sue_str}

    # WHEN
    believers_downhill_event_ints = get_believers_downhill_event_ints(
        believer_events_sets, downhill_believers, downhill_event_int
    )

    # THEN
    assert believers_downhill_event_ints == {bob_str: event2, sue_str: event2}


def test_get_believers_downhill_event_ints_ReturnsObj_Scenario2Empty_downhill_event_int():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event2 = 2
    event7 = 7
    believer_events_sets = {
        bob_str: {event1, event2},
        sue_str: {event2, event7},
        yao_str: {event1, event2, event7},
    }
    downhill_believers = {bob_str, sue_str}

    # WHEN
    believers_downhill_event_ints = get_believers_downhill_event_ints(
        believer_events_sets, downhill_believers
    )

    # THEN
    assert believers_downhill_event_ints == {bob_str: event2, sue_str: event7}


def test_get_believers_downhill_event_ints_ReturnsObj_Scenario3Empty_downhill_believers():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event2 = 2
    event7 = 7
    believer_events_sets = {
        bob_str: {event1, event2},
        sue_str: {event2, event7},
        yao_str: {event1, event2, event7},
    }

    # WHEN
    believers_downhill_event_ints = get_believers_downhill_event_ints(
        believer_events_sets
    )

    # THEN
    assert believers_downhill_event_ints == {
        bob_str: event2,
        sue_str: event7,
        yao_str: event7,
    }


def test_get_believers_downhill_event_ints_ReturnsObj_Scenario4Empty_downhill_believers_Withdownhill_event_int():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event2 = 2
    event7 = 7
    believer_events_sets = {
        bob_str: {event1, event2},
        sue_str: {event2, event7},
        yao_str: {event7},
    }
    downhill_event_int = 2

    # WHEN
    believers_downhill_event_ints = get_believers_downhill_event_ints(
        believer_events_sets, ref_event_int=downhill_event_int
    )

    # THEN
    assert believers_downhill_event_ints == {bob_str: event2, sue_str: event2}


def test_cellunit_add_json_file_SetsFile_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    time7 = 777000
    sue_str = "Sue"
    sue7_cell_path = node_path(belief_mstr_dir, a23_str, sue_str, time7)
    event3 = 3
    das = []
    quota500 = 500
    celldepth4 = 4
    penny6 = 6
    assert os_path_exists(sue7_cell_path) is False

    # WHEN
    cellunit_add_json_file(
        belief_mstr_dir=belief_mstr_dir,
        belief_label=a23_str,
        time_believer_name=sue_str,
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
    assert generated_cell_dict.get(bud_believer_name_str()) == sue_str
    assert generated_cell_dict.get(penny_str()) == penny6
    assert generated_cell_dict.get(quota_str()) == quota500


def test_cellunit_add_json_file_SetsFile_Scenario1_ManyParametersEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    time7 = 777000
    sue_str = "Sue"
    bob_str = "Bob"
    das = [bob_str, sue_str]
    sue7_cell_path = node_path(belief_mstr_dir, a23_str, sue_str, time7, das)
    event3 = 3
    assert os_path_exists(sue7_cell_path) is False

    # WHEN
    cellunit_add_json_file(
        belief_mstr_dir, a23_str, sue_str, time7, event3, bud_ancestors=das
    )

    # THEN
    print(f"{sue7_cell_path=}")
    assert os_path_exists(sue7_cell_path)
    generated_cell_dict = open_json(sue7_cell_path)
    assert generated_cell_dict.get(ancestors_str()) == das
    assert generated_cell_dict.get(event_int_str()) == event3
    assert generated_cell_dict.get(celldepth_str()) == 0
    assert generated_cell_dict.get(bud_believer_name_str()) == sue_str
    assert generated_cell_dict.get(penny_str()) == 1
    assert generated_cell_dict.get(quota_str()) == CELLNODE_QUOTA_DEFAULT


def test_cellunit_get_from_dir_ReturnsObj_Scenario0_NoFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    time7 = 777000
    sue_str = "Sue"
    bob_str = "Bob"
    das = [bob_str, sue_str]
    sue7_cell_path = node_path(belief_mstr_dir, a23_str, sue_str, time7, das)
    event3 = 3
    assert os_path_exists(sue7_cell_path) is False
    cell_dir = create_cell_dir_path(
        belief_mstr_dir, a23_str, sue_str, time7, bud_ancestors=das
    )

    # WHEN / THEN
    assert cellunit_get_from_dir(cell_dir) is None


def test_cellunit_get_from_dir_ReturnsObj_Scenario1_FileExists(env_dir_setup_cleanup):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    time7 = 777000
    sue_str = "Sue"
    bob_str = "Bob"
    das = [bob_str, sue_str]
    sue7_cell_path = node_path(belief_mstr_dir, a23_str, sue_str, time7, das)
    event3 = 3
    assert os_path_exists(sue7_cell_path) is False
    cellunit_add_json_file(
        belief_mstr_dir, a23_str, sue_str, time7, event3, bud_ancestors=das
    )
    cell_dir = create_cell_dir_path(
        belief_mstr_dir, a23_str, sue_str, time7, bud_ancestors=das
    )

    # WHEN
    gen_cellunit = cellunit_get_from_dir(cell_dir)

    # THEN
    expected_cellunit = cellunit_shop(sue_str, ancestors=das, event_int=event3)
    assert gen_cellunit == expected_cellunit


def test_cellunit_save_to_dir_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    time7 = 777000
    sue_str = "Sue"
    bob_str = "Bob"
    das = [bob_str, sue_str]
    sue7_cell_path = node_path(belief_mstr_dir, a23_str, sue_str, time7, das)
    event3 = 3
    sue_cell = cellunit_shop(sue_str, ancestors=das, event_int=event3)
    cell_dir = create_cell_dir_path(belief_mstr_dir, a23_str, sue_str, time7, das)
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
    sue_believer = believerunit_shop(sue_str, a23_str)
    sue_believer.add_partnerunit(sue_str, 3, 5)
    sue_believer.add_partnerunit(yao_str, 7, 2)
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sue_believer.add_plan(clean_fact.f_state)
    sue_believer.add_plan(dirty_fact.f_state)
    casa_rope = sue_believer.make_l1_rope("casa")
    mop_rope = sue_believer.make_rope(casa_rope, "mop")
    sue_believer.add_plan(mop_rope, 1, task=True)
    sue_believer.edit_reason(mop_rope, dirty_fact.f_context, dirty_fact.f_state)
    sue_believer.add_fact(
        dirty_fact.f_context, dirty_fact.f_state, create_missing_plans=True
    )
    sky_blue_fact = sky_blue_factunit()
    sue_believerevent_factunits = {clean_fact.f_context: clean_fact}
    sue_found_factunits = {dirty_fact.f_context: dirty_fact}
    sue_boss_factunits = {sky_blue_fact.f_context: sky_blue_fact}
    sue_cell = cellunit_shop(
        bud_believer_name=yao_str,
        ancestors=sue_ancestors,
        event_int=sue_event7,
        celldepth=sue_celldepth3,
        penny=sue_penny2,
        quota=sue_quota300,
        believeradjust=sue_believer,
        believerevent_facts=sue_believerevent_factunits,
        found_facts=sue_found_factunits,
        boss_facts=sue_boss_factunits,
        mandate=sue_mandate,
    )
    sue_cell._reason_r_contexts = set()
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


def test_save_believerpoint_file_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    t55_believerpoint = get_believerunit_with_4_levels()
    t55_bud_time = 55
    t55_believerpoint_path = create_believerpoint_path(
        mstr_dir, a23_str, sue_str, t55_bud_time
    )
    print(f"{t55_believerpoint.belief_label=}")
    print(f"               {mstr_dir=}")
    print(f"      {t55_believerpoint_path=}")
    assert os_path_exists(t55_believerpoint_path) is False

    # WHEN
    save_believerpoint_file(mstr_dir, t55_believerpoint, t55_bud_time)

    # THEN
    assert os_path_exists(t55_believerpoint_path)


def test_save_believerpoint_file_RaisesError(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    irrational_believerpoint = get_believerunit_irrational_example()
    t55_bud_time = 55

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        save_believerpoint_file(mstr_dir, irrational_believerpoint, t55_bud_time)
    exception_str = "BelieverPoint could not be saved BelieverUnit._rational is False"
    assert str(excinfo.value) == exception_str


def test_believerpoint_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    t55_bud_time = 55
    assert believerpoint_file_exists(mstr_dir, a23_str, sue_str, t55_bud_time) is False

    # WHEN
    t55_believerpoint = get_believerunit_with_4_levels()
    save_believerpoint_file(mstr_dir, t55_believerpoint, t55_bud_time)

    # THEN
    assert believerpoint_file_exists(mstr_dir, a23_str, sue_str, t55_bud_time)


def test_open_believerpoint_file_ReturnsObj_Scenario0_NoFileExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    t55_bud_time = 55
    assert not believerpoint_file_exists(mstr_dir, a23_str, sue_str, t55_bud_time)

    # WHEN / THEN
    assert not open_believerpoint_file(mstr_dir, a23_str, sue_str, t55_bud_time)


def test_open_believerpoint_file_ReturnsObj_Scenario1_FileExists(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    t55_bud_time = 55
    t55_believerpoint = get_believerunit_with_4_levels()
    save_believerpoint_file(mstr_dir, t55_believerpoint, t55_bud_time)
    assert believerpoint_file_exists(mstr_dir, a23_str, sue_str, t55_bud_time)

    # WHEN
    file_believerpoint = open_believerpoint_file(
        mstr_dir, a23_str, sue_str, t55_bud_time
    )

    # THEN
    assert file_believerpoint.get_dict() == t55_believerpoint.get_dict()


def test_get_timepoint_dirs_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    t55_bud_time = 55
    t77_bud_time = 77
    believerpoint = get_believerunit_with_4_levels()
    save_believerpoint_file(mstr_dir, believerpoint, t55_bud_time)
    save_believerpoint_file(mstr_dir, believerpoint, t77_bud_time)

    # WHEN
    timepoint_dirs = get_timepoint_dirs(mstr_dir, a23_str, sue_str)

    # THEN
    assert timepoint_dirs == [t55_bud_time, t77_bud_time]
