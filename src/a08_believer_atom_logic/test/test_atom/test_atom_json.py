from src.a00_data_toolbox.dict_toolbox import x_is_json
from src.a01_term_logic.rope import create_rope
from src.a06_believer_logic.test._util.a06_str import (
    believer_plan_factunit_str,
    f_context_str,
    f_lower_str,
    f_upper_str,
    plan_rope_str,
)
from src.a08_believer_atom_logic.atom import (
    believeratom_shop,
    get_from_json as believeratom_get_from_json,
)
from src.a08_believer_atom_logic.test._util.a08_str import (
    INSERT_str,
    crud_str,
    dimen_str,
    jkeys_str,
    jvalues_str,
)


def test_BelieverAtom_get_dict_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = believer_plan_factunit_str()
    knee_r_lower = 7
    knee_r_upper = 13
    insert_factunit_believeratom = believeratom_shop(x_dimen, INSERT_str())
    insert_factunit_believeratom.set_jkey(plan_rope_str(), ball_rope)
    insert_factunit_believeratom.set_jkey(f_context_str(), knee_rope)
    insert_factunit_believeratom.set_jvalue(f_lower_str(), knee_r_lower)
    insert_factunit_believeratom.set_jvalue(f_upper_str(), knee_r_upper)

    # WHEN
    atom_dict = insert_factunit_believeratom.get_dict()

    # THEN
    assert atom_dict == {
        dimen_str(): x_dimen,
        crud_str(): INSERT_str(),
        jkeys_str(): {plan_rope_str(): ball_rope, f_context_str(): knee_rope},
        jvalues_str(): {f_lower_str(): knee_r_lower, f_upper_str(): knee_r_upper},
    }


def test_BelieverAtom_get_json_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = believer_plan_factunit_str()
    knee_r_lower = 7
    knee_r_upper = 13
    insert_factunit_believeratom = believeratom_shop(x_dimen, INSERT_str())
    insert_factunit_believeratom.set_jkey(plan_rope_str(), ball_rope)
    insert_factunit_believeratom.set_jkey(f_context_str(), knee_rope)
    insert_factunit_believeratom.set_jvalue(f_lower_str(), knee_r_lower)
    insert_factunit_believeratom.set_jvalue(f_upper_str(), knee_r_upper)

    # WHEN
    atom_json = insert_factunit_believeratom.get_json()

    # THEN
    assert x_is_json(atom_json)


def test_believeratom_get_from_json_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = believer_plan_factunit_str()
    knee_r_lower = 7
    knee_r_upper = 13
    gen_believeratom = believeratom_shop(x_dimen, INSERT_str())
    gen_believeratom.set_jkey(plan_rope_str(), ball_rope)
    gen_believeratom.set_jkey(f_context_str(), knee_rope)
    gen_believeratom.set_jvalue(f_lower_str(), knee_r_lower)
    gen_believeratom.set_jvalue(f_upper_str(), knee_r_upper)
    atom_json = gen_believeratom.get_json()

    # WHEN
    json_believeratom = believeratom_get_from_json(atom_json)

    # THEN
    assert json_believeratom.dimen == gen_believeratom.dimen
    assert json_believeratom.crud_str == gen_believeratom.crud_str
    assert json_believeratom.jkeys == gen_believeratom.jkeys
    assert json_believeratom.jvalues == gen_believeratom.jvalues
    assert json_believeratom == gen_believeratom
