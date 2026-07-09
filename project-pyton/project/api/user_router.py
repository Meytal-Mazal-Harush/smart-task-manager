from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..dal import users_crud
from ..services import user_service, auth_service
from ..schemas import UserCreate, UserResponse
from typing import List

router = APIRouter(prefix="/users", tags=["Users & Auth"])
security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_data = auth_service.verify_access_token(token)
    return user_data


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    existing_user = await users_crud.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already registered.")
    user_data.role = "developer"
    await user_service.create_user(user_data)
    return await users_crud.get_user_by_email(user_data.email)


@router.post("/login")
async def login(user_data: UserCreate):
    user = await users_crud.get_user_by_email(user_data.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")
    if not auth_service.verify_password(user_data.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")
    token_payload = {"user_id": user["user_id"], "role": user["role"]}
    access_token = auth_service.create_access_token(data=token_payload)
    return {"access_token": access_token, "token_type": "bearer", "role": user["role"], "full_name": user["full_name"]}


@router.get("/", response_model=List[UserResponse])
async def get_all_users(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only.")
    return await users_crud.get_all_users()


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserCreate, current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only.")
    await users_crud.update_user(user_id, user_data.full_name, user_data.email, user_data.role)
    return await users_crud.get_user_by_id(user_id)


@router.delete("/{user_id}")
async def delete_user(user_id: int, current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only.")
    await users_crud.delete_user(user_id)
    return {"message": "User deleted successfully"}
