from src._world.idea import ideaunit_shop
from src._world.world import worldunit_shop
from src._world.beliefunit import beliefunit_shop
from src._world.char import charunit_shop, charlink_shop
from src._world.origin import originunit_shop
from pytest import raises as pytest_raises
from src._world.examples.example_worlds import world_v001


def test_WorldUnit_meld_BaseScenario():
    # GIVEN
    bob_text = "Bob"
    bob1_world = worldunit_shop(bob_text)
    bob2_world = worldunit_shop(bob_text)
    assert bob1_world
    assert bob1_world._owner_id == bob_text

    # WHEN
    bob1_world.meld(exterior_world=bob2_world)

    # THEN
    assert bob1_world
    assert bob1_world._owner_id == bob_text


def test_WorldUnit_meld_WeightDoesNotCombine():
    # GIVEN
    bob_text = "Bob"
    bob1_world = worldunit_shop(bob_text)
    bob1_world._weight = 3
    bob2_world = worldunit_shop(bob_text)
    bob2_world._weight = 5
    assert bob1_world._weight == 3

    # WHEN
    bob1_world.meld(exterior_world=bob2_world)

    # THEN
    assert bob1_world._weight == 3


def test_WorldUnit_meld_CharUnits():
    # GIVEN
    yao_text = "Yao"
    yao_charunit = charunit_shop(char_id=yao_text)

    bob_text = "Bob"
    bob1_world = worldunit_shop(bob_text)
    bob1_world.set_charunit(yao_charunit)

    bob2_world = worldunit_shop(bob_text)
    bob2_world.set_charunit(yao_charunit)
    zia_text = "Zia"
    zia_charunit = charunit_shop(char_id=zia_text)
    bob2_world.set_charunit(zia_charunit)
    assert len(bob1_world._chars) == 1
    assert bob1_world.char_exists(yao_text)
    assert bob1_world.char_exists(zia_text) is False

    # WHEN
    bob1_world.meld(exterior_world=bob2_world)

    # THEN
    assert len(bob1_world._chars) == 2
    assert bob1_world.char_exists(yao_text)
    assert bob1_world.char_exists(zia_text)


def test_WorldUnit_meld_CharUnits_ignore_charunits_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_charunit = charunit_shop(char_id=yao_text)

    bob_text = "Bob"
    bob1_world = worldunit_shop(bob_text)
    bob1_world.set_charunit(yao_charunit)

    bob2_world = worldunit_shop(bob_text)
    bob2_world.set_charunit(yao_charunit)
    zia_text = "Zia"
    zia_charunit = charunit_shop(char_id=zia_text)
    bob2_world.set_charunit(zia_charunit)
    assert len(bob1_world._chars) == 1
    assert bob1_world.char_exists(yao_text)
    assert bob1_world.char_exists(zia_text) is False

    # WHEN
    bob1_world.meld(exterior_world=bob2_world, ignore_charunits=True)

    # THEN
    assert len(bob1_world._chars) == 1
    assert bob1_world.char_exists(yao_text)
    assert bob1_world.char_exists(zia_text) is False


def test_WorldUnit_meld_BeliefUnits_WhereBeliefUnitIsMissing():
    # GIVEN
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(belief_id=run_text)

    bob_text = "Bob"
    bob1_world = worldunit_shop(bob_text)
    bob1_world.set_beliefunit(run_beliefunit)

    bob2_world = worldunit_shop(bob_text)
    bob2_world.set_beliefunit(run_beliefunit)
    swim_text = ",swimmers"
    swim_beliefunit = beliefunit_shop(belief_id=swim_text)
    bob2_world.set_beliefunit(swim_beliefunit)
    assert len(bob1_world._beliefs) == 1
    assert bob1_world.get_beliefunit(run_text) != None
    assert bob1_world.get_beliefunit(swim_text) is None

    # WHEN
    bob1_world.meld(exterior_world=bob2_world)

    # THEN
    # for x_belief_id in bob1_world._beliefs.values():
    #     print(f"bob1_world {x_belief_id.char_id=}")

    assert len(bob1_world._beliefs) == 2
    assert bob1_world.get_beliefunit(run_text) != None
    assert bob1_world.get_beliefunit(swim_text) != None


