"""Save personal and API preferences for the AviOS settings pages."""

import json
from datetime import date
from pathlib import Path

from fastapi import HTTPException, UploadFile

from profile_options.state import profile_data, save_profile


BASE_DIR = Path(__file__).parent.parent
SETTINGS_FILE = BASE_DIR / "settings.json"
ENV_FILE = BASE_DIR / ".env"
UPLOAD_DIR = Path(__file__).parent / "static" / "uploads"
ALLOWED_IMAGES = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}


def load_api_settings():
    defaults = {"provider": "", "model": "", "base_url": ""}
    try:
        with SETTINGS_FILE.open(encoding="utf-8") as file:
            saved = json.load(file)
            return {**defaults, **saved.get("api", {})}
    except (FileNotFoundError, json.JSONDecodeError):
        return defaults


def save_api_settings(provider, model, base_url, api_key):
    data = {
        "api": {
            "provider": provider.strip(),
            "model": model.strip(),
            "base_url": base_url.strip(),
        }
    }
    with SETTINGS_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    if api_key.strip():
        save_secret("AVIOS_API_KEY", api_key.strip())


def save_secret(name, value):
    lines = []
    if ENV_FILE.exists():
        lines = ENV_FILE.read_text(encoding="utf-8").splitlines()
    kept = [line for line in lines if not line.startswith(f"{name}=")]
    kept.append(f"{name}={value}")
    ENV_FILE.write_text("\n".join(kept) + "\n", encoding="utf-8")


def has_api_key():
    if not ENV_FILE.exists():
        return False
    return any(line.startswith("AVIOS_API_KEY=") and line.partition("=")[2] for line in ENV_FILE.read_text(encoding="utf-8").splitlines())


def calculate_age(birthdate):
    if not birthdate:
        return None
    try:
        born = date.fromisoformat(birthdate)
    except ValueError as error:
        raise HTTPException(status_code=400, detail="Invalid birthdate") from error
    today = date.today()
    if born > today:
        raise HTTPException(status_code=400, detail="Birthdate cannot be in the future")
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def update_personal_info(name, birthdate):
    name = name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")
    calculate_age(birthdate)
    profile_data.update({"name": name, "birthdate": birthdate})
    save_profile()


async def save_profile_picture(upload: UploadFile):
    extension = ALLOWED_IMAGES.get(upload.content_type)
    if not extension:
        raise HTTPException(status_code=400, detail="Use a JPG, PNG, or WebP image")
    content = await upload.read(2_000_001)
    if len(content) > 2_000_000:
        raise HTTPException(status_code=400, detail="Picture must be smaller than 2 MB")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"profile{extension}"
    (UPLOAD_DIR / filename).write_bytes(content)
    profile_data["picture"] = f"/static/uploads/{filename}"
    save_profile()


def settings_data(section="personal"):
    birthdate = profile_data.get("birthdate", "")
    return {
        "section": section if section in {"personal", "api"} else "personal",
        "profile": profile_data,
        "age": calculate_age(birthdate),
        "api": load_api_settings(),
        "has_api_key": has_api_key(),
    }
