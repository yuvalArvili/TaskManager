import heapq
from taskMoudule import Task


class priorityQueue:
    def __init__(self):
        self.h = []

    def build(self, tasks):
        self.h = [(-t.priority, t.duration_days, t) for t in tasks]
        heapq.heapify(self.h)

    def push(self, t: Task):
        heapq.heappush(self.h, (-t.priority, t.duration_days, t))

    def pop(self):
        if not self.h:
            return None
        return heapq.heappop(self.h)[2]

    def __len__(self):
        return len(self.h)