def test_WorldUnit_meld_BeliefUnits_WhereBeliefUnitMembershipIsDifferent():
    # GIVEN

    bob_text = "Bob"
    bob1_world = worldunit_shop(bob_text)
    sue_text = "Sue"
    bob1_world.set_charunit(charunit_shop(sue_text))

    run_text = ",runners"
    bob1_world.set_beliefunit(beliefunit_shop(run_text))
    bob1_world.get_beliefunit(run_text).set_charlink(charlink_shop(sue_text))

    bob2_world = worldunit_shop(bob_text)
    yao_text = "Yao"
    bob2_world.set_charunit(charunit_shop(yao_text))
    bob2_world.set_charunit(charunit_shop(sue_text))
    bob2_world.set_beliefunit(beliefunit_shop(run_text))
    bob2_world.get_beliefunit(run_text).set_charlink(charlink_shop(yao_text))
    bob2_world.get_beliefunit(run_text).set_charlink(charlink_shop(sue_text))
    assert len(bob1_world._beliefs) == 2
    assert len(bob1_world.get_beliefunit(run_text)._chars) == 1

    # WHEN
    bob1_world.meld(exterior_world=bob2_world)

    # THEN
    assert len(bob1_world._beliefs) == 3
    assert len(bob1_world.get_beliefunit(run_text)._chars) == 2


def test_WorldUnit_idearoot_meld_idearoot_AttrCorrectlyMelded():
    # GIVEN
    bob_text = "Bob"
    bob1_world = worldunit_shop(bob_text)
    bob2_world = worldunit_shop(bob_text)
    bob2_world._idearoot._uid = 4
    assert bob1_world._idearoot._uid == 1
    assert bob2_world._idearoot._uid == 4

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob1_world.meld(bob2_world)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={bob1_world._real_id} _uid:1 with {bob2_world._real_id} _uid:4"
    )


def test_WorldUnit_idearoot_meld_Add4IdeasScenario():
    # GIVEN
    bob_text = "Bob"
    bob1_world = worldunit_shop(bob_text)

    tech_text = "tech"
    tech_road = bob1_world.make_l1_road(tech_text)
    bowl_text = "bowl"
    bowl_road = bob1_world.make_road(tech_road, bowl_text)
    swim_text = "swim"
    swim_road = bob1_world.make_l1_road(swim_text)
    free_text = "freestyle"
    free_road = bob1_world.make_road(swim_road, free_text)

    bob2_world = worldunit_shop(bob_text)
    bob2_world.add_l1_idea(ideaunit_shop(tech_text))
    bob2_world.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)
    bob2_world.add_idea(ideaunit_shop(free_text), parent_road=swim_road)
    assert len(bob1_world.get_idea_dict()) == 1
    assert bob1_world.idea_exists(tech_road) is False
    assert bob1_world.idea_exists(bowl_road) is False
    assert bob1_world.idea_exists(swim_road) is False
    assert bob1_world.idea_exists(free_road) is False

    # WHEN
    bob1_world.meld(bob2_world)

    # THEN
    assert len(bob1_world.get_idea_dict()) == 5
    assert bob1_world.idea_exists(tech_road)
    assert bob1_world.idea_exists(bowl_road)
    assert bob1_world.idea_exists(swim_road)
    assert bob1_world.idea_exists(free_road)
    assert bob1_world.get_idea_obj(tech_road)._label == tech_text
    assert bob1_world.get_idea_obj(bowl_road)._label == bowl_text
    assert bob1_world.get_idea_obj(swim_road)._label == swim_text
    assert bob1_world.get_idea_obj(free_road)._label == free_text


