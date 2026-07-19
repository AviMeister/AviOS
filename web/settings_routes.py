"""Settings, help, and documentation pages for AviOS."""

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile

from web import character_service, settings_service
from web.page_routes import go, render


router = APIRouter(include_in_schema=False)


@router.get("/web/settings")
def settings_page(request: Request, section: str = "personal"):
    return render(request, "settings.html", settings_service.settings_data(section))


@router.post("/web/settings/personal")
def save_personal(name: str = Form(...), birthdate: str = Form("")):
    settings_service.update_personal_info(name, birthdate)
    return go("/web/settings", "Personal information saved")


@router.post("/web/settings/picture")
async def save_picture(picture: UploadFile = File(...)):
    await settings_service.save_profile_picture(picture)
    return go("/web/settings", "Profile picture saved")


@router.post("/web/settings/character")
def create_character():
    try:
        character_service.create_dashboard_character()
    except HTTPException as error:
        return go("/web/settings", str(error.detail))
    return go("/web/settings", "Dashboard character created")


@router.post("/web/settings/api")
def save_api(
    provider: str = Form(""),
    model: str = Form(""),
    base_url: str = Form(""),
    api_key: str = Form(""),
):
    settings_service.save_api_settings(provider, model, base_url, api_key)
    return go("/web/settings?section=api", "API settings saved")


@router.get("/web/faq")
def faq_page(request: Request):
    return render(request, "faq.html", {})


@router.get("/web/guide")
def guide_page(request: Request):
    return render(request, "guide.html", {})
