# Done today habit option for AviOS

from dashboard_options.activity import add_activity
from habit_options.state import get_today_date, habit_list, save_habits
from habit_options.view import choose_habit, view_habits


def mark_habit_done(habit_index):
    today = get_today_date()
    habit = habit_list[habit_index]

    if today in habit["done_dates"]:
        return False

    habit["done_dates"].append(today)
    save_habits()
    add_activity(f"Completed habit: {habit['name']}")
    return True


def mark_habit_done_today():
    view_habits()

    if len(habit_list) == 0:
        return

    habit_index = choose_habit()

    if habit_index is None:
        return

    if mark_habit_done(habit_index):
        print("\n Marked done today.")
    else:
        print("\n Already done today.")
