# View and manage tasks for AviOS

from task_options.display import get_task_order, print_task_line, show_task_summary
from task_options.state import task_list
from task_options.task_actions import manage_task


def view_tasks():
    print("\n Tasks:")

    task_order = get_task_order()

    if len(task_order) == 0:
        print(" No tasks yet.")
        return

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


def open_task_view():
    view_tasks()

    if len(get_task_order()) == 0:
        return

    task_index = choose_task()

    if task_index is not None:
        manage_task(task_index)
