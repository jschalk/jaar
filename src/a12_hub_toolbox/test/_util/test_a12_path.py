from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from pytest import raises as pytest_raises
from src.a00_data_toolbox.file_toolbox import create_path, get_json_filename
from src.a01_term_logic.rope import create_rope, create_rope_from_labels
from src.a09_pack_logic.test._util.a09_str import (
    belief_label_str,
    believer_name_str,
    bud_time_str,
    event_int_str,
)
from src.a12_hub_toolbox.a12_path import (
    BELIEF_FILENAME,
    BELIEVEREVENT_FILENAME,
    BELIEVERPOINT_FILENAME,
    BUDUNIT_FILENAME,
    CELL_MANDATE_FILENAME,
    CELLNODE_FILENAME,
    EVENT_ALL_PACK_FILENAME,
    EVENT_EXPRESSED_PACK_FILENAME,
    create_atoms_dir_path,
    create_belief_believers_dir_path,
    create_belief_dir_path,
    create_belief_json_path,
    create_believer_dir_path,
    create_believer_event_dir_path,
    create_believerevent_path,
    create_believerpoint_path,
    create_bud_dir_path,
    create_buds_dir_path,
    create_budunit_json_path,
    create_cell_dir_path,
    create_cell_json_path,
    create_cell_partner_mandate_ledger_path,
    create_event_all_pack_path,
    create_event_expressed_pack_path,
    create_gut_path,
    create_job_path,
    create_keep_duty_path,
    create_keep_dutys_path,
    create_keep_grades_path,
    create_keep_rope_path,
    create_keep_visions_path,
    create_keeps_dir_path,
    create_packs_dir_path,
    create_treasury_db_path,
    treasury_filename,
)
from src.a12_hub_toolbox.test._util.a12_env import get_module_temp_dir
from src.a12_hub_toolbox.test._util.a12_str import gut_str, job_str


def test_treasury_filename_ReturnsObj():
    assert treasury_filename() == "treasury.db"


def test_create_belief_dir_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"

    # WHEN
    gen_a23_dir_path = create_belief_dir_path(x_belief_mstr_dir, a23_str)

    # THEN
    beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    expected_a23_path = create_path(beliefs_dir, a23_str)
    assert gen_a23_dir_path == expected_a23_path


def test_create_belief_json_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"

    # WHEN
    gen_a23_json_path = create_belief_json_path(x_belief_mstr_dir, a23_str)

    # THEN
    beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    a23_path = create_path(beliefs_dir, a23_str)
    expected_a23_json_path = create_path(a23_path, BELIEF_FILENAME)
    assert gen_a23_json_path == expected_a23_json_path


def test_create_belief_believers_dir_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    amy23_str = "amy23"

    # WHEN
    gen_believers_dir = create_belief_believers_dir_path(x_belief_mstr_dir, amy23_str)

    # THEN
    x_beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    amy23_dir = create_path(x_beliefs_dir, amy23_str)
    expected_believers_dir = create_path(amy23_dir, "believers")
    assert gen_believers_dir == expected_believers_dir


def test_create_believer_dir_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    amy23_str = "amy23"
    sue_str = "Sue"

    # WHEN
    sue_dir = create_believer_dir_path(x_belief_mstr_dir, amy23_str, sue_str)

    # THEN
    x_beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    amy23_dir = create_path(x_beliefs_dir, amy23_str)
    believers_dir = create_path(amy23_dir, "believers")
    expected_sue_dir = create_path(believers_dir, sue_str)
    assert sue_dir == expected_sue_dir


def test_create_keeps_dir_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    amy23_str = "amy23"
    sue_str = "Sue"

    # WHEN
    keeps_dir = create_keeps_dir_path(x_belief_mstr_dir, amy23_str, sue_str)

    # THEN
    x_beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    amy23_dir = create_path(x_beliefs_dir, amy23_str)
    believers_dir = create_path(amy23_dir, "believers")
    sue_dir = create_path(believers_dir, sue_str)
    expected_keeps_dir = create_path(sue_dir, "keeps")
    assert keeps_dir == expected_keeps_dir


