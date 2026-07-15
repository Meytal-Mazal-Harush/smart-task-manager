from fastapi import APIRouter, Depends
from typing import List
from ..schemas import CommentCreate, CommentResponse
from ..dal import comments_crud
from ..api.user_router import get_current_user

router = APIRouter(prefix="/tasks/{task_id}/comments", tags=["Comments"])


@router.get("/", response_model=List[CommentResponse])
async def get_comments(task_id: int, current_user: dict = Depends(get_current_user)):
    return await comments_crud.get_comments_by_task(task_id)


@router.post("/", response_model=CommentResponse)
async def add_comment(task_id: int, comment: CommentCreate, current_user: dict = Depends(get_current_user)):
    return await comments_crud.add_comment(task_id, current_user["user_id"], comment.text)
