from priority_queue import priorityQueue
from taskMoudule import Task

class _PQItem:
    __slots__ = ("priority","duration_days","task")
    def __init__(self, task, seq):
        self.priority = task.priority
        self.duration_days = (task.duration_days, seq)
        self.task = task

class TaskDictionary:
    def __init__(self, max_days=22):
        self.max_days = max_days
        self.buckets = {i: priorityQueue() for i in range(1, max_days + 1)}
        self.bucket_lists = {i: [] for i in range(1, max_days + 1)}
        self.by_id = {}
        self._seq = {i: 0 for i in range(1, max_days + 1)}

    def _rebuild_bucket(self, d):
        self.buckets[d] = priorityQueue()
        for idx, t in enumerate(self.bucket_lists[d], start=1):
            self.buckets[d].push(_PQItem(t, idx))

    def add(self, task: Task):
        d = int(task.duration_days)
        if d < 1 or d > self.max_days:
            raise ValueError("duration out of range")
        self.bucket_lists[d].append(task)
        self.by_id[task.id] = (d, task)
        self._seq[d] += 1
        self.buckets[d].push(_PQItem(task, self._seq[d]))

    def remove(self, task_id: int):
        info = self.by_id.pop(task_id, None)
        if not info:
            return False
        d, t = info
        lst = self.bucket_lists[d]
        for i, x in enumerate(lst):
            if x is t:
                lst.pop(i)
                break
        self._rebuild_bucket(d)
        return True

    def change_priority(self, task_id: int, new_priority: int):
        info = self.by_id.get(task_id)
        if not info:
            return False
        d, t = info
        t.priority = int(new_priority)
        self._rebuild_bucket(d)
        return True

    def move(self, task_id: int, new_days: int):
        if new_days < 1 or new_days > self.max_days:
            return False
        info = self.by_id.get(task_id)
        if not info:
            return False
        old_d, t = info
        if old_d == new_days:
            return True
        lst = self.bucket_lists[old_d]
        for i, x in enumerate(lst):
            if x is t:
                lst.pop(i)
                break
        self._rebuild_bucket(old_d)
        t.duration_days = int(new_days)
        self.bucket_lists[new_days].append(t)
        self.by_id[task_id] = (new_days, t)
        self._seq[new_days] += 1
        self.buckets[new_days].push(_PQItem(t, self._seq[new_days]))
        return True

    def pop_best(self, days: int):
        if days < 1 or days > self.max_days:
            return None
        w = self.buckets[days].pop()
        if w is None:
            return None
        t = w.task
        lst = self.bucket_lists[days]
        for i, x in enumerate(lst):
            if x is t:
                lst.pop(i)
                break
        self.by_id.pop(t.id, None)
        self._rebuild_bucket(days)
        return t

    def list_day(self, days: int):
        if days < 1 or days > self.max_days:
            return []
        lst = list(self.bucket_lists[days])
        return sorted(lst, key=lambda t: (-t.priority,))

    def list_all(self):
        return {d: self.list_day(d) for d in range(1, self.max_days + 1) if self.bucket_lists[d]}
