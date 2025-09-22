from src.ch00_data_toolbox.dict_toolbox import x_is_json
from src.ch02_rope_logic.rope import create_rope
from src.ch09_belief_atom_logic._ref.ch09_terms import (
    INSERT_str,
    belief_plan_factunit_str,
    crud_str,
    dimen_str,
    fact_context_str,
    fact_lower_str,
    fact_upper_str,
    jkeys_str,
    jvalues_str,
    plan_rope_str,
)
from src.ch09_belief_atom_logic.atom_main import (
    beliefatom_shop,
    get_from_json as beliefatom_get_from_json,
)


def test_BeliefAtom_to_dict_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = belief_plan_factunit_str()
    knee_reason_lower = 7
    knee_reason_upper = 13
    insert_factunit_beliefatom = beliefatom_shop(x_dimen, INSERT_str())
    insert_factunit_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    insert_factunit_beliefatom.set_jkey(fact_context_str(), knee_rope)
    insert_factunit_beliefatom.set_jvalue(fact_lower_str(), knee_reason_lower)
    insert_factunit_beliefatom.set_jvalue(fact_upper_str(), knee_reason_upper)

    # WHEN
    atom_dict = insert_factunit_beliefatom.to_dict()

    # THEN
    assert atom_dict == {
        dimen_str(): x_dimen,
        crud_str(): INSERT_str(),
        jkeys_str(): {plan_rope_str(): ball_rope, fact_context_str(): knee_rope},
        jvalues_str(): {
            fact_lower_str(): knee_reason_lower,
            fact_upper_str(): knee_reason_upper,
        },
    }


def test_BeliefAtom_get_json_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = belief_plan_factunit_str()
    knee_reason_lower = 7
    knee_reason_upper = 13
    insert_factunit_beliefatom = beliefatom_shop(x_dimen, INSERT_str())
    insert_factunit_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    insert_factunit_beliefatom.set_jkey(fact_context_str(), knee_rope)
    insert_factunit_beliefatom.set_jvalue(fact_lower_str(), knee_reason_lower)
    insert_factunit_beliefatom.set_jvalue(fact_upper_str(), knee_reason_upper)

    # WHEN
    atom_json = insert_factunit_beliefatom.get_json()

    # THEN
    assert x_is_json(atom_json)


def test_beliefatom_get_from_json_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = belief_plan_factunit_str()
    knee_reason_lower = 7
    knee_reason_upper = 13
    gen_beliefatom = beliefatom_shop(x_dimen, INSERT_str())
    gen_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    gen_beliefatom.set_jkey(fact_context_str(), knee_rope)
    gen_beliefatom.set_jvalue(fact_lower_str(), knee_reason_lower)
    gen_beliefatom.set_jvalue(fact_upper_str(), knee_reason_upper)
    atom_json = gen_beliefatom.get_json()

    # WHEN
    json_beliefatom = beliefatom_get_from_json(atom_json)

    # THEN
    assert json_beliefatom.dimen == gen_beliefatom.dimen
    assert json_beliefatom.crud_str == gen_beliefatom.crud_str
    assert json_beliefatom.jkeys == gen_beliefatom.jkeys
    assert json_beliefatom.jvalues == gen_beliefatom.jvalues
    assert json_beliefatom == gen_beliefatom
