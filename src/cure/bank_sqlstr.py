from src.oath.oath import OathUnit, PartyUnit, Road
from src.oath.road import get_road_without_root_node
from src.cure.y_func import sqlite_bool, sqlite_null
from dataclasses import dataclass
from sqlite3 import Connection


def get_table_count_sqlstr(table_title: str) -> str:
    return f"SELECT COUNT(*) FROM {table_title}"


def get_river_flow_table_delete_sqlstr(currency_oath_healer: str) -> str:
    return f"""
        DELETE FROM river_flow
        WHERE currency_title = '{currency_oath_healer}' 
        ;
    """


def get_river_flow_table_create_sqlstr() -> str:
    return """
        CREATE TABLE IF NOT EXISTS river_flow (
          currency_title VARCHAR(255) NOT NULL
        , src_title VARCHAR(255) NOT NULL
        , dst_title VARCHAR(255) NOT NULL
        , currency_start FLOAT NOT NULL
        , currency_close FLOAT NOT NULL
        , flow_num INT NOT NULL
        , parent_flow_num INT NULL
        , river_tree_level INT NOT NULL
        , FOREIGN KEY(currency_title) REFERENCES oathunits(title)
        , FOREIGN KEY(src_title) REFERENCES oathunits(title)
        , FOREIGN KEY(dst_title) REFERENCES oathunits(title)
        )
        ;
    """


@dataclass
class RiverFlowUnit:
    currency_oath_healer: str
    src_title: str
    dst_title: str
    currency_start: float
    currency_close: float
    flow_num: int
    parent_flow_num: int
    river_tree_level: int

    def flow_returned(self) -> bool:
        return self.currency_oath_healer == self.dst_title


def get_river_flow_table_insert_sqlstr(
    river_flow_x: RiverFlowUnit,
) -> str:
    return f"""
        INSERT INTO river_flow (
          currency_title
        , src_title
        , dst_title
        , currency_start 
        , currency_close
        , flow_num
        , parent_flow_num
        , river_tree_level
        )
        VALUES (
          '{river_flow_x.currency_oath_healer}'
        , '{river_flow_x.src_title}'
        , '{river_flow_x.dst_title}'
        , {sqlite_null(river_flow_x.currency_start)}
        , {sqlite_null(river_flow_x.currency_close)}
        , {river_flow_x.flow_num}
        , {sqlite_null(river_flow_x.parent_flow_num)}
        , {river_flow_x.river_tree_level}
        )
        ;
    """


def get_river_flow_dict(
    db_conn: str, currency_oath_healer: str
) -> dict[str:RiverFlowUnit]:
    sqlstr = f"""
        SELECT 
          currency_title
        , src_title
        , dst_title
        , currency_start
        , currency_close
        , flow_num
        , parent_flow_num
        , river_tree_level
        FROM river_flow
        WHERE currency_title = '{currency_oath_healer}' 
        ;
    """
    dict_x = {}
    cursor_x = db_conn.cursor()
    results_cursor_x = cursor_x.execute(sqlstr)
    results_x = results_cursor_x.fetchall()

    for count_x, row in enumerate(results_x):
        river_flow_x = RiverFlowUnit(
            currency_oath_healer=row[0],
            src_title=row[1],
            dst_title=row[2],
            currency_start=row[3],
            currency_close=row[4],
            flow_num=row[5],
            parent_flow_num=row[6],
            river_tree_level=row[7],
        )
        dict_x[count_x] = river_flow_x
    return dict_x


def get_river_bucket_table_delete_sqlstr(currency_oath_healer: str) -> str:
    return f"""
        DELETE FROM river_bucket
        WHERE currency_title = '{currency_oath_healer}' 
        ;
    """


def get_river_bucket_table_create_sqlstr() -> str:
    return """
        CREATE TABLE IF NOT EXISTS river_bucket (
          currency_title VARCHAR(255) NOT NULL
        , dst_title VARCHAR(255) NOT NULL
        , bucket_num INT NOT NULL
        , curr_start FLOAT NOT NULL
        , curr_close FLOAT NOT NULL
        , FOREIGN KEY(currency_title) REFERENCES oathunits(title)
        , FOREIGN KEY(dst_title) REFERENCES oathunits(title)
        )
    ;
    """


def get_river_bucket_table_insert_sqlstr(currency_oath_healer: str) -> str:
    return f"""
        INSERT INTO river_bucket (
          currency_title
        , dst_title
        , bucket_num
        , curr_start
        , curr_close
        )
        SELECT 
          currency_title
        , dst_title
        , currency_bucket_num
        , min(currency_start) currency_bucket_start
        , max(currency_close) currency_bucket_close
        FROM  (
        SELECT *, SUM(step) OVER (ORDER BY currency_start) AS currency_bucket_num
        FROM  (
            SELECT 
            CASE 
            WHEN lag(currency_close) OVER (ORDER BY currency_start) < currency_start 
                OR lag(currency_close) OVER (ORDER BY currency_start) = NULL 
            THEN 1
            ELSE 0
            END AS step
            , *
            FROM  river_flow
            WHERE currency_title = '{currency_oath_healer}' and dst_title = currency_title 
            ) b
        ) c
        GROUP BY currency_title, dst_title, currency_bucket_num
        ORDER BY currency_bucket_start
        ;
    """


