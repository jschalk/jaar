from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch14_keep.rivercycle import get_doctorledger, get_patientledger
from src.ch14_keep.riverrun import riverrun_shop
from src.ch14_keep.test._util.ch14_env import (
    get_temp_dir,
    temp_moment_label,
    temp_moment_mstr_dir,
)


def test_get_patientledger_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_voice_cred_lumen = 8
    bob_voice_cred_lumen = 48
    sue_voice_cred_lumen = 66
    yao_belief = beliefunit_shop(yao_str)
    yao_belief.add_voiceunit(bob_str, yao_voice_cred_lumen)
    yao_belief.add_voiceunit(sue_str, bob_voice_cred_lumen)
    yao_belief.add_voiceunit(yao_str, sue_voice_cred_lumen)

    # WHEN
    yao_patientledger = get_patientledger(yao_belief)

    # THEN
    assert len(yao_patientledger) == 3
    assert yao_patientledger.get(bob_str) == yao_voice_cred_lumen
    assert yao_patientledger.get(sue_str) == bob_voice_cred_lumen
    assert yao_patientledger.get(yao_str) == sue_voice_cred_lumen


def test_get_patientledger_ReturnsObjWithNoEmpty_voice_cred_lumen():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_voice_cred_lumen = 8
    bob_voice_cred_lumen = 0
    sue_voice_cred_lumen = 66
    yao_belief = beliefunit_shop(yao_str)
    yao_belief.add_voiceunit(bob_str, bob_voice_cred_lumen)
    yao_belief.add_voiceunit(sue_str, sue_voice_cred_lumen)
    yao_belief.add_voiceunit(yao_str, yao_voice_cred_lumen)

    # WHEN
    yao_patientledger = get_patientledger(yao_belief)

    # THEN
    assert yao_patientledger.get(bob_str) is None
    assert yao_patientledger.get(sue_str) == sue_voice_cred_lumen
    assert yao_patientledger.get(yao_str) == yao_voice_cred_lumen
    assert len(yao_patientledger) == 2


def test_get_doctorledger_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_voice_debt_lumen = 8
    bob_voice_debt_lumen = 48
    sue_voice_debt_lumen = 66
    yao_belief = beliefunit_shop(yao_str)
    yao_belief.add_voiceunit(bob_str, 2, bob_voice_debt_lumen)
    yao_belief.add_voiceunit(sue_str, 2, sue_voice_debt_lumen)
    yao_belief.add_voiceunit(yao_str, 2, yao_voice_debt_lumen)

    # WHEN
    yao_doctorledger = get_doctorledger(yao_belief)

    # THEN
    assert len(yao_doctorledger) == 3
    assert yao_doctorledger.get(bob_str) == bob_voice_debt_lumen
    assert yao_doctorledger.get(sue_str) == sue_voice_debt_lumen
    assert yao_doctorledger.get(yao_str) == yao_voice_debt_lumen


def test_get_doctorledger_ReturnsObjWithNoEmpty_voice_debt_lumen():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_voice_debt_lumen = 8
    bob_voice_debt_lumen = 48
    sue_voice_debt_lumen = 0
    yao_belief = beliefunit_shop(yao_str)
    yao_belief.add_voiceunit(bob_str, 2, bob_voice_debt_lumen)
    yao_belief.add_voiceunit(sue_str, 2, sue_voice_debt_lumen)
    yao_belief.add_voiceunit(yao_str, 2, yao_voice_debt_lumen)

    # WHEN
    yao_doctorledger = get_doctorledger(yao_belief)

    # THEN
    assert yao_doctorledger.get(bob_str) == bob_voice_debt_lumen
    assert yao_doctorledger.get(sue_str) is None
    assert yao_doctorledger.get(yao_str) == yao_voice_debt_lumen
    assert len(yao_doctorledger) == 2


def test_RiverRun_set_voice_need_due_SetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    mstr_dir = temp_moment_mstr_dir()
    yao_str = "Yao"
    bob_riverrun = riverrun_shop(mstr_dir, None, bob_str)
    yao_str = "Yao"
    assert bob_riverrun.need_dues.get(yao_str) is None

    # WHEN
    yao_need_due = 7
    bob_riverrun.set_voice_need_due(yao_str, yao_need_due)

    # THEN
    assert bob_riverrun.need_dues.get(yao_str) == yao_need_due


