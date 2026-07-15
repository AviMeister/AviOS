# View habits option for AviOS

from habit_options.state import get_today_date, habit_list


def view_habits():
    print("\n Habits:")

    if len(habit_list) == 0:
        print(" No habits yet.")
        return

    today = get_today_date()

    for habit_number, habit in enumerate(habit_list, start=1):
        status = "x" if today in habit["done_dates"] else " "
        total_done = len(habit["done_dates"])
        print(
            f" {habit_number}. [{status}] {habit['name']} | {habit['category']} | "
            f"Done: {total_done} | Created: {habit['created_at']}"
        )


def choose_habit():
    habit_choice = input("\n Select a habit, or press Enter to go back: ").strip()

    if habit_choice == "":
        return None

    if not habit_choice.isdigit():
        print("\n Please enter a habit number.")
        return None

    habit_number = int(habit_choice)

    if habit_number < 1 or habit_number > len(habit_list):
        print("\n That habit number does not exist.")
        return None

    return habit_number - 1
