# Expenses menu for AviOS

from expense_options.add import add_expense
from expense_options.archived import show_archived_expenses
from expense_options.deleted import open_deleted_expenses
from expense_options.search import search_expenses
from expense_options.summary import show_expense_summary
from expense_options.view import open_expense_view


def pause():
    input("\n Press Enter to continue...")


def open_expenses():
    while True:
        print("\n Expenses")
        print(" 1. Add")
        print(" 2. View")
        print(" 3. Search")
        print(" 4. Summary")
        print(" 5. Archived")
        print(" 6. Deleted")
        print(" 7. Back")

        choice = input("\n Choose an option: ").strip()

        if choice == "1":
            add_expense()
            pause()
        elif choice == "2":
            open_expense_view()
            pause()
        elif choice == "3":
            search_expenses()
            pause()
        elif choice == "4":
            show_expense_summary()
            pause()
        elif choice == "5":
            show_archived_expenses()
            pause()
        elif choice == "6":
            open_deleted_expenses()
            pause()
        elif choice == "7":
            break
        else:
            print("\n Choose 1, 2, 3, 4, 5, 6 or 7.")
