from taskMoudule import Task
from treap import Treap
from taskDictionary import TaskDictionary
from scheduler import Scheduler


def input_int(msg):
    while True:
        s = input(msg).strip()
        try:
            return int(s)
        except:
            print("Invalid number, try again.")


def input_bool(msg):
    while True:
        s = input(msg + " [y/n]: ").strip().lower()
        if s in ("y", "yes", "1", "true", "t"):
            return True
        if s in ("n", "no", "0", "false", "f"):
            return False
        print("Invalid answer, try again.")


def print_tasks(tasks, title):
    print("\n" + title)
    print("-" * 78)
    print(f"{'ID':>6}  {'Name':<28}  {'Priority':>7}  {'Days':>5}  {'Approved':>8}  {'Status':>10}")
    print("-" * 78)
    for t in tasks:
        appr = "Yes" if t.approved else "No"
        print(f"{t.id:>6}  {t.title[:28]:<28}  {t.priority:>7}  {t.duration_days:>5}  {appr:>8}  {t.status:>10}")
    print("-" * 78)


def menu():
    print("\nTask Manager")
    print("1) Add task")
    print("2) Delete task")
    print("3) Find task by ID")
    print("4) Update task")
    print("5) List tasks by priority")
    print("6) Exit")


def main():
    repo = TaskDictionary()
    treap = Treap()
    scheduler = Scheduler(treap, repo)
    last_queue = []

    while True:
        menu()
        choice = input("Choose option: ").strip()

        if choice == "1":
            id_ = input_int("Enter ID: ")
            title = input("Task name: ").strip()
            pr = input_int("Priority (number): ")
            dur = input_int("Duration in days: ")
            if repo.get(id_) is not None:
                treap.delete(id_)
            t = Task(id=id_, title=title, priority=pr, duration_days=dur, approved=True)
            repo.add(t)
            treap.insert(t)
            print("Saved.")

        elif choice == "2":
            id_ = input_int("ID to delete: ")
            treap.delete(id_)
            repo.remove(id_)
            print("Deleted (if existed).")

        elif choice == "3":
            id_ = input_int("ID to find: ")
            t = repo.get(id_)
            if t:
                print_tasks([t], "Task details")
            else:
                print("NOT FOUND")

        elif choice == "4":


        elif choice == "5":
            print_tasks(tasks, "Tasks by priority")

        elif choice == "6":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()