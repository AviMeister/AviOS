# Tests that confirm the read-only Textual dashboard opens and navigates correctly.

import asyncio

from tui.app import AviOSApp


def test_dashboard_screen_shows_tasks_and_habits_sections():
    async def check_dashboard():
        app = AviOSApp()
        async with app.run_test() as pilot:
            tasks_text = str(pilot.app.screen.query_one("#tasks_summary").render())
            habits_text = str(pilot.app.screen.query_one("#habits_summary").render())
            assert "Tasks" in tasks_text
            assert "Habits" in habits_text

    asyncio.run(check_dashboard())


def test_pressing_t_navigates_to_tasks_screen():
    async def check_navigation():
        app = AviOSApp()
        async with app.run_test() as pilot:
            await pilot.press("t")
            assert type(pilot.app.screen).__name__ == "TasksScreen"

    asyncio.run(check_navigation())
