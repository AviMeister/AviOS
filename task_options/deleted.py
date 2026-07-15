# Deleted tasks option for AviOS

from task_options.display import get_deleted_task_order, print_task_line
from task_options.state import save_tasks, task_list


def show_deleted_tasks():
    deleted_tasks = get_deleted_task_order()

    print("\n Deleted:")

    if len(deleted_tasks) == 0:
        print(" No deleted tasks yet.")
        return

    for task_number, task_index in enumerate(deleted_tasks, start=1):
        task = task_list[task_index]
        print_task_line(task_number, task)


def choose_deleted_task():
    task_choice = input("\n Select a deleted task, or press Enter to go back: ").strip()

    if task_choice == "":
        return None

    if not task_choice.isdigit():
        print("\n Please enter a task number.")
        return None

    task_number = int(task_choice)
    deleted_tasks = get_deleted_task_order()

    if task_number < 1 or task_number > len(deleted_tasks):
        print("\n That deleted task number does not exist.")
        return None

    return deleted_tasks[task_number - 1]


def restore_deleted_task(task_index):
    task_list[task_index]["deleted"] = False
    task_list[task_index].pop("deleted_at", None)
    save_tasks()
    print("\n Restored task.")


def permanently_delete_task(task_index):
    confirm = input("\n Delete forever? y/n: ").strip().lower()

    if confirm != "y":
        print("\n Kept task.")
        return

    deleted_task = task_list.pop(task_index)
    save_tasks()
    print(f"\n Deleted forever: {deleted_task['name']}")


def manage_deleted_task(task_index):
    task = task_list[task_index]

    print(f"\n {task['name']} (Deleted)")
    print(" 1. Restore")
    print(" 2. Delete forever")
    print(" 3. Back")

    choice = input("\n Choose an option: ").strip()

    if choice == "1":
        restore_deleted_task(task_index)
    elif choice == "2":
        permanently_delete_task(task_index)
    elif choice == "3":
        return
    else:
        print("\n Choose 1, 2 or 3.")


def open_deleted_tasks():
    show_deleted_tasks()

    if len(get_deleted_task_order()) == 0:
        return

    task_index = choose_deleted_task()

    if task_index is not None:
        manage_deleted_task(task_index)
