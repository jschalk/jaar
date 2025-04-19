from src.a00_data_toolboxs.file_toolbox import create_path
from src.a01_word_logic.road import OwnerName, TitleUnit


class LobbyID(str):
    pass


def lobbys_str() -> str:
    return "lobbys"


def lobby_id_str() -> str:
    return "lobby_id"


def create_lobby_dir_path(lobbys_mstr_dir: str, lobby_id: LobbyID) -> str:
    """Returns path: lobby_mstr_dir\\lobbys\\lobby_id"""
    lobbys_dir = create_path(lobbys_mstr_dir, "lobbys")
    return create_path(lobbys_dir, lobby_id)
