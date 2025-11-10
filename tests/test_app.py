from fastapi.testclient import TestClient
import urllib.parse

from src.app import app


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect some known activities from the seed data
    assert "Chess Club" in data


def test_signup_and_remove_participant():
    activity = "Chess Club"
    test_email = "test_student@example.com"

    # Ensure the participant is not already present (if it is, remove it first)
    resp = client.get(f"/activities")
    assert resp.status_code == 200
    activities = resp.json()
    participants = activities[activity]["participants"]
    if test_email in participants:
        # remove existing test email
        resp = client.delete(f"/activities/{urllib.parse.quote(activity)}/participants?email={urllib.parse.quote(test_email)}")
        assert resp.status_code == 200

    # Sign up the test participant
    resp = client.post(f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(test_email)}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify participant appears in GET /activities
    resp = client.get("/activities")
    assert resp.status_code == 200
    activities = resp.json()
    assert test_email in activities[activity]["participants"]

    # Now remove the participant
    resp = client.delete(f"/activities/{urllib.parse.quote(activity)}/participants?email={urllib.parse.quote(test_email)}")
    assert resp.status_code == 200
    assert "Removed" in resp.json().get("message", "")

    # Verify participant removed
    resp = client.get("/activities")
    assert resp.status_code == 200
    activities = resp.json()
    assert test_email not in activities[activity]["participants"]
