from src.bud.reason_idea import factunit_shop
from src.bud.lemma import Lemma, Lemmas, lemmas_shop
from src.bud.idea import ideaunit_shop
from src._road.road import get_default_real_id_roadnode as root_label, create_road


def test_lemma_attributes_exist():
    x_lemma = Lemma(src_fact=1, calc_fact=2, x_idea=3, eval_status=4, eval_count=5)
    assert x_lemma.src_fact == 1
    assert x_lemma.calc_fact == 2
    assert x_lemma.x_idea == 3
    assert x_lemma.eval_status == 4
    assert x_lemma.eval_count == 5


def test_lemmas_attributes_exist():
    # ESTABLISH / WHEN
    x_lemma = Lemmas

    # THEN
    assert x_lemma.lemmas is None


def test_lemmas_shop_CorrectReturnsObj():
    # WHEN
    x_lemma = lemmas_shop()

    # THEN
    assert x_lemma.lemmas == {}


def test_lemmas_create_new_fact_createsCorrectFact_scenario1():
    # ESTABLISH
    x_lemmas_x = lemmas_shop()

    # WHEN
    hist_road = create_road(root_label(), "histoory")
    idea_kid = ideaunit_shop("timerange1", _parent_road=hist_road, _begin=0, _close=12)
    src_idea = ideaunit_shop(
        "sub_timerange", _parent_road=hist_road, _begin=-13, _close=500
    )
    tr1 = create_road(idea_kid._parent_road, idea_kid._label)
    src_fact = factunit_shop(base=tr1, pick=tr1, open=0, nigh=30)
    new_fact = x_lemmas_x._create_new_fact(
        x_idea=idea_kid, src_fact=src_fact, src_idea=src_idea
    )

    # THEN
    assert new_fact.base == tr1
    assert new_fact.pick == tr1
    assert new_fact.open == 0
    assert new_fact.nigh == 12


def test_lemmas_create_new_fact_createsCorrectFact_scenario2():
    # ESTABLISH
    x_lemmas_x = lemmas_shop()

    # WHEN
    hist_road = create_road(root_label(), "histoory")
    idea_kid = ideaunit_shop("timerange1", _parent_road=hist_road, _begin=7, _close=12)
    tr1 = create_road(idea_kid._parent_road, idea_kid._label)
    src_fact = factunit_shop(base=tr1, pick=tr1, open=0, nigh=30)
    src_idea = ideaunit_shop(
        "sub_timerange", _parent_road=hist_road, _begin=-13, _close=500
    )
    new_fact = x_lemmas_x._create_new_fact(
        x_idea=idea_kid, src_fact=src_fact, src_idea=src_idea
    )

    # THEN
    assert new_fact.open == 7
    assert new_fact.nigh == 12


def test_lemmas_create_new_fact_createsCorrectFact_scenario3_denom():
    # ESTABLISH
    x_lemmas = lemmas_shop()

    # WHEN
    hist_road = create_road(root_label(), "histoory")
    idea_kid = ideaunit_shop(
        _label="timerange1",
        _parent_road=hist_road,
        _begin=0,
        _close=20,
        _numor=1,
        _denom=10,
        _reest=False,
    )
    tr1 = create_road(idea_kid._parent_road, idea_kid._label)
    src_fact = factunit_shop(base=tr1, pick=tr1, open=0, nigh=30)
    src_idea = ideaunit_shop(
        "sub_timerange", _parent_road=hist_road, _begin=-13, _close=500
    )
    new_fact = x_lemmas._create_new_fact(
        x_idea=idea_kid, src_fact=src_fact, src_idea=src_idea
    )

    # THEN
    assert new_fact.open == 0
    assert new_fact.nigh == 3


def test_lemmas_create_new_fact_createsCorrectFact_scenario3_2_denom():
    # ESTABLISH
    x_lemmas = lemmas_shop()

    # WHEN
    hist_road = create_road(root_label(), "histoory")
    ex_idea = ideaunit_shop("range_x", _parent_road=hist_road, _begin=0, _close=10080)
    idea_kid = ideaunit_shop(
        _label="timerange1",
        _parent_road=create_road(root_label(), "range_x"),
        _begin=7200,
        _close=8440,
        _reest=False,
    )
    ex_road = create_road(ex_idea._parent_road, ex_idea._label)
    ex_fact = factunit_shop(base=ex_road, pick=ex_road, open=7200, nigh=7200)
    new_fact = x_lemmas._create_new_fact(
        x_idea=idea_kid, src_fact=ex_fact, src_idea=ex_idea
    )

    # THEN
    assert new_fact.open == 7200
    assert new_fact.nigh == 7200


def test_lemmas_create_new_fact_createsCorrectFact_scenario4_denomReest():
    # ESTABLISH
    x_lemmas_x = lemmas_shop()

    # WHEN
    hist_road = create_road(root_label(), "histoory")
    idea_kid = ideaunit_shop(
        _label="timerange1",
        _parent_road=hist_road,
        _begin=0,
        _close=60,
        _numor=1,
        _denom=1,
        _reest=True,
    )
    tr1 = create_road(idea_kid._parent_road, idea_kid._label)
    src_fact = factunit_shop(base=tr1, pick=tr1, open=120, nigh=150)
    src_idea = ideaunit_shop(
        "sub_timerange", _parent_road=hist_road, _begin=-13, _close=500
    )
    new_fact = x_lemmas_x._create_new_fact(
        x_idea=idea_kid, src_fact=src_fact, src_idea=src_idea
    )

    # THEN
    assert new_fact.open == 0
    assert new_fact.nigh == 30


def test_lemmas_create_new_fact_createsCorrectFact_scenario5_denomReest():
    # ESTABLISH
    x_lemmas_x = lemmas_shop()

    # WHEN
    hist_road = create_road(root_label(), "histoory")
    idea_kid = ideaunit_shop(
        _label="timerange1",
        _parent_road=hist_road,
        _begin=0,
        _close=60,
        _numor=1,
        _denom=952,
        _reest=True,
    )
    tr1 = create_road(idea_kid._parent_road, idea_kid._label)
    src_fact = factunit_shop(base=tr1, pick=tr1, open=100, nigh=150)
    src_idea = ideaunit_shop(
        "sub_timerange", _parent_road=hist_road, _begin=-13, _close=500
    )
    new_fact = x_lemmas_x._create_new_fact(
        x_idea=idea_kid, src_fact=src_fact, src_idea=src_idea
    )

    # THEN
    assert new_fact.open == 40
    assert new_fact.nigh == 30


