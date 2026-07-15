import pytest
import jwt
from datetime import datetime, timezone
from httpx import AsyncClient, ASGITransport
from project.server import app
from project.services.auth_service import (
    create_access_token, verify_access_token, hash_password, verify_password
)

SECRET_KEY = "SUPER_SECRET_KEY_DONT_TELL_ANYONE_12345!"
ALGORITHM = "HS256"


# ==========================================
# טסטים ל-JWT
# ==========================================

def test_create_access_token():
    token = create_access_token({"user_id": 1, "role": "admin"})
    assert isinstance(token, str)
    assert len(token) > 0


def test_verify_access_token_valid():
    token = create_access_token({"user_id": 1, "role": "developer"})
    payload = verify_access_token(token)
    assert payload["user_id"] == 1
    assert payload["role"] == "developer"


def test_verify_access_token_invalid():
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc:
        verify_access_token("invalid.token.here")
    assert exc.value.status_code == 401


def test_verify_access_token_expired():
    from fastapi import HTTPException
    from datetime import timedelta
    expired_token = jwt.encode(
        {"user_id": 1, "role": "admin", "exp": datetime.now(timezone.utc) - timedelta(minutes=1)},
        SECRET_KEY, algorithm=ALGORITHM
    )
    with pytest.raises(HTTPException) as exc:
        verify_access_token(expired_token)
    assert exc.value.status_code == 401


# ==========================================
# טסטים להצפנת סיסמאות
# ==========================================

def test_hash_password():
    hashed = hash_password("mypassword123")
    assert hashed != "mypassword123"
    assert len(hashed) > 0


def test_verify_password_correct():
    hashed = hash_password("mypassword123")
    assert verify_password("mypassword123", hashed) is True


def test_verify_password_wrong():
    hashed = hash_password("mypassword123")
    assert verify_password("wrongpassword", hashed) is False


# ==========================================
# טסטים ל-API (יצירת משימה, עדכון, סינון)
# ==========================================

@pytest.fixture
def admin_token():
    return create_access_token({"user_id": 1, "role": "admin"})


@pytest.fixture
def developer_token():
    return create_access_token({"user_id": 2, "role": "developer"})


@pytest.mark.asyncio
async def test_create_task_as_admin(admin_token):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/tasks/",
            json={"title": "Test Task", "priority": 1, "project_id": 1},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code in [201, 404]
        if response.status_code == 201:
            task_id = response.json()["task_id"]
            await client.delete(f"/tasks/{task_id}", headers={"Authorization": f"Bearer {admin_token}"})


@pytest.mark.asyncio
async def test_create_task_as_developer_forbidden(developer_token):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/tasks/",
            json={"title": "Test Task", "priority": 1, "project_id": 1},
            headers={"Authorization": f"Bearer {developer_token}"}
        )
        assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_tasks_with_filter(admin_token):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/tasks/?status=open",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        tasks = response.json()
        assert all(t["status"] == "open" for t in tasks)


@pytest.mark.asyncio
async def test_get_tasks_filter_by_priority(admin_token):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/tasks/?priority=1",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        tasks = response.json()
        assert all(t["priority"] == 1 for t in tasks)


@pytest.mark.asyncio
async def test_update_task_as_developer_forbidden_fields(developer_token):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.put(
            "/tasks/1",
            json={"title": "New Title"},
            headers={"Authorization": f"Bearer {developer_token}"}
        )
        assert response.status_code in [403, 404]


@pytest.mark.asyncio
async def test_get_tasks_no_token():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/tasks/")
        assert response.status_code == 401
