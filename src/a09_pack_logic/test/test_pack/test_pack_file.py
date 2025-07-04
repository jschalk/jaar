from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path, open_json
from src.a09_pack_logic.delta import believerdelta_shop
from src.a09_pack_logic.pack import create_packunit_from_files, packunit_shop
from src.a09_pack_logic.test._util.a09_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as beliefs_dir,
)
from src.a09_pack_logic.test._util.a09_str import believer_name_str, face_name_str
from src.a09_pack_logic.test._util.example_atoms import (
    get_atom_example_planunit_ball,
    get_atom_example_planunit_knee,
    get_atom_example_planunit_sports,
)


def test_PackUnit_save_atom_file_SavesCorrectFile(env_dir_setup_cleanup):
    # ESTABLISH
    x_belief_dir = create_path(beliefs_dir(), "amy23")
    x_believers_dir = create_path(x_belief_dir, "believers")
    sue_str = "Sue"
    sue_believer_dir = create_path(x_believers_dir, sue_str)
    sue_atoms_dir = create_path(sue_believer_dir, "atoms")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = create_path(sue_atoms_dir, two_filename)
    sue_atom6_path = create_path(sue_atoms_dir, six_filename)
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    sue_packunit = packunit_shop(sue_str, _atoms_dir=sue_atoms_dir)
    assert os_path_exists(sue_atom2_path) is False
    assert os_path_exists(sue_atom6_path) is False

    # WHEN
    sports_atom = get_atom_example_planunit_sports()
    sue_packunit._save_atom_file(two_int, sports_atom)

    # THEN
    assert os_path_exists(sue_atom2_path)
    assert os_path_exists(sue_atom6_path) is False
    two_file_dict = open_json(sue_atoms_dir, two_filename)
    assert two_file_dict == sports_atom.get_dict()


def test_PackUnit_atom_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_belief_dir = create_path(beliefs_dir(), "amy23")
    x_believers_dir = create_path(x_belief_dir, "believers")
    sue_str = "Sue"
    sue_believer_dir = create_path(x_believers_dir, sue_str)
    sue_atoms_dir = create_path(sue_believer_dir, "atoms")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = create_path(sue_atoms_dir, two_filename)
    sue_atom6_path = create_path(sue_atoms_dir, six_filename)
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    sue_packunit = packunit_shop(sue_str, _atoms_dir=sue_atoms_dir)
    assert os_path_exists(sue_atom2_path) is False
    assert sue_packunit.atom_file_exists(two_int) is False

    # WHEN
    sports_atom = get_atom_example_planunit_sports()
    sue_packunit._save_atom_file(two_int, sports_atom)

    # THEN
    assert sue_packunit.atom_file_exists(two_int)


def test_PackUnit_open_atom_file_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_belief_dir = create_path(beliefs_dir(), "amy23")
    x_believers_dir = create_path(x_belief_dir, "believers")
    sue_str = "Sue"
    sue_believer_dir = create_path(x_believers_dir, sue_str)
    sue_atoms_dir = create_path(sue_believer_dir, "atoms")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = create_path(sue_atoms_dir, two_filename)
    sue_atom6_path = create_path(sue_atoms_dir, six_filename)
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    sue_packunit = packunit_shop(sue_str, _atoms_dir=sue_atoms_dir)
    sports_atom = get_atom_example_planunit_sports()
    sue_packunit._save_atom_file(two_int, sports_atom)
    assert sue_packunit.atom_file_exists(two_int)

    # WHEN
    file_atom = sue_packunit._open_atom_file(two_int)

    # THEN
    assert file_atom == sports_atom


def test_PackUnit_save_pack_file_SavesCorrectFile(env_dir_setup_cleanup):
    # ESTABLISH
    x_belief_dir = create_path(beliefs_dir(), "amy23")
    x_believers_dir = create_path(x_belief_dir, "believers")
    sue_str = "Sue"
    sue_pack_id = 2
    sue_believer_dir = create_path(x_believers_dir, sue_str)
    sue_packs_dir = create_path(sue_believer_dir, "packs")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_pack2_path = create_path(sue_packs_dir, two_filename)
    sue_pack6_path = create_path(sue_packs_dir, six_filename)
    print(f"{sue_pack2_path=}")
    print(f"{sue_pack6_path=}")
    sue_packunit = packunit_shop(
        sue_str, None, None, sue_pack_id, _packs_dir=sue_packs_dir
    )
    assert os_path_exists(sue_pack2_path) is False
    assert os_path_exists(sue_pack6_path) is False

    # WHEN
    sue_packunit._save_pack_file()

    # THEN
    assert os_path_exists(sue_pack2_path)
    assert os_path_exists(sue_pack6_path) is False
    pack_file_dict = open_json(sue_packs_dir, two_filename)
    print(f"{pack_file_dict=}")
    assert pack_file_dict.get("delta_atom_numbers") == []
    assert pack_file_dict.get(believer_name_str()) == sue_str
    assert pack_file_dict.get(face_name_str()) is None
    print(f"{pack_file_dict.keys()=}")


