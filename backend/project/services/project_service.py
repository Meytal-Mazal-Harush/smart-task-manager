from ..dal import projects_crud
from ..schemas import ProjectCreate, ProjectUpdate
from fastapi import HTTPException, status


async def get_all_projects():
    return await projects_crud.get_all_projects()


async def get_project_by_id(project_id: int):
    project = await projects_crud.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project {project_id} not found")
    return project


async def create_project(project_data: ProjectCreate, current_user: dict):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create projects.")
    return await projects_crud.add_project(project_data.name, project_data.description)


async def update_project(project_id: int, project_data: ProjectUpdate, current_user: dict):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can update projects.")
    await get_project_by_id(project_id)
    await projects_crud.update_project(project_id, project_data.name, project_data.description)
    return await projects_crud.get_project_by_id(project_id)


async def delete_project(project_id: int, current_user: dict):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete projects.")
    await get_project_by_id(project_id)
    await projects_crud.delete_project(project_id)
    return {"message": "Project deleted successfully"}
