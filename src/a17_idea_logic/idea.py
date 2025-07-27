from csv import reader as csv_reader
from dataclasses import dataclass
from pandas import DataFrame
from src.a00_data_toolbox.dict_toolbox import (
    create_l2nested_csv_dict,
    extract_csv_headers,
    get_csv_column1_column2_metrics,
    get_positional_dict,
)
from src.a01_term_logic.term import BeliefLabel, BelieverName
from src.a06_believer_logic.believer_main import BelieverUnit
from src.a07_timeline_logic.timeline_main import timelineunit_shop
from src.a08_believer_atom_logic.atom import BelieverAtom, atomrow_shop
from src.a09_pack_logic.delta import (
    BelieverDelta,
    believerdelta_shop,
    get_dimens_cruds_believerdelta,
)
from src.a15_belief_logic.belief import BeliefUnit, beliefunit_shop
from src.a17_idea_logic.idea_config import (
    get_idea_format_headers,
    get_idearef_from_file,
)
from src.a17_idea_logic.idea_db_tool import (
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


def create_idea_df(x_believerunit: BelieverUnit, idea_name: str) -> DataFrame:
    x_believerdelta = believerdelta_shop()
    x_believerdelta.add_all_believeratoms(x_believerunit)
    x_idearef = get_idearef_obj(idea_name)
    x_belief_label = x_believerunit.belief_label
    x_believer_name = x_believerunit.believer_name
    sorted_believeratoms = _get_sorted_INSERT_str_believeratoms(
        x_believerdelta, x_idearef
    )
    d2_list = _create_d2_list(
        sorted_believeratoms, x_idearef, x_belief_label, x_believer_name
    )
    d2_list = _delta_all_task_values(d2_list, x_idearef)
    x_idea = _generate_idea_dataframe(d2_list, idea_name)
    sorting_columns = x_idearef.get_headers_list()
    return _sort_dataframe(x_idea, sorting_columns)


def _get_sorted_INSERT_str_believeratoms(
    x_believerdelta: BelieverDelta, x_idearef: IdeaRef
) -> list[BelieverAtom]:
    dimen_set = set(x_idearef.dimens)
    curd_set = {"INSERT"}
    limited_delta = get_dimens_cruds_believerdelta(x_believerdelta, dimen_set, curd_set)
    return limited_delta.get_dimen_sorted_believeratoms_list()


def _create_d2_list(
    sorted_believeratoms: list[BelieverAtom],
    x_idearef: IdeaRef,
    x_belief_label: BeliefLabel,
    x_believer_name: BelieverName,
):
    d2_list = []
    for x_believeratom in sorted_believeratoms:
        d1_list = []
        for x_attribute in x_idearef.get_headers_list():
            if x_attribute == "belief_label":
                d1_list.append(x_belief_label)
            elif x_attribute == "believer_name":
                d1_list.append(x_believer_name)
            else:
                d1_list.append(x_believeratom.get_value(x_attribute))
        d2_list.append(d1_list)
    return d2_list


def _delta_all_task_values(d2_list: list[list], x_idearef: IdeaRef) -> list[list]:
    if "task" in x_idearef._attributes:
        for x_count, x_header in enumerate(x_idearef.get_headers_list()):
            if x_header == "task":
                task_column_number = x_count
        for x_row in d2_list:
            if x_row[task_column_number] is True:
                x_row[task_column_number] = "Yes"
            else:
                x_row[task_column_number] = ""
    return d2_list


def _sort_dataframe(x_idea: DataFrame, sorting_columns: list[str]) -> DataFrame:
    ascending_bools = get_ascending_bools(sorting_columns)
    x_idea.sort_values(sorting_columns, ascending=ascending_bools, inplace=True)
    x_idea.reset_index(inplace=True)
    x_idea.drop(columns=["index"], inplace=True)
    return x_idea


def save_idea_csv(
    x_ideaname: str, x_believerunit: BelieverUnit, x_dir: str, x_filename: str
):
    x_dataframe = create_idea_df(x_believerunit, x_ideaname)
    save_dataframe_to_csv(x_dataframe, x_dir, x_filename)


def get_csv_idearef(header_row: list[str]) -> IdeaRef:
    header_row = get_default_sorted_list(header_row)
    headers_str = "".join(f",{x_header}" for x_header in header_row)
    headers_str = headers_str[1:]
    headers_str = headers_str.replace("face_name,", "")
    headers_str = headers_str.replace("event_int,", "")
    x_ideaname = get_idea_format_headers().get(headers_str)
    return get_idearef_obj(x_ideaname)


def _remove_non_believer_dimens_from_idearef(x_idearef: IdeaRef) -> IdeaRef:
    to_delete_dimen_set = {
        dimen for dimen in x_idearef.dimens if not dimen.startswith("believer")
    }
    dimens_set = set(x_idearef.dimens)
    for to_delete_dimen in to_delete_dimen_set:
        if to_delete_dimen in dimens_set:
            dimens_set.remove(to_delete_dimen)
    x_idearef.dimens = list(dimens_set)
    return x_idearef


def make_believerdelta(x_csv: str) -> BelieverDelta:
    header_row, headerless_csv = extract_csv_headers(x_csv)
    x_idearef = get_csv_idearef(header_row)
    _remove_non_believer_dimens_from_idearef(x_idearef)
    x_reader = csv_reader(headerless_csv.splitlines(), delimiter=",")
    x_dict = get_positional_dict(header_row)
    x_believerdelta = believerdelta_shop()

    for row in x_reader:
        x_atomrow = atomrow_shop(x_idearef.dimens, "INSERT")
        for x_header in header_row:
            if header_index := x_dict.get(x_header):
                x_atomrow.__dict__[x_header] = row[header_index]

        for x_believeratom in x_atomrow.get_believeratoms():
            x_believerdelta.set_believeratom(x_believeratom)
    return x_believerdelta


def get_csv_belief_label_believer_name_metrics(
    headerless_csv: str, delimiter: str = None
) -> dict[BeliefLabel, dict[BelieverName, int]]:
    return get_csv_column1_column2_metrics(headerless_csv, delimiter)


def belief_label_believer_name_nested_csv_dict(
    headerless_csv: str, delimiter: str = None
) -> dict[BeliefLabel, dict[BelieverName, str]]:
    return create_l2nested_csv_dict(headerless_csv, delimiter)


def belief_build_from_df(
    br00000_df: DataFrame,
    br00001_df: DataFrame,
    br00002_df: DataFrame,
    br00003_df: DataFrame,
    br00004_df: DataFrame,
    br00005_df: DataFrame,
    x_fund_iota: float,
    x_respect_bit: float,
    x_penny: float,
    x_beliefs_dir: str,
) -> dict[BeliefLabel, BeliefUnit]:
    belief_hours_dict = _get_belief_hours_dict(br00003_df)
    belief_months_dict = _get_belief_months_dict(br00004_df)
    belief_weekdays_dict = _get_belief_weekdays_dict(br00005_df)

    beliefunit_dict = {}
    for index, row in br00000_df.iterrows():
        x_belief_label = row["belief_label"]
        x_timeline_config = {
            "c400_number": row["c400_number"],
            "hours_config": belief_hours_dict.get(x_belief_label),
            "months_config": belief_months_dict.get(x_belief_label),
            "monthday_distortion": row["monthday_distortion"],
            "timeline_label": row["timeline_label"],
            "weekdays_config": belief_weekdays_dict.get(x_belief_label),
            "yr1_jan1_offset": row["yr1_jan1_offset"],
        }
        x_timeline = timelineunit_shop(x_timeline_config)
        x_beliefunit = beliefunit_shop(
            belief_label=x_belief_label,
            belief_mstr_dir=x_beliefs_dir,
            timeline=x_timeline,
            knot=row["knot"],
            fund_iota=x_fund_iota,
            respect_bit=x_respect_bit,
            penny=x_penny,
            job_listen_rotations=row["job_listen_rotations"],
        )
        beliefunit_dict[x_beliefunit.belief_label] = x_beliefunit
        _add_budunits_from_df(x_beliefunit, br00001_df)
        _add_paypurchases_from_df(x_beliefunit, br00002_df)
    return beliefunit_dict


def _get_belief_hours_dict(br00003_df: DataFrame) -> dict[str, list[str, str]]:
    belief_hours_dict = {}
    for y_belief_label in br00003_df.belief_label.unique():
        query_str = f"belief_label == '{y_belief_label}'"
        x_hours_list = [
            [row["hour_label"], row["cumulative_minute"]]
            for index, row in br00003_df.query(query_str).iterrows()
        ]
        belief_hours_dict[y_belief_label] = x_hours_list
    return belief_hours_dict


def _get_belief_months_dict(br00004_df: DataFrame) -> dict[str, list[str, str]]:
    belief_months_dict = {}
    for y_belief_label in br00004_df.belief_label.unique():
        query_str = f"belief_label == '{y_belief_label}'"
        x_months_list = [
            [row["month_label"], row["cumulative_day"]]
            for index, row in br00004_df.query(query_str).iterrows()
        ]
        belief_months_dict[y_belief_label] = x_months_list
    return belief_months_dict


def _get_belief_weekdays_dict(br00005_df: DataFrame) -> dict[str, list[str, str]]:
    belief_weekdays_dict = {}
    for y_belief_label in br00005_df.belief_label.unique():
        query_str = f"belief_label == '{y_belief_label}'"
        x_weekdays_list = [
            row["weekday_label"]
            for index, row in br00005_df.query(query_str).iterrows()
        ]
        belief_weekdays_dict[y_belief_label] = x_weekdays_list
    return belief_weekdays_dict


def _add_budunits_from_df(x_beliefunit: BeliefUnit, br00001_df: DataFrame):
    query_str = f"belief_label == '{x_beliefunit.belief_label}'"
    for index, row in br00001_df.query(query_str).iterrows():
        x_beliefunit.add_budunit(
            believer_name=row["believer_name"],
            bud_time=row["bud_time"],
            quota=row["quota"],
            celldepth=if_nan_return_None(row["celldepth"]),
            allow_prev_to_offi_time_max_entry=True,
        )


def _add_paypurchases_from_df(x_beliefunit: BeliefUnit, br00002_df: DataFrame):
    query_str = f"belief_label == '{x_beliefunit.belief_label}'"
    for index, row in br00002_df.query(query_str).iterrows():
        x_beliefunit.add_paypurchase(
            believer_name=row["believer_name"],
            partner_name=row["partner_name"],
            tran_time=row["tran_time"],
            amount=row["amount"],
        )


def _add_time_offi_units_from_df(x_beliefunit: BeliefUnit, br00006_df: DataFrame):
    query_str = f"belief_label == '{x_beliefunit.belief_label}'"
    for index, row in br00006_df.query(query_str).iterrows():
        x_beliefunit.offi_times.add(row["offi_time"])
