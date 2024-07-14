from src._road.road import get_default_real_id_roadnode
from src._world.beliefbox import (
    awardlink_shop,
    beliefbox_shop,
    get_chars_relevant_beliefs,
)
from src._world.char import charunit_shop, charlink_shop
from src._world.idea import ideaunit_shop
from src._world.world import worldunit_shop
from pytest import raises as pytest_raises


def test_WorldUnit_beliefs_get_beliefbox_ReturnsCorrectObj():
    # GIVEN
    x_world = worldunit_shop()
    swim_text = ",swimmers"
    # x_world.set_beliefbox(beliefbox_shop(swim_text))
    swim_beliefs = {swim_text: beliefbox_shop(swim_text)}
    x_world._beliefs = swim_beliefs

    # WHEN
    swim_beliefbox = x_world.get_beliefbox(swim_text)

    # THEN
    assert swim_beliefbox == beliefbox_shop(swim_text)


def test_WorldUnit_beliefs_set_beliefbox_CorrectlySetAttr():
    # GIVEN
    swim_text = ",swimmers"
    x_world = worldunit_shop()

    # WHEN
    x_world.set_beliefbox(beliefbox_shop(swim_text))

    # THEN
    assert len(x_world._beliefs) == 1
    swim_beliefs = {swim_text: beliefbox_shop(swim_text)}
    assert len(x_world._beliefs) == len(swim_beliefs)
    assert x_world.get_beliefbox(swim_text) != None
    swim_beliefbox = x_world.get_beliefbox(swim_text)
    assert swim_beliefbox._chars == swim_beliefs.get(swim_text)._chars
    assert x_world.get_beliefbox(swim_text) == swim_beliefs.get(swim_text)
    assert x_world._beliefs == swim_beliefs


def test_WorldUnit_beliefs_set_beliefbox_CorrectlyReplacesBelief():
    # GIVEN
    swim_text = ",swimmers"
    x_world = worldunit_shop()
    swim1_belief = beliefbox_shop(swim_text)
    bob_text = "Bob"
    swim1_belief.set_charlink(charlink_shop(bob_text))
    x_world.set_beliefbox(swim1_belief)
    assert len(x_world.get_beliefbox(swim_text)._chars) == 1

    # WHEN
    yao_text = "Yao"
    swim2_belief = beliefbox_shop(swim_text)
    swim2_belief.set_charlink(charlink_shop(bob_text))
    swim2_belief.set_charlink(charlink_shop(yao_text))
    x_world.set_beliefbox(swim2_belief, replace=False)

    # THEN
    assert len(x_world.get_beliefbox(swim_text)._chars) == 1

    # WHEN / THEN
    x_world.set_beliefbox(swim2_belief, replace=True)
    assert len(x_world.get_beliefbox(swim_text)._chars) == 2


def test_WorldUnit_beliefs_beliefbox_exists_ReturnsCorrectObj():
    # GIVEN
    swim_text = ",swimmers"
    sue_world = worldunit_shop("Sue")
    swim1_belief = beliefbox_shop(swim_text)
    bob_text = "Bob"
    swim1_belief.set_charlink(charlink_shop(bob_text))
    assert sue_world.beliefbox_exists(swim_text) == False

    # WHEN
    sue_world.set_beliefbox(swim1_belief)

    # THEN
    assert sue_world.beliefbox_exists(swim_text)


# def test_WorldUnit_beliefs_set_beliefbox_RaisesErrorWhen_char_mirrorSubmitted():
#     # GIVEN
#     yao_world = worldunit_shop("Yao")
#     bob_text = "Bob"
#     yao_world.set_charunit(charunit_shop(bob_text))
#     bob_beliefbox = yao_world.get_beliefbox(bob_text)

#     # WHEN
#     with pytest_raises(Exception) as excinfo:
#         yao_world.set_beliefbox(bob_beliefbox)
#     assert (
#         str(excinfo.value)
#         == f"WorldUnit.set_beliefbox('{bob_text}') fails because belief is _char_mirror."
#     )


