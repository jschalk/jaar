from src.a09_pack_logic.pack import PackUnit
from src.f12_world.world import WorldUnit
from dataclasses import dataclass


@dataclass
class LobbyUnit:
    lobby_id: str = None
    option_packs: list[PackUnit] = None
    selected_pack: PackUnit = None
    worlds: list[WorldUnit] = None


def lobbyunit_shop(
    lobby_id: str,
    option_packs: list[PackUnit] = None,
    selected_pack: PackUnit = None,
    worlds: list[WorldUnit] = None,
) -> LobbyUnit:
    return LobbyUnit(lobby_id=lobby_id)
