from src._world.reason_doer import doerheir_shop, doerunit_shop
from src._world.world import worldunit_shop
from src._world.idea import ideaunit_shop


def test_world_edit_idea_attr_CorrectlySetsDoerUnit():
    # GIVEN
    xio_world = worldunit_shop("Xio")
    run_text = "run"
    run_road = xio_world.make_l1_road(run_text)
    xio_world.add_l1_idea(ideaunit_shop(run_text))
    run_idea = xio_world.get_idea_obj(run_road)
    assert run_idea._doerunit == doerunit_shop()

    # WHEN
    x_doerunit = doerunit_shop()
    xio_world.edit_idea_attr(doerunit=x_doerunit, road=run_road)

    # THEN
    assert run_idea._doerunit == x_doerunit


def test_world_idearoot_doerunit_CorrectlySets_idea_doerheir():
    # GIVEN
    x_doerunit = doerunit_shop()

    tim_world = worldunit_shop("Tim")
    tim_world.edit_idea_attr(doerunit=x_doerunit, road=tim_world._real_id)
    assert tim_world._idearoot._doerunit == x_doerunit
    assert tim_world._idearoot._doerheir is None

    # WHEN
    tim_world.calc_world_metrics()

    # THEN
    x_doerheir = doerheir_shop()
    x_doerheir.set_beliefholds(
        parent_doerheir=None, doerunit=x_doerunit, world_beliefboxs=None
    )
    assert tim_world._idearoot._doerheir != None
    assert tim_world._idearoot._doerheir == x_doerheir


def test_world_ideakid_doerunit_EmptyCorrectlySets_idea_doerheir():
    # GIVEN
    bob_text = "Bob"
    x_doerunit = doerunit_shop()
    bob_world = worldunit_shop(bob_text)
    run_text = "run"
    run_road = bob_world.make_l1_road(run_text)
    bob_world.add_charunit(bob_text)
    bob_world.add_l1_idea(ideaunit_shop(run_text))
    bob_world.edit_idea_attr(run_road, doerunit=x_doerunit)
    run_idea = bob_world.get_idea_obj(run_road)
    assert run_idea._doerunit == x_doerunit
    assert run_idea._doerheir is None

    # WHEN
    bob_world.calc_world_metrics()

    # THEN
    assert run_idea._doerheir != None
    assert run_idea._doerheir._owner_id_doer

    x_doerheir = doerheir_shop()
    x_doerheir.set_beliefholds(
        parent_doerheir=None,
        doerunit=x_doerunit,
        world_beliefboxs=bob_world._beliefboxs,
    )
    x_doerheir.set_owner_id_doer(bob_world._beliefboxs, bob_world._owner_id)
    print(f"{x_doerheir._owner_id_doer=}")
    assert run_idea._doerheir._owner_id_doer == x_doerheir._owner_id_doer
    assert run_idea._doerheir == x_doerheir


def test_world_ideakid_doerunit_EmptyCorrectlySets_idea_doerheir():
    # GIVEN
    bob_text = "Bob"
    x_doerunit = doerunit_shop()
    bob_world = worldunit_shop(bob_text)
    run_text = "run"
    run_road = bob_world.make_l1_road(run_text)
    bob_world.add_charunit(bob_text)
    bob_world.add_l1_idea(ideaunit_shop(run_text))
    bob_world.edit_idea_attr(run_road, doerunit=x_doerunit)
    run_idea = bob_world.get_idea_obj(run_road)
    assert run_idea._doerunit == x_doerunit
    assert run_idea._doerheir is None

    # WHEN
    bob_world.calc_world_metrics()

    # THEN
    assert run_idea._doerheir != None
    assert run_idea._doerheir._owner_id_doer

    x_doerheir = doerheir_shop()
    x_doerheir.set_beliefholds(
        parent_doerheir=None,
        doerunit=x_doerunit,
        world_beliefboxs=bob_world._beliefboxs,
    )
    x_doerheir.set_owner_id_doer(bob_world._beliefboxs, bob_world._owner_id)
    print(f"{x_doerheir._owner_id_doer=}")
    assert run_idea._doerheir._owner_id_doer == x_doerheir._owner_id_doer
    assert run_idea._doerheir == x_doerheir


