"""Create and present AviOS's optional dashboard character."""

import base64
from datetime import date

from fastapi import HTTPException
from openai import OpenAI, OpenAIError

from profile_options.state import profile_data, save_profile
from web.settings_service import ENV_FILE, UPLOAD_DIR, load_api_settings


WEEKDAY_MESSAGES = {
    0: "Monday has arrived. We shall meet it after one respectable sip of something warm.",
    1: "Tuesday is Monday wearing a better hat. You have this.",
    2: "Halfway through the week. Very elegant work, honestly.",
    3: "Thursday: close enough to Friday to begin looking mysterious.",
    4: "Friday approves of your persistence and recommends one small victory.",
    5: "Saturday requests fewer obligations and significantly better snacks.",
    6: "Sunday says rest is productive. It is unusually firm about this.",
}


def read_secret(name):
    if not ENV_FILE.exists():
        return ""
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        key, separator, value = line.partition("=")
        if separator and key == name:
            return value.strip()
    return ""


def source_picture_path():
    picture = profile_data.get("picture", "")
    prefix = "/static/uploads/"
    if not picture.startswith(prefix):
        raise HTTPException(status_code=400, detail="Upload a profile picture first")
    path = (UPLOAD_DIR / picture.removeprefix(prefix)).resolve()
    if path.parent != UPLOAD_DIR.resolve() or not path.exists():
        raise HTTPException(status_code=400, detail="Profile picture could not be found")
    return path


def create_dashboard_character():
    api_key = read_secret("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=400, detail="Add an OpenAI API key first")
    settings = load_api_settings()
    model = settings["model"] if settings["model"].startswith("gpt-image") else "gpt-image-2"
    client_options = {"api_key": api_key}
    if settings["base_url"]:
        client_options["base_url"] = settings["base_url"]
    prompt = (
        "Transform the person in this photo into an original, warm, hand-painted Japanese animation "
        "storybook character. Keep their recognizable facial features, expression, hair, and clothing. "
        "Show a friendly waist-up pose, clean silhouette, soft natural colors, gentle ink texture, and "
        "subtle whimsy. No text, no objects covering the face, and no background. Transparent background."
    )
    try:
        with source_picture_path().open("rb") as image:
            result = OpenAI(**client_options).images.edit(
                model=model,
                image=image,
                prompt=prompt,
                background="transparent",
                input_fidelity="high",
                output_format="png",
                quality="low",
                size="1024x1024",
            )
    except OpenAIError as error:
        raise HTTPException(status_code=502, detail="Character generation could not be completed") from error
    encoded = result.data[0].b64_json
    if not encoded:
        raise HTTPException(status_code=502, detail="The image service returned no character")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    output = UPLOAD_DIR / "dashboard_character.png"
    output.write_bytes(base64.b64decode(encoded))
    profile_data["character_picture"] = "/static/uploads/dashboard_character.png"
    save_profile()
    return profile_data["character_picture"]


def character_data():
    return {
        "character_picture": profile_data.get("character_picture", ""),
        "character_message": WEEKDAY_MESSAGES[date.today().weekday()],
    }
