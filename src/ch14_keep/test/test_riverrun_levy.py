from src.ch14_keep.riverrun import riverrun_shop
from src.ch14_keep.test._util.ch14_env import (
    get_chapter_temp_dir,
    temp_moment_label,
    temp_moment_mstr_dir,
)


def test_RiverRun_levy_tax_dues_Molds_cycleledger_Scenario01():
    # ESTABLISH / WHEN
    mstr_dir = get_chapter_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    yao_tax_due = 222
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str)
    x_riverrun.set_voice_tax_due(yao_str, yao_tax_due)

    yao_paid = 500
    x_cycleledger = {yao_str: yao_paid}
    assert x_riverrun.get_voice_tax_due(yao_str) == yao_tax_due
    assert x_cycleledger.get(yao_str) == yao_paid

    # WHEN
    y_cycleledger, tax_got = x_riverrun.levy_tax_dues(x_cycleledger)

    # THEN
    assert x_riverrun.get_voice_tax_due(yao_str) == 0
    assert tax_got == 222
    assert y_cycleledger.get(yao_str) == yao_paid - yao_tax_due


def test_RiverRun_levy_tax_dues_Molds_cycleledger_Scenario02():
    # ESTABLISH / WHEN
    mstr_dir = get_chapter_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    bob_str = "Bob"
    yao_tax_due = 222
    bob_tax_due = 127
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str)
    x_riverrun.set_voice_tax_due(yao_str, yao_tax_due)
    x_riverrun.set_voice_tax_due(bob_str, bob_tax_due)

    yao_paid = 500
    bob_paid = 100
    x_cycleledger = {yao_str: yao_paid, bob_str: bob_paid}
    assert x_riverrun.get_voice_tax_due(yao_str) == yao_tax_due
    assert x_riverrun.get_voice_tax_due(bob_str) == bob_tax_due
    assert x_cycleledger.get(yao_str) == yao_paid
    assert x_cycleledger.get(bob_str) == bob_paid

    # WHEN
    y_cycleledger, tax_got = x_riverrun.levy_tax_dues(x_cycleledger)

    # THEN
    assert x_riverrun.get_voice_tax_due(yao_str) == 0
    assert x_riverrun.get_voice_tax_due(bob_str) == 27
    assert y_cycleledger.get(yao_str) == yao_paid - yao_tax_due
    assert y_cycleledger.get(bob_str) is None
    assert tax_got == 322


def test_RiverRun_cycle_chargeees_vary_ReturnsObj():
    # ESTABLISH
    mstr_dir = get_chapter_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str)
    # WHEN / THEN
    assert x_riverrun._cycle_chargeees_vary() is False

    x_riverrun._cycle_chargeees_prev = {yao_str}
    assert x_riverrun._cycle_chargeees_prev == {yao_str}
    assert x_riverrun._cycle_chargeees_curr == set()

    # WHEN / THEN
    assert x_riverrun._cycle_chargeees_vary()


def test_RiverRun_cycles_vary_ReturnsObj():
    # ESTABLISH
    mstr_dir = get_chapter_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    yao_tax_got = 5
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str)
    assert x_riverrun._cycle_chargeees_vary() is False
    assert x_riverrun._tax_gotten() is False
    assert x_riverrun.cycles_vary() is False

    # WHEN
    x_riverrun._cycle_chargeees_prev = {yao_str}
    # THEN
    assert x_riverrun._cycle_chargeees_vary()
    assert x_riverrun._tax_gotten() is False
    assert x_riverrun.cycles_vary()

    # WHEN
    x_riverrun._set_tax_got_attrs(yao_tax_got)
    # THEN
    assert x_riverrun._cycle_chargeees_vary()
    assert x_riverrun._tax_gotten()
    assert x_riverrun.cycles_vary()

    # WHEN
    x_riverrun._cycle_chargeees_curr = {yao_str}
    # THEN
    assert x_riverrun._cycle_chargeees_vary() is False
    assert x_riverrun._tax_gotten()
    assert x_riverrun.cycles_vary()
