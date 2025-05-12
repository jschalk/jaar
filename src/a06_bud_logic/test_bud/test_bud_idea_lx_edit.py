from src.a01_way_logic.way import (
    get_default_fisc_tag as root_tag,
    to_way,
    get_default_fisc_way,
)
from src.a05_idea_logic.idea import ideaunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._utils.example_buds import (
    get_budunit_with_4_levels_and_2reasons_2facts,
)
from pytest import raises as pytest_raises


def test_BudUnit_edit_idea_tag_FailsWhenIdeaDoesNotExist():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")

    casa_str = "casa"
    casa_way = yao_bud.make_l1_way(casa_str)
    swim_str = "swim"
    yao_bud.set_l1_idea(ideaunit_shop(casa_str))
    yao_bud.set_idea(ideaunit_shop(swim_str), parent_way=casa_way)

    # WHEN / THEN
    no_idea_way = yao_bud.make_l1_way("bees")
    with pytest_raises(Exception) as excinfo:
        yao_bud.edit_idea_tag(old_way=no_idea_way, new_idea_tag="birds")
    assert str(excinfo.value) == f"Idea old_way='{no_idea_way}' does not exist"


def test_BudUnit_edit_idea_tag_RaisesErrorForLevel0IdeaWhen_fisc_tag_isNone():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(owner_name=yao_str)

    casa_str = "casa"
    casa_way = yao_bud.make_l1_way(casa_str)
    swim_str = "swim"
    swim_way = yao_bud.make_way(casa_way, swim_str)
    yao_bud.set_l1_idea(ideaunit_shop(casa_str))
    yao_bud.set_idea(ideaunit_shop(swim_str), parent_way=casa_way)
    assert yao_bud.owner_name == yao_str
    assert yao_bud.idearoot.idea_tag == yao_bud.fisc_tag
    casa_idea = yao_bud.get_idea_obj(casa_way)
    assert casa_idea.parent_way == to_way(yao_bud.fisc_tag)
    swim_idea = yao_bud.get_idea_obj(swim_way)
    root_way = to_way(yao_bud.fisc_tag)
    assert swim_idea.parent_way == casa_way

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        moon_str = "moon"
        yao_bud.edit_idea_tag(old_way=root_way, new_idea_tag=moon_str)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string different than '{yao_bud.fisc_tag}'"
    )

    assert yao_bud.idearoot.idea_tag != moon_str
    assert yao_bud.idearoot.idea_tag == yao_bud.fisc_tag


def test_BudUnit_edit_idea_tag_RaisesErrorForLevel0When_fisc_tag_IsDifferent():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(owner_name=yao_str)
    casa_str = "casa"
    casa_way = yao_bud.make_l1_way(casa_str)
    swim_str = "swim"
    swim_way = yao_bud.make_way(casa_way, swim_str)
    yao_bud.set_l1_idea(ideaunit_shop(casa_str))
    yao_bud.set_idea(ideaunit_shop(swim_str), parent_way=casa_way)
    sun_str = "sun"
    yao_bud.fisc_tag = sun_str
    yao_bud.idearoot.fisc_tag = sun_str
    assert yao_bud.owner_name == yao_str
    assert yao_bud.fisc_tag == sun_str
    assert yao_bud.idearoot.fisc_tag == sun_str
    assert yao_bud.idearoot.idea_tag == root_tag()
    casa_idea = yao_bud.get_idea_obj(casa_way)
    assert casa_idea.parent_way == get_default_fisc_way()
    swim_idea = yao_bud.get_idea_obj(swim_way)
    assert swim_idea.parent_way == casa_way

    # WHEN

    with pytest_raises(Exception) as excinfo:
        moon_str = "moon"
        yao_bud.edit_idea_tag(old_way=get_default_fisc_way(), new_idea_tag=moon_str)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string different than '{sun_str}'"
    )


