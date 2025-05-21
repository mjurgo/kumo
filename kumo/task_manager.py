from typing import List, Optional

from kumo.storage import Storage
from kumo.task import Task, TaskPriority


class TaskManager:
    def __init__(self, storage: Storage):
        self.storage = storage
        self._next_id = self._get_next_id()

    def _get_next_id(self) -> int:
        tasks = self.storage.get_all_tasks()
        if not tasks:
            return 1
        return max(task.id for task in tasks) + 1

    def create_task(self, name: str, due_date: str, priority: Optional[TaskPriority] = None, category: Optional[str] = None) -> Task:
        task = Task(id=self._next_id, name=name, due_date=due_date,
                    priority=priority, category=category)
        self.storage.save_task(task)
        self._next_id += 1
        return task

    def get_task(self, id: int) -> Optional[Task]:
        return self.storage.get_task(id)

    def get_all_tasks(self) -> List[Task]:
        return self.storage.get_all_tasks()

    def get_tasks(self, category: Optional[str] = None, priority: Optional[int] = None) -> List[Task]:
        return self.storage.get_tasks(category, priority)

    def delete_task(self, id: int) -> None:
        self.storage.delete_task(id)
