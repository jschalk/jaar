from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import (
    create_path,
    delete_dir,
    get_dict_from_json,
    get_dir_file_strs,
    get_integer_filenames,
    get_json_filename,
    get_max_file_number,
    open_json,
    save_json,
)
from src.ch02_allot.allot import default_grain_num_if_None, validate_pool_num
from src.ch04_rope.rope import validate_labelterm
from src.ch07_belief_logic.belief_main import (
    BeliefUnit,
    beliefunit_shop,
    get_beliefunit_from_dict,
)
from src.ch08_belief_atom.atom_main import (
    BeliefAtom,
    get_beliefatom_from_dict,
    modify_belief_with_beliefatom,
)
from src.ch09_belief_lesson._ref.ch09_path import (
    create_atoms_dir_path,
    create_gut_path,
    create_lessons_dir_path,
)
from src.ch09_belief_lesson._ref.ch09_semantic_types import (
    BeliefName,
    KnotTerm,
    LabelTerm,
    MomentLabel,
    RopeTerm,
    default_knot_if_None,
)
from src.ch09_belief_lesson.lesson_main import (
    LessonUnit,
    create_lessonunit_from_files,
    get_init_lesson_id_if_None,
    init_lesson_id,
    lessonunit_shop,
)


def save_belief_file(
    dest_dir: str, filename: str = None, beliefunit: BeliefUnit = None
):
    save_json(dest_dir, filename, beliefunit.to_dict())


def open_belief_file(dest_dir: str, filename: str = None) -> BeliefUnit:
    if os_path_exists(create_path(dest_dir, filename)):
        return get_beliefunit_from_dict(open_json(dest_dir, filename))


def save_gut_file(moment_mstr_dir: str, beliefunit: BeliefUnit):
    gut_path = create_gut_path(
        moment_mstr_dir, beliefunit.moment_label, beliefunit.belief_name
    )
    save_belief_file(gut_path, None, beliefunit)


def open_gut_file(
    moment_mstr_dir: str, moment_label: str, belief_name: BeliefName
) -> BeliefUnit:
    gut_path = create_gut_path(moment_mstr_dir, moment_label, belief_name)
    return open_belief_file(gut_path)


def gut_file_exists(
    moment_mstr_dir: str, moment_label: str, belief_name: BeliefName
) -> bool:
    gut_path = create_gut_path(moment_mstr_dir, moment_label, belief_name)
    return os_path_exists(gut_path)


class SaveLessonFileException(Exception):
    pass


class LessonFileMissingException(Exception):
    pass


