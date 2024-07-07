from src.gift.atom_config import (
    get_flattened_atom_table_build,
    atom_hx_table_name,
    atom_mstr_table_name,
)
from src.gift.atom import AtomUnit
from src._road.road import RoadUnit

# from src._instrument.sqlite import (
#     sqlite_bool,
#     sqlite_null,
#     sqlite_text,
#     sqlite_to_python,
# )
# from dataclasses import dataclass
# from sqlite3 import Connection


def get_atom_hx_table_create_sqlstr() -> str:
    """Create table that hold atom_hx."""
    x_str = f"""
CREATE TABLE IF NOT EXISTS {atom_hx_table_name()} (
  owner_id VARCHAR(255) NOT NULL"""

    for x_key, x_value in get_flattened_atom_table_build().items():
        if x_value == "TEXT":
            x_value = "VARCHAR(255)"
        x_str = f"""{x_str}\n, {x_key} {x_value} NULL"""

    x_str = f"""{x_str}
)
;"""
    return x_str


def get_atom_hx_table_insert_sqlstr(x_atom: AtomUnit) -> str:
    return x_atom.get_insert_sqlstr()


def get_atom_mstr_table_create_sqlstr() -> str:
    """Create table that holds atomunits."""
    x_str = f"""
CREATE TABLE IF NOT EXISTS {atom_mstr_table_name()} (
  owner_id VARCHAR(255) NOT NULL
, {atom_hx_table_name()}_row_id INT NOT NULL"""

    for x_key, x_value in get_flattened_atom_table_build().items():
        if x_value == "TEXT":
            x_value = "VARCHAR(255)"
        x_str = f"""{x_str}\n, {x_key} {x_value} NULL"""

    x_str = f"""{x_str}
)
;"""
    return x_str


def get_atom_change_link_table_create_sqlstr() -> str:
    return """
CREATE TABLE atom_change_link
(
  atom_rowid INT NOT NULL
, change_rowid INT NOT NULL
, UNIQUE(atom_rowid, change_rowid)
, CONSTRAINT atom_fk FOREIGN KEY (atom_rowid) REFERENCES atom_mstr (rowid)
, CONSTRAINT change_fk FOREIGN KEY (change_rowid) REFERENCES change_mstr (rowid)
)
;"""


def get_change_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS change_mstr (
  author_owner_id VARCHAR(255) NOT NULL
, author_change_number INT NOT NULL
, UNIQUE(author_owner_id, author_change_number)
)
;"""


def get_change_gift_link_table_create_sqlstr() -> str:
    return """
CREATE TABLE change_gift_link
(
  change_rowid INT NOT NULL
, gift_rowid INT NOT NULL
, UNIQUE(change_rowid, gift_rowid)
, CONSTRAINT atom_fk FOREIGN KEY (change_rowid) REFERENCES change_mstr (rowid)
, CONSTRAINT change_fk FOREIGN KEY (gift_rowid) REFERENCES gift_mstr (rowid)
)
;"""


def get_gift_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS gift_mstr (
  author_owner_id VARCHAR(255) NOT NULL
, author_gift_number INT NOT NULL
, UNIQUE(author_owner_id, author_gift_number)
)
;"""


def get_gift_owner_link_table_create_sqlstr() -> str:
    return """
CREATE TABLE gift_owner_link
(
  gift_rowid INT NOT NULL
, owner_rowid INT NOT NULL
, UNIQUE(gift_rowid, owner_rowid)
, CONSTRAINT change_fk FOREIGN KEY (gift_rowid) REFERENCES gift_mstr (rowid)
, CONSTRAINT owner_fk FOREIGN KEY (owner_rowid) REFERENCES owner (rowid)
)
;"""


def get_owner_mstr_table_create_sqlstr() -> str:
    return """
CREATE TABLE owner_mstr
(
  owner_id VARCHAR(255) NOT NULL
, UNIQUE(owner_id)
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
    list_x.append(get_atom_mstr_table_create_sqlstr())
    list_x.append(get_atom_change_link_table_create_sqlstr())
    list_x.append(get_change_table_create_sqlstr())
    list_x.append(get_change_gift_link_table_create_sqlstr())
    list_x.append(get_gift_table_create_sqlstr())
    list_x.append(get_gift_owner_link_table_create_sqlstr())
    list_x.append(get_owner_mstr_table_create_sqlstr())
    list_x.append(get_road_ref_table_create_sqlstr())
    return list_x


# get_db_tables(treasury_conn: Connection) -> dict[str, int]:
# get_db_columns(treasury_conn: Connection) -> dict[str : dict[str, int]]:
