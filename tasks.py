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


def show_task_summary():
    done_count = sum(1 for task in task_list if task["completed"])
    open_count = len(task_list) - done_count

    print(f"\n Open: {open_count} | Done: {done_count} | Total: {len(task_list)}")


def get_task_order():
    open_tasks = [
        task_index for task_index, task in enumerate(task_list) if not task["completed"]
    ]
    done_tasks = [
        task_index for task_index, task in enumerate(task_list) if task["completed"]
    ]

    return open_tasks + done_tasks


def view_tasks():
    print("\n Tasks:")

    if len(task_list) == 0:
        print(" No tasks yet.")
    else:
        for task_number, task_index in enumerate(get_task_order(), start=1):
            task = task_list[task_index]
            status = "x" if task["completed"] else " "
            print(f" {task_number}. [{status}] {task['name']}")

        show_task_summary()


def choose_task():
    task_choice = input("\n Select a task number, or press Enter to go back: ").strip()

    if task_choice == "":
        return None

    if not task_choice.isdigit():
        print("\n Please enter a task number.")
        return None

    task_number = int(task_choice)

    task_order = get_task_order()

    if task_number < 1 or task_number > len(task_order):
        print("\n That task number does not exist.")
        return None

    return task_order[task_number - 1]


def add_task():
    task_name = input("\n Enter a new task: ").strip()

    if task_name == "":
        print("\n Task cannot be empty.")
    else:
        task_list.append({"name": task_name, "completed": False})
        save_tasks()
        print(f"\n Added: {task_name}")


def mark_task_done(task_index):
    task_list[task_index]["completed"] = True
    save_tasks()
    print("\n Marked done.")


def delete_task(task_index):
    deleted_task = task_list.pop(task_index)
    save_tasks()
    print(f"\n Deleted: {deleted_task['name']}")


def manage_task(task_index):
    while True:
        task = task_list[task_index]
        status = "Done" if task["completed"] else "Open"

        print(f"\n {task['name']} ({status})")
        print(" 1. Mark done")
        print(" 2. Delete")
        print(" 3. Back")

        choice = input("\n Choose an option: ").strip()

        if choice == "1":
            mark_task_done(task_index)
            break
        elif choice == "2":
            delete_task(task_index)
            break
        elif choice == "3":
            break
        else:
            print("\n Choose 1, 2 or 3.")


def open_task_view():
    view_tasks()

    if len(task_list) == 0:
        return

    task_index = choose_task()

    if task_index is not None:
        manage_task(task_index)


def clear_done_tasks():
    global task_list

    done_count = 0

    for task in task_list:
        if task["completed"]:
            done_count += 1

    if done_count == 0:
        print("\n No done tasks to clear.")
        return

    task_list = [task for task in task_list if not task["completed"]]
    save_tasks()

    print(f"\n Cleared {done_count} done task(s).")


def open_tasks():
    while True:
        print("\n Tasks")
        print(" 1. Add")
        print(" 2. View")
        print(" 3. Clear Done")
        print(" 4. Back")

        choice = input("\n Choose an option: ").strip()

        if choice == "1":
            add_task()
            pause()
        elif choice == "2":
            open_task_view()
            pause()
        elif choice == "3":
            clear_done_tasks()
            pause()
        elif choice == "4":
            break
        else:
            print("\n Choose 1, 2, 3 or 4.")
