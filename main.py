# AviOS: This is where AviOS starts. Light intro, tone, art/visual
# Will adjust intro text later maybe with stylings
# Greet the user when AviOS(software) launches

import datetime
import time

from dashboard import open_dashboard
from expenses import open_expenses
from habits import open_habits
from profile_options.state import get_user_name, set_user_name
from tasks import open_tasks


def show_header():
    # i need this to get the current date and time on startup so it feels alive
    now = datetime.datetime.now()

    # formatting the date to look readable like "Wednesday, 15 July 2026"
    date_str = now.strftime("%A, %d %B %Y")

    # formatting the time to just show hours and minutes, clean and simple
    time_str = now.strftime("%H:%M")

    # * 40 just repeats the "=" sign 40 times - makes a clean divider line without typing it manually
    print("=" * 40)
    print("  AviOS  |  Personal Life Operating System")

    # f-string lets me drop variables directly into the text - date and time show up live
    print(f"  {date_str}  |  {time_str}")
    print("=" * 40)


def show_main_menu():
    # Show the main menu so the user can pick what they want to do
    print("\n  1.  Tasks")
    print("  2.  Habits")
    print("  3.  Expenses")
    print("  4.  Exit AviOS")


def open_full_menu():
    while True:
        show_header()
        show_main_menu()

        # Wait for the user to type a number and store it
        choice = input("\n  > ").strip()

        # Respond based on what they picked
        # will later replace these with real features
        if choice == "1":
            open_tasks()
        elif choice == "2":
            open_habits()
        elif choice == "3":
            open_expenses()
        elif choice == "4":
            break
        else:
            print("\n  Invalid input. Choose 1, 2, 3 or 4.")


def ensure_profile_name():
    # First time AviOS runs, no name is saved yet - ask once and remember it.
    name = get_user_name()

    if name:
        return

    name = input("\n What should AviOS call you? ").strip()
    set_user_name(name or "there")


def main():
    show_header()
    ensure_profile_name()
    time.sleep(0.5)
    open_dashboard()


if __name__ == "__main__":
    main()
