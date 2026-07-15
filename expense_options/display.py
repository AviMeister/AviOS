# Shared expense display helpers for AviOS

from expense_options.state import expense_list


def format_money(amount, currency):
    return f"{amount:.2f} {currency}"


def get_converted_amount(expense):
    return expense["amount"] * expense["exchange_rate_to_eur"]


def print_expense_line(expense_number, expense):
    converted_amount = get_converted_amount(expense)

    print(
        f" {expense_number}. {expense['description']} | {expense['direction']} | "
        f"{format_money(expense['amount'], expense['currency'])} | "
        f"{expense['category']} | Created: {expense['created_at']} | "
        f"EUR value: {converted_amount:.2f}"
    )


def get_expenses_newest_first():
    return list(reversed(range(len(expense_list))))
