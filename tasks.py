# Task related features for AviOS

task_list = []


def view_tasks():
    print("\n Your tasks:")

    if len(task_list) == 0:
        print(" No tasks yet.")
    else:
        for task_number, task in enumerate(task_list, start=1):
            status = "x" if task["completed"] else " "
            print(f" {task_number}. [{status}] {task['name']}")


def add_task():
    task_name = input("\n Enter a new task: ").strip()

    if task_name == "":
        print("\n Task cannot be empty.")
    else:
        task_list.append({"name": task_name, "completed": False})
        print(f"\n Added task: {task_name}")


def complete_task():
    view_tasks()

    if len(task_list) == 0:
        return

    task_choice = input("\n Which task did you complete? ").strip()

    if not task_choice.isdigit():
        print("\n Please enter a task number.")
        return

    task_number = int(task_choice)

    if task_number < 1 or task_number > len(task_list):
        print("\n That task number does not exist.")
        return

    task_list[task_number - 1]["completed"] = True
    print("\n Task marked as complete.")


def open_tasks():
    print("\n Opening Tasks...")

    while True:
        print("\n Tasks Menu")
        print(" 1. View tasks")
        print(" 2. Add task")
        print(" 3. Complete task")
        print(" 4. Back")

        choice = input("\n Choose an option: ").strip()

        if choice == "1":
            view_tasks()
        elif choice == "2":
            add_task()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            print("\n Going back to the main menu...")
            break
        else:
            print("\n Invalid input. Choose 1, 2, 3 or 4.")
