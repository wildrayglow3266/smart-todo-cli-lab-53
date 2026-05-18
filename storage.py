"""
Storage utilities for task persistence.
"""
import json
from pathlib import Path
from datetime import datetime

DEFAULT_FILE = Path(__file__).parent / "tasks.json"

class TaskStorage:
    def __init__(self, filepath=None):
        self.filepath = Path(filepath) if filepath else DEFAULT_FILE

    def load(self):
        if self.filepath.exists():
            try:
                return json.loads(self.filepath.read_text())
            except json.JSONDecodeError:
                return []
        return []

    def save(self, tasks):
        self.filepath.write_text(json.dumps(tasks, indent=2))

    def add(self, text, priority="normal"):
        tasks = self.load()
        task = {
            "text": text,
            "done": False,
            "priority": priority,
            "created": datetime.now().isoformat(),
        }
        tasks.append(task)
        self.save(tasks)
        return task

    def get_all(self):
        return self.load()

    def mark_done(self, idx):
        tasks = self.load()
        if 1 <= idx <= len(tasks):
            tasks[idx - 1]["done"] = True
            tasks[idx - 1]["completed"] = datetime.now().isoformat()
            self.save(tasks)
            return tasks[idx - 1]
        return None

    def delete(self, idx):
        tasks = self.load()
        if 1 <= idx <= len(tasks):
            removed = tasks.pop(idx - 1)
            self.save(tasks)
            return removed
        return None

    def clear_done(self):
        tasks = self.load()
        remaining = [t for t in tasks if not t["done"]]
        removed_count = len(tasks) - len(remaining)
        self.save(remaining)
        return removed_count
