# Done today habit option for AviOS

from habit_options.state import get_today_date, habit_list, save_habits
from habit_options.view import choose_habit, view_habits


def mark_habit_done_today():
    view_habits()

    if len(habit_list) == 0:
        return

    habit_index = choose_habit()

    if habit_index is None:
        return

    today = get_today_date()
    habit = habit_list[habit_index]

    if today in habit["done_dates"]:
        print("\n Already done today.")
        return

    habit["done_dates"].append(today)
    save_habits()
    print("\n Marked done today.")
