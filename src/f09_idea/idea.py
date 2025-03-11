from src.f00_instrument.file import open_file
from src.f00_instrument.dict_toolbox import (
    extract_csv_headers,
    get_csv_column1_column2_metrics,
    create_l2nested_csv_dict,
    get_positional_dict,
    add_headers_to_csv,
    get_empty_str_if_None as if_none_str,
)
from src.f01_road.road import FiscTitle, OwnerName, FaceName
from src.f02_bud.bud import BudUnit
from src.f03_chrono.chrono import timelineunit_shop
from src.f04_gift.atom import atom_insert, atom_delete, AtomUnit, atomrow_shop
from src.f04_gift.delta import buddelta_shop, get_dimens_cruds_buddelta, BudDelta
from src.f04_gift.gift import giftunit_shop, GiftUnit
from src.f05_listen.hubunit import hubunit_shop
from src.f07_fisc.fisc import fiscunit_shop, FiscUnit
from src.f08_pidgin.pidgin import PidginUnit
from src.f09_idea.idea_config import (
    get_idearef_from_file,
    get_idea_format_headers,
    get_idea_config_dict,
    get_idea_format_filename,
    get_idea_format_headers,
)
from src.f09_idea.idea_db_tool import (
    save_dataframe_to_csv,
    get_custom_sorted_list,
    if_nan_return_None,
)
from pandas import DataFrame
from csv import reader as csv_reader
from dataclasses import dataclass


@dataclass
class IdeaRef:
    idea_name: str = None
    dimens: str = None
    _attributes: dict[str, dict[str, bool]] = None

    def set_attribute(self, x_attribute: str, otx_key: bool):
        self._attributes[x_attribute] = {"otx_key": otx_key}

    def get_headers_list(self) -> list[str]:
        return get_custom_sorted_list(self._attributes)

    def get_otx_keys_list(self) -> list[str]:
        x_set = {
            x_attr
            for x_attr, otx_dict in self._attributes.items()
            if otx_dict.get("otx_key") is True
        }
        return get_custom_sorted_list(x_set)

    def get_otx_values_list(self) -> list[str]:
        x_set = {
            x_attr
            for x_attr, otx_dict in self._attributes.items()
            if otx_dict.get("otx_key") is False
        }
        return get_custom_sorted_list(x_set)


def idearef_shop(x_idea_name: str, x_dimens: list[str]) -> IdeaRef:
    return IdeaRef(idea_name=x_idea_name, dimens=x_dimens, _attributes={})


def get_idearef_obj(idea_name: str) -> IdeaRef:
    idearef_dict = get_idearef_from_file(idea_name)
    x_idearef = idearef_shop(idea_name, idearef_dict.get("dimens"))
    x_idearef._attributes = idearef_dict.get("attributes")
    return x_idearef


def get_ascending_bools(sorting_attributes: list[str]) -> list[bool]:
    return [True for _ in sorting_attributes]


def _get_headers_list(idea_name: str) -> list[str]:
    return get_idearef_obj(idea_name).get_headers_list()


def _generate_idea_dataframe(d2_list: list[list[str]], idea_name: str) -> DataFrame:
    return DataFrame(d2_list, columns=_get_headers_list(idea_name))


def create_idea_df(x_budunit: BudUnit, idea_name: str) -> DataFrame:
    x_buddelta = buddelta_shop()
    x_buddelta.add_all_atomunits(x_budunit)
    x_idearef = get_idearef_obj(idea_name)
    x_fisc_title = x_budunit.fisc_title
    x_owner_name = x_budunit.owner_name
    sorted_atomunits = _get_sorted_atom_insert_atomunits(x_buddelta, x_idearef)
    d2_list = _create_d2_list(sorted_atomunits, x_idearef, x_fisc_title, x_owner_name)
    d2_list = _delta_all_pledge_values(d2_list, x_idearef)
    x_idea = _generate_idea_dataframe(d2_list, idea_name)
    sorting_columns = x_idearef.get_headers_list()
    return _sort_dataframe(x_idea, sorting_columns)