def test_lemmas_create_new_fact_createsCorrectFact_scenario6_denomReest():
    # ESTABLISH
    hist_road = create_road(root_label(), "histoory")
    x_lemmas_x = lemmas_shop()
    idea_src = ideaunit_shop(
        _label="timerange1",
        _parent_road=hist_road,
        _begin=0,
        _close=60,
    )

    # WHEN / THEN Check
    tr3_kid = ideaunit_shop(
        _label="subera",
        _parent_road=hist_road,
        _begin=40,
        _close=50,
    )
    tr3 = create_road(tr3_kid._parent_road, tr3_kid._label)
    src_fact = factunit_shop(base=tr3, pick=tr3, open=30, nigh=20)
    tr3_30_20_fact = x_lemmas_x._create_new_fact(
        x_idea=tr3_kid, src_fact=src_fact, src_idea=idea_src
    )
    assert tr3_30_20_fact.open == 40
    assert tr3_30_20_fact.nigh == 50

    # WHEN / THEN Check
    trb_kid = ideaunit_shop(
        _label="subera",
        _parent_road=hist_road,
        _begin=40,
        _close=60,
    )
    trb = create_road(trb_kid._parent_road, trb_kid._label)
    src_fact = factunit_shop(base=trb, pick=trb, open=30, nigh=20)
    trb_30_20_fact = x_lemmas_x._create_new_fact(
        x_idea=trb_kid, src_fact=src_fact, src_idea=idea_src
    )
    assert trb_30_20_fact.open == 40
    assert trb_30_20_fact.nigh == 60

    # WHEN / THEN Check
    tr4_kid = ideaunit_shop(
        _label="subera",
        _parent_road=hist_road,
        _begin=55,
        _close=10,
    )
    tr4 = create_road(tr4_kid._parent_road, tr4_kid._label)
    src_fact = factunit_shop(base=tr4, pick=tr4, open=30, nigh=20)
    tr4_30_20_fact = x_lemmas_x._create_new_fact(
        x_idea=tr4_kid, src_fact=src_fact, src_idea=idea_src
    )
    assert tr4_30_20_fact.open == 55
    assert tr4_30_20_fact.nigh == 10

    # WHEN / THEN Check
    tr5_kid = ideaunit_shop(
        _label="subera",
        _parent_road=hist_road,
        _begin=0,
        _close=60,
    )
    tr5 = create_road(tr5_kid._parent_road, tr5_kid._label)
    src_fact = factunit_shop(base=tr5, pick=tr5, open=30, nigh=20)
    tr5_0_60_fact = x_lemmas_x._create_new_fact(
        x_idea=tr5_kid, src_fact=src_fact, src_idea=idea_src
    )
    assert tr5_0_60_fact.open == 30
    assert tr5_0_60_fact.nigh == 20


def test_lemmas_create_new_fact_createsCorrectFact_scenario7_denomReest():
    # ESTABLISH
    x_lemmas_x = lemmas_shop()

    # WHEN
    hist_road = create_road(root_label(), "histoory")
    idea_kid = ideaunit_shop(
        _label="timerange1",
        _parent_road=hist_road,
        _begin=0,
        _close=60,
        _numor=1,
        _denom=1,
        _reest=True,
    )
    tr1 = create_road(idea_kid._parent_road, idea_kid._label)
    src_fact = factunit_shop(base=tr1, pick=tr1, open=90, nigh=150)
    src_idea = ideaunit_shop(
        "sub_timerange", _parent_road=hist_road, _begin=-13, _close=500
    )
    new_fact = x_lemmas_x._create_new_fact(
        x_idea=idea_kid, src_fact=src_fact, src_idea=src_idea
    )

    # THEN
    assert new_fact.open == 0
    assert new_fact.nigh == 60


def test_lemmas_get_unevaluated_lemma_ReturnsCorrectLemmaWhenEmpty():
    # ESTABLISH empty x_lemmas
    x_lemmas = lemmas_shop()

    # WHEN
    lem1x = x_lemmas.get_unevaluated_lemma()
    print(f"{lem1x=}")
    print(f"{x_lemmas.lemmas=}")

    # THEN
    assert x_lemmas.lemmas == {}
    assert lem1x is None


def test_lemmas_get_unevaluated_lemma_ReturnsCorrectLemmaWhenPopulated():
    # ESTABLISH 2 in x_lemmas
    hist_road = create_road(root_label(), "histoory")
    x_lemmas_x = lemmas_shop()
    x_lemmas_x.lemmas = {}
    src_idea = ideaunit_shop(
        "sub_timerange", _parent_road=hist_road, _begin=-13, _close=500
    )

    tr1_idea = ideaunit_shop("timerange1", _parent_road=hist_road, _begin=7, _close=12)
    tr1 = create_road(tr1_idea._parent_road, tr1_idea._label)
    src_fact = factunit_shop(base=tr1, pick=tr1, open=0, nigh=30)
    x_lemmas_x.eval(x_idea=tr1_idea, src_fact=src_fact, src_idea=src_idea)

    tr2_idea = ideaunit_shop("timerange2", _parent_road=hist_road, _begin=40, _close=60)
    tr2 = create_road(tr2_idea._parent_road, tr2_idea._label)
    src_fact = factunit_shop(base=tr2, pick=tr2, open=55, nigh=60)
    x_lemmas_x.eval(x_idea=tr2_idea, src_fact=src_fact, src_idea=src_idea)

    # WHEN
    lem1 = x_lemmas_x.get_unevaluated_lemma()
    print(f"{lem1.x_idea=}")
    print(f"{tr1=}")
    lem2 = x_lemmas_x.get_unevaluated_lemma()
    print(f"{lem2.x_idea=}")
    lem3 = x_lemmas_x.get_unevaluated_lemma()
    print(f"{lem3=}")

    # THEN
    assert lem1.x_idea in (tr1_idea, tr2_idea)
    assert lem2.x_idea in (tr1_idea, tr2_idea)
    assert lem3 is None

    x_lemmas_x = None


