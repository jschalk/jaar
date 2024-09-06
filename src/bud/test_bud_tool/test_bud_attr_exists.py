from src.bud.group import awardlink_shop
from src.bud.reason_idea import factunit_shop, reasonunit_shop
from src.bud.bud import budunit_shop
from src.bud.bud_tool import (
    budunit_exists,
    bud_acctunit_exists,
    bud_acct_membership_exists,
    bud_ideaunit_exists,
    bud_idea_awardlink_exists,
    bud_idea_reasonunit_exists,
    bud_idea_reason_premiseunit_exists as premiseunit_exists,
    bud_idea_teamlink_exists,
    bud_idea_healerlink_exists,
    bud_idea_factunit_exists,
)


def test_budunit_exists_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert not budunit_exists(None)
    assert budunit_exists(budunit_shop("Sue"))


def test_bud_acctunit_exists_ReturnsObj():
    # ESTABLISH
    yao_text = "Yao"
    sue_bud = budunit_shop("Sue")

    # WHEN / THEN
    assert not bud_acctunit_exists(None, None)
    assert not bud_acctunit_exists(sue_bud, yao_text)

    # WHEN
    sue_bud.add_acctunit(yao_text)

    #  THEN
    assert bud_acctunit_exists(sue_bud, yao_text)


def test_bud_acct_membership_exists_ReturnsObj():
    # ESTABLISH
    yao_text = "Yao"
    swim_text = ";swim"
    sue_bud = budunit_shop("Sue")

    # WHEN / THEN
    assert not bud_acct_membership_exists(None, None, None)
    assert not bud_acct_membership_exists(sue_bud, yao_text, swim_text)

    # WHEN
    sue_bud.add_acctunit(yao_text)
    # THEN
    assert not bud_acct_membership_exists(sue_bud, yao_text, swim_text)

    # WHEN
    yao_idea = sue_bud.get_acct(yao_text)
    yao_idea.add_membership(";run")
    # THEN
    assert not bud_acct_membership_exists(sue_bud, yao_text, swim_text)

    # WHEN
    yao_idea = sue_bud.get_acct(yao_text)
    yao_idea.add_membership(swim_text)
    # THEN
    assert bud_acct_membership_exists(sue_bud, yao_text, swim_text)


def test_bud_ideaunit_exists_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    sweep_road = sue_bud.make_road(clean_road, "sweep")
    x_parent_road = sue_bud._real_id

    # WHEN / THEN
    assert not bud_ideaunit_exists(None, None)
    assert not bud_ideaunit_exists(sue_bud, None)
    assert bud_ideaunit_exists(sue_bud, x_parent_road)
    assert not bud_ideaunit_exists(sue_bud, casa_road)
    assert not bud_ideaunit_exists(sue_bud, clean_road)
    assert not bud_ideaunit_exists(sue_bud, sweep_road)

    # WHEN
    sue_bud.add_idea(casa_road)
    # THEN
    assert not bud_ideaunit_exists(sue_bud, None)
    assert bud_ideaunit_exists(sue_bud, x_parent_road)
    assert bud_ideaunit_exists(sue_bud, casa_road)
    assert not bud_ideaunit_exists(sue_bud, clean_road)
    assert not bud_ideaunit_exists(sue_bud, sweep_road)

    # WHEN
    sue_bud.add_idea(clean_road)
    # THEN
    assert not bud_ideaunit_exists(sue_bud, None)
    assert bud_ideaunit_exists(sue_bud, x_parent_road)
    assert bud_ideaunit_exists(sue_bud, casa_road)
    assert bud_ideaunit_exists(sue_bud, clean_road)
    assert not bud_ideaunit_exists(sue_bud, sweep_road)


