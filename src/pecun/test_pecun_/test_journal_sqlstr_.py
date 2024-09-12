from src._road.road import create_road
from src.bud.bud_tool import bud_idea_factunit_str
from src.gift.atom_config import fopen_str, atom_insert, atom_hx_table_name
from src.gift.atom import atomunit_shop
from src.pecun.journal_sqlstr import (
    get_atom2change_table_create_sqlstr,
    get_atom_hx_table_create_sqlstr,
    get_atom_hx_table_insert_sqlstr,
    get_atom_mstr_table_create_sqlstr,
    get_create_table_if_not_exist_sqlstrs,
    get_change2gift_table_create_sqlstr,
    get_change_table_create_sqlstr,
    get_gift_table_create_sqlstr,
    get_gift2owner_table_create_sqlstr,
    get_owner_mstr_table_create_sqlstr,
    get_road_ref_table_create_sqlstr,
    get_road_ref_table_single_insert_sqlstr,
    get_road_ref_table_row_id_select_sqlstr,
)


def test_get_change_table_create_sqlstr_ReturnsCorrectStr():
    # ESTABLISH / WHEN / THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS change_mstr (
  author_owner_id VARCHAR(255) NOT NULL
, author_change_number INT NOT NULL
, UNIQUE(author_owner_id, author_change_number)
)
;"""
    assert example_sqlstr == get_change_table_create_sqlstr()


def test_get_atom2change_table_create_sqlstr_ReturnsCorrectStr():
    # ESTABLISH / WHEN / THEN
    example_sqlstr = """
CREATE TABLE atom2change
(
  atom_rowid INT NOT NULL
, change_rowid INT NOT NULL
, UNIQUE(atom_rowid, change_rowid)
, CONSTRAINT atom_fk FOREIGN KEY (atom_rowid) REFERENCES atom_mstr (rowid)
, CONSTRAINT change_fk FOREIGN KEY (change_rowid) REFERENCES change_mstr (rowid)
)
;"""
    assert example_sqlstr == get_atom2change_table_create_sqlstr()


def test_get_gift_table_create_sqlstr_ReturnsCorrectStr():
    # ESTABLISH / WHEN / THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS gift_mstr (
  author_owner_id VARCHAR(255) NOT NULL
, author_gift_number INT NOT NULL
, UNIQUE(author_owner_id, author_gift_number)
)
;"""
    assert example_sqlstr == get_gift_table_create_sqlstr()


def test_get_change2gift_table_create_sqlstr_ReturnsCorrectStr():
    # ESTABLISH / WHEN / THEN
    example_sqlstr = """
CREATE TABLE change2gift
(
  change_rowid INT NOT NULL
, gift_rowid INT NOT NULL
, UNIQUE(change_rowid, gift_rowid)
, CONSTRAINT atom_fk FOREIGN KEY (change_rowid) REFERENCES change_mstr (rowid)
, CONSTRAINT change_fk FOREIGN KEY (gift_rowid) REFERENCES gift_mstr (rowid)
)
;"""
    assert example_sqlstr == get_change2gift_table_create_sqlstr()


def test_get_gift2owner_table_create_sqlstr_ReturnsCorrectStr():
    # ESTABLISH / WHEN / THEN
    example_sqlstr = """
CREATE TABLE gift2owner
(
  gift_rowid INT NOT NULL
, owner_rowid INT NOT NULL
, UNIQUE(gift_rowid, owner_rowid)
, CONSTRAINT change_fk FOREIGN KEY (gift_rowid) REFERENCES gift_mstr (rowid)
, CONSTRAINT owner_fk FOREIGN KEY (owner_rowid) REFERENCES owner (rowid)
)
;"""
    assert example_sqlstr == get_gift2owner_table_create_sqlstr()


def test_get_owner_mstr_table_create_sqlstr_ReturnsCorrectStr():
    # ESTABLISH / WHEN / THEN
    example_sqlstr = """
CREATE TABLE owner_mstr
(
  owner_id VARCHAR(255) NOT NULL
, UNIQUE(owner_id)
)
;"""
    assert example_sqlstr == get_owner_mstr_table_create_sqlstr()


def test_get_road_ref_table_create_sqlstr_ReturnsCorrectStr():
    # ESTABLISH / WHEN / THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS road_ref (
  road VARCHAR(255) NOT NULL
