# Tests that confirm the Textual dashboard opens and navigates correctly.

import asyncio

from profile_options import state as profile_state
from tui import app as tui_app
from tui.app import AviOSApp


async def _instant_sleep(seconds):
    return None


def _skip_name_prompt(monkeypatch, name="Avi"):
    # get_user_name() is one shared function read by both tui.app and
    # tui.dashboard_screen, so the data it reads must be patched, not the
    # function reference in just one of the modules that imported it.
    monkeypatch.setattr(profile_state, "profile_data", {"name": name})
    monkeypatch.setattr(tui_app, "sleep", _instant_sleep)


def test_dashboard_screen_shows_tasks_and_habits_sections(monkeypatch):
    _skip_name_prompt(monkeypatch)

    async def check_dashboard():
        app = AviOSApp()
        async with app.run_test() as pilot:
            await pilot.pause()
            tasks_text = str(pilot.app.screen.query_one("#tasks_summary").render())
            habits_text = str(pilot.app.screen.query_one("#habits_summary").render())
            assert "Tasks" in tasks_text
            assert "Habits" in habits_text

    asyncio.run(check_dashboard())


def test_dashboard_greets_the_saved_name(monkeypatch):
    _skip_name_prompt(monkeypatch, name="Avi")

    async def check_dashboard():
        app = AviOSApp()
        async with app.run_test() as pilot:
            await pilot.pause()
            today_text = str(pilot.app.screen.query_one("#today").render())
            assert "Welcome, Avi!" in today_text

    asyncio.run(check_dashboard())


def test_pressing_t_navigates_to_tasks_screen(monkeypatch):
    _skip_name_prompt(monkeypatch)

    async def check_navigation():
        app = AviOSApp()
        async with app.run_test() as pilot:
            await pilot.pause()
            await pilot.press("t")
            assert type(pilot.app.screen).__name__ == "TasksScreen"

    asyncio.run(check_navigation())
