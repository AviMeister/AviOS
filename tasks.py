# Tasks menu for AviOS

from task_options.add import add_task
from task_options.archived import show_archived_tasks
from task_options.deleted import open_deleted_tasks
from task_options.search import search_tasks
from task_options.view import open_task_view


def pause():
    input("\n Press Enter to continue...")


def open_tasks():
    while True:
        print("\n Tasks")
        print(" 1. Add")
        print(" 2. View")
        print(" 3. Search")
        print(" 4. Archived")
        print(" 5. Deleted")
        print(" 6. Back")

        choice = input("\n Choose an option: ").strip()

        if choice == "1":
            add_task()
            pause()
        elif choice == "2":
            open_task_view()
            pause()
        elif choice == "3":
            search_tasks()
            pause()
        elif choice == "4":
            show_archived_tasks()
            pause()
        elif choice == "5":
            open_deleted_tasks()
            pause()
        elif choice == "6":
            break
        else:
            print("\n Choose 1, 2, 3, 4, 5 or 6.")
