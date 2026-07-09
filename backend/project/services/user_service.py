# במקום from dal import user_crud, שנו ל-
from ..dal import users_crud
# מוסיפים שתי נקודות כדי לצאת מ-dal ולמצוא את services
from ..services.auth_service import hash_password# 🌟 ייבוא פונקציית ההצפנה


async def get_all_users():
    return await users_crud.get_all_users()


async def get_user_by_id(user_id: int):
    return await users_crud.get_user_by_id(user_id)


async def create_user(user_data):
    # 🌟 הצפנת הסיסמה הגולמית לפני שהיא נשלחת לשמירה ב-Supabase!
    secure_password = hash_password(user_data.password)

    return await users_crud.add_user(
        full_name=user_data.full_name,
        email=user_data.email,
        password_hash=secure_password,  # כאן נכנסת הסיסמה המוצפנת
        role=user_data.role
    )