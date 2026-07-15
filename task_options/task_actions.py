# Task action helpers for AviOS

from dashboard_options.activity import add_activity
from task_options.habit_detection import ask_about_habit
from task_options.pinned import pin_task, unpin_task
from task_options.state import get_current_timestamp, get_today_name, save_tasks, task_list


def mark_task_done(task_index):
    task_list[task_index]["completed"] = True
    task_list[task_index].setdefault("done_history", [])
    task_list[task_index]["done_history"].append(
        {
            "done_at": get_current_timestamp(),
            "weekday": get_today_name(),
        }
    )
    save_tasks()
    print("\n Marked done.")
    print(" Good. One step forward.")
    add_activity(f"Completed task: {task_list[task_index]['name']}")
    ask_about_habit(task_index)


def mark_task_open(task_index):
    task_list[task_index]["completed"] = False
    save_tasks()
    add_activity(f"Reopened task: {task_list[task_index]['name']}")
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
    task_list[task_index]["deleted_at"] = get_current_timestamp()
    save_tasks()
    print("\n Moved to deleted.")


def archive_task(task_index):
    task_list[task_index]["archived"] = True
    save_tasks()
    add_activity(f"Archived task: {task_list[task_index]['name']}")
    print("\n Archived task.")


def manage_task(task_index):
    task = task_list[task_index]
    status = "Done" if task.get("completed", False) else "Open"

    print(f"\n {task['name']} ({status})")

    if task.get("completed", False):
        print(" 1. Mark open")
    else:
        print(" 1. Mark done")

    print(" 2. Edit")
    print(" 3. Archive")
    print(" 4. Delete")
    if task.get("pinned", False):
        print(" 5. Unpin")
    else:
        print(" 5. Pin")
    print(" 6. Back")

    choice = input("\n Choose an option: ").strip()

    if choice == "1" and task.get("completed", False):
        mark_task_open(task_index)
    elif choice == "1":
        mark_task_done(task_index)
    elif choice == "2":
        edit_task(task_index)
    elif choice == "3":
        archive_task(task_index)
    elif choice == "4":
        delete_task(task_index)
    elif choice == "5":
        if task.get("pinned", False):
            unpin_task(task_index)
        else:
            pin_task(task_index)
    elif choice == "6":
        return
    else:
        print("\n Choose one of the menu numbers.")
