from src.a00_data_toolbox.dict_toolbox import x_is_json
from src.a01_term_logic.rope import create_rope
from src.a06_plan_logic._util.a06_str import (
    concept_rope_str,
    fcontext_str,
    fnigh_str,
    fopen_str,
    plan_concept_factunit_str,
)
from src.a08_plan_atom_logic._util.a08_str import (
    INSERT_str,
    crud_str,
    dimen_str,
    jkeys_str,
    jvalues_str,
)
from src.a08_plan_atom_logic.atom import (
    get_from_json as planatom_get_from_json,
    planatom_shop,
)


def test_PlanAtom_get_dict_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = plan_concept_factunit_str()
    knee_popen = 7
    knee_pnigh = 13
    insert_factunit_planatom = planatom_shop(x_dimen, INSERT_str())
    insert_factunit_planatom.set_jkey(concept_rope_str(), ball_rope)
    insert_factunit_planatom.set_jkey(fcontext_str(), knee_rope)
    insert_factunit_planatom.set_jvalue(fopen_str(), knee_popen)
    insert_factunit_planatom.set_jvalue(fnigh_str(), knee_pnigh)

    # WHEN
    atom_dict = insert_factunit_planatom.get_dict()

    # THEN
    assert atom_dict == {
        dimen_str(): x_dimen,
        crud_str(): INSERT_str(),
        jkeys_str(): {concept_rope_str(): ball_rope, fcontext_str(): knee_rope},
        jvalues_str(): {fopen_str(): knee_popen, fnigh_str(): knee_pnigh},
    }


def test_PlanAtom_get_json_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = plan_concept_factunit_str()
    knee_popen = 7
    knee_pnigh = 13
    insert_factunit_planatom = planatom_shop(x_dimen, INSERT_str())
    insert_factunit_planatom.set_jkey(concept_rope_str(), ball_rope)
    insert_factunit_planatom.set_jkey(fcontext_str(), knee_rope)
    insert_factunit_planatom.set_jvalue(fopen_str(), knee_popen)
    insert_factunit_planatom.set_jvalue(fnigh_str(), knee_pnigh)

    # WHEN
    atom_json = insert_factunit_planatom.get_json()

    # THEN
    assert x_is_json(atom_json)


def test_planatom_get_from_json_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = plan_concept_factunit_str()
    knee_popen = 7
    knee_pnigh = 13
    gen_planatom = planatom_shop(x_dimen, INSERT_str())
    gen_planatom.set_jkey(concept_rope_str(), ball_rope)
    gen_planatom.set_jkey(fcontext_str(), knee_rope)
    gen_planatom.set_jvalue(fopen_str(), knee_popen)
    gen_planatom.set_jvalue(fnigh_str(), knee_pnigh)
    atom_json = gen_planatom.get_json()

    # WHEN
    json_planatom = planatom_get_from_json(atom_json)

    # THEN
    assert json_planatom.dimen == gen_planatom.dimen
    assert json_planatom.crud_str == gen_planatom.crud_str
    assert json_planatom.jkeys == gen_planatom.jkeys
    assert json_planatom.jvalues == gen_planatom.jvalues
    assert json_planatom == gen_planatom