def test_create_keep_rope_path_ReturnsObj_Scenario0_SimpleRope():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    amy23_str = "amy23"
    sue_str = "Sue"
    casa_str = "casa"
    casa_rope = create_rope(amy23_str, casa_str)

    # WHEN
    keep_casa_path = create_keep_rope_path(
        x_belief_mstr_dir, sue_str, amy23_str, casa_rope, None
    )

    # THEN
    keeps_dir = create_keeps_dir_path(x_belief_mstr_dir, amy23_str, sue_str)
    keep_amy23_dir = create_path(keeps_dir, amy23_str)
    expected_keep_casa_dir = create_path(keep_amy23_dir, casa_str)
    assert keep_casa_path == expected_keep_casa_dir


def test_create_keep_rope_path_ReturnsObj_Scenario1_MoreTestsForRopePathCreation():
    # ESTABLISH
    sue_str = "Sue"
    peru_str = "peru"
    belief_mstr_dir = get_module_temp_dir()
    texas_str = "texas"
    dallas_str = "dallas"
    elpaso_str = "el paso"
    kern_str = "kern"
    planroot = "planroot"
    texas_rope = create_rope_from_labels([peru_str, texas_str])
    dallas_rope = create_rope_from_labels([peru_str, texas_str, dallas_str])
    elpaso_rope = create_rope_from_labels([peru_str, texas_str, elpaso_str])
    kern_rope = create_rope_from_labels([peru_str, texas_str, elpaso_str, kern_str])

    # WHEN
    # texas_path = create_keep_rope_path(sue_hubunit, texas_rope)
    texas_path = create_keep_rope_path(
        belief_mstr_dir,
        believer_name=sue_str,
        belief_label=peru_str,
        keep_rope=texas_rope,
        knot=None,
    )
    # dallas_path = createdallas_path_keep_rope_path(sue_hubunit, dallas_rope)
    dallas_path = create_keep_rope_path(
        belief_mstr_dir,
        believer_name=sue_str,
        belief_label=peru_str,
        keep_rope=dallas_rope,
        knot=None,
    )
    # elpaso_path = create_keep_rope_path(sue_hubunit, elpaso_rope)
    elpaso_path = create_keep_rope_path(
        belief_mstr_dir,
        believer_name=sue_str,
        belief_label=peru_str,
        keep_rope=elpaso_rope,
        knot=None,
    )
    # kern_path = create_keep_rope_path(sue_hubunit, kern_rope)
    kern_path = create_keep_rope_path(
        belief_mstr_dir,
        believer_name=sue_str,
        belief_label=peru_str,
        keep_rope=kern_rope,
        knot=None,
    )

    # THEN
    keeps_dir = create_keeps_dir_path(belief_mstr_dir, peru_str, sue_str)
    planroot_dir = create_path(keeps_dir, peru_str)
    print(f"{kern_rope=}")
    print(f"{planroot_dir=}")
    assert texas_path == create_path(planroot_dir, texas_str)
    assert dallas_path == create_path(texas_path, dallas_str)
    assert elpaso_path == create_path(texas_path, elpaso_str)
    assert kern_path == create_path(elpaso_path, kern_str)

    # WHEN / THEN
    diff_root_texas_rope = create_rope_from_labels([peru_str, texas_str])
    diff_root_dallas_rope = create_rope_from_labels([peru_str, texas_str, dallas_str])
    diff_root_elpaso_rope = create_rope_from_labels([peru_str, texas_str, elpaso_str])
    assert texas_path == create_keep_rope_path(
        belief_mstr_dir,
        believer_name=sue_str,
        belief_label=peru_str,
        keep_rope=diff_root_texas_rope,
        knot=None,
    )
    assert dallas_path == create_keep_rope_path(
        belief_mstr_dir,
        believer_name=sue_str,
        belief_label=peru_str,
        keep_rope=diff_root_dallas_rope,
        knot=None,
    )
    assert elpaso_path == create_keep_rope_path(
        belief_mstr_dir,
        believer_name=sue_str,
        belief_label=peru_str,
        keep_rope=diff_root_elpaso_rope,
        knot=None,
    )


