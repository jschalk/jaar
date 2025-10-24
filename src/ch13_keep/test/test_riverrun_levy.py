from src.ch13_keep.riverrun import riverrun_shop
from src.ch13_keep.test._util.ch13_env import (
    get_temp_dir,
    temp_moment_label,
    temp_moment_mstr_dir,
)


def test_RiverRun_levy_need_dues_Molds_cycleledger_Scenario01():
    # ESTABLISH / WHEN
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    yao_need_due = 222
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str)
    x_riverrun.set_voice_need_due(yao_str, yao_need_due)

    yao_paid = 500
    x_cycleledger = {yao_str: yao_paid}
    assert x_riverrun.get_voice_need_due(yao_str) == yao_need_due
    assert x_cycleledger.get(yao_str) == yao_paid

    # WHEN
    y_cycleledger, need_got = x_riverrun.levy_need_dues(x_cycleledger)

    # THEN
    assert x_riverrun.get_voice_need_due(yao_str) == 0
    assert need_got == 222
    assert y_cycleledger.get(yao_str) == yao_paid - yao_need_due


def test_RiverRun_levy_need_dues_Molds_cycleledger_Scenario02():
    # ESTABLISH / WHEN
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    bob_str = "Bob"
    yao_need_due = 222
    bob_need_due = 127
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str)
    x_riverrun.set_voice_need_due(yao_str, yao_need_due)
    x_riverrun.set_voice_need_due(bob_str, bob_need_due)

    yao_paid = 500
    bob_paid = 100
    x_cycleledger = {yao_str: yao_paid, bob_str: bob_paid}
    assert x_riverrun.get_voice_need_due(yao_str) == yao_need_due
    assert x_riverrun.get_voice_need_due(bob_str) == bob_need_due
    assert x_cycleledger.get(yao_str) == yao_paid
    assert x_cycleledger.get(bob_str) == bob_paid

    # WHEN
    y_cycleledger, need_got = x_riverrun.levy_need_dues(x_cycleledger)

    # THEN
    assert x_riverrun.get_voice_need_due(yao_str) == 0
    assert x_riverrun.get_voice_need_due(bob_str) == 27
    assert y_cycleledger.get(yao_str) == yao_paid - yao_need_due
    assert y_cycleledger.get(bob_str) is None
    assert need_got == 322


def test_RiverRun_cycle_carees_vary_ReturnsObj():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str)
    # WHEN / THEN
    assert x_riverrun._cycle_carees_vary() is False

    x_riverrun.cycle_carees_prev = {yao_str}
    assert x_riverrun.cycle_carees_prev == {yao_str}
    assert x_riverrun.cycle_carees_curr == set()

    # WHEN / THEN
    assert x_riverrun._cycle_carees_vary()


def test_RiverRun_cycles_vary_ReturnsObj():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    yao_need_got = 5
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str)
    assert x_riverrun._cycle_carees_vary() is False
    assert x_riverrun._need_gotten() is False
    assert x_riverrun.cycles_vary() is False

    # WHEN
    x_riverrun.cycle_carees_prev = {yao_str}
    # THEN
    assert x_riverrun._cycle_carees_vary()
    assert x_riverrun._need_gotten() is False
    assert x_riverrun.cycles_vary()

    # WHEN
    x_riverrun._set_need_got_attrs(yao_need_got)
    # THEN
    assert x_riverrun._cycle_carees_vary()
    assert x_riverrun._need_gotten()
    assert x_riverrun.cycles_vary()

    # WHEN
    x_riverrun.cycle_carees_curr = {yao_str}
    # THEN
    assert x_riverrun._cycle_carees_vary() is False
    assert x_riverrun._need_gotten()
    assert x_riverrun.cycles_vary()