def _get_sorted_atom_insert_atomunits(
    x_buddelta: BudDelta, x_idearef: IdeaRef
) -> list[AtomUnit]:
    dimen_set = set(x_idearef.dimens)
    curd_set = {atom_insert()}
    limited_delta = get_dimens_cruds_buddelta(x_buddelta, dimen_set, curd_set)
    return limited_delta.get_dimen_sorted_atomunits_list()


def _create_d2_list(
    sorted_atomunits: list[AtomUnit],
    x_idearef: IdeaRef,
    x_fisc_title: FiscTitle,
    x_owner_name: OwnerName,
):
    d2_list = []
    for x_atomunit in sorted_atomunits:
        d1_list = []
        for x_attribute in x_idearef.get_headers_list():
            if x_attribute == "fisc_title":
                d1_list.append(x_fisc_title)
            elif x_attribute == "owner_name":
                d1_list.append(x_owner_name)
            else:
                d1_list.append(x_atomunit.get_value(x_attribute))
        d2_list.append(d1_list)
    return d2_list


def _delta_all_pledge_values(d2_list: list[list], x_idearef: IdeaRef) -> list[list]:
    if "pledge" in x_idearef._attributes:
        for x_count, x_header in enumerate(x_idearef.get_headers_list()):
            if x_header == "pledge":
                pledge_column_number = x_count
        for x_row in d2_list:
            if x_row[pledge_column_number] is True:
                x_row[pledge_column_number] = "Yes"
            else:
                x_row[pledge_column_number] = ""
    return d2_list


def _sort_dataframe(x_idea: DataFrame, sorting_columns: list[str]) -> DataFrame:
    ascending_bools = get_ascending_bools(sorting_columns)
    x_idea.sort_values(sorting_columns, ascending=ascending_bools, inplace=True)
    x_idea.reset_index(inplace=True)
    x_idea.drop(columns=["index"], inplace=True)
    return x_idea


def save_idea_csv(x_ideaname: str, x_budunit: BudUnit, x_dir: str, x_filename: str):
    x_dataframe = create_idea_df(x_budunit, x_ideaname)
    save_dataframe_to_csv(x_dataframe, x_dir, x_filename)


def get_csv_idearef(header_row: list[str]) -> IdeaRef:
    header_row = get_custom_sorted_list(header_row)
    headers_str = "".join(f",{x_header}" for x_header in header_row)
    headers_str = headers_str[1:]
    headers_str = headers_str.replace("face_name,", "")
    headers_str = headers_str.replace("event_int,", "")
    x_ideaname = get_idea_format_headers().get(headers_str)
    return get_idearef_obj(x_ideaname)


def make_buddelta(x_csv: str) -> BudDelta:
    header_row, headerless_csv = extract_csv_headers(x_csv)
    x_idearef = get_csv_idearef(header_row)

    x_reader = csv_reader(headerless_csv.splitlines(), delimiter=",")
    x_dict = get_positional_dict(header_row)
    x_buddelta = buddelta_shop()
    for row in x_reader:
        x_atomrow = atomrow_shop(x_idearef.dimens, atom_insert())
        for x_header in header_row:
            if header_index := x_dict.get(x_header):
                x_atomrow.__dict__[x_header] = row[header_index]

        for x_atomunit in x_atomrow.get_atomunits():
            x_buddelta.set_atomunit(x_atomunit)
    return x_buddelta


def _load_individual_idea_csv(
    complete_csv: str,
    fisc_mstr_dir: str,
    x_fisc_title: FiscTitle,
    x_owner_name: OwnerName,
):
    x_hubunit = hubunit_shop(fisc_mstr_dir, x_fisc_title, x_owner_name)
    x_hubunit.initialize_gift_voice_files()
    x_voice = x_hubunit.get_voice_bud()
    x_buddelta = make_buddelta(complete_csv)
    # x_buddelta = get_minimal_buddelta(x_buddelta, x_voice)
    x_giftunit = giftunit_shop(x_owner_name, x_fisc_title)
    x_giftunit.set_buddelta(x_buddelta)
    x_hubunit.save_gift_file(x_giftunit)
    x_hubunit._create_voice_from_gifts()