def test_create_keep_rope_path_RaisesError_Scenarion2_keep_rope_DoesNotExist():
    # ESTABLISH
    bob_str = "Bob"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        create_keep_rope_path("dir", bob_str, "amy23", None, None)
    assertion_fail_str = (
        f"'{bob_str}' cannot save to keep_path because it does not have keep_rope."
    )
    assert str(excinfo.value) == assertion_fail_str


def test_create_keep_dutys_path_ReturnsObj() -> None:
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    amy23_str = "amy23"
    sue_str = "Sue"
    casa_str = "casa"
    casa_rope = create_rope(amy23_str, casa_str)

    # WHEN
    gen_keep_dutys_path = create_keep_dutys_path(
        belief_mstr_dir=x_belief_mstr_dir,
        believer_name=sue_str,
        belief_label=amy23_str,
        keep_rope=casa_rope,
        knot=None,
    )

    # THEN
    keep_casa_path = create_keep_rope_path(
        x_belief_mstr_dir, sue_str, amy23_str, casa_rope, None
    )
    expected_keep_dutys_path = create_path(keep_casa_path, "dutys")
    assert gen_keep_dutys_path == expected_keep_dutys_path


def test_create_keep_duty_path_ReturnsObj() -> None:
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    amy23_str = "amy23"
    sue_str = "Sue"
    casa_str = "casa"
    casa_rope = create_rope(amy23_str, casa_str)
    bob_str = "Bob"

    # WHEN
    gen_keep_duty_path = create_keep_duty_path(
        belief_mstr_dir=x_belief_mstr_dir,
        believer_name=sue_str,
        belief_label=amy23_str,
        keep_rope=casa_rope,
        knot=None,
        duty_believer=bob_str,
    )

    # THEN
    keep_dutys_path = create_keep_dutys_path(
        x_belief_mstr_dir, sue_str, amy23_str, casa_rope, None
    )
    bob_filename = get_json_filename(bob_str)
    expected_keep_duty_path = create_path(keep_dutys_path, bob_filename)
    assert gen_keep_duty_path == expected_keep_duty_path


def test_create_keep_grades_path_ReturnsObj() -> None:
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    amy23_str = "amy23"
    sue_str = "Sue"
    casa_str = "casa"
    casa_rope = create_rope(amy23_str, casa_str)

    # WHEN
    gen_keep_dutys_path = create_keep_grades_path(
        belief_mstr_dir=x_belief_mstr_dir,
        believer_name=sue_str,
        belief_label=amy23_str,
        keep_rope=casa_rope,
        knot=None,
    )

    # THEN
    keep_casa_path = create_keep_rope_path(
        x_belief_mstr_dir, sue_str, amy23_str, casa_rope, None
    )
    expected_keep_dutys_path = create_path(keep_casa_path, "grades")
    assert gen_keep_dutys_path == expected_keep_dutys_path


def test_create_keep_visions_path_ReturnsObj() -> None:
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    amy23_str = "amy23"
    sue_str = "Sue"
    casa_str = "casa"
    casa_rope = create_rope(amy23_str, casa_str)

    # WHEN
    gen_keep_dutys_path = create_keep_visions_path(
        belief_mstr_dir=x_belief_mstr_dir,
        believer_name=sue_str,
        belief_label=amy23_str,
        keep_rope=casa_rope,
        knot=None,
    )

    # THEN
    keep_casa_path = create_keep_rope_path(
        x_belief_mstr_dir, sue_str, amy23_str, casa_rope, None
    )
    expected_keep_dutys_path = create_path(keep_casa_path, "visions")
    assert gen_keep_dutys_path == expected_keep_dutys_path


