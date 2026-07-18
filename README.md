# AviOS

AviOS is my beginner Python project and personal life operating system.

The goal is to learn software engineering by building something useful step by step. Right now AviOS is a terminal app, but the long-term idea is to grow it into a tool for managing tasks, habits, expenses, reminders, and eventually more advanced features.

## Current Features

AviOS opens on a Dashboard. From there you can still reach the classic Tasks, Habits, and Expenses menu.

**Dashboard**
- Shows today's focus, mood, quick note, recent activity, and task streak
- Quick Actions let you add a task, mark a habit done, add an expense, set your focus, check in your mood, or add a note without leaving the dashboard
- Shows an end-of-day review when you exit

**Tasks**
- Add, view, search, edit, delete, archive, and pin tasks
- Complete the same task a lot and AviOS notices, offering to turn it into a habit
- Saved locally in `tasks.json`

**Habits**
- Add a habit, view your progress and streak, mark it done for today
- Saved locally in `habits.json`

**Expenses**
- Add income or expenses in different currencies
- View, search, and see totals per currency plus a combined EUR summary
- Archive or delete entries
- Saved locally in `expenses.json`

**Terminal UI**
- A Textual-based interface for viewing everything and marking tasks/habits done. See the Terminal UI section below.

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

## Terminal UI

AviOS also has a Textual-based terminal UI. You can view your tasks, habits, and expenses, and mark a task or habit done straight from it. Adding new tasks, habits, or expenses, and editing or deleting things, still needs the regular CLI for now — that's coming later.

Run it with:

```powershell
.\venv\Scripts\python.exe avios_tui.py
```

Keys: `t` / `h` / `e` open Tasks / Habits / Expenses from the dashboard.
Arrow keys move between rows. Press Enter on a task or habit to mark it
done. `escape` or `b` goes back, `q` quits. The regular `python main.py`
CLI still works exactly the same as before.

## Code Check

Run Ruff:

```powershell
.\venv\Scripts\python.exe -m ruff check .
```

## Notes

`tasks.json` is ignored by Git because it contains local personal task data.

This project is intentionally small and simple right now. The mission is to understand each part before making it more advanced.
