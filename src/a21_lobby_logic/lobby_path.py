from src.a00_data_toolbox.file_toolbox import create_path
from src.a20_world_logic.world import WorldID


class LobbyID(str):
    pass


def create_lobby_dir_path(lobby_mstr_dir: str, lobby_id: LobbyID) -> str:
    """Returns path: lobby_mstr_dir\\lobbys\\lobby_id"""
    lobbys_dir = create_path(lobby_mstr_dir, "lobbys")
    return create_path(lobbys_dir, lobby_id)


def create_world_dir_path(
    lobby_mstr_dir: str, lobby_id: LobbyID, world_name: WorldID
) -> str:
    """Returns path: lobby_mstr_dir\\lobbys\\lobby_id\\worlds\\world_name"""
    lobbys_dir = create_path(lobby_mstr_dir, "lobbys")
    lobby_dir = create_path(lobbys_dir, lobby_id)
    worlds_dir = create_path(lobby_dir, "worlds")
    return create_path(worlds_dir, world_name)


def create_belief_mstr_dir_path(
    lobby_mstr_dir: str, lobby_id: LobbyID, world_name: WorldID
) -> str:
    """Returns path: lobby_mstr_dir\\lobbys\\lobby_id\\worlds\\world_name\\belief_mstr_dir"""
    lobbys_dir = create_path(lobby_mstr_dir, "lobbys")
    lobby_dir = create_path(lobbys_dir, lobby_id)
    worlds_dir = create_path(lobby_dir, "worlds")
    world_name_dir = create_path(worlds_dir, world_name)
    return create_path(world_name_dir, "belief_mstr_dir")