def test_WorldUnit_idearoot_meld_2EqualIdeasScenario():
    # GIVEN
    yao_text = "Yao"
    yao1_world = worldunit_shop(yao_text)
    tech_text = "tech"
    tech_road = yao1_world.make_l1_road(tech_text)
    bowl_text = "bowl"
    bowl_road = yao1_world.make_road(tech_road, bowl_text)

    yao1_world.add_l1_idea(ideaunit_shop(tech_text))
    yao1_world.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)

    yao2_world = worldunit_shop(yao_text)
    yao2_world.add_l1_idea(ideaunit_shop(tech_text))
    yao2_world.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)
    assert yao1_world.get_idea_obj(bowl_road)._weight == 1
    assert len(yao1_world.get_idea_dict()) == 3

    # WHEN
    yao1_world.meld(yao2_world)

    # THEN
    assert yao1_world.get_idea_obj(bowl_road)._weight == 1
    assert len(yao1_world.get_idea_dict()) == 3


def test_WorldUnit_factunits_meld_ReturnsCorrectObj_BaseScenario():
    # GIVEN
    bob_text = "Bob"
    bob1_world = worldunit_shop(bob_text)
    tech_text = "tech"
    tech_road = bob1_world.make_l1_road(tech_text)
    bowl_text = "bowl"
    bowl_road = bob1_world.make_road(tech_road, bowl_text)

    bob1_world.add_l1_idea(ideaunit_shop(tech_text))
    bob1_world.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)
    bob1_world.set_fact(base=tech_road, pick=bowl_road)

    bob2_world = worldunit_shop(bob_text)
    bob2_world.add_l1_idea(ideaunit_shop(tech_text))
    bob2_world.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)
    bob2_world.set_fact(base=tech_road, pick=bowl_road)
    bob1_idearoot = bob1_world._idearoot
    bob2_idearoot = bob2_world._idearoot
    assert len(bob1_idearoot._factunits) == 1
    assert len(bob1_idearoot._factunits) == len(bob2_idearoot._factunits)
    assert bob1_idearoot._factunits == bob2_idearoot._factunits

    # WHEN
    bob1_world.meld(bob2_world)

    # THEN
    assert len(bob1_idearoot._factunits) == 1
    assert len(bob1_idearoot._factunits) == len(bob2_idearoot._factunits)
    assert bob1_idearoot._factunits == bob2_idearoot._factunits


def test_WorldUnit_factunits_meld_ReturnsCorrectObj_2FactUnits():
    # GIVEN
    bob_text = "Bob"
    bob1_world = worldunit_shop(bob_text)
    tech_text = "tech"
    tech_road = bob1_world.make_l1_road(tech_text)
    bowl_text = "bowl"
    bowl_road = bob1_world.make_road(tech_road, bowl_text)
    swim_text = "swim"
    swim_road = bob1_world.make_l1_road(swim_text)
    free_text = "freestyle"

    bob1_world.add_l1_idea(ideaunit_shop(tech_text))
    bob1_world.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)
    bob1_world.add_idea(ideaunit_shop(free_text), parent_road=swim_road)
    bob1_world.set_fact(base=tech_road, pick=bowl_road)

    bob2_world = worldunit_shop(bob_text)
    bob2_world.add_l1_idea(ideaunit_shop(tech_text))
    bob2_world.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)
    bob2_world.add_idea(ideaunit_shop(free_text), parent_road=swim_road)
    bob2_world.set_fact(base=tech_road, pick=bowl_road)
    bob2_world.set_fact(base=swim_road, pick=swim_road)
    bob1_idearoot = bob1_world._idearoot
    bob2_idearoot = bob2_world._idearoot
    assert len(bob1_idearoot._factunits) == 1
    assert len(bob1_idearoot._factunits) != len(bob2_idearoot._factunits)
    assert bob1_idearoot._factunits != bob2_idearoot._factunits

    # WHEN
    bob1_world.meld(bob2_world)

    # THEN
    assert len(bob1_idearoot._factunits) == 2
    assert len(bob1_idearoot._factunits) == len(bob2_idearoot._factunits)
    assert bob1_idearoot._factunits == bob2_idearoot._factunits


