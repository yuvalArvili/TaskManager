from collections import deque
from treap import Treap
from taskDictionary import TaskDictionary
from priority_queue import priorityQueue

class Scheduler:
    def __init__(self, treap: Treap, repo: TaskDictionary):
        self.treap = treap
        self.repo = repo

    def schedule_month(self, capacity: int = 22, boost: int = 15):
        snapshot = [t for t in self.treap.to_list() if t.approved]
        pq = priorityQueue()
        pq.build(snapshot)
        selected = []
        load = 0
        while len(pq) and load < capacity:
            t = pq.pop()
            if load + t.duration_days <= capacity:
                selected.append(t)
                load += t.duration_days
        for t in selected:
            self.treap.delete(t.id)
            self.repo.set_status(t.id, "queued")
        leftovers = self.treap.to_list()
        for t in leftovers:
            self.treap.delete(t.id)
            t.priority += boost
            self.treap.insert(t)
        return deque(selected), load, capacity - load