# Habit related features for AviOS

import json
from datetime import datetime
from pathlib import Path

HABITS_FILE = Path(__file__).parent / "habits.json"


def get_current_timestamp():
    return datetime.now().strftime("%d-%m-%Y %I:%M %p").lower()


def get_today_date():
    return datetime.now().strftime("%d-%m-%Y")


def prepare_habits(habits):
    for habit in habits:
        habit.setdefault("category", "General")
        habit.setdefault("created_at", "Unknown")
        habit.setdefault("done_dates", [])

    return habits


def load_habits():
    if not HABITS_FILE.exists():
        return []

    try:
        with HABITS_FILE.open("r", encoding="utf-8") as file:
            return prepare_habits(json.load(file))
    except json.JSONDecodeError:
        print("\n Could not read saved habits. Starting empty.")
        return []


def save_habits():
    with HABITS_FILE.open("w", encoding="utf-8") as file:
        json.dump(habit_list, file, indent=4)


habit_list = load_habits()


def pause():
    input("\n Press Enter to continue...")


def choose_category():
    categories = ["Movement", "Sleep", "Nutrition", "Mind", "Learning", "Social"]

    print("\n Category:")

    for number, category in enumerate(categories, start=1):
        print(f" {number}. {category}")

    choice = input("\n Choose a category: ").strip()

    if not choice.isdigit():
        print("\n Using General for now.")
        return "General"

    category_number = int(choice)

    if category_number < 1 or category_number > len(categories):
        print("\n Using General for now.")
        return "General"

    return categories[category_number - 1]


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


def add_habit():
    habit_name = input("\n Enter a new habit: ").strip()

    if habit_name == "":
        print("\n Habit cannot be empty.")
        return

    category = choose_category()

    habit_list.append(
        {
            "name": habit_name,
            "category": category,
            "created_at": get_current_timestamp(),
            "done_dates": [],
        }
    )
    save_habits()
    print(f"\n Added habit: {habit_name}")


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
