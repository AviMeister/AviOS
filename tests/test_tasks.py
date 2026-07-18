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

    task_actions.mark_task_done(0)

    assert test_tasks[0]["completed"] is True
    assert len(test_tasks[0]["done_history"]) == 1
    assert test_tasks[0]["done_history"][0]["weekday"] == get_today_name()


def test_mark_task_done_never_blocks_on_input(monkeypatch):
    test_tasks = [_sample_task()]

    monkeypatch.setattr(task_actions, "task_list", test_tasks)
    monkeypatch.setattr(task_actions, "save_tasks", lambda: None)
    monkeypatch.setattr(task_actions, "add_activity", lambda message: None)

    def _fail_if_called(prompt):
        raise AssertionError("mark_task_done should never call input()")

    monkeypatch.setattr("builtins.input", _fail_if_called)

    task_actions.mark_task_done(0)


def test_mark_task_open_clears_completed_flag(monkeypatch):
    test_tasks = [_sample_task(completed=True)]

    monkeypatch.setattr(task_actions, "task_list", test_tasks)
    monkeypatch.setattr(task_actions, "save_tasks", lambda: None)
    monkeypatch.setattr(task_actions, "add_activity", lambda message: None)

    task_actions.mark_task_open(0)

    assert test_tasks[0]["completed"] is False


def test_habit_prompt_is_due_after_three_completions(monkeypatch):
    test_tasks = [
        _sample_task(completed=True),
        _sample_task(completed=True),
        _sample_task(completed=True),
    ]

    monkeypatch.setattr(habit_detection, "task_list", test_tasks)

    assert habit_detection.habit_prompt_is_due(2) is True


def test_apply_habit_decision_marks_all_related_tasks(monkeypatch):
    test_tasks = [_sample_task(), _sample_task()]

    monkeypatch.setattr(habit_detection, "task_list", test_tasks)
    monkeypatch.setattr(habit_detection, "save_tasks", lambda: None)

    habit_detection.apply_habit_decision(0, True)

    assert all(task["habit_candidate"] is True for task in test_tasks)
