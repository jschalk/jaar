from src.ch03_allot.allot import default_grain_num_if_None, validate_pool_num
from src.ch14_keep._ref.ch14_semantic_types import default_knot_if_None
from src.ch14_keep.riverrun import RiverRun, riverrun_shop
from src.ch14_keep.test._util.ch14_env import get_temp_dir, temp_moment_label
from src.ch14_keep.test._util.ch14_examples import (
    example_yao_bob_zia_credorledgers,
    example_yao_bob_zia_tax_dues,
)
from src.ref.keywords import Ch14Keywords as kw


def test_RiverRun_Exists():
    # ESTABLISH / WHEN
    x_riverrun = RiverRun()

    # THEN
    assert not x_riverrun.moment_mstr_dir
    assert not x_riverrun.moment_label
    assert not x_riverrun.belief_name
    assert not x_riverrun.keep_rope
    assert not x_riverrun.knot
    assert not x_riverrun.keep_point_magnitude
    assert not x_riverrun.money_grain
    assert not x_riverrun.number
    assert not x_riverrun.keep_credorledgers
    assert not x_riverrun.tax_dues
    assert not x_riverrun.cycle_max
    # calculated fields
    assert not x_riverrun._rivergrades
    assert not x_riverrun._grants
    assert not x_riverrun._tax_yields
    assert not x_riverrun._tax_got_prev
    assert not x_riverrun._tax_got_curr
    assert not x_riverrun._cycle_count
    assert not x_riverrun._cycle_chargeees_prev
    assert not x_riverrun._cycle_chargeees_curr
    assert not x_riverrun._debtor_count
    assert not x_riverrun._credor_count
    assert set(x_riverrun.__dict__.keys()) == {
        kw.moment_mstr_dir,
        kw.moment_label,
        kw.belief_name,
        kw.keep_rope,
        kw.knot,
        kw.keep_point_magnitude,
        kw.money_grain,
        "number",
        kw.keep_credorledgers,
        kw.tax_dues,
        kw.cycle_max,
        kw._rivergrades,
        kw._grants,
        kw._tax_yields,
        kw._tax_got_prev,
        kw._tax_got_curr,
        kw._cycle_count,
        kw._cycle_chargeees_prev,
        kw._cycle_chargeees_curr,
        kw._debtor_count,
        kw._credor_count,
    }


def test_RiverRun_set_cycle_max_SetsAttr():
    # ESTABLISH
    x_riverrun = RiverRun()
    assert not x_riverrun.cycle_max

    # WHEN / THEN
    x_riverrun.set_cycle_max(10)
    assert x_riverrun.cycle_max == 10

    # WHEN / THEN
    x_riverrun.set_cycle_max(10.0)
    assert x_riverrun.cycle_max == 10

    # WHEN / THEN
    x_riverrun.set_cycle_max(-10.0)
    assert x_riverrun.cycle_max == 0

    # WHEN / THEN
    x_riverrun.set_cycle_max(10.8)
    assert x_riverrun.cycle_max == 10


def test_riverrun_shop_ReturnsObj_Scenario0_WithArgs():
    # ESTABLISH
    ten_int = 10
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    x_keep_rope = ";fizz;"
    x_knot = ";"
    x_keep_point_magnitude = 333
    x_money_grain = 3
    keep_credorledgers = example_yao_bob_zia_credorledgers()
    x_cycle_max = 10
    x_tax_dues = example_yao_bob_zia_tax_dues()

    # WHEN
    x_riverrun = riverrun_shop(
        moment_mstr_dir=mstr_dir,
        moment_label=a23_str,
        belief_name=yao_str,
        keep_rope=x_keep_rope,
        knot=x_knot,
        keep_point_magnitude=x_keep_point_magnitude,
        money_grain=x_money_grain,
        number=ten_int,
        keep_credorledgers=keep_credorledgers,
        tax_dues=x_tax_dues,
        cycle_max=x_cycle_max,
    )

    # THEN
    assert x_riverrun.moment_mstr_dir == mstr_dir
    assert x_riverrun.moment_label == a23_str
    assert x_riverrun.belief_name == yao_str
    assert x_riverrun.keep_rope == x_keep_rope
    assert x_riverrun.knot == x_knot
    assert x_riverrun.keep_point_magnitude == x_keep_point_magnitude
    assert x_riverrun.money_grain == x_money_grain
    assert x_riverrun.number == ten_int
    assert x_riverrun.keep_credorledgers == keep_credorledgers
    assert x_riverrun.tax_dues == x_tax_dues
    assert x_riverrun.cycle_max == x_cycle_max
    assert x_riverrun._rivergrades == {}
    assert x_riverrun._grants == {}
    assert x_riverrun._tax_yields == {}
    assert x_riverrun._tax_got_prev == 0
    assert x_riverrun._tax_got_curr == 0
    assert x_riverrun._cycle_count == 0
    assert x_riverrun._cycle_chargeees_prev == set()
    assert x_riverrun._cycle_chargeees_curr == set()


