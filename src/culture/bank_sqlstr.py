from src.agenda.agenda import AgendaUnit, PartyUnit, Road, PersonName
from src.agenda.road import get_road_without_root_node
from src.culture.y_func import sqlite_bool, sqlite_null, sqlite_text, sqlite_to_python
from dataclasses import dataclass
from sqlite3 import Connection


def get_table_count_sqlstr(
    table_mame: str,
) -> (
    str
):  # "mame" is intially mispelled so that it does not interfere with person_name in the codebase
    return f"SELECT COUNT(*) FROM {table_mame}"


# river_block
def get_river_block_table_delete_sqlstr(currency_agenda_healer: str) -> str:
    return f"""
DELETE FROM river_block
WHERE currency_healer = '{currency_agenda_healer}' 
;
"""


def get_river_block_table_create_sqlstr() -> str:
    """Table that stores each block of currency from src_healer to dst_healer.
    currency_healer: every currency starts with a healer as credit source
        All river blocks with destination currency healer stop. For that currency range
        there is no more block
    src_healer: healer that is source of credit
    dst_healer: healer that is destination of credit.
    currency_start: range of currency affected start
    currency_close: range of currency affected close
    block_num: the sequence number of transactions before this one
    parent_block_num: river blocks can have multiple children but only one parent
    river_tree_level: how many ancestors between currency_healer first credit outblock
        and this river block
    JSchalk 24 Oct 2023
    """
    return """
CREATE TABLE IF NOT EXISTS river_block (
  currency_healer VARCHAR(255) NOT NULL
, src_healer VARCHAR(255) NOT NULL
, dst_healer VARCHAR(255) NOT NULL
, currency_start FLOAT NOT NULL
, currency_close FLOAT NOT NULL
, block_num INT NOT NULL
, parent_block_num INT NULL
, river_tree_level INT NOT NULL
, FOREIGN KEY(currency_healer) REFERENCES agendaunit(healer)
, FOREIGN KEY(src_healer) REFERENCES agendaunit(healer)
, FOREIGN KEY(dst_healer) REFERENCES agendaunit(healer)
)
;
"""


@dataclass
class RiverBlockUnit:
    currency_agenda_healer: str
    src_healer: str
    dst_healer: str
    currency_start: float
    currency_close: float
    block_num: int
    parent_block_num: int
    river_tree_level: int

    def block_returned(self) -> bool:
        return self.currency_agenda_healer == self.dst_healer


def get_river_block_table_insert_sqlstr(
    river_block_x: RiverBlockUnit,
) -> str:
    return f"""
INSERT INTO river_block (
  currency_healer
, src_healer
, dst_healer
, currency_start 
, currency_close
, block_num
, parent_block_num
, river_tree_level
)
VALUES (
  '{river_block_x.currency_agenda_healer}'
, '{river_block_x.src_healer}'
, '{river_block_x.dst_healer}'
, {sqlite_null(river_block_x.currency_start)}
, {sqlite_null(river_block_x.currency_close)}
, {river_block_x.block_num}
, {sqlite_null(river_block_x.parent_block_num)}
, {river_block_x.river_tree_level}
)
;
"""


def get_river_block_dict(
    db_conn: str, currency_agenda_healer: str
) -> dict[str:RiverBlockUnit]:
    sqlstr = f"""
SELECT 
  currency_healer
, src_healer
, dst_healer
, currency_start
, currency_close
, block_num
, parent_block_num
, river_tree_level
FROM river_block
WHERE currency_healer = '{currency_agenda_healer}' 
;
"""
    dict_x = {}
    cursor_x = db_conn.cursor()
    results_cursor_x = cursor_x.execute(sqlstr)
    results_x = results_cursor_x.fetchall()

    for count_x, row in enumerate(results_x):
        river_block_x = RiverBlockUnit(
            currency_agenda_healer=row[0],
            src_healer=row[1],
            dst_healer=row[2],
            currency_start=row[3],
            currency_close=row[4],
            block_num=row[5],
            parent_block_num=row[6],
            river_tree_level=row[7],
        )
        dict_x[count_x] = river_block_x
    return dict_x


# river_circle
def get_river_circle_table_delete_sqlstr(currency_agenda_healer: str) -> str:
    return f"""
DELETE FROM river_circle
WHERE currency_healer = '{currency_agenda_healer}' 
;
"""


