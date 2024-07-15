from src._world.char import charlink_shop
from src._world.belieflink import belieflink_shop
from src._world.beliefbox import beliefbox_shop
from src._world.world import worldunit_shop


def test_WorldUnit_migrate_beliefboxs_to_belieflinks_MigratesEmptySet():
    # GIVEN
    bob_world = worldunit_shop("Bob")
    assert bob_world._chars == {}

    # WHEN
    bob_world._migrate_beliefboxs_to_belieflinks()

    # THEN
    assert bob_world._chars == {}


def test_WorldUnit_migrate_beliefboxs_to_belieflinks_Migrates_charlinks_Without_credor_weight():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    zia_text = "Zia"
    bob_world = worldunit_shop("Bob")
    bob_world.add_charunit(yao_text)
    bob_world.add_charunit(sue_text)
    bob_world.add_charunit(zia_text)
    run_text = ",Run"
    bob_world.set_beliefbox(beliefbox_shop(run_text))
    run_beliefbox = bob_world.get_beliefbox(run_text)
    run_beliefbox.set_charlink(charlink_shop(sue_text))
    run_beliefbox.set_charlink(charlink_shop(zia_text))
    assert len(bob_world.get_beliefbox(yao_text)._chars) == 1
    assert len(bob_world.get_beliefbox(sue_text)._chars) == 1
    assert len(bob_world.get_beliefbox(zia_text)._chars) == 1
    assert len(bob_world.get_beliefbox(run_text)._chars) == 2
    assert len(bob_world.get_char(yao_text)._belieflinks) == 1
    assert len(bob_world.get_char(sue_text)._belieflinks) == 1

    # WHEN
    bob_world._migrate_beliefboxs_to_belieflinks()

    # THEN
    assert len(bob_world.get_beliefbox(yao_text)._chars) == 1
    assert len(bob_world.get_beliefbox(sue_text)._chars) == 1
    assert len(bob_world.get_beliefbox(zia_text)._chars) == 1
    assert len(bob_world.get_beliefbox(run_text)._chars) == 2
    assert len(bob_world.get_char(yao_text)._belieflinks) == 1
    assert len(bob_world.get_char(sue_text)._belieflinks) == 2
    assert len(bob_world.get_char(zia_text)._belieflinks) == 2
    yao_charunit = bob_world.get_char(yao_text)
    yao_belieflink = belieflink_shop(yao_text, _char_id=yao_text)
    assert yao_charunit.get_belieflink(yao_text) == yao_belieflink

    # GIVEN
    run_beliefbox.del_charlink(zia_text)
    assert len(bob_world.get_beliefbox(run_text)._chars) == 1

    # WHEN
    bob_world._migrate_beliefboxs_to_belieflinks()

    # THEN
    assert len(bob_world.get_beliefbox(sue_text)._chars) == 1
    assert len(bob_world.get_beliefbox(zia_text)._chars) == 1
    assert len(bob_world.get_beliefbox(run_text)._chars) == 1
    assert len(bob_world.get_char(sue_text)._belieflinks) == 2
    assert len(bob_world.get_char(zia_text)._belieflinks) == 1


def test_WorldUnit_migrate_beliefboxs_to_belieflinks_Migrates_charlinks_With_credor_weight():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    zia_text = "Zia"
    bob_world = worldunit_shop("Bob")
    bob_world.add_charunit(yao_text)
    bob_world.add_charunit(sue_text)
    bob_world.add_charunit(zia_text)
    run_text = ",Run"
    bob_world.set_beliefbox(beliefbox_shop(run_text))
    run_beliefbox = bob_world.get_beliefbox(run_text)
    sue_run_credor_weight = 11
    sue_run_debtor_weight = 13
    zia_run_credor_weight = 17
    zia_run_debtor_weight = 23
    sue_run_charlink = charlink_shop(
        sue_text, sue_run_credor_weight, sue_run_debtor_weight
    )
    zia_run_charlink = charlink_shop(
        zia_text, zia_run_credor_weight, zia_run_debtor_weight
    )
    run_beliefbox.set_charlink(sue_run_charlink)
    run_beliefbox.set_charlink(zia_run_charlink)
    assert len(bob_world.get_beliefbox(run_text)._chars) == 2
    assert len(bob_world.get_char(yao_text)._belieflinks) == 1
    assert len(bob_world.get_char(sue_text)._belieflinks) == 1

    # WHEN
    bob_world._migrate_beliefboxs_to_belieflinks()

    # THEN
    assert len(bob_world.get_char(sue_text)._belieflinks) == 2
    assert len(bob_world.get_char(zia_text)._belieflinks) == 2
    sue_charunit = bob_world.get_char(sue_text)
    zia_charunit = bob_world.get_char(zia_text)
    sue_belieflink = sue_charunit.get_belieflink(run_text)
    zia_belieflink = zia_charunit.get_belieflink(run_text)
    assert sue_belieflink.credor_weight == sue_run_credor_weight
    assert sue_belieflink.debtor_weight == sue_run_debtor_weight
    assert zia_belieflink.credor_weight == zia_run_credor_weight
    assert zia_belieflink.debtor_weight == zia_run_debtor_weight


def test_WorldUnit_migrate_belieflinks_to_beliefboxs_MigratesEmptySet():
    # GIVEN
    bob_world = worldunit_shop("Bob")
    assert bob_world._chars == {}
    assert bob_world._beliefs == {}

    # WHEN
    bob_world._migrate_belieflinks_to_beliefboxs()

    # THEN
    assert bob_world._chars == {}
    assert bob_world._beliefs == {}


