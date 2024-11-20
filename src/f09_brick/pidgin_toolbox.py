from src.f00_instrument.file import save_file, get_dir_file_strs
from src.f08_pidgin.pidgin import (
    PidginUnit,
    pidginunit_shop,
    AcctBridge,
    GroupBridge,
    NodeBridge,
    RoadBridge,
)
from src.f09_brick.pandas_tool import get_ordered_csv, open_csv
from pandas import DataFrame


def get_bridge_acct_dt_columns() -> list[str]:
    return [
        "face_id",
        "otx_wall",
        "inx_wall",
        "unknown_word",
        "otx_acct_id",
        "inx_acct_id",
    ]


def get_bridge_group_dt_columns() -> list[str]:
    return [
        "face_id",
        "otx_wall",
        "inx_wall",
        "unknown_word",
        "otx_group_id",
        "inx_group_id",
    ]


def get_bridge_node_dt_columns() -> list[str]:
    return [
        "face_id",
        "otx_wall",
        "inx_wall",
        "unknown_word",
        "otx_node",
        "inx_node",
    ]


def get_bridge_road_dt_columns() -> list[str]:
    return [
        "face_id",
        "otx_wall",
        "inx_wall",
        "unknown_word",
        "otx_road",
        "inx_road",
    ]


def get_nub_label_columns() -> list[str]:
    return [
        "face_id",
        "otx_wall",
        "inx_wall",
        "unknown_word",
        "otx_label",
        "inx_label",
    ]


def create_bridge_acct_dt(x_bridge: AcctBridge) -> DataFrame:
    x_rows_list = [
        {
            "face_id": x_bridge.face_id,
            "otx_wall": x_bridge.otx_wall,
            "inx_wall": x_bridge.inx_wall,
            "unknown_word": x_bridge.unknown_word,
            "otx_acct_id": otx_value,
            "inx_acct_id": inx_value,
        }
        for otx_value, inx_value in x_bridge.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_bridge_acct_dt_columns())


def create_bridge_group_dt(x_bridge: GroupBridge) -> DataFrame:
    x_rows_list = [
        {
            "face_id": x_bridge.face_id,
            "otx_wall": x_bridge.otx_wall,
            "inx_wall": x_bridge.inx_wall,
            "unknown_word": x_bridge.unknown_word,
            "otx_group_id": otx_value,
            "inx_group_id": inx_value,
        }
        for otx_value, inx_value in x_bridge.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_bridge_group_dt_columns())


def create_bridge_node_dt(x_bridge: NodeBridge) -> DataFrame:
    x_rows_list = [
        {
            "face_id": x_bridge.face_id,
            "otx_wall": x_bridge.otx_wall,
            "inx_wall": x_bridge.inx_wall,
            "unknown_word": x_bridge.unknown_word,
            "otx_node": otx_value,
            "inx_node": inx_value,
        }
        for otx_value, inx_value in x_bridge.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_bridge_node_dt_columns())


def create_bridge_road_dt(x_bridge: RoadBridge) -> DataFrame:
    x_rows_list = [
        {
            "face_id": x_bridge.face_id,
            "otx_wall": x_bridge.otx_wall,
            "inx_wall": x_bridge.inx_wall,
            "unknown_word": x_bridge.unknown_word,
            "otx_road": otx_value,
            "inx_road": inx_value,
        }
        for otx_value, inx_value in x_bridge.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_bridge_road_dt_columns())


def create_nub_label_dt(x_roadbridge: RoadBridge) -> DataFrame:
    x_rows_list = [
        {
            "face_id": x_roadbridge.face_id,
            "otx_wall": x_roadbridge.otx_wall,
            "inx_wall": x_roadbridge.inx_wall,
            "unknown_word": x_roadbridge.unknown_word,
            "otx_label": otx_value,
            "inx_label": inx_value,
        }
        for otx_value, inx_value in x_roadbridge.nub_label.items()
    ]
    return DataFrame(x_rows_list, columns=get_nub_label_columns())


def save_all_csvs_from_pidginunit(x_dir: str, x_pidginunit: PidginUnit):
    _save_bridge_acct_csv(x_dir, x_pidginunit.acctbridge)
    _save_bridge_group_csv(x_dir, x_pidginunit.groupbridge)
    _save_bridge_node_csv(x_dir, x_pidginunit.nodebridge)
    _save_bridge_road_csv(x_dir, x_pidginunit.roadbridge)
    _save_nub_label_csv(x_dir, x_pidginunit.roadbridge)


def _save_bridge_acct_csv(x_dir: str, acctbridge: AcctBridge):
    x_dt = create_bridge_acct_dt(acctbridge)
    save_file(x_dir, "acct.csv", get_ordered_csv(x_dt))


def _save_bridge_group_csv(x_dir: str, groupbridge: GroupBridge):
    x_dt = create_bridge_group_dt(groupbridge)
    save_file(x_dir, "group.csv", get_ordered_csv(x_dt))


def _save_bridge_node_csv(x_dir: str, nodebridge: NodeBridge):
    x_dt = create_bridge_node_dt(nodebridge)
    save_file(x_dir, "node.csv", get_ordered_csv(x_dt))


