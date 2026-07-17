# Builds the Textual screen that lists tasks and lets you mark them done.

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header

from task_options.display import get_task_order, get_task_status
from task_options.habit_detection import apply_habit_decision, habit_prompt_is_due
from task_options.state import task_list
from task_options.task_actions import mark_task_done, mark_task_open
from tui.habit_prompt_modal import HabitPromptModal


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
        self._load_rows()

    def _load_rows(self, focus_task_index: int | None = None) -> None:
        table = self.query_one(DataTable)
        table.clear()

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
                key=str(task_index),
            )

        if table.row_count == 0:
            table.add_row("-", "No tasks yet", "-", "-", "-", key="empty")
            return

        if focus_task_index is not None:
            try:
                table.move_cursor(row=table.get_row_index(str(focus_task_index)))
            except KeyError:
                pass

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        key = event.row_key.value

        if not key or not key.isdigit():
            return

        task_index = int(key)
        task = task_list[task_index]

        if task.get("completed", False):
            mark_task_open(task_index)
            self.notify("Marked open")
            self._load_rows(focus_task_index=task_index)
            return

        mark_task_done(task_index)
        self.notify("Marked done")

        if habit_prompt_is_due(task_index):
            self.app.push_screen(
                HabitPromptModal(task["name"]),
                lambda accepted: self._handle_habit_decision(task_index, accepted),
            )
        else:
            self._load_rows(focus_task_index=task_index)

    def _handle_habit_decision(self, task_index: int, accepted: bool) -> None:
        apply_habit_decision(task_index, accepted)
        self.notify("Saved as a habit idea" if accepted else "Kept as a regular task")
        self._load_rows(focus_task_index=task_index)
