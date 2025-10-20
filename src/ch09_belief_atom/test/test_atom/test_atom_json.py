from src.ch03_rope.rope import create_rope
from src.ch09_belief_atom.atom_main import beliefatom_shop, get_beliefatom_from_dict
from src.ref.keywords import Ch09Keywords as kw


def test_BeliefAtom_to_dict_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = kw.belief_plan_factunit
    knee_reason_lower = 7
    knee_reason_upper = 13
    insert_factunit_beliefatom = beliefatom_shop(x_dimen, kw.INSERT)
    insert_factunit_beliefatom.set_jkey(kw.plan_rope, ball_rope)
    insert_factunit_beliefatom.set_jkey(kw.fact_context, knee_rope)
    insert_factunit_beliefatom.set_jvalue(kw.fact_lower, knee_reason_lower)
    insert_factunit_beliefatom.set_jvalue(kw.fact_upper, knee_reason_upper)

    # WHEN
    atom_dict = insert_factunit_beliefatom.to_dict()

    # THEN
    assert atom_dict == {
        kw.dimen: x_dimen,
        kw.crud: kw.INSERT,
        kw.jkeys: {kw.plan_rope: ball_rope, kw.fact_context: knee_rope},
        kw.jvalues: {
            kw.fact_lower: knee_reason_lower,
            kw.fact_upper: knee_reason_upper,
        },
    }


def test_get_beliefatom_from_dict_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = kw.belief_plan_factunit
    knee_reason_lower = 7
    knee_reason_upper = 13
    gen_beliefatom = beliefatom_shop(x_dimen, kw.INSERT)
    gen_beliefatom.set_jkey(kw.plan_rope, ball_rope)
    gen_beliefatom.set_jkey(kw.fact_context, knee_rope)
    gen_beliefatom.set_jvalue(kw.fact_lower, knee_reason_lower)
    gen_beliefatom.set_jvalue(kw.fact_upper, knee_reason_upper)
    atom_serializable_dict = gen_beliefatom.to_dict()

    # WHEN
    gen_beliefatom = get_beliefatom_from_dict(atom_serializable_dict)

    # THEN
    assert gen_beliefatom.dimen == gen_beliefatom.dimen
    assert gen_beliefatom.crud_str == gen_beliefatom.crud_str
    assert gen_beliefatom.jkeys == gen_beliefatom.jkeys
    assert gen_beliefatom.jvalues == gen_beliefatom.jvalues
    assert gen_beliefatom == gen_beliefatom
