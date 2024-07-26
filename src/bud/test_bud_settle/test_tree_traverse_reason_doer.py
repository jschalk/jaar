from src.bud.reason_doer import doerheir_shop, doerunit_shop
from src.bud.bud import budunit_shop
from src.bud.idea import ideaunit_shop


def test_bud_edit_idea_attr_CorrectlySetsDoerUnit():
    # ESTABLISH
    xio_bud = budunit_shop("Xio")
    run_text = "run"
    run_road = xio_bud.make_l1_road(run_text)
    xio_bud.set_l1_idea(ideaunit_shop(run_text))
    run_idea = xio_bud.get_idea_obj(run_road)
    assert run_idea._doerunit == doerunit_shop()

    # WHEN
    x_doerunit = doerunit_shop()
    xio_bud.edit_idea_attr(doerunit=x_doerunit, road=run_road)

    # THEN
    assert run_idea._doerunit == x_doerunit


def test_bud_idearoot_doerunit_CorrectlySets_idea_doerheir():
    # ESTABLISH
    x_doerunit = doerunit_shop()

    yao_bud = budunit_shop("Yao")
    yao_bud.edit_idea_attr(doerunit=x_doerunit, road=yao_bud._real_id)
    assert yao_bud._idearoot._doerunit == x_doerunit
    assert yao_bud._idearoot._doerheir is None

    # WHEN
    yao_bud.settle_bud()

    # THEN
    x_doerheir = doerheir_shop()
    x_doerheir.set_groupholds(
        parent_doerheir=None, doerunit=x_doerunit, bud_groupboxs=None
    )
    assert yao_bud._idearoot._doerheir is not None
    assert yao_bud._idearoot._doerheir == x_doerheir


def test_bud_ideakid_doerunit_EmptyCorrectlySets_idea_doerheir():
    # ESTABLISH
    bob_text = "Bob"
    x_doerunit = doerunit_shop()
    bob_bud = budunit_shop(bob_text)
    run_text = "run"
    run_road = bob_bud.make_l1_road(run_text)
    bob_bud.add_acctunit(bob_text)
    bob_bud.set_l1_idea(ideaunit_shop(run_text))
    bob_bud.edit_idea_attr(run_road, doerunit=x_doerunit)
    run_idea = bob_bud.get_idea_obj(run_road)
    assert run_idea._doerunit == x_doerunit
    assert run_idea._doerheir is None

    # WHEN
    bob_bud.settle_bud()

    # THEN
    assert run_idea._doerheir is not None
    assert run_idea._doerheir._owner_id_doer

    x_doerheir = doerheir_shop()
    x_doerheir.set_groupholds(
        parent_doerheir=None,
        doerunit=x_doerunit,
        bud_groupboxs=bob_bud._groupboxs,
    )
    x_doerheir.set_owner_id_doer(bob_bud._groupboxs, bob_bud._owner_id)
    print(f"{x_doerheir._owner_id_doer=}")
    assert run_idea._doerheir._owner_id_doer == x_doerheir._owner_id_doer
    assert run_idea._doerheir == x_doerheir


def test_bud_ideakid_doerunit_EmptyCorrectlySets_idea_doerheir():
    # ESTABLISH
    bob_text = "Bob"
    x_doerunit = doerunit_shop()
    bob_bud = budunit_shop(bob_text)
    run_text = "run"
    run_road = bob_bud.make_l1_road(run_text)
    bob_bud.add_acctunit(bob_text)
    bob_bud.set_l1_idea(ideaunit_shop(run_text))
    bob_bud.edit_idea_attr(run_road, doerunit=x_doerunit)
    run_idea = bob_bud.get_idea_obj(run_road)
    assert run_idea._doerunit == x_doerunit
    assert run_idea._doerheir is None

    # WHEN
    bob_bud.settle_bud()

    # THEN
    assert run_idea._doerheir is not None
    assert run_idea._doerheir._owner_id_doer

    x_doerheir = doerheir_shop()
    x_doerheir.set_groupholds(
        parent_doerheir=None,
        doerunit=x_doerunit,
        bud_groupboxs=bob_bud._groupboxs,
    )
    x_doerheir.set_owner_id_doer(bob_bud._groupboxs, bob_bud._owner_id)
    print(f"{x_doerheir._owner_id_doer=}")
    assert run_idea._doerheir._owner_id_doer == x_doerheir._owner_id_doer
    assert run_idea._doerheir == x_doerheir


