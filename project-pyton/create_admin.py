import asyncio
import sys
sys.path.append('.')

from project.dal import users_crud
from project.services.auth_service import hash_password


async def create_admin():
    existing = await users_crud.get_user_by_email("admin@admin.com")
    if existing:
        print("משתמש כבר קיים!")
        return

    await users_crud.add_user(
        full_name="מנהל",
        email="admin@admin.com",
        password_hash=hash_password("admin123"),
        role="admin"
    )
    print("✅ משתמש נוצר בהצלחה!")
    print("אימייל: admin@admin.com")
    print("סיסמה: admin123")


asyncio.run(create_admin())
