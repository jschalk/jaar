from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path, open_file
from src.a01_rope_logic._ref.a01_doc_builder import get_ropepointer_explanation_md
from src.a98_docs_builder.doc_builder import (
    get_module_blurbs_md,
    save_module_blurbs_md,
    save_ropepointer_explanation_md,
)
from src.a98_docs_builder.test._util.a98_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_get_module_blurbs_md_ReturnsObj():
    # ESTABLISH / WHEN
    module_blurbs_md = get_module_blurbs_md()

    # THEN
    assert module_blurbs_md
    assert module_blurbs_md.find("a03") > 0


def test_save_module_blurbs_md_CreatesFile(env_dir_setup_cleanup):
    # ESTABLISH
    temp_dir = get_module_temp_dir()
    module_blurbs_path = create_path(temp_dir, "module_blurbs.md")
    assert not os_path_exists(module_blurbs_path)

    # WHEN
    save_module_blurbs_md(temp_dir)

    # THEN
    assert os_path_exists(module_blurbs_path)
    expected_module_blurbs_md = get_module_blurbs_md()
    assert open_file(module_blurbs_path) == expected_module_blurbs_md


def test_save_ropepointer_explanation_md_CreatesFile(env_dir_setup_cleanup):
    # ESTABLISH
    temp_dir = get_module_temp_dir()
    file_path = create_path(temp_dir, "ropepointer_explanation.md")
    assert not os_path_exists(file_path)

    # WHEN
    save_ropepointer_explanation_md(temp_dir)

    # THEN
    assert os_path_exists(file_path)
    assert open_file(file_path) == get_ropepointer_explanation_md()
