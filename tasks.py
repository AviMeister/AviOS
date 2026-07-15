# Task related features for AviOS

task_list = []


def view_tasks():
    print("\n Your tasks:")

    if len(task_list) == 0:
        print(" No tasks yet.")
    else:
        for task_number, task in enumerate(task_list, start=1):
            print(f" {task_number}. {task}")


def add_task():
    task_name = input("\n Enter a new task: ").strip()

    if task_name == "":
        print("\n Task cannot be empty.")
    else:
        task_list.append(task_name)
        print(f"\n Added task: {task_name}")


def open_tasks():
    print("\n Opening Tasks...")

    while True:
        print("\n Tasks Menu")
        print(" 1. View tasks")
        print(" 2. Add task")
        print(" 3. Back")

        choice = input("\n Choose an option: ").strip()

        if choice == "1":
            view_tasks()
        elif choice == "2":
            add_task()
        elif choice == "3":
            print("\n Going back to the main menu...")
            break
        else:
            print("\n Invalid input. Choose 1, 2 or 3.")
