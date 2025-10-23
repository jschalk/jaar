from src.ch13_keep.rivercycle import rivergrade_shop
from src.ch13_keep.riverrun import riverrun_shop
from src.ch13_keep.test._util.ch13_env import get_temp_dir, temp_moment_label


def test_RiverRun_set_initial_rivergrade_SetsAttr():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    yao_number = 8
    yao_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str, number=yao_number)
    x_doctor_count = 5
    x_patient_count = 8
    yao_riverrun._doctor_count = x_doctor_count
    yao_riverrun._patient_count = x_patient_count
    bob_str = "Bob"
    assert yao_riverrun._rivergrades.get(bob_str) is None

    # WHEN
    yao_riverrun.set_initial_rivergrade(bob_str)

    # THEN
    bob_rivergrade = rivergrade_shop(
        a23_str,
        yao_str,
        None,
        bob_str,
        yao_number,
        x_doctor_count,
        x_patient_count,
    )
    bob_rivergrade.care_amount = 0
    assert yao_riverrun._rivergrades.get(bob_str) is not None
    gen_rivergrade = yao_riverrun._rivergrades.get(bob_str)
    assert gen_rivergrade.doctor_count == x_doctor_count
    assert gen_rivergrade.patient_count == x_patient_count
    assert gen_rivergrade == bob_rivergrade


def test_RiverRun_rivergrades_is_empty_ReturnsObj():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    yao_number = 8
    yao_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str, number=yao_number)

    assert yao_riverrun._rivergrades_is_empty()

    # WHEN
    bob_str = "Bob"
    yao_riverrun.set_initial_rivergrade(bob_str)

    # THEN
    assert yao_riverrun._rivergrades_is_empty() is False


def test_RiverRun_rivergrade_exists_ReturnsObj():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    yao_number = 8
    yao_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str, yao_number)
    yao_riverrun.set_initial_rivergrade("Yao")

    bob_str = "Bob"
    assert yao_riverrun.rivergrade_exists(bob_str) is False
    assert yao_riverrun._rivergrades_is_empty() is False

    # WHEN
    yao_riverrun.set_initial_rivergrade(bob_str)

    # THEN
    assert yao_riverrun.rivergrade_exists(bob_str)
    assert yao_riverrun._rivergrades_is_empty() is False


def test_RiverRun_set_all_initial_rivergrades_SetsAttr():
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    zia_str = "Zia"
    xio_str = "Xio"
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str)
    x_riverrun.set_keep_patientledger(yao_str, yao_str, 1)
    x_riverrun.set_keep_patientledger(yao_str, bob_str, 1)
    x_riverrun.set_keep_patientledger(zia_str, bob_str, 1)
    x_riverrun.set_keep_patientledger(xio_str, sue_str, 1)
    all_voices_ids = x_riverrun.get_all_keep_patientledger_voice_names()
    assert all_voices_ids == {yao_str, bob_str, zia_str, xio_str, sue_str}
    assert x_riverrun._rivergrades_is_empty()
    assert x_riverrun.rivergrade_exists(yao_str) is False
    assert x_riverrun.rivergrade_exists(bob_str) is False
    assert x_riverrun.rivergrade_exists(zia_str) is False

    # WHEN
    x_riverrun.set_all_initial_rivergrades()

    # THEN
    assert x_riverrun._rivergrades_is_empty() is False
    assert x_riverrun.rivergrade_exists(yao_str)
    assert x_riverrun.rivergrade_exists(bob_str)
    assert x_riverrun.rivergrade_exists(zia_str)


def test_RiverRun_set_all_initial_rivergrades_OverWritesPrevious():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = temp_moment_label()
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    zia_str = "Zia"
    xio_str = "Xio"
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str)
    x_riverrun.set_keep_patientledger(yao_str, yao_str, 1)
    x_riverrun.set_keep_patientledger(yao_str, bob_str, 1)
    x_riverrun.set_keep_patientledger(zia_str, bob_str, 1)
    x_riverrun.set_keep_patientledger(xio_str, sue_str, 1)
    x_riverrun.set_all_initial_rivergrades()
    assert x_riverrun.rivergrade_exists(yao_str)
    assert x_riverrun.rivergrade_exists(bob_str)
    assert x_riverrun.rivergrade_exists(zia_str)
    assert x_riverrun.rivergrade_exists(xio_str)
    assert x_riverrun.rivergrade_exists(sue_str)

    # WHEN
    x_riverrun.delete_keep_patientledgers_belief(xio_str)
    x_riverrun.set_all_initial_rivergrades()

    # THEN
    assert x_riverrun.rivergrade_exists(yao_str)
    assert x_riverrun.rivergrade_exists(bob_str)
    assert x_riverrun.rivergrade_exists(zia_str)
    assert x_riverrun.rivergrade_exists(xio_str) is False
    assert x_riverrun.rivergrade_exists(sue_str) is False
