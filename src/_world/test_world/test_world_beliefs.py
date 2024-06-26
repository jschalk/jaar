from src._road.road import get_default_real_id_roadnode
from src._world.beliefunit import (
    BeliefID,
    balancelink_shop,
    beliefunit_shop,
    get_persons_relevant_beliefs,
    get_person_relevant_beliefs,
)
from src._world.person import PersonID, personunit_shop, personlink_shop
from src._world.idea import ideaunit_shop
from src._world.world import worldunit_shop
from src._world.examples.example_worlds import world_v001 as examples_world_v001
from pytest import raises as pytest_raises


def test_WorldUnit_beliefs_get_beliefunit_ReturnsCorrectObj():
    # GIVEN
    x_world = worldunit_shop()
    swim_text = ",swimmers"
    # x_world.set_beliefunit(y_beliefunit=beliefunit_shop(belief_id=swim_text))
    swim_beliefs = {swim_text: beliefunit_shop(belief_id=swim_text)}
    x_world._beliefs = swim_beliefs

    # WHEN
    swim_beliefunit = x_world.get_beliefunit(swim_text)

    # THEN
    assert swim_beliefunit == beliefunit_shop(belief_id=swim_text)


def test_WorldUnit_beliefs_set_beliefunit_CorrectlySetAttr():
    # GIVEN
    swim_text = ",swimmers"
    x_world = worldunit_shop()

    # WHEN
    x_world.set_beliefunit(y_beliefunit=beliefunit_shop(belief_id=swim_text))

    # THEN
    assert len(x_world._beliefs) == 1
    swim_beliefs = {swim_text: beliefunit_shop(belief_id=swim_text)}
    assert len(x_world._beliefs) == len(swim_beliefs)
    assert x_world.get_beliefunit(swim_text) != None
    swim_beliefunit = x_world.get_beliefunit(swim_text)
    assert swim_beliefunit._persons == swim_beliefs.get(swim_text)._persons
    assert x_world.get_beliefunit(swim_text) == swim_beliefs.get(swim_text)
    assert x_world._beliefs == swim_beliefs


def test_WorldUnit_beliefs_set_beliefunit_CorrectlyReplacesBelief():
    # GIVEN
    swim_text = ",swimmers"
    x_world = worldunit_shop()
    swim1_belief = beliefunit_shop(swim_text)
    bob_text = "Bob"
    swim1_belief.set_personlink(personlink_shop(bob_text))
    x_world.set_beliefunit(swim1_belief)
    assert len(x_world.get_beliefunit(swim_text)._persons) == 1

    # WHEN
    yao_text = "Yao"
    swim2_belief = beliefunit_shop(swim_text)
    swim2_belief.set_personlink(personlink_shop(bob_text))
    swim2_belief.set_personlink(personlink_shop(yao_text))
    x_world.set_beliefunit(swim2_belief, replace=False)

    # THEN
    assert len(x_world.get_beliefunit(swim_text)._persons) == 1

    # WHEN / THEN
    x_world.set_beliefunit(swim2_belief, replace=True)
    assert len(x_world.get_beliefunit(swim_text)._persons) == 2


def test_WorldUnit_beliefs_beliefunit_exists_ReturnsCorrectObj():
    # GIVEN
    swim_text = ",swimmers"
    sue_world = worldunit_shop("Sue")
    swim1_belief = beliefunit_shop(swim_text)
    bob_text = "Bob"
    swim1_belief.set_personlink(personlink_shop(bob_text))
    assert sue_world.beliefunit_exists(swim_text) == False

    # WHEN
    sue_world.set_beliefunit(swim1_belief)

    # THEN
    assert sue_world.beliefunit_exists(swim_text)


# def test_WorldUnit_beliefs_set_beliefunit_RaisesErrorWhen_person_mirrorSubmitted():
#     # GIVEN
#     yao_world = worldunit_shop("Yao")
#     bob_text = "Bob"
#     yao_world.set_personunit(personunit_shop(bob_text))
#     bob_beliefunit = yao_world.get_beliefunit(bob_text)

#     # WHEN
#     with pytest_raises(Exception) as excinfo:
#         yao_world.set_beliefunit(bob_beliefunit)
#     assert (
#         str(excinfo.value)
#         == f"WorldUnit.set_beliefunit('{bob_text}') fails because belief is _person_mirror."
#     )


def test_WorldUnit_beliefs_set_beliefunit_CorrectlySets_personlinks():
    # GIVEN
    swim_text = ",swimmers"
    x_world = worldunit_shop()
    swim1_belief = beliefunit_shop(swim_text)
    bob_text = "Bob"
    swim1_belief.set_personlink(personlink_shop(bob_text))
    x_world.set_beliefunit(swim1_belief)
    assert len(x_world.get_beliefunit(swim_text)._persons) == 1

    # WHEN
    yao_text = "Yao"
    swim2_belief = beliefunit_shop(swim_text)
    swim2_belief.set_personlink(personlink_shop(bob_text))
    swim2_belief.set_personlink(personlink_shop(yao_text))
    x_world.set_beliefunit(swim2_belief, add_personlinks=True)

    # THEN
    assert len(x_world.get_beliefunit(swim_text)._persons) == 2