@dataclass
class RiverBucketUnit:
    currency_title: str
    dst_title: str
    bucket_num: int
    curr_start: float
    curr_close: float


def get_river_bucket_dict(
    db_conn: Connection, currency_oath_healer: str
) -> dict[str:RiverBucketUnit]:
    sqlstr = f"""
        SELECT
          currency_title
        , dst_title
        , bucket_num
        , curr_start
        , curr_close
        FROM river_bucket
        WHERE currency_title = '{currency_oath_healer}'
        ;
    """
    dict_x = {}
    results = db_conn.execute(sqlstr)

    for row in results.fetchall():
        river_bucket_x = RiverBucketUnit(
            currency_title=row[0],
            dst_title=row[1],
            bucket_num=row[2],
            curr_start=row[3],
            curr_close=row[4],
        )
        dict_x[river_bucket_x.bucket_num] = river_bucket_x
    return dict_x


def get_river_tparty_table_delete_sqlstr(currency_oath_healer: str) -> str:
    return f"""
        DELETE FROM river_tparty
        WHERE currency_title = '{currency_oath_healer}' 
        ;
    """


def get_river_tparty_table_create_sqlstr() -> str:
    return """
        CREATE TABLE IF NOT EXISTS river_tparty (
          currency_title VARCHAR(255) NOT NULL
        , tax_title VARCHAR(255) NOT NULL
        , tax_total FLOAT NOT NULL
        , debt FLOAT NULL
        , tax_diff FLOAT NULL
        , FOREIGN KEY(currency_title) REFERENCES oathunits(title)
        , FOREIGN KEY(tax_title) REFERENCES oathunits(title)
        )
    ;
    """


def get_river_tparty_table_insert_sqlstr(currency_oath_healer: str) -> str:
    return f"""
        INSERT INTO river_tparty (
          currency_title
        , tax_title
        , tax_total
        , debt
        , tax_diff
        )
        SELECT 
          rt.currency_title
        , rt.src_title
        , SUM(rt.currency_close-rt.currency_start) tax_paid
        , l._oath_agenda_ratio_debt
        , l._oath_agenda_ratio_debt - SUM(rt.currency_close-rt.currency_start)
        FROM river_flow rt
        LEFT JOIN ledger l ON l.oath_healer = rt.currency_title AND l.party_title = rt.src_title
        WHERE rt.currency_title='{currency_oath_healer}' and rt.dst_title=rt.currency_title
        GROUP BY rt.currency_title, rt.src_title
        ;
    """


@dataclass
class RiverTpartyUnit:
    currency_title: str
    tax_title: str
    tax_total: float
    debt: float
    tax_diff: float


def get_river_tparty_dict(
    db_conn: Connection, currency_oath_healer: str
) -> dict[str:RiverTpartyUnit]:
    sqlstr = f"""
        SELECT
          currency_title
        , tax_title
        , tax_total
        , debt
        , tax_diff
        FROM river_tparty
        WHERE currency_title = '{currency_oath_healer}'
        ;
    """
    dict_x = {}
    results = db_conn.execute(sqlstr)

    for row in results.fetchall():
        river_tparty_x = RiverTpartyUnit(
            currency_title=row[0],
            tax_title=row[1],
            tax_total=row[2],
            debt=row[3],
            tax_diff=row[4],
        )
        dict_x[river_tparty_x.tax_title] = river_tparty_x
    return dict_x


def get_oath_table_create_sqlstr() -> str:
    return """
        CREATE TABLE IF NOT EXISTS oathunits (
          title VARCHAR(255) PRIMARY KEY ASC
        , UNIQUE(title)
        )
    ;
    """


def get_oath_table_insert_sqlstr(oath_x: OathUnit) -> str:
    return f"""
        INSERT INTO oathunits (
            title
            )
        VALUES (
            '{oath_x._healer}' 
        )
        ;
        """


def get_ledger_table_create_sqlstr() -> str:
    return """
        CREATE TABLE IF NOT EXISTS ledger (
          oath_healer INTEGER 
        , party_title INTEGER
        , _oath_credit FLOAT
        , _oath_debt FLOAT
        , _oath_agenda_credit FLOAT
        , _oath_agenda_debt FLOAT
        , _oath_agenda_ratio_credit FLOAT
        , _oath_agenda_ratio_debt FLOAT
        , _creditor_active INT
        , _debtor_active INT
        , FOREIGN KEY(oath_healer) REFERENCES oathunits(title)
        , FOREIGN KEY(party_title) REFERENCES oathunits(title)
        , UNIQUE(oath_healer, party_title)
        )
    ;
    """