def test_RiverRun_need_dues_unpaid_ReturnsObj():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str)
    assert x_riverrun.need_dues_unpaid() is False

    # WHEN
    yao_need_due = 500
    x_riverrun.set_voice_need_due(yao_str, yao_need_due)
    # THEN
    assert x_riverrun.need_dues_unpaid()

    # WHEN
    x_riverrun.delete_need_due(yao_str)
    # THEN
    assert x_riverrun.need_dues_unpaid() is False

    # WHEN
    bob_str = "Bob"
    bob_need_due = 300
    x_riverrun.set_voice_need_due(bob_str, bob_need_due)
    x_riverrun.set_voice_need_due(yao_str, yao_need_due)
    # THEN
    assert x_riverrun.need_dues_unpaid()

    # WHEN
    x_riverrun.delete_need_due(yao_str)
    # THEN
    assert x_riverrun.need_dues_unpaid()


def test_RiverRun_set_need_dues_SetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    bob_mana_amount = 1000
    bob_mana_grain = 1
    bob_riverrun = riverrun_shop(
        None,
        None,
        belief_name=bob_str,
        keep_point_magnitude=bob_mana_amount,
        mana_grain=bob_mana_grain,
    )
    sue_str = "Sue"
    yao_str = "Yao"
    bob_voice_debt_lumen = 38
    sue_voice_debt_lumen = 56
    yao_voice_debt_lumen = 6
    bob_belief = beliefunit_shop(bob_str)
    bob_belief.add_voiceunit(bob_str, 2, bob_voice_debt_lumen)
    bob_belief.add_voiceunit(sue_str, 2, sue_voice_debt_lumen)
    bob_belief.add_voiceunit(yao_str, 2, yao_voice_debt_lumen)
    bob_doctorledger = get_doctorledger(bob_belief)
    assert bob_riverrun.need_dues_unpaid() is False

    # WHEN
    bob_riverrun.set_need_dues(bob_doctorledger)

    # THEN
    assert bob_riverrun.need_dues_unpaid()
    bob_riverrun = bob_riverrun.need_dues
    assert bob_riverrun.get(bob_str) == 380
    assert bob_riverrun.get(sue_str) == 560
    assert bob_riverrun.get(yao_str) == 60


def test_RiverRun_voice_has_need_due_ReturnsBool():
    # ESTABLISH
    bob_str = "Bob"
    bob_mana_amount = 1000
    bob_mana_grain = 1
    bob_riverrun = riverrun_shop(
        None,
        None,
        belief_name=bob_str,
        keep_point_magnitude=bob_mana_amount,
        mana_grain=bob_mana_grain,
    )
    yao_str = "Yao"
    sue_str = "Sue"
    zia_str = "Zia"
    yao_voice_debt_lumen = 6
    bob_voice_debt_lumen = 38
    sue_voice_debt_lumen = 56
    bob_belief = beliefunit_shop(bob_str)
    bob_belief.add_voiceunit(bob_str, 2, bob_voice_debt_lumen)
    bob_belief.add_voiceunit(sue_str, 2, sue_voice_debt_lumen)
    bob_belief.add_voiceunit(yao_str, 2, yao_voice_debt_lumen)
    bob_doctorledger = get_doctorledger(bob_belief)
    assert bob_riverrun.voice_has_need_due(bob_str) is False
    assert bob_riverrun.voice_has_need_due(sue_str) is False
    assert bob_riverrun.voice_has_need_due(yao_str) is False
    assert bob_riverrun.voice_has_need_due(zia_str) is False

    # WHEN
    bob_riverrun.set_need_dues(bob_doctorledger)

    # THEN
    assert bob_riverrun.voice_has_need_due(bob_str)
    assert bob_riverrun.voice_has_need_due(sue_str)
    assert bob_riverrun.voice_has_need_due(yao_str)
    assert bob_riverrun.voice_has_need_due(zia_str) is False


def test_RiverRun_delete_need_due_SetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    bob_mana_amount = 88
    bob_mana_grain = 11
    bob_riverrun = riverrun_shop(
        None,
        None,
        belief_name=bob_str,
        keep_point_magnitude=bob_mana_amount,
        mana_grain=bob_mana_grain,
    )
    yao_str = "Yao"
    bob_riverrun.set_voice_need_due(yao_str, 5)
    assert bob_riverrun.voice_has_need_due(yao_str)

    # WHEN
    bob_riverrun.delete_need_due(yao_str)

    # THEN
    assert bob_riverrun.voice_has_need_due(yao_str) is False


