from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header

from task_options.display import get_task_order, get_task_status
from task_options.state import task_list


class TasksScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("b", "app.pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable(id="tasks_table")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.add_columns("Done", "Name", "Status", "Created", "Notes")

        for task_index in get_task_order():
            task = task_list[task_index]
            notes = []
            if task.get("pinned", False):
                notes.append("Pinned")
            if task.get("habit_candidate", False):
                notes.append("Habit idea")
            table.add_row(
                "x" if task.get("completed", False) else " ",
                task["name"],
                get_task_status(task),
                task.get("created_at", "Unknown"),
                ", ".join(notes) or "-",
            )

        if table.row_count == 0:
            table.add_row("-", "No tasks yet", "-", "-", "-")
