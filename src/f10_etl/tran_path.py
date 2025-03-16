from src.f00_instrument.file import create_path
from src.f01_road.road import OwnerName, TitleUnit

STANCE0001_FILENAME = "stance0001.xlsx"


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
