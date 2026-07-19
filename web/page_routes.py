"""Browser pages and form actions for AviOS."""

from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from web import dashboard_service, expense_service, habit_service, task_service, view_data


router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


def render(request, template, data):
    return templates.TemplateResponse(
        request=request,
        name=template,
        context={**data, "message": request.query_params.get("message", "")},
    )


def go(path, message):
    separator = "&" if "?" in path else "?"
    return RedirectResponse(f"{path}{separator}message={quote(message)}", status_code=303)


@router.get("/")
def dashboard_page(request: Request):
    return render(request, "dashboard.html", view_data.dashboard_data())


@router.post("/web/profile")
def update_profile(name: str = Form(...)):
    dashboard_service.update_profile(name)
    return go("/", "Profile saved")


@router.post("/web/dashboard/{field}")
def update_dashboard(field: str, value: str = Form(...)):
    dashboard_service.update_dashboard(field, value)
    return go("/", f"{field.title()} saved")


@router.get("/web/tasks")
def tasks_page(request: Request):
    return render(request, "tasks.html", view_data.tasks_data())


@router.post("/web/tasks/add")
def add_task(name: str = Form(...)):
    task_service.create_task(name)
    return go("/web/tasks", "Task added")


@router.post("/web/tasks/{task_index}/edit")
def edit_task(task_index: int, name: str = Form(...)):
    task_service.rename_task(task_index, name)
    return go("/web/tasks", "Task renamed")


@router.post("/web/tasks/{task_index}/{action}")
def task_action(task_index: int, action: str):
    task_service.apply_task_action(task_index, action)
    return go("/web/tasks", "Task updated")


@router.get("/web/habits")
def habits_page(request: Request):
    return render(request, "habits.html", view_data.habits_data())


@router.post("/web/habits/add")
def add_habit(name: str = Form(...), category: str = Form("General")):
    habit_service.create_habit(name, category)
    return go("/web/habits", "Habit added")


@router.post("/web/habits/{habit_index}/done")
def habit_done(habit_index: int):
    changed = habit_service.complete_habit(habit_index)
    message = "Habit marked done" if changed else "Habit was already done today"
    return go("/web/habits", message)


@router.get("/web/expenses")
def expenses_page(request: Request):
    return render(request, "expenses.html", view_data.expenses_data())


@router.post("/web/expenses/add")
def add_expense(
    description: str = Form(...),
    amount: float = Form(...),
    currency: str = Form("EUR"),
    direction: str = Form("pay"),
    category: str = Form("Other"),
    exchange_rate_to_eur: float = Form(1.0),
):
    expense_service.create_expense(description, amount, currency, direction, category, exchange_rate_to_eur)
    return go("/web/expenses", "Expense added")


@router.post("/web/expenses/{expense_index}/edit")
def edit_expense(expense_index: int, description: str = Form(...)):
    expense_service.rename_expense(expense_index, description)
    return go("/web/expenses", "Expense renamed")


@router.post("/web/expenses/{expense_index}/{action}")
def expense_action(expense_index: int, action: str):
    expense_service.apply_expense_action(expense_index, action)
    return go("/web/expenses", "Expense updated")
