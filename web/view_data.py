"""Build template data from AviOS's existing feature helpers."""

from datetime import datetime

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
from expense_options.display import (
    get_archived_expenses_newest_first,
    get_deleted_expenses_newest_first,
    get_expenses_newest_first,
)
from expense_options.state import expense_list
from habit_options.state import get_today_date, habit_list
from habit_options.streaks import get_current_streak
from profile_options.state import get_user_name
from task_options.display import get_archived_task_order, get_deleted_task_order, get_task_order
from task_options.state import task_list


def indexed(items, indexes=None):
    if indexes is None:
        indexes = range(len(items))
    return [{"index": index, **items[index]} for index in indexes]


def dashboard_data():
    open_tasks, done_tasks = get_task_counts()
    habits_done, habit_total = get_habit_counts()
    _, totals, balance = get_expense_balance()
    return {
        "name": get_user_name(),
        "focus": get_daily_focus(),
        "mood": get_today_mood(),
        "note": get_today_note(),
        "open_tasks": open_tasks,
        "done_tasks": done_tasks,
        "task_streak": get_task_day_streak(),
        "habits_done": habits_done,
        "habit_total": habit_total,
        "habit_streak": get_best_habit_streak(),
        "pay": totals["pay"],
        "receive": totals["receive"],
        "balance": balance,
        "progress": get_progress_message(),
        "activity": get_recent_activity(),
    }


def tasks_data():
    return {
        "active": indexed(task_list, get_task_order()),
        "archived": indexed(task_list, get_archived_task_order()),
        "deleted": indexed(task_list, get_deleted_task_order()),
    }


def habits_data():
    today = get_today_date()
    today_date = datetime.strptime(today, "%d-%m-%Y").date()
    return {
        "today": today,
        "habits": [
            {**habit, "index": index, "streak": get_current_streak(habit, today_date)}
            for index, habit in enumerate(habit_list)
        ],
    }


def expenses_data():
    return {
        "active": indexed(expense_list, get_expenses_newest_first()),
        "archived": indexed(expense_list, get_archived_expenses_newest_first()),
        "deleted": indexed(expense_list, get_deleted_expenses_newest_first()),
    }
