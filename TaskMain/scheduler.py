from taskDictionary import TaskDictionary
from priority_queue import priorityQueue

class _QItem:
    __slots__ = ("priority","duration_days","task")
    def __init__(self, task, seq):
        self.priority = int(task.priority)
        self.duration_days = (int(task.duration_days), seq)
        self.task = task

class Scheduler:
    def __init__(self, repo: TaskDictionary):
        self.repo = repo

    def _build_pq(self):
        pq = priorityQueue()
        seq = 0
        items = []
        all_map = self.repo.list_all()
        for _, lst in all_map.items():
            for t in lst:
                if getattr(t, "approved", True) and int(t.duration_days) > 0:
                    seq += 1
                    items.append(_QItem(t, seq))
        pq.build(items)
        return pq

    def schedule_month(self, capacity: int = 22, boost: int = 15):
        pq = self._build_pq()
        remaining = int(capacity)
        plan = []
        while len(pq) and remaining > 0:
            w = pq.pop()
            if w is None:
                break
            t = w.task if hasattr(w, "task") else w
            dur = int(t.duration_days)
            if dur <= 0:
                continue
            alloc = dur if dur <= remaining else remaining
            plan.append({"id": t.id, "title": t.title, "allocated_days": alloc, "priority_at_schedule": int(t.priority)})
            if alloc == dur:
                self.repo.remove(t.id)
            else:
                new_days = dur - alloc
                self.repo.move(t.id, new_days)
                self.repo.change_priority(t.id, int(t.priority) + int(boost))
            remaining -= alloc
        used = capacity - remaining
        return plan, used, remaining