def test_lemmas_is_lemmas_incomplete_ReturnsCorrectBoolWhenPopulated():
    # ESTABLISH
    hist_road = create_road(root_label(), "histoory")
    z_lemmas = lemmas_shop()
    z_lemmas.lemmas = {}
    src_idea = ideaunit_shop(
        "sub_timerange", _parent_road=hist_road, _begin=-13, _close=500
    )

    # for x_lemma in z_lemmas.lemmas.values():
    #     print(f"Does not exist: {lemma.eval_status=} {lemma.calc_fact=}")

    tr1_idea = ideaunit_shop("timerange1", _parent_road=hist_road, _begin=7, _close=12)
    tr1_road = create_road(tr1_idea._parent_road, tr1_idea._label)
    src_fact = factunit_shop(base=tr1_road, pick=tr1_road, open=0, nigh=30)
    z_lemmas.eval(x_idea=tr1_idea, src_fact=src_fact, src_idea=src_idea)

    tr2_idea = ideaunit_shop("timerange2", _parent_road=hist_road, _begin=40, _close=60)
    tr2_road = create_road(tr2_idea._parent_road, tr2_idea._label)
    src_fact = factunit_shop(base=tr2_road, pick=tr2_road, open=55, nigh=60)
    z_lemmas.eval(x_idea=tr2_idea, src_fact=src_fact, src_idea=src_idea)

    # WHEN / THEN
    assert len(z_lemmas.lemmas) == 2
    tr1_lemma = z_lemmas.lemmas.get(tr1_road)
    tr2_lemma = z_lemmas.lemmas.get(tr2_road)
    tr1_src_fact = tr1_lemma.src_fact
    tr2_src_fact = tr2_lemma.src_fact
    print(f"0 transition: {tr1_src_fact.base=} {tr1_lemma.eval_status=}")
    print(f"0 transition: {tr2_src_fact.base=} {tr2_lemma.eval_status=}")
    assert z_lemmas.is_lemmas_evaluated() is False

    # WHEN
    lem1 = z_lemmas.get_unevaluated_lemma()
    # THEN
    assert len(z_lemmas.lemmas) == 2
    print(f"1 transition: {tr1_src_fact.base=} {tr1_lemma.eval_status=}")
    print(f"1 transition: {tr2_src_fact.base=} {tr2_lemma.eval_status=}")
    assert z_lemmas.is_lemmas_evaluated() is False

    # WHEN
    lem2 = z_lemmas.get_unevaluated_lemma()
    # THEN
    assert len(z_lemmas.lemmas) == 2
    print(f"2 transition: {tr1_src_fact.base=} {tr1_lemma.eval_status=}")
    print(f"2 transition: {tr2_src_fact.base=} {tr2_lemma.eval_status=}")
    assert z_lemmas.is_lemmas_evaluated() == True


def test_lemmas_is_lemmas_incomplete_ReturnsCorrectBoolWhenEmpty():
    # ESTABLISH
    z_lemmas = lemmas_shop()
    z_lemmas.lemmas = {}
    print(f"Does not exist: {z_lemmas=}")

    # WHEN / THEN
    assert not z_lemmas.lemmas
    assert z_lemmas.is_lemmas_evaluated() == True