def test_WorldUnit_beliefs_set_beliefbox_CorrectlySets_charlinks():
    # GIVEN
    swim_text = ",swimmers"
    x_world = worldunit_shop()
    swim1_belief = beliefbox_shop(swim_text)
    bob_text = "Bob"
    swim1_belief.set_charlink(charlink_shop(bob_text))
    x_world.set_beliefbox(swim1_belief)
    assert len(x_world.get_beliefbox(swim_text)._chars) == 1

    # WHEN
    yao_text = "Yao"
    swim2_belief = beliefbox_shop(swim_text)
    swim2_belief.set_charlink(charlink_shop(bob_text))
    swim2_belief.set_charlink(charlink_shop(yao_text))
    x_world.set_beliefbox(swim2_belief, add_charlinks=True)

    # THEN
    assert len(x_world.get_beliefbox(swim_text)._chars) == 2


def test_WorldUnit_beliefs_del_beliefbox_casasCorrectly():
    # GIVEN
    x_world = worldunit_shop()
    swim_text = ",swimmers"
    swim_belief = beliefbox_shop(swim_text)
    x_world.set_beliefbox(swim_belief)
    assert x_world.get_beliefbox(swim_text) != None

    # WHEN
    x_world.del_beliefbox(swim_text)
    assert x_world.get_beliefbox(swim_text) is None
    assert x_world._beliefs == {}


def test_WorldUnit_set_awardlink_correctly_sets_awardlinks():
    # GIVEN
    sue_text = "Sue"
    sue_world = worldunit_shop(sue_text)
    yao_text = "Yao"
    zia_text = "Zia"
    Xio_text = "Xio"
    sue_world.set_charunit(charunit_shop(yao_text))
    sue_world.set_charunit(charunit_shop(zia_text))
    sue_world.set_charunit(charunit_shop(Xio_text))

    assert len(sue_world._chars) == 3
    assert len(sue_world._beliefs) == 3
    swim_text = "swim"
    sue_world.add_l1_idea(ideaunit_shop(swim_text))
    awardlink_yao = awardlink_shop(yao_text, credor_weight=10)
    awardlink_zia = awardlink_shop(zia_text, credor_weight=10)
    awardlink_Xio = awardlink_shop(Xio_text, credor_weight=10)
    swim_road = sue_world.make_l1_road(swim_text)
    sue_world.edit_idea_attr(swim_road, awardlink=awardlink_yao)
    sue_world.edit_idea_attr(swim_road, awardlink=awardlink_zia)
    sue_world.edit_idea_attr(swim_road, awardlink=awardlink_Xio)

    street_text = "streets"
    sue_world.add_idea(ideaunit_shop(street_text), parent_road=swim_road)
    assert sue_world._idearoot._awardlinks in (None, {})
    assert len(sue_world._idearoot._kids[swim_text]._awardlinks) == 3

    # WHEN
    idea_dict = sue_world.get_idea_dict()

    # THEN
    print(f"{idea_dict.keys()=} {get_default_real_id_roadnode()=}")
    root_idea = idea_dict.get(get_default_real_id_roadnode())
    swim_idea = idea_dict.get(swim_road)
    street_idea = idea_dict.get(sue_world.make_road(swim_road, street_text))

    assert len(swim_idea._awardlinks) == 3
    assert len(swim_idea._awardheirs) == 3
    assert street_idea._awardlinks in (None, {})
    assert len(street_idea._awardheirs) == 3

    print(f"{len(idea_dict)}")
    print(f"{swim_idea._awardlinks}")
    print(f"{swim_idea._awardheirs}")
    print(f"{swim_idea._awardheirs}")
    assert len(sue_world._idearoot._kids["swim"]._awardheirs) == 3


