import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'database.db')


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'developer'
        )''')
        await db.execute('''CREATE TABLE IF NOT EXISTS projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )''')
        await db.execute('''CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority INTEGER DEFAULT 1,
            due_date TEXT,
            status TEXT DEFAULT 'open',
            approved INTEGER DEFAULT 0,
            project_id INTEGER,
            assigned_to INTEGER
        )''')
        await db.commit()


async def execute_query(query: str, *params):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(query.replace('$1', '?').replace('$2', '?').replace('$3', '?').replace('$4', '?').replace('$5', '?'), params)
        await db.commit()


async def fetch_all(query: str, *params):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(query.replace('$1', '?').replace('$2', '?').replace('$3', '?').replace('$4', '?').replace('$5', '?'), params)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def fetch_one(query: str, *params):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(query.replace('$1', '?').replace('$2', '?').replace('$3', '?').replace('$4', '?').replace('$5', '?'), params)
        row = await cursor.fetchone()
        return dict(row) if row else None
