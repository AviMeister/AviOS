# Shared expense display helpers for AviOS

from expense_options.state import expense_list


def format_money(amount, currency):
    return f"{amount:.2f} {currency}"


def get_converted_amount(expense):
    return expense["amount"] * expense["exchange_rate_to_eur"]


def get_expense_status(expense):
    if expense.get("deleted", False):
        return "Deleted"
    if expense.get("archived", False):
        return "Archived"

    return "Active"


def print_expense_line(expense_number, expense):
    converted_amount = get_converted_amount(expense)
    status = get_expense_status(expense)

    print(
        f" {expense_number}. {expense['description']} | {status} | "
        f"{expense['direction']} | "
        f"{format_money(expense['amount'], expense['currency'])} | "
        f"{expense['category']} | Created: {expense['created_at']} | "
        f"EUR value: {converted_amount:.2f}"
    )


def get_expenses_newest_first():
    active_expenses = [
        expense_index
        for expense_index, expense in enumerate(expense_list)
        if not expense.get("archived", False) and not expense.get("deleted", False)
    ]

    return list(reversed(active_expenses))


def get_archived_expenses_newest_first():
    archived_expenses = [
        expense_index
        for expense_index, expense in enumerate(expense_list)
        if expense.get("archived", False) and not expense.get("deleted", False)
    ]

    return list(reversed(archived_expenses))


def get_deleted_expenses_newest_first():
    deleted_expenses = [
        expense_index
        for expense_index, expense in enumerate(expense_list)
        if expense.get("deleted", False)
    ]

    return list(reversed(deleted_expenses))
