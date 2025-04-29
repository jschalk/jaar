from src.a00_data_toolbox.file_toolbox import create_path
from src.a01_word_logic.road import OwnerName, TagUnit, FaceName, EventInt


YELL_PIDGIN_FILENAME = "pidgin.xlsx"
STANCE0001_FILENAME = "stance0001.xlsx"


def create_yell_pidgin_path(yell_dir: str) -> str:
    """Returns path: yell_dir\\pidgin.xlsx"""
    return create_path(yell_dir, "pidgin.xlsx")


def create_syntax_otx_pidgin_path(syntax_otz_dir: str, face_name: FaceName) -> str:
    """Returns path: syntax_otz_dir\\face_name\\pidgin.xlsx"""
    otz_face_dir = create_path(syntax_otz_dir, face_name)
    return create_path(otz_face_dir, "pidgin.xlsx")


def create_otx_event_pidgin_path(
    syntax_otz_dir: str, face_name: FaceName, event_int: EventInt
) -> str:
    """Returns path: syntax_otz_dir\\face_name\\event_int\\pidgin.xlsx"""
    otz_face_dir = create_path(syntax_otz_dir, face_name)
    otz_event_int_dir = create_path(otz_face_dir, event_int)
    return create_path(otz_event_int_dir, "pidgin.xlsx")


def create_stances_dir_path(fisc_mstr_dir: str) -> str:
    """Returns path: fisc_mstr_dir\\stances"""
    return create_path(fisc_mstr_dir, "stances")


def create_stances_owner_dir_path(fisc_mstr_dir: str, owner_name: OwnerName) -> str:
    """Returns path: fisc_mstr_dir\\stances\\owner_name"""
    stances_dir = create_path(fisc_mstr_dir, "stances")
    return create_path(stances_dir, owner_name)


def create_stance0001_path(fisc_mstr_dir: str) -> str:
    """Returns path: fisc_mstr_dir\\stances\\stance0001.xlsx"""
    stances_dir = create_path(fisc_mstr_dir, "stances")
    return create_path(stances_dir, "stance0001.xlsx")