def test_WorldUnit_set_awardlink_correctly_deletes_awardlinks():
    # GIVEN
    prom_text = "prom"
    x_world = worldunit_shop(prom_text)
    yao_text = "Yao"
    zia_text = "Zia"
    Xio_text = "Xio"
    x_world.set_charunit(charunit_shop(yao_text))
    x_world.set_charunit(charunit_shop(zia_text))
    x_world.set_charunit(charunit_shop(Xio_text))

    swim_text = "swim"
    swim_road = x_world.make_road(prom_text, swim_text)

    x_world.add_l1_idea(ideaunit_shop(swim_text))
    awardlink_yao = awardlink_shop(yao_text, credor_weight=10)
    awardlink_zia = awardlink_shop(zia_text, credor_weight=10)
    awardlink_Xio = awardlink_shop(Xio_text, credor_weight=10)

    swim_idea = x_world.get_idea_obj(swim_road)
    x_world.edit_idea_attr(swim_road, awardlink=awardlink_yao)
    x_world.edit_idea_attr(swim_road, awardlink=awardlink_zia)
    x_world.edit_idea_attr(swim_road, awardlink=awardlink_Xio)

    assert len(swim_idea._awardlinks) == 3
    assert len(swim_idea._awardheirs) == 3

    # print(f"{len(idea_list)}")
    # print(f"{idea_list[0]._awardlinks}")
    # print(f"{idea_list[0]._awardheirs}")
    # print(f"{idea_list[1]._awardheirs}")
    assert len(x_world._idearoot._kids[swim_text]._awardlinks) == 3
    assert len(x_world._idearoot._kids[swim_text]._awardheirs) == 3

    # WHEN
    x_world.edit_idea_attr(swim_road, awardlink_del=yao_text)

    # THEN
    swim_idea = x_world.get_idea_obj(swim_road)
    print(f"{swim_idea._label=}")
    print(f"{swim_idea._awardlinks=}")
    print(f"{swim_idea._awardheirs=}")

    assert len(x_world._idearoot._kids[swim_text]._awardlinks) == 2
    assert len(x_world._idearoot._kids[swim_text]._awardheirs) == 2


def test_WorldUnit_set_awardlink_CorrectlyCalculatesInheritedAwardLinkWorldImportance():
    # GIVEN
    sue_text = "Sue"
    sue_world = worldunit_shop(sue_text)
    yao_text = "Yao"
    zia_text = "Zia"
    Xio_text = "Xio"
    sue_world.set_charunit(charunit_shop(yao_text))
    sue_world.set_charunit(charunit_shop(zia_text))
    sue_world.set_charunit(charunit_shop(Xio_text))
    yao_awardlink = awardlink_shop(yao_text, credor_weight=20, debtor_weight=6)
    zia_awardlink = awardlink_shop(zia_text, credor_weight=10, debtor_weight=1)
    Xio_awardlink = awardlink_shop(Xio_text, credor_weight=10)
    sue_world._idearoot.set_awardlink(yao_awardlink)
    sue_world._idearoot.set_awardlink(zia_awardlink)
    sue_world._idearoot.set_awardlink(Xio_awardlink)
    assert len(sue_world._idearoot._awardlinks) == 3

    # WHEN
    idea_dict = sue_world.get_idea_dict()

    # THEN
    print(f"{idea_dict.keys()=}")
    idea_prom = idea_dict.get(get_default_real_id_roadnode())
    assert len(idea_prom._awardheirs) == 3

    bheir_yao = idea_prom._awardheirs.get(yao_text)
    bheir_zia = idea_prom._awardheirs.get(zia_text)
    bheir_Xio = idea_prom._awardheirs.get(Xio_text)
    assert bheir_yao._world_cred == 0.5
    assert bheir_yao._world_debt == 0.75
    assert bheir_zia._world_cred == 0.25
    assert bheir_zia._world_debt == 0.125
    assert bheir_Xio._world_cred == 0.25
    assert bheir_Xio._world_debt == 0.125
    assert bheir_yao._world_cred + bheir_zia._world_cred + bheir_Xio._world_cred == 1
    assert bheir_yao._world_debt + bheir_zia._world_debt + bheir_Xio._world_debt == 1

    # world_cred_sum = 0
    # world_debt_sum = 0
    # for belief in x_world._idearoot._awardheirs.values():
    #     print(f"{belief=}")
    #     assert belief._world_cred != None
    #     assert belief._world_cred in [0.25, 0.5]
    #     assert belief._world_debt != None
    #     assert belief._world_debt in [0.75, 0.125]
    #     world_cred_sum += belief._world_cred
    #     world_debt_sum += belief._world_debt

    # assert world_cred_sum == 1
    # assert world_debt_sum == 1


def test_WorldUnit_get_idea_list_CorrectlyCalculates1LevelWorldBeliefWorldImportance():
    # GIVEN
    prom_text = "prom"
    x_world = worldunit_shop(prom_text)
    yao_text = "Yao"
    zia_text = "Zia"
    Xio_text = "Xio"
    sue_text = "Sue"
    x_world.set_charunit(charunit_shop(yao_text))
    x_world.set_charunit(charunit_shop(zia_text))
    x_world.set_charunit(charunit_shop(Xio_text))
    yao_awardlink = awardlink_shop(yao_text, credor_weight=20, debtor_weight=6)
    zia_awardlink = awardlink_shop(zia_text, credor_weight=10, debtor_weight=1)
    Xio_awardlink = awardlink_shop(Xio_text, credor_weight=10)
    x_world._idearoot.set_awardlink(awardlink=yao_awardlink)
    x_world._idearoot.set_awardlink(awardlink=zia_awardlink)
    x_world._idearoot.set_awardlink(awardlink=Xio_awardlink)

    assert len(x_world._beliefs) == 3

    # WHEN
    x_world.calc_world_metrics()

    # THEN
    belief_yao = x_world.get_beliefbox(yao_text)
    belief_zia = x_world.get_beliefbox(zia_text)
    belief_Xio = x_world.get_beliefbox(Xio_text)
    assert belief_yao._world_cred == 0.5
    assert belief_yao._world_debt == 0.75
    assert belief_zia._world_cred == 0.25
    assert belief_zia._world_debt == 0.125
    assert belief_Xio._world_cred == 0.25
    assert belief_Xio._world_debt == 0.125
    assert belief_yao._world_cred + belief_zia._world_cred + belief_Xio._world_cred == 1
    assert belief_yao._world_debt + belief_zia._world_debt + belief_Xio._world_debt == 1

    # WHEN
    x_world.set_charunit(charunit_shop(sue_text))
    bl_sue = awardlink_shop(sue_text, credor_weight=37)
    x_world._idearoot.set_awardlink(awardlink=bl_sue)
    assert len(x_world._beliefs) == 4
    x_world.calc_world_metrics()

    # THEN
    belief_sue = x_world.get_beliefbox(sue_text)
    assert belief_yao._world_cred != 0.5
    assert belief_yao._world_debt != 0.75
    assert belief_zia._world_cred != 0.25
    assert belief_zia._world_debt != 0.125
    assert belief_Xio._world_cred != 0.25
    assert belief_Xio._world_debt != 0.125
    assert belief_sue._world_cred != None
    assert belief_sue._world_debt != None
    assert (
        belief_yao._world_cred
        + belief_zia._world_cred
        + belief_Xio._world_cred
        + belief_sue._world_cred
        == 1
    )
    assert (
        belief_yao._world_debt
        + belief_zia._world_debt
        + belief_Xio._world_debt
        + belief_sue._world_debt
        == 1
    )