def test_bud_idea_awardlink_exists_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    swim_text = "Swim"

    # WHEN / THEN
    assert not bud_idea_awardlink_exists(None, None, None)
    assert not bud_idea_awardlink_exists(sue_bud, None, None)
    assert not bud_idea_awardlink_exists(sue_bud, root_road, swim_text)
    assert not bud_idea_awardlink_exists(sue_bud, casa_road, swim_text)
    assert not bud_idea_awardlink_exists(sue_bud, clean_road, swim_text)

    # WHEN
    sue_bud._idearoot.set_awardlink(awardlink_shop(swim_text))

    # THEN
    assert not bud_idea_awardlink_exists(sue_bud, None, None)
    assert bud_idea_awardlink_exists(sue_bud, root_road, swim_text)
    assert not bud_idea_awardlink_exists(sue_bud, casa_road, swim_text)
    assert not bud_idea_awardlink_exists(sue_bud, clean_road, swim_text)


def test_bud_idea_reasonunit_exists_ReturnsObj():
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    week_text = "week"
    week_road = sue_bud.make_l1_road(week_text)

    # WHEN / THEN
    assert not bud_idea_reasonunit_exists(None, None, None)
    assert not bud_idea_reasonunit_exists(sue_bud, None, None)
    assert not bud_idea_reasonunit_exists(sue_bud, root_road, week_road)
    assert not bud_idea_reasonunit_exists(sue_bud, casa_road, week_road)
    assert not bud_idea_reasonunit_exists(sue_bud, clean_road, week_road)

    # WHEN
    sue_bud.add_idea(week_road)
    sue_bud._idearoot.set_reasonunit(reasonunit_shop(week_road))

    # THEN
    assert not bud_idea_reasonunit_exists(sue_bud, None, None)
    assert bud_idea_reasonunit_exists(sue_bud, root_road, week_road)
    assert not bud_idea_reasonunit_exists(sue_bud, casa_road, week_road)
    assert not bud_idea_reasonunit_exists(sue_bud, clean_road, week_road)


def test_bud_idea_reason_premiseunit_exists_ReturnsObj():
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    week_text = "week"
    week_road = sue_bud.make_l1_road(week_text)
    thur_road = sue_bud.make_road(week_road, "thur")

    # WHEN / THEN
    assert not premiseunit_exists(None, None, None, None)
    assert not premiseunit_exists(sue_bud, None, None, None)
    assert not premiseunit_exists(sue_bud, root_road, week_road, thur_road)
    assert not premiseunit_exists(sue_bud, casa_road, week_road, thur_road)
    assert not premiseunit_exists(sue_bud, clean_road, week_road, thur_road)

    # WHEN
    sue_bud.add_idea(week_road)
    sue_bud._idearoot.set_reasonunit(reasonunit_shop(week_road))

    # THEN
    assert not premiseunit_exists(sue_bud, None, None, None)
    assert not premiseunit_exists(sue_bud, root_road, week_road, thur_road)
    assert not premiseunit_exists(sue_bud, casa_road, week_road, thur_road)
    assert not premiseunit_exists(sue_bud, clean_road, week_road, thur_road)

    # WHEN
    sue_bud.add_idea(thur_road)
    sue_bud._idearoot.get_reasonunit(week_road).set_premise(thur_road)

    # THEN
    assert not premiseunit_exists(sue_bud, None, None, None)
    assert premiseunit_exists(sue_bud, root_road, week_road, thur_road)
    assert not premiseunit_exists(sue_bud, casa_road, week_road, thur_road)
    assert not premiseunit_exists(sue_bud, clean_road, week_road, thur_road)


def test_bud_idea_teamlink_exists_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    swim_text = "Swim"

    # WHEN / THEN
    assert not bud_idea_teamlink_exists(None, None, None)
    assert not bud_idea_teamlink_exists(sue_bud, None, None)
    assert not bud_idea_teamlink_exists(sue_bud, root_road, swim_text)
    assert not bud_idea_teamlink_exists(sue_bud, casa_road, swim_text)
    assert not bud_idea_teamlink_exists(sue_bud, clean_road, swim_text)

    # WHEN
    sue_bud._idearoot._teamunit.set_teamlink(swim_text)

    # THEN
    assert not bud_idea_teamlink_exists(sue_bud, None, None)
    assert bud_idea_teamlink_exists(sue_bud, root_road, swim_text)
    assert not bud_idea_teamlink_exists(sue_bud, casa_road, swim_text)
    assert not bud_idea_teamlink_exists(sue_bud, clean_road, swim_text)