def _save_bridge_road_csv(x_dir: str, roadbridge: RoadBridge):
    x_dt = create_bridge_road_dt(roadbridge)
    save_file(x_dir, "road.csv", get_ordered_csv(x_dt))


def _save_nub_label_csv(x_dir, roadbridge: RoadBridge):
    x_nub_label_dt = create_nub_label_dt(roadbridge)
    save_file(x_dir, "nub_label.csv", get_ordered_csv(x_nub_label_dt))


def _load_acctbridge_from_csv(x_dir, x_acctbridge: AcctBridge) -> AcctBridge:
    otx2inx_dt = open_csv(x_dir, "acct.csv")
    for table_row in otx2inx_dt.to_dict("records"):
        otx_value = table_row.get("otx_acct_id")
        inx_value = table_row.get("inx_acct_id")
        if x_acctbridge.otx2inx_exists(otx_value, inx_value) is False:
            x_acctbridge.set_otx2inx(otx_value, inx_value)
    return x_acctbridge


def _load_groupbridge_from_csv(x_dir, x_groupbridge: GroupBridge) -> GroupBridge:
    otx2inx_dt = open_csv(x_dir, "group.csv")
    for table_row in otx2inx_dt.to_dict("records"):
        otx_value = table_row.get("otx_group_id")
        inx_value = table_row.get("inx_group_id")
        if x_groupbridge.otx2inx_exists(otx_value, inx_value) is False:
            x_groupbridge.set_otx2inx(otx_value, inx_value)
    return x_groupbridge


def _load_nodebridge_from_csv(x_dir, x_nodebridge: NodeBridge) -> NodeBridge:
    otx2inx_dt = open_csv(x_dir, "node.csv")
    for table_row in otx2inx_dt.to_dict("records"):
        otx_value = table_row.get("otx_node")
        inx_value = table_row.get("inx_node")
        if x_nodebridge.otx2inx_exists(otx_value, inx_value) is False:
            x_nodebridge.set_otx2inx(otx_value, inx_value)
    return x_nodebridge


def _load_roadbridge_from_csv(x_dir, x_roadbridge: RoadBridge) -> RoadBridge:
    otx2inx_dt = open_csv(x_dir, "road.csv")
    for table_row in otx2inx_dt.to_dict("records"):
        otx_value = table_row.get("otx_road")
        inx_value = table_row.get("inx_road")
        if x_roadbridge.otx2inx_exists(otx_value, inx_value) is False:
            x_roadbridge.set_otx2inx(otx_value, inx_value)
    return x_roadbridge


def _load_nub_label_from_csv(x_dir, x_roadbridge: RoadBridge) -> RoadBridge:
    nub_label_dt = open_csv(x_dir, "nub_label.csv")
    for table_row in nub_label_dt.to_dict("records"):
        otx_word_value = table_row.get("otx_label")
        inx_word_value = table_row.get("inx_label")
        if x_roadbridge.nub_label_exists(otx_word_value, inx_word_value) is False:
            x_roadbridge.set_nub_label(otx_word_value, inx_word_value)
    return x_roadbridge


def create_dir_valid_empty_pidginunit(x_dir: str) -> PidginUnit:
    face_id_set = set()
    unknown_word_set = set()
    otx_wall_set = set()
    inx_wall_set = set()
    for x_filename in get_dir_file_strs(x_dir).keys():
        x_dt = open_csv(x_dir, x_filename)
        face_id_set.update(x_dt.face_id.unique())
        unknown_word_set.update(x_dt.unknown_word.unique())
        otx_wall_set.update(x_dt.otx_wall.unique())
        inx_wall_set.update(x_dt.inx_wall.unique())

    if len(face_id_set) == 1:
        x_face_id = face_id_set.pop()
    if len(unknown_word_set) == 1:
        x_unknown_word = unknown_word_set.pop()
    if len(otx_wall_set) == 1:
        x_otx_wall = otx_wall_set.pop()
    if len(inx_wall_set) == 1:
        x_inx_wall = inx_wall_set.pop()

    # if (
    #     face_id_set != set()
    #     or unknown_word_set != set()
    #     or otx_wall_set != set()
    #     or inx_wall_set != set()
    # ):
    #     raise Exception(
    #         f"{face_id_set=} {unknown_word_set=}  {otx_wall_set=} {inx_wall_set=}"
    #     )

    return pidginunit_shop(
        x_face_id=x_face_id,
        x_otx_wall=x_otx_wall,
        x_inx_wall=x_inx_wall,
        x_unknown_word=x_unknown_word,
    )


def init_pidginunit_from_dir(x_dir: str) -> PidginUnit:
    x_pidginunit = create_dir_valid_empty_pidginunit(x_dir)
    _load_acctbridge_from_csv(x_dir, x_pidginunit.acctbridge)
    _load_groupbridge_from_csv(x_dir, x_pidginunit.groupbridge)
    _load_nodebridge_from_csv(x_dir, x_pidginunit.nodebridge)
    _load_roadbridge_from_csv(x_dir, x_pidginunit.roadbridge)
    _load_nub_label_from_csv(x_dir, x_pidginunit.roadbridge)
    return x_pidginunit
