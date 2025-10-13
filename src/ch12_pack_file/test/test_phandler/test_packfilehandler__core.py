from pytest import raises as pytest_raises
from src.ch01_py.file_toolbox import create_path
from src.ch02_rope.rope import default_knot_if_None
from src.ch03_allot.allot import default_grain_num_if_None, validate_pool_num
from src.ch12_pack_file._ref.ch12_path import create_belief_dir_path
from src.ch12_pack_file.packfilehandler import PackFileHandler, packfilehandler_shop
from src.ch12_pack_file.test._util.ch12_env import get_chapter_temp_dir


def test_PackFileHandler_Exists():
    # ESTABLISH / WHEN
    x_packfilehandler = PackFileHandler()

    # THEN
    assert not x_packfilehandler.moment_mstr_dir
    assert not x_packfilehandler.moment_label
    assert not x_packfilehandler.belief_name
    assert not x_packfilehandler.knot
    assert not x_packfilehandler.fund_pool
    assert not x_packfilehandler.fund_grain
    assert not x_packfilehandler.respect_grain
    assert not x_packfilehandler.money_grain
    assert not x_packfilehandler._atoms_dir
    assert not x_packfilehandler._packs_dir


def test_packfilehandler_shop_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = "src/ch15_moment/test/_util"
    x_moment_label = "amy45"
    sue_str = "Sue"
    x_knot = "/"
    x_fund_pool = 13000
    x_fund_grain = 13
    x_respect_grain = 9
    x_money_grain = 3
    x_money_magnitude = 900

    # WHEN
    x_packfilehandler = packfilehandler_shop(
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
    assert x_packfilehandler.moment_mstr_dir == x_moment_mstr_dir
    assert x_packfilehandler.moment_label == x_moment_label
    assert x_packfilehandler.belief_name == sue_str
    assert x_packfilehandler.knot == x_knot
    assert x_packfilehandler.fund_pool == x_fund_pool
    assert x_packfilehandler.fund_grain == x_fund_grain
    assert x_packfilehandler.respect_grain == x_respect_grain
    assert x_packfilehandler.money_grain == x_money_grain
    sue_dir = create_belief_dir_path(x_moment_mstr_dir, x_moment_label, sue_str)
    assert x_packfilehandler._atoms_dir == create_path(sue_dir, "atoms")
    assert x_packfilehandler._packs_dir == create_path(sue_dir, "packs")


def test_packfilehandler_shop_ReturnsObjWhenEmpty():
    # ESTABLISH
    sue_str = "Sue"
    moment_mstr_dir = get_chapter_temp_dir()
    amy23_str = "amy23"

    # WHEN
    sue_packfilehandler = packfilehandler_shop(moment_mstr_dir, amy23_str, sue_str)

    # THEN
    assert sue_packfilehandler.moment_mstr_dir == moment_mstr_dir
    assert sue_packfilehandler.moment_label == amy23_str
    assert sue_packfilehandler.belief_name == sue_str
    assert sue_packfilehandler.knot == default_knot_if_None()
    assert sue_packfilehandler.fund_pool == validate_pool_num()
    assert sue_packfilehandler.fund_grain == default_grain_num_if_None()
    assert sue_packfilehandler.respect_grain == default_grain_num_if_None()
    assert sue_packfilehandler.money_grain == default_grain_num_if_None()


def test_packfilehandler_shop_RaisesErrorIf_belief_name_Contains_knot():
    # ESTABLISH
    slash_str = "/"
    bob_str = f"Bob{slash_str}Sue"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        packfilehandler_shop(None, None, belief_name=bob_str, knot=slash_str)
    assertion_fail_str = (
        f"'{bob_str}' needs to be a LabelTerm. Cannot contain knot: '{slash_str}'"
    )
    assert str(excinfo.value) == assertion_fail_str
