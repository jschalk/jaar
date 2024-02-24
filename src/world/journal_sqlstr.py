from src.agenda.atom import (
    get_atom_columns_build,
    atom_hx_table_name,
    atom_curr_table_name,
    AgendaAtom,
)
from src._road.road import RoadUnit
from src.instrument.sqlite import (
    sqlite_bool,
    sqlite_null,
    sqlite_text,
    sqlite_to_python,
)
from dataclasses import dataclass
from sqlite3 import Connection


def get_atom_hx_table_create_sqlstr() -> str:
    """Create table that hold atom_hx."""
    x_str = f"""
CREATE TABLE IF NOT EXISTS {atom_hx_table_name()} (
  person_id VARCHAR(255) NOT NULL"""

    for x_key, x_value in get_atom_columns_build().items():
        if x_value == "TEXT":
            x_value = "VARCHAR(255)"
        x_str = f"""{x_str}\n, {x_key} {x_value} NULL"""

    x_str = f"""{x_str}
)
;"""
    return x_str


def get_atom_hx_table_insert_sqlstr(x_atom: AgendaAtom) -> str:
    return x_atom.get_insert_sqlstr()


def get_atom_curr_table_create_sqlstr() -> str:
    """Create table that holds atom current."""
    x_str = f"""
CREATE TABLE IF NOT EXISTS {atom_curr_table_name()} (
  person_id VARCHAR(255) NOT NULL
, {atom_hx_table_name()}_row_id INT NOT NULL"""

    for x_key, x_value in get_atom_columns_build().items():
        if x_value == "TEXT":
            x_value = "VARCHAR(255)"
        x_str = f"""{x_str}\n, {x_key} {x_value} NULL"""

    x_str = f"""{x_str}
)
;"""
    return x_str


def get_atom_book_link_table_create_sqlstr() -> str:
    return """
CREATE TABLE atom_book_link
(
  atom_rowid INT NOT NULL
, book_rowid INT NOT NULL
, UNIQUE(atom_rowid, book_rowid)
, CONSTRAINT atom_fk FOREIGN KEY (atom_rowid) REFERENCES atom_curr (rowid)
, CONSTRAINT book_fk FOREIGN KEY (book_rowid) REFERENCES book_mstr (rowid)
)
;"""


def get_book_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS book_mstr (
  author_person_id VARCHAR(255) NOT NULL
, author_book_number INT NOT NULL
, UNIQUE(author_person_id, author_book_number)
)
;"""


def get_book_deal_link_table_create_sqlstr() -> str:
    return """
CREATE TABLE book_deal_link
(
  book_rowid INT NOT NULL
, deal_rowid INT NOT NULL
, UNIQUE(book_rowid, deal_rowid)
, CONSTRAINT atom_fk FOREIGN KEY (book_rowid) REFERENCES book_mstr (rowid)
, CONSTRAINT book_fk FOREIGN KEY (deal_rowid) REFERENCES deal_mstr (rowid)
)
;"""


def get_deal_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS deal_mstr (
  author_person_id VARCHAR(255) NOT NULL
, author_deal_number INT NOT NULL
, UNIQUE(author_person_id, author_deal_number)
)
;"""


def get_deal_person_link_table_create_sqlstr() -> str:
    return """
CREATE TABLE deal_person_link
(
  deal_rowid INT NOT NULL
, person_rowid INT NOT NULL
, UNIQUE(deal_rowid, person_rowid)
, CONSTRAINT book_fk FOREIGN KEY (deal_rowid) REFERENCES deal_mstr (rowid)
, CONSTRAINT person_fk FOREIGN KEY (person_rowid) REFERENCES person (rowid)
)
;"""


def get_road_ref_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS road_ref (
  road VARCHAR(255) NOT NULL
, delimiter VARCHAR(255) NOT NULL
, UNIQUE(road, delimiter)
)
;"""


def get_road_ref_table_single_insert_sqlstr(road: RoadUnit, delimiter: str) -> str:
    return f"""
INSERT OR IGNORE INTO road_ref (road, delimiter) 
VALUES (
  '{road}'
, '{delimiter}'
)
;"""


def get_road_ref_table_row_id_select_sqlstr(road: RoadUnit, delimiter: str) -> str:
    return f"""
SELECT rowid FROM road_ref  
WHERE road = '{road}' 
  AND delimiter = '{delimiter}'
)
;"""


def get_create_table_if_not_exist_sqlstrs() -> list[str]:
    list_x = [get_atom_hx_table_create_sqlstr()]
    list_x.append(get_atom_book_link_table_create_sqlstr())
    list_x.append(get_atom_curr_table_create_sqlstr())
    list_x.append(get_book_deal_link_table_create_sqlstr())
    list_x.append(get_book_table_create_sqlstr())
    list_x.append(get_deal_person_link_table_create_sqlstr())
    list_x.append(get_deal_table_create_sqlstr())
    list_x.append(get_road_ref_table_create_sqlstr())
    return list_x


# get_db_tables(treasury_conn: Connection) -> dict[str:int]:
# get_db_columns(treasury_conn: Connection) -> dict[str : dict[str:int]]: