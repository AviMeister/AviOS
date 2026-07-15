# Daily focus feature for AviOS

from dashboard_options.state import dashboard_data, save_dashboard_data


def get_daily_focus():
    return dashboard_data.get("daily_focus", "")


def set_daily_focus():
    focus = input("\n Today's focus: ").strip()

    if focus == "":
        print("\n Focus was not changed.")
        return

    dashboard_data["daily_focus"] = focus
    save_dashboard_data(dashboard_data)
    print("\n Daily focus saved.")
