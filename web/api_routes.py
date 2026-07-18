"""JSON endpoints for AviOS."""

from fastapi import APIRouter

from dashboard_options.metrics import get_expense_balance, get_habit_counts, get_task_counts
from expense_options.state import expense_list
from habit_options.state import habit_list
from task_options.state import task_list
from web import expense_service, habit_service, task_service
from web.schemas import ExpenseCreate, HabitCreate, TaskCreate


router = APIRouter(tags=["api"])


def indexed(items):
    return [{"index": index, **item} for index, item in enumerate(items)]


@router.get("/tasks")
def get_tasks():
    return indexed(task_list)


@router.post("/tasks", status_code=201)
def create_task(data: TaskCreate):
    index, task = task_service.create_task(data.name)
    return {"index": index, **task}


@router.post("/tasks/{task_index}/{action}")
def change_task(task_index: int, action: str):
    task = task_service.apply_task_action(task_index, action)
    return {"changed": True, "task": task}


@router.get("/habits")
def get_habits():
    return indexed(habit_list)


@router.post("/habits", status_code=201)
def create_habit(data: HabitCreate):
    index, habit = habit_service.create_habit(data.name, data.category)
    return {"index": index, **habit}


@router.post("/habits/{habit_index}/done")
def complete_habit(habit_index: int):
    changed = habit_service.complete_habit(habit_index)
    return {"changed": changed, "habit": habit_service.get_habit(habit_index)}


@router.get("/expenses")
def get_expenses():
    return indexed(expense_list)


@router.post("/expenses", status_code=201)
def create_expense(data: ExpenseCreate):
    index, expense = expense_service.create_expense(
        data.description,
        data.amount,
        data.currency,
        data.direction,
        data.category,
        data.exchange_rate_to_eur,
    )
    return {"index": index, **expense}


@router.post("/expenses/{expense_index}/{action}")
def change_expense(expense_index: int, action: str):
    expense = expense_service.apply_expense_action(expense_index, action)
    return {"changed": True, "expense": expense}


@router.get("/dashboard")
def dashboard_summary():
    _, totals, balance = get_expense_balance()
    return {"tasks": get_task_counts(), "habits": get_habit_counts(), "expenses": totals, "balance": balance}