def test_RiverRun_get_voice_need_due_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_mana_amount = 1000
    bob_mana_grain = 1
    bob_riverrun = riverrun_shop(
        None,
        None,
        belief_name=bob_str,
        keep_point_magnitude=bob_mana_amount,
        mana_grain=bob_mana_grain,
    )
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    bob_voice_debt_lumen = 38
    sue_voice_debt_lumen = 56
    yao_voice_debt_lumen = 6
    bob_belief = beliefunit_shop(bob_str)
    bob_belief.add_voiceunit(bob_str, 2, bob_voice_debt_lumen)
    bob_belief.add_voiceunit(sue_str, 2, sue_voice_debt_lumen)
    bob_belief.add_voiceunit(yao_str, 2, yao_voice_debt_lumen)
    bob_doctorledger = get_doctorledger(bob_belief)
    assert bob_riverrun.voice_has_need_due(bob_str) is False
    assert bob_riverrun.get_voice_need_due(bob_str) == 0
    assert bob_riverrun.voice_has_need_due(zia_str) is False
    assert bob_riverrun.get_voice_need_due(zia_str) == 0

    # WHEN
    bob_riverrun.set_need_dues(bob_doctorledger)

    # THEN
    assert bob_riverrun.voice_has_need_due(bob_str)
    assert bob_riverrun.get_voice_need_due(bob_str) == 380
    assert bob_riverrun.voice_has_need_due(zia_str) is False
    assert bob_riverrun.get_voice_need_due(zia_str) == 0


def test_RiverRun_levy_need_due_SetsAttr_ScenarioX():
    # ESTABLISH
    bob_str = "Bob"
    bob_mana_amount = 1000
    bob_mana_grain = 1
    bob_riverrun = riverrun_shop(
        None,
        None,
        belief_name=bob_str,
        keep_point_magnitude=bob_mana_amount,
        mana_grain=bob_mana_grain,
    )
    sue_str = "Sue"
    yao_str = "Yao"
    bob_voice_debt_lumen = 38
    sue_voice_debt_lumen = 56
    yao_voice_debt_lumen = 6
    bob_belief = beliefunit_shop(bob_str)
    bob_belief.add_voiceunit(bob_str, 2, bob_voice_debt_lumen)
    bob_belief.add_voiceunit(sue_str, 2, sue_voice_debt_lumen)
    bob_belief.add_voiceunit(yao_str, 2, yao_voice_debt_lumen)
    bob_doctorledger = get_doctorledger(bob_belief)
    bob_riverrun.set_need_dues(bob_doctorledger)
    assert bob_riverrun.get_voice_need_due(bob_str) == 380, 0

    # WHEN / THEN
    excess_carer_points, need_got = bob_riverrun.levy_need_due(bob_str, 5)
    assert excess_carer_points == 0
    assert need_got == 5
    assert bob_riverrun.get_voice_need_due(bob_str) == 375

    # WHEN /THEN
    excess_carer_points, need_got = bob_riverrun.levy_need_due(bob_str, 375)
    assert excess_carer_points == 0
    assert need_got == 375
    assert bob_riverrun.get_voice_need_due(bob_str) == 0
    assert bob_riverrun.voice_has_need_due(bob_str) is False

    # WHEN / THEN
    assert bob_riverrun.get_voice_need_due(sue_str) == 560
    excess_carer_points, need_got = bob_riverrun.levy_need_due(sue_str, 1000)
    assert excess_carer_points == 440
    assert need_got == 560
    assert bob_riverrun.get_voice_need_due(sue_str) == 0
    assert bob_riverrun.need_dues.get(sue_str) is None

    # WHEN / THEN
    zia_str = "Zia"
    excess_carer_points, need_got = bob_riverrun.levy_need_due(zia_str, 1000)
    assert excess_carer_points == 1000
    assert need_got == 0
    assert bob_riverrun.get_voice_need_due(zia_str) == 0

    # WHEN / THEN
    assert bob_riverrun.get_voice_need_due(yao_str) == 60
    excess_carer_points, need_got = bob_riverrun.levy_need_due(yao_str, 81)
    assert excess_carer_points == 21
    assert need_got == 60
    assert bob_riverrun.get_voice_need_due(yao_str) == 0
