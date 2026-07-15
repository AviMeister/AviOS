# Dashboard metrics for AviOS

from datetime import datetime, timedelta

from expense_options.summary import calculate_totals
from expense_options.state import expense_list
from habit_options.state import get_today_date, habit_list
from habit_options.streaks import get_current_streak
from task_options.state import task_list


def get_task_counts():
    active_tasks = [
        task
        for task in task_list
        if not task.get("archived", False) and not task.get("deleted", False)
    ]
    done_tasks = [task for task in active_tasks if task.get("completed", False)]

    return len(active_tasks) - len(done_tasks), len(done_tasks)


def get_tasks_done_today_count():
    today = get_today_date()
    return sum(
        1
        for task in task_list
        for done_entry in task.get("done_history", [])
        if done_entry.get("done_at", "").startswith(today)
    )


def get_day_streak_from_dates(done_dates, today):
    streak = 0
    current_day = today

    while current_day in done_dates:
        streak += 1
        current_day -= timedelta(days=1)

    return streak


def get_task_day_streak():
    done_dates = set()

    for task in task_list:
        for done_entry in task.get("done_history", []):
            done_date_text = done_entry.get("done_at", "")[:10]

            try:
                done_dates.add(datetime.strptime(done_date_text, "%d-%m-%Y").date())
            except ValueError:
                pass

    today = datetime.strptime(get_today_date(), "%d-%m-%Y").date()

    return get_day_streak_from_dates(done_dates, today)


def get_habit_counts():
    today = get_today_date()
    done_today = [habit for habit in habit_list if today in habit["done_dates"]]

    return len(done_today), len(habit_list)


def get_best_habit_streak():
    today = datetime.strptime(get_today_date(), "%d-%m-%Y").date()

    if len(habit_list) == 0:
        return 0

    return max(get_current_streak(habit, today) for habit in habit_list)


def get_expense_balance():
    totals_by_currency, combined_totals = calculate_totals(expense_list)
    balance = combined_totals["receive"] - combined_totals["pay"]

    return totals_by_currency, combined_totals, balance


def get_progress_message():
    tasks_done_today = get_tasks_done_today_count()
    habits_done, habit_total = get_habit_counts()

    if tasks_done_today > 0 and habits_done > 0:
        return "Good. You moved both tasks and habits forward today."
    if habits_done == habit_total and habit_total > 0:
        return "Excellent consistency today."
    if tasks_done_today > 0:
        return "Nice. You completed a task today."
    if habits_done > 0:
        return "Good. You kept a habit alive today."

    return "Start small. One useful action is enough."
