from pytest import raises as pytest_raises
from src.ch00_data_toolbox.file_toolbox import create_path
from src.ch02_rope_logic.rope import create_rope, default_knot_if_None
from src.ch03_finance_logic.finance_config import (
    default_fund_iota_if_None,
    default_RespectBit_if_None,
    filter_penny,
    validate_fund_pool,
)
from src.ch06_plan_logic.plan import get_default_moment_label as root_label
from src.ch12_hub_toolbox.ch12_path import (
    create_belief_dir_path,
    create_keep_rope_path,
    create_treasury_db_path,
)
from src.ch12_hub_toolbox.hubunit import HubUnit, hubunit_shop
from src.ch12_hub_toolbox.test._util.ch12_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_HubUnit_Exists():
    # ESTABLISH / WHEN
    x_hubunit = HubUnit()

    # THEN
    assert not x_hubunit.moment_mstr_dir
    assert not x_hubunit.moment_label
    assert not x_hubunit.belief_name
    assert not x_hubunit.keep_rope
    assert not x_hubunit.knot
    assert not x_hubunit.fund_pool
    assert not x_hubunit.fund_iota
    assert not x_hubunit.respect_bit
    assert not x_hubunit.penny
    assert not x_hubunit.keep_point_magnitude
    assert not x_hubunit.keeps_dir
    assert not x_hubunit._atoms_dir
    assert not x_hubunit._packs_dir


def test_hubunit_shop_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = "src/ch15_moment_logic/test/_util"
    x_moment_label = "amy45"
    sue_str = "Sue"
    x_knot = "/"
    x_fund_pool = 13000
    x_fund_iota = 13
    x_respect_bit = 9
    x_penny = 3
    x_money_magnitude = 900

    # WHEN
    x_hubunit = hubunit_shop(
        moment_mstr_dir=x_moment_mstr_dir,
        moment_label=x_moment_label,
        belief_name=sue_str,
        keep_rope=None,
        knot=x_knot,
        fund_pool=x_fund_pool,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        penny=x_penny,
        keep_point_magnitude=x_money_magnitude,
    )

    # THEN
    assert x_hubunit.moment_mstr_dir == x_moment_mstr_dir
    assert x_hubunit.moment_label == x_moment_label
    assert x_hubunit.belief_name == sue_str
    assert x_hubunit.knot == x_knot
    assert x_hubunit.fund_pool == x_fund_pool
    assert x_hubunit.fund_iota == x_fund_iota
    assert x_hubunit.respect_bit == x_respect_bit
    assert x_hubunit.penny == x_penny
    assert x_hubunit.keep_point_magnitude == x_money_magnitude
    sue_dir = create_belief_dir_path(x_moment_mstr_dir, x_moment_label, sue_str)
    assert x_hubunit.keeps_dir == create_path(sue_dir, "keeps")
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
    moment_mstr_dir = get_module_temp_dir()
    amy23_str = "amy23"

    # WHEN
    sue_hubunit = hubunit_shop(moment_mstr_dir, amy23_str, sue_str, texas_rope)

    # THEN
    keep_path = create_keep_rope_path(
        moment_mstr_dir, sue_str, amy23_str, texas_rope, None
    )
    x_visions_path = create_path(keep_path, "visions")
    x_grades_path = create_path(keep_path, "grades")

    assert sue_hubunit.moment_mstr_dir == moment_mstr_dir
    assert sue_hubunit.moment_label == amy23_str
    assert sue_hubunit.belief_name == sue_str
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


def test_hubunit_shop_RaisesErrorIf_belief_name_Contains_knot():
    # ESTABLISH
    slash_str = "/"
    bob_str = f"Bob{slash_str}Sue"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        hubunit_shop(None, None, belief_name=bob_str, knot=slash_str)
    assertion_fail_str = (
        f"'{bob_str}' needs to be a LabelTerm. Cannot contain knot: '{slash_str}'"
    )
    assert str(excinfo.value) == assertion_fail_str
