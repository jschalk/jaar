from src._world.belieflink import belieflink_shop
from src._world.beliefstory import beliefstory_shop
from pytest import raises as pytest_raises


def test_BeliefStory_set_belieflink_CorrectlySetsAttr():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    swim_text = ",swimmers"
    yao_swim_belieflink = belieflink_shop(swim_text)
    sue_swim_belieflink = belieflink_shop(swim_text)
    yao_swim_belieflink._char_id = yao_text
    sue_swim_belieflink._char_id = sue_text
    swimmers_beliefstory = beliefstory_shop(swim_text)

    # WHEN
    swimmers_beliefstory.set_belieflink(yao_swim_belieflink)
    swimmers_beliefstory.set_belieflink(sue_swim_belieflink)

    # THEN
    swimmers_belieflinks = {
        yao_swim_belieflink._char_id: yao_swim_belieflink,
        sue_swim_belieflink._char_id: sue_swim_belieflink,
    }
    assert swimmers_beliefstory._belieflinks == swimmers_belieflinks


def test_BeliefStory_set_belieflink_SetsAttr_credor_pool_debtor_pool():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    ohio_text = ",Ohio"
    yao_ohio_belieflink = belieflink_shop(ohio_text)
    sue_ohio_belieflink = belieflink_shop(ohio_text)
    yao_ohio_belieflink._char_id = yao_text
    yao_ohio_belieflink._char_id = yao_text
    sue_ohio_belieflink._char_id = sue_text
    yao_ohio_belieflink._credor_pool = 66
    sue_ohio_belieflink._credor_pool = 22
    yao_ohio_belieflink._debtor_pool = 6600
    sue_ohio_belieflink._debtor_pool = 2200
    ohio_beliefstory = beliefstory_shop(ohio_text)
    assert ohio_beliefstory._credor_pool == 0
    assert ohio_beliefstory._debtor_pool == 0

    # WHEN
    ohio_beliefstory.set_belieflink(yao_ohio_belieflink)
    # THEN
    assert ohio_beliefstory._credor_pool == 66
    assert ohio_beliefstory._debtor_pool == 6600

    # WHEN
    ohio_beliefstory.set_belieflink(sue_ohio_belieflink)
    # THEN
    assert ohio_beliefstory._credor_pool == 88
    assert ohio_beliefstory._debtor_pool == 8800


def test_BeliefStory_set_belieflink_RaisesErrorIf_belieflink_belief_id_IsWrong():
    # GIVEN
    yao_text = "Yao"
    ohio_text = ",Ohio"
    iowa_text = ",Iowa"
    yao_ohio_belieflink = belieflink_shop(ohio_text)
    yao_ohio_belieflink._char_id = yao_text
    yao_ohio_belieflink._char_id = yao_text
    yao_ohio_belieflink._credor_pool = 66
    yao_ohio_belieflink._debtor_pool = 6600
    iowa_beliefstory = beliefstory_shop(iowa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        iowa_beliefstory.set_belieflink(yao_ohio_belieflink)
    assert (
        str(excinfo.value)
        == f"BeliefStory.belief_id={iowa_text} cannot set belieflink.belief_id={ohio_text}"
    )


def test_BeliefStory_set_belieflink_RaisesErrorIf_char_id_IsNone():
    # GIVEN
    ohio_text = ",Ohio"
    ohio_beliefstory = beliefstory_shop(ohio_text)
    yao_ohio_belieflink = belieflink_shop(ohio_text)
    assert yao_ohio_belieflink._char_id is None

    with pytest_raises(Exception) as excinfo:
        ohio_beliefstory.set_belieflink(yao_ohio_belieflink)
    assert (
        str(excinfo.value)
        == f"belieflink belief_id={ohio_text} cannot be set when _char_id is None."
    )
