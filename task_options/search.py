# Search tasks option for AviOS

from task_options.display import get_search_task_order, print_task_line
from task_options.state import task_list


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