def test_WorldUnit_factunits_meld_IdeasMeldedBeforeFacts():
    # GIVEN
    bob_text = "Bob"
    bob1_world = worldunit_shop(bob_text)

    swim_text = "swim"
    swim_road = bob1_world.make_l1_road(swim_text)
    free_text = "freestyle"

    bob2_world = worldunit_shop(bob_text)
    bob2_world.add_idea(ideaunit_shop(free_text), parent_road=swim_road)
    bob2_world.set_fact(base=swim_road, pick=swim_road)
    bob1_idearoot = bob1_world._idearoot
    bob2_idearoot = bob2_world._idearoot
    assert len(bob1_idearoot._factunits) == 0
    assert bob1_world.idea_exists(swim_road) is False
    assert len(bob1_idearoot._factunits) != len(bob2_idearoot._factunits)
    assert bob1_idearoot._factunits != bob2_world._idearoot._factunits

    # WHEN
    bob1_world.meld(bob2_world)

    # THEN
    assert len(bob1_idearoot._factunits) == 1
    assert bob1_world.get_idea_obj(swim_road)._label == swim_text
    assert len(bob1_idearoot._factunits) == len(bob2_idearoot._factunits)
    assert bob1_idearoot._factunits == bob2_world._idearoot._factunits


def test_WorldUnit_meld_BeliefsMeldedBefore_Chars():
    # GIVEN
    yao_text = "Yao"
    yao1_world = worldunit_shop(yao_text)
    yao2_world = worldunit_shop(yao_text)
    bob_text = "Bob"
    yao2_world.set_charunit(charunit_shop(bob_text))
    assert yao2_world.get_beliefunit(bob_text) != None
    yao2_world.set_beliefunit(beliefunit_shop(bob_text, _char_mirror=True))

    # WHEN/THEN
    assert yao1_world.meld(yao2_world) is None  # No error raised


def test_WorldUnit_factunits_meld_FactsAttributeCorrectlySet():
    # GIVEN
    bob_text = "Bob"
    bob1_world = worldunit_shop(bob_text)

    swim_text = "swim"
    swim_road = bob1_world.make_l1_road(swim_text)
    free_text = "freestyle"
    free_road = bob1_world.make_l1_road(free_text)
    bob1_world.add_idea(ideaunit_shop(free_text), parent_road=swim_road)

    bob2_world = worldunit_shop(bob_text)
    bob2_world.add_idea(ideaunit_shop(free_text), parent_road=swim_road)
    bob2_world.set_fact(base=swim_road, pick=free_road, open=23, nigh=27)
    bob1_idearoot = bob1_world._idearoot
    assert len(bob1_idearoot._factunits) == 0

    # WHEN
    bob1_world.meld(bob2_world)

    # THEN
    assert len(bob1_idearoot._factunits) == 1
    assert bob1_idearoot._factunits[swim_road].base == swim_road
    assert bob1_idearoot._factunits[swim_road].pick == free_road
    assert bob1_idearoot._factunits[swim_road].open == 23
    assert bob1_idearoot._factunits[swim_road].nigh == 27