def test_WorldUnit_beliefs_del_beliefunit_casasCorrectly():
    # GIVEN
    x_world = worldunit_shop()
    swim_text = "swimmers"
    swim_belief = beliefunit_shop(belief_id=BeliefID(swim_text))
    x_world.set_beliefunit(y_beliefunit=swim_belief)
    assert x_world.get_beliefunit(swim_text) != None

    # WHEN
    x_world.del_beliefunit(belief_id=swim_text)
    assert x_world.get_beliefunit(swim_text) is None
    assert x_world._beliefs == {}


def test_examples_world_v001_HasBeliefs():
    # GIVEN / WHEN
    x_world = examples_world_v001()

    # THEN
    assert x_world._beliefs != None
    assert len(x_world._beliefs) == 34
    everyone_persons_len = None
    everyone_belief = x_world.get_beliefunit(",Everyone")
    everyone_persons_len = len(everyone_belief._persons)
    assert everyone_persons_len == 22

    # WHEN
    x_world.calc_world_metrics()
    idea_dict = x_world._idea_dict

    # THEN
    print(f"{len(idea_dict)=}")
    db_idea = idea_dict.get(x_world.make_l1_road("D&B"))
    print(f"{db_idea._label=} {db_idea._balancelinks=}")
    assert len(db_idea._balancelinks) == 3
    # for idea_key in idea_dict:
    #     print(f"{idea_key=}")
    #     if idea._label == "D&B":
    #         print(f"{idea._label=} {idea._balancelinks=}")
    #         db_balancelink_len = len(idea._balancelinks)
    # assert db_balancelink_len == 3


