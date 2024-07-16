from src._world.char import charlink_shop
from src._world.belieflink import belieflink_shop
from src._world.beliefstory import beliefbox_shop
from src._world.world import worldunit_shop


def test_WorldUnit_get_belief_ids_dict_ReturnsObj():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    zia_text = "Zia"
    bob_world = worldunit_shop("Bob")
    bob_world.add_charunit(yao_text)
    bob_world.add_charunit(sue_text)
    bob_world.add_charunit(zia_text)
    sue_charunit = bob_world.get_char(sue_text)
    zia_charunit = bob_world.get_char(zia_text)
    run_text = ",Run"
    swim_text = ",Swim"
    sue_charunit.add_belieflink(run_text)
    zia_charunit.add_belieflink(run_text)
    zia_charunit.add_belieflink(swim_text)

    # WHEN
    belief_ids_dict = bob_world.get_belief_ids_dict()

    # THEN
    print(f"{belief_ids_dict=}")
    all_belief_ids = {yao_text, sue_text, zia_text, run_text, swim_text}
    assert set(belief_ids_dict.keys()) == all_belief_ids
    assert set(belief_ids_dict.keys()) != {swim_text, run_text}
    assert belief_ids_dict.get(swim_text) == {zia_text}
    assert belief_ids_dict.get(run_text) == {zia_text, sue_text}
    assert belief_ids_dict.get(yao_text) == {yao_text}
    assert belief_ids_dict.get(sue_text) == {sue_text}
    assert belief_ids_dict.get(zia_text) == {zia_text}