def get_river_circle_table_create_sqlstr() -> str:
    """Check get_river_circle_table_insert_sqlstrget_river_circle_table_insert_sqlstr doc string"""
    return """
CREATE TABLE IF NOT EXISTS river_circle (
  currency_healer VARCHAR(255) NOT NULL
, dst_healer VARCHAR(255) NOT NULL
, circle_num INT NOT NULL
, curr_start FLOAT NOT NULL
, curr_close FLOAT NOT NULL
, FOREIGN KEY(currency_healer) REFERENCES agendaunit(healer)
, FOREIGN KEY(dst_healer) REFERENCES agendaunit(healer)
)
;
"""


def get_river_circle_table_insert_sqlstr(currency_agenda_healer: str) -> str:
    """Table that stores discontinuous currency ranges that circle back from source (currency_healer)
    to final destination (currency_healer)
    Columns
    currency_healer: every currency starts with a healer as credit source
    dst_healer: healer that is destination of credit.
        All river blocks with destination healer are summed into ranges called circles
    circle_num: all destination healer circles have a unique number. (sequential 0, 1, 2...)
    currency_start: range of circle start
    currency_close: range of circle close
    JSchalk 24 Oct 2023
    """
    return f"""
INSERT INTO river_circle (
  currency_healer
, dst_healer
, circle_num
, curr_start
, curr_close
)
SELECT 
  currency_healer
, dst_healer
, currency_circle_num
, min(currency_start) currency_circle_start
, max(currency_close) currency_circle_close
FROM  (
SELECT *, SUM(step) OVER (ORDER BY currency_start) AS currency_circle_num
FROM  (
    SELECT 
    CASE 
    WHEN lag(currency_close) OVER (ORDER BY currency_start) < currency_start 
        OR lag(currency_close) OVER (ORDER BY currency_start) = NULL 
    THEN 1
    ELSE 0
    END AS step
    , *
    FROM  river_block
    WHERE currency_healer = '{currency_agenda_healer}' and dst_healer = currency_healer 
    ) b
) c
GROUP BY currency_healer, dst_healer, currency_circle_num
ORDER BY currency_circle_start
;
"""


@dataclass
class RivercircleUnit:
    currency_healer: str
    dst_healer: str
    circle_num: int
    curr_start: float
    curr_close: float


def get_river_circle_dict(
    db_conn: Connection, currency_agenda_healer: str
) -> dict[str:RivercircleUnit]:
    sqlstr = f"""
SELECT
  currency_healer
, dst_healer
, circle_num
, curr_start
, curr_close
FROM river_circle
WHERE currency_healer = '{currency_agenda_healer}'
;
"""
    dict_x = {}
    results = db_conn.execute(sqlstr)

    for row in results.fetchall():
        river_circle_x = RivercircleUnit(
            currency_healer=row[0],
            dst_healer=row[1],
            circle_num=row[2],
            curr_start=row[3],
            curr_close=row[4],
        )
        dict_x[river_circle_x.circle_num] = river_circle_x
    return dict_x


# river tally
def get_river_tally_table_delete_sqlstr(currency_agenda_healer: str) -> str:
    return f"""
DELETE FROM river_tally
WHERE currency_healer = '{currency_agenda_healer}' 
;
"""


def get_river_tally_table_create_sqlstr() -> str:
    """Table that stores for sum of source healer's river circle currency ranges when
        the circle destination healer is the currency manager (currency_healer).
    currency_healer: every currency starts with a healer as credit source
    tax_healer: river circles source healer
        All river circles have destination healer == currency_healer
    tax_total: sum of all circle ranges. Between 0 and 1
    debt: the debt set by the currency manager's partyunit debt attributes
    tax_diff: how much debt the tax_healer is under or over sending to currency_healer
    JSchalk 24 Oct 2023
    """
    return """
CREATE TABLE IF NOT EXISTS river_tally (
  currency_healer VARCHAR(255) NOT NULL
, tax_healer VARCHAR(255) NOT NULL
, tax_total FLOAT NOT NULL
, debt FLOAT NULL
, tax_diff FLOAT NULL
, FOREIGN KEY(currency_healer) REFERENCES agendaunit(healer)
, FOREIGN KEY(tax_healer) REFERENCES agendaunit(healer)
)
;
"""


def get_river_tally_table_insert_sqlstr(currency_agenda_healer: str) -> str:
    return f"""
INSERT INTO river_tally (
  currency_healer
, tax_healer
, tax_total
, debt
, tax_diff
)
SELECT 
  rt.currency_healer
, rt.src_healer
, SUM(rt.currency_close-rt.currency_start) tax_paid
, l._agenda_goal_ratio_debt
, l._agenda_goal_ratio_debt - SUM(rt.currency_close-rt.currency_start)
FROM river_block rt
LEFT JOIN ledger l ON l.agenda_healer = rt.currency_healer AND l.party_title = rt.src_healer
WHERE rt.currency_healer='{currency_agenda_healer}' and rt.dst_healer=rt.currency_healer
GROUP BY rt.currency_healer, rt.src_healer
;
"""