def test_WorldUnit_set_balancelink_correctly_sets_balancelinks():
    # GIVEN
    sue_text = "Sue"
    sue_world = worldunit_shop(sue_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    sue_world.set_personunit(personunit=personunit_shop(person_id=PersonID(rico_text)))
    sue_world.set_personunit(personunit=personunit_shop(person_id=PersonID(carm_text)))
    sue_world.set_personunit(personunit=personunit_shop(person_id=PersonID(patr_text)))

    assert len(sue_world._persons) == 3
    assert len(sue_world._beliefs) == 3
    swim_text = "swim"
    sue_world.add_l1_idea(ideaunit_shop(swim_text))
    balancelink_rico = balancelink_shop(belief_id=BeliefID(rico_text), credor_weight=10)
    balancelink_carm = balancelink_shop(belief_id=BeliefID(carm_text), credor_weight=10)
    balancelink_patr = balancelink_shop(belief_id=BeliefID(patr_text), credor_weight=10)
    swim_road = sue_world.make_l1_road(swim_text)
    sue_world.edit_idea_attr(road=swim_road, balancelink=balancelink_rico)
    sue_world.edit_idea_attr(road=swim_road, balancelink=balancelink_carm)
    sue_world.edit_idea_attr(road=swim_road, balancelink=balancelink_patr)

    street_text = "streets"
    sue_world.add_idea(ideaunit_shop(street_text), parent_road=swim_road)
    assert sue_world._idearoot._balancelinks in (None, {})
    assert len(sue_world._idearoot._kids[swim_text]._balancelinks) == 3

    # WHEN
    idea_dict = sue_world.get_idea_dict()

    # THEN
    print(f"{idea_dict.keys()=} {get_default_real_id_roadnode()=}")
    root_idea = idea_dict.get(get_default_real_id_roadnode())
    swim_idea = idea_dict.get(swim_road)
    street_idea = idea_dict.get(sue_world.make_road(swim_road, street_text))

    assert len(swim_idea._balancelinks) == 3
    assert len(swim_idea._balanceheirs) == 3
    assert street_idea._balancelinks in (None, {})
    assert len(street_idea._balanceheirs) == 3

    print(f"{len(idea_dict)}")
    print(f"{swim_idea._balancelinks}")
    print(f"{swim_idea._balanceheirs}")
    print(f"{swim_idea._balanceheirs}")
    assert len(sue_world._idearoot._kids["swim"]._balanceheirs) == 3


def test_WorldUnit_set_balancelink_correctly_deletes_balancelinks():
    # GIVEN
    prom_text = "prom"
    x_world = worldunit_shop(prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_world.set_personunit(personunit=personunit_shop(person_id=PersonID(rico_text)))
    x_world.set_personunit(personunit=personunit_shop(person_id=PersonID(carm_text)))
    x_world.set_personunit(personunit=personunit_shop(person_id=PersonID(patr_text)))

    swim_text = "swim"
    swim_road = x_world.make_road(prom_text, swim_text)

    x_world.add_l1_idea(ideaunit_shop(swim_text))
    balancelink_rico = balancelink_shop(belief_id=BeliefID(rico_text), credor_weight=10)
    balancelink_carm = balancelink_shop(belief_id=BeliefID(carm_text), credor_weight=10)
    balancelink_patr = balancelink_shop(belief_id=BeliefID(patr_text), credor_weight=10)

    swim_idea = x_world.get_idea_obj(swim_road)
    x_world.edit_idea_attr(road=swim_road, balancelink=balancelink_rico)
    x_world.edit_idea_attr(road=swim_road, balancelink=balancelink_carm)
    x_world.edit_idea_attr(road=swim_road, balancelink=balancelink_patr)

    assert len(swim_idea._balancelinks) == 3
    assert len(swim_idea._balanceheirs) == 3

    # print(f"{len(idea_list)}")
    # print(f"{idea_list[0]._balancelinks}")
    # print(f"{idea_list[0]._balanceheirs}")
    # print(f"{idea_list[1]._balanceheirs}")
    assert len(x_world._idearoot._kids[swim_text]._balancelinks) == 3
    assert len(x_world._idearoot._kids[swim_text]._balanceheirs) == 3

    # WHEN
    x_world.edit_idea_attr(road=swim_road, balancelink_del=rico_text)

    # THEN
    swim_idea = x_world.get_idea_obj(swim_road)
    print(f"{swim_idea._label=}")
    print(f"{swim_idea._balancelinks=}")
    print(f"{swim_idea._balanceheirs=}")

    assert len(x_world._idearoot._kids[swim_text]._balancelinks) == 2
    assert len(x_world._idearoot._kids[swim_text]._balanceheirs) == 2


def test_WorldUnit_set_balancelink_CorrectlyCalculatesInheritedBalanceLinkWorldImportance():
    # GIVEN
    sue_text = "Sue"
    sue_world = worldunit_shop(sue_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    sue_world.set_personunit(personunit=personunit_shop(person_id=PersonID(rico_text)))
    sue_world.set_personunit(personunit=personunit_shop(person_id=PersonID(carm_text)))
    sue_world.set_personunit(personunit=personunit_shop(person_id=PersonID(patr_text)))
    blink_rico = balancelink_shop(
        belief_id=rico_text, credor_weight=20, debtor_weight=6
    )
    blink_carm = balancelink_shop(
        belief_id=carm_text, credor_weight=10, debtor_weight=1
    )
    blink_patr = balancelink_shop(belief_id=patr_text, credor_weight=10)
    sue_world._idearoot.set_balancelink(balancelink=blink_rico)
    sue_world._idearoot.set_balancelink(balancelink=blink_carm)
    sue_world._idearoot.set_balancelink(balancelink=blink_patr)
    assert len(sue_world._idearoot._balancelinks) == 3

    # WHEN
    idea_dict = sue_world.get_idea_dict()

    # THEN
    print(f"{idea_dict.keys()=}")
    idea_prom = idea_dict.get(get_default_real_id_roadnode())
    assert len(idea_prom._balanceheirs) == 3

    bheir_rico = idea_prom._balanceheirs.get(rico_text)
    bheir_carm = idea_prom._balanceheirs.get(carm_text)
    bheir_patr = idea_prom._balanceheirs.get(patr_text)
    assert bheir_rico._world_cred == 0.5
    assert bheir_rico._world_debt == 0.75
    assert bheir_carm._world_cred == 0.25
    assert bheir_carm._world_debt == 0.125
    assert bheir_patr._world_cred == 0.25
    assert bheir_patr._world_debt == 0.125
    assert bheir_rico._world_cred + bheir_carm._world_cred + bheir_patr._world_cred == 1
    assert bheir_rico._world_debt + bheir_carm._world_debt + bheir_patr._world_debt == 1

    # world_cred_sum = 0
    # world_debt_sum = 0
    # for belief in x_world._idearoot._balanceheirs.values():
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
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    sele_text = "selena"
    x_world.set_personunit(personunit=personunit_shop(person_id=PersonID(rico_text)))
    x_world.set_personunit(personunit=personunit_shop(person_id=PersonID(carm_text)))
    x_world.set_personunit(personunit=personunit_shop(person_id=PersonID(patr_text)))
    blink_rico = balancelink_shop(
        belief_id=rico_text, credor_weight=20, debtor_weight=6
    )
    blink_carm = balancelink_shop(
        belief_id=carm_text, credor_weight=10, debtor_weight=1
    )
    blink_patr = balancelink_shop(belief_id=patr_text, credor_weight=10)
    x_world._idearoot.set_balancelink(balancelink=blink_rico)
    x_world._idearoot.set_balancelink(balancelink=blink_carm)
    x_world._idearoot.set_balancelink(balancelink=blink_patr)

    assert len(x_world._beliefs) == 3

    # WHEN
    x_world.calc_world_metrics()

    # THEN
    belief_rico = x_world.get_beliefunit(rico_text)
    belief_carm = x_world.get_beliefunit(carm_text)
    belief_patr = x_world.get_beliefunit(patr_text)
    assert belief_rico._world_cred == 0.5
    assert belief_rico._world_debt == 0.75
    assert belief_carm._world_cred == 0.25
    assert belief_carm._world_debt == 0.125
    assert belief_patr._world_cred == 0.25
    assert belief_patr._world_debt == 0.125
    assert (
        belief_rico._world_cred + belief_carm._world_cred + belief_patr._world_cred == 1
    )
    assert (
        belief_rico._world_debt + belief_carm._world_debt + belief_patr._world_debt == 1
    )

    # WHEN
    x_world.set_personunit(personunit=personunit_shop(person_id=PersonID(sele_text)))
    bl_sele = balancelink_shop(belief_id=sele_text, credor_weight=37)
    x_world._idearoot.set_balancelink(balancelink=bl_sele)
    assert len(x_world._beliefs) == 4
    x_world.calc_world_metrics()

    # THEN
    belief_sele = x_world.get_beliefunit(sele_text)
    assert belief_rico._world_cred != 0.5
    assert belief_rico._world_debt != 0.75
    assert belief_carm._world_cred != 0.25
    assert belief_carm._world_debt != 0.125
    assert belief_patr._world_cred != 0.25
    assert belief_patr._world_debt != 0.125
    assert belief_sele._world_cred != None
    assert belief_sele._world_debt != None
    assert (
        belief_rico._world_cred
        + belief_carm._world_cred
        + belief_patr._world_cred
        + belief_sele._world_cred
        == 1
    )
    assert (
        belief_rico._world_debt
        + belief_carm._world_debt
        + belief_patr._world_debt
        + belief_sele._world_debt
        == 1
    )


def test_WorldUnit_get_idea_list_CorrectlyCalculates3levelWorldBeliefWorldImportance():
    # GIVEN
    prom_text = "prom"
    x_world = worldunit_shop(prom_text)
    swim_text = "swim"
    x_world.add_l1_idea(ideaunit_shop(swim_text))

    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_world.set_personunit(personunit=personunit_shop(person_id=PersonID(rico_text)))
    x_world.set_personunit(personunit=personunit_shop(person_id=PersonID(carm_text)))
    x_world.set_personunit(personunit=personunit_shop(person_id=PersonID(patr_text)))
    rico_balancelink = balancelink_shop(
        belief_id=rico_text, credor_weight=20, debtor_weight=6
    )
    carm_balancelink = balancelink_shop(
        belief_id=carm_text, credor_weight=10, debtor_weight=1
    )
    parm_balancelink = balancelink_shop(belief_id=patr_text, credor_weight=10)
    x_world._idearoot._kids[swim_text].set_balancelink(balancelink=rico_balancelink)
    x_world._idearoot._kids[swim_text].set_balancelink(balancelink=carm_balancelink)
    x_world._idearoot._kids[swim_text].set_balancelink(balancelink=parm_balancelink)
    assert len(x_world._beliefs) == 3

    # WHEN
    x_world.calc_world_metrics()

    # THEN
    belief_rico = x_world.get_beliefunit(rico_text)
    belief_carm = x_world.get_beliefunit(carm_text)
    belief_patr = x_world.get_beliefunit(patr_text)
    assert belief_rico._world_cred == 0.5
    assert belief_rico._world_debt == 0.75
    assert belief_carm._world_cred == 0.25
    assert belief_carm._world_debt == 0.125
    assert belief_patr._world_cred == 0.25
    assert belief_patr._world_debt == 0.125
    assert (
        belief_rico._world_cred + belief_carm._world_cred + belief_patr._world_cred == 1
    )
    assert (
        belief_rico._world_debt + belief_carm._world_debt + belief_patr._world_debt == 1
    )


def test_WorldUnit_get_idea_list_CorrectlyCalculatesBeliefWorldImportanceLWwithBeliefEmptyAncestors():
    # GIVEN
    prom_text = "prom"
    x_world = worldunit_shop(prom_text)
    swim_text = "swim"
    x_world.add_l1_idea(ideaunit_shop(swim_text))

    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_world.set_personunit(personunit=personunit_shop(person_id=PersonID(rico_text)))
    x_world.set_personunit(personunit=personunit_shop(person_id=PersonID(carm_text)))
    x_world.set_personunit(personunit=personunit_shop(person_id=PersonID(patr_text)))
    rico_balancelink = balancelink_shop(
        belief_id=rico_text, credor_weight=20, debtor_weight=6
    )
    carm_balancelink = balancelink_shop(
        belief_id=carm_text, credor_weight=10, debtor_weight=1
    )
    parm_balancelink = balancelink_shop(belief_id=patr_text, credor_weight=10)
    x_world._idearoot._kids[swim_text].set_balancelink(balancelink=rico_balancelink)
    x_world._idearoot._kids[swim_text].set_balancelink(balancelink=carm_balancelink)
    x_world._idearoot._kids[swim_text].set_balancelink(balancelink=parm_balancelink)

    # no balancelinks attached to this one
    x_world.add_l1_idea(ideaunit_shop("hunt", _weight=3))

    # WHEN
    x_world.calc_world_metrics()

    # THEN

    with pytest_raises(Exception) as excinfo:
        x_world._idearoot._balancelinks[rico_text]
    assert str(excinfo.value) == f"'{rico_text}'"
    with pytest_raises(Exception) as excinfo:
        x_world._idearoot._balancelinks[carm_text]
    assert str(excinfo.value) == f"'{carm_text}'"
    with pytest_raises(Exception) as excinfo:
        x_world._idearoot._balancelinks[patr_text]
    assert str(excinfo.value) == f"'{patr_text}'"
    with pytest_raises(Exception) as excinfo:
        x_world._idearoot._kids["hunt"]._balanceheirs[rico_text]
    assert str(excinfo.value) == f"'{rico_text}'"
    with pytest_raises(Exception) as excinfo:
        x_world._idearoot._kids["hunt"]._balanceheirs[carm_text]
    assert str(excinfo.value) == f"'{carm_text}'"
    with pytest_raises(Exception) as excinfo:
        x_world._idearoot._kids["hunt"]._balanceheirs[patr_text]
    assert str(excinfo.value) == f"'{patr_text}'"

    # THEN
    belief_rico = x_world.get_beliefunit(rico_text)
    belief_carm = x_world.get_beliefunit(carm_text)
    belief_patr = x_world.get_beliefunit(patr_text)
    assert belief_rico._world_cred == 0.125
    assert belief_rico._world_debt == 0.1875
    assert belief_carm._world_cred == 0.0625
    assert belief_carm._world_debt == 0.03125
    assert belief_patr._world_cred == 0.0625
    assert belief_patr._world_debt == 0.03125
    assert (
        belief_rico._world_cred + belief_carm._world_cred + belief_patr._world_cred
        == 0.25
    )
    assert (
        belief_rico._world_debt + belief_carm._world_debt + belief_patr._world_debt
        == 0.25
    )


def test_WorldUnit_edit_beliefunit_belief_id_CorrectlyCreatesNewPersonID():
    # GIVEN
    world = worldunit_shop("prom")
    rico_text = "rico"
    world.add_personunit(person_id=rico_text)
    swim_text = ",swimmers"
    swim_belief = beliefunit_shop(belief_id=swim_text)
    swim_belief.set_personlink(personlink=personlink_shop(person_id=rico_text))
    world.set_beliefunit(swim_belief)
    assert len(world._persons) == 1
    assert len(world._beliefs) == 2
    assert world.get_beliefunit(swim_text) != None
    assert world.get_beliefunit(swim_text)._person_mirror is False
    assert len(world.get_beliefunit(swim_text)._persons) == 1

    # WHEN
    jog_text = ",jog"
    world.edit_beliefunit_belief_id(
        old_belief_id=swim_text, new_belief_id=jog_text, allow_belief_overwite=False
    )

    # THEN
    assert world.get_beliefunit(jog_text) != None
    assert world.get_beliefunit(swim_text) is None
    assert len(world._persons) == 1
    assert len(world._beliefs) == 2
    assert world.get_beliefunit(jog_text)._person_mirror is False
    assert len(world.get_beliefunit(jog_text)._persons) == 1


def test_WorldUnit_edit_Beliefunit_belief_id_raiseErrorNewPersonIDPreviouslyExists():
    # GIVEN
    world = worldunit_shop("prom")
    rico_text = "rico"
    world.add_personunit(person_id=rico_text)
    swim_text = ",swimmers"
    world.set_beliefunit(beliefunit_shop(belief_id=swim_text))
    jog_text = ",jog"
    world.set_beliefunit(beliefunit_shop(belief_id=jog_text))

    # WHEN
    with pytest_raises(Exception) as excinfo:
        world.edit_beliefunit_belief_id(
            old_belief_id=swim_text,
            new_belief_id=jog_text,
            allow_belief_overwite=False,
        )
    assert (
        str(excinfo.value)
        == f"Belief '{swim_text}' modify to '{jog_text}' failed since '{jog_text}' exists."
    )


def test_WorldUnit_edit_beliefunit_belief_id_CorrectlyMeldPersonIDs():
    # GIVEN
    world = worldunit_shop("prom")
    rico_text = "rico"
    world.add_personunit(person_id=rico_text)
    swim_text = ",swimmers"
    swim_belief = beliefunit_shop(belief_id=swim_text)
    swim_belief.set_personlink(
        personlink=personlink_shop(
            person_id=rico_text, credor_weight=5, debtor_weight=3
        )
    )
    world.set_beliefunit(swim_belief)
    jog_text = ",jog"
    jog_belief = beliefunit_shop(belief_id=jog_text)
    jog_belief.set_personlink(
        personlink=personlink_shop(
            person_id=rico_text, credor_weight=7, debtor_weight=10
        )
    )
    world.set_beliefunit(jog_belief)
    print(f"{world.get_beliefunit(jog_text)._persons.get(rico_text)=}")
    assert world.get_beliefunit(jog_text) != None

    # WHEN
    world.edit_beliefunit_belief_id(
        old_belief_id=swim_text,
        new_belief_id=jog_text,
        allow_belief_overwite=True,
    )

    # THEN
    assert world.get_beliefunit(jog_text) != None
    assert world.get_beliefunit(swim_text) is None
    assert len(world._persons) == 1
    assert len(world._beliefs) == 2
    assert world.get_beliefunit(jog_text)._person_mirror is False
    assert len(world.get_beliefunit(jog_text)._persons) == 1
    assert world.get_beliefunit(jog_text)._persons.get(rico_text).credor_weight == 12
    assert world.get_beliefunit(jog_text)._persons.get(rico_text).debtor_weight == 13


def test_WorldUnit_edit_beliefunit_belief_id_CorrectlyModifiesBalanceLinks():
    # GIVEN
    x_world = worldunit_shop("prom")
    rico_text = "rico"
    x_world.add_personunit(person_id=rico_text)
    swim_text = ",swimmers"
    swim_beliefunit = beliefunit_shop(belief_id=swim_text)
    x_world.set_beliefunit(swim_beliefunit)
    outdoor_text = "outdoors"
    outdoor_road = x_world.make_road(x_world._owner_id, outdoor_text)
    camping_text = "camping"
    camping_road = x_world.make_road(outdoor_road, camping_text)
    x_world.add_idea(ideaunit_shop(camping_text), parent_road=outdoor_road)

    camping_idea = x_world.get_idea_obj(camping_road)
    swim_balancelink = balancelink_shop(
        belief_id=swim_beliefunit.belief_id, credor_weight=5, debtor_weight=3
    )
    camping_idea.set_balancelink(swim_balancelink)
    assert camping_idea._balancelinks.get(swim_text) != None
    assert camping_idea._balancelinks.get(swim_text).credor_weight == 5
    assert camping_idea._balancelinks.get(swim_text).debtor_weight == 3

    # WHEN
    jog_text = ",jog"
    x_world.edit_beliefunit_belief_id(
        old_belief_id=swim_text, new_belief_id=jog_text, allow_belief_overwite=False
    )

    # THEN
    assert camping_idea._balancelinks.get(swim_text) is None
    assert camping_idea._balancelinks.get(jog_text) != None
    assert camping_idea._balancelinks.get(jog_text).credor_weight == 5
    assert camping_idea._balancelinks.get(jog_text).debtor_weight == 3


def test_WorldUnit_edit_beliefunit_belief_id_CorrectlyMeldsBalanceLinesBalanceLinksBalanceHeirs():
    # GIVEN
    x_world = worldunit_shop("prom")
    rico_text = "rico"
    x_world.add_personunit(person_id=rico_text)
    swim_text = ",swimmers"
    swim_beliefunit = beliefunit_shop(belief_id=swim_text)
    x_world.set_beliefunit(swim_beliefunit)

    jog_text = ",jog"
    jog_beliefunit = beliefunit_shop(belief_id=jog_text)
    x_world.set_beliefunit(jog_beliefunit)

    outdoor_text = "outdoors"
    outdoor_road = x_world.make_road(x_world._owner_id, outdoor_text)
    camping_text = "camping"
    camping_road = x_world.make_road(outdoor_road, camping_text)
    x_world.add_idea(ideaunit_shop(camping_text), parent_road=outdoor_road)

    camping_idea = x_world.get_idea_obj(camping_road)
    swim_balancelink = balancelink_shop(
        belief_id=swim_beliefunit.belief_id, credor_weight=5, debtor_weight=3
    )
    camping_idea.set_balancelink(swim_balancelink)
    jog_balancelink = balancelink_shop(
        belief_id=jog_beliefunit.belief_id, credor_weight=7, debtor_weight=10
    )
    camping_idea.set_balancelink(jog_balancelink)
    assert camping_idea._balancelinks.get(swim_text) != None
    assert camping_idea._balancelinks.get(swim_text).credor_weight == 5
    assert camping_idea._balancelinks.get(swim_text).debtor_weight == 3
    assert camping_idea._balancelinks.get(jog_text) != None
    assert camping_idea._balancelinks.get(jog_text).credor_weight == 7
    assert camping_idea._balancelinks.get(jog_text).debtor_weight == 10

    # WHEN
    x_world.edit_beliefunit_belief_id(
        old_belief_id=swim_text, new_belief_id=jog_text, allow_belief_overwite=True
    )

    # THEN
    assert camping_idea._balancelinks.get(swim_text) is None
    assert camping_idea._balancelinks.get(jog_text) != None
    assert camping_idea._balancelinks.get(jog_text).credor_weight == 12
    assert camping_idea._balancelinks.get(jog_text).debtor_weight == 13


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
    balancelink_z = balancelink_shop(belief_id=family_text)
    clean_cookery_idea.set_balancelink(balancelink=balancelink_z)
    assert len(x_world._beliefs) == 0
    assert x_world.get_beliefunit(family_text) is None

    # WHEN
    x_world.add_l1_idea(clean_cookery_idea, create_missing_beliefs=True)

    # THEN
    assert len(x_world._beliefs) == 1
    assert x_world.get_beliefunit(family_text) != None
    assert x_world.get_beliefunit(family_text)._persons in (None, {})


def test_WorldUnit__get_filtered_balancelinks_idea_CorrectlyFiltersIdea_balancelinks():
    # GIVEN
    noa_text = "Noa"
    x1_world = worldunit_shop(noa_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    x1_world.add_personunit(person_id=xia_text)
    x1_world.add_personunit(person_id=zoa_text)

    casa_text = "casa"
    casa_road = x1_world.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = x1_world.make_l1_road(swim_text)
    x1_world.add_l1_idea(ideaunit_shop(casa_text))
    x1_world.add_l1_idea(ideaunit_shop(swim_text))
    x1_world.edit_idea_attr(swim_road, balancelink=balancelink_shop(xia_text))
    x1_world.edit_idea_attr(swim_road, balancelink=balancelink_shop(zoa_text))
    x1_world_swim_idea = x1_world.get_idea_obj(swim_road)
    assert len(x1_world_swim_idea._balancelinks) == 2
    x_world = worldunit_shop(noa_text)
    x_world.add_personunit(person_id=xia_text)

    # WHEN
    filtered_idea = x_world._get_filtered_balancelinks_idea(x1_world_swim_idea)

    # THEN
    assert len(filtered_idea._balancelinks) == 1
    assert list(filtered_idea._balancelinks.keys()) == [xia_text]


def test_WorldUnit_add_idea_CorrectlyFiltersIdea_balancelinks():
    # GIVEN
    noa_text = "Noa"
    x1_world = worldunit_shop(noa_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    x1_world.add_personunit(person_id=xia_text)
    x1_world.add_personunit(person_id=zoa_text)

    casa_text = "casa"
    casa_road = x1_world.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = x1_world.make_l1_road(swim_text)
    x1_world.add_l1_idea(ideaunit_shop(casa_text))
    x1_world.add_l1_idea(ideaunit_shop(swim_text))
    x1_world.edit_idea_attr(
        road=swim_road, balancelink=balancelink_shop(belief_id=xia_text)
    )
    x1_world.edit_idea_attr(
        road=swim_road, balancelink=balancelink_shop(belief_id=zoa_text)
    )
    x1_world_swim_idea = x1_world.get_idea_obj(swim_road)
    assert len(x1_world_swim_idea._balancelinks) == 2

    # WHEN
    x_world = worldunit_shop(noa_text)
    x_world.add_personunit(person_id=xia_text)
    x_world.add_l1_idea(x1_world_swim_idea, create_missing_ideas=False)

    # THEN
    x_world_swim_idea = x_world.get_idea_obj(swim_road)
    assert len(x_world_swim_idea._balancelinks) == 1
    assert list(x_world_swim_idea._balancelinks.keys()) == [xia_text]


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
    balancelink_z = balancelink_shop(belief_id=family_text)
    clean_cookery_idea.set_balancelink(balancelink=balancelink_z)

    beliefunit_z = beliefunit_shop(belief_id=family_text)
    beliefunit_z.set_personlink(personlink=personlink_shop(person_id="ann1"))
    beliefunit_z.set_personlink(personlink=personlink_shop(person_id="bet1"))
    bob_world.set_beliefunit(y_beliefunit=beliefunit_z)

    # assert len(bob_world._beliefs) == 0
    # assert bob_world.get_beliefunit(family_text) is None
    assert len(bob_world._beliefs) == 1
    assert len(bob_world.get_beliefunit(family_text)._persons) == 2

    # WHEN
    bob_world.add_idea(
        idea_kid=clean_cookery_idea,
        parent_road=new_idea_parent_road,
        create_missing_beliefs=True,
    )

    # THEN

    # assert len(bob_world._beliefs) == 1
    # assert len(bob_world.get_beliefunit(family_text)._persons) == 0
    # beliefunit_z = beliefunit_shop(belief_id=family_text)
    # beliefunit_z.set_personlink(personlink=personlink_shop(person_id="ann2"))
    # beliefunit_z.set_personlink(personlink=personlink_shop(person_id="bet2"))
    # bob_world.set_beliefunit(y_beliefunit=beliefunit_z)

    assert len(bob_world._beliefs) == 1
    assert len(bob_world.get_beliefunit(family_text)._persons) == 2


def test_WorldUnit_set_beliefunit_create_missing_persons_DoesCreateMissingPersons():
    # GIVEN
    bob_world = worldunit_shop("Bob")
    family_text = ",family"
    anna_text = "anna"
    beto_text = "beto"
    beliefunit_z = beliefunit_shop(belief_id=family_text)
    beliefunit_z.set_personlink(
        personlink=personlink_shop(
            person_id=anna_text, credor_weight=3, debtor_weight=7
        )
    )
    beliefunit_z.set_personlink(
        personlink=personlink_shop(
            person_id=beto_text, credor_weight=5, debtor_weight=11
        )
    )

    assert beliefunit_z._persons.get(anna_text).credor_weight == 3
    assert beliefunit_z._persons.get(anna_text).debtor_weight == 7

    assert beliefunit_z._persons.get(beto_text).credor_weight == 5
    assert beliefunit_z._persons.get(beto_text).debtor_weight == 11

    assert len(bob_world._persons) == 0
    assert len(bob_world._beliefs) == 0

    # WHEN
    bob_world.set_beliefunit(y_beliefunit=beliefunit_z, create_missing_persons=True)

    # THEN
    assert len(bob_world._persons) == 2
    assert len(bob_world._beliefs) == 3
    assert bob_world._persons.get(anna_text).credor_weight == 3
    assert bob_world._persons.get(anna_text).debtor_weight == 7

    assert bob_world._persons.get(beto_text).credor_weight == 5
    assert bob_world._persons.get(beto_text).debtor_weight == 11


def test_WorldUnit_set_beliefunit_create_missing_persons_DoesNotReplacePersons():
    # GIVEN
    bob_world = worldunit_shop("Bob")
    family_text = ",family"
    anna_text = "anna"
    beto_text = "beto"
    bob_world.set_personunit(
        personunit_shop(person_id=anna_text, credor_weight=17, debtor_weight=88)
    )
    bob_world.set_personunit(
        personunit_shop(person_id=beto_text, credor_weight=46, debtor_weight=71)
    )
    beliefunit_z = beliefunit_shop(belief_id=family_text)
    beliefunit_z.set_personlink(
        personlink=personlink_shop(
            person_id=anna_text, credor_weight=3, debtor_weight=7
        )
    )
    beliefunit_z.set_personlink(
        personlink=personlink_shop(
            person_id=beto_text, credor_weight=5, debtor_weight=11
        )
    )

    assert beliefunit_z._persons.get(anna_text).credor_weight == 3
    assert beliefunit_z._persons.get(anna_text).debtor_weight == 7
    assert beliefunit_z._persons.get(beto_text).credor_weight == 5
    assert beliefunit_z._persons.get(beto_text).debtor_weight == 11
    assert len(bob_world._persons) == 2
    assert bob_world._persons.get(anna_text).credor_weight == 17
    assert bob_world._persons.get(anna_text).debtor_weight == 88
    assert bob_world._persons.get(beto_text).credor_weight == 46
    assert bob_world._persons.get(beto_text).debtor_weight == 71

    # WHEN
    bob_world.set_beliefunit(y_beliefunit=beliefunit_z, create_missing_persons=True)

    # THEN
    assert len(bob_world._persons) == 2
    assert bob_world._persons.get(anna_text).credor_weight == 17
    assert bob_world._persons.get(anna_text).debtor_weight == 88
    assert bob_world._persons.get(beto_text).credor_weight == 46
    assert bob_world._persons.get(beto_text).debtor_weight == 71


def test_WorldUnit_get_beliefunits_dict_ReturnsCorrectObj():
    # GIVEN
    bob_world = worldunit_shop("Bob")
    swim_text = ",swimmers"
    run_text = ",runners"
    fly_text = ",flyers"
    yao_text = "Yao"
    bob_world.set_personunit(personunit_shop(yao_text))
    bob_world.set_beliefunit(y_beliefunit=beliefunit_shop(belief_id=swim_text))
    bob_world.set_beliefunit(y_beliefunit=beliefunit_shop(belief_id=run_text))
    bob_world.set_beliefunit(y_beliefunit=beliefunit_shop(belief_id=fly_text))
    assert len(bob_world._beliefs) == 4

    # WHEN
    x_beliefunits_dict = bob_world.get_beliefunits_dict()

    # THEN
    assert x_beliefunits_dict.get(fly_text) != None
    assert x_beliefunits_dict.get(run_text) != None
    assert x_beliefunits_dict.get(swim_text) != None
    assert x_beliefunits_dict.get(yao_text) is None
    assert len(x_beliefunits_dict) == 3


def test_get_persons_relevant_beliefs_ReturnsEmptyDict():
    # GIVEN
    bob_text = "Bob"
    world_with_persons = worldunit_shop(bob_text)

    sam_text = "sam"
    wil_text = "wil"
    world_with_persons.set_personunit(personunit=personunit_shop(person_id=bob_text))
    world_with_persons.set_personunit(personunit=personunit_shop(person_id=sam_text))

    world_with_beliefs = worldunit_shop()

    # WHEN
    print(f"{len(world_with_persons._persons)=} {len(world_with_beliefs._beliefs)=}")
    relevant_x = get_persons_relevant_beliefs(
        world_with_beliefs._beliefs, world_with_persons._persons
    )

    # THEN
    assert relevant_x == {}


def test_get_persons_relevant_beliefs_Returns2SinglePersonBeliefs():
    # GIVEN
    bob_text = "Bob"
    sam_text = "Sam"
    wil_text = "Wil"
    world_3beliefs = worldunit_shop(bob_text)
    world_3beliefs.set_personunit(personunit=personunit_shop(person_id=bob_text))
    world_3beliefs.set_personunit(personunit=personunit_shop(person_id=sam_text))
    world_3beliefs.set_personunit(personunit=personunit_shop(person_id=wil_text))

    world_2persons = worldunit_shop(bob_text)
    world_2persons.set_personunit(personunit=personunit_shop(person_id=bob_text))
    world_2persons.set_personunit(personunit=personunit_shop(person_id=sam_text))

    # WHEN
    print(f"{len(world_2persons._persons)=} {len(world_3beliefs._beliefs)=}")
    mrg_x = get_persons_relevant_beliefs(
        world_3beliefs._beliefs, world_2persons._persons
    )

    # THEN
    assert mrg_x == {bob_text: {bob_text: -1}, sam_text: {sam_text: -1}}


def test_get_person_relevant_beliefs_ReturnsCorrectDict():
    # GIVEN
    jes_text = "Jessi"
    jes_world = worldunit_shop(jes_text)
    bob_text = "Bob"
    jes_world.set_personunit(personunit_shop(person_id=jes_text))
    jes_world.set_personunit(personunit_shop(person_id=bob_text))

    hike_text = "hikers"
    jes_world.set_beliefunit(beliefunit_shop(belief_id=hike_text))
    hike_belief = jes_world.get_beliefunit(hike_text)
    hike_belief.set_personlink(personlink_shop(bob_text))

    # WHEN
    noa_text = "Noa"
    noa_mrg = get_person_relevant_beliefs(jes_world._beliefs, noa_text)

    # THEN
    assert noa_mrg == {}


def test_get_person_relevant_beliefs_ReturnsCorrectDict():
    # GIVEN
    jes_text = "Jessi"
    jes_world = worldunit_shop(jes_text)
    bob_text = "Bob"
    noa_text = "Noa"
    eli_text = "Eli"
    jes_world.set_personunit(personunit_shop(person_id=jes_text))
    jes_world.set_personunit(personunit_shop(person_id=bob_text))
    jes_world.set_personunit(personunit_shop(person_id=noa_text))
    jes_world.set_personunit(personunit_shop(person_id=eli_text))

    swim_text = ",swimmers"
    jes_world.set_beliefunit(beliefunit_shop(belief_id=swim_text))
    swim_belief = jes_world.get_beliefunit(swim_text)
    swim_belief.set_personlink(personlink_shop(bob_text))

    hike_text = ",hikers"
    jes_world.set_beliefunit(beliefunit_shop(belief_id=hike_text))
    hike_belief = jes_world.get_beliefunit(hike_text)
    hike_belief.set_personlink(personlink_shop(bob_text))
    hike_belief.set_personlink(personlink_shop(noa_text))

    hunt_text = ",hunters"
    jes_world.set_beliefunit(beliefunit_shop(belief_id=hunt_text))
    hike_belief = jes_world.get_beliefunit(hunt_text)
    hike_belief.set_personlink(personlink_shop(noa_text))
    hike_belief.set_personlink(personlink_shop(eli_text))

    # WHEN
    print(f"{len(jes_world._persons)=} {len(jes_world._beliefs)=}")
    bob_mrg = get_person_relevant_beliefs(jes_world._beliefs, bob_text)

    # THEN
    assert bob_mrg == {bob_text: -1, swim_text: -1, hike_text: -1}
