from src.a00_data_toolbox.dict_toolbox import x_is_json
from src.a01_way_logic.way import create_way
from src.a06_bud_logic._test_util.a06_str import bud_concept_factunit_str
from src.a06_bud_logic._test_util.a06_str import (
    concept_way_str,
    fcontext_str,
    fopen_str,
    fnigh_str,
)
from src.a08_bud_atom_logic._test_util.a08_str import (
    jkeys_str,
    jvalues_str,
    dimen_str,
    crud_str,
)
from src.a08_bud_atom_logic.atom import (
    budatom_shop,
    atom_insert,
    get_from_json as budatom_get_from_json,
)


def test_BudAtom_get_dict_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_way = create_way("a", sports_str)
    ball_str = "basketball"
    ball_way = create_way(sports_way, ball_str)
    knee_str = "knee"
    knee_way = create_way("a", knee_str)
    x_dimen = bud_concept_factunit_str()
    knee_popen = 7
    knee_pnigh = 13
    insert_factunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_factunit_budatom.set_jkey(concept_way_str(), ball_way)
    insert_factunit_budatom.set_jkey(fcontext_str(), knee_way)
    insert_factunit_budatom.set_jvalue(fopen_str(), knee_popen)
    insert_factunit_budatom.set_jvalue(fnigh_str(), knee_pnigh)

    # WHEN
    atom_dict = insert_factunit_budatom.get_dict()

    # THEN
    assert atom_dict == {
        dimen_str(): x_dimen,
        crud_str(): atom_insert(),
        jkeys_str(): {concept_way_str(): ball_way, fcontext_str(): knee_way},
        jvalues_str(): {fopen_str(): knee_popen, fnigh_str(): knee_pnigh},
    }


def test_BudAtom_get_json_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_way = create_way("a", sports_str)
    ball_str = "basketball"
    ball_way = create_way(sports_way, ball_str)
    knee_str = "knee"
    knee_way = create_way("a", knee_str)
    x_dimen = bud_concept_factunit_str()
    knee_popen = 7
    knee_pnigh = 13
    insert_factunit_budatom = budatom_shop(x_dimen, atom_insert())
    insert_factunit_budatom.set_jkey(concept_way_str(), ball_way)
    insert_factunit_budatom.set_jkey(fcontext_str(), knee_way)
    insert_factunit_budatom.set_jvalue(fopen_str(), knee_popen)
    insert_factunit_budatom.set_jvalue(fnigh_str(), knee_pnigh)

    # WHEN
    atom_json = insert_factunit_budatom.get_json()

    # THEN
    assert x_is_json(atom_json)


def test_budatom_get_from_json_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_way = create_way("a", sports_str)
    ball_str = "basketball"
    ball_way = create_way(sports_way, ball_str)
    knee_str = "knee"
    knee_way = create_way("a", knee_str)
    x_dimen = bud_concept_factunit_str()
    knee_popen = 7
    knee_pnigh = 13
    gen_budatom = budatom_shop(x_dimen, atom_insert())
    gen_budatom.set_jkey(concept_way_str(), ball_way)
    gen_budatom.set_jkey(fcontext_str(), knee_way)
    gen_budatom.set_jvalue(fopen_str(), knee_popen)
    gen_budatom.set_jvalue(fnigh_str(), knee_pnigh)
    atom_json = gen_budatom.get_json()

    # WHEN
    json_budatom = budatom_get_from_json(atom_json)

    # THEN
    assert json_budatom.dimen == gen_budatom.dimen
    assert json_budatom.crud_str == gen_budatom.crud_str
    assert json_budatom.jkeys == gen_budatom.jkeys
    assert json_budatom.jvalues == gen_budatom.jvalues
    assert json_budatom == gen_budatom
