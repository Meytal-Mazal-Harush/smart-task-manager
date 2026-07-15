from ..dal import users_crud
from ..services.auth_service import hash_password
from fastapi import HTTPException, status
import re

EMAIL_REGEX = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$')
PASSWORD_REGEX = re.compile(r'^.{6,}$')


async def get_all_users():
    return await users_crud.get_all_users()


async def get_user_by_id(user_id: int):
    return await users_crud.get_user_by_id(user_id)


async def create_user(user_data):
    if not EMAIL_REGEX.match(user_data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format.")
    if not PASSWORD_REGEX.match(user_data.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 6 characters.")

    secure_password = hash_password(user_data.password)
    return await users_crud.add_user(
        full_name=user_data.full_name,
        email=user_data.email,
        password_hash=secure_password,
        role=user_data.role
    )