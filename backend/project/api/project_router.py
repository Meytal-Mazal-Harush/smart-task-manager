from fastapi import APIRouter, Depends, status
from typing import List
from ..schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from ..services import project_service
from ..api.user_router import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/", response_model=List[ProjectResponse])
async def get_all_projects(current_user: dict = Depends(get_current_user)):
    return await project_service.get_all_projects()


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, current_user: dict = Depends(get_current_user)):
    return await project_service.get_project_by_id(project_id)


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project_data: ProjectCreate, current_user: dict = Depends(get_current_user)):
    return await project_service.create_project(project_data, current_user)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, project_data: ProjectUpdate, current_user: dict = Depends(get_current_user)):
    return await project_service.update_project(project_id, project_data, current_user)


@router.delete("/{project_id}")
async def delete_project(project_id: int, current_user: dict = Depends(get_current_user)):
    return await project_service.delete_project(project_id, current_user)
