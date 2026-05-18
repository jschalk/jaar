# TODO: rebuild pip tests, start with manual tests, then create pytests one at a time
# """
# Tests for keg2 PyPI library.

# Mirrors the publish.yaml GitHub Actions pipeline locally:
# 1. A wheel can be built from the local repo (python -m build)
# 2. The built wheel installs without errors (pip install dist/*.whl)
# 3. A keg2 tkinter app can be launched and closed without errors

# Run with:
#     pytest test_pypi_package.py -v --check_pip

# Requirements:
#     pip install pytest build

# Environment variables:
#     REPO_ROOT   Path to the repo root (default: auto-detected by walking up to pyproject.toml)
# """

# from glob import glob as glob_glob
# from os import environ as os_environ
# from os.path import (
#     abspath as os_path_abspath,
#     dirname as os_path_dirname,
#     isfile as os_path_isfile,
#     join as os_path_join,
# )
# from pytest import (
#     TempPathFactory as pytest_TempPathFactory,
#     fixture as pytest_fixture,
#     mark as pytest_mark,
#     skip as pytest_skip,
# )
# from subprocess import (
#     PIPE as subprocess_PIPE,
#     CompletedProcess as subprocess_CompletedProcess,
#     run as subprocess_run,
# )
# from sys import executable as sys_executable


# def _find_repo_root(start: str) -> str:
#     """Walk up from start until we find a directory containing pyproject.toml."""
#     current = os_path_abspath(start)
#     while True:
#         if os_path_isfile(os_path_join(current, "pyproject.toml")):
#             return current
#         parent = os_path_dirname(current)
#         if parent == current:
#             raise FileNotFoundError(
#                 "Could not find pyproject.toml in any parent directory of "
#                 f"{start}. Set the REPO_ROOT environment variable explicitly."
#             )
#         current = parent


# # Repo root: walk up from this file to find pyproject.toml, or override via env var.
# REPO_ROOT = os_environ.get(
#     "REPO_ROOT", _find_repo_root(os_path_dirname(os_path_abspath(__file__)))
# )

# check_pip = pytest_mark.skipif(
#     "not config.getoption('--check_pip')",
#     reason="Pass --check_pip to run tests that download/install packages",
# )


# def _run(cmd: list[str], **kwargs) -> subprocess_CompletedProcess:
#     """Run a subprocess command, capturing stdout and stderr."""
#     return subprocess_run(
#         cmd,
#         stdout=subprocess_PIPE,
#         stderr=subprocess_PIPE,
#         text=True,
#         **kwargs,
#     )


# # ---------------------------------------------------------------------------
# # 1. Wheel build tests  (mirrors "Build package" step in publish.yaml)
# # ---------------------------------------------------------------------------


# class TestWheelBuild:
#     """Confirm a wheel can be built from the local source tree.

#     Mirrors:
#         pip install build
#         python -m build
#     """

#     def test_build_package_ExitsZero(self, tmp_path, check_pip_enabled):
#         """python -m build must exit with code 0."""
#         # ESTABLISH / WHEN
#         result = _run(
#             [sys_executable, "-m", "build", "--outdir", str(tmp_path)],
#             cwd=REPO_ROOT,
#             timeout=120,
#         )
#         # THEN
#         assert result.returncode == 0, (
#             f"'python -m build' failed (exit {result.returncode}).\n"
#             f"stdout:\n{result.stdout}\n"
#             f"stderr:\n{result.stderr}"
#         )

#     def test_wheel_FileIsProduced(self, tmp_path, check_pip_enabled):
#         """python -m build must produce at least one .whl file."""
#         # ESTABLISH / WHEN
#         _run(
#             [sys_executable, "-m", "build", "--outdir", str(tmp_path)],
#             cwd=REPO_ROOT,
#             timeout=120,
#         )
#         # THEN
#         wheels = glob_glob(str(tmp_path / "*.whl"))
#         assert wheels, (
#             f"No .whl file found in {tmp_path} after 'python -m build'.\n"
#             f"Contents: {list(tmp_path.iterdir())}"
#         )