@dataclass
class LessonFileHandler:
    belief_name: BeliefName = None
    moment_mstr_dir: str = None
    moment_label: MomentLabel = None
    knot: KnotTerm = None
    fund_pool: float = None
    fund_grain: float = None
    respect_grain: float = None
    mana_grain: float = None
    atoms_dir: str = None
    lessons_dir: str = None

    def set_dir_attrs(self):
        mstr_dir = self.moment_mstr_dir
        moment_label = self.moment_label
        belief_name = self.belief_name
        self.atoms_dir = create_atoms_dir_path(mstr_dir, moment_label, belief_name)
        self.lessons_dir = create_lessons_dir_path(mstr_dir, moment_label, belief_name)

    def default_gut_belief(self) -> BeliefUnit:
        x_beliefunit = beliefunit_shop(
            belief_name=self.belief_name,
            moment_label=self.moment_label,
            knot=self.knot,
            fund_pool=self.fund_pool,
            fund_grain=self.fund_grain,
            respect_grain=self.respect_grain,
            mana_grain=self.mana_grain,
        )
        x_beliefunit.last_lesson_id = init_lesson_id()
        return x_beliefunit

    # lesson methods
    def get_max_atom_file_number(self) -> int:
        return get_max_file_number(self.atoms_dir)

    def _get_next_atom_file_number(self) -> int:
        max_file_number = self.get_max_atom_file_number()
        return 0 if max_file_number is None else max_file_number + 1

    def atom_filename(self, atom_number: int) -> str:
        return f"{atom_number}.json"

    def atom_file_path(self, atom_number: int) -> str:
        "Returns path: _atoms_dir/atom_number.json"
        return create_path(self.atoms_dir, self.atom_filename(atom_number))

    def _save_valid_atom_file(self, x_atom: BeliefAtom, file_number: int):
        save_json(
            self.atoms_dir,
            self.atom_filename(file_number),
            x_atom.to_dict(),
            replace=False,
        )
        return file_number

    def save_atom_file(self, x_atom: BeliefAtom):
        x_atom_filename = self._get_next_atom_file_number()
        return self._save_valid_atom_file(x_atom, x_atom_filename)

    def h_atom_file_exists(self, atom_number: int) -> bool:
        return os_path_exists(self.atom_file_path(atom_number))

    def delete_atom_file(self, atom_number: int):
        delete_dir(self.atom_file_path(atom_number))

    def _get_belief_from_atom_files(self) -> BeliefUnit:
        x_belief = beliefunit_shop(self.belief_name, self.moment_label)
        if self.h_atom_file_exists(self.get_max_atom_file_number()):
            x_atom_files = get_dir_file_strs(self.atoms_dir, delete_extensions=True)
            sorted_atom_filenames = sorted(list(x_atom_files.keys()))

            for x_atom_filename in sorted_atom_filenames:
                x_json_str = x_atom_files.get(x_atom_filename)
                x_dict = get_dict_from_json(x_json_str)
                x_atom = get_beliefatom_from_dict(x_dict)
                modify_belief_with_beliefatom(x_belief, x_atom)
        return x_belief

    def get_max_lesson_file_number(self) -> int:
        return get_max_file_number(self.lessons_dir)

    def _get_next_lesson_file_number(self) -> int:
        max_file_number = self.get_max_lesson_file_number()
        init_lesson_id = get_init_lesson_id_if_None()
        return init_lesson_id if max_file_number is None else max_file_number + 1

    def lesson_filename(self, lesson_id: int) -> str:
        return get_json_filename(lesson_id)

    def lesson_file_path(self, lesson_id: int) -> str:
        """Returns path: _lessons/lesson_id.json"""

        lesson_filename = self.lesson_filename(lesson_id)
        return create_path(self.lessons_dir, lesson_filename)

    def hub_lesson_file_exists(self, lesson_id: int) -> bool:
        return os_path_exists(self.lesson_file_path(lesson_id))

    def validate_lessonunit(self, x_lessonunit: LessonUnit) -> LessonUnit:
        if x_lessonunit.atoms_dir != self.atoms_dir:
            x_lessonunit.atoms_dir = self.atoms_dir
        if x_lessonunit.lessons_dir != self.lessons_dir:
            x_lessonunit.lessons_dir = self.lessons_dir
        if x_lessonunit._lesson_id != self._get_next_lesson_file_number():
            x_lessonunit._lesson_id = self._get_next_lesson_file_number()
        if x_lessonunit.belief_name != self.belief_name:
            x_lessonunit.belief_name = self.belief_name
        if x_lessonunit._delta_start != self._get_next_atom_file_number():
            x_lessonunit._delta_start = self._get_next_atom_file_number()
        return x_lessonunit

    def save_lesson_file(
        self,
        x_lesson: LessonUnit,
        replace: bool = True,
        correct_invalid_attrs: bool = True,
    ) -> LessonUnit:
        if correct_invalid_attrs:
            x_lesson = self.validate_lessonunit(x_lesson)

        if x_lesson.atoms_dir != self.atoms_dir:
            raise SaveLessonFileException(
                f"LessonUnit file cannot be saved because lessonunit.atoms_dir is incorrect: {x_lesson.atoms_dir}. It must be {self.atoms_dir}."
            )
        if x_lesson.lessons_dir != self.lessons_dir:
            raise SaveLessonFileException(
                f"LessonUnit file cannot be saved because lessonunit.lessons_dir is incorrect: {x_lesson.lessons_dir}. It must be {self.lessons_dir}."
            )
        if x_lesson.belief_name != self.belief_name:
            raise SaveLessonFileException(
                f"LessonUnit file cannot be saved because lessonunit.belief_name is incorrect: {x_lesson.belief_name}. It must be {self.belief_name}."
            )
        lesson_filename = self.lesson_filename(x_lesson._lesson_id)
        if not replace and self.hub_lesson_file_exists(x_lesson._lesson_id):
            raise SaveLessonFileException(
                f"LessonUnit file {lesson_filename} exists and cannot be saved over."
            )
        x_lesson.save_files()
        return x_lesson

    def _del_lesson_file(self, lesson_id: int):
        delete_dir(self.lesson_file_path(lesson_id))

    def _default_lessonunit(self) -> LessonUnit:
        return lessonunit_shop(
            belief_name=self.belief_name,
            _lesson_id=self._get_next_lesson_file_number(),
            atoms_dir=self.atoms_dir,
            lessons_dir=self.lessons_dir,
        )

    def create_save_lesson_file(
        self, before_belief: BeliefUnit, after_belief: BeliefUnit
    ):
        new_lessonunit = self._default_lessonunit()
        new_beliefdelta = new_lessonunit._beliefdelta
        new_beliefdelta.add_all_different_beliefatoms(before_belief, after_belief)
        self.save_lesson_file(new_lessonunit)

    def get_lessonunit(self, lesson_id: int) -> LessonUnit:
        if self.hub_lesson_file_exists(lesson_id) is False:
            raise LessonFileMissingException(
                f"LessonUnit file_number {lesson_id} does not exist."
            )
        x_lessons_dir = self.lessons_dir
        x_atoms_dir = self.atoms_dir
        return create_lessonunit_from_files(x_lessons_dir, lesson_id, x_atoms_dir)

    def _merge_any_lessons(self, x_belief: BeliefUnit) -> BeliefUnit:
        lessons_dir = self.lessons_dir
        lesson_ints = get_integer_filenames(lessons_dir, x_belief.last_lesson_id)
        if len(lesson_ints) == 0:
            return copy_deepcopy(x_belief)

        for lesson_int in lesson_ints:
            x_lesson = self.get_lessonunit(lesson_int)
            new_belief = x_lesson._beliefdelta.get_atom_edited_belief(x_belief)
        return new_belief

    def _create_initial_lesson_files_from_default(self):
        x_lessonunit = lessonunit_shop(
            belief_name=self.belief_name,
            _lesson_id=get_init_lesson_id_if_None(),
            lessons_dir=self.lessons_dir,
            atoms_dir=self.atoms_dir,
        )
        x_lessonunit._beliefdelta.add_all_different_beliefatoms(
            before_belief=self.default_gut_belief(),
            after_belief=self.default_gut_belief(),
        )
        x_lessonunit.save_files()

    def _create_gut_from_lessons(self):
        x_belief = self._merge_any_lessons(self.default_gut_belief())
        save_gut_file(self.moment_mstr_dir, x_belief)

    def _create_initial_lesson_and_gut_files(self):
        self._create_initial_lesson_files_from_default()
        self._create_gut_from_lessons()

    def _create_initial_lesson_files_from_gut(self):
        x_lessonunit = self._default_lessonunit()
        x_lessonunit._beliefdelta.add_all_different_beliefatoms(
            before_belief=self.default_gut_belief(),
            after_belief=open_gut_file(
                self.moment_mstr_dir, self.moment_label, self.belief_name
            ),
        )
        x_lessonunit.save_files()

    def initialize_lesson_gut_files(self):
        x_gut_file_exists = gut_file_exists(
            self.moment_mstr_dir, self.moment_label, self.belief_name
        )
        lesson_file_exists = self.hub_lesson_file_exists(init_lesson_id())
        if x_gut_file_exists is False and lesson_file_exists is False:
            self._create_initial_lesson_and_gut_files()
        elif x_gut_file_exists is False and lesson_file_exists:
            self._create_gut_from_lessons()
        elif x_gut_file_exists and lesson_file_exists is False:
            self._create_initial_lesson_files_from_gut()

    def append_lessons_to_gut_file(self) -> BeliefUnit:
        gut_belief = open_gut_file(
            self.moment_mstr_dir, self.moment_label, self.belief_name
        )
        gut_belief = self._merge_any_lessons(gut_belief)
        save_gut_file(self.moment_mstr_dir, gut_belief)
        return gut_belief


def lessonfilehandler_shop(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName = None,
    knot: KnotTerm = None,
    fund_pool: float = None,
    fund_grain: float = None,
    respect_grain: float = None,
    mana_grain: float = None,
) -> LessonFileHandler:
    x_lessonfilehandler = LessonFileHandler(
        moment_mstr_dir=moment_mstr_dir,
        moment_label=moment_label,
        belief_name=validate_labelterm(belief_name, knot),
        knot=default_knot_if_None(knot),
        fund_pool=validate_pool_num(fund_pool),
        fund_grain=default_grain_num_if_None(fund_grain),
        respect_grain=default_grain_num_if_None(respect_grain),
        mana_grain=default_grain_num_if_None(mana_grain),
    )
    x_lessonfilehandler.set_dir_attrs()
    return x_lessonfilehandler
