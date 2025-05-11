from src.a00_data_toolbox.file_toolbox import open_file
from src.a00_data_toolbox.dict_toolbox import (
    extract_csv_headers,
    get_csv_column1_column2_metrics,
    create_l2nested_csv_dict,
    get_positional_dict,
    add_headers_to_csv,
)
from src.a01_way_logic.way import FiscTag, OwnerName
from src.a06_bud_logic.bud import BudUnit
from src.a07_calendar_logic.chrono import timelineunit_shop
from src.a08_bud_atom_logic.atom import atom_insert, BudAtom, atomrow_shop
from src.a09_pack_logic.delta import buddelta_shop, get_dimens_cruds_buddelta, BudDelta
from src.a09_pack_logic.pack import packunit_shop
from src.a12_hub_tools.hub_tool import open_gut_file, save_gut_file
from src.a12_hub_tools.hubunit import hubunit_shop
from src.a15_fisc_logic.fisc import fiscunit_shop, FiscUnit
from src.a17_idea_logic.idea_config import (
    get_idearef_from_file,
    get_idea_format_headers,
    get_idea_format_headers,
)
from src.a17_idea_logic.idea_db_tool import (
    save_dataframe_to_csv,
    get_default_sorted_list,
    if_nan_return_None,
)
from pandas import DataFrame
from csv import reader as csv_reader
from dataclasses import dataclass


@dataclass
class IdeaRef:
    idea_name: str = None
    dimens: list[str] = None
    _attributes: dict[str, dict[str, bool]] = None

    def set_attribute(self, x_attribute: str, otx_key: bool):
        self._attributes[x_attribute] = {"otx_key": otx_key}

    def get_headers_list(self) -> list[str]:
        return get_default_sorted_list(self._attributes)

    def get_otx_keys_list(self) -> list[str]:
        x_set = {
            x_attr
            for x_attr, otx_dict in self._attributes.items()
            if otx_dict.get("otx_key") is True
        }
        return get_default_sorted_list(x_set)

    def get_otx_values_list(self) -> list[str]:
        x_set = {
            x_attr
            for x_attr, otx_dict in self._attributes.items()
            if otx_dict.get("otx_key") is False
        }
        return get_default_sorted_list(x_set)


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
    x_buddelta.add_all_budatoms(x_budunit)
    x_idearef = get_idearef_obj(idea_name)
    x_fisc_tag = x_budunit.fisc_tag
    x_owner_name = x_budunit.owner_name
    sorted_budatoms = _get_sorted_atom_insert_budatoms(x_buddelta, x_idearef)
    d2_list = _create_d2_list(sorted_budatoms, x_idearef, x_fisc_tag, x_owner_name)
    d2_list = _delta_all_pledge_values(d2_list, x_idearef)
    x_idea = _generate_idea_dataframe(d2_list, idea_name)
    sorting_columns = x_idearef.get_headers_list()
    return _sort_dataframe(x_idea, sorting_columns)


def _get_sorted_atom_insert_budatoms(
    x_buddelta: BudDelta, x_idearef: IdeaRef
) -> list[BudAtom]:
    dimen_set = set(x_idearef.dimens)
    curd_set = {atom_insert()}
    limited_delta = get_dimens_cruds_buddelta(x_buddelta, dimen_set, curd_set)
    return limited_delta.get_dimen_sorted_budatoms_list()


def _create_d2_list(
    sorted_budatoms: list[BudAtom],
    x_idearef: IdeaRef,
    x_fisc_tag: FiscTag,
    x_owner_name: OwnerName,
):
    d2_list = []
    for x_budatom in sorted_budatoms:
        d1_list = []
        for x_attribute in x_idearef.get_headers_list():
            if x_attribute == "fisc_tag":
                d1_list.append(x_fisc_tag)
            elif x_attribute == "owner_name":
                d1_list.append(x_owner_name)
            else:
                d1_list.append(x_budatom.get_value(x_attribute))
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
    header_row = get_default_sorted_list(header_row)
    headers_str = "".join(f",{x_header}" for x_header in header_row)
    headers_str = headers_str[1:]
    headers_str = headers_str.replace("face_name,", "")
    headers_str = headers_str.replace("event_int,", "")
    x_ideaname = get_idea_format_headers().get(headers_str)
    return get_idearef_obj(x_ideaname)