#     def test_build_ProducesNoErrorOutput(self, tmp_path, check_pip_enabled):
#         # ESTABLISH / WHEN
#         """python -m build must not print ERROR lines to stderr."""
#         result = _run(
#             [sys_executable, "-m", "build", "--outdir", str(tmp_path)],
#             cwd=REPO_ROOT,
#             timeout=120,
#         )
#         # THEN
#         error_lines = [
#             line
#             for line in (result.stdout + result.stderr).splitlines()
#             if line.strip().startswith("ERROR")
#         ]
#         assert not error_lines, "'python -m build' produced ERROR lines:\n" + "\n".join(
#             error_lines
#         )


# # ---------------------------------------------------------------------------
# # 2. Installation tests  (mirrors pip install from the built wheel)
# # ---------------------------------------------------------------------------


# @pytest_fixture(scope="module")
# def built_wheel(tmp_path: pytest_TempPathFactory, check_pip_enabled):
#     """Build the package once and return the path to the .whl file."""
#     out_dir = tmp_path.mktemp("dist")
#     result = _run(
#         [sys_executable, "-m", "build", "--outdir", str(out_dir)],
#         cwd=REPO_ROOT,
#         timeout=120,
#     )
#     if result.returncode != 0:
#         pytest_skip(f"Wheel build failed � skipping install tests.\n{result.stderr}")
#     wheels = glob_glob(str(out_dir / "*.whl"))
#     if not wheels:
#         pytest_skip("No .whl produced � skipping install tests.")
#     return wheels[0]


# @pytest_fixture(scope="module")
# def check_pip_enabled(request):
#     """Skip the test if --check_pip was not passed."""
#     if not request.config.getoption("--check_pip"):
#         pytest_skip("Pass --check_pip to run pip/build tests")


# class TestInstallation:
#     """Confirm the built wheel installs cleanly via pip."""

#     def test_pip_install_wheel_ExitsZero(self, built_wheel, check_pip_enabled):
#         """pip install <wheel> must exit with code 0."""
#         # ESTABLISH / WHEN
#         result = _run(
#             [sys_executable, "-m", "pip", "install", built_wheel],
#             timeout=120,
#         )
#         # THEN
#         assert result.returncode == 0, (
#             f"pip install failed (exit {result.returncode}).\n"
#             f"stdout:\n{result.stdout}\n"
#             f"stderr:\n{result.stderr}"
#         )

#     def test_pip_install_wheel_NoErrorOutput(self, built_wheel, check_pip_enabled):
#         """pip install must not produce ERROR lines."""
#         # ESTABLISH / WHEN
#         result = _run(
#             [sys_executable, "-m", "pip", "install", built_wheel],
#             timeout=120,
#         )
#         # THEN
#         error_lines = [
#             line
#             for line in (result.stdout + result.stderr).splitlines()
#             if line.strip().upper().startswith("ERROR")
#         ]
#         assert not error_lines, "pip install produced ERROR lines:\n" + "\n".join(
#             error_lines
#         )

#     # def test_keg2_importable_after_install(self, built_wheel, check_pip_enabled):
#     #     """keg2 must be importable in a fresh subprocess after installing the wheel."""
#     #     # Install first
#     #     install = _run(
#     #         [sys_executable, "-m", "pip", "install", built_wheel],
#     #         timeout=120,
#     #     )
#     #     assert (
#     #         install.returncode == 0
#     #     ), f"pip install failed before import check.\n{install.stderr}"
#     #     # Check importability in a subprocess � avoids the stale sys.path
#     #     # issue that would occur if we tried to import in the running interpreter.
#     #     result = _run(
#     #         [sys_executable, "-c", "import keg2"],
#     #         timeout=30,
#     #     )
#     #     assert result.returncode == 0, (
#     #         f"'import keg2' failed in subprocess after pip install.\n"
#     #         f"stderr:\n{result.stderr}"
#     #     )


