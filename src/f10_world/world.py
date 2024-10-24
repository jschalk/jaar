from src.f00_instrument.file import create_file_path, dir_files
from src.f00_instrument.dict_tool import (
    get_empty_dict_if_none,
    get_0_if_None,
    get_empty_set_if_none,
)
from src.f01_road.finance_tran import TimeLinePoint, TimeConversion
from src.f01_road.road import (
    FiscalID,
    WorldID,
    TimeLineLabel,
    get_default_world_id,
    FaceID,
)
from src.f07_fiscal.fiscal import FiscalUnit
from src.f09_filter.filter import (
    FilterUnit,
    filterunit_shop,
    save_all_csvs_from_filterunit,
)
from dataclasses import dataclass
from os.path import exists as os_path_exists


def get_default_worlds_dir() -> str:
    return "src/f10_world/examples/worlds"


@dataclass
class WorldUnit:
    world_id: WorldID = None
    worlds_dir: str = None
    current_time: TimeLinePoint = None
    faces: dict[FaceID, FilterUnit] = None
    _faces_dir: dict[FaceID,] = None
    timeconversions: dict[TimeLineLabel, TimeConversion] = None
    _fiscalunits: set[FiscalID] = None

    def set_face_id(self, face_id: FaceID, x_filterunit: FilterUnit = None):
        if x_filterunit is None:
            x_filterunit = filterunit_shop(face_id)
        self.faces[face_id] = x_filterunit

    def face_id_exists(self, face_id: FaceID) -> bool:
        return self.faces.get(face_id) != None

    def get_face_id_filterunit(self, face_id: FaceID) -> FilterUnit:
        return self.faces.get(face_id)

    def del_face_id(self, face_id: FaceID):
        self.faces.pop(face_id)

    def del_all_face_id(self):
        self.faces = {}

    def face_ids_empty(self) -> bool:
        return self.faces == {}

    def save_face_files(self, face_id: FaceID):
        x_filterunit = self.get_face_id_filterunit(face_id)
        face_dir = get_face_dir(self._faces_dir, face_id)
        save_all_csvs_from_filterunit(face_dir, x_filterunit)

    def face_files_exists(self, face_id: FaceID) -> bool:
        face_dir = get_face_dir(self._faces_dir, face_id)
        return os_path_exists(face_dir)

    def _set_all_face_ids_from_dirs(self):
        self.del_all_face_id()
        for dir_name in dir_files(self._faces_dir, include_files=False).keys():
            self.set_face_id(dir_name)

    def get_timeconversions_dict(self) -> dict[TimeLineLabel, TimeConversion]:
        return self.timeconversions

    def get_dict(self) -> dict:
        return {
            "world_id": self.world_id,
            "current_time": self.current_time,
            "timeconversions": self.get_timeconversions_dict(),
            "faces": self.faces,
        }


def worldunit_shop(
    world_id: WorldID = None,
    worlds_dir: str = None,
    current_time: TimeLinePoint = None,
    timeconversions: dict[TimeLineLabel, TimeConversion] = None,
    faces: set[str] = None,
    _fiscalunits: set[FiscalID] = None,
) -> WorldUnit:
    if world_id is None:
        world_id = get_default_world_id()
    if worlds_dir is None:
        worlds_dir = get_default_worlds_dir()
    return WorldUnit(
        world_id=world_id,
        worlds_dir=worlds_dir,
        current_time=get_0_if_None(current_time),
        timeconversions=get_empty_dict_if_none(timeconversions),
        faces=get_empty_dict_if_none(faces),
        _faces_dir=create_file_path(worlds_dir, "faces"),
        _fiscalunits=get_empty_set_if_none(_fiscalunits),
    )


def init_fiscalunits_from_dirs(x_dirs: list[str]) -> list[FiscalUnit]:
    return []


def get_face_dir(faces_dir: str, face_id: FaceID) -> str:
    return create_file_path(faces_dir, face_id)
