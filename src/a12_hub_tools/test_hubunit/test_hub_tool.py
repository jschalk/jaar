from os.path import exists as os_path_exists
from pytest import raises as pytest_raises
from src.a00_data_toolbox.file_toolbox import create_path, open_json, set_dir
from src.a01_term_logic.way import create_way
from src.a02_finance_logic._test_util.a02_str import quota_str
from src.a06_bud_logic._test_util.a06_str import penny_str
from src.a06_bud_logic._test_util.example_buds import (
    get_budunit_irrational_example,
    get_budunit_with_4_levels,
)
from src.a06_bud_logic.bud import budunit_shop
from src.a09_pack_logic._test_util.a09_str import event_int_str
from src.a11_deal_cell_logic._test_util.a11_str import (
    ancestors_str,
    celldepth_str,
    deal_owner_name_str,
)
from src.a11_deal_cell_logic._test_util.example_factunits import (
    example_casa_clean_factunit as clean_factunit,
)
from src.a11_deal_cell_logic._test_util.example_factunits import (
    example_casa_dirty_factunit as dirty_factunit,
)
from src.a11_deal_cell_logic._test_util.example_factunits import (
    example_casa_grimy_factunit as grimy_factunit,
)
from src.a11_deal_cell_logic._test_util.example_factunits import (
    example_sky_blue_factunit as sky_blue_factunit,
)
from src.a11_deal_cell_logic.cell import CELLNODE_QUOTA_DEFAULT, cellunit_shop
from src.a12_hub_tools._test_util.a12_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a12_hub_tools._test_util.example_hub_atoms import (
    get_dealunit_55_example,
    get_dealunit_invalid_example,
)
from src.a12_hub_tools.hub_path import (
    create_budevent_path,
    create_budpoint_path,
    create_cell_acct_mandate_ledger_path,
    create_cell_dir_path,
)
from src.a12_hub_tools.hub_path import (
    create_dealunit_json_path,
    create_gut_path,
    create_job_path,
    create_owner_event_dir_path,
)
from src.a12_hub_tools.hub_path import create_cell_json_path as node_path
from src.a12_hub_tools.hub_tool import (
    budpoint_file_exists,
    cellunit_add_json_file,
    cellunit_get_from_dir,
    cellunit_save_to_dir,
    collect_owner_event_dir_sets,
    create_cell_acct_mandate_ledger_json,
    deal_file_exists,
    get_budevent_obj,
    get_owners_downhill_event_ints,
    get_timepoint_dirs,
    gut_file_exists,
    job_file_exists,
    open_bud_file,
    open_budpoint_file,
    open_deal_file,
    open_gut_file,
    open_job_file,
    save_arbitrary_budevent,
    save_bud_file,
    save_budpoint_file,
    save_deal_file,
    save_gut_file,
    save_job_file,
)


def test_save_bud_file_SetsFile(env_dir_setup_cleanup):
    # ESTABLISH
    temp_dir = get_module_temp_dir()
    bud_filename = "bud.json"
    bud_path = create_path(temp_dir, bud_filename)
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    assert os_path_exists(bud_path) is False

    # WHEN
    save_bud_file(bud_path, None, sue_bud)

    # THEN
    assert os_path_exists(bud_path)


def test_open_bud_file_ReturnsObj_Scenario0_NoFile():
    # ESTABLISH
    temp_dir = get_module_temp_dir()
    bud_filename = "bud.json"
    bud_path = create_path(temp_dir, bud_filename)
    assert os_path_exists(bud_path) is False

    # WHEN
    gen_sue_bud = open_bud_file(bud_path)

    # THEN
    assert not gen_sue_bud


def test_open_bud_file_ReturnsObj_Scenario1_FileExists():
    # ESTABLISH
    temp_dir = get_module_temp_dir()
    bud_filename = "bud.json"
    bud_path = create_path(temp_dir, bud_filename)
    sue_str = "Sue"
    expected_sue_bud = budunit_shop(sue_str)
    save_bud_file(bud_path, None, expected_sue_bud)
    assert os_path_exists(bud_path)

    # WHEN
    gen_sue_bud = open_bud_file(bud_path)

    # THEN
    assert gen_sue_bud == expected_sue_bud


def test_save_gut_file_SetsFile(env_dir_setup_cleanup):
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    sue_gut_path = create_gut_path(fisc_mstr_dir, a23_str, sue_str)
    sue_bud = budunit_shop(sue_str, a23_str)
    assert os_path_exists(sue_gut_path) is False

    # WHEN
    save_gut_file(fisc_mstr_dir, sue_bud)

    # THEN
    assert os_path_exists(sue_gut_path)


