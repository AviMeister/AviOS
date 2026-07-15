from dashboard_options import activity, mood, notes
from task_options import pinned


def test_recent_activity_keeps_latest_five(monkeypatch):
    test_data = {"recent_activity": []}

    monkeypatch.setattr(activity, "dashboard_data", test_data)
    monkeypatch.setattr(activity, "save_dashboard_data", lambda data: None)
    monkeypatch.setattr(activity, "get_current_timestamp", lambda: "16-07-2026 01:00 am")

    for number in range(6):
        activity.add_activity(f"Message {number}")

    assert len(test_data["recent_activity"]) == 5
    assert test_data["recent_activity"][0]["message"] == "Message 5"
    assert test_data["recent_activity"][-1]["message"] == "Message 1"


def test_mood_check_in_saves_today_score(monkeypatch):
    test_data = {"mood_checkins": {}}

    monkeypatch.setattr(mood, "dashboard_data", test_data)
    monkeypatch.setattr(mood, "save_dashboard_data", lambda data: None)
    monkeypatch.setattr(mood, "get_today_date", lambda: "16-07-2026")
    monkeypatch.setattr("builtins.input", lambda prompt: "4")

    mood.check_in_mood()

    assert test_data["mood_checkins"]["16-07-2026"] == 4


def test_quick_note_saves_today_note(monkeypatch):
    test_data = {"quick_notes": {}}

    monkeypatch.setattr(notes, "dashboard_data", test_data)
    monkeypatch.setattr(notes, "save_dashboard_data", lambda data: None)
    monkeypatch.setattr(notes, "get_today_date", lambda: "16-07-2026")
    monkeypatch.setattr("builtins.input", lambda prompt: "Felt focused today")

    notes.set_quick_note()

    assert test_data["quick_notes"]["16-07-2026"] == "Felt focused today"


def test_pin_task_allows_only_one_pinned_task(monkeypatch):
    test_tasks = [
        {"name": "Task A", "pinned": True},
        {"name": "Task B", "pinned": False},
    ]

    monkeypatch.setattr(pinned, "task_list", test_tasks)
    monkeypatch.setattr(pinned, "save_tasks", lambda: None)

    pinned.pin_task(1)

    assert test_tasks[0]["pinned"] is False
    assert test_tasks[1]["pinned"] is True
