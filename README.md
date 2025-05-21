# Kumo

"Kumo" means "cloud" in Japanese.

A very simple command-line app for managing tasks — built with Python. Add, update, delete, and list tasks directly from your terminal. Tasks are stored in a JSON file or SQLite database, depending on your preference.

## Features
- Simple command-line interface
- Multiple storage backends (JSON and SQLite)
- Task categorization and prioritization
- Clean, modular code design
- Type-checked with mypy
- Test coverage with pytest

## Tech
- Python (3.13)
- `argparse` library
- `mypy`
- `pytest`


## Installation
1. Clone the repository:
```
git clone [https://github.com/mjurgo/kumo.git](https://github.com/mjurgo/kumo.git)
cd kumo
``` 

2. Set up a virtual environment (optional):
```
python -m venv venv
. venv/bin/activate
# On Windows: venv\Scripts\activate
``` 

3. Install dependencies:
```
pip install -r requirements.txt
``` 

## Available Commands
Kumo supports the following actions:
### Add a task
``` 
python main.py add --name <task_name> [--due <due_date>] [--priority <priority>] [--category <category>] [--storage <storage_type>]
```
### Get a task
```
python main.py get --id <task_id> [--storage <storage_type>]
```
### List tasks
``` 
python main.py list [--category <category>] [--priority <priority>] [--storage <storage_type>]
```
### Delete a task
``` 
python main.py delete --id <task_id> [--storage <storage_type>]
```
#### Parameters:
- `--id`: Task ID (required for get and delete actions)
- `--name`: Task name (required for add action)
- `--due`: Task due date
- `--category`: Task category
- `--priority`: Task priority (1 - LOW, 2 - MEDIUM, 3 - HIGH)
- `--storage`: Storage type (available: json, sqlite), default: json
