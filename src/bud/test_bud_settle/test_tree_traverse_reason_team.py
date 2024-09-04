from src.bud.reason_team import teamheir_shop, teamunit_shop
from src.bud.bud import budunit_shop
from src.bud.idea import ideaunit_shop


def test_bud_edit_idea_attr_CorrectlySetsTeamUnit():
    # ESTABLISH
    xio_bud = budunit_shop("Xio")
    run_text = "run"
    run_road = xio_bud.make_l1_road(run_text)
    xio_bud.set_l1_idea(ideaunit_shop(run_text))
    run_idea = xio_bud.get_idea_obj(run_road)
    assert run_idea._teamunit == teamunit_shop()

    # WHEN
    x_teamunit = teamunit_shop()
    xio_bud.edit_idea_attr(teamunit=x_teamunit, road=run_road)

    # THEN
    assert run_idea._teamunit == x_teamunit


def test_bud_idearoot_teamunit_CorrectlySets_idea_teamheir():
    # ESTABLISH
    x_teamunit = teamunit_shop()

    yao_bud = budunit_shop("Yao")
    yao_bud.edit_idea_attr(teamunit=x_teamunit, road=yao_bud._real_id)
    assert yao_bud._idearoot._teamunit == x_teamunit
    assert yao_bud._idearoot._teamheir is None

    # WHEN
    yao_bud.settle_bud()

    # THEN
    x_teamheir = teamheir_shop()
    x_teamheir.set_teamlinks(
        parent_teamheir=None, teamunit=x_teamunit, bud_groupboxs=None
    )
    assert yao_bud._idearoot._teamheir is not None
    assert yao_bud._idearoot._teamheir == x_teamheir


def test_bud_ideakid_teamunit_EmptyCorrectlySets_idea_teamheir():
    # ESTABLISH
    bob_text = "Bob"
    x_teamunit = teamunit_shop()
    bob_bud = budunit_shop(bob_text)
    run_text = "run"
    run_road = bob_bud.make_l1_road(run_text)
    bob_bud.add_acctunit(bob_text)
    bob_bud.set_l1_idea(ideaunit_shop(run_text))
    bob_bud.edit_idea_attr(run_road, teamunit=x_teamunit)
    run_idea = bob_bud.get_idea_obj(run_road)
    assert run_idea._teamunit == x_teamunit
    assert run_idea._teamheir is None

    # WHEN
    bob_bud.settle_bud()

    # THEN
    assert run_idea._teamheir is not None
    assert run_idea._teamheir._owner_id_team

    x_teamheir = teamheir_shop()
    x_teamheir.set_teamlinks(
        parent_teamheir=None,
        teamunit=x_teamunit,
        bud_groupboxs=bob_bud._groupboxs,
    )
    x_teamheir.set_owner_id_team(bob_bud._groupboxs, bob_bud._owner_id)
    print(f"{x_teamheir._owner_id_team=}")
    assert run_idea._teamheir._owner_id_team == x_teamheir._owner_id_team
    assert run_idea._teamheir == x_teamheir


def test_bud_ideakid_teamunit_EmptyCorrectlySets_idea_teamheir():
    # ESTABLISH
    bob_text = "Bob"
    x_teamunit = teamunit_shop()
    bob_bud = budunit_shop(bob_text)
    run_text = "run"
    run_road = bob_bud.make_l1_road(run_text)
    bob_bud.add_acctunit(bob_text)
    bob_bud.set_l1_idea(ideaunit_shop(run_text))
    bob_bud.edit_idea_attr(run_road, teamunit=x_teamunit)
    run_idea = bob_bud.get_idea_obj(run_road)
    assert run_idea._teamunit == x_teamunit
    assert run_idea._teamheir is None

    # WHEN
    bob_bud.settle_bud()

    # THEN
    assert run_idea._teamheir is not None
    assert run_idea._teamheir._owner_id_team

    x_teamheir = teamheir_shop()
    x_teamheir.set_teamlinks(
        parent_teamheir=None,
        teamunit=x_teamunit,
        bud_groupboxs=bob_bud._groupboxs,
    )
    x_teamheir.set_owner_id_team(bob_bud._groupboxs, bob_bud._owner_id)
    print(f"{x_teamheir._owner_id_team=}")
    assert run_idea._teamheir._owner_id_team == x_teamheir._owner_id_team
    assert run_idea._teamheir == x_teamheir