def test_BudUnit_find_replace_way_CorrectlyModifies_kids_Scenario1():
    # ESTABLISH Idea with kids that will be different
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)

    old_casa_str = "casa"
    old_casa_way = yao_bud.make_l1_way(old_casa_str)
    bloomers_str = "bloomers"
    old_bloomers_way = yao_bud.make_way(old_casa_way, bloomers_str)
    roses_str = "roses"
    old_roses_way = yao_bud.make_way(old_bloomers_way, roses_str)
    red_str = "red"
    old_red_way = yao_bud.make_way(old_roses_way, red_str)

    yao_bud.set_l1_idea(ideaunit_shop(old_casa_str))
    yao_bud.set_idea(ideaunit_shop(bloomers_str), parent_way=old_casa_way)
    yao_bud.set_idea(ideaunit_shop(roses_str), parent_way=old_bloomers_way)
    yao_bud.set_idea(ideaunit_shop(red_str), parent_way=old_roses_way)
    r_idea_roses = yao_bud.get_idea_obj(old_roses_way)
    r_idea_bloomers = yao_bud.get_idea_obj(old_bloomers_way)

    assert r_idea_bloomers._kids.get(roses_str) is not None
    assert r_idea_roses.parent_way == old_bloomers_way
    assert r_idea_roses._kids.get(red_str) is not None
    r_idea_red = r_idea_roses._kids.get(red_str)
    assert r_idea_red.parent_way == old_roses_way

    # WHEN
    new_casa_str = "casita"
    new_casa_way = yao_bud.make_l1_way(new_casa_str)
    yao_bud.edit_idea_tag(old_way=old_casa_way, new_idea_tag=new_casa_str)

    # THEN
    assert yao_bud.idearoot._kids.get(new_casa_str) is not None
    assert yao_bud.idearoot._kids.get(old_casa_str) is None

    assert r_idea_bloomers.parent_way == new_casa_way
    assert r_idea_bloomers._kids.get(roses_str) is not None

    r_idea_roses = r_idea_bloomers._kids.get(roses_str)
    new_bloomers_way = yao_bud.make_way(new_casa_way, bloomers_str)
    assert r_idea_roses.parent_way == new_bloomers_way
    assert r_idea_roses._kids.get(red_str) is not None
    r_idea_red = r_idea_roses._kids.get(red_str)
    new_roses_way = yao_bud.make_way(new_bloomers_way, roses_str)
    assert r_idea_red.parent_way == new_roses_way


def test_bud_edit_idea_tag_Modifies_factunits():
    # ESTABLISH bud with factunits that will be different
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)

    casa_str = "casa"
    casa_way = yao_bud.make_l1_way(casa_str)
    bloomers_str = "bloomers"
    bloomers_way = yao_bud.make_way(casa_way, bloomers_str)
    roses_str = "roses"
    roses_way = yao_bud.make_way(bloomers_way, roses_str)
    old_water_str = "water"
    old_water_way = yao_bud.make_l1_way(old_water_str)
    rain_str = "rain"
    old_rain_way = yao_bud.make_way(old_water_way, rain_str)

    yao_bud.set_l1_idea(ideaunit_shop(casa_str))
    yao_bud.set_idea(ideaunit_shop(roses_str), parent_way=bloomers_way)
    yao_bud.set_idea(ideaunit_shop(rain_str), parent_way=old_water_way)
    yao_bud.add_fact(fcontext=old_water_way, fbranch=old_rain_way)

    idea_x = yao_bud.get_idea_obj(roses_way)
    assert yao_bud.idearoot.factunits[old_water_way] is not None
    old_water_rain_factunit = yao_bud.idearoot.factunits[old_water_way]
    assert old_water_rain_factunit.fcontext == old_water_way
    assert old_water_rain_factunit.fbranch == old_rain_way

    # WHEN
    new_water_str = "h2o"
    new_water_way = yao_bud.make_l1_way(new_water_str)
    yao_bud.set_l1_idea(ideaunit_shop(new_water_str))
    assert yao_bud.idearoot.factunits.get(new_water_way) is None
    yao_bud.edit_idea_tag(old_way=old_water_way, new_idea_tag=new_water_str)

    # THEN
    assert yao_bud.idearoot.factunits.get(old_water_way) is None
    assert yao_bud.idearoot.factunits.get(new_water_way) is not None
    new_water_rain_factunit = yao_bud.idearoot.factunits[new_water_way]
    assert new_water_rain_factunit.fcontext == new_water_way
    new_rain_way = yao_bud.make_way(new_water_way, rain_str)
    assert new_water_rain_factunit.fbranch == new_rain_way

    assert yao_bud.idearoot.factunits.get(new_water_way)
    x_factunit = yao_bud.idearoot.factunits.get(new_water_way)
    # for factunit_key, x_factunit in yao_bud.idearoot.factunits.items():
    #     assert factunit_key == new_water_way
    assert x_factunit.fcontext == new_water_way
    assert x_factunit.fbranch == new_rain_way


