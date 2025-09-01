from taskPool import Task

class TaskRepo:
    def __init__(self):
        self.d = {}
    def add(self, task: Task):
        self.d[task.id] = task

    def get(self, id: int):
        return self.d.get(id)

    def remove(self, id: int):
        self.d.pop(id, None)

    def all(self):
        return list(self.d.values())
    
    def set_status(self, id: int, status: str):
        if id in self.d:
            self.d[id].status = status
