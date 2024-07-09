from src._world.reason_culture import cultureheir_shop, cultureunit_shop
from src._world.world import worldunit_shop
from src._world.idea import ideaunit_shop
from src._world.beliefunit import beliefunit_shop


def test_world_edit_idea_attr_CorrectlySetsCultureUnit():
    # GIVEN
    xio_world = worldunit_shop("Xio")
    run_text = "run"
    run_road = xio_world.make_l1_road(run_text)
    xio_world.add_l1_idea(ideaunit_shop(run_text))
    run_idea = xio_world.get_idea_obj(run_road)
    assert run_idea._cultureunit == cultureunit_shop()

    # WHEN
    x_cultureunit = cultureunit_shop()
    xio_world.edit_idea_attr(cultureunit=x_cultureunit, road=run_road)

    # THEN
    assert run_idea._cultureunit == x_cultureunit


def test_world_idearoot_cultureunit_CorrectlySets_idea_cultureheir():
    # GIVEN
    x_cultureunit = cultureunit_shop()

    tim_world = worldunit_shop("Tim")
    tim_world.edit_idea_attr(cultureunit=x_cultureunit, road=tim_world._real_id)
    assert tim_world._idearoot._cultureunit == x_cultureunit
    assert tim_world._idearoot._cultureheir is None

    # WHEN
    tim_world.calc_world_metrics()

    # THEN
    x_cultureheir = cultureheir_shop()
    x_cultureheir.set_allyholds(
        parent_cultureheir=None, cultureunit=x_cultureunit, world_beliefs=None
    )
    assert tim_world._idearoot._cultureheir != None
    assert tim_world._idearoot._cultureheir == x_cultureheir


def test_world_ideakid_cultureunit_EmptyCorrectlySets_idea_cultureheir():
    # GIVEN
    bob_text = "Bob"
    x_cultureunit = cultureunit_shop()
    bob_world = worldunit_shop(bob_text)
    run_text = "run"
    run_road = bob_world.make_l1_road(run_text)
    bob_world.add_charunit(bob_text)
    bob_world.add_l1_idea(ideaunit_shop(run_text))
    bob_world.edit_idea_attr(run_road, cultureunit=x_cultureunit)
    run_idea = bob_world.get_idea_obj(run_road)
    assert run_idea._cultureunit == x_cultureunit
    assert run_idea._cultureheir is None

    # WHEN
    bob_world.calc_world_metrics()

    # THEN
    assert run_idea._cultureheir != None
    assert run_idea._cultureheir._owner_id_culture

    x_cultureheir = cultureheir_shop()
    x_cultureheir.set_allyholds(
        parent_cultureheir=None,
        cultureunit=x_cultureunit,
        world_beliefs=bob_world._beliefs,
    )
    x_cultureheir.set_owner_id_culture(bob_world._beliefs, bob_world._owner_id)
    print(f"{x_cultureheir._owner_id_culture=}")
    assert run_idea._cultureheir._owner_id_culture == x_cultureheir._owner_id_culture
    assert run_idea._cultureheir == x_cultureheir


def test_world_ideakid_cultureunit_EmptyCorrectlySets_idea_cultureheir():
    # GIVEN
    bob_text = "Bob"
    x_cultureunit = cultureunit_shop()
    bob_world = worldunit_shop(bob_text)
    run_text = "run"
    run_road = bob_world.make_l1_road(run_text)
    bob_world.add_charunit(bob_text)
    bob_world.add_l1_idea(ideaunit_shop(run_text))
    bob_world.edit_idea_attr(run_road, cultureunit=x_cultureunit)
    run_idea = bob_world.get_idea_obj(run_road)
    assert run_idea._cultureunit == x_cultureunit
    assert run_idea._cultureheir is None

    # WHEN
    bob_world.calc_world_metrics()

    # THEN
    assert run_idea._cultureheir != None
    assert run_idea._cultureheir._owner_id_culture

    x_cultureheir = cultureheir_shop()
    x_cultureheir.set_allyholds(
        parent_cultureheir=None,
        cultureunit=x_cultureunit,
        world_beliefs=bob_world._beliefs,
    )
    x_cultureheir.set_owner_id_culture(bob_world._beliefs, bob_world._owner_id)
    print(f"{x_cultureheir._owner_id_culture=}")
    assert run_idea._cultureheir._owner_id_culture == x_cultureheir._owner_id_culture
    assert run_idea._cultureheir == x_cultureheir


