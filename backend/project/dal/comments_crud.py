from ..dal.db_context import fetch_all, execute_query
import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'database.db')


async def add_comment(task_id: int, user_id: int, text: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO comments (task_id, user_id, text) VALUES (?, ?, ?)",
            (task_id, user_id, text)
        )
        await db.commit()
        comment_id = cursor.lastrowid
    from ..dal.db_context import fetch_one
    return await fetch_one("SELECT * FROM comments WHERE comment_id = $1", comment_id)


async def get_comments_by_task(task_id: int):
    return await fetch_all("SELECT * FROM comments WHERE task_id = $1", task_id)
