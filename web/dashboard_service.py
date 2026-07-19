"""Dashboard and profile updates for the AviOS web interface."""

from fastapi import HTTPException

from dashboard_options.state import dashboard_data, save_dashboard_data
from habit_options.state import get_today_date
from profile_options.state import set_user_name


def update_profile(name):
    name = name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")
    set_user_name(name)


def update_dashboard(field, value):
    value = value.strip()
    if field == "focus":
        if not value:
            raise HTTPException(status_code=400, detail="Focus cannot be empty")
        dashboard_data["daily_focus"] = value
    elif field == "note":
        if not value:
            raise HTTPException(status_code=400, detail="Note cannot be empty")
        dashboard_data.setdefault("quick_notes", {})[get_today_date()] = value
    elif field == "mood":
        if value not in {"1", "2", "3", "4", "5"}:
            raise HTTPException(status_code=400, detail="Mood must be 1 to 5")
        dashboard_data.setdefault("mood_checkins", {})[get_today_date()] = int(value)
    else:
        raise HTTPException(status_code=400, detail="Unknown dashboard field")
    save_dashboard_data(dashboard_data)
