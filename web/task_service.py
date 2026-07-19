"""Task operations used by the AviOS web interface."""

from fastapi import HTTPException

from dashboard_options.activity import add_activity
from task_options.pinned import pin_task, unpin_task
from task_options.state import get_current_timestamp, save_tasks, task_list
from task_options.task_actions import archive_task, mark_task_done, mark_task_open


def get_task(task_index):
    if task_index < 0 or task_index >= len(task_list):
        raise HTTPException(status_code=404, detail="Task not found")
    return task_list[task_index]


def create_task(name):
    name = name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Task name is required")
    task = {
        "name": name,
        "completed": False,
        "archived": False,
        "deleted": False,
        "created_at": get_current_timestamp(),
        "done_history": [],
        "habit_candidate": False,
        "habit_prompt_dismissed": False,
        "pinned": False,
    }
    task_list.append(task)
    save_tasks()
    add_activity(f"Added task: {name}")
    return len(task_list) - 1, task


def rename_task(task_index, name):
    task = get_task(task_index)
    name = name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Task name is required")
    task["name"] = name
    save_tasks()
    return task


_VALID_TASK_ACTIONS = {"done", "open", "pin", "unpin", "archive", "delete", "restore", "purge"}


def apply_task_action(task_index, action):
    task = get_task(task_index)
    if action not in _VALID_TASK_ACTIONS:
        raise HTTPException(status_code=400, detail="Unsupported task action")
    if action == "done" and not task.get("completed", False):
        mark_task_done(task_index)
    elif action == "open" and task.get("completed", False):
        mark_task_open(task_index)
    elif action == "pin":
        pin_task(task_index)
    elif action == "unpin":
        unpin_task(task_index)
    elif action == "archive":
        archive_task(task_index)
    elif action == "delete":
        task["deleted"] = True
        task["deleted_at"] = get_current_timestamp()
        save_tasks()
    elif action == "restore":
        task["deleted"] = False
        task.pop("deleted_at", None)
        save_tasks()
    elif action == "purge":
        if not task.get("deleted", False):
            raise HTTPException(status_code=400, detail="Task must be deleted before purging")
        task_list.pop(task_index)
        save_tasks()
        return None
    return task