def _remove_non_bud_dimens_from_idearef(x_idearef: IdeaRef) -> IdeaRef:
    to_delete_dimen_set = {dimen for dimen in x_idearef.dimens if dimen[:3] != "bud"}
    dimens_set = set(x_idearef.dimens)
    for to_delete_dimen in to_delete_dimen_set:
        if to_delete_dimen in dimens_set:
            dimens_set.remove(to_delete_dimen)
    x_idearef.dimens = list(dimens_set)
    return x_idearef


def make_buddelta(x_csv: str) -> BudDelta:
    header_row, headerless_csv = extract_csv_headers(x_csv)
    x_idearef = get_csv_idearef(header_row)
    _remove_non_bud_dimens_from_idearef(x_idearef)
    x_reader = csv_reader(headerless_csv.splitlines(), delimiter=",")
    x_dict = get_positional_dict(header_row)
    x_buddelta = buddelta_shop()

    for row in x_reader:
        x_atomrow = atomrow_shop(x_idearef.dimens, atom_insert())
        for x_header in header_row:
            if header_index := x_dict.get(x_header):
                x_atomrow.__dict__[x_header] = row[header_index]

        for x_budatom in x_atomrow.get_budatoms():
            x_buddelta.set_budatom(x_budatom)
    return x_buddelta


def _load_individual_idea_csv(
    complete_csv: str,
    fisc_mstr_dir: str,
    x_fisc_tag: FiscTag,
    x_owner_name: OwnerName,
):
    x_hubunit = hubunit_shop(fisc_mstr_dir, x_fisc_tag, x_owner_name)
    x_hubunit.initialize_pack_gut_files()
    x_buddelta = make_buddelta(complete_csv)
    # x_buddelta = get_minimal_buddelta(x_buddelta, x_gut)
    x_packunit = packunit_shop(x_owner_name, x_fisc_tag)
    x_packunit.set_buddelta(x_buddelta)
    x_hubunit.save_pack_file(x_packunit)
    x_hubunit._create_gut_from_packs()


def load_idea_csv(fisc_mstr_dir: str, x_file_dir: str, x_filename: str):
    x_csv = open_file(x_file_dir, x_filename)
    headers_list, headerless_csv = extract_csv_headers(x_csv)
    nested_csv = fisc_tag_owner_name_nested_csv_dict(headerless_csv, delimiter=",")
    for x_fisc_tag, fisc_dict in nested_csv.items():
        for x_owner_name, owner_csv in fisc_dict.items():
            complete_csv = add_headers_to_csv(headers_list, owner_csv)
            _load_individual_idea_csv(
                complete_csv, fisc_mstr_dir, x_fisc_tag, x_owner_name
            )


def get_csv_fisc_tag_owner_name_metrics(
    headerless_csv: str, delimiter: str = None
) -> dict[FiscTag, dict[OwnerName, int]]:
    return get_csv_column1_column2_metrics(headerless_csv, delimiter)


