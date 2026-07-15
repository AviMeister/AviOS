# Archived tasks option for AviOS

from task_options.display import get_archived_task_order, print_task_line
from task_options.state import task_list


def show_archived_tasks():
    archived_tasks = get_archived_task_order()

    print("\n Archived:")

    if len(archived_tasks) == 0:
        print(" No archived tasks yet.")
        return

    for task_number, task_index in enumerate(archived_tasks, start=1):
        task = task_list[task_index]
        print_task_line(task_number, task)
