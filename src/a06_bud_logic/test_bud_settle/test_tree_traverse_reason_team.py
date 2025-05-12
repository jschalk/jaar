from src.a01_way_logic.way import to_way
from src.a04_reason_logic.reason_team import teamheir_shop, teamunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a05_idea_logic.idea import ideaunit_shop


def test_bud_edit_idea_attr_CorrectlySetsTeamUnit():
    # ESTABLISH
    xio_bud = budunit_shop("Xio")
    run_str = "run"
    run_way = xio_bud.make_l1_way(run_str)
    xio_bud.set_l1_idea(ideaunit_shop(run_str))
    run_idea = xio_bud.get_idea_obj(run_way)
    assert run_idea.teamunit == teamunit_shop()

    # WHEN
    x_teamunit = teamunit_shop()
    xio_bud.edit_idea_attr(run_way, teamunit=x_teamunit)

    # THEN
    assert run_idea.teamunit == x_teamunit


def test_bud_idearoot_teamunit_CorrectlySets_idea_teamheir():
    # ESTABLISH
    x_teamunit = teamunit_shop()

    yao_bud = budunit_shop("Yao")
    root_way = to_way(yao_bud.fisc_tag)
    yao_bud.edit_idea_attr(root_way, teamunit=x_teamunit)
    assert yao_bud.idearoot.teamunit == x_teamunit
    assert yao_bud.idearoot._teamheir is None

    # WHEN
    yao_bud.settle_bud()

    # THEN
    x_teamheir = teamheir_shop()
    x_teamheir.set_teamlinks(
        parent_teamheir=None, teamunit=x_teamunit, bud_groupunits=None
    )
    assert yao_bud.idearoot._teamheir is not None
    assert yao_bud.idearoot._teamheir == x_teamheir


def test_bud_ideakid_teamunit_EmptyCorrectlySets_idea_teamheir():
    # ESTABLISH
    bob_str = "Bob"
    x_teamunit = teamunit_shop()
    bob_bud = budunit_shop(bob_str)
    run_str = "run"
    run_way = bob_bud.make_l1_way(run_str)
    bob_bud.add_acctunit(bob_str)
    bob_bud.set_l1_idea(ideaunit_shop(run_str))
    bob_bud.edit_idea_attr(run_way, teamunit=x_teamunit)
    run_idea = bob_bud.get_idea_obj(run_way)
    assert run_idea.teamunit == x_teamunit
    assert run_idea._teamheir is None

    # WHEN
    bob_bud.settle_bud()

    # THEN
    assert run_idea._teamheir is not None
    assert run_idea._teamheir._owner_name_team

    x_teamheir = teamheir_shop()
    x_teamheir.set_teamlinks(
        parent_teamheir=None,
        teamunit=x_teamunit,
        bud_groupunits=bob_bud._groupunits,
    )
    x_teamheir.set_owner_name_team(bob_bud._groupunits, bob_bud.owner_name)
    print(f"{x_teamheir._owner_name_team=}")
    assert run_idea._teamheir._owner_name_team == x_teamheir._owner_name_team
    assert run_idea._teamheir == x_teamheir


def test_bud_ideakid_teamunit_EmptyCorrectlySets_idea_teamheir():
    # ESTABLISH
    bob_str = "Bob"
    x_teamunit = teamunit_shop()
    bob_bud = budunit_shop(bob_str)
    run_str = "run"
    run_way = bob_bud.make_l1_way(run_str)
    bob_bud.add_acctunit(bob_str)
    bob_bud.set_l1_idea(ideaunit_shop(run_str))
    bob_bud.edit_idea_attr(run_way, teamunit=x_teamunit)
    run_idea = bob_bud.get_idea_obj(run_way)
    assert run_idea.teamunit == x_teamunit
    assert run_idea._teamheir is None

    # WHEN
    bob_bud.settle_bud()

    # THEN
    assert run_idea._teamheir is not None
    assert run_idea._teamheir._owner_name_team

    x_teamheir = teamheir_shop()
    x_teamheir.set_teamlinks(
        parent_teamheir=None,
        teamunit=x_teamunit,
        bud_groupunits=bob_bud._groupunits,
    )
    x_teamheir.set_owner_name_team(bob_bud._groupunits, bob_bud.owner_name)
    print(f"{x_teamheir._owner_name_team=}")
    assert run_idea._teamheir._owner_name_team == x_teamheir._owner_name_team
    assert run_idea._teamheir == x_teamheir


