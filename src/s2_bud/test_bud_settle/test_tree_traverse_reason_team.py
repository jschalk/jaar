from src.s2_bud.reason_team import teamheir_shop, teamunit_shop
from src.s2_bud.bud import budunit_shop
from src.s2_bud.idea import ideaunit_shop


def test_bud_edit_idea_attr_CorrectlySetsTeamUnit():
    # ESTABLISH
    xio_bud = budunit_shop("Xio")
    run_str = "run"
    run_road = xio_bud.make_l1_road(run_str)
    xio_bud.set_l1_idea(ideaunit_shop(run_str))
    run_idea = xio_bud.get_idea_obj(run_road)
    assert run_idea.teamunit == teamunit_shop()

    # WHEN
    x_teamunit = teamunit_shop()
    xio_bud.edit_idea_attr(teamunit=x_teamunit, road=run_road)

    # THEN
    assert run_idea.teamunit == x_teamunit


def test_bud_idearoot_teamunit_CorrectlySets_idea_teamheir():
    # ESTABLISH
    x_teamunit = teamunit_shop()

    yao_bud = budunit_shop("Yao")
    yao_bud.edit_idea_attr(teamunit=x_teamunit, road=yao_bud._fiscal_id)
    assert yao_bud._idearoot.teamunit == x_teamunit
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
    bob_str = "Bob"
    x_teamunit = teamunit_shop()
    bob_bud = budunit_shop(bob_str)
    run_str = "run"
    run_road = bob_bud.make_l1_road(run_str)
    bob_bud.add_acctunit(bob_str)
    bob_bud.set_l1_idea(ideaunit_shop(run_str))
    bob_bud.edit_idea_attr(run_road, teamunit=x_teamunit)
    run_idea = bob_bud.get_idea_obj(run_road)
    assert run_idea.teamunit == x_teamunit
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
    bob_str = "Bob"
    x_teamunit = teamunit_shop()
    bob_bud = budunit_shop(bob_str)
    run_str = "run"
    run_road = bob_bud.make_l1_road(run_str)
    bob_bud.add_acctunit(bob_str)
    bob_bud.set_l1_idea(ideaunit_shop(run_str))
    bob_bud.edit_idea_attr(run_road, teamunit=x_teamunit)
    run_idea = bob_bud.get_idea_obj(run_road)
    assert run_idea.teamunit == x_teamunit
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
    swim_str = "swimming"
    swim_road = sue_bud.make_l1_road(swim_str)
    morn_str = "morning"
    morn_road = sue_bud.make_road(swim_road, morn_str)
    four_str = "fourth"
    four_road = sue_bud.make_road(morn_road, four_str)
    x_teamunit = teamunit_shop()
    swimmers_str = ";swimmers"
    x_teamunit.set_teamlink(group_id=swimmers_str)

    yao_str = "Yao"
    sue_bud.add_acctunit(yao_str)
    yao_acctunit = sue_bud.get_acct(yao_str)
    yao_acctunit.add_membership(swimmers_str)

    sue_bud.set_l1_idea(ideaunit_shop(swim_str))
    sue_bud.set_idea(ideaunit_shop(morn_str), parent_road=swim_road)
    sue_bud.set_idea(ideaunit_shop(four_str), parent_road=morn_road)
    sue_bud.edit_idea_attr(swim_road, teamunit=x_teamunit)
    # print(sue_bud.make_road(four_road=}\n{morn_road=))
    four_idea = sue_bud.get_idea_obj(four_road)
    assert four_idea.teamunit == teamunit_shop()
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
    sue_str = "Sue"
    sue1_bud = budunit_shop(sue_str)
    xia_str = "Xia"
    zoa_str = "Zoa"
    sue1_bud.add_acctunit(xia_str)
    sue1_bud.add_acctunit(zoa_str)

    casa_str = "casa"
    casa_road = sue1_bud.make_l1_road(casa_str)
    swim_str = "swim"
    swim_road = sue1_bud.make_l1_road(swim_str)
    sue1_bud.set_idea(ideaunit_shop(casa_str), parent_road=sue1_bud._fiscal_id)
    sue1_bud.set_idea(ideaunit_shop(swim_str), parent_road=sue1_bud._fiscal_id)
    swim_teamunit = teamunit_shop()
    swim_teamunit.set_teamlink(group_id=xia_str)
    swim_teamunit.set_teamlink(group_id=zoa_str)
    sue1_bud.edit_idea_attr(swim_road, teamunit=swim_teamunit)
    sue1_bud_swim_idea = sue1_bud.get_idea_obj(swim_road)
    sue1_bud_swim_teamlinks = sue1_bud_swim_idea.teamunit._teamlinks
    assert len(sue1_bud_swim_teamlinks) == 2

    # WHEN
    sue2_bud = budunit_shop(sue_str)
    sue2_bud.add_acctunit(xia_str)
    filtered_idea = sue2_bud._get_filtered_awardlinks_idea(sue1_bud_swim_idea)

    # THEN
    filtered_swim_teamlinks = filtered_idea.teamunit._teamlinks
    assert len(filtered_swim_teamlinks) == 1
    assert list(filtered_swim_teamlinks) == [xia_str]


def test_BudUnit_set_idea_CorrectlyFiltersIdea_awardlinks():
    # ESTABLISH
    sue1_bud = budunit_shop("Sue")
    xia_str = "Xia"
    zoa_str = "Zoa"
    sue1_bud.add_acctunit(xia_str)
    sue1_bud.add_acctunit(zoa_str)

    casa_str = "casa"
    casa_road = sue1_bud.make_l1_road(casa_str)
    swim_str = "swim"
    swim_road = sue1_bud.make_l1_road(swim_str)
    sue1_bud.set_idea(ideaunit_shop(casa_str), parent_road=sue1_bud._fiscal_id)
    sue1_bud.set_idea(ideaunit_shop(swim_str), parent_road=sue1_bud._fiscal_id)
    swim_teamunit = teamunit_shop()
    swim_teamunit.set_teamlink(group_id=xia_str)
    swim_teamunit.set_teamlink(group_id=zoa_str)
    sue1_bud.edit_idea_attr(swim_road, teamunit=swim_teamunit)
    sue1_bud_swim_idea = sue1_bud.get_idea_obj(swim_road)
    sue1_bud_swim_teamlinks = sue1_bud_swim_idea.teamunit._teamlinks
    assert len(sue1_bud_swim_teamlinks) == 2

    # WHEN
    sue2_bud = budunit_shop("Sue")
    sue2_bud.add_acctunit(xia_str)
    sue2_bud.set_l1_idea(
        sue1_bud_swim_idea, filter_out_missing_awardlinks_group_ids=False
    )

    # THEN
    sue2_bud_swim_idea = sue2_bud.get_idea_obj(swim_road)
    sue2_bud_swim_teamlinks = sue2_bud_swim_idea.teamunit._teamlinks
    assert len(sue2_bud_swim_teamlinks) == 1
    assert list(sue2_bud_swim_teamlinks) == [xia_str]
