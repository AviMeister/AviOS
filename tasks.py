# Task related features for AviOS

task_list = []


def open_tasks():
    print("\n Opening Tasks...")

    task_name = input("\n Enter a new task: ").strip()

    if task_name == "":
        print("\n Task cannot be empty.")
    else:
        task_list.append(task_name)
        print(f"\n Added task: {task_name}")
