import pytest
import os
import json
import sqlite3
import tempfile
import shutil

from kumo.task import Task, TaskPriority
from kumo.storage import JsonStorage, SqliteStorage


@pytest.fixture
def temp_dir():
    dir_path = tempfile.mkdtemp()
    yield dir_path
    shutil.rmtree(dir_path)


@pytest.fixture
def json_storage(temp_dir):
    json_file = os.path.join(temp_dir, "test_tasks.json")
    return JsonStorage(json_file)


@pytest.fixture
def sqlite_storage(temp_dir):
    db_file = os.path.join(temp_dir, "test_tasks.db")
    return SqliteStorage(db_file)


@pytest.fixture
def populated_json_storage(json_storage):
    task1 = Task(id=1, name="Test task 1", due_date="1918-11-11", priority=TaskPriority.HIGH, category="test")
    task2 = Task(id=2, name="Test task 2", due_date="1918-11-11", priority=TaskPriority.MEDIUM, category="test")
    task3 = Task(id=3, name="Test task 3", due_date="1918-11-11", priority=TaskPriority.MEDIUM, category="test 2")

    json_storage.save_task(task1)
    json_storage.save_task(task2)
    json_storage.save_task(task3)

    return json_storage


def test_json_ensure_file_exists(json_storage, temp_dir):
    json_file = os.path.join(temp_dir, "test_tasks.json")
    assert os.path.exists(json_file)
    with open(json_file, "r") as file:
        content = json.load(file)
    assert content == []


def test_json_save_and_get_task(json_storage):
    task = Task(
        id=1,
        name="Test task",
        due_date="1918-11-11",
        priority=TaskPriority.MEDIUM,
        category="test"
    )
    json_storage.save_task(task)

    retrieved_task = json_storage.get_task(1)
    assert retrieved_task is not None
    assert retrieved_task.id == 1
    assert retrieved_task.name == "Test task"
    assert retrieved_task.due_date.isoformat() == "1918-11-11"
    assert retrieved_task.priority == TaskPriority.MEDIUM
    assert retrieved_task.category == "test"


def test_json_get_nonexistent_task(json_storage):
    retrieved_task = json_storage.get_task(1863)
    assert retrieved_task is None


def test_json_save_and_get_task_without_priority_and_category(json_storage):
    task = Task(
        id=1,
        name="Test task",
        due_date="1918-11-11",
    )
    json_storage.save_task(task)

    retrieved_task = json_storage.get_task(1)
    assert retrieved_task is not None
    assert retrieved_task.id == 1
    assert retrieved_task.name == "Test task"
    assert retrieved_task.due_date.isoformat() == "1918-11-11"
    assert retrieved_task.priority is None
    assert retrieved_task.category is None


def test_json_get_all_tasks(json_storage):
    task1 = Task(id=1, name="Test task 1", due_date="1918-11-11")
    task2 = Task(id=2, name="Test task 2", due_date="1918-11-11")
    json_storage.save_task(task1)
    json_storage.save_task(task2)

    tasks = json_storage.get_all_tasks()
    assert len(tasks) == 2

    task_ids = [task.id for task in tasks]
    assert 1 in task_ids
    assert 2 in task_ids


def test_json_get_tasks_by_priority(populated_json_storage):
    tasks = populated_json_storage.get_tasks(priority=TaskPriority.MEDIUM.value)
    assert len(tasks) == 2
    names = [task.name for task in tasks]
    assert "Test task 2" in names
    assert "Test task 3" in names


def test_json_get_tasks_by_category(populated_json_storage):
    tasks =  populated_json_storage.get_tasks(category="test")
    assert len(tasks) == 2

    names = [task.name for task in tasks]
    assert "Test task 1" in names
    assert "Test task 2" in names


