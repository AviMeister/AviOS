# Add habit option for AviOS

from habit_options.state import get_current_timestamp, habit_list, save_habits


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