def test_world_ideakid_cultureunit_CorrectlySets_grandchild_idea_cultureheir():
    # GIVEN
    noa_world = worldunit_shop("Noa")
    swim_text = "swimming"
    swim_road = noa_world.make_l1_road(swim_text)
    morn_text = "morning"
    morn_road = noa_world.make_road(swim_road, morn_text)
    four_text = "fourth"
    four_road = noa_world.make_road(morn_road, four_text)
    x_cultureunit = cultureunit_shop()
    swimmers_text = ",swimmers"
    x_cultureunit.set_allyhold(belief_id=swimmers_text)

    noa_world.set_beliefunit(y_beliefunit=beliefunit_shop(belief_id=swimmers_text))
    noa_world.add_l1_idea(ideaunit_shop(swim_text))
    noa_world.add_idea(ideaunit_shop(morn_text), parent_road=swim_road)
    noa_world.add_idea(ideaunit_shop(four_text), parent_road=morn_road)
    noa_world.edit_idea_attr(swim_road, cultureunit=x_cultureunit)
    # print(noa_world.make_road(four_road=}\n{morn_road=))
    four_idea = noa_world.get_idea_obj(four_road)
    assert four_idea._cultureunit == cultureunit_shop()
    assert four_idea._cultureheir is None

    # WHEN
    noa_world.calc_world_metrics()

    # THEN
    x_cultureheir = cultureheir_shop()
    x_cultureheir.set_allyholds(
        parent_cultureheir=None,
        cultureunit=x_cultureunit,
        world_beliefs=noa_world._beliefs,
    )
    assert four_idea._cultureheir != None
    assert four_idea._cultureheir == x_cultureheir


def test_WorldUnit__get_filtered_fiscallinks_idea_CorrectlyFiltersIdea_Cultureunit():
    # GIVEN
    noa_text = "Noa"
    noa1_world = worldunit_shop(noa_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    noa1_world.add_charunit(xia_text)
    noa1_world.add_charunit(zoa_text)

    casa_text = "casa"
    casa_road = noa1_world.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = noa1_world.make_l1_road(swim_text)
    noa1_world.add_idea(ideaunit_shop(casa_text), parent_road=noa1_world._real_id)
    noa1_world.add_idea(ideaunit_shop(swim_text), parent_road=noa1_world._real_id)
    swim_cultureunit = cultureunit_shop()
    swim_cultureunit.set_allyhold(belief_id=xia_text)
    swim_cultureunit.set_allyhold(belief_id=zoa_text)
    noa1_world.edit_idea_attr(swim_road, cultureunit=swim_cultureunit)
    noa1_world_swim_idea = noa1_world.get_idea_obj(swim_road)
    noa1_world_swim_allyholds = noa1_world_swim_idea._cultureunit._allyholds
    assert len(noa1_world_swim_allyholds) == 2

    # WHEN
    noa2_world = worldunit_shop(noa_text)
    noa2_world.add_charunit(xia_text)
    filtered_idea = noa2_world._get_filtered_fiscallinks_idea(noa1_world_swim_idea)

    # THEN
    filtered_swim_allyholds = filtered_idea._cultureunit._allyholds
    assert len(filtered_swim_allyholds) == 1
    assert list(filtered_swim_allyholds) == [xia_text]


def test_WorldUnit_add_idea_CorrectlyFiltersIdea_fiscallinks():
    # GIVEN
    noa1_world = worldunit_shop("Noa")
    xia_text = "Xia"
    zoa_text = "Zoa"
    noa1_world.add_charunit(xia_text)
    noa1_world.add_charunit(zoa_text)

    casa_text = "casa"
    casa_road = noa1_world.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = noa1_world.make_l1_road(swim_text)
    noa1_world.add_idea(ideaunit_shop(casa_text), parent_road=noa1_world._real_id)
    noa1_world.add_idea(ideaunit_shop(swim_text), parent_road=noa1_world._real_id)
    swim_cultureunit = cultureunit_shop()
    swim_cultureunit.set_allyhold(belief_id=xia_text)
    swim_cultureunit.set_allyhold(belief_id=zoa_text)
    noa1_world.edit_idea_attr(swim_road, cultureunit=swim_cultureunit)
    noa1_world_swim_idea = noa1_world.get_idea_obj(swim_road)
    noa1_world_swim_allyholds = noa1_world_swim_idea._cultureunit._allyholds
    assert len(noa1_world_swim_allyholds) == 2

    # WHEN
    noa2_world = worldunit_shop("Noa")
    noa2_world.add_charunit(xia_text)
    noa2_world.add_l1_idea(noa1_world_swim_idea, create_missing_beliefs=False)

    # THEN
    noa2_world_swim_idea = noa2_world.get_idea_obj(swim_road)
    noa2_world_swim_allyholds = noa2_world_swim_idea._cultureunit._allyholds
    assert len(noa2_world_swim_allyholds) == 1
    assert list(noa2_world_swim_allyholds) == [xia_text]
