# Shared profile data for AviOS

import json
from pathlib import Path

PROFILE_FILE = Path(__file__).parent.parent / "profile.json"


def load_profile():
    if not PROFILE_FILE.exists():
        return {}

    try:
        with PROFILE_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("\n Could not read saved profile. Starting empty.")
        return {}


def save_profile():
    with PROFILE_FILE.open("w", encoding="utf-8") as file:
        json.dump(profile_data, file, indent=4)


def get_user_name():
    return profile_data.get("name", "")


def set_user_name(name):
    profile_data["name"] = name
    save_profile()


profile_data = load_profile()
