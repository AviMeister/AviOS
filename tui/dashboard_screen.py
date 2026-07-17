# Builds the read-only dashboard screen with AviOS's current daily overview.

from textual import events
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, Static

from dashboard_options.activity import get_recent_activity
from dashboard_options.focus import get_daily_focus
from dashboard_options.metrics import (
    get_best_habit_streak,
    get_expense_balance,
    get_habit_counts,
    get_progress_message,
    get_task_counts,
    get_task_day_streak,
)
from dashboard_options.mood import get_today_mood
from dashboard_options.notes import get_today_note
from profile_options.state import get_user_name
from task_options.pinned import get_pinned_task
from tui.expenses_screen import ExpensesScreen
from tui.habits_screen import HabitsScreen
from tui.tasks_screen import TasksScreen


class DashboardScreen(Screen):
    BINDINGS = [
        ("t", "show_tasks", "Tasks"),
        ("h", "show_habits", "Habits"),
        ("e", "show_expenses", "Expenses"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static(id="today"),
            Static(id="tasks_summary"),
            Static(id="habits_summary"),
            Static(id="expenses_summary"),
            Static(id="progress"),
            Static(id="activity"),
            id="dashboard_body",
        )
        yield Footer()

    def on_mount(self) -> None:
        self._refresh()

    def on_screen_resume(self, event: events.ScreenResume) -> None:
        self._refresh()

    def _refresh(self) -> None:
        open_tasks, done_tasks = get_task_counts()
        habits_done, habit_total = get_habit_counts()
        _, combined_totals, balance = get_expense_balance()
        pinned_task = get_pinned_task()

        name = get_user_name()
        self.query_one("#today", Static).update(
            f"Welcome, {name}!\n\n"
            f"Focus: {get_daily_focus() or 'Not set yet'}\n"
            f"Mood: {get_today_mood() or 'Not checked in'}\n"
            f"Note: {get_today_note() or 'No note yet'}"
        )
        self.query_one("#tasks_summary", Static).update(
            f"Tasks — Open: {open_tasks}  Done: {done_tasks}  "
            f"Day streak: {get_task_day_streak()}\n"
            f"Pinned: {pinned_task['name'] if pinned_task else 'None'}"
        )
        self.query_one("#habits_summary", Static).update(
            f"Habits — Done today: {habits_done}/{habit_total}  "
            f"Best streak: {get_best_habit_streak()}"
        )
        self.query_one("#expenses_summary", Static).update(
            f"Expenses — To pay: {combined_totals['pay']:.2f} EUR  "
            f"To receive: {combined_totals['receive']:.2f} EUR  "
            f"Balance: {balance:.2f} EUR"
        )
        self.query_one("#progress", Static).update(get_progress_message())

        recent = get_recent_activity()[:3]
        lines = "\n".join(f"- {item['message']}" for item in recent) or "(none yet)"
        self.query_one("#activity", Static).update(f"Recent Activity\n{lines}")

    def action_show_tasks(self) -> None:
        self.app.push_screen(TasksScreen())

    def action_show_habits(self) -> None:
        self.app.push_screen(HabitsScreen())

    def action_show_expenses(self) -> None:
        self.app.push_screen(ExpensesScreen())