def load_idea_csv(fisc_mstr_dir: str, x_file_dir: str, x_filename: str):
    x_csv = open_file(x_file_dir, x_filename)
    headers_list, headerless_csv = extract_csv_headers(x_csv)
    nested_csv = fisc_title_owner_name_nested_csv_dict(headerless_csv, delimiter=",")
    for x_fisc_title, fisc_dict in nested_csv.items():
        for x_owner_name, owner_csv in fisc_dict.items():
            complete_csv = add_headers_to_csv(headers_list, owner_csv)
            _load_individual_idea_csv(
                complete_csv, fisc_mstr_dir, x_fisc_title, x_owner_name
            )


def get_csv_fisc_title_owner_name_metrics(
    headerless_csv: str, delimiter: str = None
) -> dict[FiscTitle, dict[OwnerName, int]]:
    return get_csv_column1_column2_metrics(headerless_csv, delimiter)


def fisc_title_owner_name_nested_csv_dict(
    headerless_csv: str, delimiter: str = None
) -> dict[FiscTitle, dict[OwnerName, str]]:
    return create_l2nested_csv_dict(headerless_csv, delimiter)


def fisc_build_from_df(
    br00000_df: DataFrame,
    br00001_df: DataFrame,
    br00002_df: DataFrame,
    br00003_df: DataFrame,
    br00004_df: DataFrame,
    br00005_df: DataFrame,
    x_fund_coin: float,
    x_respect_bit: float,
    x_penny: float,
    x_fiscs_dir: str,
) -> dict[FiscTitle, FiscUnit]:
    fisc_hours_dict = _get_fisc_hours_dict(br00003_df)
    fisc_months_dict = _get_fisc_months_dict(br00004_df)
    fisc_weekdays_dict = _get_fisc_weekdays_dict(br00005_df)

    fiscunit_dict = {}
    for index, row in br00000_df.iterrows():
        x_fisc_title = row["fisc_title"]
        x_timeline_config = {
            "c400_number": row["c400_number"],
            "hours_config": fisc_hours_dict.get(x_fisc_title),
            "months_config": fisc_months_dict.get(x_fisc_title),
            "monthday_distortion": row["monthday_distortion"],
            "timeline_title": row["timeline_title"],
            "weekdays_config": fisc_weekdays_dict.get(x_fisc_title),
            "yr1_jan1_offset": row["yr1_jan1_offset"],
        }
        x_timeline = timelineunit_shop(x_timeline_config)
        x_fiscunit = fiscunit_shop(
            fisc_title=x_fisc_title,
            fisc_mstr_dir=x_fiscs_dir,
            timeline=x_timeline,
            present_time=row["present_time"],
            # in_memory_journal=row["in_memory_journal"],
            bridge=row["bridge"],
            fund_coin=x_fund_coin,
            respect_bit=x_respect_bit,
            penny=x_penny,
        )
        fiscunit_dict[x_fiscunit.fisc_title] = x_fiscunit
        _add_dealunits_from_df(x_fiscunit, br00001_df)
        _add_cashpurchases_from_df(x_fiscunit, br00002_df)
    return fiscunit_dict


def _get_fisc_hours_dict(br00003_df: DataFrame) -> dict[str, list[str, str]]:
    fisc_hours_dict = {}
    for y_fisc_title in br00003_df.fisc_title.unique():
        query_str = f"fisc_title == '{y_fisc_title}'"
        x_hours_list = [
            [row["hour_title"], row["cumlative_minute"]]
            for index, row in br00003_df.query(query_str).iterrows()
        ]
        fisc_hours_dict[y_fisc_title] = x_hours_list
    return fisc_hours_dict


def _get_fisc_months_dict(br00004_df: DataFrame) -> dict[str, list[str, str]]:
    fisc_months_dict = {}
    for y_fisc_title in br00004_df.fisc_title.unique():
        query_str = f"fisc_title == '{y_fisc_title}'"
        x_months_list = [
            [row["month_title"], row["cumlative_day"]]
            for index, row in br00004_df.query(query_str).iterrows()
        ]
        fisc_months_dict[y_fisc_title] = x_months_list
    return fisc_months_dict


