# test_pip_version.py
from importlib import import_module as importlib_import_module
from pytest import skip as pytest_skip
from subprocess import check_call as subprocess_check_call
from sys import executable as sys_executable, path as sys_path

# # TODO reactivate this test and get it working
# def test_download_and_check_version(tmp_path, check_pip):
#     # sourcery skip: no-conditionals-in-tests
#     if not check_pip:
#         pytest_skip("use --check_pip to run this test")

#     package_name = "keg2"

#     install_dir = tmp_path / "site"
#     install_dir.mkdir()

#     subprocess_check_call(
#         [
#             sys_executable,
#             "-m",
#             "pip",
#             "install",
#             package_name,
#             "--target",
#             str(install_dir),
#         ]
#     )

#     sys_path.insert(0, str(install_dir))
#     module = importlib_import_module(package_name)
#     print(f"{module.__name__} version: {module.__version__}")
#     # expected_version = get_version()
#     # print(f"{expected_version}")
#     assert module.__version__ == "huh"
