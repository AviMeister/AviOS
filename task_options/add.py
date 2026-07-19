# Add task option for AviOS

from dashboard_options.activity import add_activity
from task_options.state import build_task, save_tasks, task_list


def add_task():
    task_name = input("\n Enter a new task: ").strip()

    if task_name == "":
        print("\n Task cannot be empty.")
        return

    task_list.append(build_task(task_name))
    save_tasks()
    add_activity(f"Added task: {task_name}")
    print(f"\n Added: {task_name}")