def test_bud_ideakid_teamunit_CorrectlySets_grandchild_idea_teamheir():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    swim_text = "swimming"
    swim_road = sue_bud.make_l1_road(swim_text)
    morn_text = "morning"
    morn_road = sue_bud.make_road(swim_road, morn_text)
    four_text = "fourth"
    four_road = sue_bud.make_road(morn_road, four_text)
    x_teamunit = teamunit_shop()
    swimmers_text = ";swimmers"
    x_teamunit.set_teamlink(group_id=swimmers_text)

    yao_text = "Yao"
    sue_bud.add_acctunit(yao_text)
    yao_acctunit = sue_bud.get_acct(yao_text)
    yao_acctunit.add_membership(swimmers_text)

    sue_bud.set_l1_idea(ideaunit_shop(swim_text))
    sue_bud.set_idea(ideaunit_shop(morn_text), parent_road=swim_road)
    sue_bud.set_idea(ideaunit_shop(four_text), parent_road=morn_road)
    sue_bud.edit_idea_attr(swim_road, teamunit=x_teamunit)
    # print(sue_bud.make_road(four_road=}\n{morn_road=))
    four_idea = sue_bud.get_idea_obj(four_road)
    assert four_idea._teamunit == teamunit_shop()
    assert four_idea._teamheir is None

    # WHEN
    sue_bud.settle_bud()

    # THEN
    x_teamheir = teamheir_shop()
    x_teamheir.set_teamlinks(
        parent_teamheir=None,
        teamunit=x_teamunit,
        bud_groupboxs=sue_bud._groupboxs,
    )
    assert four_idea._teamheir is not None
    assert four_idea._teamheir == x_teamheir


def test_BudUnit__get_filtered_awardlinks_idea_CorrectlyFiltersIdea_Teamunit():
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
    swim_teamunit = teamunit_shop()
    swim_teamunit.set_teamlink(group_id=xia_text)
    swim_teamunit.set_teamlink(group_id=zoa_text)
    sue1_bud.edit_idea_attr(swim_road, teamunit=swim_teamunit)
    sue1_bud_swim_idea = sue1_bud.get_idea_obj(swim_road)
    sue1_bud_swim_teamlinks = sue1_bud_swim_idea._teamunit._teamlinks
    assert len(sue1_bud_swim_teamlinks) == 2

    # WHEN
    sue2_bud = budunit_shop(sue_text)
    sue2_bud.add_acctunit(xia_text)
    filtered_idea = sue2_bud._get_filtered_awardlinks_idea(sue1_bud_swim_idea)

    # THEN
    filtered_swim_teamlinks = filtered_idea._teamunit._teamlinks
    assert len(filtered_swim_teamlinks) == 1
    assert list(filtered_swim_teamlinks) == [xia_text]


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
    swim_teamunit = teamunit_shop()
    swim_teamunit.set_teamlink(group_id=xia_text)
    swim_teamunit.set_teamlink(group_id=zoa_text)
    sue1_bud.edit_idea_attr(swim_road, teamunit=swim_teamunit)
    sue1_bud_swim_idea = sue1_bud.get_idea_obj(swim_road)
    sue1_bud_swim_teamlinks = sue1_bud_swim_idea._teamunit._teamlinks
    assert len(sue1_bud_swim_teamlinks) == 2

    # WHEN
    sue2_bud = budunit_shop("Sue")
    sue2_bud.add_acctunit(xia_text)
    sue2_bud.set_l1_idea(
        sue1_bud_swim_idea, filter_out_missing_awardlinks_group_ids=False
    )

    # THEN
    sue2_bud_swim_idea = sue2_bud.get_idea_obj(swim_road)
    sue2_bud_swim_teamlinks = sue2_bud_swim_idea._teamunit._teamlinks
    assert len(sue2_bud_swim_teamlinks) == 1
    assert list(sue2_bud_swim_teamlinks) == [xia_text]
