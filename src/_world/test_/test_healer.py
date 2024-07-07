from src._world.healer import HealerHold, healerhold_shop, healerhold_get_from_dict
from src._world.beliefunit import BeliefID


def test_HealerHold_exists():
    # GIVEN
    run_text = ",runners"
    run_belief_ids = {run_text}

    # WHEN
    x_healerhold = HealerHold(_belief_ids=run_belief_ids)

    # THEN
    assert x_healerhold
    assert x_healerhold._belief_ids == run_belief_ids


def test_healerhold_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    run_text = ",runners"
    run_belief_ids = {run_text}

    # WHEN
    x_healerhold = healerhold_shop(_belief_ids=run_belief_ids)

    # THEN
    assert x_healerhold
    assert x_healerhold._belief_ids == run_belief_ids


def test_healerhold_shop_ifEmptyReturnsCorrectWithCorrectAttributes():
    # GIVEN / WHEN
    x_healerhold = healerhold_shop()

    # THEN
    assert x_healerhold
    assert x_healerhold._belief_ids == set()


def test_HealerHold_get_dict_ReturnsCorrectDictWithSingleBelief_id():
    # GIVEN
    bob_belief_id = BeliefID("Bob")
    run_belief_ids = {bob_belief_id}
    x_healerhold = healerhold_shop(_belief_ids=run_belief_ids)

    # WHEN
    obj_dict = x_healerhold.get_dict()

    # THEN
    assert obj_dict != None
    run_list = [bob_belief_id]
    example_dict = {"healerhold_belief_ids": run_list}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_HealerHold_set_belief_id_CorrectlySets_belief_ids_v1():
    # GIVEN
    x_healerhold = healerhold_shop()
    assert len(x_healerhold._belief_ids) == 0

    # WHEN
    jim_text = "Jim"
    x_healerhold.set_belief_id(x_belief_id=jim_text)

    # THEN
    assert len(x_healerhold._belief_ids) == 1


def test_HealerHold_del_belief_id_CorrectlyDeletes_belief_ids_v1():
    # GIVEN
    x_healerhold = healerhold_shop()
    jim_text = "Jim"
    sue_text = "Sue"
    x_healerhold.set_belief_id(x_belief_id=jim_text)
    x_healerhold.set_belief_id(x_belief_id=sue_text)
    assert len(x_healerhold._belief_ids) == 2

    # WHEN
    x_healerhold.del_belief_id(x_belief_id=sue_text)

    # THEN
    assert len(x_healerhold._belief_ids) == 1


def test_HealerHold_belief_id_exists_ReturnsCorrectObj():
    # GIVEN
    x_healerhold = healerhold_shop()
    jim_text = "Jim"
    sue_text = "Sue"
    assert x_healerhold.belief_id_exists(jim_text) is False
    assert x_healerhold.belief_id_exists(sue_text) is False

    # WHEN
    x_healerhold.set_belief_id(x_belief_id=jim_text)

    # THEN
    assert x_healerhold.belief_id_exists(jim_text)
    assert x_healerhold.belief_id_exists(sue_text) is False


def test_HealerHold_any_belief_id_exists_ReturnsCorrectObj():
    # GIVEN
    x_healerhold = healerhold_shop()
    assert x_healerhold.any_belief_id_exists() is False

    # WHEN / THEN
    sue_text = "Sue"
    x_healerhold.set_belief_id(x_belief_id=sue_text)
    assert x_healerhold.any_belief_id_exists()

    # WHEN / THEN
    jim_text = "Jim"
    x_healerhold.set_belief_id(x_belief_id=jim_text)
    assert x_healerhold.any_belief_id_exists()

    # WHEN / THEN
    x_healerhold.del_belief_id(x_belief_id=jim_text)
    assert x_healerhold.any_belief_id_exists()

    # WHEN / THEN
    x_healerhold.del_belief_id(x_belief_id=sue_text)
    assert x_healerhold.any_belief_id_exists() is False


def test_healerhold_get_from_dict_ReturnsCorrectObj():
    # GIVEN
    empty_dict = {}

    # WHEN / THEN
    assert healerhold_get_from_dict(empty_dict) == healerhold_shop()

    # WHEN / THEN
    sue_text = "Sue"
    jim_text = "Jim"
    static_healerhold = healerhold_shop()
    static_healerhold.set_belief_id(x_belief_id=sue_text)
    static_healerhold.set_belief_id(x_belief_id=jim_text)

    sue_dict = {"healerhold_belief_ids": [sue_text, jim_text]}
    assert healerhold_get_from_dict(sue_dict) == static_healerhold