@dataclass
class RiverTallyUnit:
    currency_healer: str
    tax_healer: str
    tax_total: float
    debt: float
    tax_diff: float
    credit_score: float
    voice_rank: int


def get_river_tally_dict(
    db_conn: Connection, currency_agenda_healer: str
) -> dict[str:RiverTallyUnit]:
    sqlstr = f"""
SELECT
  currency_healer
, tax_healer
, tax_total
, debt
, tax_diff
FROM river_tally
WHERE currency_healer = '{currency_agenda_healer}'
;
"""
    dict_x = {}
    results = db_conn.execute(sqlstr)

    for row in results.fetchall():
        river_tally_x = RiverTallyUnit(
            currency_healer=row[0],
            tax_healer=row[1],
            tax_total=row[2],
            debt=row[3],
            tax_diff=row[4],
            credit_score=None,
            voice_rank=None,
        )
        dict_x[river_tally_x.tax_healer] = river_tally_x
    return dict_x


# agenda
def get_agendaunit_table_create_sqlstr() -> str:
    """Create table that references the title of every agenda. The healer name of the one running that agenda's kitchen."""
    return """
CREATE TABLE IF NOT EXISTS agendaunit (
  healer VARCHAR(255) PRIMARY KEY ASC
, rational INT NULL
, UNIQUE(healer)
)
;
"""


def get_agendaunit_table_insert_sqlstr(x_agenda: AgendaUnit) -> str:
    return f"""
INSERT INTO agendaunit (
  healer
, rational
)
VALUES (
  '{x_agenda._healer}' 
, NULL
)
;
"""


def get_agendaunits_select_sqlstr():
    return """
SELECT 
  healer
, rational
FROM agendaunit
;
"""


@dataclass
class AgendaBankUnit:
    healer: PersonName
    rational: bool


def get_agendabankunits_dict(db_conn: Connection) -> dict[PersonName:AgendaBankUnit]:
    results = db_conn.execute(get_agendaunits_select_sqlstr())
    dict_x = {}
    for row in results.fetchall():
        x_agendabankunit = AgendaBankUnit(
            healer=row[0], rational=sqlite_to_python(row[1])
        )
        dict_x[x_agendabankunit.healer] = x_agendabankunit
    return dict_x


def get_agendaunit_update_sqlstr(agenda: AgendaUnit) -> str:
    return f"""
UPDATE agendaunit
SET rational = {sqlite_text(agenda._rational)}
WHERE healer = '{agenda._healer}'
;
"""


# ledger
def get_ledger_table_create_sqlstr() -> str:
    """Create table that holds the starting river metrics for every agenda's party. All the metrics."""
    return """
CREATE TABLE IF NOT EXISTS ledger (
  agenda_healer VARCHAR(255) NOT NULL 
, party_title VARCHAR(255) NOT NULL
, _agenda_credit FLOAT
, _agenda_debt FLOAT
, _agenda_goal_credit FLOAT
, _agenda_goal_debt FLOAT
, _agenda_goal_ratio_credit FLOAT
, _agenda_goal_ratio_debt FLOAT
, _creditor_active INT
, _debtor_active INT
, FOREIGN KEY(agenda_healer) REFERENCES agendaunit(healer)
, FOREIGN KEY(party_title) REFERENCES agendaunit(healer)
, UNIQUE(agenda_healer, party_title)
)
;
"""


def get_ledger_table_insert_sqlstr(x_agenda: AgendaUnit, partyunit_x: PartyUnit) -> str:
    """Create table that holds a the output credit metrics."""
    return f"""
INSERT INTO ledger (
  agenda_healer
, party_title
, _agenda_credit
, _agenda_debt
, _agenda_goal_credit
, _agenda_goal_debt
, _agenda_goal_ratio_credit
, _agenda_goal_ratio_debt
, _creditor_active
, _debtor_active
)
VALUES (
  '{x_agenda._healer}' 
, '{partyunit_x.title}'
, {sqlite_null(partyunit_x._agenda_credit)} 
, {sqlite_null(partyunit_x._agenda_debt)}
, {sqlite_null(partyunit_x._agenda_goal_credit)}
, {sqlite_null(partyunit_x._agenda_goal_debt)}
, {sqlite_null(partyunit_x._agenda_goal_ratio_credit)}
, {sqlite_null(partyunit_x._agenda_goal_ratio_debt)}
, {sqlite_bool(partyunit_x._creditor_active)}
, {sqlite_bool(partyunit_x._debtor_active)}
)
;
"""