def test_bud_idea_healerlink_exists_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    swim_text = "Swim"

    # WHEN / THEN
    assert not bud_idea_healerlink_exists(None, None, None)
    assert not bud_idea_healerlink_exists(sue_bud, None, None)
    assert not bud_idea_healerlink_exists(sue_bud, root_road, swim_text)
    assert not bud_idea_healerlink_exists(sue_bud, casa_road, swim_text)
    assert not bud_idea_healerlink_exists(sue_bud, clean_road, swim_text)

    # WHEN
    sue_bud._idearoot._healerlink.set_healer_id(swim_text)

    # THEN
    assert not bud_idea_healerlink_exists(sue_bud, None, None)
    assert bud_idea_healerlink_exists(sue_bud, root_road, swim_text)
    assert not bud_idea_healerlink_exists(sue_bud, casa_road, swim_text)
    assert not bud_idea_healerlink_exists(sue_bud, clean_road, swim_text)


def test_bud_idea_factunit_exists_ReturnsObj():
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    week_text = "week"
    week_road = sue_bud.make_l1_road(week_text)

    # WHEN / THEN
    assert not bud_idea_factunit_exists(None, None, None)
    assert not bud_idea_factunit_exists(sue_bud, None, None)
    assert not bud_idea_factunit_exists(sue_bud, root_road, week_road)
    assert not bud_idea_factunit_exists(sue_bud, casa_road, week_road)
    assert not bud_idea_factunit_exists(sue_bud, clean_road, week_road)

    # WHEN
    sue_bud.add_idea(week_road)
    sue_bud._idearoot.set_factunit(factunit_shop(week_road))

    # THEN
    assert not bud_idea_factunit_exists(sue_bud, None, None)
    assert bud_idea_factunit_exists(sue_bud, root_road, week_road)
    assert not bud_idea_factunit_exists(sue_bud, casa_road, week_road)
    assert not bud_idea_factunit_exists(sue_bud, clean_road, week_road)


def test_budunit_exists_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert not budunit_exists(None)
    assert budunit_exists(budunit_shop("Sue"))


def test_bud_acctunit_exists_ReturnsObj():
    # ESTABLISH
    yao_text = "Yao"
    sue_bud = budunit_shop("Sue")

    # WHEN / THEN
    assert not bud_acctunit_exists(None, None)
    assert not bud_acctunit_exists(sue_bud, yao_text)

    # WHEN
    sue_bud.add_acctunit(yao_text)

    #  THEN
    assert bud_acctunit_exists(sue_bud, yao_text)


def test_bud_acct_membership_exists_ReturnsObj():
    # ESTABLISH
    yao_text = "Yao"
    swim_text = ";swim"
    sue_bud = budunit_shop("Sue")

    # WHEN / THEN
    assert not bud_acct_membership_exists(None, None, None)
    assert not bud_acct_membership_exists(sue_bud, yao_text, swim_text)

    # WHEN
    sue_bud.add_acctunit(yao_text)
    # THEN
    assert not bud_acct_membership_exists(sue_bud, yao_text, swim_text)

    # WHEN
    yao_idea = sue_bud.get_acct(yao_text)
    yao_idea.add_membership(";run")
    # THEN
    assert not bud_acct_membership_exists(sue_bud, yao_text, swim_text)

    # WHEN
    yao_idea = sue_bud.get_acct(yao_text)
    yao_idea.add_membership(swim_text)
    # THEN
    assert bud_acct_membership_exists(sue_bud, yao_text, swim_text)


def test_bud_ideaunit_exists_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    sweep_road = sue_bud.make_road(clean_road, "sweep")
    x_parent_road = sue_bud._real_id

    # WHEN / THEN
    assert not bud_ideaunit_exists(None, None)
    assert not bud_ideaunit_exists(sue_bud, None)
    assert bud_ideaunit_exists(sue_bud, x_parent_road)
    assert not bud_ideaunit_exists(sue_bud, casa_road)
    assert not bud_ideaunit_exists(sue_bud, clean_road)
    assert not bud_ideaunit_exists(sue_bud, sweep_road)

    # WHEN
    sue_bud.add_idea(casa_road)
    # THEN
    assert not bud_ideaunit_exists(sue_bud, None)
    assert bud_ideaunit_exists(sue_bud, x_parent_road)
    assert bud_ideaunit_exists(sue_bud, casa_road)
    assert not bud_ideaunit_exists(sue_bud, clean_road)
    assert not bud_ideaunit_exists(sue_bud, sweep_road)

    # WHEN
    sue_bud.add_idea(clean_road)
    # THEN
    assert not bud_ideaunit_exists(sue_bud, None)
    assert bud_ideaunit_exists(sue_bud, x_parent_road)
    assert bud_ideaunit_exists(sue_bud, casa_road)
    assert bud_ideaunit_exists(sue_bud, clean_road)
    assert not bud_ideaunit_exists(sue_bud, sweep_road)


def test_bud_idea_awardlink_exists_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    swim_text = "Swim"

    # WHEN / THEN
    assert not bud_idea_awardlink_exists(None, None, None)
    assert not bud_idea_awardlink_exists(sue_bud, None, None)
    assert not bud_idea_awardlink_exists(sue_bud, root_road, swim_text)
    assert not bud_idea_awardlink_exists(sue_bud, casa_road, swim_text)
    assert not bud_idea_awardlink_exists(sue_bud, clean_road, swim_text)

    # WHEN
    sue_bud._idearoot.set_awardlink(awardlink_shop(swim_text))

    # THEN
    assert not bud_idea_awardlink_exists(sue_bud, None, None)
    assert bud_idea_awardlink_exists(sue_bud, root_road, swim_text)
    assert not bud_idea_awardlink_exists(sue_bud, casa_road, swim_text)
    assert not bud_idea_awardlink_exists(sue_bud, clean_road, swim_text)


def test_bud_idea_reasonunit_exists_ReturnsObj():
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    week_text = "week"
    week_road = sue_bud.make_l1_road(week_text)

    # WHEN / THEN
    assert not bud_idea_reasonunit_exists(None, None, None)
    assert not bud_idea_reasonunit_exists(sue_bud, None, None)
    assert not bud_idea_reasonunit_exists(sue_bud, root_road, week_road)
    assert not bud_idea_reasonunit_exists(sue_bud, casa_road, week_road)
    assert not bud_idea_reasonunit_exists(sue_bud, clean_road, week_road)

    # WHEN
    sue_bud.add_idea(week_road)
    sue_bud._idearoot.set_reasonunit(reasonunit_shop(week_road))

    # THEN
    assert not bud_idea_reasonunit_exists(sue_bud, None, None)
    assert bud_idea_reasonunit_exists(sue_bud, root_road, week_road)
    assert not bud_idea_reasonunit_exists(sue_bud, casa_road, week_road)
    assert not bud_idea_reasonunit_exists(sue_bud, clean_road, week_road)