def test_bud_edit_idea_tag_ModifiesIdeaReasonUnitsScenario1():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels_and_2reasons_2facts()
    old_weekday_str = "weekdays"
    old_weekday_way = sue_bud.make_l1_way(old_weekday_str)
    wednesday_str = "Wednesday"
    old_wednesday_way = sue_bud.make_way(old_weekday_way, wednesday_str)
    casa_idea = sue_bud.get_idea_obj(sue_bud.make_l1_way("casa"))
    # casa_wk_reason = reasonunit_shop(weekday, premises={wed_premise.rbranch: wed_premise})
    # nation_reason = reasonunit_shop(nationstate, premises={usa_premise.rbranch: usa_premise})
    assert len(casa_idea.reasonunits) == 2
    assert casa_idea.reasonunits.get(old_weekday_way) is not None
    wednesday_idea = sue_bud.get_idea_obj(old_weekday_way)
    casa_weekday_reason = casa_idea.reasonunits.get(old_weekday_way)
    assert casa_weekday_reason.premises.get(old_wednesday_way) is not None
    assert (
        casa_weekday_reason.premises.get(old_wednesday_way).rbranch == old_wednesday_way
    )
    new_weekday_str = "days of week"
    new_weekday_way = sue_bud.make_l1_way(new_weekday_str)
    new_wednesday_way = sue_bud.make_way(new_weekday_way, wednesday_str)
    assert casa_idea.reasonunits.get(new_weekday_str) is None

    # WHEN
    # for key_x, x_reason in casa_idea.reasonunits.items():
    #     print(f"Before {key_x=} {x_reason.rcontext=}")
    print(f"before {wednesday_idea.idea_tag=}")
    print(f"before {wednesday_idea.parent_way=}")
    sue_bud.edit_idea_tag(old_way=old_weekday_way, new_idea_tag=new_weekday_str)
    # for key_x, x_reason in casa_idea.reasonunits.items():
    #     print(f"after {key_x=} {x_reason.rcontext=}")
    print(f"after  {wednesday_idea.idea_tag=}")
    print(f"after  {wednesday_idea.parent_way=}")

    # THEN
    assert casa_idea.reasonunits.get(new_weekday_way) is not None
    assert casa_idea.reasonunits.get(old_weekday_way) is None
    casa_weekday_reason = casa_idea.reasonunits.get(new_weekday_way)
    assert casa_weekday_reason.premises.get(new_wednesday_way) is not None
    assert (
        casa_weekday_reason.premises.get(new_wednesday_way).rbranch == new_wednesday_way
    )
    assert len(casa_idea.reasonunits) == 2


def test_bud_set_owner_name_CorrectlyModifiesBoth():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels_and_2reasons_2facts()
    assert sue_bud.owner_name == "Sue"
    assert sue_bud.idearoot.idea_tag == sue_bud.fisc_tag
    # mid_idea_tag1 = "Yao"
    # sue_bud.edit_idea_tag(old_way=old_idea_tag, new_idea_tag=mid_idea_tag1)
    # assert sue_bud.owner_name == old_idea_tag
    # assert sue_bud.idearoot.idea_tag == mid_idea_tag1

    # WHEN
    bob_str = "Bob"
    sue_bud.set_owner_name(new_owner_name=bob_str)

    # THEN
    assert sue_bud.owner_name == bob_str
    assert sue_bud.idearoot.idea_tag == sue_bud.fisc_tag


def test_bud_edit_idea_tag_RaisesErrorIfbridgeIsInTag():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels_and_2reasons_2facts()
    old_weekday_str = "weekdays"
    old_weekday_way = sue_bud.make_l1_way(old_weekday_str)

    # WHEN / THEN
    new_weekday_str = "days; of week"
    with pytest_raises(Exception) as excinfo:
        sue_bud.edit_idea_tag(old_way=old_weekday_way, new_idea_tag=new_weekday_str)
    assert (
        str(excinfo.value)
        == f"Cannot modify '{old_weekday_way}' because new_idea_tag {new_weekday_str} contains bridge {sue_bud.bridge}"
    )
