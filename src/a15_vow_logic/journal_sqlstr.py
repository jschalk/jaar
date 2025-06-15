from src.a01_term_logic.rope import RopeTerm
from src.a08_plan_atom_logic.atom import PlanAtom
from src.a08_plan_atom_logic.atom_config import get_flattened_atom_table_build


def get_atom_hx_table_create_sqlstr() -> str:
    """Create table that hold atom_hx."""
    x_str = """
CREATE TABLE IF NOT EXISTS atom_hx (
  owner_name VARCHAR(255) NOT NULL"""

    for x_key, x_value in get_flattened_atom_table_build().items():
        if x_value == "TEXT":
            x_value = "VARCHAR(255)"
        x_str = f"""{x_str}\n, {x_key} {x_value} NULL"""

    return f"""{x_str}
)
;"""


def get_atom_hx_table_insert_sqlstr(x_atom: PlanAtom) -> str:
    return x_atom.get_insert_sqlstr()


def get_atom_mstr_table_create_sqlstr() -> str:
    """Create table that holds planatoms."""
    x_str = """
CREATE TABLE IF NOT EXISTS atom_mstr (
  owner_name VARCHAR(255) NOT NULL
, atom_hx_row_id INT NOT NULL"""

    for x_key, x_value in get_flattened_atom_table_build().items():
        if x_value == "TEXT":
            x_value = "VARCHAR(255)"
        x_str = f"""{x_str}\n, {x_key} {x_value} NULL"""

    return f"""{x_str}
)
;"""


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


def get_delta2pack_table_create_sqlstr() -> str:
    return """
CREATE TABLE delta2pack
(
  delta_rowid INT NOT NULL
, pack_rowid INT NOT NULL
, UNIQUE(delta_rowid, pack_rowid)
, CONSTRAINT atom_fk FOREIGN KEY (delta_rowid) REFERENCES delta_mstr (rowid)
, CONSTRAINT delta_fk FOREIGN KEY (pack_rowid) REFERENCES pack_mstr (rowid)
)
;"""


def get_pack_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS pack_mstr (
  author_owner_name VARCHAR(255) NOT NULL
, author_pack_number INT NOT NULL
, UNIQUE(author_owner_name, author_pack_number)
)
;"""


def get_pack2owner_table_create_sqlstr() -> str:
    return """
CREATE TABLE pack2owner
(
  pack_rowid INT NOT NULL
, owner_rowid INT NOT NULL
, UNIQUE(pack_rowid, owner_rowid)
, CONSTRAINT delta_fk FOREIGN KEY (pack_rowid) REFERENCES pack_mstr (rowid)
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


def get_rope_ref_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS rope_ref (
  rope VARCHAR(255) NOT NULL
, knot VARCHAR(255) NOT NULL
, UNIQUE(rope, knot)
)
;"""


def get_rope_ref_table_single_insert_sqlstr(rope: RopeTerm, knot: str) -> str:
    return f"""
INSERT OR IGNORE INTO rope_ref (rope, knot) 
VALUES (
  '{rope}'
, '{knot}'
)
;"""


def get_rope_ref_table_row_id_select_sqlstr(rope: RopeTerm, knot: str) -> str:
    return f"""
SELECT rowid FROM rope_ref  
WHERE rope = '{rope}' 
  AND knot = '{knot}'
)
;"""


def get_create_table_if_not_exist_sqlstrs() -> list[str]:
    list_x = [get_atom_hx_table_create_sqlstr()]
    list_x.append(get_atom_mstr_table_create_sqlstr())
    list_x.append(get_atom2delta_table_create_sqlstr())
    list_x.append(get_delta_table_create_sqlstr())
    list_x.append(get_delta2pack_table_create_sqlstr())
    list_x.append(get_pack_table_create_sqlstr())
    list_x.append(get_pack2owner_table_create_sqlstr())
    list_x.append(get_owner_mstr_table_create_sqlstr())
    list_x.append(get_rope_ref_table_create_sqlstr())
    return list_x


# get_db_tables(treasury_conn: Connection) -> dict[str, int]:
# get_db_columns(treasury_conn: Connection) -> dict[str : dict[str, int]]:
