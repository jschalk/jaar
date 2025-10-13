from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from src.ch01_py.file_toolbox import create_path
from src.ch10_pack._ref.ch10_path import (
    MOMENT_FILENAME,
    create_atoms_dir_path,
    create_belief_dir_path,
    create_gut_path,
    create_job_path,
    create_moment_beliefs_dir_path,
    create_moment_dir_path,
    create_moment_json_path,
    create_packs_dir_path,
)
from src.ch10_pack.test._util.ch10_env import get_chapter_temp_dir
from src.ref.keywords import Ch10Keywords as wx


def test_create_moment_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_chapter_temp_dir()
    a23_str = "amy23"

    # WHEN
    gen_a23_dir_path = create_moment_dir_path(x_moment_mstr_dir, a23_str)

    # THEN
    moments_dir = create_path(x_moment_mstr_dir, "moments")
    expected_a23_path = create_path(moments_dir, a23_str)
    assert gen_a23_dir_path == expected_a23_path


def test_create_moment_json_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_chapter_temp_dir()
    a23_str = "amy23"

    # WHEN
    gen_a23_json_path = create_moment_json_path(x_moment_mstr_dir, a23_str)

    # THEN
    moments_dir = create_path(x_moment_mstr_dir, "moments")
    a23_path = create_path(moments_dir, a23_str)
    expected_a23_json_path = create_path(a23_path, MOMENT_FILENAME)
    assert gen_a23_json_path == expected_a23_json_path


def test_create_moment_beliefs_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_chapter_temp_dir()
    amy23_str = "amy23"

    # WHEN
    gen_beliefs_dir = create_moment_beliefs_dir_path(x_moment_mstr_dir, amy23_str)

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, amy23_str)
    expected_beliefs_dir = create_path(amy23_dir, "beliefs")
    assert gen_beliefs_dir == expected_beliefs_dir


def test_create_belief_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_chapter_temp_dir()
    amy23_str = "amy23"
    sue_str = "Sue"

    # WHEN
    sue_dir = create_belief_dir_path(x_moment_mstr_dir, amy23_str, sue_str)

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, amy23_str)
    beliefs_dir = create_path(amy23_dir, "beliefs")
    expected_sue_dir = create_path(beliefs_dir, sue_str)
    assert sue_dir == expected_sue_dir


def test_create_atoms_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_chapter_temp_dir()
    amy23_str = "amy23"
    sue_str = "Sue"

    # WHEN
    atoms_dir = create_atoms_dir_path(x_moment_mstr_dir, amy23_str, sue_str)

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, amy23_str)
    beliefs_dir = create_path(amy23_dir, "beliefs")
    sue_dir = create_path(beliefs_dir, sue_str)
    expected_atoms_dir = create_path(sue_dir, "atoms")
    assert atoms_dir == expected_atoms_dir


def test_create_packs_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_chapter_temp_dir()
    amy23_str = "amy23"
    sue_str = "Sue"

    # WHEN
    packs_dir = create_packs_dir_path(x_moment_mstr_dir, amy23_str, sue_str)

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, amy23_str)
    beliefs_dir = create_path(amy23_dir, "beliefs")
    sue_dir = create_path(beliefs_dir, sue_str)
    expected_packs_dir = create_path(sue_dir, "packs")
    assert packs_dir == expected_packs_dir


def test_create_gut_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_chapter_temp_dir()
    a23_str = "amy23"
    bob_str = "Bob"

    # WHEN
    gen_a23_e3_belief_path = create_gut_path(x_moment_mstr_dir, a23_str, bob_str)

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    a23_dir = create_path(x_moments_dir, a23_str)
    a23_beliefs_dir = create_path(a23_dir, "beliefs")
    a23_bob_dir = create_path(a23_beliefs_dir, bob_str)
    a23_bob_gut_dir = create_path(a23_bob_dir, wx.gut)
    expected_a23_bob_gut_json_path = create_path(a23_bob_gut_dir, f"{bob_str}.json")
    # belief_filename = "belief.json"
    # expected_a23_e3_belief_path = create_path(a23_bob_e3_dir, belief_filename)
    assert gen_a23_e3_belief_path == expected_a23_bob_gut_json_path


def test_create_job_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_chapter_temp_dir()
    a23_str = "amy23"
    bob_str = "Bob"

    # WHEN
    gen_a23_e3_belief_path = create_job_path(x_moment_mstr_dir, a23_str, bob_str)

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    a23_dir = create_path(x_moments_dir, a23_str)
    a23_beliefs_dir = create_path(a23_dir, "beliefs")
    a23_bob_dir = create_path(a23_beliefs_dir, bob_str)
    a23_bob_job_dir = create_path(a23_bob_dir, wx.job)
    expected_a23_bob_job_json_path = create_path(a23_bob_job_dir, f"{bob_str}.json")
    # belief_filename = "belief.json"
    # expected_a23_e3_belief_path = create_path(a23_bob_e3_dir, belief_filename)
    assert gen_a23_e3_belief_path == expected_a23_bob_job_json_path


LINUX_OS = platform_system() == "Linux"


def test_create_moment_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_moment_dir_path("moment_mstr_dir", wx.moment_label)
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_moment_dir_path) == doc_str


def test_create_moment_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_moment_json_path("moment_mstr_dir", moment_label=wx.moment_label)
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_moment_json_path) == doc_str


def test_create_moment_beliefs_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_moment_beliefs_dir_path(
        "moment_mstr_dir", moment_label=wx.moment_label
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_moment_beliefs_dir_path) == doc_str


def test_create_belief_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_belief_dir_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=wx.moment_label,
        belief_name=wx.belief_name,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_belief_dir_path) == doc_str


def test_create_atoms_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_atoms_dir_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=wx.moment_label,
        belief_name=wx.belief_name,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_atoms_dir_path) == doc_str


def test_create_packs_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_packs_dir_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=wx.moment_label,
        belief_name=wx.belief_name,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_packs_dir_path) == doc_str


def test_create_gut_path_HasDocString():
    # ESTABLISH
    doc_str = create_gut_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=wx.moment_label,
        belief_name=wx.belief_name,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    print(f"{doc_str=}")
    print(f"{inspect_getdoc(create_gut_path)=}")
    print(inspect_getdoc(create_gut_path))
    assert LINUX_OS or inspect_getdoc(create_gut_path) == doc_str


def test_create_job_path_HasDocString():
    # ESTABLISH
    doc_str = create_job_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=wx.moment_label,
        belief_name=wx.belief_name,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_job_path) == doc_str
