import pytest
import os
import tempfile
import shutil
from kumo.task import TaskPriority
from kumo.storage import JsonStorage
from kumo.task_manager import TaskManager


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
def task_manager(json_storage):
    return TaskManager(json_storage)


def test_create_task(task_manager):
    task = task_manager.create_task(
        "Test task",
        "1918-11-11",
        TaskPriority.MEDIUM,
        "test"
    )
    assert task.id == 1
    assert task.name == "Test task"
    assert task.due_date.isoformat() == "1918-11-11"
    assert task.priority == TaskPriority.MEDIUM
    assert task.category == "test"

    retrieved_task = task_manager.get_task(1)
    assert retrieved_task is not None
    assert retrieved_task.id == 1
    assert retrieved_task.name == "Test task"
    assert retrieved_task.due_date.isoformat() == "1918-11-11"
    assert retrieved_task.priority == TaskPriority.MEDIUM
    assert retrieved_task.category == "test"


def test_create_task_without_priority_and_category(task_manager):
    task = task_manager.create_task(
        "Test task",
        "1918-11-11",
    )
    assert task.id == 1
    assert task.name == "Test task"
    assert task.due_date.isoformat() == "1918-11-11"
    assert task.priority is None
    assert task.category is None


def test_get_next_id(task_manager):
    task1 = task_manager.create_task("Test task 1", "1918-11-11")
    task2 = task_manager.create_task("Test task 2", "1918-11-11")

    assert task1.id == 1
    assert task2.id == 2


def test_get_task(task_manager):
    task = task_manager.create_task("Test task", "1918-11-11")
    retrieved_task = task_manager.get_task(task.id)

    assert retrieved_task is not None
    assert retrieved_task.id == task.id
    assert retrieved_task.name == task.name
    assert retrieved_task.due_date.isoformat() == task.due_date.isoformat()
    assert retrieved_task.priority == task.priority
    assert retrieved_task.category == task.category


def test_get_all_tasks(task_manager):
    task_manager.create_task("Test task 1", "1918-11-11")
    task_manager.create_task("Test task 2", "1918-11-11")

    tasks = task_manager.get_all_tasks()
    assert len(tasks) == 2

    names = [task.name for task in tasks]
    assert "Test task 1" in names
    assert "Test task 2" in names


def test_get_tasks(task_manager):
    task_manager.create_task("Test task 1", "1918-11-11", TaskPriority.HIGH, "test")
    task_manager.create_task("Test task 2", "1918-11-11", TaskPriority.MEDIUM, "test")
    task_manager.create_task("Test task 3", "1918-11-11", TaskPriority.MEDIUM, "test 2")

    tasks = task_manager.get_tasks(priority=TaskPriority.MEDIUM.value)
    assert len(tasks) == 2

    names = [task.name for task in tasks]
    assert "Test task 2" in names
    assert "Test task 3" in names

    tasks = task_manager.get_tasks(category="test")
    assert len(tasks) == 2

    names = [task.name for task in tasks]
    assert "Test task 1" in names
    assert "Test task 2" in names


def test_delete_task(task_manager):
    task = task_manager.create_task("Test task", "1918-11-11")

    assert task_manager.get_task(task.id) is not None

    task_manager.delete_task(task.id)

    assert task_manager.get_task(task.id) is None