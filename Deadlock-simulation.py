import threading
import time

# Shared resources
balance = [1000, 1000]
locks = [threading.Semaphore(1), threading.Semaphore(1)]

# --- Deadlock version ---
def transfer_deadlock(account_from, account_to, amount):
    print(f"[Deadlock] {threading.current_thread().name} attempting transfer...")
    locks[account_from].acquire()
    print(f"[Deadlock] {threading.current_thread().name} locked account {account_from}")
    time.sleep(1)  # force context switch
    locks[account_to].acquire()
    print(f"[Deadlock] {threading.current_thread().name} locked account {account_to}")

    balance[account_from] -= amount
    balance[account_to] += amount
    print(f"[Deadlock] Transfer complete by {threading.current_thread().name}")

    locks[account_to].release()
    locks[account_from].release()

# --- Fixed version (ordering) ---
def transfer_fixed(account_from, account_to, amount):
    print(f"[Fixed] {threading.current_thread().name} attempting transfer...")
    a = min(account_from, account_to)
    b = max(account_from, account_to)

    locks[a].acquire()
    print(f"[Fixed] {threading.current_thread().name} locked account {a}")
    time.sleep(1)
    locks[b].acquire()
    print(f"[Fixed] {threading.current_thread().name} locked account {b}")

    balance[account_from] -= amount
    balance[account_to] += amount
    print(f"[Fixed] Transfer complete by {threading.current_thread().name}")

    locks[b].release()
    locks[a].release()

# --- Run Deadlock Demo ---
print("\n=== Running Deadlock Demo ===")
t1 = threading.Thread(target=transfer_deadlock, args=(0, 1, 100), name="T1")
t2 = threading.Thread(target=transfer_deadlock, args=(1, 0, 200), name="T2")
t1.start()
t2.start()

# join with timeout so program doesn't hang forever
t1.join(timeout=5)
t2.join(timeout=5)
print("Deadlock demo likely froze here (threads stuck).")

# Reset balances and locks for next run
balance = [1000, 1000]
locks = [threading.Semaphore(1), threading.Semaphore(1)]

# --- Run Fixed Demo ---
print("\n=== Running Fixed Demo ===")
t3 = threading.Thread(target=transfer_fixed, args=(0, 1, 100), name="T3")
t4 = threading.Thread(target=transfer_fixed, args=(1, 0, 200), name="T4")
t3.start()
t4.start()
t3.join()
t4.join()
print("Final balances after fixed demo:", balance)