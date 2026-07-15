# Pinned task helpers for AviOS

from task_options.state import save_tasks, task_list


def get_pinned_task():
    for task in task_list:
        if (
            task.get("pinned", False)
            and not task.get("archived", False)
            and not task.get("deleted", False)
        ):
            return task

    return None


def pin_task(task_index):
    for task in task_list:
        task["pinned"] = False

    task_list[task_index]["pinned"] = True
    save_tasks()
    print("\n Pinned task.")


def unpin_task(task_index):
    task_list[task_index]["pinned"] = False
    save_tasks()
    print("\n Unpinned task.")
