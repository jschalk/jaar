from dataclasses import dataclass
from src.a09_pack_logic.pack import PackUnit
from src.a20_fis_logic.fis import FisID, FisUnit


@dataclass
class LobbyUnit:
    lobby_id: str = None
    option_packs: list[PackUnit] = None
    selected_pack: PackUnit = None
    fiss: list[FisID] = None


def lobbyunit_shop(
    lobby_id: str,
    option_packs: list[PackUnit] = None,
    selected_pack: PackUnit = None,
    fiss: list[FisID] = None,
) -> LobbyUnit:
    return LobbyUnit(lobby_id=lobby_id)
