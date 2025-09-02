from typing import Optional,List
from taskMoudule import Task

class Node:
    __slots__ = ("key","prio","task","left","right")
    def __init__(self, task: Task):
        self.key = task.id
        self.prio = int(task.priority)
        self.task = task
        self.left = None
        self.right = None

class Treap:
    def __init__(self):
        self.root = None
        self._size = 0

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _rotate_right(self, y):
        x = y.left
        y.left = x.right
        x.right = y
        return x

    def _insert(self, node, task: Task):
        if node is None:
            self._size += 1
            return Node(task)
        if task.id < node.key:
            node.left = self._insert(node.left, task)
            if node.left and node.left.prio > node.prio:
                node = self._rotate_right(node)
        elif task.id > node.key:
            node.right = self._insert(node.right, task)
            if node.right and node.right.prio > node.prio:
                node = self._rotate_left(node)
        else:
            node.task = task
            node.prio = task.priority
        return node

    def insert(self, task: Task):
        self.root = self._insert(self.root, task)

    def _find(self, node, key: int):
        if node is None:
            return None
        if key < node.key:
            return self._find(node.left, key)
        if key > node.key:
            return self._find(node.right, key)
        return node

    def find(self, key: int):
        n = self._find(self.root, key)
        return n.task if n else None

    def _delete(self, node, key: int):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                self._size -= 1
                return node.right
            if node.right is None:
                self._size -= 1
                return node.left
            if node.left.prio > node.right.prio:
                node = self._rotate_right(node)
                node.right = self._delete(node.right, key)
            else:
                node = self._rotate_left(node)
                node.left = self._delete(node.left, key)
        return node

    def delete(self, key: int):
        self.root = self._delete(self.root, key)

    def extract_max(self):
        if self.root is None:
            return None
        t = self.root.task
        self.root = self._delete(self.root, self.root.key)
        return t

    def __len__(self):
        return self._size

    def _inorder(self, node, out: List[Task]):
        if not node:
            return
        self._inorder(node.left, out)
        out.append(node.task)
        self._inorder(node.right, out)

    def to_list(self) -> List[Task]:
        out = []
        self._inorder(self.root, out)
        return out

    def update_priority(self, task_id: int, new_priority: int):
        t = self.find(task_id)
        if not t:
            return
        self.delete(task_id)
        t.priority = new_priority
        self.insert(t)

    def increase_priority(self, task_id: int, delta: int):
        t = self.find(task_id)
        if not t:
            return
        self.delete(task_id)
        t.priority += delta
        self.insert(t)

    def list_all_by_priority(self):
        tasks = [t for _, t in self.by_id.values()]
        return sorted(tasks, key=lambda t: (-int(t.priority), int(t.duration_days)))

    def list_all_by_id(self):
        tasks = [t for _, t in self.by_id.values()]
        return sorted(tasks, key=lambda t: int(t.id))