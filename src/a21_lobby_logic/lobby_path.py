from src.a00_data_toolbox.file_toolbox import create_path
from src.a20_fis_logic.fis import FisID


class LobbyID(str):
    pass


def create_lobby_dir_path(lobby_mstr_dir: str, lobby_id: LobbyID) -> str:
    """Returns path: lobby_mstr_dir\\lobbys\\lobby_id"""
    lobbys_dir = create_path(lobby_mstr_dir, "lobbys")
    return create_path(lobbys_dir, lobby_id)


def create_fis_dir_path(lobby_mstr_dir: str, lobby_id: LobbyID, fis_id: FisID) -> str:
    """Returns path: lobby_mstr_dir\\lobbys\\lobby_id\\fiss\\fis_id"""
    lobbys_dir = create_path(lobby_mstr_dir, "lobbys")
    lobby_dir = create_path(lobbys_dir, lobby_id)
    fiss_dir = create_path(lobby_dir, "fiss")
    return create_path(fiss_dir, fis_id)


def create_bank_mstr_dir_path(
    lobby_mstr_dir: str, lobby_id: LobbyID, fis_id: FisID
) -> str:
    """Returns path: lobby_mstr_dir\\lobbys\\lobby_id\\fiss\\fis_id\\bank_mstr_dir"""
    lobbys_dir = create_path(lobby_mstr_dir, "lobbys")
    lobby_dir = create_path(lobbys_dir, lobby_id)
    fiss_dir = create_path(lobby_dir, "fiss")
    fis_id_dir = create_path(fiss_dir, fis_id)
    return create_path(fis_id_dir, "bank_mstr_dir")
