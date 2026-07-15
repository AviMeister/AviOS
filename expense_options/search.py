# Search expenses option for AviOS

from expense_options.display import print_expense_line
from expense_options.state import expense_list


def search_expenses():
    search_text = input("\n Search for: ").strip().lower()

    if search_text == "":
        print("\n Search cannot be empty.")
        return

    results = []

    for expense_index, expense in enumerate(expense_list):
        searchable_text = (
            f"{expense['description']} {expense['category']} "
            f"{expense['currency']} {expense['direction']}"
        ).lower()

        if search_text in searchable_text:
            results.append(expense_index)

    print("\n Search results:")

    if len(results) == 0:
        print(" No matching expenses found.")
        return

    for expense_number, expense_index in enumerate(reversed(results), start=1):
        expense = expense_list[expense_index]
        print_expense_line(expense_number, expense)
