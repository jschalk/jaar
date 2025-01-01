from src.f00_instrument.file import save_file, get_dir_file_strs, create_path
from src.f08_pidgin.pidgin import (
    PidginUnit,
    pidginunit_shop,
    AcctMap,
    GroupMap,
    IdeaMap,
    RoadMap,
)
from src.f09_brick.pandas_tool import get_ordered_csv, open_csv
from pandas import DataFrame
from os.path import exists as os_path_exists


def get_map_acct_dt_columns() -> list[str]:
    return [
        "face_name",
        "event_int",
        "otx_bridge",
        "inx_bridge",
        "unknown_word",
        "otx_name",
        "inx_name",
    ]


def get_map_group_dt_columns() -> list[str]:
    return [
        "face_name",
        "event_int",
        "otx_bridge",
        "inx_bridge",
        "unknown_word",
        "otx_label",
        "inx_label",
    ]


def get_map_idea_dt_columns() -> list[str]:
    return [
        "face_name",
        "event_int",
        "otx_bridge",
        "inx_bridge",
        "unknown_word",
        "otx_idea",
        "inx_idea",
    ]


def get_map_road_dt_columns() -> list[str]:
    return [
        "face_name",
        "event_int",
        "otx_bridge",
        "inx_bridge",
        "unknown_word",
        "otx_road",
        "inx_road",
    ]


def create_map_acct_dt(x_map: AcctMap) -> DataFrame:
    x_rows_list = [
        {
            "event_int": x_map.event_int,
            "face_name": x_map.face_name,
            "otx_bridge": x_map.otx_bridge,
            "inx_bridge": x_map.inx_bridge,
            "unknown_word": x_map.unknown_word,
            "otx_name": otx_value,
            "inx_name": inx_value,
        }
        for otx_value, inx_value in x_map.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_map_acct_dt_columns())


def create_map_group_dt(x_map: GroupMap) -> DataFrame:
    x_rows_list = [
        {
            "event_int": x_map.event_int,
            "face_name": x_map.face_name,
            "otx_bridge": x_map.otx_bridge,
            "inx_bridge": x_map.inx_bridge,
            "unknown_word": x_map.unknown_word,
            "otx_label": otx_value,
            "inx_label": inx_value,
        }
        for otx_value, inx_value in x_map.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_map_group_dt_columns())


def create_map_idea_dt(x_map: IdeaMap) -> DataFrame:
    x_rows_list = [
        {
            "event_int": x_map.event_int,
            "face_name": x_map.face_name,
            "otx_bridge": x_map.otx_bridge,
            "inx_bridge": x_map.inx_bridge,
            "unknown_word": x_map.unknown_word,
            "otx_idea": otx_value,
            "inx_idea": inx_value,
        }
        for otx_value, inx_value in x_map.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_map_idea_dt_columns())


def create_map_road_dt(x_map: RoadMap) -> DataFrame:
    x_rows_list = [
        {
            "event_int": x_map.event_int,
            "face_name": x_map.face_name,
            "otx_bridge": x_map.otx_bridge,
            "inx_bridge": x_map.inx_bridge,
            "unknown_word": x_map.unknown_word,
            "otx_road": otx_value,
            "inx_road": inx_value,
        }
        for otx_value, inx_value in x_map.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_map_road_dt_columns())


def save_all_csvs_from_pidginunit(x_dir: str, x_pidginunit: PidginUnit):
    _save_map_acct_csv(x_dir, x_pidginunit.acctmap)
    _save_map_group_csv(x_dir, x_pidginunit.groupmap)
    _save_map_idea_csv(x_dir, x_pidginunit.ideamap)
    _save_map_road_csv(x_dir, x_pidginunit.roadmap)


def _save_map_acct_csv(x_dir: str, acctmap: AcctMap):
    x_dt = create_map_acct_dt(acctmap)
    save_file(x_dir, "name.csv", get_ordered_csv(x_dt))


def _save_map_group_csv(x_dir: str, groupmap: GroupMap):
    x_dt = create_map_group_dt(groupmap)
    save_file(x_dir, "label.csv", get_ordered_csv(x_dt))


def _save_map_idea_csv(x_dir: str, ideamap: IdeaMap):
    x_dt = create_map_idea_dt(ideamap)
    save_file(x_dir, "idea.csv", get_ordered_csv(x_dt))


