# מוסיפים שתי נקודות בהתחלה כדי לצאת מהתיקייה הנוכחית ולמצוא את dal
from ..dal.db_context import fetch_all, fetch_one, execute_query

async def get_all_users():
    return await fetch_all("SELECT user_id, full_name, email, role FROM users")

async def get_user_by_id(user_id: int):
    return await fetch_one("SELECT user_id, full_name, email, role FROM users WHERE user_id = $1", user_id)

async def get_user_by_email(email: str):
    # פונקציה קריטית עבור שלב ההתחברות (Login) והצפנת הסיסמאות
    return await fetch_one("SELECT * FROM users WHERE email = $1", email)

async def add_user(full_name: str, email: str, password_hash: str, role: str = 'developer'):
    await execute_query(
        "INSERT INTO users (full_name, email, password_hash, role) VALUES ($1, $2, $3, $4)",
        full_name, email, password_hash, role
    )

async def update_user(user_id: int, full_name: str, email: str, role: str):
    await execute_query(
        "UPDATE users SET full_name = $1, email = $2, role = $3 WHERE user_id = $4",
        full_name, email, role, user_id
    )

async def delete_user(user_id: int):
    await execute_query("DELETE FROM users WHERE user_id = $1", user_id)