from src.f04_favor.atom_config import (
    get_flattened_atom_table_build,
    atom_hx_table_name,
    atom_mstr_table_name,
)
from src.f04_favor.atom import BudAtom
from src.f01_road.road import RoadUnit

# from src.f00_instrument.sqlite import (
#     sqlite_bool,
#     sqlite_null,
#     sqlite_str,
#     sqlite_to_python,
# )
# from dataclasses import dataclass
# from sqlite3 import Connection


def get_atom_hx_table_create_sqlstr() -> str:
    """Create table that hold atom_hx."""
    x_str = f"""
CREATE TABLE IF NOT EXISTS {atom_hx_table_name()} (
  owner_name VARCHAR(255) NOT NULL"""

    for x_key, x_value in get_flattened_atom_table_build().items():
        if x_value == "TEXT":
            x_value = "VARCHAR(255)"
        x_str = f"""{x_str}\n, {x_key} {x_value} NULL"""

    x_str = f"""{x_str}
)
;"""
    return x_str


def get_atom_hx_table_insert_sqlstr(x_atom: BudAtom) -> str:
    return x_atom.get_insert_sqlstr()


def get_atom_mstr_table_create_sqlstr() -> str:
    """Create table that holds budatoms."""
    x_str = f"""
CREATE TABLE IF NOT EXISTS {atom_mstr_table_name()} (
  owner_name VARCHAR(255) NOT NULL
, {atom_hx_table_name()}_row_id INT NOT NULL"""

    for x_key, x_value in get_flattened_atom_table_build().items():
        if x_value == "TEXT":
            x_value = "VARCHAR(255)"
        x_str = f"""{x_str}\n, {x_key} {x_value} NULL"""

    x_str = f"""{x_str}
)
;"""
    return x_str


def get_atom2delta_table_create_sqlstr() -> str:
    return """
CREATE TABLE atom2delta
(
  atom_rowid INT NOT NULL
, delta_rowid INT NOT NULL
, UNIQUE(atom_rowid, delta_rowid)
, CONSTRAINT atom_fk FOREIGN KEY (atom_rowid) REFERENCES atom_mstr (rowid)
, CONSTRAINT delta_fk FOREIGN KEY (delta_rowid) REFERENCES delta_mstr (rowid)
)
;"""


def get_delta_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS delta_mstr (
  author_owner_name VARCHAR(255) NOT NULL
, author_delta_number INT NOT NULL
, UNIQUE(author_owner_name, author_delta_number)
)
;"""


def get_delta2favor_table_create_sqlstr() -> str:
    return """
CREATE TABLE delta2favor
(
  delta_rowid INT NOT NULL
, favor_rowid INT NOT NULL
, UNIQUE(delta_rowid, favor_rowid)
, CONSTRAINT atom_fk FOREIGN KEY (delta_rowid) REFERENCES delta_mstr (rowid)
, CONSTRAINT delta_fk FOREIGN KEY (favor_rowid) REFERENCES favor_mstr (rowid)
)
;"""


def get_favor_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS favor_mstr (
  author_owner_name VARCHAR(255) NOT NULL
, author_favor_number INT NOT NULL
, UNIQUE(author_owner_name, author_favor_number)
)
;"""


def get_favor2owner_table_create_sqlstr() -> str:
    return """
CREATE TABLE favor2owner
(
  favor_rowid INT NOT NULL
, owner_rowid INT NOT NULL
, UNIQUE(favor_rowid, owner_rowid)
, CONSTRAINT delta_fk FOREIGN KEY (favor_rowid) REFERENCES favor_mstr (rowid)
, CONSTRAINT owner_fk FOREIGN KEY (owner_rowid) REFERENCES owner (rowid)
)
;"""


def get_owner_mstr_table_create_sqlstr() -> str:
    return """
CREATE TABLE owner_mstr
(
  owner_name VARCHAR(255) NOT NULL
, UNIQUE(owner_name)
)
;"""


def get_road_ref_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS road_ref (
  road VARCHAR(255) NOT NULL
, bridge VARCHAR(255) NOT NULL
, UNIQUE(road, bridge)
)
;"""


def get_road_ref_table_single_insert_sqlstr(road: RoadUnit, bridge: str) -> str:
    return f"""
INSERT OR IGNORE INTO road_ref (road, bridge) 
VALUES (
  '{road}'
, '{bridge}'
)
;"""


def get_road_ref_table_row_id_select_sqlstr(road: RoadUnit, bridge: str) -> str:
    return f"""
SELECT rowid FROM road_ref  
WHERE road = '{road}' 
  AND bridge = '{bridge}'
)
;"""


def get_create_table_if_not_exist_sqlstrs() -> list[str]:
    list_x = [get_atom_hx_table_create_sqlstr()]
    list_x.append(get_atom_mstr_table_create_sqlstr())
    list_x.append(get_atom2delta_table_create_sqlstr())
    list_x.append(get_delta_table_create_sqlstr())
    list_x.append(get_delta2favor_table_create_sqlstr())
    list_x.append(get_favor_table_create_sqlstr())
    list_x.append(get_favor2owner_table_create_sqlstr())
    list_x.append(get_owner_mstr_table_create_sqlstr())
    list_x.append(get_road_ref_table_create_sqlstr())
    return list_x


# get_db_tables(treasury_conn: Connection) -> dict[str, int]:
# get_db_columns(treasury_conn: Connection) -> dict[str : dict[str, int]]:
