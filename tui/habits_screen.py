# Habits screen for the AviOS TUI

from datetime import datetime

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header

from habit_options.done_today import mark_habit_done
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
        self._columns = table.add_columns("Today", "Name", "Category", "Streak", "Total Done")

        for index, habit in enumerate(habit_list):
            table.add_row(*self._row_values(habit), key=str(index))

        if table.row_count == 0:
            table.add_row("-", "No habits yet", "-", "-", "-", key="empty")

    def _row_values(self, habit):
        today = get_today_date()
        today_date = datetime.strptime(today, "%d-%m-%Y").date()

        return (
            "x" if today in habit["done_dates"] else " ",
            habit["name"],
            habit["category"],
            str(get_current_streak(habit, today_date)),
            str(len(habit["done_dates"])),
        )

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        key = event.row_key.value

        if not key or not key.isdigit():
            return

        habit_index = int(key)

        if mark_habit_done(habit_index):
            self.notify("Marked done today")
        else:
            self.notify("Already done today")

        table = self.query_one(DataTable)
        values = self._row_values(habit_list[habit_index])

        for column_key, value in zip(self._columns, values):
            table.update_cell(key, column_key, value)
