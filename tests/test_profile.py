# Tests for saving and reusing the user's name across app launches.

import main
from profile_options import state


def test_set_user_name_saves_and_get_user_name_reads_it_back(monkeypatch):
    test_profile = {}

    monkeypatch.setattr(state, "profile_data", test_profile)
    monkeypatch.setattr(state, "save_profile", lambda: None)

    state.set_user_name("Avi")

    assert state.get_user_name() == "Avi"
    assert test_profile["name"] == "Avi"


def test_get_user_name_is_empty_when_nothing_saved(monkeypatch):
    monkeypatch.setattr(state, "profile_data", {})

    assert state.get_user_name() == ""


def test_ensure_profile_name_skips_prompt_when_name_already_saved(monkeypatch):
    monkeypatch.setattr(main, "get_user_name", lambda: "Avi")

    def _fail_if_called(prompt):
        raise AssertionError("should not ask again once a name is saved")

    monkeypatch.setattr("builtins.input", _fail_if_called)

    main.ensure_profile_name()


def test_ensure_profile_name_asks_and_saves_on_first_run(monkeypatch):
    saved = {}

    monkeypatch.setattr(main, "get_user_name", lambda: "")
    monkeypatch.setattr(main, "set_user_name", lambda name: saved.setdefault("name", name))
    monkeypatch.setattr("builtins.input", lambda prompt: "Avi")

    main.ensure_profile_name()

    assert saved["name"] == "Avi"


def test_ensure_profile_name_falls_back_to_there_when_left_blank(monkeypatch):
    saved = {}

    monkeypatch.setattr(main, "get_user_name", lambda: "")
    monkeypatch.setattr(main, "set_user_name", lambda name: saved.setdefault("name", name))
    monkeypatch.setattr("builtins.input", lambda prompt: "")

    main.ensure_profile_name()

    assert saved["name"] == "there"
