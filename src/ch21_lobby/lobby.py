from dataclasses import dataclass
from src.ch10_lesson.lesson_main import LessonUnit
from src.ch20_world_logic.world import WorldName


@dataclass
class LobbyUnit:
    lobby_id: str = None
    option_lessons: list[LessonUnit] = None
    selected_lesson: LessonUnit = None
    worlds: list[WorldName] = None


def lobbyunit_shop(
    lobby_id: str,
    option_lessons: list[LessonUnit] = None,
    selected_lesson: LessonUnit = None,
    worlds: list[WorldName] = None,
) -> LobbyUnit:
    return LobbyUnit(lobby_id=lobby_id)
