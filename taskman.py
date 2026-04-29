import json
import sys
from pathlib import Path

DATA_FILE = Path(__file__).parent / "tasks.json"

def load_tasks():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []

def save_tasks(tasks):
    DATA_FILE.write_text(json.dumps(tasks, indent=2))

def add_task(text):
    tasks = load_tasks()
    tasks.append({"text": text, "done": False})
    save_tasks(tasks)
    print(f"Added: {text}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet!")
        return
    for i, task in enumerate(tasks, 1):
        status = "x" if task["done"] else " "
        print(f"[{status}] {i}. {task['text']}")

def mark_done(idx):
    tasks = load_tasks()
    if 1 <= idx <= len(tasks):
        tasks[idx - 1]["done"] = True
        save_tasks(tasks)
        print(f"Done: {tasks[idx - 1]['text']}")
    else:
        print(f"Invalid task number: {idx}")

def delete_task(idx):
    tasks = load_tasks()
    if 1 <= idx <= len(tasks):
        removed = tasks.pop(idx - 1)
        save_tasks(tasks)
        print(f"Deleted: {removed['text']}")
    else:
        print(f"Invalid task number: {idx}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        list_tasks()
    elif sys.argv[1] == "add":
        add_task(" ".join(sys.argv[2:]))
    elif sys.argv[1] == "list":
        list_tasks()
    elif sys.argv[1] == "done":
        mark_done(int(sys.argv[2]))
    elif sys.argv[1] == "delete":
        delete_task(int(sys.argv[2]))
    else:
        print(f"Unknown command: {sys.argv[1]}")
