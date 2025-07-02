from src.a00_data_toolbox.dict_toolbox import x_is_json
from src.a01_term_logic.rope import create_rope
from src.a06_owner_logic.test._util.a06_str import (
    concept_rope_str,
    fcontext_str,
    fnigh_str,
    fopen_str,
    owner_concept_factunit_str,
)
from src.a08_owner_atom_logic.atom import (
    get_from_json as owneratom_get_from_json,
    owneratom_shop,
)
from src.a08_owner_atom_logic.test._util.a08_str import (
    INSERT_str,
    crud_str,
    dimen_str,
    jkeys_str,
    jvalues_str,
)


def test_OwnerAtom_get_dict_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = owner_concept_factunit_str()
    knee_popen = 7
    knee_pnigh = 13
    insert_factunit_owneratom = owneratom_shop(x_dimen, INSERT_str())
    insert_factunit_owneratom.set_jkey(concept_rope_str(), ball_rope)
    insert_factunit_owneratom.set_jkey(fcontext_str(), knee_rope)
    insert_factunit_owneratom.set_jvalue(fopen_str(), knee_popen)
    insert_factunit_owneratom.set_jvalue(fnigh_str(), knee_pnigh)

    # WHEN
    atom_dict = insert_factunit_owneratom.get_dict()

    # THEN
    assert atom_dict == {
        dimen_str(): x_dimen,
        crud_str(): INSERT_str(),
        jkeys_str(): {concept_rope_str(): ball_rope, fcontext_str(): knee_rope},
        jvalues_str(): {fopen_str(): knee_popen, fnigh_str(): knee_pnigh},
    }


def test_OwnerAtom_get_json_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = owner_concept_factunit_str()
    knee_popen = 7
    knee_pnigh = 13
    insert_factunit_owneratom = owneratom_shop(x_dimen, INSERT_str())
    insert_factunit_owneratom.set_jkey(concept_rope_str(), ball_rope)
    insert_factunit_owneratom.set_jkey(fcontext_str(), knee_rope)
    insert_factunit_owneratom.set_jvalue(fopen_str(), knee_popen)
    insert_factunit_owneratom.set_jvalue(fnigh_str(), knee_pnigh)

    # WHEN
    atom_json = insert_factunit_owneratom.get_json()

    # THEN
    assert x_is_json(atom_json)


def test_owneratom_get_from_json_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = owner_concept_factunit_str()
    knee_popen = 7
    knee_pnigh = 13
    gen_owneratom = owneratom_shop(x_dimen, INSERT_str())
    gen_owneratom.set_jkey(concept_rope_str(), ball_rope)
    gen_owneratom.set_jkey(fcontext_str(), knee_rope)
    gen_owneratom.set_jvalue(fopen_str(), knee_popen)
    gen_owneratom.set_jvalue(fnigh_str(), knee_pnigh)
    atom_json = gen_owneratom.get_json()

    # WHEN
    json_owneratom = owneratom_get_from_json(atom_json)

    # THEN
    assert json_owneratom.dimen == gen_owneratom.dimen
    assert json_owneratom.crud_str == gen_owneratom.crud_str
    assert json_owneratom.jkeys == gen_owneratom.jkeys
    assert json_owneratom.jvalues == gen_owneratom.jvalues
    assert json_owneratom == gen_owneratom
