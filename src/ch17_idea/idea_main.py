from csv import reader as csv_reader
from dataclasses import dataclass
from pandas import DataFrame
from src.ch01_data_toolbox.dict_toolbox import (
    create_l2nested_csv_dict,
    extract_csv_headers,
    get_csv_column1_column2_metrics,
    get_positional_dict,
)
from src.ch07_belief_logic.belief_main import BeliefUnit
from src.ch08_epoch_logic.epoch_main import epochunit_shop
from src.ch09_belief_atom_logic.atom_main import BeliefAtom, atomrow_shop
from src.ch10_pack_logic.delta import (
    BeliefDelta,
    beliefdelta_shop,
    get_dimens_cruds_beliefdelta,
)
from src.ch11_bud_logic._ref.ch11_semantic_types import BeliefName, MomentLabel
from src.ch15_moment_logic.moment_main import MomentUnit, momentunit_shop
from src.ch17_idea.idea_config import get_idea_format_headers, get_idearef_from_file
from src.ch17_idea.idea_db_tool import (
    get_default_sorted_list,
    if_nan_return_None,
    save_dataframe_to_csv,
)


@dataclass
class IdeaRef:
    idea_name: str = None
    dimens: list[str] = None
    _attributes: dict[str, dict[str, bool]] = None

    def set_attribute(self, x_attribute: str, otx_key: bool):
        self._attributes[x_attribute] = {"otx_key": otx_key}

    def get_headers_list(self) -> list[str]:
        return get_default_sorted_list(set(self._attributes.keys()))

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


def create_idea_df(x_beliefunit: BeliefUnit, idea_name: str) -> DataFrame:
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.add_all_beliefatoms(x_beliefunit)
    x_idearef = get_idearef_obj(idea_name)
    x_moment_label = x_beliefunit.moment_label
    x_belief_name = x_beliefunit.belief_name
    sorted_beliefatoms = _get_sorted_INSERT_str_beliefatoms(x_beliefdelta, x_idearef)
    d2_list = _create_d2_list(
        sorted_beliefatoms, x_idearef, x_moment_label, x_belief_name
    )
    d2_list = _delta_all_pledge_values(d2_list, x_idearef)
    x_idea = _generate_idea_dataframe(d2_list, idea_name)
    sorting_columns = x_idearef.get_headers_list()
    return _sort_dataframe(x_idea, sorting_columns)


def _get_sorted_INSERT_str_beliefatoms(
    x_beliefdelta: BeliefDelta, x_idearef: IdeaRef
) -> list[BeliefAtom]:
    dimen_set = set(x_idearef.dimens)
    curd_set = {"INSERT"}
    limited_delta = get_dimens_cruds_beliefdelta(x_beliefdelta, dimen_set, curd_set)
    return limited_delta.get_dimen_sorted_beliefatoms_list()


def _create_d2_list(
    sorted_beliefatoms: list[BeliefAtom],
    x_idearef: IdeaRef,
    x_moment_label: MomentLabel,
    x_belief_name: BeliefName,
):
    d2_list = []
    for x_beliefatom in sorted_beliefatoms:
        d1_list = []
        for x_attribute in x_idearef.get_headers_list():
            if x_attribute == "moment_label":
                d1_list.append(x_moment_label)
            elif x_attribute == "belief_name":
                d1_list.append(x_belief_name)
            else:
                d1_list.append(x_beliefatom.get_value(x_attribute))
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


def save_idea_csv(
    x_ideaname: str, x_beliefunit: BeliefUnit, x_dir: str, x_filename: str
):
    x_dataframe = create_idea_df(x_beliefunit, x_ideaname)
    save_dataframe_to_csv(x_dataframe, x_dir, x_filename)


def get_csv_idearef(header_row: list[str]) -> IdeaRef:
    header_row = get_default_sorted_list(set(header_row))
    headers_str = "".join(f",{x_header}" for x_header in header_row)
    headers_str = headers_str[1:]
    headers_str = headers_str.replace("face_name,", "")
    headers_str = headers_str.replace("event_int,", "")
    x_ideaname = get_idea_format_headers().get(headers_str)
    return get_idearef_obj(x_ideaname)


def _remove_non_belief_dimens_from_idearef(x_idearef: IdeaRef) -> IdeaRef:
    to_delete_dimen_set = {
        dimen for dimen in x_idearef.dimens if not dimen.startswith("belief")
    }
    dimens_set = set(x_idearef.dimens)
    for to_delete_dimen in to_delete_dimen_set:
        if to_delete_dimen in dimens_set:
            dimens_set.remove(to_delete_dimen)
    x_idearef.dimens = list(dimens_set)
    return x_idearef


def make_beliefdelta(x_csv: str) -> BeliefDelta:
    header_row, headerless_csv = extract_csv_headers(x_csv)
    x_idearef = get_csv_idearef(header_row)
    _remove_non_belief_dimens_from_idearef(x_idearef)
    x_reader = csv_reader(headerless_csv.splitlines(), delimiter=",")
    x_dict = get_positional_dict(header_row)
    x_beliefdelta = beliefdelta_shop()

    for row in x_reader:
        x_atomrow = atomrow_shop(x_idearef.dimens, "INSERT")
        for x_header in header_row:
            if header_index := x_dict.get(x_header):
                x_atomrow.__dict__[x_header] = row[header_index]

        for x_beliefatom in x_atomrow.get_beliefatoms():
            x_beliefdelta.set_beliefatom(x_beliefatom)
    return x_beliefdelta


