# Tests that confirm marking a task or habit done through the TUI actually works.

import asyncio

from habit_options import done_today
from profile_options import state as profile_state
from task_options import display, habit_detection, state, task_actions
from tui import app as tui_app
from tui import habits_screen, tasks_screen
from tui.app import AviOSApp


async def _instant_sleep(seconds):
    return None


def _skip_name_prompt(monkeypatch):
    # get_user_name() is one shared function read by both tui.app and
    # tui.dashboard_screen, so the data it reads must be patched, not the
    # function reference in just one of the modules that imported it.
    monkeypatch.setattr(profile_state, "profile_data", {"name": "Avi"})
    monkeypatch.setattr(tui_app, "sleep", _instant_sleep)


def _sample_task(name="Water the plants"):
    return {
        "name": name,
        "completed": False,
        "archived": False,
        "deleted": False,
        "done_history": [],
        "habit_candidate": False,
        "habit_prompt_dismissed": False,
        "pinned": False,
        "created_at": "01-01-2026",
    }


def _sample_habit(name="Drink water"):
    return {
        "name": name,
        "category": "Health",
        "created_at": "01-01-2026",
        "done_dates": [],
    }


def test_pressing_enter_on_a_task_row_marks_it_done(monkeypatch):
    test_tasks = [_sample_task()]

    for module in (state, display, task_actions, habit_detection, tasks_screen):
        monkeypatch.setattr(module, "task_list", test_tasks)
    monkeypatch.setattr(task_actions, "save_tasks", lambda: None)
    monkeypatch.setattr(task_actions, "add_activity", lambda message: None)
    _skip_name_prompt(monkeypatch)

    async def check():
        app = AviOSApp()
        async with app.run_test() as pilot:
            await pilot.pause()
            await pilot.press("t")
            await pilot.press("enter")
            await pilot.pause()

    asyncio.run(check())

    assert test_tasks[0]["completed"] is True


def test_pressing_enter_on_a_habit_row_marks_it_done_today(monkeypatch):
    test_habits = [_sample_habit()]

    monkeypatch.setattr(habits_screen, "habit_list", test_habits)
    monkeypatch.setattr(done_today, "habit_list", test_habits)
    monkeypatch.setattr(done_today, "save_habits", lambda: None)
    monkeypatch.setattr(done_today, "add_activity", lambda message: None)
    monkeypatch.setattr(done_today, "get_today_date", lambda: "18-07-2026")
    _skip_name_prompt(monkeypatch)

    async def check():
        app = AviOSApp()
        async with app.run_test() as pilot:
            await pilot.pause()
            await pilot.press("h")
            await pilot.press("enter")
            await pilot.pause()

    asyncio.run(check())

    assert test_habits[0]["done_dates"] == ["18-07-2026"]