def test_bud_ideakid_doerunit_CorrectlySets_grandchild_idea_doerheir():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    swim_text = "swimming"
    swim_road = sue_bud.make_l1_road(swim_text)
    morn_text = "morning"
    morn_road = sue_bud.make_road(swim_road, morn_text)
    four_text = "fourth"
    four_road = sue_bud.make_road(morn_road, four_text)
    x_doerunit = doerunit_shop()
    swimmers_text = ";swimmers"
    x_doerunit.set_grouphold(group_id=swimmers_text)

    yao_text = "Yao"
    sue_bud.add_acctunit(yao_text)
    yao_acctunit = sue_bud.get_acct(yao_text)
    yao_acctunit.add_membership(swimmers_text)

    sue_bud.set_l1_idea(ideaunit_shop(swim_text))
    sue_bud.set_idea(ideaunit_shop(morn_text), parent_road=swim_road)
    sue_bud.set_idea(ideaunit_shop(four_text), parent_road=morn_road)
    sue_bud.edit_idea_attr(swim_road, doerunit=x_doerunit)
    # print(sue_bud.make_road(four_road=}\n{morn_road=))
    four_idea = sue_bud.get_idea_obj(four_road)
    assert four_idea._doerunit == doerunit_shop()
    assert four_idea._doerheir is None

    # WHEN
    sue_bud.settle_bud()

    # THEN
    x_doerheir = doerheir_shop()
    x_doerheir.set_groupholds(
        parent_doerheir=None,
        doerunit=x_doerunit,
        bud_groupboxs=sue_bud._groupboxs,
    )
    assert four_idea._doerheir is not None
    assert four_idea._doerheir == x_doerheir


def test_BudUnit__get_filtered_awardlinks_idea_CorrectlyFiltersIdea_Doerunit():
    # ESTABLISH
    sue_text = "Sue"
    sue1_bud = budunit_shop(sue_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    sue1_bud.add_acctunit(xia_text)
    sue1_bud.add_acctunit(zoa_text)

    casa_text = "casa"
    casa_road = sue1_bud.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = sue1_bud.make_l1_road(swim_text)
    sue1_bud.set_idea(ideaunit_shop(casa_text), parent_road=sue1_bud._real_id)
    sue1_bud.set_idea(ideaunit_shop(swim_text), parent_road=sue1_bud._real_id)
    swim_doerunit = doerunit_shop()
    swim_doerunit.set_grouphold(group_id=xia_text)
    swim_doerunit.set_grouphold(group_id=zoa_text)
    sue1_bud.edit_idea_attr(swim_road, doerunit=swim_doerunit)
    sue1_bud_swim_idea = sue1_bud.get_idea_obj(swim_road)
    sue1_bud_swim_groupholds = sue1_bud_swim_idea._doerunit._groupholds
    assert len(sue1_bud_swim_groupholds) == 2

    # WHEN
    sue2_bud = budunit_shop(sue_text)
    sue2_bud.add_acctunit(xia_text)
    filtered_idea = sue2_bud._get_filtered_awardlinks_idea(sue1_bud_swim_idea)

    # THEN
    filtered_swim_groupholds = filtered_idea._doerunit._groupholds
    assert len(filtered_swim_groupholds) == 1
    assert list(filtered_swim_groupholds) == [xia_text]


def test_BudUnit_set_idea_CorrectlyFiltersIdea_awardlinks():
    # ESTABLISH
    sue1_bud = budunit_shop("Sue")
    xia_text = "Xia"
    zoa_text = "Zoa"
    sue1_bud.add_acctunit(xia_text)
    sue1_bud.add_acctunit(zoa_text)

    casa_text = "casa"
    casa_road = sue1_bud.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = sue1_bud.make_l1_road(swim_text)
    sue1_bud.set_idea(ideaunit_shop(casa_text), parent_road=sue1_bud._real_id)
    sue1_bud.set_idea(ideaunit_shop(swim_text), parent_road=sue1_bud._real_id)
    swim_doerunit = doerunit_shop()
    swim_doerunit.set_grouphold(group_id=xia_text)
    swim_doerunit.set_grouphold(group_id=zoa_text)
    sue1_bud.edit_idea_attr(swim_road, doerunit=swim_doerunit)
    sue1_bud_swim_idea = sue1_bud.get_idea_obj(swim_road)
    sue1_bud_swim_groupholds = sue1_bud_swim_idea._doerunit._groupholds
    assert len(sue1_bud_swim_groupholds) == 2

    # WHEN
    sue2_bud = budunit_shop("Sue")
    sue2_bud.add_acctunit(xia_text)
    sue2_bud.set_l1_idea(
        sue1_bud_swim_idea, filter_out_missing_awardlinks_group_ids=False
    )

    # THEN
    sue2_bud_swim_idea = sue2_bud.get_idea_obj(swim_road)
    sue2_bud_swim_groupholds = sue2_bud_swim_idea._doerunit._groupholds
    assert len(sue2_bud_swim_groupholds) == 1
    assert list(sue2_bud_swim_groupholds) == [xia_text]
