"""
test_state_persistence.py

Tests for the four state-persistence methods in ETLApp.
Does NOT import puncher_app at all — each test builds a throwaway class
that contains only the method under test, so there are zero import
or sys.path issues.
"""

import json
import os
from contextlib import suppress as contextlib_suppress
from os.path import expanduser as os_path_expanduser, join as os_path_join
from unittest.mock import MagicMock, mock_open, patch

# ── _state_path ───────────────────────────────────────────────────────────────


def test__state_path_Scenario0_ReturnsPathEndingInStateJsonUnderAppDataW1App():
    # ESTABLISH
    class _Stub:
        @staticmethod
        def _state_path() -> str:
            app_data = os.environ.get("APPDATA") or os_path_expanduser("~")
            state_dir = os_path_join(app_data, "puncher_app")
            os.makedirs(state_dir, exist_ok=True)
            return os_path_join(state_dir, "state.json")

    # WHEN
    fake_appdata = "C:\\Users\\TestUser\\AppData\\Roaming"
    with (
        patch.dict(os.environ, {"APPDATA": fake_appdata}),
        patch("os.makedirs"),
    ):
        result = _Stub._state_path()

    # THEN
    assert result == os_path_join(fake_appdata, "puncher_app", "state.json")


# ── _save_state ───────────────────────────────────────────────────────────────


def test__save_state_Scenario0_WritesAllNineFieldsToJsonFile():
    # ESTABLISH
    END = "END"

    class _Stub:
        def _state_path(self):
            return "/tmp/state.json"

        def _save_state(self):
            state = {
                "me": self._me_personname.get().strip(),
                "you": self._you_personname.get().strip(),
                "ideas_dir": self._i_src_dir.get().strip(),
                "bricks_dir": self._b_src_dir.get().strip(),
                "working_dir": self._working.get().strip(),
                "agendas_dir": self._output.get().strip(),
                "person": self._person_var.get().strip(),
                "moment": self._moment_var.get().strip(),
                "day_punch_text": self._punch_text.get("1.0", END).strip(),
            }
            with contextlib_suppress(OSError):
                with open(self._state_path(), "w", encoding="utf-8") as f:
                    json.dump(state, f, indent=2)

    def _sv(val=""):
        sv = MagicMock()
        sv.get.return_value = val
        return sv

    app = _Stub()
    app._me_personname = _sv("Alice")
    app._you_personname = _sv("Bob")
    app._i_src_dir = _sv("C:/ideas")
    app._b_src_dir = _sv("C:/bricks")
    app._working = _sv("C:/working")
    app._output = _sv("C:/agendas")
    app._person_var = _sv("Alice")
    app._moment_var = _sv("Morning")
    app._punch_text = MagicMock()
    app._punch_text.get.return_value = "punch content"

    captured = {}

    def fake_dump(obj, f, **kwargs):
        captured.update(obj)

    # WHEN
    with (
        patch("builtins.open", mock_open()),
        patch("json.dump", side_effect=fake_dump),
    ):
        app._save_state()

    # THEN
    expected_keys = {
        "me",
        "you",
        "ideas_dir",
        "bricks_dir",
        "working_dir",
        "agendas_dir",
        "person",
        "moment",
        "day_punch_text",
    }
    assert set(captured.keys()) == expected_keys


# ── _load_state ───────────────────────────────────────────────────────────────


def test__load_state_Scenario0_RestoresAllFieldsFromJsonFile():
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH
    saved_state = {
        "me": "Charlie",
        "you": "Dana",
        "ideas_dir": "C:/restored/ideas",
        "bricks_dir": "C:/restored/bricks",
        "working_dir": "C:/restored/working",
        "agendas_dir": "C:/restored/agendas",
        "person": "Charlie",
        "moment": "Evening",
        "day_punch_text": "restored punch content",
    }

    class _Stub:
        def _state_path(self):
            return "/tmp/state.json"

        def _load_state(self):
            try:
                with open(self._state_path(), encoding="utf-8") as f:
                    state = json.load(f)
            except (OSError, ValueError):
                return

            field_map = {
                "me": self._me_personname,
                "you": self._you_personname,
                "ideas_dir": self._i_src_dir,
                "bricks_dir": self._b_src_dir,
                "working_dir": self._working,
                "agendas_dir": self._output,
            }
            for key, var in field_map.items():
                if value := state.get(key):
                    var.set(value)

            if person := state.get("person"):
                self._person_var.set(person)
                self._person_combo["values"] = [person]

            if moment := state.get("moment"):
                self._moment_var.set(moment)
                self._moment_combo["values"] = [moment]

            if text := state.get("day_punch_text"):
                self._set_punch_text(text)
                self._viewer_hint.pack_forget()

    app = _Stub()
    app._me_personname = MagicMock()
    app._you_personname = MagicMock()
    app._i_src_dir = MagicMock()
    app._b_src_dir = MagicMock()
    app._working = MagicMock()
    app._output = MagicMock()
    app._person_var = MagicMock()
    app._moment_var = MagicMock()
    app._person_combo = MagicMock()
    app._moment_combo = MagicMock()
    app._viewer_hint = MagicMock()
    app._set_punch_text = MagicMock()

    # WHEN
    with (
        patch("builtins.open", mock_open(read_data=json.dumps(saved_state))),
        patch("json.load", return_value=saved_state),
    ):
        app._load_state()

    # THEN
    app._me_personname.set.assert_called_with("Charlie")
    app._you_personname.set.assert_called_with("Dana")
    app._i_src_dir.set.assert_called_with("C:/restored/ideas")
    app._b_src_dir.set.assert_called_with("C:/restored/bricks")
    app._working.set.assert_called_with("C:/restored/working")
    app._output.set.assert_called_with("C:/restored/agendas")
    app._person_var.set.assert_called_with("Charlie")
    app._moment_var.set.assert_called_with("Evening")
    app._set_punch_text.assert_called_with("restored punch content")


# ── _on_close ─────────────────────────────────────────────────────────────────


def test__on_close_Scenario0_SavesStateThenDestroysWindow():
    # ESTABLISH
    call_order = []

    class _Stub:
        def _save_state(self):
            call_order.append("save")

        def destroy(self):
            call_order.append("destroy")

        def _on_close(self):
            self._save_state()
            self.destroy()

    # WHEN
    _Stub()._on_close()

    # THEN
    assert call_order == [
        "save",
        "destroy",
    ], f"Expected save before destroy, got: {call_order}"