def test_gut_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str, a23_str)
    assert gut_file_exists(fisc_mstr_dir, a23_str, sue_str) is False

    # WHEN
    save_gut_file(fisc_mstr_dir, sue_bud)

    # THEN
    assert gut_file_exists(fisc_mstr_dir, a23_str, sue_str)


def test_open_gut_file_ReturnsObj_Scenario0_noFile():
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    sue_gut_path = create_gut_path(fisc_mstr_dir, a23_str, sue_str)
    assert os_path_exists(sue_gut_path) is False

    # WHEN / THEN
    assert not open_gut_file(fisc_mstr_dir, a23_str, sue_str)


def test_open_gut_file_ReturnsObj_Scenario1_FileExists():
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    sue_gut_path = create_gut_path(fisc_mstr_dir, a23_str, sue_str)
    sue_bud = budunit_shop(sue_str, a23_str)
    save_gut_file(fisc_mstr_dir, sue_bud)
    assert os_path_exists(sue_gut_path)

    # WHEN / THEN
    assert sue_bud == open_gut_file(fisc_mstr_dir, a23_str, sue_str)


def test_save_job_file_SetsFile(env_dir_setup_cleanup):
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    sue_job_path = create_job_path(fisc_mstr_dir, a23_str, sue_str)
    sue_bud = budunit_shop(sue_str, a23_str)
    assert os_path_exists(sue_job_path) is False

    # WHEN
    save_job_file(fisc_mstr_dir, sue_bud)

    # THEN
    assert os_path_exists(sue_job_path)


def test_job_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str, a23_str)
    assert job_file_exists(fisc_mstr_dir, a23_str, sue_str) is False

    # WHEN
    save_job_file(fisc_mstr_dir, sue_bud)

    # THEN
    assert job_file_exists(fisc_mstr_dir, a23_str, sue_str)


def test_open_job_file_ReturnsObj_Scenario0_noFile():
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    sue_job_path = create_job_path(fisc_mstr_dir, a23_str, sue_str)
    assert os_path_exists(sue_job_path) is False

    # WHEN / THEN
    assert not open_job_file(fisc_mstr_dir, a23_str, sue_str)


def test_open_job_file_ReturnsObj_Scenario1_FileExists():
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    sue_job_path = create_job_path(fisc_mstr_dir, a23_str, sue_str)
    sue_bud = budunit_shop(sue_str, a23_str)
    save_job_file(fisc_mstr_dir, sue_bud)
    assert os_path_exists(sue_job_path)

    # WHEN / THEN
    assert sue_bud == open_job_file(fisc_mstr_dir, a23_str, sue_str)


def test_save_arbitrary_budevent_SetsFile_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    event5 = 5
    sue_str = "Sue"
    budevent_path = create_budevent_path(fisc_mstr_dir, a23_str, sue_str, event5)
    assert os_path_exists(budevent_path) is False

    # WHEN
    save_arbitrary_budevent(fisc_mstr_dir, a23_str, sue_str, event5)

    # THEN
    assert os_path_exists(budevent_path)
    expected_sue_bud = budunit_shop(sue_str, a23_str)
    assert open_bud_file(budevent_path).get_dict() == expected_sue_bud.get_dict()


def test_save_arbitrary_budevent_SetsFile_Scenario1_includes_facts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    event5 = 5
    sue_str = "Sue"
    budevent_path = create_budevent_path(fisc_mstr_dir, a23_str, sue_str, event5)
    casa_way = create_way(a23_str, "casa")
    clean_way = create_way(casa_way, "clean")
    clean_fopen = 11
    clean_fnigh = 16
    x_facts = [(casa_way, clean_way, clean_fopen, clean_fnigh)]
    assert os_path_exists(budevent_path) is False

    # WHEN
    save_arbitrary_budevent(fisc_mstr_dir, a23_str, sue_str, event5, facts=x_facts)

    # THEN
    assert os_path_exists(budevent_path)
    expected_sue_bud = budunit_shop(sue_str, a23_str)
    expected_sue_bud.add_fact(casa_way, clean_way, clean_fopen, clean_fnigh, True)
    gen_sue_bud = open_bud_file(budevent_path)
    assert gen_sue_bud.get_factunits_dict() == expected_sue_bud.get_factunits_dict()
    assert gen_sue_bud.get_dict() == expected_sue_bud.get_dict()


def test_get_budevent_obj_ReturnsObj_Scenario0_NoFile(env_dir_setup_cleanup):
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord"
    sue_str = "Sue"
    t3 = 3

    # WHEN / THEN
    assert get_budevent_obj(fisc_mstr_dir, a23_str, sue_str, t3) is None


