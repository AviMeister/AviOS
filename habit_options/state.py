# Shared habit data for AviOS

import json
from datetime import datetime
from pathlib import Path

HABITS_FILE = Path(__file__).parent.parent / "habits.json"


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
