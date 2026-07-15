# Today dashboard for AviOS

from dashboard_options.activity import get_recent_activity
from dashboard_options.focus import get_daily_focus
from dashboard_options.metrics import (
    get_best_habit_streak,
    get_expense_balance,
    get_habit_counts,
    get_progress_message,
    get_task_day_streak,
    get_task_counts,
)
from dashboard_options.mood import get_today_mood
from dashboard_options.notes import get_today_note
from task_options.pinned import get_pinned_task


def show_today_dashboard():
    open_tasks, done_tasks = get_task_counts()
    habits_done, habit_total = get_habit_counts()
    _, combined_totals, balance = get_expense_balance()
    daily_focus = get_daily_focus()
    best_streak = get_best_habit_streak()
    task_streak = get_task_day_streak()
    pinned_task = get_pinned_task()
    mood = get_today_mood()
    note = get_today_note()

    print("\n Today")
    print(f" Focus: {daily_focus or 'Not set yet'}")
    print(f" Mood: {mood or 'Not checked in'}")
    print(f" Note: {note or 'No note yet'}")

    print("\n Tasks")
    print(f" Open: {open_tasks} | Done: {done_tasks} | Day streak: {task_streak}")
    print(f" Pinned: {pinned_task['name'] if pinned_task else 'None'}")

    print("\n Habits")
    print(f" Done today: {habits_done}/{habit_total} | Best streak: {best_streak}")

    print("\n Expenses")
    print(f" To pay: {combined_totals['pay']:.2f} EUR")
    print(f" To receive: {combined_totals['receive']:.2f} EUR")
    print(f" Balance: {balance:.2f} EUR")

    print(f"\n {get_progress_message()}")

    recent_activity = get_recent_activity()

    if len(recent_activity) > 0:
        print("\n Recent Activity")

        for activity in recent_activity[:3]:
            print(f" - {activity['message']}")
