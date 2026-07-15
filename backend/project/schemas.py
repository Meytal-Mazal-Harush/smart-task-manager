from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import date, datetime
from typing import Optional, List

# ==========================================
# 1. סכמות עבור משתמשים (Users)
# ==========================================
class UserBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6) # הסיסמה הגולמית שהמשתמש שולח (נצפין אותה ב-Service)
    role: Optional[str] = "developer" # 'admin' או 'developer'

class UserResponse(UserBase):
    user_id: int
    role: str
    model_config = ConfigDict(from_attributes=True)

# ==========================================
# 2. סכמות עבור פרויקטים (Projects)
# ==========================================
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

# ==========================================
# 3. סכמות עבור משימות (Tasks)
# ==========================================
class TaskBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    description: Optional[str] = None
    priority: int = Field(default=1, ge=1, le=3) # 1=נמוך, 2=בינוני, 3=גבוה
    due_date: Optional[date] = None
    status: str = "open" # 'open', 'in_progress', 'closed'

class TaskCreate(TaskBase):
    project_id: int # חובה לשייך לפרויקט בעת היצירה

class TaskUpdate(BaseModel): # שדות אופציונליים לעדכון משימה
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

# ==========================================
# 4. סכמות עבור הערות (Comments)
# ==========================================
class CommentCreate(BaseModel):
    text: str = Field(..., min_length=1)

class CommentResponse(BaseModel):
    comment_id: int
    task_id: int
    user_id: int
    text: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)