def test_create_treasury_db_path_ReturnsObj() -> None:
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    amy23_str = "amy23"
    sue_str = "Sue"
    casa_str = "casa"
    casa_rope = create_rope(amy23_str, casa_str)

    # WHEN
    gen_keep_dutys_path = create_treasury_db_path(
        belief_mstr_dir=x_belief_mstr_dir,
        believer_name=sue_str,
        belief_label=amy23_str,
        keep_rope=casa_rope,
        knot=None,
    )

    # THEN
    keep_casa_path = create_keep_rope_path(
        x_belief_mstr_dir, sue_str, amy23_str, casa_rope, None
    )
    expected_keep_dutys_path = create_path(keep_casa_path, "treasury.db")
    assert gen_keep_dutys_path == expected_keep_dutys_path


def test_create_atoms_dir_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    amy23_str = "amy23"
    sue_str = "Sue"

    # WHEN
    atoms_dir = create_atoms_dir_path(x_belief_mstr_dir, amy23_str, sue_str)

    # THEN
    x_beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    amy23_dir = create_path(x_beliefs_dir, amy23_str)
    believers_dir = create_path(amy23_dir, "believers")
    sue_dir = create_path(believers_dir, sue_str)
    expected_atoms_dir = create_path(sue_dir, "atoms")
    assert atoms_dir == expected_atoms_dir


def test_create_packs_dir_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    amy23_str = "amy23"
    sue_str = "Sue"

    # WHEN
    packs_dir = create_packs_dir_path(x_belief_mstr_dir, amy23_str, sue_str)

    # THEN
    x_beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    amy23_dir = create_path(x_beliefs_dir, amy23_str)
    believers_dir = create_path(amy23_dir, "believers")
    sue_dir = create_path(believers_dir, sue_str)
    expected_packs_dir = create_path(sue_dir, "packs")
    assert packs_dir == expected_packs_dir


def test_create_buds_dir_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    amy23_str = "amy23"
    sue_str = "Sue"

    # WHEN
    buds_dir = create_buds_dir_path(x_belief_mstr_dir, amy23_str, sue_str)

    # THEN
    x_beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    amy23_dir = create_path(x_beliefs_dir, amy23_str)
    believers_dir = create_path(amy23_dir, "believers")
    sue_dir = create_path(believers_dir, sue_str)
    expected_buds_dir = create_path(sue_dir, "buds")
    assert buds_dir == expected_buds_dir


def test_create_bud_dir_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    amy23_str = "amy23"
    sue_str = "Sue"
    timepoint7 = 7

    # WHEN
    generated_timepoint_dir = create_bud_dir_path(
        x_belief_mstr_dir, amy23_str, sue_str, timepoint7
    )

    # THEN
    x_beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    amy23_dir = create_path(x_beliefs_dir, amy23_str)
    believers_dir = create_path(amy23_dir, "believers")
    sue_dir = create_path(believers_dir, sue_str)
    buds_dir = create_path(sue_dir, "buds")
    expected_timepoint_dir = create_path(buds_dir, timepoint7)
    assert generated_timepoint_dir == expected_timepoint_dir


def test_create_budunit_json_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    timepoint7 = 7

    # WHEN
    gen_bud_path = create_budunit_json_path(
        x_belief_mstr_dir, a23_str, sue_str, timepoint7
    )

    # THEN
    x_beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    amy23_dir = create_path(x_beliefs_dir, a23_str)
    believers_dir = create_path(amy23_dir, "believers")
    sue_dir = create_path(believers_dir, sue_str)
    buds_dir = create_path(sue_dir, "buds")
    timepoint_dir = create_path(buds_dir, timepoint7)
    expected_bud_path_dir = create_path(timepoint_dir, BUDUNIT_FILENAME)
    assert gen_bud_path == expected_bud_path_dir


