# Shared task data for AviOS

import json
from datetime import datetime
from pathlib import Path

TASKS_FILE = Path(__file__).parent.parent / "tasks.json"


def prepare_tasks(tasks):
    for task in tasks:
        task.setdefault("completed", False)
        task.setdefault("archived", False)
        task.setdefault("deleted", False)
        task.setdefault("created_at", "Unknown")
        task.setdefault("done_history", [])
        task.setdefault("habit_candidate", False)
        task.setdefault("habit_prompt_dismissed", False)

    return tasks


def load_tasks():
    if not TASKS_FILE.exists():
        return []

    try:
        with TASKS_FILE.open("r", encoding="utf-8") as file:
            return prepare_tasks(json.load(file))
    except json.JSONDecodeError:
        print("\n Could not read saved tasks. Starting empty.")
        return []


def save_tasks():
    with TASKS_FILE.open("w", encoding="utf-8") as file:
        json.dump(task_list, file, indent=4)


def get_current_timestamp():
    return datetime.now().strftime("%d-%m-%Y %I:%M %p").lower()


def get_today_name():
    return datetime.now().strftime("%A")


def parse_created_at(task):
    created_at = task.get("created_at", "Unknown")
    created_at_upper = created_at.upper()

    for date_format in (
        "%d-%m-%Y %I:%M %p",
        "%d-%m-%Y",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
    ):
        try:
            return datetime.strptime(created_at_upper, date_format)
        except ValueError:
            pass

    return datetime.min


def sort_by_newest(task_indexes):
    return sorted(
        task_indexes,
        key=lambda task_index: parse_created_at(task_list[task_index]),
        reverse=True,
    )


task_list = load_tasks()