def get_ledger_table_insert_sqlstr(oath_x: OathUnit, partyunit_x: PartyUnit) -> str:
    return f"""
        INSERT INTO ledger (
              oath_healer
            , party_title
            , _oath_credit
            , _oath_debt
            , _oath_agenda_credit
            , _oath_agenda_debt
            , _oath_agenda_ratio_credit
            , _oath_agenda_ratio_debt
            , _creditor_active
            , _debtor_active
            )
        VALUES (
            '{oath_x._healer}' 
            , '{partyunit_x.title}'
            , {sqlite_null(partyunit_x._oath_credit)} 
            , {sqlite_null(partyunit_x._oath_debt)}
            , {sqlite_null(partyunit_x._oath_agenda_credit)}
            , {sqlite_null(partyunit_x._oath_agenda_debt)}
            , {sqlite_null(partyunit_x._oath_agenda_ratio_credit)}
            , {sqlite_null(partyunit_x._oath_agenda_ratio_debt)}
            , {sqlite_bool(partyunit_x._creditor_active)}
            , {sqlite_bool(partyunit_x._debtor_active)}
        )
        ;
        """


@dataclass
class LedgerUnit:
    oath_healer: str
    party_title: str
    _oath_credit: float
    _oath_debt: float
    _oath_agenda_credit: float
    _oath_agenda_debt: float
    _oath_agenda_ratio_credit: float
    _oath_agenda_ratio_debt: float
    _creditor_active: float
    _debtor_active: float


def get_ledger_dict(db_conn: Connection, payer_title: str) -> dict[str:LedgerUnit]:
    sqlstr = f"""
        SELECT 
          oath_healer
        , party_title
        , _oath_credit
        , _oath_debt
        , _oath_agenda_credit
        , _oath_agenda_debt
        , _oath_agenda_ratio_credit
        , _oath_agenda_ratio_debt
        , _creditor_active
        , _debtor_active
        FROM ledger
        WHERE oath_healer = '{payer_title}' 
        ;
    """
    dict_x = {}
    results = db_conn.execute(sqlstr)

    for row in results.fetchall():
        ledger_x = LedgerUnit(
            oath_healer=row[0],
            party_title=row[1],
            _oath_credit=row[2],
            _oath_debt=row[3],
            _oath_agenda_credit=row[4],
            _oath_agenda_debt=row[5],
            _oath_agenda_ratio_credit=row[6],
            _oath_agenda_ratio_debt=row[7],
            _creditor_active=row[8],
            _debtor_active=row[9],
        )
        dict_x[ledger_x.party_title] = ledger_x
    return dict_x


@dataclass
class RiverLedgerUnit:
    oath_healer: str
    currency_onset: float
    currency_cease: float
    _ledgers: dict[str:LedgerUnit]
    river_tree_level: int
    flow_num: int

    def get_range(self):
        return self.currency_cease - self.currency_onset


def get_river_ledger_unit(
    db_conn: Connection, river_flow_x: RiverFlowUnit = None
) -> RiverLedgerUnit:
    ledger_x = get_ledger_dict(db_conn, river_flow_x.dst_title)
    return RiverLedgerUnit(
        oath_healer=river_flow_x.dst_title,
        currency_onset=river_flow_x.currency_start,
        currency_cease=river_flow_x.currency_close,
        _ledgers=ledger_x,
        river_tree_level=river_flow_x.river_tree_level,
        flow_num=river_flow_x.flow_num,
    )


def get_idea_catalog_table_create_sqlstr() -> str:
    return """
        CREATE TABLE IF NOT EXISTS idea_catalog (
          oath_healer VARCHAR(255) NOT NULL
        , idea_road VARCHAR(1000) NOT NULL
        )
        ;
    """


def get_idea_catalog_table_count(db_conn: Connection, oath_healer: str) -> str:
    sqlstr = f"""
        {get_table_count_sqlstr("idea_catalog")} WHERE oath_healer = '{oath_healer}'
        ;
    """
    results = db_conn.execute(sqlstr)
    oath_row_count = 0
    for row in results.fetchall():
        oath_row_count = row[0]
    return oath_row_count


@dataclass
class IdeaCatalog:
    oath_healer: str
    idea_road: str