def test_create_believerpoint_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    timepoint7 = 7

    # WHEN
    gen_believerpoint_path = create_believerpoint_path(
        x_belief_mstr_dir, a23_str, sue_str, timepoint7
    )

    # THEN
    x_beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    amy23_dir = create_path(x_beliefs_dir, a23_str)
    believers_dir = create_path(amy23_dir, "believers")
    sue_dir = create_path(believers_dir, sue_str)
    buds_dir = create_path(sue_dir, "buds")
    timepoint_dir = create_path(buds_dir, timepoint7)
    expected_believerpoint_path_dir = create_path(timepoint_dir, BELIEVERPOINT_FILENAME)
    assert gen_believerpoint_path == expected_believerpoint_path_dir


def test_create_cell_dir_path_ReturnsObj_Scenario0_No_bud_ancestors():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    tp7 = 7

    # WHEN
    gen_cell_dir = create_cell_dir_path(x_belief_mstr_dir, a23_str, sue_str, tp7, [])

    # THEN
    timepoint_dir = create_bud_dir_path(x_belief_mstr_dir, a23_str, sue_str, tp7)
    assert gen_cell_dir == timepoint_dir


def test_create_cell_dir_path_ReturnsObj_Scenario1_One_bud_ancestors():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    tp7 = 7
    yao_str = "Yao"
    x_bud_ancestors = [yao_str]

    # WHEN
    gen_cell_dir = create_cell_dir_path(
        x_belief_mstr_dir, a23_str, sue_str, tp7, bud_ancestors=x_bud_ancestors
    )

    # THEN
    timepoint_dir = create_bud_dir_path(x_belief_mstr_dir, a23_str, sue_str, tp7)
    tp_yao_dir = create_path(timepoint_dir, yao_str)
    assert gen_cell_dir == tp_yao_dir


def test_create_cell_dir_path_ReturnsObj_Scenario2_Three_bud_ancestors():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    tp7 = 7
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    x_bud_ancestors = [yao_str, bob_str, zia_str]

    # WHEN
    gen_bud_celldepth_dir_path = create_cell_dir_path(
        x_belief_mstr_dir, a23_str, sue_str, tp7, bud_ancestors=x_bud_ancestors
    )

    # THEN
    timepoint_dir = create_bud_dir_path(x_belief_mstr_dir, a23_str, sue_str, tp7)
    tp_yao_dir = create_path(timepoint_dir, yao_str)
    tp_yao_bob_dir = create_path(tp_yao_dir, bob_str)
    expected_tp_yao_bob_zia_dir = create_path(tp_yao_bob_dir, zia_str)
    assert gen_bud_celldepth_dir_path == expected_tp_yao_bob_zia_dir


def test_create_cell_json_path_ReturnsObj_Scenario0_Empty_bud_ancestors():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    timepoint7 = 7

    # WHEN
    gen_cell_json_path = create_cell_json_path(
        x_belief_mstr_dir, a23_str, sue_str, timepoint7
    )

    # THEN
    x_beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    amy23_dir = create_path(x_beliefs_dir, a23_str)
    believers_dir = create_path(amy23_dir, "believers")
    sue_dir = create_path(believers_dir, sue_str)
    buds_dir = create_path(sue_dir, "buds")
    timepoint_dir = create_path(buds_dir, timepoint7)
    expected_cell_json_path = create_path(timepoint_dir, CELLNODE_FILENAME)
    assert gen_cell_json_path == expected_cell_json_path


def test_create_cell_json_path_ReturnsObj_Scenario1_Three_bud_ancestors():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    tp7 = 7
    yao_str = "Yao"
    bob_str = "Bob"
    bud_ancestors = [yao_str, bob_str]

    # WHEN
    gen_cell_json_path = create_cell_json_path(
        x_belief_mstr_dir, a23_str, sue_str, tp7, bud_ancestors=bud_ancestors
    )

    # THEN
    timepoint_dir = create_bud_dir_path(x_belief_mstr_dir, a23_str, sue_str, tp7)
    tp_yao_dir = create_path(timepoint_dir, yao_str)
    tp_yao_bob_dir = create_path(tp_yao_dir, bob_str)
    expected_cell_json_path = create_path(tp_yao_bob_dir, CELLNODE_FILENAME)
    assert gen_cell_json_path == expected_cell_json_path


