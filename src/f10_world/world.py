from src.f00_instrument.file import (
    set_dir,
    create_file_path,
    get_dir_file_strs,
    delete_dir,
)
from src.f00_instrument.dict_toolbox import (
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
from src.f09_brick.filter_toolbox import (
    save_all_csvs_from_filterunit,
    init_filterunit_from_dir,
)
from src.f09_brick.brick_models import Base as brick_modelsBase
from src.f08_filter.filter import FilterUnit, filterunit_shop
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection
from sqlalchemy import create_engine, Engine
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
    _world_dir: str = None
    _jungle_dir: str = None
    _zoo_dir: str = None

    def set_face_id(self, face_id: FaceID, x_filterunit: FilterUnit = None):
        if x_filterunit is None:
            x_filterunit = filterunit_shop(face_id)
        self.faces[face_id] = x_filterunit

    def face_id_exists(self, face_id: FaceID) -> bool:
        return self.faces.get(face_id) != None

    def get_filterunit(self, face_id: FaceID) -> FilterUnit:
        return self.faces.get(face_id)

    def del_face_id(self, face_id: FaceID):
        self.faces.pop(face_id)

    def del_all_face_id(self):
        self.faces = {}

    def face_ids_empty(self) -> bool:
        return self.faces == {}

    def _face_dir(self, face_id: FaceID) -> str:
        return create_file_path(self._faces_dir, face_id)

    def save_filterunit_files(self, face_id: FaceID):
        x_filterunit = self.get_filterunit(face_id)
        save_all_csvs_from_filterunit(self._face_dir(face_id), x_filterunit)

    def face_dir_exists(self, face_id: FaceID) -> bool:
        return os_path_exists(self._face_dir(face_id))

    def _set_all_face_ids_from_dirs(self):
        self.del_all_face_id()
        for dir_name in get_dir_file_strs(self._faces_dir, include_files=False).keys():
            self.set_face_id(dir_name)

    def _delete_filterunit_dir(self, face_id: FaceID):
        delete_dir(self._face_dir(face_id))

    # def get_db_path(self) -> str:
    #     return create_file_path(self._world_dir, "wrd.db")

    # def _create_wrd_db(self):
    #     engine = create_engine(f"sqlite:///{self.get_db_path()}", echo=False)
    #     brick_modelsBase.metadata.create_all(engine)
    #     engine.dispose()

    # def db_exists(self) -> bool:
    #     return os_path_exists(self.get_db_path())

    # def get_db_engine(self) -> Engine:
    #     if self.db_exists() is False:
    #         self._create_wrd_db()
    #     return create_engine(f"sqlite:///{self.get_db_path()}", echo=False)

    def _set_world_dirs(self):
        self._world_dir = create_file_path(self.worlds_dir, self.world_id)
        self._faces_dir = create_file_path(self._world_dir, "faces")
        self._jungle_dir = create_file_path(self._world_dir, "jungle")
        self._zoo_dir = create_file_path(self._world_dir, "zoo")
        if not os_path_exists(self._world_dir):
            set_dir(self._world_dir)
        if not os_path_exists(self._faces_dir):
            set_dir(self._faces_dir)
        if not os_path_exists(self._jungle_dir):
            set_dir(self._jungle_dir)
        if not os_path_exists(self._zoo_dir):
            set_dir(self._zoo_dir)

    def get_timeconversions_dict(self) -> dict[TimeLineLabel, TimeConversion]:
        return self.timeconversions

    def load_filterunit_from_files(self, face_id: FaceID):
        x_filterunit = init_filterunit_from_dir(self._face_dir(face_id))
        self.set_face_id(face_id, x_filterunit)

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
    in_memory_db: bool = None,
) -> WorldUnit:
    if world_id is None:
        world_id = get_default_world_id()
    if worlds_dir is None:
        worlds_dir = get_default_worlds_dir()
    x_worldunit = WorldUnit(
        world_id=world_id,
        worlds_dir=worlds_dir,
        current_time=get_0_if_None(current_time),
        timeconversions=get_empty_dict_if_none(timeconversions),
        faces=get_empty_dict_if_none(faces),
        _faces_dir=create_file_path(worlds_dir, "faces"),
        _fiscalunits=get_empty_set_if_none(_fiscalunits),
    )
    x_worldunit._set_world_dirs()
    return x_worldunit


def init_fiscalunits_from_dirs(x_dirs: list[str]) -> list[FiscalUnit]:
    return []
