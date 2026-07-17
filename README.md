# AviOS

AviOS is my beginner Python project and personal life operating system.

The goal is to learn software engineering by building something useful step by step. Right now AviOS is a terminal app, but the long-term idea is to grow it into a tool for managing tasks, habits, expenses, reminders, and eventually more advanced features.

## Current Features

- Shows a simple AviOS start screen with the current date and time
- Main menu with Tasks, Habits, Expenses, and Exit
- Tasks menu
- Add tasks
- View tasks
- Mark tasks as done
- Delete tasks
- Save tasks locally in `tasks.json`

## What I Am Learning

- Python files and imports
- Functions
- Lists
- Dictionaries
- Loops
- User input
- Reading and writing JSON files
- Git and GitHub
- Building a project in small steps

## How To Run

From the AviOS folder:

```powershell
.\venv\Scripts\python.exe main.py
```

## Terminal UI (Phase 1 — read-only preview)

AviOS also has an early Textual-based terminal UI. Right now it is
view-only: it shows the same dashboard/task/habit/expense data as the
CLI, but you can't add, edit, or delete anything from it yet — that's
planned for a later phase.

Run it with:

```powershell
.\venv\Scripts\python.exe avios_tui.py
```

Keys: `t` / `h` / `e` open Tasks / Habits / Expenses from the dashboard,
arrow keys move between rows in a list, `escape` or `b` goes back,
`q` quits. The existing `python main.py` CLI is unchanged and still the
primary way to add/edit/delete things.

## Code Check

Run Ruff:

```powershell
.\venv\Scripts\python.exe -m ruff check .
```

## Notes

`tasks.json` is ignored by Git because it contains local personal task data.

This project is intentionally small and simple right now. The mission is to understand each part before making it more advanced.
