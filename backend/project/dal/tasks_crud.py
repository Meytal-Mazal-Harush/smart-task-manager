import aiosqlite
import os
from ..dal.db_context import fetch_all, fetch_one, execute_query

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'database.db')


TASK_QUERY = """SELECT t.*, u.full_name as assigned_name
    FROM tasks t LEFT JOIN users u ON t.assigned_to = u.user_id"""


async def get_all_tasks():
    return await fetch_all(TASK_QUERY)


async def get_task_by_id(task_id: int):
    return await fetch_one(f"{TASK_QUERY} WHERE t.task_id = $1", task_id)


async def get_tasks_by_user(user_id: int):
    return await fetch_all(f"{TASK_QUERY} WHERE t.assigned_to = $1", user_id)


async def get_tasks_by_project(project_id: int):
    return await fetch_all("SELECT * FROM tasks WHERE project_id = $1", project_id)


async def add_task(title: str, description: str, priority: int, due_date, project_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO tasks (title, description, priority, due_date, project_id) VALUES (?, ?, ?, ?, ?)",
            (title, description, priority, due_date, project_id)
        )
        await db.commit()
        task_id = cursor.lastrowid
    return await get_task_by_id(task_id)


async def update_task_fields(task_id: int, update_data: dict):
    # פונקציה חכמה שמעדכנת דינמית רק את השדות שהשתנו
    if not update_data:
        return

    set_clauses = []
    values = []
    for i, (key, value) in enumerate(update_data.items(), start=1):
        set_clauses.append(f"{key} = ${i}")
        values.append(value)

    query = f"UPDATE tasks SET {', '.join(set_clauses)} WHERE task_id = ${len(values) + 1}"
    values.append(task_id)

    await execute_query(query, *values)


async def delete_task(task_id: int):
    await execute_query("DELETE FROM tasks WHERE task_id = $1", task_id)