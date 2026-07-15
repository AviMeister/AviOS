# Shared dashboard data for AviOS

import json
from pathlib import Path

DASHBOARD_FILE = Path(__file__).parent.parent / "dashboard.json"


def prepare_dashboard_data(data):
    data.setdefault("daily_focus", "")
    data.setdefault("mood_checkins", {})
    data.setdefault("quick_notes", {})
    data.setdefault("recent_activity", [])

    return data


def load_dashboard_data():
    if not DASHBOARD_FILE.exists():
        return prepare_dashboard_data({})

    try:
        with DASHBOARD_FILE.open("r", encoding="utf-8") as file:
            return prepare_dashboard_data(json.load(file))
    except json.JSONDecodeError:
        return prepare_dashboard_data({})


def save_dashboard_data(data):
    with DASHBOARD_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


dashboard_data = load_dashboard_data()
