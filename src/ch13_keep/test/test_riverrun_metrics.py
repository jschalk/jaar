from src.ch13_keep.riverrun import riverrun_shop
from src.ch13_keep.test._util.ch13_env import get_temp_dir, temp_moment_label


def test_RiverRun_calc_metrics_SetsAttrsScenario01():
    # ESTABLISH / WHEN
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    yao_voice_cred_lumen = 500
    x_keep_point_magnitude = 444
    x_riverrun = riverrun_shop(
        mstr_dir, a23_str, yao_str, keep_point_magnitude=x_keep_point_magnitude
    )
    x_riverrun.set_keep_patientledger(yao_str, yao_str, yao_voice_cred_lumen)
    assert x_riverrun.get_voice_need_due(yao_str) == 0

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_voice_need_due(yao_str) == 0
    assert x_riverrun._cycle_count == 1
    assert x_riverrun._doctor_count == 0
    assert x_riverrun._patient_count == 1
    yao_rivergrade = x_riverrun.get_rivergrade(yao_str)
    assert yao_rivergrade is not None
    assert yao_rivergrade.moment_label == a23_str
    assert yao_rivergrade.belief_name == yao_str
    assert yao_rivergrade.keep_rope is None
    assert yao_rivergrade.number == 0
    assert yao_rivergrade.care_amount == x_keep_point_magnitude
    assert yao_rivergrade.need_bill_amount == 0
    assert yao_rivergrade.need_paid_amount == 0
    assert yao_rivergrade.need_paid_bool
    # assert yao_rivergrade.need_paid_rank_num == 1
    # assert yao_rivergrade.need_paid_rank_percent == 1.0
    # assert yao_rivergrade.doctor_rank_num is None
    # assert yao_rivergrade.patient_rank_num == 1
    # assert yao_rivergrade.doctor_rank_percent == 1.0
    # assert yao_rivergrade.doctor_count == 0
    # assert yao_rivergrade.patient_count == 1
    # assert yao_rivergrade.patient_rank_percent == 1.0
    # assert yao_rivergrade.rewards_count == 1
    # assert yao_rivergrade.rewards_magnitude == 500


def test_RiverRun_calc_metrics_SetsAttrsScenario02():
    # ESTABLISH / WHEN
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    yao_voice_cred_lumen = 500
    bob_str = "Bob"
    bob_voice_debt_lumen = 350
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str)
    x_riverrun.set_keep_patientledger(yao_str, yao_str, yao_voice_cred_lumen)
    x_riverrun.set_need_dues({bob_str: bob_voice_debt_lumen})
    assert x_riverrun.get_voice_need_due(yao_str) == 0
    keep_mana_amount = x_riverrun.keep_point_magnitude
    assert x_riverrun.get_voice_need_due(bob_str) == keep_mana_amount

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_voice_need_due(yao_str) == 0
    assert x_riverrun.get_voice_need_due(bob_str) == keep_mana_amount
    assert x_riverrun._cycle_count == 1
    assert x_riverrun._doctor_count == 1
    assert x_riverrun._patient_count == 1
    yao_rivergrade = x_riverrun.get_rivergrade(yao_str)
    assert yao_rivergrade is not None
    assert yao_rivergrade.moment_label == a23_str
    assert yao_rivergrade.belief_name == yao_str
    assert yao_rivergrade.keep_rope is None
    assert yao_rivergrade.number == 0
    assert yao_rivergrade.care_amount == keep_mana_amount
    assert yao_rivergrade.need_bill_amount == 0
    assert yao_rivergrade.need_paid_amount == 0
    assert yao_rivergrade.need_paid_bool
    # assert yao_rivergrade.need_paid_rank_num == 1
    # assert yao_rivergrade.need_paid_rank_percent == 1.0
    # assert yao_rivergrade.doctor_rank_num is None
    # assert yao_rivergrade.patient_rank_num == 1
    # assert yao_rivergrade.doctor_rank_percent == 1.0
    # assert yao_rivergrade.doctor_count == 0
    # assert yao_rivergrade.patient_count == 1
    # assert yao_rivergrade.patient_rank_percent == 1.0
    # assert yao_rivergrade.rewards_count == 1
    # assert yao_rivergrade.rewards_magnitude == 500


