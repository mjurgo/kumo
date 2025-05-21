import argparse
import sys
from typing import Optional

from kumo.storage import JsonStorage, SqliteStorage, Storage
from kumo.task import TaskPriority
from kumo.task_manager import TaskManager

DEFAULT_STORAGE_TYPE = "json"
STORAGE_TYPES = {
    "json": lambda: JsonStorage("tasks.json"),
    "sqlite": lambda: SqliteStorage("tasks.db")
}
ERROR_ID_REQUIRED = "id option is required for this action"


def get_storage(storage_type: Optional[str] = None) -> Storage:
    if not storage_type or storage_type not in STORAGE_TYPES:
        storage_type = DEFAULT_STORAGE_TYPE
    return STORAGE_TYPES[storage_type]()


def check_required_id(args: argparse.Namespace) -> None:
    if not args.id:
        print(ERROR_ID_REQUIRED)
        sys.exit(1)


def handle_get_task(manager: TaskManager, args: argparse.Namespace) -> None:
    check_required_id(args)
    print(manager.get_task(args.id))


def handle_list_tasks(manager: TaskManager, args: argparse.Namespace) -> None:
    for task in manager.get_tasks(args.category, args.priority):
        print(task)


def handle_add_task(manager: TaskManager, args: argparse.Namespace) -> None:
    priority = TaskPriority(args.priority) if args.priority else None
    manager.create_task(args.name, args.due, priority, args.category)


def handle_delete_task(manager: TaskManager, args: argparse.Namespace) -> None:
    check_required_id(args)
    manager.delete_task(args.id)
    for task in manager.get_tasks():
        print(task)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="action to perform", type=str)
    parser.add_argument("--id", help="task id", type=int)
    parser.add_argument("--name", help="task name", type=str)
    parser.add_argument("--due", help="task due date", type=str)
    parser.add_argument("--category", help="task category", type=str)

    priority_help = f"task priority [1 - {TaskPriority.LOW.name}, 2 - {TaskPriority.MEDIUM.name}, 3 - {TaskPriority.HIGH.name}]"
    parser.add_argument("--priority", help=priority_help, type=int)

    storage_help = f"type of storage to use, available: {list(STORAGE_TYPES.keys())}"
    parser.add_argument("--storage", help=storage_help, type=str)

    args = parser.parse_args()

    storage = get_storage(args.storage)
    manager = TaskManager(storage)

    actions = {
        "get": handle_get_task,
        "list": handle_list_tasks,
        "add": handle_add_task,
        "delete": handle_delete_task
    }

    if args.action in actions:
        actions[args.action](manager, args)
    else:
        print(f"Unknown action: {args.action}")
        print(f"Available actions: {', '.join(actions.keys())}")
        sys.exit(1)


if __name__ == "__main__":
    main()
