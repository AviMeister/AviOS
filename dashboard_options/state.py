# Shared dashboard data for AviOS

import json
from pathlib import Path

DASHBOARD_FILE = Path(__file__).parent.parent / "dashboard.json"


def load_dashboard_data():
    if not DASHBOARD_FILE.exists():
        return {"daily_focus": ""}

    try:
        with DASHBOARD_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {"daily_focus": ""}


def save_dashboard_data(data):
    with DASHBOARD_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


dashboard_data = load_dashboard_data()
