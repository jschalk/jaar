from src._road.road import default_road_delimiter_if_none
from src._road.finance import default_planck_if_none
from src.agenda.agenda import duty_str, work_str
from src.real.nook import NookUnit, nookunit_shop
from src.real.gift import get_gifts_folder
from src.real.examples.real_env_kit import get_test_reals_dir, get_test_real_id


def test_NookUnit_Exists():
    # GIVEN / WHEN
    x_nookunit = NookUnit()

    # THEN
    assert x_nookunit.person_id is None
    assert x_nookunit.real_id is None
    assert x_nookunit.real_dir is None
    assert x_nookunit.reals_dir is None
    assert x_nookunit.persons_dir is None
    assert x_nookunit.person_dir is None
    assert x_nookunit._econs_dir is None
    assert x_nookunit._atoms_dir is None
    assert x_nookunit._gifts_dir is None
    assert x_nookunit._duty_obj is None
    assert x_nookunit._duty_file_name is None
    assert x_nookunit._duty_path is None
    assert x_nookunit._work_obj is None
    assert x_nookunit._work_file_name is None
    assert x_nookunit._work_path is None
    assert x_nookunit._econ_objs is None
    assert x_nookunit._road_delimiter is None
    assert x_nookunit._planck is None


def test_nookunit_shop_ReturnsCorrectObj():
    # GIVEN
    x_reals_dir = "src/real/examples"
    x_real_id = "music"
    sue_text = "Sue"
    x_road_delimiter = "/"
    x_planck = 3

    # WHEN
    x_nookunit = nookunit_shop(
        x_reals_dir, x_real_id, sue_text, x_road_delimiter, x_planck
    )

    # THEN
    assert x_nookunit.real_dir == f"{x_reals_dir}/{x_real_id}"
    assert x_nookunit.persons_dir == f"{x_nookunit.real_dir}/persons"
    assert x_nookunit.person_id == sue_text
    assert x_nookunit.person_dir == f"{x_nookunit.persons_dir}/{sue_text}"
    assert x_nookunit._econs_dir == f"{x_nookunit.person_dir}/econs"
    assert x_nookunit._atoms_dir == f"{x_nookunit.person_dir}/atoms"
    assert x_nookunit._gifts_dir == f"{x_nookunit.person_dir}/{get_gifts_folder()}"
    assert x_nookunit._duty_file_name == f"{duty_str()}.json"
    x_duty_path = f"{x_nookunit.person_dir}/{x_nookunit._duty_file_name}"
    assert x_nookunit._duty_path == x_duty_path
    assert x_nookunit._work_file_name == f"{work_str()}.json"
    x_workpath = f"{x_nookunit.person_dir}/{x_nookunit._work_file_name}"
    assert x_nookunit._work_path == x_workpath
    assert x_nookunit._road_delimiter == x_road_delimiter
    assert x_nookunit._planck == x_planck


def test_nookunit_shop_ReturnsCorrectObjWhenEmpty():
    # GIVEN
    sue_text = "Sue"

    # WHEN
    sue_nookunit = nookunit_shop(None, None, sue_text)

    # THEN
    assert sue_nookunit.real_dir == f"{get_test_reals_dir()}/{get_test_real_id()}"
    assert sue_nookunit.persons_dir == f"{sue_nookunit.real_dir}/persons"
    assert sue_nookunit.person_id == sue_text
    assert sue_nookunit.person_dir == f"{sue_nookunit.persons_dir}/{sue_text}"
    assert sue_nookunit._econs_dir == f"{sue_nookunit.person_dir}/econs"
    assert sue_nookunit._atoms_dir == f"{sue_nookunit.person_dir}/atoms"
    assert sue_nookunit._gifts_dir == f"{sue_nookunit.person_dir}/{get_gifts_folder()}"
    assert sue_nookunit._duty_file_name == f"{duty_str()}.json"
    x_duty_path = f"{sue_nookunit.person_dir}/{sue_nookunit._duty_file_name}"
    assert sue_nookunit._duty_path == x_duty_path
    assert sue_nookunit._work_file_name == f"{work_str()}.json"
    x_workpath = f"{sue_nookunit.person_dir}/{sue_nookunit._work_file_name}"
    assert sue_nookunit._work_path == x_workpath
    assert sue_nookunit._road_delimiter == default_road_delimiter_if_none()
    assert sue_nookunit._planck == default_planck_if_none()