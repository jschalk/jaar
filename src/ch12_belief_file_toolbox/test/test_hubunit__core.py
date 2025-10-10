from pytest import raises as pytest_raises
from src.ch01_data_toolbox.file_toolbox import create_path
from src.ch02_rope_logic.rope import default_knot_if_None
from src.ch03_allot_toolbox.allot import default_grain_num_if_None, validate_pool_num
from src.ch12_belief_file_toolbox._ref.ch12_path import create_belief_dir_path
from src.ch12_belief_file_toolbox.hubunit import HubUnit, hubunit_shop
from src.ch12_belief_file_toolbox.test._util.ch12_env import get_chapter_temp_dir


def test_HubUnit_Exists():
    # ESTABLISH / WHEN
    x_hubunit = HubUnit()

    # THEN
    assert not x_hubunit.moment_mstr_dir
    assert not x_hubunit.moment_label
    assert not x_hubunit.belief_name
    assert not x_hubunit.knot
    assert not x_hubunit.fund_pool
    assert not x_hubunit.fund_grain
    assert not x_hubunit.respect_grain
    assert not x_hubunit.money_grain
    assert not x_hubunit._atoms_dir
    assert not x_hubunit._packs_dir


def test_hubunit_shop_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = "src/ch15_moment_logic/test/_util"
    x_moment_label = "amy45"
    sue_str = "Sue"
    x_knot = "/"
    x_fund_pool = 13000
    x_fund_grain = 13
    x_respect_grain = 9
    x_money_grain = 3
    x_money_magnitude = 900

    # WHEN
    x_hubunit = hubunit_shop(
        moment_mstr_dir=x_moment_mstr_dir,
        moment_label=x_moment_label,
        belief_name=sue_str,
        knot=x_knot,
        fund_pool=x_fund_pool,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
        money_grain=x_money_grain,
    )

    # THEN
    assert x_hubunit.moment_mstr_dir == x_moment_mstr_dir
    assert x_hubunit.moment_label == x_moment_label
    assert x_hubunit.belief_name == sue_str
    assert x_hubunit.knot == x_knot
    assert x_hubunit.fund_pool == x_fund_pool
    assert x_hubunit.fund_grain == x_fund_grain
    assert x_hubunit.respect_grain == x_respect_grain
    assert x_hubunit.money_grain == x_money_grain
    sue_dir = create_belief_dir_path(x_moment_mstr_dir, x_moment_label, sue_str)
    assert x_hubunit._atoms_dir == create_path(sue_dir, "atoms")
    assert x_hubunit._packs_dir == create_path(sue_dir, "packs")


def test_hubunit_shop_ReturnsObjWhenEmpty():
    # ESTABLISH
    sue_str = "Sue"
    moment_mstr_dir = get_chapter_temp_dir()
    amy23_str = "amy23"

    # WHEN
    sue_hubunit = hubunit_shop(moment_mstr_dir, amy23_str, sue_str)

    # THEN
    assert sue_hubunit.moment_mstr_dir == moment_mstr_dir
    assert sue_hubunit.moment_label == amy23_str
    assert sue_hubunit.belief_name == sue_str
    assert sue_hubunit.knot == default_knot_if_None()
    assert sue_hubunit.fund_pool == validate_pool_num()
    assert sue_hubunit.fund_grain == default_grain_num_if_None()
    assert sue_hubunit.respect_grain == default_grain_num_if_None()
    assert sue_hubunit.money_grain == default_grain_num_if_None()


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