def test_WorldUnit_meld_ReturnsCorrectObj_LargeExample():
    # GIVEN
    bob_text = "Bob"
    bob_world = worldunit_shop(bob_text, "music")
    bob_idearoot = bob_world._idearoot
    bob_idearoot._uid = 1
    yao_world = world_v001()

    yao_idearoot = yao_world._idearoot
    yao_worldr_bl = yao_idearoot._awardlines
    family_text = ",Family"
    yao_family_bl = yao_worldr_bl.get(family_text)

    print(f"Before {yao_family_bl._world_cred=} ")
    print(f"Before   {yao_family_bl._world_debt=} ")

    # WHEN
    bob_world.meld(yao_world)
    bob_world.get_tree_metrics()

    # THEN
    print(f"After  {yao_family_bl._world_cred=} ")
    print(f"After    {yao_family_bl._world_debt=} ")
    assert bob_world._weight == yao_world._weight
    assert bob_idearoot._kids == yao_idearoot._kids
    assert bob_idearoot._uid == yao_idearoot._uid
    assert bob_idearoot._factunits == yao_idearoot._factunits
    assert bob_world._beliefs == yao_world._beliefs
    assert bob_world._chars == yao_world._chars

    assert len(bob_idearoot._factunits) == 2
    assert len(bob_idearoot._factunits) == len(yao_idearoot._factunits)
    assert bob_world._owner_id != yao_world._owner_id
    print(f"{len(bob_world._beliefs.items())=}")
    # for bob_world_belief_key, bob_world_belief_obj in bob_world._beliefs.items():
    #     print(f"{bob_world_belief_key=}")
    #     assert bob_world_belief_obj.uid == yao_world._beliefs[bob_world_belief_key].uid
    #     assert bob_world_belief_obj == yao_world._beliefs[bob_world_belief_key]
    assert bob_world._beliefs == yao_world._beliefs
    assert len(bob_world.get_idea_dict()) == len(yao_world.get_idea_dict())

    bob_worldr_bl = bob_idearoot._awardlines
    bob_family_bl = bob_worldr_bl.get(family_text)
    print("Melded")

    assert bob_family_bl != None
    # assert bob_family_bl == yao_family_bl
    # assert bob_family_bl.world_cred == yao_family_bl .world_cred
    print(f"{bob_family_bl._world_cred=} ")
    print(f"{yao_family_bl._world_cred=} ")
    print(f"  {bob_family_bl._world_debt=} ")
    print(f"  {yao_family_bl._world_debt=} ")
    assert abs(bob_family_bl._world_cred - yao_family_bl._world_cred) < 0.0001
    assert abs(bob_family_bl._world_debt - yao_family_bl._world_debt) < 0.0001

    # for awardline in bob_worldr_bl.values():
    #     if awardline.char_id != fam_text:
    #         assert awardline == yao_worldr_bl.get(awardline.char_id)
    assert bob_worldr_bl == yao_worldr_bl
    # assert x_world1._idearoot._awardlines == bob2_world._idearoot._awardlines
    # assert x_world1._idearoot == bob2_world._idearoot


def test_WorldUnit__meld_originholds_CorrectlySetsOriginHolds():
    # GIVEN
    bob_text = "Bob"
    sue_text = "Sue"
    sue_weight = 4
    bob_world = worldunit_shop(bob_text)
    assert len(bob_world._originunit._originholds) == 0

    # WHEN
    bob_world._meld_originholds(char_id=sue_text, char_weight=sue_weight)

    # THEN
    assert len(bob_world._originunit._originholds) == 1
    bob_sue_originunit = originunit_shop()
    bob_sue_originunit.set_originhold(char_id=sue_text, weight=sue_weight)
    assert bob_world._originunit == bob_sue_originunit


def test_WorldUnit_meld_OriginUnitsCorrectlySet():
    # GIVEN
    bob_text = "Bob"
    bob_world = worldunit_shop(bob_text)

    swim_text = "swim"
    swim_road = bob_world.make_l1_road(swim_text)
    free_text = "freestyle"
    free_road = bob_world.make_road(swim_road, free_text)
    back_text = "backstroke"
    back_road = bob_world.make_road(swim_road, back_text)
    bob_world.add_idea(ideaunit_shop(free_text), parent_road=swim_road)

    sue_text = "Sue"
    sue_weight = 4
    sue_x_world = worldunit_shop(sue_text)
    sue_x_world.add_idea(ideaunit_shop(free_text), parent_road=swim_road)
    sue_x_world.set_fact(base=swim_road, pick=free_road, open=23, nigh=27)
    sue_x_world.add_idea(ideaunit_shop(back_text), parent_road=swim_road)
    assert len(bob_world._originunit._originholds) == 0

    # WHEN
    bob_world.meld(sue_x_world, char_weight=sue_weight)

    # THEN
    sue_originunit = originunit_shop()
    sue_originunit.set_originhold(char_id=sue_text, weight=sue_weight)
    assert len(bob_world._originunit._originholds) == 1
    assert bob_world._originunit == sue_originunit
    bob_free_idea = bob_world.get_idea_obj(free_road)
    bob_back_idea = bob_world.get_idea_obj(back_road)
    print(f"{bob_free_idea._originunit=}")
    print(f"{bob_back_idea._originunit=}")
    assert bob_free_idea._originunit != None
    assert bob_free_idea._originunit != originunit_shop()
    assert bob_free_idea._originunit == sue_originunit
    assert bob_back_idea._originunit != None
    assert bob_back_idea._originunit != originunit_shop()
    assert bob_back_idea._originunit == sue_originunit
