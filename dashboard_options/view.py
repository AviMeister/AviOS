# Today dashboard for AviOS

from dashboard_options.focus import get_daily_focus
from dashboard_options.metrics import (
    get_best_habit_streak,
    get_expense_balance,
    get_habit_counts,
    get_progress_message,
    get_task_day_streak,
    get_task_counts,
)


def show_today_dashboard():
    open_tasks, done_tasks = get_task_counts()
    habits_done, habit_total = get_habit_counts()
    _, combined_totals, balance = get_expense_balance()
    daily_focus = get_daily_focus()
    best_streak = get_best_habit_streak()
    task_streak = get_task_day_streak()

    print("\n Today")
    print(f" Focus: {daily_focus or 'Not set yet'}")

    print("\n Tasks")
    print(f" Open: {open_tasks} | Done: {done_tasks} | Day streak: {task_streak}")

    print("\n Habits")
    print(f" Done today: {habits_done}/{habit_total} | Best streak: {best_streak}")

    print("\n Expenses")
    print(f" To pay: {combined_totals['pay']:.2f} EUR")
    print(f" To receive: {combined_totals['receive']:.2f} EUR")
    print(f" Balance: {balance:.2f} EUR")

    print(f"\n {get_progress_message()}")
