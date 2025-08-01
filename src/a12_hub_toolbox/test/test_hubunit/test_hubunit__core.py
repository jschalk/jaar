from pytest import raises as pytest_raises
from src.a00_data_toolbox.file_toolbox import create_path
from src.a01_term_logic.rope import create_rope, default_knot_if_None
from src.a02_finance_logic.finance_config import (
    default_fund_iota_if_None,
    default_RespectBit_if_None,
    filter_penny,
    validate_fund_pool,
)
from src.a05_plan_logic.plan import get_default_belief_label as root_label
from src.a12_hub_toolbox.a12_path import (
    create_believer_dir_path,
    create_keep_rope_path,
    create_treasury_db_path,
)
from src.a12_hub_toolbox.hubunit import HubUnit, hubunit_shop
from src.a12_hub_toolbox.test._util.a12_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_HubUnit_Exists():
    # ESTABLISH / WHEN
    x_hubunit = HubUnit()

    # THEN
    assert not x_hubunit.belief_mstr_dir
    assert not x_hubunit.belief_label
    assert not x_hubunit.believer_name
    assert not x_hubunit.keep_rope
    assert not x_hubunit.knot
    assert not x_hubunit.fund_pool
    assert not x_hubunit.fund_iota
    assert not x_hubunit.respect_bit
    assert not x_hubunit.penny
    assert not x_hubunit.keep_point_magnitude
    assert not x_hubunit._keeps_dir
    assert not x_hubunit._atoms_dir
    assert not x_hubunit._packs_dir


def test_hubunit_shop_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = "src/a15_belief_logic/test/_util"
    x_belief_label = "amy45"
    sue_str = "Sue"
    x_knot = "/"
    x_fund_pool = 13000
    x_fund_iota = 13
    x_respect_bit = 9
    x_penny = 3
    x_money_magnitude = 900

    # WHEN
    x_hubunit = hubunit_shop(
        belief_mstr_dir=x_belief_mstr_dir,
        belief_label=x_belief_label,
        believer_name=sue_str,
        keep_rope=None,
        knot=x_knot,
        fund_pool=x_fund_pool,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        penny=x_penny,
        keep_point_magnitude=x_money_magnitude,
    )

    # THEN
    assert x_hubunit.belief_mstr_dir == x_belief_mstr_dir
    assert x_hubunit.belief_label == x_belief_label
    assert x_hubunit.believer_name == sue_str
    assert x_hubunit.knot == x_knot
    assert x_hubunit.fund_pool == x_fund_pool
    assert x_hubunit.fund_iota == x_fund_iota
    assert x_hubunit.respect_bit == x_respect_bit
    assert x_hubunit.penny == x_penny
    assert x_hubunit.keep_point_magnitude == x_money_magnitude
    sue_dir = create_believer_dir_path(x_belief_mstr_dir, x_belief_label, sue_str)
    assert x_hubunit._keeps_dir == create_path(sue_dir, "keeps")
    assert x_hubunit._atoms_dir == create_path(sue_dir, "atoms")
    assert x_hubunit._packs_dir == create_path(sue_dir, "packs")


def test_hubunit_shop_ReturnsObjWhenEmpty():
    # ESTABLISH
    sue_str = "Sue"
    nation_str = "nation"
    nation_rope = create_rope(root_label(), nation_str)
    usa_str = "USA"
    usa_rope = create_rope(nation_rope, usa_str)
    texas_str = "Texas"
    texas_rope = create_rope(usa_rope, texas_str)
    belief_mstr_dir = get_module_temp_dir()
    amy23_str = "amy23"

    # WHEN
    sue_hubunit = hubunit_shop(belief_mstr_dir, amy23_str, sue_str, texas_rope)

    # THEN
    keep_path = create_keep_rope_path(
        belief_mstr_dir, sue_str, amy23_str, texas_rope, None
    )
    x_visions_path = create_path(keep_path, "visions")
    x_grades_path = create_path(keep_path, "grades")

    assert sue_hubunit.belief_mstr_dir == belief_mstr_dir
    assert sue_hubunit.belief_label == amy23_str
    assert sue_hubunit.believer_name == sue_str
    assert sue_hubunit.knot == default_knot_if_None()
    assert sue_hubunit.fund_pool == validate_fund_pool()
    assert sue_hubunit.fund_iota == default_fund_iota_if_None()
    assert sue_hubunit.respect_bit == default_RespectBit_if_None()
    assert sue_hubunit.penny == filter_penny()
    assert sue_hubunit.keep_rope == texas_rope
    bob_str = "Bob"
    assert sue_hubunit.visions_path() == x_visions_path
    assert sue_hubunit.grades_path() == x_grades_path
    sue_visions_path = sue_hubunit.visions_path()
    sue_grades_path = sue_hubunit.grades_path()
    x_vision_path = create_path(sue_visions_path, f"{bob_str}.json")
    x_grade_path = create_path(sue_grades_path, f"{bob_str}.json")
    assert sue_hubunit.vision_path(bob_str) == x_vision_path
    assert sue_hubunit.grade_path(bob_str) == x_grade_path


def test_hubunit_shop_RaisesErrorIf_believer_name_Contains_knot():
    # ESTABLISH
    slash_str = "/"
    bob_str = f"Bob{slash_str}Sue"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        hubunit_shop(None, None, believer_name=bob_str, knot=slash_str)
    assertion_fail_str = (
        f"'{bob_str}' needs to be a LabelTerm. Cannot contain knot: '{slash_str}'"
    )
    assert str(excinfo.value) == assertion_fail_str
