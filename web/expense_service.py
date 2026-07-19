"""Expense operations used by the AviOS web interface."""

from fastapi import HTTPException

from dashboard_options.activity import add_activity
from expense_options.state import build_expense, expense_list, get_current_timestamp, save_expenses


CURRENCIES = {"EUR", "USD", "GBP", "SRD"}
DIRECTIONS = {"pay", "receive"}
CATEGORIES = {"Food", "Transport", "Health", "Learning", "Bills", "Fun", "Other"}


def get_expense(expense_index):
    if expense_index < 0 or expense_index >= len(expense_list):
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense_list[expense_index]


def create_expense(description, amount, currency, direction, category, rate):
    description = description.strip()
    if not description:
        raise HTTPException(status_code=400, detail="Description is required")
    if amount <= 0 or rate <= 0:
        raise HTTPException(status_code=400, detail="Amount and rate must be positive")
    currency = currency if currency in CURRENCIES else "EUR"
    direction = direction if direction in DIRECTIONS else "pay"
    category = category if category in CATEGORIES else "Other"
    expense = build_expense(description, amount, currency, direction, category, rate)
    expense_list.append(expense)
    save_expenses()
    add_activity(f"Added expense: {description}")
    return len(expense_list) - 1, expense


def rename_expense(expense_index, description):
    expense = get_expense(expense_index)
    description = description.strip()
    if not description:
        raise HTTPException(status_code=400, detail="Description is required")
    expense["description"] = description
    save_expenses()
    return expense


def apply_expense_action(expense_index, action):
    expense = get_expense(expense_index)
    if action == "archive":
        expense["archived"] = True
    elif action == "delete":
        expense["deleted"] = True
        expense["deleted_at"] = get_current_timestamp()
    elif action == "restore":
        expense["deleted"] = False
        expense.pop("deleted_at", None)
    elif action == "purge":
        if not expense.get("deleted", False):
            raise HTTPException(status_code=400, detail="Expense must be deleted before purging")
        expense_list.pop(expense_index)
        save_expenses()
        return None
    else:
        raise HTTPException(status_code=400, detail="Unsupported expense action")
    save_expenses()
    return expense
