from dataclasses import dataclass

@dataclass
class Task:
    _counter = 0

    def __init__(self, name, priority, duration_days, approved=True):
        Task._counter += 1
        self.id = Task._counter
        self.title = str(name)
        self.priority = int(priority)
        self.duration_days = int(duration_days)
        self.approved = bool(approved)

    def printTask(self):
        print(f"Task ID: {self.id}\n"
              f"Task Name: {self.title}\n"
              f"Task Priority: {self.priority}\n"
              f"Task Duration: {self.duration_days}\n")

    def getId(self):
        return self.id

    def getTitle(self):
        return str(self.title)

    def getPriority(self):
        return self.priority

    def getDuration(self):
        return self.duration_days

    def getApproval(self):
        return self.approved