def test_create_cell_partner_mandate_ledger_path_ReturnsObj_Scenario1_Three_bud_ancestors():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    tp7 = 7
    yao_str = "Yao"
    bob_str = "Bob"
    bud_ancestors = [yao_str, bob_str]

    # WHEN
    gen_cell_json_path = create_cell_partner_mandate_ledger_path(
        x_belief_mstr_dir, a23_str, sue_str, tp7, bud_ancestors=bud_ancestors
    )

    # THEN
    timepoint_dir = create_bud_dir_path(x_belief_mstr_dir, a23_str, sue_str, tp7)
    tp_yao_dir = create_path(timepoint_dir, yao_str)
    tp_yao_bob_dir = create_path(tp_yao_dir, bob_str)
    expected_cell_json_path = create_path(tp_yao_bob_dir, CELL_MANDATE_FILENAME)
    assert gen_cell_json_path == expected_cell_json_path


def test_create_believer_event_dir_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    amy23_str = "amy23"
    bob_str = "Bob"
    event3 = 3

    # WHEN
    gen_a23_e3_dir_path = create_believer_event_dir_path(
        x_belief_mstr_dir, amy23_str, bob_str, event3
    )

    # THEN
    x_beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    a23_dir = create_path(x_beliefs_dir, amy23_str)
    a23_believers_dir = create_path(a23_dir, "believers")
    a23_bob_dir = create_path(a23_believers_dir, bob_str)
    a23_events_dir = create_path(a23_bob_dir, "events")
    expected_a23_bob_e3_dir = create_path(a23_events_dir, event3)
    assert gen_a23_e3_dir_path == expected_a23_bob_e3_dir


def test_create_believerevent_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    amy23_str = "amy23"
    bob_str = "Bob"
    event3 = 3

    # WHEN
    gen_a23_e3_believer_path = create_believerevent_path(
        x_belief_mstr_dir, amy23_str, bob_str, event3
    )

    # THEN
    x_beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    a23_dir = create_path(x_beliefs_dir, amy23_str)
    a23_believers_dir = create_path(a23_dir, "believers")
    a23_bob_dir = create_path(a23_believers_dir, bob_str)
    a23_events_dir = create_path(a23_bob_dir, "events")
    a23_bob_e3_dir = create_path(a23_events_dir, event3)
    expected_a23_bob_e3_believer_path = create_path(
        a23_bob_e3_dir, BELIEVEREVENT_FILENAME
    )
    assert gen_a23_e3_believer_path == expected_a23_bob_e3_believer_path


def test_create_event_all_pack_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    amy23_str = "amy23"
    bob_str = "Bob"
    event3 = 3

    # WHEN
    gen_a23_e3_believer_path = create_event_all_pack_path(
        x_belief_mstr_dir, amy23_str, bob_str, event3
    )

    # THEN
    x_beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    a23_dir = create_path(x_beliefs_dir, amy23_str)
    a23_believers_dir = create_path(a23_dir, "believers")
    a23_bob_dir = create_path(a23_believers_dir, bob_str)
    a23_events_dir = create_path(a23_bob_dir, "events")
    a23_bob_e3_dir = create_path(a23_events_dir, event3)
    expected_a23_bob_e3_all_pack_path = create_path(
        a23_bob_e3_dir, EVENT_ALL_PACK_FILENAME
    )
    assert gen_a23_e3_believer_path == expected_a23_bob_e3_all_pack_path


