# Tests that check daily habit completion and habit views behave as expected.

from habit_options import done_today, view


def _sample_habit(name="Drink water", done_dates=None):
    return {
        "name": name,
        "category": "Health",
        "created_at": "01-01-2026",
        "done_dates": done_dates or [],
    }


def test_mark_habit_done_returns_true_and_records_date(monkeypatch):
    test_habits = [_sample_habit()]

    monkeypatch.setattr(done_today, "habit_list", test_habits)
    monkeypatch.setattr(done_today, "save_habits", lambda: None)
    monkeypatch.setattr(done_today, "add_activity", lambda message: None)
    monkeypatch.setattr(done_today, "get_today_date", lambda: "18-07-2026")

    result = done_today.mark_habit_done(0)

    assert result is True
    assert test_habits[0]["done_dates"] == ["18-07-2026"]


def test_mark_habit_done_returns_false_when_already_done(monkeypatch):
    test_habits = [_sample_habit(done_dates=["18-07-2026"])]

    monkeypatch.setattr(done_today, "habit_list", test_habits)
    monkeypatch.setattr(done_today, "save_habits", lambda: None)
    monkeypatch.setattr(done_today, "add_activity", lambda message: None)
    monkeypatch.setattr(done_today, "get_today_date", lambda: "18-07-2026")

    result = done_today.mark_habit_done(0)

    assert result is False
    assert test_habits[0]["done_dates"] == ["18-07-2026"]


def test_mark_habit_done_today_records_todays_date(monkeypatch):
    test_habits = [_sample_habit()]

    monkeypatch.setattr(done_today, "habit_list", test_habits)
    monkeypatch.setattr(view, "habit_list", test_habits)
    monkeypatch.setattr(done_today, "save_habits", lambda: None)
    monkeypatch.setattr(done_today, "add_activity", lambda message: None)
    monkeypatch.setattr(done_today, "get_today_date", lambda: "18-07-2026")
    monkeypatch.setattr("builtins.input", lambda prompt: "1")

    done_today.mark_habit_done_today()

    assert test_habits[0]["done_dates"] == ["18-07-2026"]


def test_mark_habit_done_today_does_not_duplicate_same_day(monkeypatch):
    test_habits = [_sample_habit(done_dates=["18-07-2026"])]

    monkeypatch.setattr(done_today, "habit_list", test_habits)
    monkeypatch.setattr(view, "habit_list", test_habits)
    monkeypatch.setattr(done_today, "save_habits", lambda: None)
    monkeypatch.setattr(done_today, "add_activity", lambda message: None)
    monkeypatch.setattr(done_today, "get_today_date", lambda: "18-07-2026")
    monkeypatch.setattr("builtins.input", lambda prompt: "1")

    done_today.mark_habit_done_today()

    assert test_habits[0]["done_dates"] == ["18-07-2026"]
