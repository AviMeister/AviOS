# Builds the read-only Textual screen that shows habits and today's progress.

from datetime import datetime

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header

from habit_options.state import get_today_date, habit_list
from habit_options.streaks import get_current_streak


class HabitsScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("b", "app.pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable(id="habits_table")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.add_columns("Today", "Name", "Category", "Streak", "Total Done")

        today = get_today_date()
        today_date = datetime.strptime(today, "%d-%m-%Y").date()

        for habit in habit_list:
            table.add_row(
                "x" if today in habit["done_dates"] else " ",
                habit["name"],
                habit["category"],
                str(get_current_streak(habit, today_date)),
                str(len(habit["done_dates"])),
            )

        if table.row_count == 0:
            table.add_row("-", "No habits yet", "-", "-", "-")