def test_get_budevent_obj_ReturnsObj_Scenario1_FileExists(env_dir_setup_cleanup):
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord"
    sue_str = "Sue"
    t3 = 3
    t3_json_path = create_budevent_path(fisc_mstr_dir, a23_str, sue_str, t3)
    sue_bud = budunit_shop(sue_str, a23_str)
    casa_way = sue_bud.make_l1_way("case")
    clean_way = sue_bud.make_l1_way("clean")
    dirty_way = sue_bud.make_l1_way("dirty")
    sue_bud.add_fact(casa_way, dirty_way, create_missing_concepts=True)
    save_bud_file(t3_json_path, None, sue_bud)

    # WHEN
    gen_a3_budevent = get_budevent_obj(fisc_mstr_dir, a23_str, sue_str, t3)

    # THEN
    assert gen_a3_budevent == sue_bud


def test_collect_owner_event_dir_sets_ReturnsObj_Scenario0_none(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    # WHEN
    owner_events_sets = collect_owner_event_dir_sets(fisc_mstr_dir, a23_str)
    # THEN
    assert owner_events_sets == {}


def test_collect_owner_event_dir_sets_ReturnsObj_Scenario1_DirsExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    bob_str = "Bob"
    event1 = 1
    event2 = 2
    bob1_dir = create_owner_event_dir_path(fisc_mstr_dir, a23_str, bob_str, event1)
    bob2_dir = create_owner_event_dir_path(fisc_mstr_dir, a23_str, bob_str, event2)
    print(f"  {bob1_dir=}")
    print(f"  {bob2_dir=}")
    set_dir(bob1_dir)
    set_dir(bob2_dir)

    # WHEN
    owner_events_sets = collect_owner_event_dir_sets(fisc_mstr_dir, a23_str)

    # THEN
    assert owner_events_sets == {bob_str: {event1, event2}}


def test_collect_owner_event_dir_sets_ReturnsObj_Scenario2_DirsExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    bob_str = "Bob"
    sue_str = "Sue"
    event1 = 1
    event2 = 2
    event7 = 7
    bob1_dir = create_owner_event_dir_path(fisc_mstr_dir, a23_str, bob_str, event1)
    bob2_dir = create_owner_event_dir_path(fisc_mstr_dir, a23_str, bob_str, event2)
    sue2_dir = create_owner_event_dir_path(fisc_mstr_dir, a23_str, sue_str, event2)
    sue7_dir = create_owner_event_dir_path(fisc_mstr_dir, a23_str, sue_str, event7)
    set_dir(bob1_dir)
    set_dir(bob2_dir)
    set_dir(sue2_dir)
    set_dir(sue7_dir)

    # WHEN
    owner_events_sets = collect_owner_event_dir_sets(fisc_mstr_dir, a23_str)

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
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    time7 = 777000
    sue_str = "Sue"
    sue7_cell_path = node_path(fisc_mstr_dir, a23_str, sue_str, time7)
    event3 = 3
    das = []
    quota500 = 500
    celldepth4 = 4
    penny6 = 6
    assert os_path_exists(sue7_cell_path) is False

    # WHEN
    cellunit_add_json_file(
        fisc_mstr_dir=fisc_mstr_dir,
        fisc_label=a23_str,
        time_owner_name=sue_str,
        deal_time=time7,
        quota=quota500,
        event_int=event3,
        celldepth=celldepth4,
        penny=penny6,
        deal_ancestors=das,
    )

    # THEN
    print(f"{sue7_cell_path=}")
    assert os_path_exists(sue7_cell_path)
    generated_cell_dict = open_json(sue7_cell_path)
    assert generated_cell_dict.get(ancestors_str()) == das
    assert generated_cell_dict.get(event_int_str()) == event3
    assert generated_cell_dict.get(celldepth_str()) == celldepth4
    assert generated_cell_dict.get(deal_owner_name_str()) == sue_str
    assert generated_cell_dict.get(penny_str()) == penny6
    assert generated_cell_dict.get(quota_str()) == quota500


def test_cellunit_add_json_file_SetsFile_Scenario1_ManyParametersEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    time7 = 777000
    sue_str = "Sue"
    bob_str = "Bob"
    das = [bob_str, sue_str]
    sue7_cell_path = node_path(fisc_mstr_dir, a23_str, sue_str, time7, das)
    event3 = 3
    assert os_path_exists(sue7_cell_path) is False

    # WHEN
    cellunit_add_json_file(
        fisc_mstr_dir, a23_str, sue_str, time7, event3, deal_ancestors=das
    )

    # THEN
    print(f"{sue7_cell_path=}")
    assert os_path_exists(sue7_cell_path)
    generated_cell_dict = open_json(sue7_cell_path)
    assert generated_cell_dict.get(ancestors_str()) == das
    assert generated_cell_dict.get(event_int_str()) == event3
    assert generated_cell_dict.get(celldepth_str()) == 0
    assert generated_cell_dict.get(deal_owner_name_str()) == sue_str
    assert generated_cell_dict.get(penny_str()) == 1
    assert generated_cell_dict.get(quota_str()) == CELLNODE_QUOTA_DEFAULT


def test_cellunit_get_from_dir_ReturnsObj_Scenario0_NoFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    time7 = 777000
    sue_str = "Sue"
    bob_str = "Bob"
    das = [bob_str, sue_str]
    sue7_cell_path = node_path(fisc_mstr_dir, a23_str, sue_str, time7, das)
    event3 = 3
    assert os_path_exists(sue7_cell_path) is False
    cell_dir = create_cell_dir_path(
        fisc_mstr_dir, a23_str, sue_str, time7, deal_ancestors=das
    )

    # WHEN / THEN
    assert cellunit_get_from_dir(cell_dir) is None


def test_cellunit_get_from_dir_ReturnsObj_Scenario1_FileExists(env_dir_setup_cleanup):
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    time7 = 777000
    sue_str = "Sue"
    bob_str = "Bob"
    das = [bob_str, sue_str]
    sue7_cell_path = node_path(fisc_mstr_dir, a23_str, sue_str, time7, das)
    event3 = 3
    assert os_path_exists(sue7_cell_path) is False
    cellunit_add_json_file(
        fisc_mstr_dir, a23_str, sue_str, time7, event3, deal_ancestors=das
    )
    cell_dir = create_cell_dir_path(
        fisc_mstr_dir, a23_str, sue_str, time7, deal_ancestors=das
    )

    # WHEN
    gen_cellunit = cellunit_get_from_dir(cell_dir)

    # THEN
    expected_cellunit = cellunit_shop(sue_str, ancestors=das, event_int=event3)
    assert gen_cellunit == expected_cellunit


def test_cellunit_save_to_dir_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    time7 = 777000
    sue_str = "Sue"
    bob_str = "Bob"
    das = [bob_str, sue_str]
    sue7_cell_path = node_path(fisc_mstr_dir, a23_str, sue_str, time7, das)
    event3 = 3
    sue_cell = cellunit_shop(sue_str, ancestors=das, event_int=event3)
    cell_dir = create_cell_dir_path(fisc_mstr_dir, a23_str, sue_str, time7, das)
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
    sue_bud = budunit_shop(sue_str, a23_str)
    sue_bud.add_acctunit(sue_str, 3, 5)
    sue_bud.add_acctunit(yao_str, 7, 2)
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sue_bud.add_concept(clean_fact.fstate)
    sue_bud.add_concept(dirty_fact.fstate)
    casa_way = sue_bud.make_l1_way("casa")
    mop_way = sue_bud.make_way(casa_way, "mop")
    sue_bud.add_concept(mop_way, 1, pledge=True)
    sue_bud.edit_reason(mop_way, dirty_fact.fcontext, dirty_fact.fstate)
    sue_bud.add_fact(
        dirty_fact.fcontext, dirty_fact.fstate, create_missing_concepts=True
    )
    sky_blue_fact = sky_blue_factunit()
    sue_budevent_factunits = {clean_fact.fcontext: clean_fact}
    sue_found_factunits = {dirty_fact.fcontext: dirty_fact}
    sue_boss_factunits = {sky_blue_fact.fcontext: sky_blue_fact}
    sue_cell = cellunit_shop(
        deal_owner_name=yao_str,
        ancestors=sue_ancestors,
        event_int=sue_event7,
        celldepth=sue_celldepth3,
        penny=sue_penny2,
        quota=sue_quota300,
        budadjust=sue_bud,
        budevent_facts=sue_budevent_factunits,
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


def test_save_valid_deal_file_Scenario0_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    yao_str = "Yao"
    t55_deal = get_dealunit_55_example()
    t55_deal_time = t55_deal.deal_time
    t55_deal_path = create_dealunit_json_path(mstr_dir, a23_str, yao_str, t55_deal_time)
    assert os_path_exists(t55_deal_path) is False

    # WHEN
    save_deal_file(mstr_dir, a23_str, yao_str, t55_deal)

    # THEN
    assert os_path_exists(t55_deal_path)


def test_save_valid_deal_file_Scenario1_RaisesError(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    yao_str = "Yao"
    invalid_deal = get_dealunit_invalid_example()

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        save_deal_file(mstr_dir, a23_str, yao_str, invalid_deal)
    exception_str = (
        "magnitude cannot be calculated: debt_deal_acct_net=-5, cred_deal_acct_net=3"
    )
    assert str(excinfo.value) == exception_str


def test_deal_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    yao_str = "Yao"
    t55_deal = get_dealunit_55_example()
    assert not deal_file_exists(mstr_dir, a23_str, yao_str, t55_deal.deal_time)

    # WHEN
    save_deal_file(mstr_dir, a23_str, yao_str, t55_deal)

    # THEN
    assert deal_file_exists(mstr_dir, a23_str, yao_str, t55_deal.deal_time)


def test_open_deal_file_ReturnsObj_Scenario0_NoFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    yao_str = "Yao"
    t55_deal = get_dealunit_55_example()
    t55_deal_time = t55_deal.deal_time
    assert not deal_file_exists(mstr_dir, a23_str, yao_str, t55_deal_time)

    # WHEN / THEN
    assert not open_deal_file(mstr_dir, a23_str, yao_str, t55_deal_time)


def test_open_deal_file_ReturnsObj_Scenario1_FileExists(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    yao_str = "Yao"
    t55_deal = get_dealunit_55_example()
    t55_deal_time = t55_deal.deal_time
    save_deal_file(mstr_dir, a23_str, yao_str, t55_deal)
    assert deal_file_exists(mstr_dir, a23_str, yao_str, t55_deal_time)

    # WHEN / THEN
    assert open_deal_file(mstr_dir, a23_str, yao_str, t55_deal_time) == t55_deal


def test_save_budpoint_file_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    t55_budpoint = get_budunit_with_4_levels()
    t55_deal_time = 55
    t55_budpoint_path = create_budpoint_path(mstr_dir, a23_str, sue_str, t55_deal_time)
    print(f"{t55_budpoint.fisc_label=}")
    print(f"               {mstr_dir=}")
    print(f"      {t55_budpoint_path=}")
    assert os_path_exists(t55_budpoint_path) is False

    # WHEN
    save_budpoint_file(mstr_dir, t55_budpoint, t55_deal_time)

    # THEN
    assert os_path_exists(t55_budpoint_path)


def test_save_budpoint_file_RaisesError(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    irrational_budpoint = get_budunit_irrational_example()
    t55_deal_time = 55

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        save_budpoint_file(mstr_dir, irrational_budpoint, t55_deal_time)
    exception_str = "BudPoint could not be saved BudUnit._rational is False"
    assert str(excinfo.value) == exception_str


def test_budpoint_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    t55_deal_time = 55
    assert budpoint_file_exists(mstr_dir, a23_str, sue_str, t55_deal_time) is False

    # WHEN
    t55_budpoint = get_budunit_with_4_levels()
    save_budpoint_file(mstr_dir, t55_budpoint, t55_deal_time)

    # THEN
    assert budpoint_file_exists(mstr_dir, a23_str, sue_str, t55_deal_time)


def test_open_budpoint_file_ReturnsObj_Scenario0_NoFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    t55_deal_time = 55
    assert not budpoint_file_exists(mstr_dir, a23_str, sue_str, t55_deal_time)

    # WHEN / THEN
    assert not open_budpoint_file(mstr_dir, a23_str, sue_str, t55_deal_time)


def test_open_budpoint_file_ReturnsObj_Scenario1_FileExists(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    t55_deal_time = 55
    t55_budpoint = get_budunit_with_4_levels()
    save_budpoint_file(mstr_dir, t55_budpoint, t55_deal_time)
    assert budpoint_file_exists(mstr_dir, a23_str, sue_str, t55_deal_time)

    # WHEN
    file_budpoint = open_budpoint_file(mstr_dir, a23_str, sue_str, t55_deal_time)

    # THEN
    assert file_budpoint.get_dict() == t55_budpoint.get_dict()


def test_get_timepoint_dirs_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    t55_deal_time = 55
    t77_deal_time = 77
    budpoint = get_budunit_with_4_levels()
    save_budpoint_file(mstr_dir, budpoint, t55_deal_time)
    save_budpoint_file(mstr_dir, budpoint, t77_deal_time)

    # WHEN
    timepoint_dirs = get_timepoint_dirs(mstr_dir, a23_str, sue_str)

    # THEN
    assert timepoint_dirs == [t55_deal_time, t77_deal_time]
