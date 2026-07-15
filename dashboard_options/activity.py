# Recent activity helpers for AviOS

from dashboard_options.state import dashboard_data, save_dashboard_data
from task_options.state import get_current_timestamp


def add_activity(message):
    dashboard_data.setdefault("recent_activity", [])
    dashboard_data["recent_activity"].insert(
        0,
        {
            "message": message,
            "created_at": get_current_timestamp(),
        },
    )
    dashboard_data["recent_activity"] = dashboard_data["recent_activity"][:5]
    save_dashboard_data(dashboard_data)


def get_recent_activity():
    return dashboard_data.get("recent_activity", [])