def test_bud_idea_reason_premiseunit_exists_ReturnsObj():
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    week_text = "week"
    week_road = sue_bud.make_l1_road(week_text)
    thur_road = sue_bud.make_road(week_road, "thur")

    # WHEN / THEN
    assert not premiseunit_exists(None, None, None, None)
    assert not premiseunit_exists(sue_bud, None, None, None)
    assert not premiseunit_exists(sue_bud, root_road, week_road, thur_road)
    assert not premiseunit_exists(sue_bud, casa_road, week_road, thur_road)
    assert not premiseunit_exists(sue_bud, clean_road, week_road, thur_road)

    # WHEN
    sue_bud.add_idea(week_road)
    sue_bud._idearoot.set_reasonunit(reasonunit_shop(week_road))

    # THEN
    assert not premiseunit_exists(sue_bud, None, None, None)
    assert not premiseunit_exists(sue_bud, root_road, week_road, thur_road)
    assert not premiseunit_exists(sue_bud, casa_road, week_road, thur_road)
    assert not premiseunit_exists(sue_bud, clean_road, week_road, thur_road)

    # WHEN
    sue_bud.add_idea(thur_road)
    sue_bud._idearoot.get_reasonunit(week_road).set_premise(thur_road)

    # THEN
    assert not premiseunit_exists(sue_bud, None, None, None)
    assert premiseunit_exists(sue_bud, root_road, week_road, thur_road)
    assert not premiseunit_exists(sue_bud, casa_road, week_road, thur_road)
    assert not premiseunit_exists(sue_bud, clean_road, week_road, thur_road)


def test_bud_idea_teamlink_exists_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    swim_text = "Swim"

    # WHEN / THEN
    assert not bud_idea_teamlink_exists(None, None, None)
    assert not bud_idea_teamlink_exists(sue_bud, None, None)
    assert not bud_idea_teamlink_exists(sue_bud, root_road, swim_text)
    assert not bud_idea_teamlink_exists(sue_bud, casa_road, swim_text)
    assert not bud_idea_teamlink_exists(sue_bud, clean_road, swim_text)

    # WHEN
    sue_bud._idearoot._teamunit.set_teamlink(swim_text)

    # THEN
    assert not bud_idea_teamlink_exists(sue_bud, None, None)
    assert bud_idea_teamlink_exists(sue_bud, root_road, swim_text)
    assert not bud_idea_teamlink_exists(sue_bud, casa_road, swim_text)
    assert not bud_idea_teamlink_exists(sue_bud, clean_road, swim_text)


def test_bud_idea_healerlink_exists_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    swim_text = "Swim"

    # WHEN / THEN
    assert not bud_idea_healerlink_exists(None, None, None)
    assert not bud_idea_healerlink_exists(sue_bud, None, None)
    assert not bud_idea_healerlink_exists(sue_bud, root_road, swim_text)
    assert not bud_idea_healerlink_exists(sue_bud, casa_road, swim_text)
    assert not bud_idea_healerlink_exists(sue_bud, clean_road, swim_text)

    # WHEN
    sue_bud._idearoot._healerlink.set_healer_id(swim_text)

    # THEN
    assert not bud_idea_healerlink_exists(sue_bud, None, None)
    assert bud_idea_healerlink_exists(sue_bud, root_road, swim_text)
    assert not bud_idea_healerlink_exists(sue_bud, casa_road, swim_text)
    assert not bud_idea_healerlink_exists(sue_bud, clean_road, swim_text)


def test_bud_idea_factunit_exists_ReturnsObj():
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = sue_bud.make_road(casa_road, clean_text)
    root_road = sue_bud._real_id
    week_text = "week"
    week_road = sue_bud.make_l1_road(week_text)

    # WHEN / THEN
    assert not bud_idea_factunit_exists(None, None, None)
    assert not bud_idea_factunit_exists(sue_bud, None, None)
    assert not bud_idea_factunit_exists(sue_bud, root_road, week_road)
    assert not bud_idea_factunit_exists(sue_bud, casa_road, week_road)
    assert not bud_idea_factunit_exists(sue_bud, clean_road, week_road)

    # WHEN
    sue_bud.add_idea(week_road)
    sue_bud._idearoot.set_factunit(factunit_shop(week_road))

    # THEN
    assert not bud_idea_factunit_exists(sue_bud, None, None)
    assert bud_idea_factunit_exists(sue_bud, root_road, week_road)
    assert not bud_idea_factunit_exists(sue_bud, casa_road, week_road)
    assert not bud_idea_factunit_exists(sue_bud, clean_road, week_road)