def test_bud_ideakid_teamunit_CorrectlySets_grandchild_idea_teamheir():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    swim_str = "swimming"
    swim_way = sue_bud.make_l1_way(swim_str)
    morn_str = "morning"
    morn_way = sue_bud.make_way(swim_way, morn_str)
    four_str = "fourth"
    four_way = sue_bud.make_way(morn_way, four_str)
    x_teamunit = teamunit_shop()
    swimmers_str = ";swimmers"
    x_teamunit.set_teamlink(team_label=swimmers_str)

    yao_str = "Yao"
    sue_bud.add_acctunit(yao_str)
    yao_acctunit = sue_bud.get_acct(yao_str)
    yao_acctunit.add_membership(swimmers_str)

    sue_bud.set_l1_idea(ideaunit_shop(swim_str))
    sue_bud.set_idea(ideaunit_shop(morn_str), parent_way=swim_way)
    sue_bud.set_idea(ideaunit_shop(four_str), parent_way=morn_way)
    sue_bud.edit_idea_attr(swim_way, teamunit=x_teamunit)
    # print(sue_bud.make_way(four_way=}\n{morn_way=))
    four_idea = sue_bud.get_idea_obj(four_way)
    assert four_idea.teamunit == teamunit_shop()
    assert four_idea._teamheir is None

    # WHEN
    sue_bud.settle_bud()

    # THEN
    x_teamheir = teamheir_shop()
    x_teamheir.set_teamlinks(
        parent_teamheir=None,
        teamunit=x_teamunit,
        bud_groupunits=sue_bud._groupunits,
    )
    assert four_idea._teamheir is not None
    assert four_idea._teamheir == x_teamheir


def test_BudUnit__get_filtered_awardlinks_idea_CorrectlyCleansIdea_Teamunit():
    # ESTABLISH
    sue_str = "Sue"
    sue1_bud = budunit_shop(sue_str)
    xia_str = "Xia"
    zoa_str = "Zoa"
    sue1_bud.add_acctunit(xia_str)
    sue1_bud.add_acctunit(zoa_str)

    casa_str = "casa"
    casa_way = sue1_bud.make_l1_way(casa_str)
    swim_str = "swim"
    swim_way = sue1_bud.make_l1_way(swim_str)
    sue1_bud.set_idea(ideaunit_shop(casa_str), parent_way=sue1_bud.fisc_tag)
    sue1_bud.set_idea(ideaunit_shop(swim_str), parent_way=sue1_bud.fisc_tag)
    swim_teamunit = teamunit_shop()
    swim_teamunit.set_teamlink(team_label=xia_str)
    swim_teamunit.set_teamlink(team_label=zoa_str)
    sue1_bud.edit_idea_attr(swim_way, teamunit=swim_teamunit)
    sue1_bud_swim_idea = sue1_bud.get_idea_obj(swim_way)
    sue1_bud_swim_teamlinks = sue1_bud_swim_idea.teamunit._teamlinks
    assert len(sue1_bud_swim_teamlinks) == 2

    # WHEN
    sue2_bud = budunit_shop(sue_str)
    sue2_bud.add_acctunit(xia_str)
    cleaned_idea = sue2_bud._get_filtered_awardlinks_idea(sue1_bud_swim_idea)

    # THEN
    cleaned_swim_teamlinks = cleaned_idea.teamunit._teamlinks
    assert len(cleaned_swim_teamlinks) == 1
    assert list(cleaned_swim_teamlinks) == [xia_str]


def test_BudUnit_set_idea_CorrectlyCleansIdea_awardlinks():
    # ESTABLISH
    sue1_bud = budunit_shop("Sue")
    xia_str = "Xia"
    zoa_str = "Zoa"
    sue1_bud.add_acctunit(xia_str)
    sue1_bud.add_acctunit(zoa_str)

    casa_str = "casa"
    casa_way = sue1_bud.make_l1_way(casa_str)
    swim_str = "swim"
    swim_way = sue1_bud.make_l1_way(swim_str)
    sue1_bud.set_idea(ideaunit_shop(casa_str), parent_way=sue1_bud.fisc_tag)
    sue1_bud.set_idea(ideaunit_shop(swim_str), parent_way=sue1_bud.fisc_tag)
    swim_teamunit = teamunit_shop()
    swim_teamunit.set_teamlink(team_label=xia_str)
    swim_teamunit.set_teamlink(team_label=zoa_str)
    sue1_bud.edit_idea_attr(swim_way, teamunit=swim_teamunit)
    sue1_bud_swim_idea = sue1_bud.get_idea_obj(swim_way)
    sue1_bud_swim_teamlinks = sue1_bud_swim_idea.teamunit._teamlinks
    assert len(sue1_bud_swim_teamlinks) == 2

    # WHEN
    sue2_bud = budunit_shop("Sue")
    sue2_bud.add_acctunit(xia_str)
    sue2_bud.set_l1_idea(
        sue1_bud_swim_idea, get_rid_of_missing_awardlinks_awardee_labels=False
    )

    # THEN
    sue2_bud_swim_idea = sue2_bud.get_idea_obj(swim_way)
    sue2_bud_swim_teamlinks = sue2_bud_swim_idea.teamunit._teamlinks
    assert len(sue2_bud_swim_teamlinks) == 1
    assert list(sue2_bud_swim_teamlinks) == [xia_str]