def test_WorldUnit_get_idea_list_CorrectlyCalculates3levelWorldBeliefWorldImportance():
    # GIVEN
    prom_text = "prom"
    x_world = worldunit_shop(prom_text)
    swim_text = "swim"
    x_world.add_l1_idea(ideaunit_shop(swim_text))

    yao_text = "Yao"
    zia_text = "Zia"
    Xio_text = "Xio"
    x_world.set_charunit(charunit_shop(yao_text))
    x_world.set_charunit(charunit_shop(zia_text))
    x_world.set_charunit(charunit_shop(Xio_text))
    yao_awardlink = awardlink_shop(
        belief_id=yao_text, credor_weight=20, debtor_weight=6
    )
    zia_awardlink = awardlink_shop(
        belief_id=zia_text, credor_weight=10, debtor_weight=1
    )
    parm_awardlink = awardlink_shop(Xio_text, credor_weight=10)
    x_world._idearoot._kids[swim_text].set_awardlink(awardlink=yao_awardlink)
    x_world._idearoot._kids[swim_text].set_awardlink(awardlink=zia_awardlink)
    x_world._idearoot._kids[swim_text].set_awardlink(awardlink=parm_awardlink)
    assert len(x_world._beliefs) == 3

    # WHEN
    x_world.calc_world_metrics()

    # THEN
    belief_yao = x_world.get_beliefbox(yao_text)
    belief_zia = x_world.get_beliefbox(zia_text)
    belief_Xio = x_world.get_beliefbox(Xio_text)
    assert belief_yao._world_cred == 0.5
    assert belief_yao._world_debt == 0.75
    assert belief_zia._world_cred == 0.25
    assert belief_zia._world_debt == 0.125
    assert belief_Xio._world_cred == 0.25
    assert belief_Xio._world_debt == 0.125
    assert belief_yao._world_cred + belief_zia._world_cred + belief_Xio._world_cred == 1
    assert belief_yao._world_debt + belief_zia._world_debt + belief_Xio._world_debt == 1


def test_WorldUnit_get_idea_list_CorrectlyCalculatesBeliefWorldImportanceLWwithBeliefEmptyAncestors():
    # GIVEN
    prom_text = "prom"
    x_world = worldunit_shop(prom_text)
    swim_text = "swim"
    x_world.add_l1_idea(ideaunit_shop(swim_text))

    yao_text = "Yao"
    zia_text = "Zia"
    Xio_text = "Xio"
    x_world.set_charunit(charunit_shop(yao_text))
    x_world.set_charunit(charunit_shop(zia_text))
    x_world.set_charunit(charunit_shop(Xio_text))
    yao_awardlink = awardlink_shop(
        belief_id=yao_text, credor_weight=20, debtor_weight=6
    )
    zia_awardlink = awardlink_shop(
        belief_id=zia_text, credor_weight=10, debtor_weight=1
    )
    parm_awardlink = awardlink_shop(Xio_text, credor_weight=10)
    x_world._idearoot._kids[swim_text].set_awardlink(awardlink=yao_awardlink)
    x_world._idearoot._kids[swim_text].set_awardlink(awardlink=zia_awardlink)
    x_world._idearoot._kids[swim_text].set_awardlink(awardlink=parm_awardlink)

    # no awardlinks attached to this one
    x_world.add_l1_idea(ideaunit_shop("hunt", _weight=3))

    # WHEN
    x_world.calc_world_metrics()

    # THEN

    with pytest_raises(Exception) as excinfo:
        x_world._idearoot._awardlinks[yao_text]
    assert str(excinfo.value) == f"'{yao_text}'"
    with pytest_raises(Exception) as excinfo:
        x_world._idearoot._awardlinks[zia_text]
    assert str(excinfo.value) == f"'{zia_text}'"
    with pytest_raises(Exception) as excinfo:
        x_world._idearoot._awardlinks[Xio_text]
    assert str(excinfo.value) == f"'{Xio_text}'"
    with pytest_raises(Exception) as excinfo:
        x_world._idearoot._kids["hunt"]._awardheirs[yao_text]
    assert str(excinfo.value) == f"'{yao_text}'"
    with pytest_raises(Exception) as excinfo:
        x_world._idearoot._kids["hunt"]._awardheirs[zia_text]
    assert str(excinfo.value) == f"'{zia_text}'"
    with pytest_raises(Exception) as excinfo:
        x_world._idearoot._kids["hunt"]._awardheirs[Xio_text]
    assert str(excinfo.value) == f"'{Xio_text}'"

    # THEN
    belief_yao = x_world.get_beliefbox(yao_text)
    belief_zia = x_world.get_beliefbox(zia_text)
    belief_Xio = x_world.get_beliefbox(Xio_text)
    assert belief_yao._world_cred == 0.125
    assert belief_yao._world_debt == 0.1875
    assert belief_zia._world_cred == 0.0625
    assert belief_zia._world_debt == 0.03125
    assert belief_Xio._world_cred == 0.0625
    assert belief_Xio._world_debt == 0.03125
    assert (
        belief_yao._world_cred + belief_zia._world_cred + belief_Xio._world_cred == 0.25
    )
    assert (
        belief_yao._world_debt + belief_zia._world_debt + belief_Xio._world_debt == 0.25
    )


