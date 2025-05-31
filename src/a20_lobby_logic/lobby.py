from dataclasses import dataclass
from src.a01_term_logic.way import WorldID
from src.a09_pack_logic.pack import PackUnit
from src.a19_world_logic.world import WorldUnit


@dataclass
class LobbyUnit:
    lobby_id: str = None
    option_packs: list[PackUnit] = None
    selected_pack: PackUnit = None
    worlds: list[WorldID] = None


def lobbyunit_shop(
    lobby_id: str,
    option_packs: list[PackUnit] = None,
    selected_pack: PackUnit = None,
    worlds: list[WorldID] = None,
) -> LobbyUnit:
    return LobbyUnit(lobby_id=lobby_id)