def test_RiverRun_calc_metrics_SetsAttrsScenario03():
    # ESTABLISH / WHEN
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    yao_voice_cred_lumen = 500
    bob_str = "Bob"
    bob_voice_debt_lumen = 25
    sue_str = "Sue"
    sue_voice_debt_lumen = 75
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str)
    x_riverrun.set_keep_patientledger(yao_str, yao_str, yao_voice_cred_lumen)
    doctorledger = {bob_str: bob_voice_debt_lumen, sue_str: sue_voice_debt_lumen}
    x_riverrun.set_need_dues(doctorledger)
    assert x_riverrun.get_voice_need_due(yao_str) == 0
    keep_mana_amount = x_riverrun.keep_point_magnitude
    assert x_riverrun.get_voice_need_due(bob_str) == keep_mana_amount * 0.25
    assert x_riverrun.get_voice_need_due(sue_str) == keep_mana_amount * 0.75

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_voice_need_due(yao_str) == 0
    assert x_riverrun.get_voice_need_due(bob_str) == keep_mana_amount * 0.25
    assert x_riverrun.get_voice_need_due(sue_str) == keep_mana_amount * 0.75
    assert x_riverrun._cycle_count == 1
    assert x_riverrun._doctor_count == 2
    assert x_riverrun._patient_count == 1
    yao_rivergrade = x_riverrun.get_rivergrade(yao_str)
    assert yao_rivergrade is not None
    assert yao_rivergrade.moment_label == a23_str
    assert yao_rivergrade.belief_name == yao_str
    assert yao_rivergrade.keep_rope is None
    assert yao_rivergrade.number == 0
    assert yao_rivergrade.care_amount == keep_mana_amount
    assert yao_rivergrade.need_bill_amount == 0
    assert yao_rivergrade.need_paid_amount == 0
    assert yao_rivergrade.need_paid_bool
    # assert yao_rivergrade.need_paid_rank_num == 1
    # assert yao_rivergrade.need_paid_rank_percent == 1.0
    # assert yao_rivergrade.doctor_rank_num is None
    # assert yao_rivergrade.patient_rank_num == 1
    # assert yao_rivergrade.doctor_rank_percent == 1.0
    # assert yao_rivergrade.doctor_count == 0
    # assert yao_rivergrade.patient_count == 1
    # assert yao_rivergrade.patient_rank_percent == 1.0
    # assert yao_rivergrade.rewards_count == 1
    # assert yao_rivergrade.rewards_magnitude == 500


def test_RiverRun_calc_metrics_SetsAttrsScenario04():
    # ESTABLISH / WHEN
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    yao_yao_voice_cred_lumen = 500
    yao_sue_voice_cred_lumen = 2000
    bob_str = "Bob"
    bob_voice_debt_lumen = 25
    sue_str = "Sue"
    sue_voice_debt_lumen = 75
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str)
    x_riverrun.set_keep_patientledger(yao_str, yao_str, yao_yao_voice_cred_lumen)
    x_riverrun.set_keep_patientledger(yao_str, sue_str, yao_sue_voice_cred_lumen)
    doctorledger = {bob_str: bob_voice_debt_lumen, sue_str: sue_voice_debt_lumen}
    x_riverrun.set_need_dues(doctorledger)
    assert x_riverrun.get_voice_need_due(yao_str) == 0
    keep_mana_amount = x_riverrun.keep_point_magnitude
    assert x_riverrun.get_voice_need_due(bob_str) == keep_mana_amount * 0.25
    assert x_riverrun.get_voice_need_due(sue_str) == keep_mana_amount * 0.75

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_voice_need_due(yao_str) == 0
    assert x_riverrun.get_voice_need_due(bob_str) == keep_mana_amount * 0.25
    assert x_riverrun.get_voice_need_due(sue_str) == 0
    assert x_riverrun.get_voice_need_yield(sue_str) == keep_mana_amount * 0.75
    assert x_riverrun._cycle_count == 2
    assert x_riverrun._doctor_count == 2
    assert x_riverrun._patient_count == 2
    yao_rivergrade = x_riverrun.get_rivergrade(yao_str)
    sue_rivergrade = x_riverrun.get_rivergrade(sue_str)
    assert yao_rivergrade.care_amount == keep_mana_amount * 0.2
    assert sue_rivergrade.care_amount == keep_mana_amount * 0.8
    assert yao_rivergrade.need_bill_amount == 0
    assert yao_rivergrade.need_paid_amount == 0
    assert yao_rivergrade.need_paid_bool
    # assert yao_rivergrade.need_paid_rank_num == 1
    # assert yao_rivergrade.need_paid_rank_percent == 1.0
    # assert yao_rivergrade.doctor_rank_num is None
    # assert yao_rivergrade.patient_rank_num == 1
    # assert yao_rivergrade.doctor_rank_percent == 1.0
    # assert yao_rivergrade.doctor_count == 0
    # assert yao_rivergrade.patient_count == 1
    # assert yao_rivergrade.patient_rank_percent == 1.0
    # assert yao_rivergrade.rewards_count == 1
    # assert yao_rivergrade.rewards_magnitude == 500