def _save_map_road_csv(x_dir: str, roadmap: RoadMap):
    x_dt = create_map_road_dt(roadmap)
    save_file(x_dir, "road.csv", get_ordered_csv(x_dt))


def _load_acctmap_from_csv(x_dir, x_acctmap: AcctMap) -> AcctMap:
    name_filename = "name.csv"
    if os_path_exists(create_path(x_dir, name_filename)):
        otx2inx_dt = open_csv(x_dir, name_filename)
        for table_row in otx2inx_dt.to_dict("records"):
            otx_value = table_row.get("otx_name")
            inx_value = table_row.get("inx_name")
            if x_acctmap.otx2inx_exists(otx_value, inx_value) is False:
                x_acctmap.set_otx2inx(otx_value, inx_value)
    return x_acctmap


def _load_groupmap_from_csv(x_dir, x_groupmap: GroupMap) -> GroupMap:
    label_filename = "label.csv"
    if os_path_exists(create_path(x_dir, label_filename)):
        otx2inx_dt = open_csv(x_dir, label_filename)
        for table_row in otx2inx_dt.to_dict("records"):
            otx_value = table_row.get("otx_label")
            inx_value = table_row.get("inx_label")
            if x_groupmap.otx2inx_exists(otx_value, inx_value) is False:
                x_groupmap.set_otx2inx(otx_value, inx_value)
    return x_groupmap


def _load_ideamap_from_csv(x_dir, x_ideamap: IdeaMap) -> IdeaMap:
    idea_filename = "idea.csv"
    if os_path_exists(create_path(x_dir, idea_filename)):
        otx2inx_dt = open_csv(x_dir, "idea.csv")
        for table_row in otx2inx_dt.to_dict("records"):
            otx_value = table_row.get("otx_idea")
            inx_value = table_row.get("inx_idea")
            if x_ideamap.otx2inx_exists(otx_value, inx_value) is False:
                x_ideamap.set_otx2inx(otx_value, inx_value)
    return x_ideamap


def _load_roadmap_from_csv(x_dir, x_roadmap: RoadMap) -> RoadMap:
    road_filename = "road.csv"
    if os_path_exists(create_path(x_dir, road_filename)):
        otx2inx_dt = open_csv(x_dir, "road.csv")
        for table_row in otx2inx_dt.to_dict("records"):
            otx_value = table_row.get("otx_road")
            inx_value = table_row.get("inx_road")
            if x_roadmap.otx2inx_exists(otx_value, inx_value) is False:
                x_roadmap.set_otx2inx(otx_value, inx_value)
    return x_roadmap


def create_dir_valid_empty_pidginunit(x_dir: str) -> PidginUnit:
    face_name_set = set()
    event_int_set = set()
    unknown_word_set = set()
    otx_bridge_set = set()
    inx_bridge_set = set()
    for x_filename in get_dir_file_strs(x_dir).keys():
        x_dt = open_csv(x_dir, x_filename)
        face_name_set.update(x_dt.face_name.unique())
        event_int_set.update(x_dt.event_int.unique())
        unknown_word_set.update(x_dt.unknown_word.unique())
        otx_bridge_set.update(x_dt.otx_bridge.unique())
        inx_bridge_set.update(x_dt.inx_bridge.unique())

    if len(face_name_set) == 1:
        face_name = face_name_set.pop()
    if len(event_int_set) == 1:
        event_int = event_int_set.pop()
    if len(unknown_word_set) == 1:
        unknown_word = unknown_word_set.pop()
    if len(otx_bridge_set) == 1:
        otx_bridge = otx_bridge_set.pop()
    if len(inx_bridge_set) == 1:
        inx_bridge = inx_bridge_set.pop()

    return pidginunit_shop(
        face_name=face_name,
        event_int=event_int,
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_word=unknown_word,
    )


def init_pidginunit_from_dir(x_dir: str) -> PidginUnit:
    x_pidginunit = create_dir_valid_empty_pidginunit(x_dir)
    _load_acctmap_from_csv(x_dir, x_pidginunit.acctmap)
    _load_groupmap_from_csv(x_dir, x_pidginunit.groupmap)
    _load_ideamap_from_csv(x_dir, x_pidginunit.ideamap)
    _load_roadmap_from_csv(x_dir, x_pidginunit.roadmap)
    x_pidginunit.roadmap.ideamap = x_pidginunit.ideamap
    return x_pidginunit