def get_csv_moment_label_belief_name_metrics(
    headerless_csv: str, delimiter: str = None
) -> dict[MomentLabel, dict[BeliefName, int]]:
    return get_csv_column1_column2_metrics(headerless_csv, delimiter)


def moment_label_belief_name_nested_csv_dict(
    headerless_csv: str, delimiter: str = None
) -> dict[MomentLabel, dict[BeliefName, str]]:
    return create_l2nested_csv_dict(headerless_csv, delimiter)


def moment_build_from_df(
    br00000_df: DataFrame,
    br00001_df: DataFrame,
    br00002_df: DataFrame,
    br00003_df: DataFrame,
    br00004_df: DataFrame,
    br00005_df: DataFrame,
    x_fund_grain: float,
    x_respect_grain: float,
    x_money_grain: float,
    x_moments_dir: str,
) -> dict[MomentLabel, MomentUnit]:
    moment_hours_dict = _get_moment_hours_dict(br00003_df)
    moment_months_dict = _get_moment_months_dict(br00004_df)
    moment_weekdays_dict = _get_moment_weekdays_dict(br00005_df)

    momentunit_dict = {}
    for index, row in br00000_df.iterrows():
        x_moment_label = row["moment_label"]
        x_epoch_config = {
            "c400_number": row["c400_number"],
            "hours_config": moment_hours_dict.get(x_moment_label),
            "months_config": moment_months_dict.get(x_moment_label),
            "monthday_index": row["monthday_index"],
            "epoch_label": row["epoch_label"],
            "weekdays_config": moment_weekdays_dict.get(x_moment_label),
            "yr1_jan1_offset": row["yr1_jan1_offset"],
        }
        x_epoch = epochunit_shop(x_epoch_config)
        x_momentunit = momentunit_shop(
            moment_label=x_moment_label,
            moment_mstr_dir=x_moments_dir,
            epoch=x_epoch,
            knot=row["knot"],
            fund_grain=x_fund_grain,
            respect_grain=x_respect_grain,
            money_grain=x_money_grain,
            job_listen_rotations=row["job_listen_rotations"],
        )
        momentunit_dict[x_momentunit.moment_label] = x_momentunit
        _add_budunits_from_df(x_momentunit, br00001_df)
        _add_paypurchases_from_df(x_momentunit, br00002_df)
    return momentunit_dict


def _get_moment_hours_dict(br00003_df: DataFrame) -> dict[str, list[str, str]]:
    moment_hours_dict = {}
    for y_moment_label in br00003_df.moment_label.unique():
        query_str = f"moment_label == '{y_moment_label}'"
        x_hours_list = [
            [row["hour_label"], row["cumulative_minute"]]
            for index, row in br00003_df.query(query_str).iterrows()
        ]
        moment_hours_dict[y_moment_label] = x_hours_list
    return moment_hours_dict


def _get_moment_months_dict(br00004_df: DataFrame) -> dict[str, list[str, str]]:
    moment_months_dict = {}
    for y_moment_label in br00004_df.moment_label.unique():
        query_str = f"moment_label == '{y_moment_label}'"
        x_months_list = [
            [row["month_label"], row["cumulative_day"]]
            for index, row in br00004_df.query(query_str).iterrows()
        ]
        moment_months_dict[y_moment_label] = x_months_list
    return moment_months_dict


def _get_moment_weekdays_dict(br00005_df: DataFrame) -> dict[str, list[str, str]]:
    moment_weekdays_dict = {}
    for y_moment_label in br00005_df.moment_label.unique():
        query_str = f"moment_label == '{y_moment_label}'"
        x_weekdays_list = [
            row["weekday_label"]
            for index, row in br00005_df.query(query_str).iterrows()
        ]
        moment_weekdays_dict[y_moment_label] = x_weekdays_list
    return moment_weekdays_dict


def _add_budunits_from_df(x_momentunit: MomentUnit, br00001_df: DataFrame):
    query_str = f"moment_label == '{x_momentunit.moment_label}'"
    for index, row in br00001_df.query(query_str).iterrows():
        x_momentunit.add_budunit(
            belief_name=row["belief_name"],
            bud_time=row["bud_time"],
            quota=row["quota"],
            celldepth=if_nan_return_None(row["celldepth"]),
            allow_prev_to_offi_time_max_entry=True,
        )


def _add_paypurchases_from_df(x_momentunit: MomentUnit, br00002_df: DataFrame):
    query_str = f"moment_label == '{x_momentunit.moment_label}'"
    for index, row in br00002_df.query(query_str).iterrows():
        x_momentunit.add_paypurchase(
            belief_name=row["belief_name"],
            voice_name=row["voice_name"],
            tran_time=row["tran_time"],
            amount=row["amount"],
        )


def _add_time_offi_units_from_df(x_momentunit: MomentUnit, br00006_df: DataFrame):
    query_str = f"moment_label == '{x_momentunit.moment_label}'"
    for index, row in br00006_df.query(query_str).iterrows():
        x_momentunit.offi_times.add(row["offi_time"])