def test_WorldUnit_add_idea_CreatesMissingBeliefs():
    # GIVEN
    bob_text = "Bob"
    x_world = worldunit_shop(bob_text)
    casa_road = x_world.make_l1_road("casa")
    new_idea_parent_road = x_world.make_road(casa_road, "cleaning")
    clean_cookery_text = "clean_cookery"
    clean_cookery_idea = ideaunit_shop(
        _weight=40, _label=clean_cookery_text, pledge=True
    )

    family_text = ",family"
    awardlink_z = awardlink_shop(family_text)
    clean_cookery_idea.set_awardlink(awardlink=awardlink_z)
    assert len(x_world._beliefs) == 0
    assert x_world.get_beliefbox(family_text) is None

    # WHEN
    x_world.add_l1_idea(clean_cookery_idea, create_missing_beliefs=True)

    # THEN
    assert len(x_world._beliefs) == 1
    assert x_world.get_beliefbox(family_text) != None
    assert x_world.get_beliefbox(family_text)._chars in (None, {})


def test_WorldUnit__get_filtered_awardlinks_idea_CorrectlyFiltersIdea_awardlinks():
    # GIVEN
    noa_text = "Noa"
    x1_world = worldunit_shop(noa_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    x1_world.add_charunit(xia_text)
    x1_world.add_charunit(zoa_text)

    casa_text = "casa"
    casa_road = x1_world.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = x1_world.make_l1_road(swim_text)
    x1_world.add_l1_idea(ideaunit_shop(casa_text))
    x1_world.add_l1_idea(ideaunit_shop(swim_text))
    x1_world.edit_idea_attr(swim_road, awardlink=awardlink_shop(xia_text))
    x1_world.edit_idea_attr(swim_road, awardlink=awardlink_shop(zoa_text))
    x1_world_swim_idea = x1_world.get_idea_obj(swim_road)
    assert len(x1_world_swim_idea._awardlinks) == 2
    x_world = worldunit_shop(noa_text)
    x_world.add_charunit(xia_text)

    # WHEN
    filtered_idea = x_world._get_filtered_awardlinks_idea(x1_world_swim_idea)

    # THEN
    assert len(filtered_idea._awardlinks) == 1
    assert list(filtered_idea._awardlinks.keys()) == [xia_text]


def test_WorldUnit_add_idea_CorrectlyFiltersIdea_awardlinks():
    # GIVEN
    noa_text = "Noa"
    x1_world = worldunit_shop(noa_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    x1_world.add_charunit(xia_text)
    x1_world.add_charunit(zoa_text)

    casa_text = "casa"
    casa_road = x1_world.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = x1_world.make_l1_road(swim_text)
    x1_world.add_l1_idea(ideaunit_shop(casa_text))
    x1_world.add_l1_idea(ideaunit_shop(swim_text))
    x1_world.edit_idea_attr(swim_road, awardlink=awardlink_shop(xia_text))
    x1_world.edit_idea_attr(swim_road, awardlink=awardlink_shop(zoa_text))
    x1_world_swim_idea = x1_world.get_idea_obj(swim_road)
    assert len(x1_world_swim_idea._awardlinks) == 2

    # WHEN
    x_world = worldunit_shop(noa_text)
    x_world.add_charunit(xia_text)
    x_world.add_l1_idea(x1_world_swim_idea, create_missing_ideas=False)

    # THEN
    x_world_swim_idea = x_world.get_idea_obj(swim_road)
    assert len(x_world_swim_idea._awardlinks) == 1
    assert list(x_world_swim_idea._awardlinks.keys()) == [xia_text]


def test_WorldUnit_add_idea_DoesNotOverwriteBeliefs():
    # GIVEN
    bob_text = "Bob"
    bob_world = worldunit_shop(bob_text)
    casa_road = bob_world.make_l1_road("casa")
    new_idea_parent_road = bob_world.make_road(casa_road, "cleaning")
    clean_cookery_text = "clean_cookery"
    clean_cookery_idea = ideaunit_shop(
        _weight=40, _label=clean_cookery_text, pledge=True
    )

    family_text = ",family"
    awardlink_z = awardlink_shop(family_text)
    clean_cookery_idea.set_awardlink(awardlink=awardlink_z)

    beliefbox_z = beliefbox_shop(family_text)
    beliefbox_z.set_charlink(charlink_shop("ann1"))
    beliefbox_z.set_charlink(charlink_shop("bet1"))
    bob_world.set_beliefbox(beliefbox_z)

    # assert len(bob_world._beliefs) == 0
    # assert bob_world.get_beliefbox(family_text) is None
    assert len(bob_world._beliefs) == 1
    assert len(bob_world.get_beliefbox(family_text)._chars) == 2

    # WHEN
    bob_world.add_idea(
        idea_kid=clean_cookery_idea,
        parent_road=new_idea_parent_road,
        create_missing_beliefs=True,
    )

    # THEN

    # assert len(bob_world._beliefs) == 1
    # assert len(bob_world.get_beliefbox(family_text)._chars) == 0
    # beliefbox_z = beliefbox_shop(family_text)
    # beliefbox_z.set_charlink(charlink_shop("ann2"))
    # beliefbox_z.set_charlink(charlink_shop("bet2"))
    # bob_world.set_beliefbox(beliefbox_z)

    assert len(bob_world._beliefs) == 1
    assert len(bob_world.get_beliefbox(family_text)._chars) == 2


def test_WorldUnit_set_beliefbox_create_missing_chars_DoesCreateMissingChars():
    # GIVEN
    bob_world = worldunit_shop("Bob")
    family_text = ",family"
    yao_text = "Yao"
    sue_text = "Sue"
    beliefbox_z = beliefbox_shop(family_text)
    beliefbox_z.set_charlink(charlink_shop(yao_text, credor_weight=3, debtor_weight=7))
    beliefbox_z.set_charlink(charlink_shop(sue_text, credor_weight=5, debtor_weight=11))

    assert beliefbox_z._chars.get(yao_text).credor_weight == 3
    assert beliefbox_z._chars.get(yao_text).debtor_weight == 7

    assert beliefbox_z._chars.get(sue_text).credor_weight == 5
    assert beliefbox_z._chars.get(sue_text).debtor_weight == 11

    assert len(bob_world._chars) == 0
    assert len(bob_world._beliefs) == 0

    # WHEN
    bob_world.set_beliefbox(beliefbox_z, create_missing_chars=True)

    # THEN
    assert len(bob_world._chars) == 2
    assert len(bob_world._beliefs) == 3
    assert bob_world.get_char(yao_text).credor_weight == 3
    assert bob_world.get_char(yao_text).debtor_weight == 7

    assert bob_world.get_char(sue_text).credor_weight == 5
    assert bob_world.get_char(sue_text).debtor_weight == 11


def test_WorldUnit_set_beliefbox_create_missing_chars_DoesNotReplaceChars():
    # GIVEN
    bob_world = worldunit_shop("Bob")
    family_text = ",family"
    yao_text = "Yao"
    sue_text = "Sue"
    bob_world.set_charunit(charunit_shop(yao_text, credor_weight=17, debtor_weight=88))
    bob_world.set_charunit(charunit_shop(sue_text, credor_weight=46, debtor_weight=71))
    beliefbox_z = beliefbox_shop(family_text)
    beliefbox_z.set_charlink(charlink_shop(yao_text, credor_weight=3, debtor_weight=7))
    beliefbox_z.set_charlink(charlink_shop(sue_text, credor_weight=5, debtor_weight=11))

    assert beliefbox_z._chars.get(yao_text).credor_weight == 3
    assert beliefbox_z._chars.get(yao_text).debtor_weight == 7
    assert beliefbox_z._chars.get(sue_text).credor_weight == 5
    assert beliefbox_z._chars.get(sue_text).debtor_weight == 11
    assert len(bob_world._chars) == 2
    assert bob_world.get_char(yao_text).credor_weight == 17
    assert bob_world.get_char(yao_text).debtor_weight == 88
    assert bob_world.get_char(sue_text).credor_weight == 46
    assert bob_world.get_char(sue_text).debtor_weight == 71

    # WHEN
    bob_world.set_beliefbox(beliefbox_z, create_missing_chars=True)

    # THEN
    assert len(bob_world._chars) == 2
    assert bob_world.get_char(yao_text).credor_weight == 17
    assert bob_world.get_char(yao_text).debtor_weight == 88
    assert bob_world.get_char(sue_text).credor_weight == 46
    assert bob_world.get_char(sue_text).debtor_weight == 71


def test_get_chars_relevant_beliefs_ReturnsEmptyDict():
    # GIVEN
    bob_text = "Bob"
    world_with_chars = worldunit_shop(bob_text)

    yao_text = "Yao"
    world_with_chars.set_charunit(charunit_shop(bob_text))
    world_with_chars.set_charunit(charunit_shop(yao_text))

    world_with_beliefs = worldunit_shop()

    # WHEN
    print(f"{len(world_with_chars._chars)=} {len(world_with_beliefs._beliefs)=}")
    relevant_x = get_chars_relevant_beliefs(
        world_with_beliefs._beliefs, world_with_chars._chars
    )

    # THEN
    assert relevant_x == {}


def test_get_chars_relevant_beliefs_Returns2SingleCharBeliefs():
    # GIVEN
    bob_text = "Bob"
    yao_text = "Yao"
    zia_text = "Zia"
    world_3beliefs = worldunit_shop(bob_text)
    world_3beliefs.set_charunit(charunit_shop(bob_text))
    world_3beliefs.set_charunit(charunit_shop(yao_text))
    world_3beliefs.set_charunit(charunit_shop(zia_text))

    world_2chars = worldunit_shop(bob_text)
    world_2chars.set_charunit(charunit_shop(bob_text))
    world_2chars.set_charunit(charunit_shop(yao_text))

    # WHEN
    print(f"{len(world_2chars._chars)=} {len(world_3beliefs._beliefs)=}")
    mrg_x = get_chars_relevant_beliefs(world_3beliefs._beliefs, world_2chars._chars)

    # THEN
    assert mrg_x == {bob_text: {bob_text: -1}, yao_text: {yao_text: -1}}