@dataclass
class LedgerUnit:
    agenda_healer: str
    party_title: str
    _agenda_credit: float
    _agenda_debt: float
    _agenda_goal_credit: float
    _agenda_goal_debt: float
    _agenda_goal_ratio_credit: float
    _agenda_goal_ratio_debt: float
    _creditor_active: float
    _debtor_active: float


def get_ledger_dict(db_conn: Connection, payer_healer: str) -> dict[str:LedgerUnit]:
    sqlstr = f"""
SELECT 
  agenda_healer
, party_title
, _agenda_credit
, _agenda_debt
, _agenda_goal_credit
, _agenda_goal_debt
, _agenda_goal_ratio_credit
, _agenda_goal_ratio_debt
, _creditor_active
, _debtor_active
FROM ledger
WHERE agenda_healer = '{payer_healer}' 
;
"""
    dict_x = {}
    results = db_conn.execute(sqlstr)

    for row in results.fetchall():
        ledger_x = LedgerUnit(
            agenda_healer=row[0],
            party_title=row[1],
            _agenda_credit=row[2],
            _agenda_debt=row[3],
            _agenda_goal_credit=row[4],
            _agenda_goal_debt=row[5],
            _agenda_goal_ratio_credit=row[6],
            _agenda_goal_ratio_debt=row[7],
            _creditor_active=row[8],
            _debtor_active=row[9],
        )
        dict_x[ledger_x.party_title] = ledger_x
    return dict_x


@dataclass
class RiverLedgerUnit:
    agenda_healer: str
    currency_onset: float
    currency_cease: float
    _ledgers: dict[str:LedgerUnit]
    river_tree_level: int
    block_num: int

    def get_range(self):
        return self.currency_cease - self.currency_onset


def get_river_ledger_unit(
    db_conn: Connection, river_block_x: RiverBlockUnit = None
) -> RiverLedgerUnit:
    ledger_x = get_ledger_dict(db_conn, river_block_x.dst_healer)
    return RiverLedgerUnit(
        agenda_healer=river_block_x.dst_healer,
        currency_onset=river_block_x.currency_start,
        currency_cease=river_block_x.currency_close,
        _ledgers=ledger_x,
        river_tree_level=river_block_x.river_tree_level,
        block_num=river_block_x.block_num,
    )


# idea_catalog
def get_idea_catalog_table_create_sqlstr() -> str:
    """table that holds every road and its healer"""
    return """
CREATE TABLE IF NOT EXISTS idea_catalog (
  agenda_healer VARCHAR(255) NOT NULL
, idea_road VARCHAR(1000) NOT NULL
)
;
"""


def get_idea_catalog_table_count(db_conn: Connection, agenda_healer: str) -> str:
    sqlstr = f"""
{get_table_count_sqlstr("idea_catalog")} WHERE agenda_healer = '{agenda_healer}'
;
"""
    results = db_conn.execute(sqlstr)
    agenda_row_count = 0
    for row in results.fetchall():
        agenda_row_count = row[0]
    return agenda_row_count


@dataclass
class IdeaCatalog:
    agenda_healer: str
    idea_road: str


def get_idea_catalog_table_insert_sqlstr(
    idea_catalog: IdeaCatalog,
) -> str:
    # return f"""INSERT INTO idea_catalog (agenda_healer, idea_road) VALUES ('{idea_catalog.agenda_healer}', '{idea_catalog.idea_road}');"""
    return f"""
INSERT INTO idea_catalog (
  agenda_healer
, idea_road
)
VALUES (
  '{idea_catalog.agenda_healer}'
, '{get_road_without_root_node(idea_catalog.idea_road)}'
)
;
"""


def get_idea_catalog_dict(db_conn: Connection, search_road: Road = None):
    if search_road is None:
        where_clause = ""
    else:
        search_road_without_root_node = get_road_without_root_node(search_road)
        where_clause = f"WHERE idea_road = '{search_road_without_root_node}'"
    sqlstr = f"""
SELECT 
  agenda_healer
, idea_road
FROM idea_catalog
{where_clause}
;
"""
    results = db_conn.execute(sqlstr)

    dict_x = {}
    for row in results.fetchall():
        idea_catalog_x = IdeaCatalog(agenda_healer=row[0], idea_road=row[1])
        dict_key = f"{idea_catalog_x.agenda_healer} {idea_catalog_x.idea_road}"
        dict_x[dict_key] = idea_catalog_x
    return dict_x


