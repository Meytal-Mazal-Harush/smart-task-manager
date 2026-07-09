from ..dal.db_context import fetch_all, fetch_one, execute_query


async def get_all_projects():
    return await fetch_all("SELECT * FROM projects")


async def get_project_by_id(project_id: int):
    return await fetch_one("SELECT * FROM projects WHERE project_id = $1", project_id)


async def add_project(name: str, description: str = None):
    await execute_query(
        "INSERT INTO projects (name, description) VALUES ($1, $2)",
        name, description
    )
    return await fetch_one("SELECT * FROM projects WHERE name = $1", name)


async def update_project(project_id: int, name: str, description: str = None):
    await execute_query(
        "UPDATE projects SET name = $1, description = $2 WHERE project_id = $3",
        name, description, project_id
    )


async def delete_project(project_id: int):
    await execute_query("DELETE FROM projects WHERE project_id = $1", project_id)
