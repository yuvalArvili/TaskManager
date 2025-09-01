from taskPool import Task
from treap import Treap
from repo import TaskRepo
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
        if s in ("y","yes","1","true","t"):
            return True
        if s in ("n","no","0","false","f"):
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
    print("1) Add/Update task")
    print("2) Delete task")
    print("3) Find task by ID")
    print("4) Toggle approval")
    print("5) Change priority")
    print("6) List tasks by priority")
    print("7) Monthly scheduling")
    print("8) Show last scheduled queue")
    print("9) Exit")

def backlog_sorted(treap):
    tasks = treap.to_list()
    tasks.sort(key=lambda t: (-t.priority, t.duration_days, t.id))
    return tasks

def main():
    repo = TaskRepo()
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
            appr = input_bool("Approved?")
            if repo.get(id_) is not None:
                treap.delete(id_)
            t = Task(id=id_, title=title, priority=pr, duration_days=dur, approved=appr, status="backlog")
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
            id_ = input_int("ID to toggle approval: ")
            t = repo.get(id_)
            if not t:
                print("NOT FOUND")
            else:
                t.approved = not t.approved
                print(f"Approval now: {'Yes' if t.approved else 'No'}")

        elif choice == "5":
            id_ = input_int("ID to change priority: ")
            if repo.get(id_) is None:
                print("NOT FOUND")
            else:
                np = input_int("New priority: ")
                treap.update_priority(id_, np)
                repo.get(id_).priority = np
                print("Updated.")

        elif choice == "6":
            tasks = backlog_sorted(treap)
            print_tasks(tasks, "Tasks by priority")

        elif choice == "7":
            cap = input_int("Monthly capacity (days, default 22): ") or 22
            boost = input_int("Boost for non-scheduled (default 15): ") or 15
            dq, used, left = scheduler.schedule_month(capacity=cap, boost=boost)
            last_queue = list(dq)
            print_tasks(last_queue, "Execution queue for current month")
            print(f"Total days scheduled: {used} | Capacity left: {left}")
            print_tasks(backlog_sorted(treap), "Backlog after scheduling (not scheduled, after boost)")

        elif choice == "8":
            if not last_queue:
                print("No last queue to show.")
            else:
                print_tasks(last_queue, "Last scheduled queue")

        elif choice == "9":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()