# acptfact_catalog
def get_acptfact_catalog_table_create_sqlstr() -> str:
    """table that holds every accepted fact base and pick of every agenda. missing open/nigh. (clearly not used, maybe add in the future)"""
    return """
CREATE TABLE IF NOT EXISTS acptfact_catalog (
  agenda_healer VARCHAR(255) NOT NULL
, base VARCHAR(1000) NOT NULL
, pick VARCHAR(1000) NOT NULL
)
;
"""


def get_acptfact_catalog_table_count(db_conn: Connection, agenda_healer: str) -> str:
    sqlstr = f"""
{get_table_count_sqlstr("acptfact_catalog")} WHERE agenda_healer = '{agenda_healer}'
;
"""
    results = db_conn.execute(sqlstr)
    agenda_row_count = 0
    for row in results.fetchall():
        agenda_row_count = row[0]
    return agenda_row_count


@dataclass
class AcptFactCatalog:
    agenda_healer: str
    base: str
    pick: str


def get_acptfact_catalog_table_insert_sqlstr(
    acptfact_catalog: AcptFactCatalog,
) -> str:
    return f"""
INSERT INTO acptfact_catalog (
  agenda_healer
, base
, pick
)
VALUES (
  '{acptfact_catalog.agenda_healer}'
, '{acptfact_catalog.base}'
, '{acptfact_catalog.pick}'
)
;
"""


# groupunit_catalog
def get_groupunit_catalog_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS groupunit_catalog (
  agenda_healer VARCHAR(255) NOT NULL
, groupunit_brand VARCHAR(1000) NOT NULL
, partylinks_set_by_culture_road VARCHAR(1000) NULL
)
;
"""


def get_groupunit_catalog_table_count(db_conn: Connection, agenda_healer: str) -> str:
    sqlstr = f"""
{get_table_count_sqlstr("groupunit_catalog")} WHERE agenda_healer = '{agenda_healer}'
;
"""
    results = db_conn.execute(sqlstr)
    agenda_row_count = 0
    for row in results.fetchall():
        agenda_row_count = row[0]
    return agenda_row_count


@dataclass
class GroupUnitCatalog:
    agenda_healer: str
    groupunit_brand: str
    partylinks_set_by_culture_road: str


def get_groupunit_catalog_table_insert_sqlstr(
    groupunit_catalog: GroupUnitCatalog,
) -> str:
    return f"""
INSERT INTO groupunit_catalog (
  agenda_healer
, groupunit_brand
, partylinks_set_by_culture_road
)
VALUES (
  '{groupunit_catalog.agenda_healer}'
, '{groupunit_catalog.groupunit_brand}'
, '{groupunit_catalog.partylinks_set_by_culture_road}'
)
;
"""


def get_groupunit_catalog_dict(db_conn: Connection) -> dict[str:GroupUnitCatalog]:
    sqlstr = """
SELECT 
  agenda_healer
, groupunit_brand
, partylinks_set_by_culture_road
FROM groupunit_catalog
;
"""
    results = db_conn.execute(sqlstr)

    dict_x = {}
    for row in results.fetchall():
        groupunit_catalog_x = GroupUnitCatalog(
            agenda_healer=row[0],
            groupunit_brand=row[1],
            partylinks_set_by_culture_road=row[2],
        )
        dict_key = (
            f"{groupunit_catalog_x.agenda_healer} {groupunit_catalog_x.groupunit_brand}"
        )
        dict_x[dict_key] = groupunit_catalog_x
    return dict_x


def get_create_table_if_not_exist_sqlstrs() -> list[str]:
    list_x = [get_agendaunit_table_create_sqlstr()]
    list_x.append(get_acptfact_catalog_table_create_sqlstr())
    list_x.append(get_idea_catalog_table_create_sqlstr())
    list_x.append(get_ledger_table_create_sqlstr())
    list_x.append(get_river_block_table_create_sqlstr())
    list_x.append(get_river_circle_table_create_sqlstr())
    list_x.append(get_river_tally_table_create_sqlstr())
    list_x.append(get_groupunit_catalog_table_create_sqlstr())
    return list_x


def get_db_tables(bank_conn: Connection) -> dict[str:int]:
    sqlstr = "SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;"
    results = bank_conn.execute(sqlstr)

    return {row[0]: 1 for row in results}


def get_db_columns(bank_conn: Connection) -> dict[str : dict[str:int]]:
    table_names = get_db_tables(bank_conn)
    table_column_dict = {}
    for table_name in table_names.keys():
        sqlstr = f"SELECT name FROM PRAGMA_TABLE_INFO('{table_name}');"
        results = bank_conn.execute(sqlstr)
        table_column_dict[table_name] = {row[0]: 1 for row in results}

    return table_column_dict
