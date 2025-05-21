import datetime
import json
import sqlite3
from typing import Any, Dict, List, Optional, Protocol, Union

from kumo.task import Task, TaskPriority


def adapt_datetime_iso(val):
    return val.isoformat()


def convert_datetime(val):
    return datetime.datetime.fromisoformat(val.decode())


class Storage(Protocol):
    def get_task(self, id: int) -> Optional[Task]:
        ...

    def get_all_tasks(self) -> List[Task]:
        ...

    def get_tasks(self, category: Optional[str] = None, priority: Optional[int] = None) -> List[Task]:
        ...

    def save_task(self, task: Task) -> None:
        ...

    def update_task(self, task: Task) -> None:
        ...

    def delete_task(self, id: int) -> None:
        ...


class JsonStorage:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        try:
            with open(self.file_path, "r") as f:
                json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def _read_tasks(self) -> List[Dict[str, Any]]:
        with open(self.file_path, "r") as f:
            return json.load(f)

    def _write_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        with open(self.file_path, "w") as f:
            json.dump(tasks, f, indent=2)

    def get_task(self, id: int) -> Optional[Task]:
        tasks = self._read_tasks()
        for task in tasks:
            if task["id"] == id:
                return Task.from_dict(task)
        return None

    def get_all_tasks(self) -> List[Task]:
        return [Task.from_dict(task) for task in self._read_tasks()]

    def get_tasks(self, category: Optional[str] = None, priority: Optional[int] = None) -> List[Task]:
        return [
            Task.from_dict(task)
            for task in self._read_tasks()
            if (category is None or task.get("category") == category) and
            (priority is None or task.get("priority") == priority)
        ]

    def save_task(self, task: Task) -> None:
        tasks = self._read_tasks()
        tasks.append(task.to_dict())
        self._write_tasks(tasks)

    def update_task(self, task: Task) -> None:
        tasks = self._read_tasks()
        for i, task_data in enumerate(tasks):
            if task_data["id"] == task.id:
                tasks[i] = task.to_dict()
        self._write_tasks(tasks)

    def delete_task(self, id: int) -> None:
        tasks = self._read_tasks()
        tasks = [task for task in tasks if task["id"] != id]
        self._write_tasks(tasks)


class SqliteStorage:
    def __init__(self, db_path: str):
        self.db_path = db_path

        sqlite3.register_adapter(datetime.datetime, adapt_datetime_iso)
        sqlite3.register_converter("datetime", convert_datetime)

        self._initialize_db()

    def _initialize_db(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                due_date TEXT NOT NULL,
                priority INTEGER DEFAULT NULL,
                category TEXT DEFAULT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def get_task(self, id: int) -> Optional[Task]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            priority = TaskPriority(row[3]) if row[3] is not None else None
            return Task(
                id=row[0],
                name=row[1],
                due_date=row[2],
                priority=priority,
                category=row[4]
            )
        return None

    def get_all_tasks(self) -> List[Task]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        conn.close()

        return [
            Task(
                id=row[0],
                name=row[1],
                due_date=row[2],
                priority=row[3],
                category=row[4]
            )
            for row in rows
        ]

    def get_tasks(self, category: Optional[str] = None, priority: Optional[int] = None) -> List[Task]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query = "SELECT * FROM tasks"

        params: List[Union[str, int]] = []
        where = []

        if category is not None:
            where.append("category = ?")
            params.append(category)
        if priority is not None:
            where.append("priority = ?")
            params.append(priority)

        if where:
            query += " WHERE " + " AND ".join(where)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [
            Task(
                id=row[0],
                name=row[1],
                due_date=row[2],
                priority=row[3],
                category=row[4]
            )
            for row in rows
        ]

    def save_task(self, task: Task) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        priority_value = task.priority.value if task.priority else None

        cursor.execute(
            "INSERT INTO tasks (id, name, due_date, priority, category) VALUES (?, ?, ?, ?, ?)",
            (task.id, task.name, task.due_date.isoformat(), priority_value, task.category)
        )
        conn.commit()
        conn.close()

    def update_task(self, task: Task) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        priority_value = task.priority.value if task.priority else None

        cursor.execute(
            "UPDATE tasks SET name = ?, due_date = ?, priority = ?, category = ? WHERE id = ?",
            (task.name, task.due_date.isoformat(), priority_value, task.category, task.id)
        )
        conn.commit()
        conn.close()

    def delete_task(self, id: int) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
        conn.commit()
        conn.close()
