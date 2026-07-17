from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import date, datetime
from typing import Optional, List


class UserBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    role: Optional[str] = "developer"

class UserUpdate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    role: str

class UserResponse(UserBase):
    user_id: int
    role: str
    model_config = ConfigDict(from_attributes=True)


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None

class ProjectResponse(ProjectBase):
    project_id: int
    model_config = ConfigDict(from_attributes=True)


class TaskBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    description: Optional[str] = None
    priority: int = Field(default=1, ge=1, le=3)
    due_date: Optional[date] = None
    status: str = "open"

class TaskCreate(TaskBase):
    project_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    due_date: Optional[date] = None
    status: Optional[str] = None
    assigned_to: Optional[int] = None
    approved: Optional[bool] = None

class TaskResponse(TaskBase):
    task_id: int
    approved: bool
    project_id: int
    assigned_to: Optional[int] = None
    assigned_name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class CommentCreate(BaseModel):
    text: str = Field(..., min_length=1)

class CommentResponse(BaseModel):
    comment_id: int
    task_id: int
    user_id: int
    text: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)