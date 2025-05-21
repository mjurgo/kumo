import datetime
import json

from enum import Enum
from typing import Any, Dict, Optional


class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Task:
    def __init__(self, id: int, name: str, due_date: str, priority: Optional[TaskPriority] = None, category: Optional[str] = None):
        self.id = id
        self.name = name
        self.due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
        self.priority = priority
        self.category = category

    @property
    def due_date(self) -> datetime.date:
        return self._due_date

    @due_date.setter
    def due_date(self, value: str):
        if  isinstance(value, str):
            self._due_date = datetime.datetime.strptime(value, "%Y-%m-%d").date()
        else:
            self._due_date = value

    def __str__(self):
        return f"Task #{self.id}: {self.name}, due date: {self.due_date}, priority: {TaskPriority(self.priority).name if self.priority else None}, category: {self.category}"

    def to_dict(self) -> dict:
        result = {
            "id": self.id,
            "name": self.name,
            "dueDate": self.due_date.isoformat(),
        }

        if self.priority is not None:
            result["priority"] = self.priority.value
        if self.category is not None:
            result["category"] = self.category

        return result

    @classmethod
    def from_dict(cls,  data: Dict[str, Any]) -> "Task":
        priority_value = data.get("priority")
        priority = TaskPriority(priority_value) if priority_value is not None else None

        return cls(
            id=data["id"],
            name=data["name"],
            due_date=data["dueDate"],
            priority=priority,
            category=data.get("category")
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
