# Habits menu for AviOS

from habit_options.add import add_habit
from habit_options.done_today import mark_habit_done_today
from habit_options.view import view_habits


def pause():
    input("\n Press Enter to continue...")


def open_habits():
    while True:
        print("\n Habits")
        print(" 1. Add")
        print(" 2. View")
        print(" 3. Done Today")
        print(" 4. Back")

        choice = input("\n Choose an option: ").strip()

        if choice == "1":
            add_habit()
            pause()
        elif choice == "2":
            view_habits()
            pause()
        elif choice == "3":
            mark_habit_done_today()
            pause()
        elif choice == "4":
            break
        else:
            print("\n Choose 1, 2, 3 or 4.")
