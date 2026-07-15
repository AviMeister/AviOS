# End-of-day style review for AviOS

from dashboard_options.metrics import (
    get_expense_balance,
    get_habit_counts,
    get_tasks_done_today_count,
)


def show_end_of_day_review():
    tasks_done = get_tasks_done_today_count()
    habits_done, habit_total = get_habit_counts()
    _, combined_totals, balance = get_expense_balance()

    print("\n Today Review")
    print(f" Tasks done today: {tasks_done}")
    print(f" Habits done today: {habits_done}/{habit_total}")
    print(f" To pay: {combined_totals['pay']:.2f} EUR")
    print(f" To receive: {combined_totals['receive']:.2f} EUR")
    print(f" Balance: {balance:.2f} EUR")
    print("\n Closing AviOS. See you next time.")