# # ---------------------------------------------------------------------------
# # 3. Tkinter / app launch tests
# # ---------------------------------------------------------------------------


# class TestTkinterLaunch:
#     """Confirm the keg2 tkinter app opens and closes without errors."""

#     # Runs in a subprocess so the Tk mainloop never blocks pytest.
#     # Update the entry-point list to match your actual API if needed.
#     _LAUNCH_SCRIPT = """\
# import sys, importlib

# # ---- Tk availability guard -------------------------------------------------
# import tkinter as tk
# try:
#     root = tk.Tk()
#     root.withdraw()
#     root.destroy()
# except Exception as exc:
#     print(f"TKINTER_UNAVAILABLE: {exc}", file=sys.stderr)
#     sys.exit(2)

# # ---- keg2 app launch -------------------------------------------------------
# import keg2

# # Try common entry-point patterns; update to match your actual API:
# #   Pattern A - module-level function  : keg2.create_app() / keg2.run()
# #   Pattern B - App class              : keg2.App()
# #   Pattern C - Keg2App class          : keg2.Keg2App()
# launched = False

# for attr in ("create_app", "App", "Keg2App", "KegApp", "run"):
#     if hasattr(keg2, attr):
#         obj = getattr(keg2, attr)
#         try:
#             if callable(obj):
#                 instance = obj()
#                 if hasattr(instance, "destroy"):
#                     instance.destroy()
#                 elif hasattr(instance, "quit"):
#                     instance.quit()
#             launched = True
#             break
#         except Exception as exc:
#             print(f"LAUNCH_ERROR via keg2.{attr}: {exc}", file=sys.stderr)
#             sys.exit(3)

# if not launched:
#     print(
#         "LAUNCH_SKIPPED: no recognised entry point found in keg2. "
#         "Add your entry point to the attr list in _LAUNCH_SCRIPT.",
#         file=sys.stderr,
#     )
#     sys.exit(4)

# sys.exit(0)
# """

#     def _run_launch(self) -> subprocess_CompletedProcess:
#         return _run(
#             [sys_executable, "-c", self._LAUNCH_SCRIPT],
#             timeout=30,
#         )

#     def test_tkinter_IsAvailable(self, check_pip_enabled):
#         """The test environment must have a working tkinter installation."""
#         result = _run(
#             [sys_executable, "-c", "import tkinter; tkinter.Tk().destroy()"],
#             timeout=10,
#         )
#         if result.returncode != 0:
#             pytest.skip(
#                 "tkinter is not available in this environment � "
#                 f"skipping GUI tests.\nstderr: {result.stderr}"
#             )

#     # def test_app_launches_without_error(self, check_pip_enabled):
#     #     """keg2 app must initialise and close without raising an exception."""
#     #     result = self._run_launch()
#     #     if result.returncode == 2:
#     #         pytest.skip("tkinter unavailable in subprocess.")
#     #     if result.returncode == 4:
#     #         pytest.skip("No recognised entry point found � update _LAUNCH_SCRIPT.")
#     #     assert result.returncode == 0, (
#     #         f"keg2 app launch failed (exit {result.returncode}).\n"
#     #         f"stdout:\n{result.stdout}\n"
#     #         f"stderr:\n{result.stderr}"
#     #     )

#     # def test_app_launch_produces_no_tracebacks(self, check_pip_enabled):
#     #     """keg2 app launch must not print Python tracebacks."""
#     #     result = self._run_launch()
#     #     if result.returncode in (2, 4):
#     #         pytest.skip("Skipping traceback check � environment or config issue.")
#     #     combined = result.stdout + result.stderr
#     #     assert "Traceback (most recent call last)" not in combined, (
#     #         "A Python traceback was printed during app launch:\n" + combined
#     #     )
