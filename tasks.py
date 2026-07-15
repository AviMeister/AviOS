# Task related features for AviOS

import json
from pathlib import Path

TASKS_FILE = Path(__file__).parent / "tasks.json"


def load_tasks():
    if not TASKS_FILE.exists():
        return []

    try:
        with TASKS_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("\n Could not read saved tasks. Starting empty.")
        return []


def save_tasks():
    with TASKS_FILE.open("w", encoding="utf-8") as file:
        json.dump(task_list, file, indent=4)


task_list = load_tasks()


def pause():
    input("\n Press Enter to continue...")


def view_tasks():
    print("\n Tasks:")

    if len(task_list) == 0:
        print(" No tasks yet.")
    else:
        for task_number, task in enumerate(task_list, start=1):
            status = "x" if task["completed"] else " "
            print(f" {task_number}. [{status}] {task['name']}")


def add_task():
    task_name = input("\n Enter a new task: ").strip()

    if task_name == "":
        print("\n Task cannot be empty.")
    else:
        task_list.append({"name": task_name, "completed": False})
        save_tasks()
        print(f"\n Added: {task_name}")


def complete_task():
    view_tasks()

    if len(task_list) == 0:
        return

    task_choice = input("\n Task number: ").strip()

    if not task_choice.isdigit():
        print("\n Please enter a task number.")
        return

    task_number = int(task_choice)

    if task_number < 1 or task_number > len(task_list):
        print("\n That task number does not exist.")
        return

    task_list[task_number - 1]["completed"] = True
    save_tasks()
    print("\n Marked done.")


def delete_task():
    view_tasks()

    if len(task_list) == 0:
        return

    task_choice = input("\n Delete task number: ").strip()

    if not task_choice.isdigit():
        print("\n Please enter a task number.")
        return

    task_number = int(task_choice)

    if task_number < 1 or task_number > len(task_list):
        print("\n That task number does not exist.")
        return

    deleted_task = task_list.pop(task_number - 1)
    save_tasks()
    print(f"\n Deleted: {deleted_task['name']}")


def open_tasks():
    while True:
        print("\n Tasks")
        print(" 1. View")
        print(" 2. Add")
        print(" 3. Done")
        print(" 4. Delete")
        print(" 5. Back")

        choice = input("\n Choose an option: ").strip()

        if choice == "1":
            view_tasks()
            pause()
        elif choice == "2":
            add_task()
            pause()
        elif choice == "3":
            complete_task()
            pause()
        elif choice == "4":
            delete_task()
            pause()
        elif choice == "5":
            break
        else:
            print("\n Choose 1, 2, 3, 4 or 5.")