def fisc_tag_owner_name_nested_csv_dict(
    headerless_csv: str, delimiter: str = None
) -> dict[FiscTag, dict[OwnerName, str]]:
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
) -> dict[FiscTag, FiscUnit]:
    fisc_hours_dict = _get_fisc_hours_dict(br00003_df)
    fisc_months_dict = _get_fisc_months_dict(br00004_df)
    fisc_weekdays_dict = _get_fisc_weekdays_dict(br00005_df)

    fiscunit_dict = {}
    for index, row in br00000_df.iterrows():
        x_fisc_tag = row["fisc_tag"]
        x_timeline_config = {
            "c400_number": row["c400_number"],
            "hours_config": fisc_hours_dict.get(x_fisc_tag),
            "months_config": fisc_months_dict.get(x_fisc_tag),
            "monthday_distortion": row["monthday_distortion"],
            "timeline_tag": row["timeline_tag"],
            "weekdays_config": fisc_weekdays_dict.get(x_fisc_tag),
            "yr1_jan1_offset": row["yr1_jan1_offset"],
        }
        x_timeline = timelineunit_shop(x_timeline_config)
        x_fiscunit = fiscunit_shop(
            fisc_tag=x_fisc_tag,
            fisc_mstr_dir=x_fiscs_dir,
            timeline=x_timeline,
            # in_memory_journal=row["in_memory_journal"],
            bridge=row["bridge"],
            fund_coin=x_fund_coin,
            respect_bit=x_respect_bit,
            penny=x_penny,
            job_listen_rotations=row["job_listen_rotations"],
        )
        fiscunit_dict[x_fiscunit.fisc_tag] = x_fiscunit
        _add_dealunits_from_df(x_fiscunit, br00001_df)
        _add_cashpurchases_from_df(x_fiscunit, br00002_df)
    return fiscunit_dict


def _get_fisc_hours_dict(br00003_df: DataFrame) -> dict[str, list[str, str]]:
    fisc_hours_dict = {}
    for y_fisc_tag in br00003_df.fisc_tag.unique():
        query_str = f"fisc_tag == '{y_fisc_tag}'"
        x_hours_list = [
            [row["hour_tag"], row["cumlative_minute"]]
            for index, row in br00003_df.query(query_str).iterrows()
        ]
        fisc_hours_dict[y_fisc_tag] = x_hours_list
    return fisc_hours_dict


def _get_fisc_months_dict(br00004_df: DataFrame) -> dict[str, list[str, str]]:
    fisc_months_dict = {}
    for y_fisc_tag in br00004_df.fisc_tag.unique():
        query_str = f"fisc_tag == '{y_fisc_tag}'"
        x_months_list = [
            [row["month_tag"], row["cumlative_day"]]
            for index, row in br00004_df.query(query_str).iterrows()
        ]
        fisc_months_dict[y_fisc_tag] = x_months_list
    return fisc_months_dict


def _get_fisc_weekdays_dict(br00005_df: DataFrame) -> dict[str, list[str, str]]:
    fisc_weekdays_dict = {}
    for y_fisc_tag in br00005_df.fisc_tag.unique():
        query_str = f"fisc_tag == '{y_fisc_tag}'"
        x_weekdays_list = [
            row["weekday_tag"] for index, row in br00005_df.query(query_str).iterrows()
        ]
        fisc_weekdays_dict[y_fisc_tag] = x_weekdays_list
    return fisc_weekdays_dict


def _add_dealunits_from_df(x_fiscunit: FiscUnit, br00001_df: DataFrame):
    query_str = f"fisc_tag == '{x_fiscunit.fisc_tag}'"
    for index, row in br00001_df.query(query_str).iterrows():
        x_fiscunit.add_dealunit(
            owner_name=row["owner_name"],
            deal_time=row["deal_time"],
            quota=row["quota"],
            celldepth=if_nan_return_None(row["celldepth"]),
            allow_prev_to_offi_time_max_entry=True,
        )


def _add_cashpurchases_from_df(x_fiscunit: FiscUnit, br00002_df: DataFrame):
    query_str = f"fisc_tag == '{x_fiscunit.fisc_tag}'"
    for index, row in br00002_df.query(query_str).iterrows():
        x_fiscunit.add_cashpurchase(
            owner_name=row["owner_name"],
            acct_name=row["acct_name"],
            tran_time=row["tran_time"],
            amount=row["amount"],
        )


def _add_time_offi_units_from_df(x_fiscunit: FiscUnit, br00006_df: DataFrame):
    query_str = f"fisc_tag == '{x_fiscunit.fisc_tag}'"
    for index, row in br00006_df.query(query_str).iterrows():
        x_fiscunit.offi_times.add(row["offi_time"])
