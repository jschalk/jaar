from src.a00_data_toolbox.file_toolbox import create_path
from src.a19_world_logic.world import WorldID


class LobbyID(str):
    pass


def create_lobby_dir_path(lobby_mstr_dir: str, lobby_id: LobbyID) -> str:
    """Returns path: lobby_mstr_dir\\lobbys\\lobby_id"""
    lobbys_dir = create_path(lobby_mstr_dir, "lobbys")
    return create_path(lobbys_dir, lobby_id)


def create_world_dir_path(
    lobby_mstr_dir: str, lobby_id: LobbyID, world_id: WorldID
) -> str:
    """Returns path: lobby_mstr_dir\\lobbys\\lobby_id\\worlds\\world_id"""
    lobbys_dir = create_path(lobby_mstr_dir, "lobbys")
    lobby_dir = create_path(lobbys_dir, lobby_id)
    worlds_dir = create_path(lobby_dir, "worlds")
    return create_path(worlds_dir, world_id)


def create_vow_mstr_dir_path(
    lobby_mstr_dir: str, lobby_id: LobbyID, world_id: WorldID
) -> str:
    """Returns path: lobby_mstr_dir\\lobbys\\lobby_id\\worlds\\world_id\\vow_mstr_dir"""
    lobbys_dir = create_path(lobby_mstr_dir, "lobbys")
    lobby_dir = create_path(lobbys_dir, lobby_id)
    worlds_dir = create_path(lobby_dir, "worlds")
    world_id_dir = create_path(worlds_dir, world_id)
    return create_path(world_id_dir, "vow_mstr_dir")
