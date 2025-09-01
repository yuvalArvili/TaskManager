from dataclasses import dataclass

@dataclass
class Task:
    id: int
    title: str
    priority: int
    duration_days: int
    approved: bool = True
    status: str = "backlog"




