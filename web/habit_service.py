"""Habit operations used by the AviOS web interface."""

from fastapi import HTTPException

from habit_options.done_today import mark_habit_done
from habit_options.state import get_current_timestamp, habit_list, save_habits


CATEGORIES = ["Movement", "Sleep", "Nutrition", "Mind", "Learning", "Social", "General"]


def get_habit(habit_index):
    if habit_index < 0 or habit_index >= len(habit_list):
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit_list[habit_index]


def create_habit(name, category):
    name = name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Habit name is required")
    if category not in CATEGORIES:
        category = "General"
    habit = {
        "name": name,
        "category": category,
        "created_at": get_current_timestamp(),
        "done_dates": [],
    }
    habit_list.append(habit)
    save_habits()
    return len(habit_list) - 1, habit


def complete_habit(habit_index):
    get_habit(habit_index)
    return mark_habit_done(habit_index)
