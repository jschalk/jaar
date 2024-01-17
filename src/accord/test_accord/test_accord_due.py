# from src.world.examples.examples import (
#     get_farm_wantunit as examples_get_farm_wantunit,
#     get_farm_requestunit as examples_get_farm_requestunit,
# )
from src._prime.road import create_road
from src.accord.accord import accordunit_shop, dueunit_shop
from src.accord.examples.example_topics import (
    get_cooking_dueunit,
    get_speedboat_action_dueunit,
    get_climate_dueunit,
)


def test_AccordUnit_set_dueunit_SetsAttrCorrectly():
    # GIVEN
    farm_accordunit = accordunit_shop(_author="Bob", _reader="Tim")
    assert farm_accordunit._dueunits == {}

    # WHEN
    x_uid = 7
    x_author_weight = 3
    x_reader_weight = 9
    farm_accordunit.set_dueunit(dueunit_shop(x_uid, x_author_weight, x_reader_weight))

    # THEN
    assert len(farm_accordunit._dueunits) == 1
    assert farm_accordunit._dueunits.get(x_uid) != None
    x_dueunit = farm_accordunit._dueunits.get(x_uid)
    assert x_dueunit.author_weight == x_author_weight
    assert x_dueunit.reader_weight == x_reader_weight
    assert x_dueunit == dueunit_shop(x_uid, x_author_weight, x_reader_weight)


def test_AccordUnit_get_dueunit_ReturnsCorrectObj():
    # GIVEN
    farm_accordunit = accordunit_shop(_author="Bob", _reader="Tim")
    one_text = "1"
    farm_accordunit.set_dueunit(dueunit_shop(one_text))

    # WHEN / THEN
    assert farm_accordunit.get_dueunit(one_text) != None


def test_AccordUnit_dueunit_exists_ReturnsCorrectObj():
    # GIVEN
    farm_accordunit = accordunit_shop(_author="Bob", _reader="Tim")
    one_text = "1"
    assert farm_accordunit.dueunit_exists(one_text) == False

    # WHEN
    farm_accordunit.set_dueunit(dueunit_shop(one_text))

    # THEN
    assert farm_accordunit.dueunit_exists(one_text)


def test_AccordUnit_del_dueunit_CorrectlySetsAttr():
    # GIVEN
    farm_accordunit = accordunit_shop(_author="Bob", _reader="Tim")
    one_text = "1"
    farm_accordunit.set_dueunit(dueunit_shop(one_text))
    assert farm_accordunit.dueunit_exists(one_text)

    # WHEN
    farm_accordunit.del_dueunit(one_text)

    # THEN
    assert farm_accordunit.dueunit_exists(one_text) == False


def test_AccordUnit_add_dueunit_SetsAttrCorrectly():
    # GIVEN
    farm_accordunit = accordunit_shop(_author="Bob", _reader="Tim")
    assert farm_accordunit._dueunits == {}

    # WHEN
    one_dueunit = farm_accordunit.add_dueunit()

    # THEN
    assert one_dueunit.uid == 1
    assert one_dueunit.get_due_id() == "Due 0001"
    assert len(farm_accordunit._dueunits) == 1
    assert farm_accordunit.get_dueunit(one_dueunit.uid) != None

    # WHEN
    two_dueunit = farm_accordunit.add_dueunit()

    # THEN
    assert two_dueunit.uid == 2
    assert two_dueunit.get_due_id() == "Due 0002"
    assert len(farm_accordunit._dueunits) == 2
    assert farm_accordunit.get_dueunit(two_dueunit.uid) != None

    x_int = 7
    farm_accordunit.set_dueunit(dueunit_shop(x_int))
    assert len(farm_accordunit._dueunits) == 3

    # WHEN
    eight_dueunit = farm_accordunit.add_dueunit()

    # THEN
    assert eight_dueunit.uid == 8
    assert eight_dueunit.get_due_id() == "Due 0008"
    assert len(farm_accordunit._dueunits) == 4
    assert farm_accordunit.get_dueunit(eight_dueunit.uid) != None


def test_AccordUnit_edit_dueunit_attr_CorrectlySetsAttribute():
    # GIVEN
    tim_text = "Tim"
    farm_accordunit = accordunit_shop(_author="Bob", _reader=tim_text)
    x_uid = 7
    x_author_weight = 3
    x_reader_weight = 3
    farm_accordunit.set_dueunit(dueunit_shop(x_uid, x_author_weight, x_reader_weight))

    x_dueunit = farm_accordunit._dueunits.get(x_uid)
    assert x_dueunit.author_weight == x_author_weight
    assert x_dueunit.reader_weight == x_reader_weight
    assert x_dueunit.actor is None

    # WHEN
    y_author_weight = 7
    y_reader_weight = 15
    farm_accordunit.edit_dueunit_attr(
        x_uid,
        author_weight=y_author_weight,
        reader_weight=y_reader_weight,
        actor=tim_text,
    )

    # THEN
    x_dueunit = farm_accordunit._dueunits.get(x_uid)
    assert x_dueunit.author_weight != x_author_weight
    assert x_dueunit.reader_weight != x_reader_weight
    assert x_dueunit.author_weight == y_author_weight
    assert x_dueunit.reader_weight == y_reader_weight
    assert x_dueunit.actor != None
    assert x_dueunit.actor == tim_text