def test_world_ideakid_doerunit_CorrectlySets_grandchild_idea_doerheir():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    swim_text = "swimming"
    swim_road = sue_world.make_l1_road(swim_text)
    morn_text = "morning"
    morn_road = sue_world.make_road(swim_road, morn_text)
    four_text = "fourth"
    four_road = sue_world.make_road(morn_road, four_text)
    x_doerunit = doerunit_shop()
    swimmers_text = ",swimmers"
    x_doerunit.set_beliefhold(belief_id=swimmers_text)

    yao_text = "Yao"
    sue_world.add_charunit(yao_text)
    yao_charunit = sue_world.get_char(yao_text)
    yao_charunit.add_belieflink(swimmers_text)

    sue_world.add_l1_idea(ideaunit_shop(swim_text))
    sue_world.add_idea(ideaunit_shop(morn_text), parent_road=swim_road)
    sue_world.add_idea(ideaunit_shop(four_text), parent_road=morn_road)
    sue_world.edit_idea_attr(swim_road, doerunit=x_doerunit)
    # print(sue_world.make_road(four_road=}\n{morn_road=))
    four_idea = sue_world.get_idea_obj(four_road)
    assert four_idea._doerunit == doerunit_shop()
    assert four_idea._doerheir is None

    # WHEN
    sue_world.calc_world_metrics()

    # THEN
    x_doerheir = doerheir_shop()
    x_doerheir.set_beliefholds(
        parent_doerheir=None,
        doerunit=x_doerunit,
        world_beliefboxs=sue_world._beliefboxs,
    )
    assert four_idea._doerheir != None
    assert four_idea._doerheir == x_doerheir


def test_WorldUnit__get_filtered_awardlinks_idea_CorrectlyFiltersIdea_Doerunit():
    # GIVEN
    sue_text = "Sue"
    sue1_world = worldunit_shop(sue_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    sue1_world.add_charunit(xia_text)
    sue1_world.add_charunit(zoa_text)

    casa_text = "casa"
    casa_road = sue1_world.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = sue1_world.make_l1_road(swim_text)
    sue1_world.add_idea(ideaunit_shop(casa_text), parent_road=sue1_world._real_id)
    sue1_world.add_idea(ideaunit_shop(swim_text), parent_road=sue1_world._real_id)
    swim_doerunit = doerunit_shop()
    swim_doerunit.set_beliefhold(belief_id=xia_text)
    swim_doerunit.set_beliefhold(belief_id=zoa_text)
    sue1_world.edit_idea_attr(swim_road, doerunit=swim_doerunit)
    sue1_world_swim_idea = sue1_world.get_idea_obj(swim_road)
    sue1_world_swim_beliefholds = sue1_world_swim_idea._doerunit._beliefholds
    assert len(sue1_world_swim_beliefholds) == 2

    # WHEN
    sue2_world = worldunit_shop(sue_text)
    sue2_world.add_charunit(xia_text)
    filtered_idea = sue2_world._get_filtered_awardlinks_idea(sue1_world_swim_idea)

    # THEN
    filtered_swim_beliefholds = filtered_idea._doerunit._beliefholds
    assert len(filtered_swim_beliefholds) == 1
    assert list(filtered_swim_beliefholds) == [xia_text]


def test_WorldUnit_add_idea_CorrectlyFiltersIdea_awardlinks():
    # GIVEN
    sue1_world = worldunit_shop("Sue")
    xia_text = "Xia"
    zoa_text = "Zoa"
    sue1_world.add_charunit(xia_text)
    sue1_world.add_charunit(zoa_text)

    casa_text = "casa"
    casa_road = sue1_world.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = sue1_world.make_l1_road(swim_text)
    sue1_world.add_idea(ideaunit_shop(casa_text), parent_road=sue1_world._real_id)
    sue1_world.add_idea(ideaunit_shop(swim_text), parent_road=sue1_world._real_id)
    swim_doerunit = doerunit_shop()
    swim_doerunit.set_beliefhold(belief_id=xia_text)
    swim_doerunit.set_beliefhold(belief_id=zoa_text)
    sue1_world.edit_idea_attr(swim_road, doerunit=swim_doerunit)
    sue1_world_swim_idea = sue1_world.get_idea_obj(swim_road)
    sue1_world_swim_beliefholds = sue1_world_swim_idea._doerunit._beliefholds
    assert len(sue1_world_swim_beliefholds) == 2

    # WHEN
    sue2_world = worldunit_shop("Sue")
    sue2_world.add_charunit(xia_text)
    sue2_world.add_l1_idea(
        sue1_world_swim_idea, filter_out_missing_awardlinks_belief_ids=False
    )

    # THEN
    sue2_world_swim_idea = sue2_world.get_idea_obj(swim_road)
    sue2_world_swim_beliefholds = sue2_world_swim_idea._doerunit._beliefholds
    assert len(sue2_world_swim_beliefholds) == 1
    assert list(sue2_world_swim_beliefholds) == [xia_text]
