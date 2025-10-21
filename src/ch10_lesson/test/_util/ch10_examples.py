from src.ch04_rope.rope import RopeTerm, create_rope, create_rope_from_labels
from src.ch09_belief_atom.atom_main import BeliefAtom, beliefatom_shop
from src.ch10_lesson._ref.ch10_semantic_types import LabelTerm, MomentLabel
from src.ch10_lesson.delta import BeliefDelta, beliefdelta_shop
from src.ch10_lesson.lesson_main import LessonUnit, lessonunit_shop
from src.ref.keywords import Ch10Keywords as kw


def get_ch10_example_moment_label() -> str:
    return "FizzBuzz2"


def get_texas_rope() -> RopeTerm:
    moment_label = get_ch10_example_moment_label()
    nation_str = "nation"
    usa_str = "USA"
    texas_str = "Texas"
    return create_rope_from_labels([moment_label, nation_str, usa_str, texas_str])


def get_atom_example_factunit_knee(first_label: LabelTerm = None) -> BeliefAtom:
    if not first_label:
        first_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(first_label, sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope(first_label, knee_str)
    knee_fact_lower = 7
    knee_fact_upper = 23
    x_dimen = kw.belief_plan_factunit
    insert_factunit_beliefatom = beliefatom_shop(x_dimen, kw.INSERT)
    insert_factunit_beliefatom.set_jkey(kw.plan_rope, ball_rope)
    insert_factunit_beliefatom.set_jkey(kw.fact_context, knee_rope)
    insert_factunit_beliefatom.set_jvalue(kw.fact_lower, knee_fact_lower)
    insert_factunit_beliefatom.set_jvalue(kw.fact_upper, knee_fact_upper)
    return insert_factunit_beliefatom


def get_atom_example_planunit_sports(moment_label: MomentLabel = None) -> BeliefAtom:
    if not moment_label:
        moment_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(moment_label, sports_str)
    insert_planunit_beliefatom = beliefatom_shop(kw.belief_planunit, kw.INSERT)
    insert_planunit_beliefatom.set_jkey(kw.plan_rope, sports_rope)
    return insert_planunit_beliefatom


def get_atom_example_planunit_ball(moment_label: MomentLabel = None) -> BeliefAtom:
    if not moment_label:
        moment_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(moment_label, sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    insert_planunit_beliefatom = beliefatom_shop(kw.belief_planunit, kw.INSERT)
    insert_planunit_beliefatom.set_jkey(kw.plan_rope, ball_rope)
    return insert_planunit_beliefatom


def get_atom_example_planunit_knee(moment_label: MomentLabel = None) -> BeliefAtom:
    if not moment_label:
        moment_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(moment_label, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    begin_str = "begin"
    close_str = "close"
    knee_rope = create_rope(sports_rope, knee_str)
    insert_planunit_beliefatom = beliefatom_shop(kw.belief_planunit, crud_str=kw.INSERT)
    insert_planunit_beliefatom.set_jkey(kw.plan_rope, knee_rope)
    insert_planunit_beliefatom.set_jvalue(begin_str, knee_begin)
    insert_planunit_beliefatom.set_jvalue(close_str, knee_close)
    return insert_planunit_beliefatom


def get_beliefdelta_sue_example() -> BeliefDelta:
    sue_beliefdelta = beliefdelta_shop()

    pool_beliefatom = beliefatom_shop(kw.beliefunit, kw.UPDATE)
    pool_attribute = kw.credor_respect
    pool_beliefatom.set_jvalue(pool_attribute, 77)
    sue_beliefdelta.set_beliefatom(pool_beliefatom)

    dimen = kw.belief_voiceunit
    sue_str = "Sue"
    sue_beliefatom = beliefatom_shop(dimen, kw.DELETE)
    sue_beliefatom.set_jkey(kw.voice_name, sue_str)
    sue_beliefdelta.set_beliefatom(sue_beliefatom)
    return sue_beliefdelta


def get_beliefdelta_example1() -> BeliefDelta:
    sue_beliefdelta = beliefdelta_shop()

    x_beliefatom = beliefatom_shop(kw.beliefunit, kw.UPDATE)
    x_beliefatom.set_jvalue(kw.tally, 55)
    x_beliefatom.set_jvalue(kw.max_tree_traverse, 66)
    x_beliefatom.set_jvalue(kw.credor_respect, 77)
    x_beliefatom.set_jvalue(kw.debtor_respect, 88)
    sue_beliefdelta.set_beliefatom(x_beliefatom)

    zia_str = "Zia"
    x_beliefatom = beliefatom_shop(dimen=kw.belief_voiceunit, crud_str=kw.DELETE)
    x_beliefatom.set_jkey(kw.voice_name, zia_str)
    sue_beliefdelta.set_beliefatom(x_beliefatom)
    return sue_beliefdelta


def get_sue_lessonunit() -> LessonUnit:
    return lessonunit_shop(belief_name="Sue", _lesson_id=37, face_name="Yao")


def sue_1beliefatoms_lessonunit() -> LessonUnit:
    x_lessonunit = lessonunit_shop(belief_name="Sue", _lesson_id=53, face_name="Yao")
    x_lessonunit._beliefdelta.set_beliefatom(get_atom_example_planunit_sports())
    return x_lessonunit


def sue_2beliefatoms_lessonunit() -> LessonUnit:
    x_lessonunit = lessonunit_shop(belief_name="Sue", _lesson_id=53, face_name="Yao")
    x_lessonunit._beliefdelta.set_beliefatom(get_atom_example_planunit_knee())
    x_lessonunit._beliefdelta.set_beliefatom(get_atom_example_planunit_sports())
    return x_lessonunit


def sue_3beliefatoms_lessonunit() -> LessonUnit:
    x_lessonunit = lessonunit_shop(belief_name="Sue", _lesson_id=37, face_name="Yao")
    x_lessonunit._beliefdelta.set_beliefatom(get_atom_example_factunit_knee())
    x_lessonunit._beliefdelta.set_beliefatom(get_atom_example_planunit_ball())
    x_lessonunit._beliefdelta.set_beliefatom(get_atom_example_planunit_knee())
    return x_lessonunit


def sue_4beliefatoms_lessonunit() -> LessonUnit:
    x_lessonunit = lessonunit_shop(belief_name="Sue", _lesson_id=47, face_name="Yao")
    x_lessonunit._beliefdelta.set_beliefatom(get_atom_example_factunit_knee())
    x_lessonunit._beliefdelta.set_beliefatom(get_atom_example_planunit_ball())
    x_lessonunit._beliefdelta.set_beliefatom(get_atom_example_planunit_knee())
    x_lessonunit._beliefdelta.set_beliefatom(get_atom_example_planunit_sports())
    return x_lessonunit