def test_riverrun_shop_ReturnsObj_Scenario1_WithoutArgs():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"

    # WHEN
    x_riverrun = riverrun_shop(
        moment_mstr_dir=mstr_dir,
        moment_label=a23_str,
        belief_name=yao_str,
    )

    # THEN
    assert x_riverrun.moment_mstr_dir == mstr_dir
    assert x_riverrun.moment_label == a23_str
    assert x_riverrun.belief_name == yao_str
    assert x_riverrun.keep_rope == None
    assert x_riverrun.knot == default_knot_if_None()
    assert x_riverrun.keep_point_magnitude == validate_pool_num()
    assert x_riverrun.money_grain == default_grain_num_if_None()
    assert x_riverrun.number == 0
    assert x_riverrun.keep_credorledgers == {}
    assert x_riverrun.tax_dues == {}
    assert x_riverrun._rivergrades == {}
    assert x_riverrun._grants == {}
    assert x_riverrun._tax_yields == {}
    assert x_riverrun._cycle_count == 0
    assert x_riverrun.cycle_max == 10


def test_RiverRun_set_keep_credorledger_SetsAttr():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    yao_voice_cred_lumen = 500
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str)
    assert x_riverrun.keep_credorledgers == {}

    # WHEN
    x_riverrun.set_keep_credorledger(
        belief_name=yao_str,
        voice_name=yao_str,
        credit_ledger=yao_voice_cred_lumen,
    )

    # THEN
    assert x_riverrun.keep_credorledgers == {yao_str: {yao_str: yao_voice_cred_lumen}}


def test_RiverRun_delete_keep_credorledgers_belief_SetsAttr():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str)
    x_riverrun.set_keep_credorledger(yao_str, yao_str, 1)
    x_riverrun.set_keep_credorledger(bob_str, bob_str, 1)
    x_riverrun.set_keep_credorledger(bob_str, sue_str, 1)
    assert x_riverrun.keep_credorledgers == {
        yao_str: {yao_str: 1},
        bob_str: {bob_str: 1, sue_str: 1},
    }

    # WHEN
    x_riverrun.delete_keep_credorledgers_belief(bob_str)

    # THEN
    assert x_riverrun.keep_credorledgers == {yao_str: {yao_str: 1}}


def test_RiverRun_get_all_keep_credorledger_voice_names_ReturnsObj():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    zia_str = "Zia"
    xio_str = "Xio"
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str)

    # WHEN
    all_voices_ids = x_riverrun.get_all_keep_credorledger_voice_names()
    # THEN
    assert all_voices_ids == set()

    # WHEN
    x_riverrun.set_keep_credorledger(yao_str, yao_str, 1)
    x_riverrun.set_keep_credorledger(yao_str, bob_str, 1)
    all_voices_ids = x_riverrun.get_all_keep_credorledger_voice_names()
    # THEN
    assert all_voices_ids == {yao_str, bob_str}

    # WHEN
    x_riverrun.set_keep_credorledger(zia_str, bob_str, 1)
    all_voices_ids = x_riverrun.get_all_keep_credorledger_voice_names()
    # THEN
    assert all_voices_ids == {yao_str, bob_str, zia_str}

    # WHEN
    x_riverrun.set_keep_credorledger(xio_str, sue_str, 1)
    all_voices_ids = x_riverrun.get_all_keep_credorledger_voice_names()
    # THEN
    assert all_voices_ids == {yao_str, bob_str, zia_str, xio_str, sue_str}