def test_AccordUnit_set_actor_dueunit_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    farm_accordunit = accordunit_shop(_author=bob_text, _reader="Tim")
    eight_dueunit = get_cooking_dueunit()
    farm_accordunit.set_dueunit(eight_dueunit)

    cooking_dueunit = farm_accordunit.get_dueunit(eight_dueunit.uid)
    assert cooking_dueunit.get_actor(bob_text) is None

    # WHEN
    farm_accordunit.set_actor(actor=bob_text, due_uid=eight_dueunit.uid)

    # THEN
    assert cooking_dueunit.get_actor(bob_text) != None


def test_AccordUnit_del_actor_dueunit_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    farm_accordunit = accordunit_shop(_author=bob_text, _reader="Tim")
    eight_dueunit = get_cooking_dueunit()
    farm_accordunit.set_dueunit(eight_dueunit)
    cooking_dueunit = farm_accordunit.get_dueunit(eight_dueunit.uid)
    farm_accordunit.set_actor(actor=bob_text, due_uid=eight_dueunit.uid)
    assert cooking_dueunit.get_actor(bob_text) != None

    # WHEN
    farm_accordunit.del_actor(actor=bob_text, due_uid=eight_dueunit.uid)

    # THEN
    assert cooking_dueunit.get_actor(bob_text) is None


def test_AccordUnit_get_actor_dueunits_ReturnsCorrectObjs():
    # GIVEN
    bob_text = "Bob"
    farm_accordunit = accordunit_shop(_author=bob_text, _reader="Tim")
    eight_dueunit = get_cooking_dueunit()
    farm_accordunit.set_dueunit(eight_dueunit)
    assert farm_accordunit.get_actor_dueunits(eight_dueunit.uid) == {}

    # WHEN
    farm_accordunit.set_actor(bob_text, due_uid=eight_dueunit.uid)

    # THEN
    assert farm_accordunit.get_actor_dueunits(bob_text) != {}
    bob_dueunits = farm_accordunit.get_actor_dueunits(bob_text)
    assert len(bob_dueunits) == 1
    example_cooking_dueunit = get_cooking_dueunit()
    example_cooking_dueunit.set_actor(bob_text)
    assert bob_dueunits.get(eight_dueunit.uid) == example_cooking_dueunit


def test_AccordUnit_get_actor_dueunits_ReturnsCorrectActionTopics():
    # GIVEN
    bob_text = "Bob"
    yao_text = "Yao"
    farm_accordunit = accordunit_shop(_author=bob_text, _reader=yao_text)
    assert farm_accordunit.actor_has_dueunit(bob_text, action_filter=True) == False
    assert farm_accordunit.actor_has_dueunit(yao_text, action_filter=True) == False

    # WHEN
    farm_accordunit.set_dueunit(get_cooking_dueunit(), bob_text)
    farm_accordunit.set_dueunit(get_speedboat_action_dueunit(), yao_text)
    farm_accordunit.set_dueunit(get_climate_dueunit(), yao_text)

    # THEN
    assert farm_accordunit.actor_has_dueunit(bob_text, action_filter=True) == False
    assert farm_accordunit.actor_has_dueunit(yao_text, action_filter=True)


def test_AccordUnit_set_accord_metrics_CorrectlySetsDue_relative_accord_weight():
    # GIVEN
    bob_text = "Bob"
    yao_text = "Yao"
    farm_accordunit = accordunit_shop(_author=bob_text, _reader=yao_text)
    s1_dueunit = farm_accordunit.add_dueunit()
    s1_dueunit.set_actor(bob_text)
    s1_dueunit.edit_attr(author_weight=4, reader_weight=1)
    s2_dueunit = farm_accordunit.add_dueunit()
    s2_dueunit.set_actor(bob_text)
    s2_dueunit.edit_attr(author_weight=6, reader_weight=3)
    assert s1_dueunit._relative_author_weight == 0
    assert s1_dueunit._relative_reader_weight == 0
    assert s2_dueunit._relative_author_weight == 0
    assert s2_dueunit._relative_reader_weight == 0

    # WHEN
    farm_accordunit.set_accord_metrics()

    # THEN
    assert s1_dueunit._relative_author_weight == 0.4
    assert s1_dueunit._relative_reader_weight == 0.25
    assert s2_dueunit._relative_author_weight == 0.6
    assert s2_dueunit._relative_reader_weight == 0.75
