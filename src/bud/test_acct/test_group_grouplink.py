from src.bud.group import groupship_shop
from src.bud.group import groupbox_shop
from pytest import raises as pytest_raises


def test_GroupBox_set_groupship_CorrectlySetsAttr():
    # ESTABLISH
    yao_text = "Yao"
    sue_text = "Sue"
    swim_text = ",swimmers"
    yao_swim_groupship = groupship_shop(swim_text)
    sue_swim_groupship = groupship_shop(swim_text)
    yao_swim_groupship._acct_id = yao_text
    sue_swim_groupship._acct_id = sue_text
    swimmers_groupbox = groupbox_shop(swim_text)

    # WHEN
    swimmers_groupbox.set_groupship(yao_swim_groupship)
    swimmers_groupbox.set_groupship(sue_swim_groupship)

    # THEN
    swimmers_groupships = {
        yao_swim_groupship._acct_id: yao_swim_groupship,
        sue_swim_groupship._acct_id: sue_swim_groupship,
    }
    assert swimmers_groupbox._groupships == swimmers_groupships


def test_GroupBox_set_groupship_SetsAttr_credor_pool_debtor_pool():
    # ESTABLISH
    yao_text = "Yao"
    sue_text = "Sue"
    ohio_text = ",Ohio"
    yao_ohio_groupship = groupship_shop(ohio_text)
    sue_ohio_groupship = groupship_shop(ohio_text)
    yao_ohio_groupship._acct_id = yao_text
    yao_ohio_groupship._acct_id = yao_text
    sue_ohio_groupship._acct_id = sue_text
    yao_ohio_groupship._credor_pool = 66
    sue_ohio_groupship._credor_pool = 22
    yao_ohio_groupship._debtor_pool = 6600
    sue_ohio_groupship._debtor_pool = 2200
    ohio_groupbox = groupbox_shop(ohio_text)
    assert ohio_groupbox._credor_pool == 0
    assert ohio_groupbox._debtor_pool == 0

    # WHEN
    ohio_groupbox.set_groupship(yao_ohio_groupship)
    # THEN
    assert ohio_groupbox._credor_pool == 66
    assert ohio_groupbox._debtor_pool == 6600

    # WHEN
    ohio_groupbox.set_groupship(sue_ohio_groupship)
    # THEN
    assert ohio_groupbox._credor_pool == 88
    assert ohio_groupbox._debtor_pool == 8800


def test_GroupBox_set_groupship_RaisesErrorIf_groupship_group_id_IsWrong():
    # ESTABLISH
    yao_text = "Yao"
    ohio_text = ",Ohio"
    iowa_text = ",Iowa"
    yao_ohio_groupship = groupship_shop(ohio_text)
    yao_ohio_groupship._acct_id = yao_text
    yao_ohio_groupship._acct_id = yao_text
    yao_ohio_groupship._credor_pool = 66
    yao_ohio_groupship._debtor_pool = 6600
    iowa_groupbox = groupbox_shop(iowa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        iowa_groupbox.set_groupship(yao_ohio_groupship)
    assert (
        str(excinfo.value)
        == f"GroupBox.group_id={iowa_text} cannot set groupship.group_id={ohio_text}"
    )


def test_GroupBox_set_groupship_RaisesErrorIf_acct_id_IsNone():
    # ESTABLISH
    ohio_text = ",Ohio"
    ohio_groupbox = groupbox_shop(ohio_text)
    yao_ohio_groupship = groupship_shop(ohio_text)
    assert yao_ohio_groupship._acct_id is None

    with pytest_raises(Exception) as excinfo:
        ohio_groupbox.set_groupship(yao_ohio_groupship)
    assert (
        str(excinfo.value)
        == f"groupship group_id={ohio_text} cannot be set when _acct_id is None."
    )
