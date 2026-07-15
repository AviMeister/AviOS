# Add task option for AviOS

from dashboard_options.activity import add_activity
from task_options.state import get_current_timestamp, save_tasks, task_list


def add_task():
    task_name = input("\n Enter a new task: ").strip()

    if task_name == "":
        print("\n Task cannot be empty.")
        return

    task_list.append(
        {
            "name": task_name,
            "completed": False,
            "archived": False,
            "deleted": False,
            "created_at": get_current_timestamp(),
            "done_history": [],
            "habit_candidate": False,
            "habit_prompt_dismissed": False,
            "pinned": False,
        }
    )
    save_tasks()
    add_activity(f"Added task: {task_name}")
    print(f"\n Added: {task_name}")
