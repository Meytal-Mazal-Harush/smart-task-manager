from fastapi import APIRouter, Depends, status
from typing import List, Optional
from ..schemas import TaskCreate, TaskUpdate, TaskResponse
from ..services import task_service
from ..api.user_router import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[TaskResponse])
async def read_all_tasks(
    status: Optional[str] = None,
    priority: Optional[int] = None,
    assigned_to: Optional[int] = None,
    title: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    return await task_service.get_all_tasks(current_user, status=status, priority=priority, assigned_to=assigned_to, title=title)


@router.get("/my", response_model=List[TaskResponse])
async def read_my_tasks(current_user: dict = Depends(get_current_user)):
    return await task_service.get_my_tasks(current_user)


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_new_task(task_data: TaskCreate, current_user: dict = Depends(get_current_user)):
    return await task_service.create_task(task_data, current_user)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_existing_task(task_id: int, update_data: TaskUpdate, current_user: dict = Depends(get_current_user)):
    return await task_service.update_task(task_id, update_data, current_user)


@router.delete("/{task_id}")
async def delete_existing_task(task_id: int, current_user: dict = Depends(get_current_user)):
    return await task_service.delete_task(task_id, current_user)