def test_create_event_expressed_pack_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    amy23_str = "amy23"
    bob_str = "Bob"
    event3 = 3

    # WHEN
    gen_a23_e3_believer_path = create_event_expressed_pack_path(
        x_belief_mstr_dir, amy23_str, bob_str, event3
    )

    # THEN
    x_beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    a23_dir = create_path(x_beliefs_dir, amy23_str)
    a23_believers_dir = create_path(a23_dir, "believers")
    a23_bob_dir = create_path(a23_believers_dir, bob_str)
    a23_events_dir = create_path(a23_bob_dir, "events")
    a23_bob_e3_dir = create_path(a23_events_dir, event3)
    expected_a23_bob_e3_expressed_pack_path = create_path(
        a23_bob_e3_dir, EVENT_EXPRESSED_PACK_FILENAME
    )
    assert gen_a23_e3_believer_path == expected_a23_bob_e3_expressed_pack_path


def test_create_gut_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    bob_str = "Bob"

    # WHEN
    gen_a23_e3_believer_path = create_gut_path(x_belief_mstr_dir, a23_str, bob_str)

    # THEN
    x_beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    a23_dir = create_path(x_beliefs_dir, a23_str)
    a23_believers_dir = create_path(a23_dir, "believers")
    a23_bob_dir = create_path(a23_believers_dir, bob_str)
    a23_bob_gut_dir = create_path(a23_bob_dir, gut_str())
    expected_a23_bob_gut_json_path = create_path(a23_bob_gut_dir, f"{bob_str}.json")
    # believer_filename = "believer.json"
    # expected_a23_e3_believer_path = create_path(a23_bob_e3_dir, believer_filename)
    assert gen_a23_e3_believer_path == expected_a23_bob_gut_json_path


def test_create_job_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    bob_str = "Bob"

    # WHEN
    gen_a23_e3_believer_path = create_job_path(x_belief_mstr_dir, a23_str, bob_str)

    # THEN
    x_beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    a23_dir = create_path(x_beliefs_dir, a23_str)
    a23_believers_dir = create_path(a23_dir, "believers")
    a23_bob_dir = create_path(a23_believers_dir, bob_str)
    a23_bob_job_dir = create_path(a23_bob_dir, job_str())
    expected_a23_bob_job_json_path = create_path(a23_bob_job_dir, f"{bob_str}.json")
    # believer_filename = "believer.json"
    # expected_a23_e3_believer_path = create_path(a23_bob_e3_dir, believer_filename)
    assert gen_a23_e3_believer_path == expected_a23_bob_job_json_path


LINUX_OS = platform_system() == "Linux"


def test_create_belief_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_belief_dir_path("belief_mstr_dir", belief_label_str())
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_belief_dir_path) == doc_str


def test_create_belief_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_belief_json_path(
        "belief_mstr_dir", belief_label=belief_label_str()
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_belief_json_path) == doc_str


def test_create_belief_believers_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_belief_believers_dir_path(
        "belief_mstr_dir", belief_label=belief_label_str()
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_belief_believers_dir_path) == doc_str


def test_create_believer_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_believer_dir_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_believer_dir_path) == doc_str


def test_create_keeps_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_keeps_dir_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_keeps_dir_path) == doc_str


def test_create_keep_rope_path_HasDocString() -> None:
    # ESTABLISH
    level1_label_str = "level1_label"
    level1_rope = create_rope("planroot", level1_label_str)
    doc_str = create_keep_rope_path(
        belief_mstr_dir="belief_mstr_dir",
        believer_name=believer_name_str(),
        belief_label=belief_label_str(),
        keep_rope=level1_rope,
        knot=None,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_keep_rope_path) == doc_str