def _get_fisc_weekdays_dict(br00005_df: DataFrame) -> dict[str, list[str, str]]:
    fisc_weekdays_dict = {}
    for y_fisc_title in br00005_df.fisc_title.unique():
        query_str = f"fisc_title == '{y_fisc_title}'"
        x_weekdays_list = [
            row["weekday_title"]
            for index, row in br00005_df.query(query_str).iterrows()
        ]
        fisc_weekdays_dict[y_fisc_title] = x_weekdays_list
    return fisc_weekdays_dict


def _add_dealunits_from_df(x_fiscunit: FiscUnit, br00001_df: DataFrame):
    query_str = f"fisc_title == '{x_fiscunit.fisc_title}'"
    for index, row in br00001_df.query(query_str).iterrows():
        x_fiscunit.add_dealunit(
            owner_name=row["owner_name"],
            time_int=row["time_int"],
            quota=row["quota"],
            celldepth=if_nan_return_None(row["celldepth"]),
            allow_prev_to_present_time_entry=True,
        )


def _add_cashpurchases_from_df(x_fiscunit: FiscUnit, br00002_df: DataFrame):
    query_str = f"fisc_title == '{x_fiscunit.fisc_title}'"
    for index, row in br00002_df.query(query_str).iterrows():
        x_fiscunit.add_cashpurchase(
            owner_name=row["owner_name"],
            acct_name=row["acct_name"],
            time_int=row["time_int"],
            amount=row["amount"],
        )


def create_init_stance_idea_brick_csv_strs() -> dict[str, str]:
    """Returns strings of csv headers with comma delimiter"""
    stance_idea_bricks = [
        "br00000",
        "br00001",
        "br00002",
        "br00003",
        "br00004",
        "br00005",
        "br00020",
        "br00021",
        "br00022",
        "br00023",
        "br00024",
        "br00025",
        "br00026",
        "br00027",
        "br00028",
        "br00029",
        "br00042",
        "br00043",
        "br00044",
        "br00045",
    ]
    idea_format_headers = get_idea_format_headers()

    fisc_csv_strs = {}
    for idea_brick in stance_idea_bricks:
        idea_format_filename = get_idea_format_filename(idea_brick)
        for idea_columns, idea_file_name in idea_format_headers.items():
            if idea_file_name == idea_format_filename:
                fisc_csv_strs[idea_brick] = f"face_name,event_int,{idea_columns}\n"
    return fisc_csv_strs


def add_fiscunits_to_stance_csv_strs(
    fiscs_dict: dict[FiscTitle, FiscUnit],
    fisc_csv_strs: dict[str, str],
    csv_delimiter: str,
):
    for x_fisc in fiscs_dict.values():
        add_fiscunit_to_stance_csv_strs(x_fisc, fisc_csv_strs, csv_delimiter)


def add_fiscunit_to_stance_csv_strs(
    x_fisc: FiscUnit, fisc_csv_strs: dict[str, str], csv_delimiter: str
) -> dict[str, str]:
    br00000_csv = fisc_csv_strs.get("br00000")
    br00001_csv = fisc_csv_strs.get("br00001")
    br00002_csv = fisc_csv_strs.get("br00002")
    br00003_csv = fisc_csv_strs.get("br00003")
    br00004_csv = fisc_csv_strs.get("br00004")
    br00005_csv = fisc_csv_strs.get("br00005")
    br00000_csv = _add_fiscunit_to_br00000_csv(br00000_csv, x_fisc, csv_delimiter)
    br00001_csv = _add_dealunit_to_br00001_csv(br00001_csv, x_fisc, csv_delimiter)
    br00002_csv = _add_cashbook_to_br00002_csv(br00002_csv, x_fisc, csv_delimiter)
    br00003_csv = _add_hours_to_br00003_csv(br00003_csv, x_fisc, csv_delimiter)
    br00004_csv = _add_months_to_br00004_csv(br00004_csv, x_fisc, csv_delimiter)
    br00005_csv = _add_weekdays_to_br00005_csv(br00005_csv, x_fisc, csv_delimiter)
    fisc_csv_strs["br00000"] = br00000_csv
    fisc_csv_strs["br00001"] = br00001_csv
    fisc_csv_strs["br00002"] = br00002_csv
    fisc_csv_strs["br00003"] = br00003_csv
    fisc_csv_strs["br00004"] = br00004_csv
    fisc_csv_strs["br00005"] = br00005_csv


