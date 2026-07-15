# Deleted expenses option for AviOS

from expense_options.display import get_deleted_expenses_newest_first, print_expense_line
from expense_options.state import expense_list, save_expenses


def show_deleted_expenses():
    deleted_expenses = get_deleted_expenses_newest_first()

    print("\n Deleted expenses:")

    if len(deleted_expenses) == 0:
        print(" No deleted expenses yet.")
        return

    for expense_number, expense_index in enumerate(deleted_expenses, start=1):
        expense = expense_list[expense_index]
        print_expense_line(expense_number, expense)


def choose_deleted_expense():
    choice = input("\n Select a deleted expense, or press Enter to go back: ").strip()

    if choice == "":
        return None

    if not choice.isdigit():
        print("\n Please enter an expense number.")
        return None

    expense_number = int(choice)
    deleted_expenses = get_deleted_expenses_newest_first()

    if expense_number < 1 or expense_number > len(deleted_expenses):
        print("\n That deleted expense number does not exist.")
        return None

    return deleted_expenses[expense_number - 1]


def restore_deleted_expense(expense_index):
    expense_list[expense_index]["deleted"] = False
    expense_list[expense_index].pop("deleted_at", None)
    save_expenses()
    print("\n Restored expense.")


def permanently_delete_expense(expense_index):
    confirm = input("\n Delete forever? y/n: ").strip().lower()

    if confirm != "y":
        print("\n Kept expense.")
        return

    deleted_expense = expense_list.pop(expense_index)
    save_expenses()
    print(f"\n Deleted forever: {deleted_expense['description']}")


def manage_deleted_expense(expense_index):
    expense = expense_list[expense_index]

    print(f"\n {expense['description']} (Deleted)")
    print(" 1. Restore")
    print(" 2. Delete forever")
    print(" 3. Back")

    choice = input("\n Choose an option: ").strip()

    if choice == "1":
        restore_deleted_expense(expense_index)
    elif choice == "2":
        permanently_delete_expense(expense_index)
    elif choice == "3":
        return
    else:
        print("\n Choose 1, 2 or 3.")


def open_deleted_expenses():
    show_deleted_expenses()

    if len(get_deleted_expenses_newest_first()) == 0:
        return

    expense_index = choose_deleted_expense()

    if expense_index is not None:
        manage_deleted_expense(expense_index)
