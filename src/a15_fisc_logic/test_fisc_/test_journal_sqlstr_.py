from src.a01_term_logic.way import create_way
from src.a06_bud_logic._test_util.a06_str import (
    bud_concept_factunit_str,
    concept_way_str,
    fcontext_str,
    fopen_str,
)
from src.a08_bud_atom_logic._test_util.a08_str import INSERT_str, atom_hx_str
from src.a08_bud_atom_logic.atom import budatom_shop
from src.a15_fisc_logic.journal_sqlstr import (
    get_atom2delta_table_create_sqlstr,
    get_atom_hx_table_create_sqlstr,
    get_atom_hx_table_insert_sqlstr,
    get_atom_mstr_table_create_sqlstr,
    get_create_table_if_not_exist_sqlstrs,
    get_delta2pack_table_create_sqlstr,
    get_delta_table_create_sqlstr,
    get_owner_mstr_table_create_sqlstr,
    get_pack2owner_table_create_sqlstr,
    get_pack_table_create_sqlstr,
    get_way_ref_table_create_sqlstr,
    get_way_ref_table_row_id_select_sqlstr,
    get_way_ref_table_single_insert_sqlstr,
)


def test_get_delta_table_create_sqlstr_ReturnsCorrectStr():
    # ESTABLISH / WHEN / THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS delta_mstr (
  author_owner_name VARCHAR(255) NOT NULL
, author_delta_number INT NOT NULL
, UNIQUE(author_owner_name, author_delta_number)
)
;"""
    assert example_sqlstr == get_delta_table_create_sqlstr()


def test_get_atom2delta_table_create_sqlstr_ReturnsCorrectStr():
    # ESTABLISH / WHEN / THEN
    example_sqlstr = """
CREATE TABLE atom2delta
(
  atom_rowid INT NOT NULL
, delta_rowid INT NOT NULL
, UNIQUE(atom_rowid, delta_rowid)
, CONSTRAINT atom_fk FOREIGN KEY (atom_rowid) REFERENCES atom_mstr (rowid)
, CONSTRAINT delta_fk FOREIGN KEY (delta_rowid) REFERENCES delta_mstr (rowid)
)
;"""
    assert example_sqlstr == get_atom2delta_table_create_sqlstr()


def test_get_pack_table_create_sqlstr_ReturnsCorrectStr():
    # ESTABLISH / WHEN / THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS pack_mstr (
  author_owner_name VARCHAR(255) NOT NULL
, author_pack_number INT NOT NULL
, UNIQUE(author_owner_name, author_pack_number)
)
;"""
    assert example_sqlstr == get_pack_table_create_sqlstr()


def test_get_delta2pack_table_create_sqlstr_ReturnsCorrectStr():
    # ESTABLISH / WHEN / THEN
    example_sqlstr = """
CREATE TABLE delta2pack
(
  delta_rowid INT NOT NULL
, pack_rowid INT NOT NULL
, UNIQUE(delta_rowid, pack_rowid)
, CONSTRAINT atom_fk FOREIGN KEY (delta_rowid) REFERENCES delta_mstr (rowid)
, CONSTRAINT delta_fk FOREIGN KEY (pack_rowid) REFERENCES pack_mstr (rowid)
)
;"""
    assert example_sqlstr == get_delta2pack_table_create_sqlstr()


def test_get_pack2owner_table_create_sqlstr_ReturnsCorrectStr():
    # ESTABLISH / WHEN / THEN
    example_sqlstr = """
CREATE TABLE pack2owner
(
  pack_rowid INT NOT NULL
, owner_rowid INT NOT NULL
, UNIQUE(pack_rowid, owner_rowid)
, CONSTRAINT delta_fk FOREIGN KEY (pack_rowid) REFERENCES pack_mstr (rowid)
, CONSTRAINT owner_fk FOREIGN KEY (owner_rowid) REFERENCES owner (rowid)
)
;"""
    assert example_sqlstr == get_pack2owner_table_create_sqlstr()


def test_get_owner_mstr_table_create_sqlstr_ReturnsCorrectStr():
    # ESTABLISH / WHEN / THEN
    example_sqlstr = """
CREATE TABLE owner_mstr
(
  owner_name VARCHAR(255) NOT NULL
, UNIQUE(owner_name)
)
;"""
    assert example_sqlstr == get_owner_mstr_table_create_sqlstr()


def test_get_way_ref_table_create_sqlstr_ReturnsCorrectStr():
    # ESTABLISH / WHEN / THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS way_ref (
  way VARCHAR(255) NOT NULL