def test_json_update_task(json_storage):
    task = Task(
        id=1,
        name="Test task",
        due_date="1918-11-11",
        priority=TaskPriority.MEDIUM,
        category="test"
    )
    json_storage.save_task(task)

    task.name = "Test task updated"
    task.due_date = "1920-08-25"
    task.priority = TaskPriority.HIGH
    task.category = "updated"
    json_storage.update_task(task)

    updated_task = json_storage.get_task(1)
    assert updated_task.name == "Test task updated"
    assert updated_task.due_date.isoformat() == "1920-08-25"
    assert updated_task.priority == TaskPriority.HIGH
    assert updated_task.category == "updated"


def test_json_delete_task(json_storage):
    task = Task(
        id=1,
        name="Test task",
        due_date="1918-11-11",
        priority=TaskPriority.MEDIUM,
        category="test"
    )
    json_storage.save_task(task)

    assert json_storage.get_task(1) is not None

    json_storage.delete_task(1)

    assert json_storage.get_task(1) is None


def test_json_delete_nonexistent_task(json_storage):
    json_storage.delete_task(1683)


def test_sqlite_initialize_db(sqlite_storage, temp_dir):
    db_file = os.path.join(temp_dir, "test_tasks.db")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
    assert cursor.fetchone() is not None
    conn.close()


def test_sqlite_save_and_get_task(sqlite_storage):
    task = Task(
        id=1,
        name="Test task",
        due_date="1918-11-11",
        priority=TaskPriority.MEDIUM,
        category="test"
    )
    sqlite_storage.save_task(task)

    retrieved_task = sqlite_storage.get_task(1)
    assert retrieved_task is not None
    assert retrieved_task.id == 1
    assert retrieved_task.name == "Test task"
    assert retrieved_task.due_date.isoformat() == "1918-11-11"
    assert retrieved_task.priority == TaskPriority.MEDIUM
    assert retrieved_task.category == "test"


def test_sqlite_get_nonexistent_task(sqlite_storage):
    task = sqlite_storage.get_task(1683)
    assert task is None


def test_sqlite_save_and_get_task_without_priority_and_category(sqlite_storage):
    task = Task(
        id=1,
        name="Test task",
        due_date="1918-11-11"
    )
    sqlite_storage.save_task(task)

    retrieved_task = sqlite_storage.get_task(1)
    assert retrieved_task is not None
    assert retrieved_task.id == 1
    assert retrieved_task.name == "Test task"
    assert retrieved_task.due_date.isoformat() == "1918-11-11"
    assert retrieved_task.priority is None
    assert retrieved_task.category is None


def test_sqlite_get_all_tasks(sqlite_storage):
    task1 = Task(id=1, name="Test task 1", due_date="1918-11-11")
    task2 = Task(id=2, name="Test task 2", due_date="1918-11-11")
    sqlite_storage.save_task(task1)
    sqlite_storage.save_task(task2)

    tasks = sqlite_storage.get_all_tasks()
    assert len(tasks) == 2

    task_ids = [task.id for task in tasks]
    assert 1 in task_ids
    assert 2 in task_ids


def test_sqlite_update_task(sqlite_storage):
    task = Task(
        id=1,
        name="Test task",
        due_date="1918-11-11",
        priority=TaskPriority.MEDIUM,
        category="test"
    )
    sqlite_storage.save_task(task)

    task.name = "Test task updated"
    task.due_date = "1920-08-25"
    task.priority = TaskPriority.HIGH
    task.category = "updated"
    sqlite_storage.update_task(task)

    updated_task = sqlite_storage.get_task(1)
    assert updated_task.name == "Test task updated"
    assert updated_task.due_date.isoformat() == "1920-08-25"
    assert updated_task.priority == TaskPriority.HIGH
    assert updated_task.category == "updated"


def test_sqlite_delete_task(sqlite_storage):
    task = Task(
        id=1,
        name="Test task",
        due_date="1918-11-11",
        priority=TaskPriority.MEDIUM,
        category="test"
    )
    sqlite_storage.save_task(task)

    assert sqlite_storage.get_task(1) is not None

    sqlite_storage.delete_task(1)

    assert sqlite_storage.get_task(1) is None