def get_idea_catalog_table_insert_sqlstr(
    idea_catalog: IdeaCatalog,
) -> str:
    # return f"""INSERT INTO idea_catalog (oath_healer, idea_road) VALUES ('{idea_catalog.oath_healer}', '{idea_catalog.idea_road}');"""
    return f"""
        INSERT INTO idea_catalog (
          oath_healer
        , idea_road
        )
        VALUES (
          '{idea_catalog.oath_healer}'
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
          oath_healer
        , idea_road
        FROM idea_catalog
        {where_clause}
        ;
    """
    results = db_conn.execute(sqlstr)

    dict_x = {}
    for row in results.fetchall():
        idea_catalog_x = IdeaCatalog(oath_healer=row[0], idea_road=row[1])
        dict_key = f"{idea_catalog_x.oath_healer} {idea_catalog_x.idea_road}"
        dict_x[dict_key] = idea_catalog_x
    return dict_x


def get_acptfact_catalog_table_create_sqlstr() -> str:
    return """
        CREATE TABLE IF NOT EXISTS acptfact_catalog (
          oath_healer VARCHAR(255) NOT NULL
        , base VARCHAR(1000) NOT NULL
        , pick VARCHAR(1000) NOT NULL
        )
        ;
    """


def get_acptfact_catalog_table_count(db_conn: Connection, oath_healer: str) -> str:
    sqlstr = f"""
        {get_table_count_sqlstr("acptfact_catalog")} WHERE oath_healer = '{oath_healer}'
        ;
    """
    results = db_conn.execute(sqlstr)
    oath_row_count = 0
    for row in results.fetchall():
        oath_row_count = row[0]
    return oath_row_count


@dataclass
class AcptFactCatalog:
    oath_healer: str
    base: str
    pick: str


def get_acptfact_catalog_table_insert_sqlstr(
    acptfact_catalog: AcptFactCatalog,
) -> str:
    return f"""
        INSERT INTO acptfact_catalog (
          oath_healer
        , base
        , pick
        )
        VALUES (
          '{acptfact_catalog.oath_healer}'
        , '{acptfact_catalog.base}'
        , '{acptfact_catalog.pick}'
        )
        ;
    """


def get_groupunit_catalog_table_create_sqlstr() -> str:
    return """
        CREATE TABLE IF NOT EXISTS groupunit_catalog (
          oath_healer VARCHAR(255) NOT NULL
        , groupunit_brand VARCHAR(1000) NOT NULL
        , partylinks_set_by_cure_road VARCHAR(1000) NULL
        )
        ;
    """


def get_groupunit_catalog_table_count(db_conn: Connection, oath_healer: str) -> str:
    sqlstr = f"""
        {get_table_count_sqlstr("groupunit_catalog")} WHERE oath_healer = '{oath_healer}'
        ;
    """
    results = db_conn.execute(sqlstr)
    oath_row_count = 0
    for row in results.fetchall():
        oath_row_count = row[0]
    return oath_row_count


@dataclass
class GroupUnitCatalog:
    oath_healer: str
    groupunit_brand: str
    partylinks_set_by_cure_road: str


def get_groupunit_catalog_table_insert_sqlstr(
    groupunit_catalog: GroupUnitCatalog,
) -> str:
    return f"""
        INSERT INTO groupunit_catalog (
          oath_healer
        , groupunit_brand
        , partylinks_set_by_cure_road
        )
        VALUES (
          '{groupunit_catalog.oath_healer}'
        , '{groupunit_catalog.groupunit_brand}'
        , '{groupunit_catalog.partylinks_set_by_cure_road}'
        )
        ;
    """


def get_groupunit_catalog_dict(db_conn: Connection) -> dict[str:GroupUnitCatalog]:
    sqlstr = """
        SELECT 
          oath_healer
        , groupunit_brand
        , partylinks_set_by_cure_road
        FROM groupunit_catalog
        ;
    """
    results = db_conn.execute(sqlstr)

    dict_x = {}
    for row in results.fetchall():
        groupunit_catalog_x = GroupUnitCatalog(
            oath_healer=row[0],
            groupunit_brand=row[1],
            partylinks_set_by_cure_road=row[2],
        )
        dict_key = (
            f"{groupunit_catalog_x.oath_healer} {groupunit_catalog_x.groupunit_brand}"
        )
        dict_x[dict_key] = groupunit_catalog_x
    return dict_x


def get_create_table_if_not_exist_sqlstrs() -> list[str]:
    list_x = [get_oath_table_create_sqlstr()]
    list_x.append(get_acptfact_catalog_table_create_sqlstr())
    list_x.append(get_idea_catalog_table_create_sqlstr())
    list_x.append(get_ledger_table_create_sqlstr())
    list_x.append(get_river_flow_table_create_sqlstr())
    list_x.append(get_river_bucket_table_create_sqlstr())
    list_x.append(get_river_tparty_table_create_sqlstr())
    list_x.append(get_groupunit_catalog_table_create_sqlstr())
    return list_x


def get_db_tables(bank_conn: Connection):
    sqlstr = "SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;"
    results = bank_conn.execute(sqlstr)

    return {row[0]: 1 for row in results}
