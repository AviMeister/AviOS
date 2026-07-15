# Task related features for AviOS

import json
from datetime import datetime
from pathlib import Path

TASKS_FILE = Path(__file__).parent / "tasks.json"


def prepare_tasks(tasks):
    for task in tasks:
        task.setdefault("completed", False)
        task.setdefault("archived", False)
        task.setdefault("deleted", False)
        task.setdefault("created_at", "Unknown")

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


task_list = load_tasks()


def pause():
    input("\n Press Enter to continue...")


def show_task_summary():
    visible_tasks = [
        task
        for task in task_list
        if not task.get("archived", False) and not task.get("deleted", False)
    ]
    done_count = sum(1 for task in visible_tasks if task.get("completed", False))
    open_count = len(visible_tasks) - done_count

    print(f"\n Open: {open_count} | Done: {done_count} | Total: {len(visible_tasks)}")


def get_task_order():
    open_tasks = [
        task_index
        for task_index, task in enumerate(task_list)
        if not task.get("completed", False)
        and not task.get("archived", False)
        and not task.get("deleted", False)
    ]
    done_tasks = [
        task_index
        for task_index, task in enumerate(task_list)
        if task.get("completed", False)
        and not task.get("archived", False)
        and not task.get("deleted", False)
    ]

    return open_tasks + done_tasks


def get_archived_task_order():
    return [
        task_index
        for task_index, task in enumerate(task_list)
        if task.get("archived", False) and not task.get("deleted", False)
    ]


def get_search_task_order(search_text):
    search_text = search_text.lower()

    open_tasks = []
    done_tasks = []
    archived_tasks = []
    deleted_tasks = []

    for task_index, task in enumerate(task_list):
        task_name = task["name"].lower()

        if search_text not in task_name:
            continue

        if task.get("deleted", False):
            deleted_tasks.append(task_index)
        elif task.get("archived", False):
            archived_tasks.append(task_index)
        elif task.get("completed", False):
            done_tasks.append(task_index)
        else:
            open_tasks.append(task_index)

    return open_tasks + done_tasks + archived_tasks + deleted_tasks


def get_task_status(task):
    if task.get("deleted", False):
        return "Deleted"
    if task.get("archived", False):
        return "Archived"
    if task.get("completed", False):
        return "Done"

    return "Open"


def print_task_line(task_number, task):
    status = "x" if task.get("completed", False) else " "
    created_at = task.get("created_at", "Unknown")
    task_status = get_task_status(task)
    print(f" {task_number}. [{status}] {task['name']} | {task_status} | Created: {created_at}")


def view_tasks():
    print("\n Tasks:")

    task_order = get_task_order()

    if len(task_order) == 0:
        print(" No tasks yet.")
    else:
        for task_number, task_index in enumerate(task_order, start=1):
            task = task_list[task_index]
            print_task_line(task_number, task)

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
        task_list.append(
            {
                "name": task_name,
                "completed": False,
                "archived": False,
                "deleted": False,
                "created_at": datetime.now().strftime("%Y-%m-%d"),
            }
        )
        save_tasks()
        print(f"\n Added: {task_name}")


def mark_task_done(task_index):
    task_list[task_index]["completed"] = True
    save_tasks()
    print("\n Marked done.")


def mark_task_open(task_index):
    task_list[task_index]["completed"] = False
    save_tasks()
    print("\n Marked open.")


def edit_task(task_index):
    current_name = task_list[task_index]["name"]
    new_name = input(f"\n Rename '{current_name}' to: ").strip()

    if new_name == "":
        print("\n Name was not changed.")
        return

    task_list[task_index]["name"] = new_name
    save_tasks()
    print("\n Task renamed.")


def delete_task(task_index):
    confirm = input("\n Delete this task? y/n: ").strip().lower()

    if confirm != "y":
        print("\n Kept task.")
        return

    task_list[task_index]["deleted"] = True
    task_list[task_index]["deleted_at"] = datetime.now().strftime("%Y-%m-%d")
    save_tasks()
    print("\n Moved to deleted.")


def archive_task(task_index):
    task_list[task_index]["archived"] = True
    save_tasks()
    print("\n Archived task.")


def manage_task(task_index):
    while True:
        task = task_list[task_index]
        status = "Done" if task.get("completed", False) else "Open"

        print(f"\n {task['name']} ({status})")

        if task.get("completed", False):
            print(" 1. Mark open")
            print(" 2. Edit")
            print(" 3. Archive")
            print(" 4. Delete")
            print(" 5. Back")
        else:
            print(" 1. Mark done")
            print(" 2. Edit")
            print(" 3. Archive")
            print(" 4. Delete")
            print(" 5. Back")

        choice = input("\n Choose an option: ").strip()

        if choice == "1" and task.get("completed", False):
            mark_task_open(task_index)
            break
        elif choice == "1":
            mark_task_done(task_index)
            break
        elif choice == "2":
            edit_task(task_index)
            break
        elif choice == "3":
            archive_task(task_index)
            break
        elif choice == "4":
            delete_task(task_index)
            break
        elif choice == "5":
            break
        else:
            print("\n Choose one of the menu numbers.")


def open_task_view():
    view_tasks()

    if len(get_task_order()) == 0:
        return

    task_index = choose_task()

    if task_index is not None:
        manage_task(task_index)


def show_archived_tasks():
    archived_tasks = get_archived_task_order()

    print("\n Archived:")

    if len(archived_tasks) == 0:
        print(" No archived tasks yet.")
        return

    for task_number, task_index in enumerate(archived_tasks, start=1):
        task = task_list[task_index]
        print_task_line(task_number, task)


def search_tasks():
    search_text = input("\n Search for: ").strip()

    if search_text == "":
        print("\n Search cannot be empty.")
        return

    search_results = get_search_task_order(search_text)

    print("\n Search results:")

    if len(search_results) == 0:
        print(" No matching tasks found.")
        return

    for task_number, task_index in enumerate(search_results, start=1):
        task = task_list[task_index]
        print_task_line(task_number, task)


def open_tasks():
    while True:
        print("\n Tasks")
        print(" 1. Add")
        print(" 2. View")
        print(" 3. Search")
        print(" 4. Archived")
        print(" 5. Back")

        choice = input("\n Choose an option: ").strip()

        if choice == "1":
            add_task()
            pause()
        elif choice == "2":
            open_task_view()
            pause()
        elif choice == "3":
            search_tasks()
            pause()
        elif choice == "4":
            show_archived_tasks()
            pause()
        elif choice == "5":
            break
        else:
            print("\n Choose 1, 2, 3, 4 or 5.")