def test_RiverRun_calc_metrics_SetsAttrsScenario05():
    # ESTABLISH / WHEN
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    yao_voice_cred_lumen = 500
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str)
    x_riverrun.set_keep_patientledger(yao_str, yao_str, yao_voice_cred_lumen)
    x_riverrun.set_need_dues({yao_str: 1})
    keep_mana_amount = x_riverrun.keep_point_magnitude
    assert x_riverrun.get_voice_need_due(yao_str) == keep_mana_amount
    assert x_riverrun.get_voice_need_yield(yao_str) == 0

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_voice_need_due(yao_str) == 0
    assert x_riverrun.get_voice_need_yield(yao_str) == keep_mana_amount
    assert x_riverrun._cycle_count == 2
    assert x_riverrun._doctor_count == 1
    assert x_riverrun._patient_count == 1
    yao_rivergrade = x_riverrun.get_rivergrade(yao_str)
    assert yao_rivergrade is not None
    assert yao_rivergrade.moment_label == a23_str
    assert yao_rivergrade.belief_name == yao_str
    assert yao_rivergrade.keep_rope is None
    assert yao_rivergrade.number == 0
    assert yao_rivergrade.care_amount == keep_mana_amount
    assert yao_rivergrade.need_bill_amount == keep_mana_amount
    assert yao_rivergrade.need_paid_amount == keep_mana_amount
    assert yao_rivergrade.need_paid_bool


def test_RiverRun_calc_metrics_EachTimeResets_need_yield():
    # ESTABLISH / WHEN
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    yao_voice_cred_lumen = 500
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str)
    x_riverrun.set_keep_patientledger(yao_str, yao_str, yao_voice_cred_lumen)
    x_riverrun.set_need_dues({yao_str: 1})
    keep_mana_amount = x_riverrun.keep_point_magnitude
    x_riverrun.calc_metrics()
    assert x_riverrun.get_voice_need_due(yao_str) == 0
    assert x_riverrun.get_voice_need_yield(yao_str) == keep_mana_amount

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_voice_need_due(yao_str) == 0
    assert x_riverrun.get_voice_need_yield(yao_str) == keep_mana_amount


def test_RiverRun_calc_metrics_EndsRiverCycleLoopIfNoDifferencesBetweenCycles():
    # ESTABLISH / WHEN
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str)
    bob_str = "Bob"
    x_riverrun.set_keep_patientledger(yao_str, yao_str, 1)
    x_riverrun.set_need_dues({bob_str: 1})
    keep_mana_amount = x_riverrun.keep_point_magnitude
    assert x_riverrun.get_voice_need_due(yao_str) == 0
    assert x_riverrun.get_voice_need_due(bob_str) == keep_mana_amount
    assert x_riverrun._cycle_count == 0
    assert x_riverrun._cycle_carees_prev == set()
    assert x_riverrun._cycle_carees_curr == set()

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun._cycle_carees_prev == {yao_str}
    assert x_riverrun._cycle_carees_curr == {yao_str}
    assert x_riverrun.get_voice_need_due(yao_str) == 0
    assert x_riverrun.get_voice_need_due(bob_str) == keep_mana_amount
    assert x_riverrun._cycle_count == 1
