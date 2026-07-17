# Tests that check task actions and repeated-task habit suggestions.

from task_options import habit_detection, task_actions
from task_options.state import get_today_name


def _sample_task(name="Water the plants", completed=False):
    return {
        "name": name,
        "completed": completed,
        "archived": False,
        "deleted": False,
        "done_history": [],
        "habit_candidate": False,
        "habit_prompt_dismissed": False,
        "pinned": False,
    }


def test_mark_task_done_records_completion_and_history(monkeypatch):
    test_tasks = [_sample_task()]

    monkeypatch.setattr(task_actions, "task_list", test_tasks)
    monkeypatch.setattr(task_actions, "save_tasks", lambda: None)
    monkeypatch.setattr(task_actions, "add_activity", lambda message: None)
    monkeypatch.setattr(habit_detection, "task_list", test_tasks)
    monkeypatch.setattr(habit_detection, "save_tasks", lambda: None)

    task_actions.mark_task_done(0)

    assert test_tasks[0]["completed"] is True
    assert len(test_tasks[0]["done_history"]) == 1
    assert test_tasks[0]["done_history"][0]["weekday"] == get_today_name()


def test_mark_task_open_clears_completed_flag(monkeypatch):
    test_tasks = [_sample_task(completed=True)]

    monkeypatch.setattr(task_actions, "task_list", test_tasks)
    monkeypatch.setattr(task_actions, "save_tasks", lambda: None)
    monkeypatch.setattr(task_actions, "add_activity", lambda message: None)

    task_actions.mark_task_open(0)

    assert test_tasks[0]["completed"] is False


def test_mark_task_done_offers_habit_idea_after_repeats(monkeypatch):
    test_tasks = [
        _sample_task(completed=True),
        _sample_task(completed=True),
        _sample_task(),
    ]

    monkeypatch.setattr(task_actions, "task_list", test_tasks)
    monkeypatch.setattr(task_actions, "save_tasks", lambda: None)
    monkeypatch.setattr(task_actions, "add_activity", lambda message: None)
    monkeypatch.setattr(habit_detection, "task_list", test_tasks)
    monkeypatch.setattr(habit_detection, "save_tasks", lambda: None)
    monkeypatch.setattr("builtins.input", lambda prompt: "y")

    task_actions.mark_task_done(2)

    assert all(task["habit_candidate"] is True for task in test_tasks)
