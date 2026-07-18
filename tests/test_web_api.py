"""Focused tests for the AviOS web layer."""

from fastapi.testclient import TestClient

from web import settings_service, task_service
from web_api import app


client = TestClient(app)


def sample_task(completed=False):
    return {
        "name": "Test task",
        "completed": completed,
        "archived": False,
        "deleted": False,
        "done_history": [],
        "pinned": False,
    }


def test_browser_dashboard_loads():
    response = client.get("/")

    assert response.status_code == 200
    assert "AviOS" in response.text


def test_settings_help_pages_load():
    for path in ["/web/settings", "/web/faq", "/web/guide"]:
        response = client.get(path)
        assert response.status_code == 200


def test_personal_settings_calculate_age(monkeypatch):
    profile = {}
    monkeypatch.setattr(settings_service, "profile_data", profile)
    monkeypatch.setattr(settings_service, "save_profile", lambda: None)

    settings_service.update_personal_info("Avi", "2000-01-01")

    assert profile == {"name": "Avi", "birthdate": "2000-01-01"}
    assert settings_service.calculate_age("2000-01-01") >= 25


def test_api_key_is_not_rendered(monkeypatch):
    monkeypatch.setattr(settings_service, "has_api_key", lambda: True)

    response = client.get("/web/settings?section=api")

    assert response.status_code == 200
    assert "A key is already saved" in response.text
    assert "AVIOS_API_KEY=" not in response.text


def test_missing_task_returns_404(monkeypatch):
    monkeypatch.setattr(task_service, "task_list", [])

    response = client.post("/tasks/99/done")

    assert response.status_code == 404


def test_completing_done_task_does_not_duplicate_history(monkeypatch):
    tasks = [sample_task(completed=True)]
    monkeypatch.setattr(task_service, "task_list", tasks)

    response = client.post("/tasks/0/done")

    assert response.status_code == 200
    assert tasks[0]["done_history"] == []
