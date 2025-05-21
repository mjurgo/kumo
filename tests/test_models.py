from kumo.task import Task, TaskPriority


def test_task_init():
    task = Task(
        id=1,
        name="Test task",
        due_date="1918-11-11",
        priority=TaskPriority.MEDIUM,
        category="test")
    assert task.id == 1
    assert task.name == "Test task"
    assert task.due_date.isoformat() == "1918-11-11"
    assert task.priority == TaskPriority.MEDIUM
    assert task.category == "test"


def test_task_init_with_default():
    task = Task(
        id=1,
        name="Test task",
        due_date="1918-11-11",
    )
    assert task.id == 1
    assert task.name == "Test task"
    assert task.due_date.isoformat() == "1918-11-11"
    assert task.priority is None
    assert task.category is None


def test_task_to_dict():
    task = Task(
        id=1,
        name="Test task",
        due_date="1918-11-11",
        priority=TaskPriority.MEDIUM,
        category="test"
    )
    task_dict = task.to_dict()
    assert task_dict["id"] == 1
    assert task_dict["name"] == "Test task"
    assert task_dict["dueDate"] == "1918-11-11"
    assert task_dict["priority"] == TaskPriority.MEDIUM.value
    assert task_dict["category"] == "test"


def test_task_to_dict_without_priority_and_category():
    task = Task(
        id=1,
        name="Test task",
        due_date="1918-11-11",
    )
    task_dict = task.to_dict()
    assert task_dict["id"] == 1
    assert task_dict["name"] == "Test task"
    assert task_dict["dueDate"] == "1918-11-11"
    assert "priority" not in task_dict
    assert "category" not in task_dict


def test_task_from_dict():
    task_dict = {
        "id": 1,
        "name": "Test task",
        "dueDate": "1918-11-11",
        "priority": TaskPriority.MEDIUM,
        "category": "test"
    }
    task = Task.from_dict(task_dict)
    assert task.id == 1
    assert task.name == "Test task"
    assert task.due_date.isoformat() == "1918-11-11"
    assert task.priority == TaskPriority.MEDIUM
    assert task.category == "test"


def test_task_from_dict_without_priority_and_category():
    task_dict = {
        "id": 1,
        "name": "Test task",
        "dueDate": "1918-11-11",
    }
    task = Task.from_dict(task_dict)
    assert task.id == 1
    assert task.name == "Test task"
    assert task.due_date.isoformat() == "1918-11-11"
    assert task.priority is None
    assert task.category is None