def test_WorldUnit_migrate_belieflinks_to_beliefboxs_Migrates_charlinks_Without_credor_weight():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    zia_text = "Zia"
    bob_world = worldunit_shop("Bob")
    bob_world.add_charunit(yao_text)
    bob_world.add_charunit(sue_text)
    bob_world.add_charunit(zia_text)
    yao_charunit = bob_world.get_char(yao_text)
    sue_charunit = bob_world.get_char(sue_text)
    zia_charunit = bob_world.get_char(zia_text)
    yao_charunit.set_belieflink(belieflink_shop(yao_text))
    sue_charunit.set_belieflink(belieflink_shop(sue_text))
    zia_charunit.set_belieflink(belieflink_shop(zia_text))
    run_text = ",Run"
    sue_charunit.set_belieflink(belieflink_shop(run_text))
    zia_charunit.set_belieflink(belieflink_shop(run_text))
    assert len(bob_world.get_char(yao_text)._belieflinks) == 1
    assert len(bob_world.get_char(sue_text)._belieflinks) == 2
    assert len(bob_world.get_char(zia_text)._belieflinks) == 2
    assert len(bob_world.get_char(zia_text)._belieflinks) == 2
    assert set(bob_world._beliefs.keys()) == {yao_text, sue_text, zia_text}

    # WHEN
    bob_world._migrate_belieflinks_to_beliefboxs()

    # THEN
    assert len(bob_world.get_beliefbox(yao_text)._chars) == 1
    assert len(bob_world.get_beliefbox(sue_text)._chars) == 1
    assert len(bob_world.get_beliefbox(zia_text)._chars) == 1
    assert len(bob_world.get_beliefbox(run_text)._chars) == 2
    assert len(bob_world.get_char(yao_text)._belieflinks) == 0
    assert len(bob_world.get_char(sue_text)._belieflinks) == 0
    assert len(bob_world.get_char(zia_text)._belieflinks) == 0

    run_beliefbox = bob_world.get_beliefbox(run_text)
    assert run_beliefbox._chars.get(zia_text) == charlink_shop(zia_text)
    assert run_beliefbox._chars.get(sue_text) == charlink_shop(sue_text)
    yao_charunit = bob_world.get_char(yao_text)
    assert yao_charunit.get_belieflink(yao_text) is None


def test_WorldUnit_migrate_belieflinks_to_beliefboxs_Migrates_charlinks_With_credor_weight():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    zia_text = "Zia"
    bob_world = worldunit_shop("Bob")
    bob_world.add_charunit(yao_text)
    bob_world.add_charunit(sue_text)
    bob_world.add_charunit(zia_text)
    yao_charunit = bob_world.get_char(yao_text)
    sue_charunit = bob_world.get_char(sue_text)
    zia_charunit = bob_world.get_char(zia_text)
    yao_charunit.set_belieflink(belieflink_shop(yao_text))
    sue_charunit.set_belieflink(belieflink_shop(sue_text))
    zia_charunit.set_belieflink(belieflink_shop(zia_text))
    run_text = ",Run"
    sue_run_credor_weight = 11
    sue_run_debtor_weight = 13
    zia_run_credor_weight = 17
    zia_run_debtor_weight = 23
    sue_run_belieflink = belieflink_shop(
        run_text, sue_run_credor_weight, sue_run_debtor_weight
    )
    zia_run_belieflink = belieflink_shop(
        run_text, zia_run_credor_weight, zia_run_debtor_weight
    )
    sue_charunit.set_belieflink(sue_run_belieflink)
    zia_charunit.set_belieflink(zia_run_belieflink)
    assert len(bob_world.get_char(yao_text)._belieflinks) == 1
    assert len(bob_world.get_char(sue_text)._belieflinks) == 2
    assert len(bob_world.get_char(zia_text)._belieflinks) == 2
    assert len(bob_world.get_char(zia_text)._belieflinks) == 2
    assert set(bob_world._beliefs.keys()) == {yao_text, sue_text, zia_text}

    # WHEN
    bob_world._migrate_belieflinks_to_beliefboxs()

    # THEN
    assert len(bob_world.get_beliefbox(yao_text)._chars) == 1
    assert len(bob_world.get_beliefbox(sue_text)._chars) == 1
    assert len(bob_world.get_beliefbox(zia_text)._chars) == 1
    assert len(bob_world.get_beliefbox(run_text)._chars) == 2
    assert len(bob_world.get_char(yao_text)._belieflinks) == 0
    assert len(bob_world.get_char(sue_text)._belieflinks) == 0
    assert len(bob_world.get_char(zia_text)._belieflinks) == 0

    static_sue_run_charlink = charlink_shop(
        sue_text, sue_run_credor_weight, sue_run_debtor_weight
    )
    static_zia_run_charlink = charlink_shop(
        zia_text, zia_run_credor_weight, zia_run_debtor_weight
    )
    run_beliefbox = bob_world.get_beliefbox(run_text)
    assert run_beliefbox._chars.get(zia_text) != None
    assert run_beliefbox._chars.get(sue_text) != None
    gen_zia_run_charlink = run_beliefbox._chars.get(zia_text)
    gen_sue_run_charlink = run_beliefbox._chars.get(sue_text)
    assert gen_sue_run_charlink == static_sue_run_charlink
    assert gen_zia_run_charlink == static_zia_run_charlink


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