def _add_fiscunit_to_br00000_csv(
    x_csv: str,
    x_fisc: FiscUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    if x_fisc.bridge == csv_delimiter:
        x_bridge = f"""\"{str(x_fisc.bridge)}\""""
    else:
        x_bridge = x_fisc.bridge

    x_row = [
        if_none_str(face_name),
        if_none_str(event_int),
        x_fisc.fisc_title,
        x_fisc.timeline.timeline_title,
        str(x_fisc.timeline.c400_number),
        str(x_fisc.timeline.yr1_jan1_offset),
        str(x_fisc.timeline.monthday_distortion),
        str(x_fisc.fund_coin),
        str(x_fisc.penny),
        str(x_fisc.respect_bit),
        str(x_fisc.present_time),
        x_bridge,
    ]
    x_csv += csv_delimiter.join(x_row)
    x_csv += "\n"
    return x_csv


def _add_dealunit_to_br00001_csv(
    x_csv: str,
    x_fisc: FiscUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for broker_owner_name, brokerunits in x_fisc.brokerunits.items():
        for time_int, dealunit in brokerunits.deals.items():
            x_row = [if_none_str(face_name), if_none_str(event_int)]
            x_row.extend(
                [
                    x_fisc.fisc_title,
                    broker_owner_name,
                    str(time_int),
                    str(dealunit.quota),
                    str(dealunit.celldepth),
                ]
            )
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def _add_cashbook_to_br00002_csv(
    x_csv: str,
    x_fisc: FiscUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for owner_name, tranunit in x_fisc.cashbook.tranunits.items():
        for acct_name, time_dict in tranunit.items():
            for time_int, amount in time_dict.items():
                fisc_title = x_fisc.fisc_title
                x_row = [
                    if_none_str(face_name),
                    if_none_str(event_int),
                    fisc_title,
                    owner_name,
                    acct_name,
                    str(time_int),
                    str(amount),
                ]
                x_csv += csv_delimiter.join(x_row)
                x_csv += "\n"
    return x_csv


def _add_hours_to_br00003_csv(
    x_csv: str,
    x_fisc: FiscUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for hour_item in x_fisc.timeline.hours_config:
        x_row = [if_none_str(face_name), if_none_str(event_int)]
        x_row.extend([x_fisc.fisc_title, str(hour_item[1]), hour_item[0]])
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def _add_months_to_br00004_csv(
    x_csv: str,
    x_fisc: FiscUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for month_item in x_fisc.timeline.months_config:
        x_row = [if_none_str(face_name), if_none_str(event_int)]
        x_row.extend([x_fisc.fisc_title, str(month_item[1]), month_item[0]])
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def _add_weekdays_to_br00005_csv(
    x_csv: str,
    x_fisc: FiscUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for count_x, weekday_title in enumerate(x_fisc.timeline.weekdays_config):
        x_row = [if_none_str(face_name), if_none_str(event_int)]
        x_row.extend([x_fisc.fisc_title, str(count_x), weekday_title])
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_bud_to_br00020_csv(
    x_csv: str,
    x_bud: BudUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for acctunit in x_bud.accts.values():
        for membership in acctunit._memberships.values():
            x_row = [if_none_str(face_name), if_none_str(event_int)]
            x_row.extend(
                [
                    x_bud.fisc_title,
                    x_bud.owner_name,
                    acctunit.acct_name,
                    membership.group_label,
                    if_none_str(membership.credit_vote),
                    if_none_str(membership.debtit_vote),
                ]
            )
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_bud_to_br00021_csv(
    x_csv: str,
    x_bud: BudUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for acctunit in x_bud.accts.values():
        x_row = [if_none_str(face_name), if_none_str(event_int)]
        x_row.extend(
            [
                x_bud.fisc_title,
                x_bud.owner_name,
                acctunit.acct_name,
                if_none_str(acctunit.credit_belief),
                if_none_str(acctunit.debtit_belief),
            ]
        )
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_bud_to_br00022_csv(
    x_csv: str,
    x_bud: BudUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for itemunit in x_bud._item_dict.values():
        for awardlink in itemunit.awardlinks.values():
            x_row = [if_none_str(face_name), if_none_str(event_int)]
            x_row.extend(
                [
                    x_bud.fisc_title,
                    x_bud.owner_name,
                    itemunit.get_road(),
                    awardlink.awardee_tag,
                    if_none_str(awardlink.give_force),
                    if_none_str(awardlink.take_force),
                ]
            )
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_bud_to_br00023_csv(
    x_csv: str,
    x_bud: BudUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for factunit in x_bud.itemroot.factunits.values():
        x_row = [if_none_str(face_name), if_none_str(event_int)]
        x_row.extend(
            [
                x_bud.fisc_title,
                x_bud.owner_name,
                factunit.base,
                factunit.pick,
                if_none_str(factunit.fopen),
                if_none_str(factunit.fnigh),
            ]
        )
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_bud_to_br00024_csv(
    x_csv: str,
    x_bud: BudUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for itemunit in x_bud._item_dict.values():
        for group_tag in itemunit.teamunit._teamlinks:
            x_row = [if_none_str(face_name), if_none_str(event_int)]
            x_row.extend(
                [x_bud.fisc_title, x_bud.owner_name, itemunit.get_road(), group_tag]
            )
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_bud_to_br00025_csv(
    x_csv: str,
    x_bud: BudUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for itemunit in x_bud._item_dict.values():
        for group_tag in itemunit.healerlink._healer_names:
            x_row = [if_none_str(face_name), if_none_str(event_int)]
            x_row.extend(
                [x_bud.fisc_title, x_bud.owner_name, itemunit.get_road(), group_tag]
            )
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_bud_to_br00026_csv(
    x_csv: str,
    x_bud: BudUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for itemunit in x_bud._item_dict.values():
        for reasonunit in itemunit.reasonunits.values():
            for premiseunit in reasonunit.premises.values():
                x_row = [if_none_str(face_name), if_none_str(event_int)]
                x_row.extend(
                    [
                        x_bud.fisc_title,
                        x_bud.owner_name,
                        itemunit.get_road(),
                        reasonunit.base,
                        premiseunit.need,
                        if_none_str(premiseunit.open),
                        if_none_str(premiseunit.nigh),
                        if_none_str(premiseunit.divisor),
                    ]
                )
                x_csv += csv_delimiter.join(x_row)
                x_csv += "\n"
    return x_csv


def add_bud_to_br00027_csv(
    x_csv: str,
    x_bud: BudUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for itemunit in x_bud._item_dict.values():
        for reasonunit in itemunit.reasonunits.values():
            x_row = [if_none_str(face_name), if_none_str(event_int)]
            x_row.extend(
                [
                    x_bud.fisc_title,
                    x_bud.owner_name,
                    itemunit.get_road(),
                    reasonunit.base,
                    if_none_str(reasonunit.base_item_active_requisite),
                ]
            )
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_bud_to_br00028_csv(
    x_csv: str,
    x_bud: BudUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    for itemunit in x_bud._item_dict.values():
        x_row = [if_none_str(face_name), if_none_str(event_int)]
        x_row.extend(
            [
                x_bud.fisc_title,
                x_bud.owner_name,
                itemunit._parent_road,
                itemunit._item_title,
                if_none_str(itemunit.begin),
                if_none_str(itemunit.close),
                if_none_str(itemunit.addin),
                if_none_str(itemunit.numor),
                if_none_str(itemunit.denom),
                if_none_str(itemunit.morph),
                if_none_str(itemunit.gogo_want),
                if_none_str(itemunit.stop_want),
                if_none_str(itemunit.mass),
                if_none_str(itemunit.pledge),
                if_none_str(itemunit.problem_bool),
            ]
        )
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_bud_to_br00029_csv(
    x_csv: str,
    x_bud: BudUnit,
    csv_delimiter: str,
    face_name: FaceName = None,
    event_int: int = None,
) -> str:
    x_row = [if_none_str(face_name), if_none_str(event_int)]
    x_row.extend(
        [
            x_bud.fisc_title,
            x_bud.owner_name,
            if_none_str(x_bud.credor_respect),
            if_none_str(x_bud.debtor_respect),
            if_none_str(x_bud.fund_pool),
            if_none_str(x_bud.max_tree_traverse),
            if_none_str(x_bud.tally),
            if_none_str(x_bud.fund_coin),
            if_none_str(x_bud.penny),
            if_none_str(x_bud.respect_bit),
        ]
    )
    x_csv += csv_delimiter.join(x_row)
    x_csv += "\n"
    return x_csv


def add_budunit_to_stance_csv_strs(
    x_bud: BudUnit, fisc_csv_strs: dict[str, str], csv_delimiter: str
) -> str:
    br00020_csv = fisc_csv_strs.get("br00020")
    br00021_csv = fisc_csv_strs.get("br00021")
    br00022_csv = fisc_csv_strs.get("br00022")
    br00023_csv = fisc_csv_strs.get("br00023")
    br00024_csv = fisc_csv_strs.get("br00024")
    br00025_csv = fisc_csv_strs.get("br00025")
    br00026_csv = fisc_csv_strs.get("br00026")
    br00027_csv = fisc_csv_strs.get("br00027")
    br00028_csv = fisc_csv_strs.get("br00028")
    br00029_csv = fisc_csv_strs.get("br00029")
    br00020_csv = add_bud_to_br00020_csv(br00020_csv, x_bud, csv_delimiter)
    br00021_csv = add_bud_to_br00021_csv(br00021_csv, x_bud, csv_delimiter)
    br00022_csv = add_bud_to_br00022_csv(br00022_csv, x_bud, csv_delimiter)
    br00023_csv = add_bud_to_br00023_csv(br00023_csv, x_bud, csv_delimiter)
    br00024_csv = add_bud_to_br00024_csv(br00024_csv, x_bud, csv_delimiter)
    br00025_csv = add_bud_to_br00025_csv(br00025_csv, x_bud, csv_delimiter)
    br00026_csv = add_bud_to_br00026_csv(br00026_csv, x_bud, csv_delimiter)
    br00027_csv = add_bud_to_br00027_csv(br00027_csv, x_bud, csv_delimiter)
    br00028_csv = add_bud_to_br00028_csv(br00028_csv, x_bud, csv_delimiter)
    br00029_csv = add_bud_to_br00029_csv(br00029_csv, x_bud, csv_delimiter)
    fisc_csv_strs["br00020"] = br00020_csv
    fisc_csv_strs["br00021"] = br00021_csv
    fisc_csv_strs["br00022"] = br00022_csv
    fisc_csv_strs["br00023"] = br00023_csv
    fisc_csv_strs["br00024"] = br00024_csv
    fisc_csv_strs["br00025"] = br00025_csv
    fisc_csv_strs["br00026"] = br00026_csv
    fisc_csv_strs["br00027"] = br00027_csv
    fisc_csv_strs["br00028"] = br00028_csv
    fisc_csv_strs["br00029"] = br00029_csv


def add_to_br00042_csv(x_csv: str, x_pidginunit: PidginUnit, csv_delimiter: str) -> str:
    for x_otx, x_inx in x_pidginunit.labelmap.otx2inx.items():
        x_row = [
            x_pidginunit.face_name,
            str(x_pidginunit.event_int),
            x_otx,
            x_pidginunit.otx_bridge,
            x_inx,
            x_pidginunit.inx_bridge,
            x_pidginunit.unknown_word,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_to_br00043_csv(x_csv: str, x_pidginunit: PidginUnit, csv_delimiter: str) -> str:
    for x_otx, x_inx in x_pidginunit.namemap.otx2inx.items():
        x_row = [
            x_pidginunit.face_name,
            str(x_pidginunit.event_int),
            x_otx,
            x_pidginunit.otx_bridge,
            x_inx,
            x_pidginunit.inx_bridge,
            x_pidginunit.unknown_word,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_to_br00044_csv(x_csv: str, x_pidginunit: PidginUnit, csv_delimiter: str) -> str:
    for x_otx, x_inx in x_pidginunit.titlemap.otx2inx.items():
        x_row = [
            x_pidginunit.face_name,
            str(x_pidginunit.event_int),
            x_otx,
            x_pidginunit.otx_bridge,
            x_inx,
            x_pidginunit.inx_bridge,
            x_pidginunit.unknown_word,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_to_br00045_csv(x_csv: str, x_pidginunit: PidginUnit, csv_delimiter: str) -> str:
    for x_otx, x_inx in x_pidginunit.roadmap.otx2inx.items():
        x_row = [
            x_pidginunit.face_name,
            str(x_pidginunit.event_int),
            x_otx,
            x_pidginunit.otx_bridge,
            x_inx,
            x_pidginunit.inx_bridge,
            x_pidginunit.unknown_word,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_pidginunit_to_stance_csv_strs(
    x_pidgin: PidginUnit, fisc_csv_strs: dict[str, str], csv_delimiter: str
) -> str:
    br00042_csv = fisc_csv_strs.get("br00042")
    br00043_csv = fisc_csv_strs.get("br00043")
    br00044_csv = fisc_csv_strs.get("br00044")
    br00045_csv = fisc_csv_strs.get("br00045")
    br00042_csv = add_to_br00042_csv(br00042_csv, x_pidgin, csv_delimiter)
    br00043_csv = add_to_br00043_csv(br00043_csv, x_pidgin, csv_delimiter)
    br00044_csv = add_to_br00044_csv(br00044_csv, x_pidgin, csv_delimiter)
    br00045_csv = add_to_br00045_csv(br00045_csv, x_pidgin, csv_delimiter)
    fisc_csv_strs["br00042"] = br00042_csv
    fisc_csv_strs["br00043"] = br00043_csv
    fisc_csv_strs["br00044"] = br00044_csv
    fisc_csv_strs["br00045"] = br00045_csv


def add_gift_to_br00020_csv(
    x_csv: str, x_giftunit: GiftUnit, csv_delimiter: str
) -> str:
    return ""


def add_gift_to_br00021_csv(
    x_csv: str, x_giftunit: GiftUnit, csv_delimiter: str
) -> str:
    return ""


def add_gift_to_br00022_csv(
    x_csv: str, x_giftunit: GiftUnit, csv_delimiter: str
) -> str:
    return ""


def add_gift_to_br00023_csv(
    x_csv: str, x_giftunit: GiftUnit, csv_delimiter: str
) -> str:
    return ""


def add_gift_to_br00024_csv(
    x_csv: str, x_giftunit: GiftUnit, csv_delimiter: str
) -> str:
    return ""


def add_gift_to_br00025_csv(
    x_csv: str, x_giftunit: GiftUnit, csv_delimiter: str
) -> str:
    return ""


def add_gift_to_br00026_csv(
    x_csv: str, x_giftunit: GiftUnit, csv_delimiter: str
) -> str:
    return ""


def add_gift_to_br00027_csv(
    x_csv: str, x_giftunit: GiftUnit, csv_delimiter: str
) -> str:
    return ""


def add_gift_to_br00028_csv(
    x_csv: str, x_giftunit: GiftUnit, csv_delimiter: str
) -> str:
    return ""


def add_gift_to_br00029_csv(
    x_csv: str, x_giftunit: GiftUnit, csv_delimiter: str
) -> str:
    return ""
