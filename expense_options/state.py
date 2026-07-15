# Shared expense data for AviOS

import json
from datetime import datetime
from pathlib import Path

EXPENSES_FILE = Path(__file__).parent.parent / "expenses.json"


def get_current_timestamp():
    return datetime.now().strftime("%d-%m-%Y %I:%M %p").lower()


def prepare_expenses(expenses):
    for expense in expenses:
        expense.setdefault("description", "No description")
        expense.setdefault("amount", 0.0)
        expense.setdefault("currency", "EUR")
        expense.setdefault("direction", "pay")
        expense.setdefault("category", "Other")
        expense.setdefault("exchange_rate_to_eur", 1.0)
        expense.setdefault("created_at", "Unknown")

    return expenses


def load_expenses():
    if not EXPENSES_FILE.exists():
        return []

    try:
        with EXPENSES_FILE.open("r", encoding="utf-8") as file:
            return prepare_expenses(json.load(file))
    except json.JSONDecodeError:
        print("\n Could not read saved expenses. Starting empty.")
        return []


def save_expenses():
    with EXPENSES_FILE.open("w", encoding="utf-8") as file:
        json.dump(expense_list, file, indent=4)


expense_list = load_expenses()