def test_PackUnit_pack_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_belief_dir = create_path(beliefs_dir(), "amy23")
    x_believers_dir = create_path(x_belief_dir, "believers")
    sue_str = "Sue"
    sue_believer_dir = create_path(x_believers_dir, sue_str)
    sue_packs_dir = create_path(sue_believer_dir, "packs")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_pack2_path = create_path(sue_packs_dir, two_filename)
    sue_pack6_path = create_path(sue_packs_dir, six_filename)
    print(f"{sue_pack2_path=}")
    print(f"{sue_pack6_path=}")
    sue_packunit = packunit_shop(sue_str, _packs_dir=sue_packs_dir)
    assert os_path_exists(sue_pack2_path) is False
    assert sue_packunit.pack_file_exists() is False

    # WHEN
    sue_packunit._save_pack_file()

    # THEN
    assert sue_packunit.pack_file_exists()


def test_PackUnit_save_files_CorrectlySavesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    x_belief_dir = create_path(beliefs_dir(), "amy23")
    x_believers_dir = create_path(x_belief_dir, "believers")
    sue_str = "Sue"
    sue_believer_dir = create_path(x_believers_dir, sue_str)
    sue_atoms_dir = create_path(sue_believer_dir, "atoms")
    sue_packs_dir = create_path(sue_believer_dir, "packs")

    zia_str = "Zia"
    yao_str = "Yao"
    sue_delta_start = 4
    sue_packunit = packunit_shop(
        sue_str, _atoms_dir=sue_atoms_dir, _packs_dir=sue_packs_dir
    )
    sue_packunit.set_delta_start(sue_delta_start)
    sue_packunit.set_face(zia_str)
    sue_packunit.set_face(yao_str)
    int4 = 4
    int5 = 5
    sports_atom = get_atom_example_planunit_sports()
    knee_atom = get_atom_example_planunit_knee()
    sue_packunit._believerdelta.set_believeratom(sports_atom)
    sue_packunit._believerdelta.set_believeratom(knee_atom)
    assert sue_packunit.pack_file_exists() is False
    assert sue_packunit.atom_file_exists(int4) is False
    assert sue_packunit.atom_file_exists(int5) is False

    # WHEN
    sue_packunit.save_files()

    # THEN
    assert sue_packunit.pack_file_exists()
    assert sue_packunit.atom_file_exists(int4)
    assert sue_packunit.atom_file_exists(int5)


def test_PackUnit_create_believerdelta_from_atom_files_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    x_belief_dir = create_path(beliefs_dir(), "amy23")
    x_believers_dir = create_path(x_belief_dir, "believers")
    sue_str = "Sue"
    sue_believer_dir = create_path(x_believers_dir, sue_str)
    sue_atoms_dir = create_path(sue_believer_dir, "atoms")

    sue_packunit = packunit_shop(sue_str, _atoms_dir=sue_atoms_dir)
    int4 = 4
    int5 = 5
    int9 = 9
    spor_atom = get_atom_example_planunit_sports()
    knee_atom = get_atom_example_planunit_knee()
    ball_atom = get_atom_example_planunit_ball()
    sue_packunit._save_atom_file(int4, spor_atom)
    sue_packunit._save_atom_file(int5, knee_atom)
    sue_packunit._save_atom_file(int9, ball_atom)
    assert sue_packunit._believerdelta == believerdelta_shop()

    # WHEN
    atoms_list = [int4, int5, int9]
    sue_packunit._create_believerdelta_from_atom_files(atoms_list)

    # THEN
    static_believerdelta = believerdelta_shop()
    static_believerdelta.set_believeratom(spor_atom)
    static_believerdelta.set_believeratom(knee_atom)
    static_believerdelta.set_believeratom(ball_atom)
    assert sue_packunit._believerdelta != believerdelta_shop()
    assert sue_packunit._believerdelta == static_believerdelta


def test_create_packunit_from_files_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_belief_dir = create_path(beliefs_dir(), "amy23")
    x_believers_dir = create_path(x_belief_dir, "believers")
    sue_str = "Sue"
    sue_believer_dir = create_path(x_believers_dir, sue_str)
    sue_atoms_dir = create_path(sue_believer_dir, "atoms")
    sue_packs_dir = create_path(sue_believer_dir, "packs")

    yao_str = "Yao"
    sue_delta_start = 4
    src_sue_packunit = packunit_shop(
        sue_str, _atoms_dir=sue_atoms_dir, _packs_dir=sue_packs_dir
    )
    src_sue_packunit.set_delta_start(sue_delta_start)
    src_sue_packunit.set_face(yao_str)
    sports_atom = get_atom_example_planunit_sports()
    knee_atom = get_atom_example_planunit_knee()
    ball_atom = get_atom_example_planunit_ball()
    src_sue_packunit._believerdelta.set_believeratom(sports_atom)
    src_sue_packunit._believerdelta.set_believeratom(knee_atom)
    src_sue_packunit._believerdelta.set_believeratom(ball_atom)
    src_sue_packunit.save_files()

    # WHEN
    new_sue_packunit = create_packunit_from_files(
        packs_dir=sue_packs_dir,
        pack_id=src_sue_packunit._pack_id,
        atoms_dir=sue_atoms_dir,
    )

    # THEN
    assert src_sue_packunit.believer_name == new_sue_packunit.believer_name
    assert src_sue_packunit.face_name == new_sue_packunit.face_name
    assert src_sue_packunit._believerdelta == new_sue_packunit._believerdelta