def test_create_keep_dutys_path_HasDocString() -> None:
    # ESTABLISH
    expected_doc_str = create_keep_dutys_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        keep_rope="planroot;level1;leveln",
        knot=None,
    )
    expected_doc_str = f"Returns path: {expected_doc_str}"
    print(f"{expected_doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_keep_dutys_path) == expected_doc_str


def test_create_keep_duty_path_HasDocString() -> None:
    # ESTABLISH
    duty_believer_str = "duty_believer"
    expected_doc_str = create_keep_duty_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        keep_rope="planroot;level1;leveln",
        knot=None,
        duty_believer=duty_believer_str,
    )
    expected_doc_str = f"Returns path: {expected_doc_str}"
    print(f"{expected_doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_keep_duty_path) == expected_doc_str


def test_create_keep_grades_path_HasDocString() -> None:
    # ESTABLISH
    doc_str = create_keep_grades_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        keep_rope="planroot;level1;leveln",
        knot=None,
    )
    doc_str = f"Returns path: {doc_str}"
    print(f"                             {doc_str=}")
    print(f"{inspect_getdoc(create_keep_grades_path)=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_keep_grades_path) == doc_str


def test_create_keep_visions_path_HasDocString() -> None:
    # ESTABLISH
    doc_str = create_keep_visions_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        keep_rope="planroot;level1;leveln",
        knot=None,
    )
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_keep_visions_path) == doc_str


def test_create_treasury_db_path_HasDocString() -> None:
    # ESTABLISH
    doc_str = create_treasury_db_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        keep_rope="planroot;level1;leveln",
        knot=None,
    )
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_treasury_db_path) == doc_str


def test_create_atoms_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_atoms_dir_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_atoms_dir_path) == doc_str


def test_create_packs_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_packs_dir_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_packs_dir_path) == doc_str


def test_create_buds_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_buds_dir_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_buds_dir_path) == doc_str


def test_create_bud_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_bud_dir_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        bud_time=bud_time_str(),
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_bud_dir_path) == doc_str


def test_create_cell_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_cell_dir_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        bud_time=bud_time_str(),
        bud_ancestors=["ledger_believer1", "ledger_believer2", "ledger_believer3"],
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_dir_path) == doc_str


def test_create_cell_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_cell_json_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        bud_time=bud_time_str(),
        bud_ancestors=["ledger_believer1", "ledger_believer2", "ledger_believer3"],
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_json_path) == doc_str


def test_create_cell_partner_mandate_ledger_path_HasDocString():
    # ESTABLISH
    doc_str = create_cell_partner_mandate_ledger_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        bud_time=bud_time_str(),
        bud_ancestors=["ledger_believer1", "ledger_believer2", "ledger_believer3"],
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert (
        LINUX_OS or inspect_getdoc(create_cell_partner_mandate_ledger_path) == doc_str
    )


def test_create_budunit_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_budunit_json_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        bud_time=bud_time_str(),
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_budunit_json_path) == doc_str


def test_create_believerpoint_path_HasDocString():
    # ESTABLISH
    doc_str = create_believerpoint_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        bud_time=bud_time_str(),
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_believerpoint_path) == doc_str


def test_create_believer_event_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_believer_event_dir_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        event_int=event_int_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_believer_event_dir_path) == doc_str


def test_create_believerevent_path_HasDocString():
    # ESTABLISH
    doc_str = create_believerevent_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        event_int=event_int_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_believerevent_path) == doc_str


def test_create_event_all_pack_path_HasDocString():
    # ESTABLISH
    doc_str = create_event_all_pack_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        event_int=event_int_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_event_all_pack_path) == doc_str


def test_create_event_expressed_pack_path_HasDocString():
    # ESTABLISH
    doc_str = create_event_expressed_pack_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        event_int=event_int_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_event_expressed_pack_path) == doc_str


def test_create_gut_path_HasDocString():
    # ESTABLISH
    doc_str = create_gut_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    print(f"{doc_str=}")
    print(f"{inspect_getdoc(create_gut_path)=}")
    print(inspect_getdoc(create_gut_path))
    assert LINUX_OS or inspect_getdoc(create_gut_path) == doc_str


def test_create_job_path_HasDocString():
    # ESTABLISH
    doc_str = create_job_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_job_path) == doc_str
