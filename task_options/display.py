# Shared task display helpers for AviOS

from task_options.state import sort_by_newest, task_list


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

    return sort_by_newest(open_tasks) + sort_by_newest(done_tasks)


def get_archived_task_order():
    archived_tasks = [
        task_index
        for task_index, task in enumerate(task_list)
        if task.get("archived", False) and not task.get("deleted", False)
    ]

    return sort_by_newest(archived_tasks)


def get_deleted_task_order():
    deleted_tasks = [
        task_index for task_index, task in enumerate(task_list) if task.get("deleted", False)
    ]

    return sort_by_newest(deleted_tasks)


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

    return (
        sort_by_newest(open_tasks)
        + sort_by_newest(done_tasks)
        + sort_by_newest(archived_tasks)
        + sort_by_newest(deleted_tasks)
    )


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
    habit_text = " | Habit idea" if task.get("habit_candidate", False) else ""
    print(
        f" {task_number}. [{status}] {task['name']} | {task_status} | "
        f"Created: {created_at}{habit_text}"
    )


def show_task_summary():
    visible_tasks = [
        task
        for task in task_list
        if not task.get("archived", False) and not task.get("deleted", False)
    ]
    done_count = sum(1 for task in visible_tasks if task.get("completed", False))
    open_count = len(visible_tasks) - done_count

    print(f"\n Open: {open_count} | Done: {done_count} | Total: {len(visible_tasks)}")
