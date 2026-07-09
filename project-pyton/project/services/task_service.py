from ..dal import tasks_crud
from fastapi import HTTPException, status
from typing import Optional


async def get_all_tasks(current_user: dict, status: Optional[str] = None, priority: Optional[int] = None, assigned_to: Optional[int] = None, title: Optional[str] = None):
    tasks = await tasks_crud.get_all_tasks()
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    if priority:
        tasks = [t for t in tasks if t["priority"] == priority]
    if assigned_to:
        tasks = [t for t in tasks if t["assigned_to"] == assigned_to]
    if title:
        tasks = [t for t in tasks if title.lower() in t["title"].lower()]
    return tasks


async def get_my_tasks(current_user: dict):
    user_id = current_user.get("user_id")
    return await tasks_crud.get_tasks_by_user(user_id)


async def get_task_by_id(task_id: int):
    task = await tasks_crud.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


async def create_task(task_data, current_user: dict):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only administrators can create tasks.")
    return await tasks_crud.add_task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        due_date=task_data.due_date,
        project_id=task_data.project_id
    )


async def update_task(task_id: int, update_data, current_user: dict):
    existing_task = await get_task_by_id(task_id)
    user_role = current_user.get("role")
    user_id = current_user.get("user_id")
    updates = update_data.model_dump(exclude_unset=True)

    if user_role == "admin":
        await tasks_crud.update_task_fields(task_id, updates)
        return await get_task_by_id(task_id)

    elif user_role == "developer":
        allowed_updates = {}

        if "status" in updates and updates["status"] == "in_progress":
            if existing_task["assigned_to"] is not None and existing_task["assigned_to"] != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This task is already assigned to another developer.")
            allowed_updates["status"] = "in_progress"
            allowed_updates["assigned_to"] = user_id

        elif "status" in updates and updates["status"] == "closed":
            if existing_task["assigned_to"] != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only close tasks assigned to you.")
            allowed_updates["status"] = "closed"

        for field in ["approved", "title", "description", "priority", "due_date"]:
            if field in updates:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Developers cannot modify '{field}'.")

        if allowed_updates:
            await tasks_crud.update_task_fields(task_id, allowed_updates)
            return await get_task_by_id(task_id)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No valid updates provided.")


async def delete_task(task_id: int, current_user: dict):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only administrators can delete tasks.")
    await get_task_by_id(task_id)
    await tasks_crud.delete_task(task_id)
    return {"message": "Task deleted successfully"}