, bridge VARCHAR(255) NOT NULL
, UNIQUE(way, bridge)
)
;"""
    assert example_sqlstr == get_way_ref_table_create_sqlstr()


def test_get_way_ref_table_single_insert_sqlstr_ReturnsCorrectStr():
    # ESTABLISH
    accord45_str = "accord45"
    slash_str = "/"
    texas_way = create_way(accord45_str, "texas", bridge=slash_str)

    # WHEN
    generate_sqlstr = get_way_ref_table_single_insert_sqlstr(texas_way, slash_str)

    # THEN
    example_sqlstr = f"""
INSERT OR IGNORE INTO way_ref (way, bridge) 
VALUES (
  '{texas_way}'
, '{slash_str}'
)
;"""
    assert example_sqlstr == generate_sqlstr


def test_get_way_ref_table_row_id_select_sqlstr_ReturnsCorrectStr():
    # ESTABLISH
    accord45_str = "accord45"
    slash_str = "/"
    texas_way = create_way(accord45_str, "texas", bridge=slash_str)

    # WHEN
    generate_sqlstr = get_way_ref_table_row_id_select_sqlstr(texas_way, slash_str)

    # THEN
    example_sqlstr = f"""
SELECT rowid FROM way_ref  
WHERE way = '{texas_way}' 
  AND bridge = '{slash_str}'
)
;"""
    assert example_sqlstr == generate_sqlstr


def test_get_atom_hx_table_create_sqlstr_ReturnsCorrectStr():
    # ESTABLISH / WHEN
    generated_sqlstr = get_atom_hx_table_create_sqlstr()

    # THEN
    begin_sqlstr = """
CREATE TABLE IF NOT EXISTS atom_hx (
  owner_name VARCHAR(255) NOT NULL"""
    end_sqlstr = """)
;"""

    assert generated_sqlstr.find(begin_sqlstr) == 0
    assert generated_sqlstr.find(end_sqlstr) > 0
    example_concept_reasonunit_str = (
        "concept_reasonunit_UPDATE_rconcept_active_requisite INTEGER NULL"
    )
    assert generated_sqlstr.find(example_concept_reasonunit_str) > 0
    assert generated_sqlstr.find(example_concept_reasonunit_str) == 3949


def test_get_atom_hx_table_insert_sqlstr_ReturnsCorrectStr():
    # WHEN
    sports_str = "sports"
    sports_way = create_way("a", sports_str)
    ball_str = "basketball"
    ball_way = create_way(sports_way, ball_str)
    knee_str = "knee"
    knee_way = create_way("a", knee_str)
    knee_fopen = 7

    # WHEN
    x_dimen = bud_concept_factunit_str()
    update_disc_budatom = budatom_shop(x_dimen, INSERT_str())
    update_disc_budatom.set_jkey(concept_way_str(), ball_way)
    update_disc_budatom.set_jkey(fcontext_str(), knee_way)
    update_disc_budatom.set_jvalue(fopen_str(), knee_fopen)

    # THEN
    example_sqlstr = f"""
INSERT INTO {atom_hx_str()} (
  {x_dimen}_{INSERT_str()}_{concept_way_str()}
, {x_dimen}_{INSERT_str()}_{fcontext_str()}
, {x_dimen}_{INSERT_str()}_{fopen_str()}
)
VALUES (
  '{ball_way}'
, '{knee_way}'
, {knee_fopen}
)
;"""
    assert get_atom_hx_table_insert_sqlstr(update_disc_budatom) == example_sqlstr


def test_get_atom_mstr_table_create_sqlstr_ReturnsCorrectStr():
    # ESTABLISH / WHEN
    generated_sqlstr = get_atom_mstr_table_create_sqlstr()

    # THEN
    begin_sqlstr = """
CREATE TABLE IF NOT EXISTS atom_mstr (
  owner_name VARCHAR(255) NOT NULL
, atom_hx_row_id INT NOT NULL"""
    end_sqlstr = """)
;"""
    assert generated_sqlstr.find(begin_sqlstr) == 0
    assert generated_sqlstr.find(end_sqlstr) > 0
    assert generated_sqlstr.find(end_sqlstr) == 5614
    example_concept_reasonunit_str = (
        "concept_reasonunit_UPDATE_rconcept_active_requisite INTEGER NULL"
    )
    assert generated_sqlstr.find(example_concept_reasonunit_str) > 0
    assert generated_sqlstr.find(example_concept_reasonunit_str) == 3981


def test_get_create_table_if_not_exist_sqlstrs_HasCorrectNumberOfNumber():
    # ESTABLISH / WHEN / THEN
    assert len(get_create_table_if_not_exist_sqlstrs()) == 9

    # SELECT name FROM my_db.sqlite_master WHERE type='table
