from dataclasses import dataclass

@dataclass
class Task:
    _counter = 0

    def __init__(self, name, priority, duration_days, approved=True):
        Task.increase_counter()
        self.id = Task.create_id()
        self.title = str(name)
        self.priority = int(priority)
        self.duration_days = int(duration_days)
        self.approved = bool(approved)

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

    def setPriority(self,new_priority):
        if(new_priority is not None):
            self.priority = int(new_priority)
            return True
        return False

    def setDuration(self, new_duration):
        if(new_duration is not None):
            self.duration_days = int(new_duration)
            return True
        return False

    def setAprroval(self, new_status):
        self.approved = bool(new_status)
        return True

    @classmethod
    def create_id(cls):
        return cls._counter

    @classmethod
    def increase_counter(cls):
        cls._counter += 1



    def printTask(self):
        print(f"Task ID: {self.id}\n"
              f"Task Name: {self.title}\n"
              f"Task Priority: {self.priority}\n"
              f"Task Duration: {self.duration_days}\n")