, delimiter VARCHAR(255) NOT NULL
, UNIQUE(road, delimiter)
)
;"""
    assert example_sqlstr == get_road_ref_table_create_sqlstr()


def test_get_road_ref_table_single_insert_sqlstr_ReturnsCorrectStr():
    # ESTABLISH
    music_str = "Music"
    slash_str = "/"
    texas_road = create_road(music_str, "texas", delimiter=slash_str)

    # WHEN
    generate_sqlstr = get_road_ref_table_single_insert_sqlstr(texas_road, slash_str)

    # THEN
    example_sqlstr = f"""
INSERT OR IGNORE INTO road_ref (road, delimiter) 
VALUES (
  '{texas_road}'
, '{slash_str}'
)
;"""
    assert example_sqlstr == generate_sqlstr


def test_get_road_ref_table_row_id_select_sqlstr_ReturnsCorrectStr():
    # ESTABLISH
    music_str = "Music"
    slash_str = "/"
    texas_road = create_road(music_str, "texas", delimiter=slash_str)

    # WHEN
    generate_sqlstr = get_road_ref_table_row_id_select_sqlstr(texas_road, slash_str)

    # THEN
    example_sqlstr = f"""
SELECT rowid FROM road_ref  
WHERE road = '{texas_road}' 
  AND delimiter = '{slash_str}'
)
;"""
    assert example_sqlstr == generate_sqlstr


def test_get_atom_hx_table_create_sqlstr_ReturnsCorrectStr():
    # ESTABLISH / WHEN
    generated_sqlstr = get_atom_hx_table_create_sqlstr()

    # THEN
    begin_sqlstr = """
CREATE TABLE IF NOT EXISTS atom_hx (
  owner_id VARCHAR(255) NOT NULL"""
    end_sqlstr = """)
;"""

    assert generated_sqlstr.find(begin_sqlstr) == 0
    assert generated_sqlstr.find(end_sqlstr) > 0
    example_idea_reasonunit_str = (
        "idea_reasonunit_UPDATE_base_idea_active_requisite INTEGER NULL"
    )
    assert generated_sqlstr.find(example_idea_reasonunit_str) > 0
    assert generated_sqlstr.find(example_idea_reasonunit_str) == 3423


def test_get_atom_hx_table_insert_sqlstr_ReturnsCorrectStr():
    # WHEN
    sports_str = "sports"
    sports_road = create_road("a", sports_str)
    ball_str = "basketball"
    ball_road = create_road(sports_road, ball_str)
    knee_str = "knee"
    knee_road = create_road("a", knee_str)
    knee_fopen = 7

    # WHEN
    x_category = bud_idea_factunit_str()
    road_str = "road"
    base_str = "base"
    update_disc_atomunit = atomunit_shop(x_category, atom_insert())
    update_disc_atomunit.set_required_arg(road_str, ball_road)
    update_disc_atomunit.set_required_arg(base_str, knee_road)
    update_disc_atomunit.set_optional_arg(fopen_str(), knee_fopen)

    # THEN
    example_sqlstr = f"""
INSERT INTO {atom_hx_table_name()} (
  {x_category}_{atom_insert()}_{road_str}
, {x_category}_{atom_insert()}_{base_str}
, {x_category}_{atom_insert()}_{fopen_str()}
)
VALUES (
  '{ball_road}'
, '{knee_road}'
, {knee_fopen}
)
;"""
    assert get_atom_hx_table_insert_sqlstr(update_disc_atomunit) == example_sqlstr


def test_get_atom_mstr_table_create_sqlstr_ReturnsCorrectStr():
    # ESTABLISH / WHEN
    generated_sqlstr = get_atom_mstr_table_create_sqlstr()

    # THEN
    begin_sqlstr = """
CREATE TABLE IF NOT EXISTS atom_mstr (
  owner_id VARCHAR(255) NOT NULL
, atom_hx_row_id INT NOT NULL"""
    end_sqlstr = """)
;"""
    assert generated_sqlstr.find(begin_sqlstr) == 0
    assert generated_sqlstr.find(end_sqlstr) > 0
    assert generated_sqlstr.find(end_sqlstr) == 5401
    example_idea_reasonunit_str = (
        "idea_reasonunit_UPDATE_base_idea_active_requisite INTEGER NULL"
    )
    assert generated_sqlstr.find(example_idea_reasonunit_str) > 0
    assert generated_sqlstr.find(example_idea_reasonunit_str) == 3455


def test_get_create_table_if_not_exist_sqlstrs_HasCorrectNumberOfNumber():
    # ESTABLISH / WHEN / THEN
    assert len(get_create_table_if_not_exist_sqlstrs()) == 9

    # SELECT name FROM my_db.sqlite_master WHERE type='table
