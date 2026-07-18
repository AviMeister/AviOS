"""Request models for the AviOS JSON API."""

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    name: str


class HabitCreate(BaseModel):
    name: str
    category: str = "General"


class ExpenseCreate(BaseModel):
    description: str
    amount: float = Field(gt=0)
    currency: str = "EUR"
    direction: str = "pay"
    category: str = "Other"
    exchange_rate_to_eur: float = Field(default=1.0, gt=0)
